from __future__ import annotations

from collections.abc import Mapping
from typing import NoReturn, Optional, Union, cast

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_accessible_tenant,
    get_current_user,
    require_tenant_write_access,
)
from app.db.session import get_db_session
from app.integrations.erpnext_runtime import (
    ERPNextConfigurationError,
    get_erpnext_client,
    get_erpnext_runtime_summary,
)
from app.models.domain import SaaSUser, Tenant
from app.models.erpnext import ERPNextIntegrationMetadata, TenantProvisioningRecord
from app.schemas.erpnext import BackupRecord as BackupRecordSchema
from app.schemas.erpnext import (
    ERPNextTenantMappingResponse,
    ERPNextTenantMappingUpdateRequest,
    ProvisionRequest,
    ProvisionResponse,
)
from app.schemas.erpnext import OperationResult as OperationResultSchema
from app.schemas.erpnext import SiteStatus as SiteStatusSchema
from app.services.control_plane_service import (
    ControlPlaneAccessError,
    ControlPlaneNotFoundError,
    ControlPlaneService,
    ControlPlaneValidationError,
)
from app.services.erpnext_service import ERPNextService
from app.workers.provisioning_worker import ProvisioningWorker

router = APIRouter(tags=["integrations"])
control_plane_service = ControlPlaneService()


def _integration_unavailable(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


def _raise_control_plane_error(
    exc: Union[ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError],
) -> NoReturn:
    if isinstance(exc, ControlPlaneNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    if isinstance(exc, ControlPlaneValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


def _get_erp_service() -> ERPNextService:
    try:
        return ERPNextService(get_erpnext_client())
    except ERPNextConfigurationError as exc:
        raise _integration_unavailable(str(exc)) from exc


def _string_or_none(value: object) -> Optional[str]:
    return str(value) if value is not None else None


def _as_mapping(value: object) -> Mapping[str, object]:
    return cast(Mapping[str, object], value) if isinstance(value, Mapping) else {}


def _build_tenant_mapping_response(
    tenant: Tenant,
    metadata: Optional[ERPNextIntegrationMetadata],
) -> ERPNextTenantMappingResponse:
    metadata_json = dict(metadata.metadata_json or {}) if metadata else {}
    site_id = metadata.site_id if metadata else None
    site_name = (
        metadata.site_name
        if metadata and metadata.site_name
        else tenant.erpnext_site_name
    )
    base_url = (
        metadata.base_url if metadata and metadata.base_url else tenant.erpnext_base_url
    )
    configured = any(
        [
            site_id,
            site_name,
            base_url,
            tenant.erpnext_api_key_ref,
            tenant.erpnext_api_secret_ref,
        ]
    )

    return ERPNextTenantMappingResponse(
        tenant_id=tenant.id,
        organization_id=tenant.organization_id,
        configured=bool(configured),
        site_id=site_id,
        site_name=site_name,
        base_url=base_url,
        api_key_ref=tenant.erpnext_api_key_ref,
        api_secret_ref=tenant.erpnext_api_secret_ref,
        provisioning_status=tenant.provisioning_status,
        tenant_status=tenant.status,
        metadata=metadata_json,
    )


def _resolve_site_id(
    session: Session, tenant_id: str, site_id: Optional[str] = None
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
            "metadata written by provisioning or manual cutover mapping."
        ),
    )


@router.get("/integrations/erpnext/runtime")
def erpnext_runtime() -> dict[str, str]:
    return get_erpnext_runtime_summary()


@router.get(
    "/tenants/{tenant_id}/integration/erpnext",
    response_model=ERPNextTenantMappingResponse,
)
def get_tenant_erpnext_mapping(
    tenant_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        tenant = control_plane_service.get_tenant(session, current_user, tenant_id)
    except (
        ControlPlaneAccessError,
        ControlPlaneNotFoundError,
        ControlPlaneValidationError,
    ) as exc:
        _raise_control_plane_error(exc)

    metadata = (
        session.query(ERPNextIntegrationMetadata)
        .filter_by(tenant_id=tenant.id)
        .one_or_none()
    )
    return _build_tenant_mapping_response(tenant, metadata)


@router.put(
    "/tenants/{tenant_id}/integration/erpnext",
    response_model=ERPNextTenantMappingResponse,
)
def upsert_tenant_erpnext_mapping(
    tenant_id: str,
    payload: ERPNextTenantMappingUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        tenant = control_plane_service.get_tenant(session, current_user, tenant_id)
        control_plane_service._ensure_organization_write_access(
            session, current_user, tenant.organization_id
        )
    except (
        ControlPlaneAccessError,
        ControlPlaneNotFoundError,
        ControlPlaneValidationError,
    ) as exc:
        _raise_control_plane_error(exc)

    metadata = (
        session.query(ERPNextIntegrationMetadata)
        .filter_by(tenant_id=tenant.id)
        .one_or_none()
    )
    if metadata is None:
        metadata = ERPNextIntegrationMetadata(
            tenant_id=tenant.id,
            site_id=payload.site_id,
            site_name=payload.site_name,
            base_url=payload.base_url,
            metadata_json={},
        )

    provided_fields = payload.model_fields_set
    metadata.site_id = payload.site_id

    if "site_name" in provided_fields:
        metadata.site_name = payload.site_name
    elif not metadata.site_name and tenant.erpnext_site_name:
        metadata.site_name = tenant.erpnext_site_name

    if "base_url" in provided_fields:
        metadata.base_url = payload.base_url
    elif not metadata.base_url and tenant.erpnext_base_url:
        metadata.base_url = tenant.erpnext_base_url

    merged_metadata = dict(metadata.metadata_json or {})
    merged_metadata.update(payload.metadata or {})
    merged_metadata["mapping_source"] = "phase_18_manual_cutover"
    metadata.metadata_json = merged_metadata

    tenant.erpnext_site_name = metadata.site_name or tenant.erpnext_site_name
    tenant.erpnext_base_url = metadata.base_url or tenant.erpnext_base_url
    tenant.provisioning_status = (
        payload.provisioning_status or tenant.provisioning_status
    )
    tenant.status = payload.tenant_status or tenant.status

    if "api_key_ref" in provided_fields:
        tenant.erpnext_api_key_ref = payload.api_key_ref
    if "api_secret_ref" in provided_fields:
        tenant.erpnext_api_secret_ref = payload.api_secret_ref

    session.add(metadata)
    session.add(tenant)
    session.commit()
    session.refresh(tenant)
    session.refresh(metadata)

    return _build_tenant_mapping_response(tenant, metadata)


@router.post(
    "/organizations/{organization_id}/tenants/{tenant_id}/provision",
    status_code=status.HTTP_202_ACCEPTED,
)
def provision_tenant(
    organization_id: str,
    tenant_id: str,
    payload: ProvisionRequest = Body(...),
    session: Session = Depends(get_db_session),
    tenant: Tenant = Depends(require_tenant_write_access),
):
    """Create a DB-backed provisioning record and run the current safe worker path."""
    if tenant.organization_id != organization_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tenant not found")

    site_options = {
        **(payload.options or {}),
        **{"custom_app": payload.custom_app, "domain": payload.domain},
    }

    try:
        worker = ProvisioningWorker(client=get_erpnext_client())
    except ERPNextConfigurationError as exc:
        raise _integration_unavailable(str(exc)) from exc

    provision_id = worker.run(session, tenant.organization_id, tenant.id, site_options)
    return {"id": provision_id}


@router.get("/provisioning/{provision_id}")
def get_provisioning_status(
    provision_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    record = (
        session.query(TenantProvisioningRecord).filter_by(id=provision_id).one_or_none()
    )
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="provisioning record not found",
        )

    try:
        control_plane_service.get_tenant(session, current_user, str(record.tenant_id))
    except (ControlPlaneAccessError, ControlPlaneNotFoundError) as exc:
        _raise_control_plane_error(exc)

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
    site_id: Optional[str] = None,
    session: Session = Depends(get_db_session),
    _: Tenant = Depends(get_accessible_tenant),
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
    site_id: Optional[str] = None,
    session: Session = Depends(get_db_session),
    _: Tenant = Depends(require_tenant_write_access),
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
    site_id: Optional[str] = None,
    session: Session = Depends(get_db_session),
    _: Tenant = Depends(require_tenant_write_access),
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
    site_id: Optional[str] = None,
    session: Session = Depends(get_db_session),
    _: Tenant = Depends(require_tenant_write_access),
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
