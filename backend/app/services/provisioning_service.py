from __future__ import annotations

import re
import secrets
from datetime import timedelta
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import and_, or_, select, update
from sqlalchemy.orm import Session

from app.models.domain import ProvisioningEvent, ProvisioningJob, ProvisioningStep, utcnow


SAFE_PAYLOAD_KEYS = {"organization_id", "site_options", "domain", "custom_app", "environment", "failure_inject_step"}
SECRET_KEY_RE = re.compile(r"(password|secret|token|api[_-]?key|private[_-]?key|authorization|credential)", re.I)


def sanitize_value(value: Any, *, depth: int = 0) -> Any:
    if depth > 4:
        return "[truncated]"
    if isinstance(value, dict):
        return {str(key): ("[REDACTED]" if SECRET_KEY_RE.search(str(key)) else sanitize_value(item, depth=depth + 1)) for key, item in list(value.items())[:40]}
    if isinstance(value, (list, tuple)):
        return [sanitize_value(item, depth=depth + 1) for item in list(value)[:40]]
    if isinstance(value, (str, int, float, bool)) or value is None:
        text = str(value)
        if len(text) > 500:
            return text[:500] + "…"
        return value
    return str(value)[:500]


class ProvisioningService:
    """Durable job repository with compare-and-set lease acquisition."""

    def queue_provisioning_job(self, session: Session, tenant_id: str, job_type: str, requested_by_user_id: Optional[str] = None, payload: Optional[dict[str, Any]] = None) -> ProvisioningJob:
        if job_type not in {"initial_provision", "provision_tenant", "legacy_compatibility"}:
            raise ValueError("Unsupported provisioning job type.")
        now = utcnow()
        safe_payload = {key: sanitize_value(value) for key, value in (payload or {}).items() if key in SAFE_PAYLOAD_KEYS}
        rec = ProvisioningJob(tenant_id=tenant_id, job_type=job_type, status="queued", requested_by_user_id=requested_by_user_id, attempt_count=0, max_attempts=3, next_attempt_at=now, external_refs_json={"legacy_payload": safe_payload}, logs_json=[{"ts": now.isoformat(), "event": "queued", "message": "Legacy compatibility job queued."}])
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec

    def get_job(self, session: Session, job_id: str) -> Optional[ProvisioningJob]:
        return session.get(ProvisioningJob, job_id)

    def list_jobs_for_tenant(self, session: Session, tenant_id: str) -> list[ProvisioningJob]:
        return session.execute(select(ProvisioningJob).where(ProvisioningJob.tenant_id == tenant_id).order_by(ProvisioningJob.created_at)).scalars().all()

    def append_job_log(self, session: Session, job: ProvisioningJob, entry: dict[str, Any]) -> ProvisioningJob:
        safe = sanitize_value(entry)
        if not isinstance(safe, dict):
            safe = {"event": "worker_event", "message": str(safe)}
        safe.setdefault("ts", utcnow().isoformat())
        logs = list(job.logs_json or [])
        logs.append(safe)
        job.logs_json = logs[-100:]
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def update_job_status(self, session: Session, job: ProvisioningJob, status: str, err: Optional[str] = None) -> ProvisioningJob:
        if status not in {"awaiting_execution_authorization", "queued", "running", "validation", "success", "failed", "cancelled"}:
            raise ValueError("Invalid provisioning job status.")
        job.status = status
        if status == "running":
            job.started_at = job.started_at or utcnow()
        if status in {"failed", "success", "cancelled"}:
            job.finished_at = utcnow()
            job.lease_expires_at = None
            job.worker_id = None
            job.lease_token = None
        if err:
            job.error_message = sanitize_value(err)
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def claim_next_job(self, session: Session, worker_id: str, lease_seconds: int = 120) -> Optional[ProvisioningJob]:
        now = utcnow()
        queued = and_(
            ProvisioningJob.status == "queued",
            or_(ProvisioningJob.next_attempt_at.is_(None), ProvisioningJob.next_attempt_at <= now),
        )
        expired = and_(
            ProvisioningJob.status.in_(("running", "validation")),
            ProvisioningJob.lease_expires_at.is_not(None),
            ProvisioningJob.lease_expires_at <= now,
        )
        candidate = session.execute(
            select(ProvisioningJob)
            .where(or_(queued, expired))
            .order_by(ProvisioningJob.created_at)
            .limit(1)
        ).scalar_one_or_none()
        if candidate is None:
            return None
        lease_until = now + timedelta(seconds=max(15, lease_seconds))
        lease_token = secrets.token_urlsafe(32)
        if candidate.status in {"running", "validation"}:
            stale_worker_id = candidate.worker_id
            reclaimed = session.execute(
                update(ProvisioningJob)
                .execution_options(synchronize_session=False)
                .where(
                    ProvisioningJob.id == candidate.id,
                    ProvisioningJob.status.in_(("running", "validation")),
                    ProvisioningJob.lease_expires_at <= now,
                )
                .values(
                    status="queued",
                    worker_id=None,
                    lease_token=None,
                    lease_expires_at=None,
                    heartbeat_at=None,
                    next_attempt_at=now,
                    error_message="Worker lease expired; the durable job was reclaimed.",
                )
            )
            if reclaimed.rowcount != 1:
                session.rollback()
                return None
            session.execute(
                update(ProvisioningStep)
                .execution_options(synchronize_session=False)
                .where(
                    ProvisioningStep.job_id == candidate.id,
                    ProvisioningStep.status == "running",
                    ProvisioningStep.worker_id == stale_worker_id,
                )
                .values(status="queued", worker_id=None, lease_expires_at=None, next_attempt_at=now)
            )
        result = session.execute(
            update(ProvisioningJob)
            .execution_options(synchronize_session=False)
            .where(
                ProvisioningJob.id == candidate.id,
                ProvisioningJob.status == "queued",
                or_(ProvisioningJob.next_attempt_at.is_(None), ProvisioningJob.next_attempt_at <= now),
            )
            .values(
                status="running",
                worker_id=worker_id,
                lease_token=lease_token,
                lease_expires_at=lease_until,
                heartbeat_at=now,
                started_at=candidate.started_at or now,
                attempt_count=ProvisioningJob.attempt_count + 1,
            )
        )
        if result.rowcount != 1:
            session.rollback()
            return None
        session.commit()
        return session.get(ProvisioningJob, candidate.id)

    def renew_lease(self, session: Session, job_id: str, worker_id: str, lease_seconds: int = 120, lease_token: Optional[str] = None) -> bool:
        now = utcnow()
        conditions = [
            ProvisioningJob.id == job_id,
            ProvisioningJob.status.in_(("running", "validation")),
            ProvisioningJob.worker_id == worker_id,
            ProvisioningJob.lease_expires_at > now,
        ]
        if lease_token is not None:
            conditions.append(ProvisioningJob.lease_token == lease_token)
        result = session.execute(
            update(ProvisioningJob)
            .execution_options(synchronize_session=False)
            .where(*conditions)
            .values(heartbeat_at=now, lease_expires_at=now + timedelta(seconds=max(15, lease_seconds)))
        )
        session.commit()
        return result.rowcount == 1

    def assert_lease(self, session: Session, job_id: str, worker_id: str, lease_token: Optional[str]) -> None:
        now = utcnow()
        job = session.execute(
            select(ProvisioningJob).where(
                ProvisioningJob.id == job_id,
                ProvisioningJob.status.in_(("running", "validation")),
                ProvisioningJob.worker_id == worker_id,
                ProvisioningJob.lease_token == lease_token,
                ProvisioningJob.lease_expires_at > now,
            )
        ).scalar_one_or_none()
        if job is None:
            raise RuntimeError("The provisioning worker lease was lost; external work will be reconciled on retry.")

    def release_for_retry(self, session: Session, job: ProvisioningJob, worker_id: str, delay_seconds: int, message: str) -> ProvisioningJob:
        if job.worker_id != worker_id:
            raise ValueError("Worker lease is not owned by this worker.")
        job.status = "queued"
        job.worker_id = None
        job.lease_expires_at = None
        job.next_attempt_at = utcnow() + timedelta(seconds=max(0, delay_seconds))
        self._append_without_commit(job, {"event": "retry_scheduled", "message": message, "next_attempt_at": job.next_attempt_at.isoformat()})
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def add_event(self, session: Session, step: ProvisioningStep, job_id: str, event_code: str, public_message: str, context: Optional[dict[str, Any]] = None) -> ProvisioningEvent:
        event = ProvisioningEvent(step_id=step.id, job_id=job_id, attempt=step.attempt_count, event_code=event_code[:64], public_message=public_message[:500], context_json=sanitize_value(context or {}))
        session.add(event)
        session.flush()
        return event

    def _append_without_commit(self, job: ProvisioningJob, entry: dict[str, Any]) -> None:
        safe = sanitize_value(entry)
        if isinstance(safe, dict):
            safe.setdefault("ts", utcnow().isoformat())
        logs = list(job.logs_json or [])
        logs.append(safe if isinstance(safe, dict) else {"event": "worker_event", "message": str(safe)})
        job.logs_json = logs[-100:]


provisioning_service = ProvisioningService()
