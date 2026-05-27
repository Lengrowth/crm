from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.integrations.erpnext_runtime import (
    ERPNextConfigurationError,
    get_erpnext_client,
    get_erpnext_runtime_summary,
)
from app.models.erpnext import ERPNextIntegrationMetadata, TenantProvisioningRecord
from app.schemas.erpnext import BackupRecord as BackupRecordSchema
from app.schemas.erpnext import OperationResult as OperationResultSchema
from app.schemas.erpnext import ProvisionRequest, ProvisionResponse
from app.schemas.erpnext import SiteStatus as SiteStatusSchema
from app.services.erpnext_service import ERPNextService
from app.workers.provisioning_worker import ProvisioningWorker

router = APIRouter(tags=["integrations"])


def _integration_unavailable(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


def _get_erp_service() -> ERPNextService:
    try:
        return ERPNextService(get_erpnext_client())
    except ERPNextConfigurationError as exc:
        raise _integration_unavailable(str(exc)) from exc


def _string_or_none(value: object) -> str | None:
    return str(value) if value is not None else None


def _as_mapping(value: object) -> Mapping[str, object]:
    return cast(Mapping[str, object], value) if isinstance(value, Mapping) else {}


def _resolve_site_id(
    session: Session, tenant_id: str, site_id: str | None = None
) -> str:
    if site_id:
        return site_id

    metadata = (
        session.query(ERPNextIntegrationMetadata)
        .filter_by(tenant_id=tenant_id)
        .one_or_none()
    )
    if metadata and metadata.site_id:
        return metadata.site_id

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            "site_id query parameter required until this tenant has ERPNext integration "
            "metadata written by provisioning."
        ),
    )


@router.get("/integrations/erpnext/runtime")
def erpnext_runtime() -> dict[str, str]:
    return get_erpnext_runtime_summary()


@router.post(
    "/organizations/{organization_id}/tenants/{tenant_id}/provision",
    status_code=status.HTTP_202_ACCEPTED,
)
def provision_tenant(
    organization_id: str,
    tenant_id: str,
    payload: ProvisionRequest = Body(...),
    session: Session = Depends(get_db_session),
):
    """Create a DB-backed provisioning record and run the current safe worker path."""
    site_options = {
        **(payload.options or {}),
        **{"custom_app": payload.custom_app, "domain": payload.domain},
    }

    try:
        worker = ProvisioningWorker(client=get_erpnext_client())
    except ERPNextConfigurationError as exc:
        raise _integration_unavailable(str(exc)) from exc

    provision_id = worker.run(session, organization_id, tenant_id, site_options)
    return {"id": provision_id}


@router.get("/provisioning/{provision_id}")
def get_provisioning_status(
    provision_id: str, session: Session = Depends(get_db_session)
):
    record = (
        session.query(TenantProvisioningRecord).filter_by(id=provision_id).one_or_none()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="provisioning record not found",
        )

    details = record.details or {}
    create_site_details = _as_mapping(details.get("create_site"))

    return ProvisionResponse(
        id=str(record.id),
        organization_id=str(record.organization_id),
        tenant_id=str(record.tenant_id),
        status=str(record.status),
        started_at=record.started_at.isoformat() if record.started_at else None,
        finished_at=record.finished_at.isoformat() if record.finished_at else None,
        details=details,
        site_id=_string_or_none(create_site_details.get("site_id")),
    )


@router.get("/tenants/{tenant_id}/site-status")
def tenant_site_status(
    tenant_id: str,
    site_id: str | None = None,
    session: Session = Depends(get_db_session),
):
    resolved_site_id = _resolve_site_id(session, tenant_id, site_id)
    status_data = _get_erp_service().get_site_status(resolved_site_id)

    return SiteStatusSchema(
        status=str(status_data.get("status") or "unknown"),
        site_id=_string_or_none(status_data.get("site_id")),
        site_name=_string_or_none(status_data.get("site_name")),
        error=_string_or_none(status_data.get("error")),
    )


@router.post("/tenants/{tenant_id}/backup")
def tenant_backup(
    tenant_id: str,
    site_id: str | None = None,
    session: Session = Depends(get_db_session),
):
    resolved_site_id = _resolve_site_id(session, tenant_id, site_id)
    backup = _get_erp_service().backup_site(resolved_site_id)

    return BackupRecordSchema(
        status=str(backup.get("status") or "unknown"),
        backup_id=_string_or_none(backup.get("backup_id")),
        site_id=_string_or_none(backup.get("site_id")),
    )


@router.post("/tenants/{tenant_id}/restore")
def tenant_restore(
    tenant_id: str,
    backup_id: str = Body(..., embed=True),
    site_id: str | None = None,
    session: Session = Depends(get_db_session),
):
    resolved_site_id = _resolve_site_id(session, tenant_id, site_id)
    result = _get_erp_service().restore_site(resolved_site_id, backup_id)

    return OperationResultSchema(
        status=str(result.get("status") or "unknown"),
        site_id=_string_or_none(result.get("site_id")),
        backup_id=_string_or_none(result.get("backup_id")),
        error=_string_or_none(result.get("error")),
        app=_string_or_none(result.get("app")),
        domain=_string_or_none(result.get("domain")),
    )


@router.post("/tenants/{tenant_id}/bind-domain")
def tenant_bind_domain(
    tenant_id: str,
    domain: str = Body(..., embed=True),
    site_id: str | None = None,
    session: Session = Depends(get_db_session),
):
    resolved_site_id = _resolve_site_id(session, tenant_id, site_id)
    result = _get_erp_service().bind_domain(resolved_site_id, domain)

    return OperationResultSchema(
        status=str(result.get("status") or "unknown"),
        site_id=_string_or_none(result.get("site_id")),
        domain=_string_or_none(result.get("domain")),
        error=_string_or_none(result.get("error")),
        app=_string_or_none(result.get("app")),
        backup_id=_string_or_none(result.get("backup_id")),
    )
