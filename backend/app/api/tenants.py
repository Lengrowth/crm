from __future__ import annotations

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.control import TenantCreateRequest, TenantLifecycleActionRequest, TenantUpdateRequest
from app.schemas.domain import TenantRead
from app.services.control_plane_service import (
    ControlPlaneAccessError,
    ControlPlaneNotFoundError,
    ControlPlaneService,
    ControlPlaneValidationError,
)

router = APIRouter(tags=["tenants"])
control_plane_service = ControlPlaneService()


def _raise_control_plane_error(
    exc: Union[ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError]
) -> None:
    if isinstance(exc, ControlPlaneNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, ControlPlaneValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.get("/tenants", response_model=list[TenantRead])
def list_tenants(
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    return control_plane_service.list_tenants(session, current_user)


@router.post("/tenants", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def create_tenant(
    payload: TenantCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.create_tenant(session, current_user, payload)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.get("/tenants/{tenant_id}", response_model=TenantRead)
def get_tenant(
    tenant_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.get_tenant(session, current_user, tenant_id)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.patch("/tenants/{tenant_id}", response_model=TenantRead)
def update_tenant(
    tenant_id: str,
    payload: TenantUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.update_tenant(session, current_user, tenant_id, payload)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.post("/tenants/{tenant_id}/suspend", response_model=TenantRead)
def suspend_tenant(
    tenant_id: str,
    payload: TenantLifecycleActionRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.suspend_tenant(session, current_user, tenant_id, payload)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.post("/tenants/{tenant_id}/reactivate", response_model=TenantRead)
def reactivate_tenant(
    tenant_id: str,
    payload: TenantLifecycleActionRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.reactivate_tenant(session, current_user, tenant_id, payload)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)
