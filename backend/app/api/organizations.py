from __future__ import annotations

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.control import OrganizationCreateRequest, OrganizationUpdateRequest, TenantCreateRequest
from app.schemas.domain import OrganizationRead, TenantRead
from app.services.control_plane_service import (
    ControlPlaneAccessError,
    ControlPlaneNotFoundError,
    ControlPlaneService,
    ControlPlaneValidationError,
)

router = APIRouter(tags=["organizations"])
control_plane_service = ControlPlaneService()


def _raise_control_plane_error(
    exc: Union[ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError]
) -> None:
    if isinstance(exc, ControlPlaneNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, ControlPlaneValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.get("/organizations", response_model=list[OrganizationRead])
def list_organizations(
    limit: int | None = Query(default=None, ge=1, le=100),
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    return control_plane_service.list_organizations(session, current_user, limit=limit)


@router.post("/organizations", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_organization(
    payload: OrganizationCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    return control_plane_service.create_organization(session, current_user, payload)


@router.get("/organizations/{organization_id}", response_model=OrganizationRead)
def get_organization(
    organization_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.get_organization(session, current_user, organization_id)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.patch("/organizations/{organization_id}", response_model=OrganizationRead)
def update_organization(
    organization_id: str,
    payload: OrganizationUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.update_organization(session, current_user, organization_id, payload)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.get("/organizations/{organization_id}/tenants", response_model=list[TenantRead])
def list_organization_tenants(
    organization_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.list_tenants(session, current_user, organization_id)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)


@router.post("/organizations/{organization_id}/tenants", response_model=TenantRead, status_code=status.HTTP_201_CREATED)
def create_organization_tenant(
    organization_id: str,
    payload: TenantCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return control_plane_service.create_tenant(session, current_user, payload, organization_id)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneValidationError) as exc:
        _raise_control_plane_error(exc)
