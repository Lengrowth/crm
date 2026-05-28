from __future__ import annotations

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_accessible_tenant, get_current_user, require_tenant_write_access
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.provisioning import ProvisioningJobCreate, ProvisioningJobRead
from app.services.provisioning_service import provisioning_service
from app.services.control_plane_service import ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneService

router = APIRouter(tags=["provisioning"])
control_plane_service = ControlPlaneService()


def _raise_control_plane_error(
    exc: Union[ControlPlaneAccessError, ControlPlaneNotFoundError]
) -> None:
    if isinstance(exc, ControlPlaneNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.post(
    "/tenants/{tenant_id}/provisioning_jobs",
    response_model=ProvisioningJobRead,
    status_code=status.HTTP_201_CREATED,
)
def create_provisioning_job(
    tenant_id: str,
    payload: ProvisioningJobCreate,
    session: Session = Depends(get_db_session),
    _: object = Depends(require_tenant_write_access),
    current_user: SaaSUser = Depends(get_current_user),
):
    rec = provisioning_service.queue_provisioning_job(
        session,
        tenant_id=tenant_id,
        job_type=payload.job_type,
        requested_by_user_id=current_user.id if current_user else None,
        payload=payload.payload,
    )
    return rec


@router.get(
    "/tenants/{tenant_id}/provisioning_jobs", response_model=list[ProvisioningJobRead]
)
def list_provisioning_jobs(
    tenant_id: str,
    session: Session = Depends(get_db_session),
    _: object = Depends(get_accessible_tenant),
):
    return provisioning_service.list_jobs_for_tenant(session, tenant_id)


@router.get("/provisioning_jobs/{job_id}", response_model=ProvisioningJobRead)
def get_provisioning_job(
    job_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    rec = provisioning_service.get_job(session, job_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="job not found"
        )
    try:
        control_plane_service.get_tenant(session, current_user, rec.tenant_id)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError) as exc:
        _raise_control_plane_error(exc)
    return rec
