from __future__ import annotations

from typing import Callable

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import extract_session_token
from app.db.session import get_db_session
from app.models.domain import AuthSession, SaaSUser
from app.services.auth_service import AuthContext, AuthError, AuthService

auth_service = AuthService()


def get_auth_token(
    authorization: str | None = Header(default=None),
    x_session_token: str | None = Header(default=None, alias="X-Session-Token"),
) -> str:
    return extract_session_token(authorization, x_session_token)


def get_auth_context(
    session: Session = Depends(get_db_session),
    token: str = Depends(get_auth_token),
) -> AuthContext:
    try:
        return auth_service.get_context(session, token)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def get_current_user(context: AuthContext = Depends(get_auth_context)) -> SaaSUser:
    return context.user


def get_current_session(context: AuthContext = Depends(get_auth_context)) -> AuthSession:
    if context.session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication session not found.")
    return context.session


def require_platform_admin(current_user: SaaSUser = Depends(get_current_user)) -> SaaSUser:
    if not current_user.is_platform_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Platform admin access required.")
    return current_user


def require_organization_role(
    allowed_roles: set[str],
) -> Callable[[str, Session, AuthContext], AuthContext]:
    def dependency(
        organization_id: str,
        session: Session = Depends(get_db_session),
        context: AuthContext = Depends(get_auth_context),
    ) -> AuthContext:
        if auth_service.user_has_organization_role(session, context.user, organization_id, allowed_roles):
            return context

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organization access denied.")

    return dependency
