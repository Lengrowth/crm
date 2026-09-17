from __future__ import annotations

from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.db.session import get_db_session
from app.models.domain import OrganizationMembership, SaaSUser
from app.schemas.modules import (
    ModuleAuditRead,
    ModuleChangeRequest,
    ModuleChangeResult,
    ModuleEffectiveRead,
    ModulePreviewRead,
    ModuleReversalRequest,
)
from app.services.control_plane_service import ControlPlaneAccessError, ControlPlaneNotFoundError, ControlPlaneService
from app.services.module_entitlement_service import (
    MODULE_WRITE_ROLES,
    ModuleEntitlementAccessError,
    ModuleEntitlementError,
    ModuleEntitlementNotFound,
    ModuleEntitlementValidationError,
    module_entitlement_service,
)

router = APIRouter(tags=["modules"])
control_plane_service = ControlPlaneService()


def _organization_access(session: Session, user: SaaSUser, organization_id: str, *, write: bool = False, preview: bool = False) -> None:
    try:
        control_plane_service._ensure_organization_access(session, user, organization_id)
    except (ControlPlaneAccessError, ControlPlaneNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN if isinstance(exc, ControlPlaneAccessError) else status.HTTP_404_NOT_FOUND, detail="Organization access denied." if isinstance(exc, ControlPlaneAccessError) else "Organization not found.") from exc
    if not write:
        return
    if preview:
        # Preview is read-only and available to the same narrow organization
        # roles that may eventually apply a change.
        if user.is_platform_admin:
            return
        role = session.execute(select(OrganizationMembership.role).where(OrganizationMembership.organization_id == organization_id, OrganizationMembership.user_id == user.id)).scalar_one_or_none()
        if role not in MODULE_WRITE_ROLES:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Module administration access required.")
        return
    flags = settings.feature_flag_map
    if not flags.get("module_entitlement_writes", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Module entitlement writes are not enabled.")
    if flags.get("module_entitlement_operator_only", False) and not user.is_platform_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator-only module rollout is active.")
    if not user.is_platform_admin:
        role = session.execute(select(OrganizationMembership.role).where(OrganizationMembership.organization_id == organization_id, OrganizationMembership.user_id == user.id)).scalar_one_or_none()
        if role not in MODULE_WRITE_ROLES or not flags.get("module_entitlement_general", False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Module administration access required.")


def _raise_module_error(exc: ModuleEntitlementError) -> None:
    if isinstance(exc, ModuleEntitlementNotFound):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module resource not found.") from exc
    if isinstance(exc, ModuleEntitlementAccessError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Module administration access denied.") from exc
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


def _path_payload(organization_id: str, payload: ModuleChangeRequest) -> ModuleChangeRequest:
    if payload.organization_id != organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization identifiers do not match.")
    return payload


@router.get("/organizations/{organization_id}/modules", response_model=ModuleEffectiveRead)
def get_effective_modules(organization_id: str, session: Session = Depends(get_db_session), current_user: SaaSUser = Depends(get_current_user)):
    _organization_access(session, current_user, organization_id)
    try:
        return module_entitlement_service.resolve(session, organization_id)
    except ModuleEntitlementError as exc:
        _raise_module_error(exc)


@router.post("/organizations/{organization_id}/modules/preview", response_model=ModulePreviewRead)
def preview_modules(organization_id: str, payload: ModuleChangeRequest, session: Session = Depends(get_db_session), current_user: SaaSUser = Depends(get_current_user)):
    _organization_access(session, current_user, organization_id, write=True, preview=True)
    try:
        return module_entitlement_service.preview(session, _path_payload(organization_id, payload))
    except ModuleEntitlementError as exc:
        _raise_module_error(exc)


@router.post("/organizations/{organization_id}/modules/apply", response_model=ModuleChangeResult)
def apply_modules(organization_id: str, payload: ModuleChangeRequest, session: Session = Depends(get_db_session), current_user: SaaSUser = Depends(get_current_user)):
    _organization_access(session, current_user, organization_id, write=True)
    try:
        return module_entitlement_service.apply(session, current_user, _path_payload(organization_id, payload))
    except ModuleEntitlementError as exc:
        _raise_module_error(exc)


@router.post("/organizations/{organization_id}/modules/reverse", response_model=ModuleChangeResult)
def reverse_modules(organization_id: str, payload: ModuleReversalRequest, session: Session = Depends(get_db_session), current_user: SaaSUser = Depends(get_current_user)):
    _organization_access(session, current_user, organization_id, write=True)
    if payload.organization_id != organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization identifiers do not match.")
    try:
        return module_entitlement_service.reverse(session, current_user, payload)
    except ModuleEntitlementError as exc:
        _raise_module_error(exc)


@router.get("/organizations/{organization_id}/modules/audit", response_model=list[ModuleAuditRead])
def list_module_audit(organization_id: str, limit: int = Query(default=100, ge=1, le=500), session: Session = Depends(get_db_session), current_user: SaaSUser = Depends(get_current_user)):
    _organization_access(session, current_user, organization_id)
    return module_entitlement_service.list_audit(session, organization_id, limit)
