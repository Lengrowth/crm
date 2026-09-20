from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.hardening import DatabaseRateLimiter
from app.core.config import settings
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.sso import (
    SSOAuthorizationRequest,
    SSOAuthorizationResponse,
    SSOIdentityMappingRequest,
    SSOIdentityMappingResponse,
    SSOTokenRequest,
    SSOTokenResponse,
)
from app.services.sso_service import SSOBrokerError, sso_service


router = APIRouter(prefix="/sso", tags=["sso"])
request_limiter = DatabaseRateLimiter()


def _limit(request: Request, operation: str, session: Session) -> None:
    host = request.client.host if request.client else "anonymous"
    allowed, retry_after = request_limiter.allow(
        session,
        f"{operation}:{host}",
        limit=30,
        window_seconds=60,
    )
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many identity requests. Try again shortly.",
            headers={"Retry-After": str(retry_after)},
        )


def _raise(exc: SSOBrokerError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc


@router.post("/authorize", response_model=SSOAuthorizationResponse)
def authorize(
    payload: SSOAuthorizationRequest,
    request: Request,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    _limit(request, "authorize", session)
    try:
        return sso_service.authorize(session, current_user, payload)
    except SSOBrokerError as exc:
        _raise(exc)


@router.get("/readiness/{tenant_id}")
def readiness(
    tenant_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return sso_service.readiness(session, current_user, tenant_id)
    except SSOBrokerError as exc:
        _raise(exc)


@router.post("/token", response_model=SSOTokenResponse)
def token(
    payload: SSOTokenRequest,
    request: Request,
    session: Session = Depends(get_db_session),
):
    _limit(request, "token", session)
    try:
        return sso_service.exchange(session, payload)
    except SSOBrokerError as exc:
        _raise(exc)


@router.post("/mappings", response_model=SSOIdentityMappingResponse)
def mappings(
    payload: SSOIdentityMappingRequest,
    request: Request,
    session: Session = Depends(get_db_session),
):
    _limit(request, "mapping", session)
    try:
        return sso_service.record_mapping(session, payload)
    except SSOBrokerError as exc:
        _raise(exc)
