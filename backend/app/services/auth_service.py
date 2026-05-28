from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import quote

import logging

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    generate_auth_token,
    generate_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.models.domain import AuthSession, AuthToken, Organization, OrganizationMembership, SaaSUser
from app.schemas.auth import (
    AuthEmailVerificationConfirm,
    AuthEmailVerificationRequest,
    AuthMessageResponse,
    AuthLoginRequest,
    AuthPasswordResetConfirm,
    AuthPasswordResetRequest,
    AuthRegisterRequest,
    AuthSessionRead,
    AuthTokenResponse,
    AuthUserRead,
)
from app.services.communication_service import CommunicationError, CommunicationService


logger = logging.getLogger(__name__)

PASSWORD_RESET_PURPOSE = "password_reset"
EMAIL_VERIFICATION_PURPOSE = "email_verification"


class AuthError(Exception):
    pass


@dataclass
class AuthMembershipSummary:
    organization_id: str
    organization_name: str
    role: str


@dataclass
class AuthContext:
    user: SaaSUser
    session: Optional[AuthSession]
    memberships: list[AuthMembershipSummary]


class AuthService:
    def __init__(self, email_sender: CommunicationService | None = None) -> None:
        self.session_ttl_days = getattr(settings, "auth_session_days", 30)
        self.password_reset_ttl = timedelta(minutes=getattr(settings, "auth_password_reset_token_minutes", 60))
        self.email_verification_ttl = timedelta(hours=getattr(settings, "auth_email_verification_token_hours", 24))
        self.email_sender = email_sender

    def register(self, session: Session, payload: AuthRegisterRequest) -> AuthTokenResponse:
        if self._get_user_by_email(session, payload.email) is not None:
            raise AuthError("A user with that email already exists.")

        now = datetime.now(timezone.utc)
        user = SaaSUser(
            email=payload.email.lower(),
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
            status="active",
            is_platform_admin=payload.is_platform_admin,
            email_verified_at=None,
            password_changed_at=now,
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

        user.last_login_at = now
        access_token, auth_session = self._create_session(session, user)
        verification_token = self._issue_auth_token(
            session,
            user=user,
            purpose=EMAIL_VERIFICATION_PURPOSE,
            ttl=self.email_verification_ttl,
            now=now,
        )
        session.commit()

        self._send_email_verification(user.email, verification_token, user.full_name)

        return self._build_token_response(session, user, auth_session, access_token)

    def login(self, session: Session, payload: AuthLoginRequest) -> AuthTokenResponse:
        user = self._get_user_by_email(session, payload.email)
        if user is None or user.status != "active":
            raise AuthError("Invalid email or password.")
        if not verify_password(payload.password, user.password_hash):
            raise AuthError("Invalid email or password.")

        user.last_login_at = datetime.now(timezone.utc)
        access_token, auth_session = self._create_session(session, user)
        session.commit()

        return self._build_token_response(session, user, auth_session, access_token)

    def request_password_reset(
        self, session: Session, payload: AuthPasswordResetRequest
    ) -> AuthMessageResponse:
        user = self._get_user_by_email(session, payload.email)
        if user is not None and user.status == "active" and user.password_hash:
            token = self._issue_auth_token(
                session,
                user=user,
                purpose=PASSWORD_RESET_PURPOSE,
                ttl=self.password_reset_ttl,
            )
            session.commit()
            self._send_password_reset_email(user.email, token, user.full_name)
        return AuthMessageResponse(
            detail="If an account exists for that email, we sent a password reset link.",
        )

    def reset_password(
        self, session: Session, payload: AuthPasswordResetConfirm
    ) -> AuthMessageResponse:
        token_record = self._get_valid_auth_token(
            session,
            payload.token,
            purpose=PASSWORD_RESET_PURPOSE,
        )
        user = session.get(SaaSUser, token_record.user_id)
        if user is None or user.status != "active":
            raise AuthError("Invalid or expired token.")

        now = datetime.now(timezone.utc)
        user.password_hash = hash_password(payload.new_password)
        user.password_changed_at = now
        token_record.used_at = now
        self._revoke_user_sessions(session, user.id, now=now)
        self._revoke_tokens_for_user_purpose(session, user.id, PASSWORD_RESET_PURPOSE, now=now)
        session.commit()

        return AuthMessageResponse(detail="Password updated successfully.")

    def request_email_verification(
        self, session: Session, payload: AuthEmailVerificationRequest
    ) -> AuthMessageResponse:
        user = self._get_user_by_email(session, payload.email)
        if user is not None and user.status == "active" and user.email_verified_at is None:
            token = self._issue_auth_token(
                session,
                user=user,
                purpose=EMAIL_VERIFICATION_PURPOSE,
                ttl=self.email_verification_ttl,
            )
            session.commit()
            self._send_email_verification(user.email, token, user.full_name)
        return AuthMessageResponse(
            detail="If the email address exists, we sent a verification link.",
        )

    def resend_email_verification(
        self, session: Session, payload: AuthEmailVerificationRequest
    ) -> AuthMessageResponse:
        return self.request_email_verification(session, payload)

    def verify_email(
        self, session: Session, payload: AuthEmailVerificationConfirm
    ) -> AuthMessageResponse:
        token_record = self._get_valid_auth_token(
            session,
            payload.token,
            purpose=EMAIL_VERIFICATION_PURPOSE,
        )
        user = session.get(SaaSUser, token_record.user_id)
        if user is None or user.status != "active":
            raise AuthError("Invalid or expired token.")

        now = datetime.now(timezone.utc)
        user.email_verified_at = now
        token_record.used_at = now
        self._revoke_tokens_for_user_purpose(session, user.id, EMAIL_VERIFICATION_PURPOSE, now=now)
        session.commit()

        return AuthMessageResponse(detail="Email address verified successfully.")

    def logout(self, session: Session, current_session: AuthSession) -> None:
        if current_session.revoked_at is None:
            current_session.revoked_at = datetime.now(timezone.utc)
            session.commit()

    def get_context(self, session: Session, token: str) -> AuthContext:
        session_record = self._get_session_by_token(session, token)
        if session_record is None:
            raise AuthError("Invalid or expired session.")
        if session_record.revoked_at is not None:
            raise AuthError("Session has been revoked.")
        if self._as_utc(session_record.expires_at) <= datetime.now(timezone.utc):
            session_record.revoked_at = datetime.now(timezone.utc)
            session.commit()
            raise AuthError("Session has expired.")

        user = session.get(SaaSUser, session_record.user_id)
        if user is None or user.status != "active":
            raise AuthError("User account is not active.")

        session_record.last_used_at = datetime.now(timezone.utc)
        session.commit()

        return AuthContext(user=user, session=session_record, memberships=self._list_memberships(session, user.id))

    def user_has_organization_role(
        self,
        session: Session,
        user: SaaSUser,
        organization_id: str,
        allowed_roles: Optional[set[str]] = None,
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
            email_verified_at=self._as_utc(user.email_verified_at),
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
        expires_at = datetime.now(timezone.utc) + timedelta(days=self.session_ttl_days)
        auth_session = AuthSession(
            user_id=user.id,
            session_token_hash=hash_session_token(cleartext_token),
            expires_at=expires_at,
            last_used_at=datetime.now(timezone.utc),
        )
        session.add(auth_session)
        session.flush()
        return cleartext_token, auth_session

    def _issue_auth_token(
        self,
        session: Session,
        user: SaaSUser,
        purpose: str,
        ttl: timedelta,
        now: Optional[datetime] = None,
    ) -> str:
        current_time = now or datetime.now(timezone.utc)
        self._revoke_tokens_for_user_purpose(session, user.id, purpose, now=current_time)
        cleartext_token = generate_auth_token()
        auth_token = AuthToken(
            user_id=user.id,
            purpose=purpose,
            token_hash=hash_session_token(cleartext_token),
            sent_to_email=user.email,
            expires_at=current_time + ttl,
        )
        session.add(auth_token)
        session.flush()
        return cleartext_token

    def _get_user_by_email(self, session: Session, email: str) -> Optional[SaaSUser]:
        statement = select(SaaSUser).where(SaaSUser.email == email.strip().lower())
        return session.execute(statement).scalar_one_or_none()

    def _get_valid_auth_token(self, session: Session, token: str, purpose: str) -> AuthToken:
        statement = select(AuthToken).where(
            AuthToken.token_hash == hash_session_token(token),
            AuthToken.purpose == purpose,
        )
        token_record = session.execute(statement).scalar_one_or_none()
        if token_record is None:
            raise AuthError("Invalid or expired token.")

        now = datetime.now(timezone.utc)
        if token_record.revoked_at is not None or token_record.used_at is not None or self._as_utc(token_record.expires_at) <= now:
            token_record.revoked_at = token_record.revoked_at or now
            session.commit()
            raise AuthError("Invalid or expired token.")

        return token_record

    def _get_session_by_token(self, session: Session, token: str) -> Optional[AuthSession]:
        statement = select(AuthSession).where(AuthSession.session_token_hash == hash_session_token(token))
        return session.execute(statement).scalar_one_or_none()

    def _revoke_tokens_for_user_purpose(
        self,
        session: Session,
        user_id: str,
        purpose: str,
        now: Optional[datetime] = None,
    ) -> None:
        current_time = now or datetime.now(timezone.utc)
        statement = (
            update(AuthToken)
            .where(
                AuthToken.user_id == user_id,
                AuthToken.purpose == purpose,
                AuthToken.used_at.is_(None),
                AuthToken.revoked_at.is_(None),
            )
            .values(revoked_at=current_time)
        )
        session.execute(statement)

    def _revoke_user_sessions(self, session: Session, user_id: str, now: Optional[datetime] = None) -> None:
        current_time = now or datetime.now(timezone.utc)
        statement = (
            update(AuthSession)
            .where(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
            .values(revoked_at=current_time)
        )
        session.execute(statement)

    def _send_password_reset_email(self, email: str, token: str, full_name: str) -> None:
        reset_url = self._build_frontend_url("/reset-password", token)
        subject = "Reset your password"
        text = (
            f"Hi {full_name},\n\n"
            f"Use this link to reset your password:\n{reset_url}\n\n"
            "If you did not request a password reset, you can ignore this email.\n"
        )
        self._send_auth_email(email, subject, text)

    def _send_email_verification(self, email: str, token: str, full_name: str) -> None:
        verify_url = self._build_frontend_url("/verify-email", token)
        subject = "Verify your email address"
        text = (
            f"Hi {full_name},\n\n"
            f"Use this link to verify your email address:\n{verify_url}\n\n"
            "If you did not create an account, you can ignore this email.\n"
        )
        self._send_auth_email(email, subject, text)

    def _build_frontend_url(self, path: str, token: str) -> str:
        base_url = settings.frontend_base_url.rstrip("/")
        return f"{base_url}{path}?token={quote(token)}"

    def _send_auth_email(self, email: str, subject: str, text: str) -> None:
        if self.email_sender is not None:
            try:
                self.email_sender.send_transactional_email([email], subject, text)
            except CommunicationError:
                logger.exception("Failed to send auth email to %s", email)
            return

        if settings.is_local_environment or not settings.resend_api_key:
            logger.info("Auth email suppressed for %s in local or unconfigured environment.", email)
            return

        try:
            CommunicationService().send_transactional_email([email], subject, text)
        except CommunicationError:
            logger.exception("Failed to send auth email to %s", email)

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
    def _as_utc(value: Optional[datetime]) -> Optional[datetime]:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
