from __future__ import annotations

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.dependencies import (
    get_accessible_tenant,
    get_current_user,
    require_tenant_write_access,
)
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.domain_management import (
    DomainCreateRequest,
    DomainOut,
    DomainUpdateRequest,
    ManualActivationRequest,
)
from app.services.domain_service import (
    DomainAccessError,
    DomainNotFoundError,
    DomainService,
    DomainValidationError,
)

router = APIRouter(tags=["domains"])
service = DomainService()


def _require_legacy_domain_mutation() -> None:
    if not settings.feature_flag_map.get("legacy_domain_mutations", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Direct domain mutation is disabled. Use an approved onboarding workflow.",
        )


def _raise_domain_error(
    exc: Union[DomainAccessError, DomainNotFoundError, DomainValidationError],
) -> None:
    if isinstance(exc, DomainNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    if isinstance(exc, DomainValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.get("/tenants/{tenant_id}/domains", response_model=list[DomainOut])
def list_domains(
    tenant_id: str,
    session: Session = Depends(get_db_session),
    _: object = Depends(get_accessible_tenant),
):
    return service.list_domains(session, tenant_id)


@router.post(
    "/tenants/{tenant_id}/domains",
    response_model=DomainOut,
    status_code=status.HTTP_201_CREATED,
)
def create_domain(
    tenant_id: str,
    payload: DomainCreateRequest,
    session: Session = Depends(get_db_session),
    _: object = Depends(require_tenant_write_access),
):
    _require_legacy_domain_mutation()
    try:
        return service.create_domain(session, tenant_id, payload)
    except (DomainAccessError, DomainNotFoundError, DomainValidationError) as exc:
        _raise_domain_error(exc)


@router.patch("/tenants/{tenant_id}/domains/{domain_id}", response_model=DomainOut)
def update_domain(
    tenant_id: str,
    domain_id: str,
    payload: DomainUpdateRequest,
    session: Session = Depends(get_db_session),
    _: object = Depends(require_tenant_write_access),
):
    _require_legacy_domain_mutation()
    try:
        return service.update_domain(session, tenant_id, domain_id, payload)
    except (DomainAccessError, DomainNotFoundError, DomainValidationError) as exc:
        _raise_domain_error(exc)


@router.post(
    "/tenants/{tenant_id}/domains/{domain_id}/manual_activate", response_model=DomainOut
)
def manual_activate(
    tenant_id: str,
    domain_id: str,
    payload: ManualActivationRequest,
    session: Session = Depends(get_db_session),
    _: object = Depends(require_tenant_write_access),
    current_user: SaaSUser = Depends(get_current_user),
):
    _require_legacy_domain_mutation()
    try:
        return service.manual_activate(session, tenant_id, domain_id, current_user, payload)
    except (DomainAccessError, DomainNotFoundError, DomainValidationError) as exc:
        _raise_domain_error(exc)
