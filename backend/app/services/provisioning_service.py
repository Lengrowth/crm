from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.domain import ProvisioningJob, utcnow


class ProvisioningService:
    """Service for creating and inspecting ProvisioningJob records.

    This keeps things simple for Phase 12: jobs are stored in the `provisioning_jobs`
    table and carry a `logs_json` array for structured logs and a `payload` stored as
    the first log entry under key `payload`.
    """

    def queue_provisioning_job(
        self,
        session: Session,
        tenant_id: str,
        job_type: str,
        requested_by_user_id: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> ProvisioningJob:
        now = utcnow()
        initial_log: dict[str, Any] = {
            "ts": now.isoformat(),
            "event": "queued",
        }
        if payload is not None:
            initial_log["payload"] = payload

        rec = ProvisioningJob(
            tenant_id=tenant_id,
            job_type=job_type,
            status="queued",
            requested_by_user_id=requested_by_user_id,
            attempt_count=0,
            logs_json=[initial_log],
        )
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec

    def get_job(self, session: Session, job_id: str) -> Optional[ProvisioningJob]:
        return session.query(ProvisioningJob).filter_by(id=job_id).one_or_none()

    def list_jobs_for_tenant(
        self, session: Session, tenant_id: str
    ) -> list[ProvisioningJob]:
        return (
            session.query(ProvisioningJob)
            .filter_by(tenant_id=tenant_id)
            .order_by(ProvisioningJob.created_at)
            .all()
        )

    def append_job_log(
        self, session: Session, job: ProvisioningJob, entry: dict[str, Any]
    ) -> ProvisioningJob:
        # ensure timestamp
        if "ts" not in entry:
            entry["ts"] = datetime.utcnow().isoformat()
        logs = list(job.logs_json or [])
        logs.append(entry)
        job.logs_json = logs
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def update_job_status(
        self,
        session: Session,
        job: ProvisioningJob,
        status: str,
        err: Optional[str] = None,
    ) -> ProvisioningJob:
        job.status = status
        if status == "running":
            job.started_at = utcnow()
        if status in ("failed", "success"):
            job.finished_at = utcnow()
        if err:
            job.error_message = err
        session.add(job)
        session.commit()
        session.refresh(job)
        return job


provisioning_service = ProvisioningService()
