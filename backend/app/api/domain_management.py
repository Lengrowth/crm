from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
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


def _raise_domain_error(
    exc: DomainAccessError | DomainNotFoundError | DomainValidationError,
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
    current_user: SaaSUser = Depends(get_current_user),
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
    current_user: SaaSUser = Depends(get_current_user),
):
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
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        # note: tenant_id not enforced here but could be enforced by service
        return service.update_domain(session, domain_id, payload)
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
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return service.manual_activate(session, domain_id, current_user, payload)
    except (DomainAccessError, DomainNotFoundError, DomainValidationError) as exc:
        _raise_domain_error(exc)
