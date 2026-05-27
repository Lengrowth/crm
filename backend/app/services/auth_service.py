from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import generate_session_token, hash_password, hash_session_token, verify_password
from app.models.domain import AuthSession, Organization, OrganizationMembership, SaaSUser
from app.schemas.auth import (
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthSessionRead,
    AuthTokenResponse,
    AuthUserRead,
)


class AuthError(Exception):
    pass


@dataclass(slots=True)
class AuthMembershipSummary:
    organization_id: str
    organization_name: str
    role: str


@dataclass(slots=True)
class AuthContext:
    user: SaaSUser
    session: AuthSession | None
    memberships: list[AuthMembershipSummary]


class AuthService:
    def __init__(self) -> None:
        self.session_ttl_days = getattr(settings, "auth_session_days", 30)

    def register(self, session: Session, payload: AuthRegisterRequest) -> AuthTokenResponse:
        if self._get_user_by_email(session, payload.email) is not None:
            raise AuthError("A user with that email already exists.")

        user = SaaSUser(
            email=payload.email.lower(),
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            status="active",
            is_platform_admin=payload.is_platform_admin,
        )
        session.add(user)
        session.flush()

        organization = Organization(
            name=payload.organization_name,
            status="lead",
        )
        session.add(organization)
        session.flush()

        membership = OrganizationMembership(
            organization_id=organization.id,
            user_id=user.id,
            role=payload.membership_role,
        )
        session.add(membership)
        session.flush()

        user.last_login_at = datetime.now(UTC)
        access_token, auth_session = self._create_session(session, user)
        session.commit()

        return self._build_token_response(session, user, auth_session, access_token)

    def login(self, session: Session, payload: AuthLoginRequest) -> AuthTokenResponse:
        user = self._get_user_by_email(session, payload.email)
        if user is None or user.status != "active":
            raise AuthError("Invalid email or password.")
        if not verify_password(payload.password, user.password_hash):
            raise AuthError("Invalid email or password.")

        user.last_login_at = datetime.now(UTC)
        access_token, auth_session = self._create_session(session, user)
        session.commit()

        return self._build_token_response(session, user, auth_session, access_token)

    def logout(self, session: Session, current_session: AuthSession) -> None:
        if current_session.revoked_at is None:
            current_session.revoked_at = datetime.now(UTC)
            session.commit()

    def get_context(self, session: Session, token: str) -> AuthContext:
        session_record = self._get_session_by_token(session, token)
        if session_record is None:
            raise AuthError("Invalid or expired session.")
        if session_record.revoked_at is not None:
            raise AuthError("Session has been revoked.")
        if self._as_utc(session_record.expires_at) <= datetime.now(UTC):
            session_record.revoked_at = datetime.now(UTC)
            session.commit()
            raise AuthError("Session has expired.")

        user = session.get(SaaSUser, session_record.user_id)
        if user is None or user.status != "active":
            raise AuthError("User account is not active.")

        session_record.last_used_at = datetime.now(UTC)
        session.commit()

        return AuthContext(user=user, session=session_record, memberships=self._list_memberships(session, user.id))

    def user_has_organization_role(
        self,
        session: Session,
        user: SaaSUser,
        organization_id: str,
        allowed_roles: set[str] | None = None,
    ) -> bool:
        if user.is_platform_admin:
            return True

        memberships = self._list_memberships(session, user.id)
        for membership in memberships:
            if membership.organization_id != organization_id:
                continue
            if not allowed_roles or membership.role in allowed_roles:
                return True
        return False

    def build_user_read(self, session: Session, user: SaaSUser) -> AuthUserRead:
        memberships = self._list_memberships(session, user.id)
        return AuthUserRead(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            status=user.status,
            is_platform_admin=user.is_platform_admin,
            last_login_at=self._as_utc(user.last_login_at),
            memberships=[
                {
                    "organization_id": membership.organization_id,
                    "organization_name": membership.organization_name,
                    "role": membership.role,  # type: ignore[arg-type]
                }
                for membership in memberships
            ],
        )

    def build_session_read(self, auth_session: AuthSession) -> AuthSessionRead:
        return AuthSessionRead(
            id=auth_session.id,
            user_id=auth_session.user_id,
            expires_at=self._as_utc(auth_session.expires_at),
            revoked_at=self._as_utc(auth_session.revoked_at),
            last_used_at=self._as_utc(auth_session.last_used_at),
            created_at=self._as_utc(auth_session.created_at),
            updated_at=self._as_utc(auth_session.updated_at),
        )

    def _build_token_response(
        self,
        session: Session,
        user: SaaSUser,
        auth_session: AuthSession,
        access_token: str,
    ) -> AuthTokenResponse:
        return AuthTokenResponse(
            access_token=access_token,
            expires_at=auth_session.expires_at,
            user=self.build_user_read(session, user),
            session=self.build_session_read(auth_session),
        )

    def _create_session(self, session: Session, user: SaaSUser) -> tuple[str, AuthSession]:
        cleartext_token = generate_session_token()
        expires_at = datetime.now(UTC) + timedelta(days=self.session_ttl_days)
        auth_session = AuthSession(
            user_id=user.id,
            session_token_hash=hash_session_token(cleartext_token),
            expires_at=expires_at,
            last_used_at=datetime.now(UTC),
        )
        session.add(auth_session)
        session.flush()
        return cleartext_token, auth_session

    def _get_user_by_email(self, session: Session, email: str) -> SaaSUser | None:
        statement = select(SaaSUser).where(SaaSUser.email == email.strip().lower())
        return session.execute(statement).scalar_one_or_none()

    def _get_session_by_token(self, session: Session, token: str) -> AuthSession | None:
        statement = select(AuthSession).where(AuthSession.session_token_hash == hash_session_token(token))
        return session.execute(statement).scalar_one_or_none()

    def _list_memberships(self, session: Session, user_id: str) -> list[AuthMembershipSummary]:
        statement = (
            select(OrganizationMembership, Organization.name)
            .join(Organization, Organization.id == OrganizationMembership.organization_id)
            .where(OrganizationMembership.user_id == user_id)
            .order_by(OrganizationMembership.created_at.asc())
        )
        rows = session.execute(statement).all()
        return [
            AuthMembershipSummary(
                organization_id=membership.organization_id,
                organization_name=organization_name,
                role=membership.role,
            )
            for membership, organization_name in rows
        ]

    @staticmethod
    def _as_utc(value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
