from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session, get_current_user
from app.db.session import get_db_session
from app.models.domain import AuthSession, SaaSUser
from app.schemas.auth import (
    AuthEmailVerificationConfirm,
    AuthEmailVerificationRequest,
    AuthMessageResponse,
    AuthLoginRequest,
    AuthPasswordResetConfirm,
    AuthPasswordResetRequest,
    AuthLogoutResponse,
    AuthMeResponse,
    AuthRegisterRequest,
    AuthTokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", response_model=AuthTokenResponse)
def register(payload: AuthRegisterRequest, session: Session = Depends(get_db_session)):
    return auth_service.register(session, payload)


@router.post("/login", response_model=AuthTokenResponse)
def login(payload: AuthLoginRequest, session: Session = Depends(get_db_session)):
    return auth_service.login(session, payload)


@router.post("/password-reset/request", response_model=AuthMessageResponse)
def request_password_reset(
    payload: AuthPasswordResetRequest, session: Session = Depends(get_db_session)
):
    return auth_service.request_password_reset(session, payload)


@router.post("/password-reset/confirm", response_model=AuthMessageResponse)
def reset_password(payload: AuthPasswordResetConfirm, session: Session = Depends(get_db_session)):
    return auth_service.reset_password(session, payload)


@router.post("/email-verification/request", response_model=AuthMessageResponse)
def request_email_verification(
    payload: AuthEmailVerificationRequest, session: Session = Depends(get_db_session)
):
    return auth_service.request_email_verification(session, payload)


@router.post("/email-verification/resend", response_model=AuthMessageResponse)
def resend_email_verification(
    payload: AuthEmailVerificationRequest, session: Session = Depends(get_db_session)
):
    return auth_service.resend_email_verification(session, payload)


@router.post("/email-verification/verify", response_model=AuthMessageResponse)
def verify_email(
    payload: AuthEmailVerificationConfirm, session: Session = Depends(get_db_session)
):
    return auth_service.verify_email(session, payload)


@router.post("/logout", response_model=AuthLogoutResponse)
def logout(
    session: Session = Depends(get_db_session),
    current_session: AuthSession = Depends(get_current_session),
):
    auth_service.logout(session, current_session)
    return AuthLogoutResponse(detail="Signed out locally.")


@router.get("/me", response_model=AuthMeResponse)
def me(current_user: SaaSUser = Depends(get_current_user), session: Session = Depends(get_db_session)):
    return AuthMeResponse(user=auth_service.build_user_read(session, current_user))
