from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.integrations.erpnext_client import ERPNextClient
from app.integrations.erpnext_runtime import get_erpnext_client
from app.models.domain import ProvisioningJob
from app.services.erpnext_service import PersistentERPNextService
from app.services.provisioning_service import provisioning_service


class ProvisioningWorker:
    """Simple synchronous provisioning worker.

    For now this runs in-process and synchronously. It is idempotent-safe for records that are
    already finished.
    """

    def __init__(self, client: Optional[ERPNextClient] = None) -> None:
        self.client = client or get_erpnext_client()
        self.service = PersistentERPNextService(self.client)

    def run(
        self,
        session: Session,
        organization_id: str,
        tenant_id: str,
        site_options: dict[str, Any],
    ) -> str:
        """Create a provisioning record and run provisioning.

        Returns the provisioning record id.
        """
        record = self.service.create_provision_record(
            session, organization_id, tenant_id
        )
        self.service.provision_tenant_persistent(session, record, site_options)
        return record.id


def run_next_job(
    session: Session, client: Optional[ERPNextClient] = None, max_attempts: int = 3
) -> Optional[ProvisioningJob]:
    """Pick the next queued provisioning job and execute it synchronously."""
    job = (
        session.query(ProvisioningJob)
        .filter_by(status="queued")
        .order_by(ProvisioningJob.created_at)
        .with_for_update(read=False)
        .first()
    )
    if not job:
        return None

    service = PersistentERPNextService(client or get_erpnext_client())

    job.attempt_count = (job.attempt_count or 0) + 1
    job = provisioning_service.update_job_status(session, job, "running")
    provisioning_service.append_job_log(
        session, job, {"event": "started", "attempt": job.attempt_count}
    )

    payload: Optional[dict[str, Any]] = None
    if job.logs_json and job.logs_json[0].get("payload"):
        raw_payload = job.logs_json[0].get("payload")
        if isinstance(raw_payload, dict):
            payload = raw_payload

    try:
        organization_id = str(payload.get("organization_id") or "") if payload else ""
        raw_site_options = payload.get("site_options") if payload else {}
        site_options = raw_site_options if isinstance(raw_site_options, dict) else {}

        record = service.create_provision_record(
            session, organization_id, job.tenant_id
        )
        service.provision_tenant_persistent(session, record, site_options)

        provisioning_service.append_job_log(
            session, job, {"event": "provision_success", "provision_id": record.id}
        )
        provisioning_service.update_job_status(session, job, "success")

        try:
            from app.models.domain import Tenant

            tenant = session.get(Tenant, job.tenant_id)
            if tenant:
                tenant.provisioning_status = "ready"
                tenant.status = "ready"
                session.add(tenant)
                session.commit()
                session.refresh(tenant)
        except Exception:
            pass
    except Exception as exc:
        message = str(exc)
        provisioning_service.append_job_log(
            session, job, {"event": "provision_error", "message": message}
        )
        if job.attempt_count >= max_attempts:
            provisioning_service.update_job_status(session, job, "failed", err=message)
        else:
            provisioning_service.append_job_log(
                session,
                job,
                {"event": "retry_scheduled", "next_attempt": job.attempt_count + 1},
            )
            job.status = "queued"
            session.add(job)
            session.commit()
            session.refresh(job)

    return job
