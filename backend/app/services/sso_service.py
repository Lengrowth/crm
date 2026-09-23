from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urlsplit

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.domain import (
    AuditLog,
    ERPIdentityMapping,
    Organization,
    OrganizationMembership,
    SaaSUser,
    SSOAuthorizationCode,
    SSOAuthorizationRequest as SSOAuthorizationRequestRecord,
    Tenant,
)
from app.schemas.sso import (
    SSOAuthorizationRequest,
    SSOAuthorizationResponse,
    SSOIdentityMappingRequest,
    SSOIdentityMappingResponse,
    SSOTokenRequest,
    SSOTokenResponse,
)


logger = logging.getLogger(__name__)


class SSOBrokerError(Exception):
    def __init__(self, message: str, status_code: int = 400, *, audit_action: str = "sso_denied") -> None:
        super().__init__(message)
        self.status_code = status_code
        self.audit_action = audit_action


class SSOService:
    """Temporary isolated broker with an explicit OIDC replacement boundary.

    The broker carries only a one-time authorization code. It is intentionally
    not an access-token issuer: the ERP exchanges the code server-to-server and
    creates its own host-scoped Frappe session.
    """

    def __init__(self) -> None:
        self.code_ttl = timedelta(seconds=max(30, settings.sso_code_ttl_seconds))

    @staticmethod
    def enabled() -> bool:
        return settings.feature_flag_map.get("phase3_unified_identity", False)

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _audit(
        session: Session,
        *,
        action: str,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        entity_id: str = "sso",
        metadata: Optional[dict[str, object]] = None,
    ) -> None:
        session.add(
            AuditLog(
                actor_user_id=user_id,
                organization_id=organization_id,
                tenant_id=tenant_id,
                action=action,
                entity_type="sso",
                entity_id=entity_id,
                metadata_json=metadata or {},
            )
        )

    @staticmethod
    def _deny(
        session: Session,
        message: str,
        *,
        status_code: int = 403,
        action: str = "sso_denied",
        tenant_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[dict[str, object]] = None,
    ) -> None:
        SSOService._audit(
            session,
            action=action,
            user_id=user_id,
            organization_id=organization_id,
            tenant_id=tenant_id,
            metadata=metadata,
        )
        session.commit()
        raise SSOBrokerError(message, status_code, audit_action=action)

    @staticmethod
    def _require_exchange_secret(payload_secret: Optional[str]) -> None:
        expected = settings.sso_exchange_secret
        if not expected or not payload_secret or not hmac.compare_digest(payload_secret, expected):
            raise SSOBrokerError("The ERP identity exchange is unavailable.", 401, audit_action="sso_exchange_denied")

    @staticmethod
    def expected_redirect_uri(tenant: Tenant) -> str:
        if not tenant.erpnext_base_url:
            raise SSOBrokerError("This ERP destination is not ready for central sign-in.", 403)
        parsed = urlsplit(tenant.erpnext_base_url.strip())
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise SSOBrokerError("This ERP destination is not an approved HTTPS destination.", 403)
        return f"{tenant.erpnext_base_url.rstrip('/')}{settings.sso_callback_path}"

    @staticmethod
    def _validate_requested_path(path: str) -> None:
        from urllib.parse import unquote

        decoded = path
        for _ in range(5):
            next_value = unquote(decoded)
            if next_value == decoded:
                break
            decoded = next_value
        parsed = urlsplit(decoded)
        if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment or "\\" in decoded or any(ord(char) < 0x20 for char in decoded):
            raise SSOBrokerError("The requested ERP destination is not allowed.", 400)
        if not decoded.startswith("/") or decoded.startswith("//") or ".." in decoded.split("/"):
            raise SSOBrokerError("The requested ERP destination is not allowed.", 400)

    @staticmethod
    def _validate_membership(session: Session, user: SaaSUser, tenant: Tenant) -> None:
        membership = session.execute(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == tenant.organization_id,
                OrganizationMembership.user_id == user.id,
            )
        ).scalar_one_or_none()
        if user.status != "active" or user.email_verified_at is None or membership is None:
            raise SSOBrokerError("Central membership does not authorize this ERP site.", 403)
        if tenant.status != "ready" or tenant.provisioning_status != "ready":
            raise SSOBrokerError("This ERP site is not ready for central sign-in.", 403)
        if not tenant.erp_role_profile_version or tenant.erp_role_profile_status != "ready":
            raise SSOBrokerError("An approved ERP role profile is not ready for this site.", 403)
        if not tenant.sso_rollout_enabled:
            raise SSOBrokerError("Central ERP sign-in is not enabled for this site.", 403)

    def authorize(
        self,
        session: Session,
        user: SaaSUser,
        payload: SSOAuthorizationRequest,
    ) -> SSOAuthorizationResponse:
        if not self.enabled():
            self._deny(session, "Central ERP sign-in is not enabled.", status_code=404, action="sso_disabled")
        tenant = session.get(Tenant, payload.tenant_id)
        if tenant is None:
            self._deny(session, "The requested ERP destination is unavailable.", status_code=404)
        assert tenant is not None
        try:
            self._validate_membership(session, user, tenant)
            expected_redirect = self.expected_redirect_uri(tenant)
            self._validate_requested_path(payload.requested_path)
        except SSOBrokerError as exc:
            self._deny(
                session,
                str(exc),
                status_code=exc.status_code,
                tenant_id=tenant.id,
                organization_id=tenant.organization_id,
                user_id=user.id,
                action=exc.audit_action,
            )
        if payload.client_id != settings.sso_client_id or payload.audience != settings.sso_audience:
            self._deny(session, "The ERP identity request is not approved.", tenant_id=tenant.id, organization_id=tenant.organization_id, user_id=user.id, action="sso_wrong_client")
        if payload.redirect_uri != expected_redirect:
            self._deny(session, "The ERP destination is not approved.", tenant_id=tenant.id, organization_id=tenant.organization_id, user_id=user.id, action="sso_unapproved_redirect")
        state_hash = self._hash(payload.state)
        if session.execute(select(SSOAuthorizationRequestRecord).where(SSOAuthorizationRequestRecord.state_hash == state_hash)).scalar_one_or_none() is not None:
            self._deny(session, "This sign-in request has already been used.", status_code=409, tenant_id=tenant.id, organization_id=tenant.organization_id, user_id=user.id, action="sso_state_replay")

        now = self._now()
        request = SSOAuthorizationRequestRecord(
            organization_id=tenant.organization_id,
            tenant_id=tenant.id,
            user_id=user.id,
            state_hash=state_hash,
            code_challenge=payload.code_challenge,
            code_challenge_method=payload.code_challenge_method,
            client_id=payload.client_id,
            audience=payload.audience,
            redirect_uri=payload.redirect_uri,
            requested_path=payload.requested_path,
            expires_at=now + self.code_ttl,
        )
        code = secrets.token_urlsafe(32)
        session.add(request)
        session.flush()
        session.add(
            SSOAuthorizationCode(
                request_id=request.id,
                code_hash=self._hash(code),
                user_id=user.id,
                organization_id=tenant.organization_id,
                tenant_id=tenant.id,
                client_id=payload.client_id,
                audience=payload.audience,
                redirect_uri=payload.redirect_uri,
                code_challenge=payload.code_challenge,
                expires_at=now + self.code_ttl,
            )
        )
        self._audit(session, action="sso_authorization_issued", user_id=user.id, organization_id=tenant.organization_id, tenant_id=tenant.id, entity_id=request.id, metadata={"client_id": payload.client_id, "audience": payload.audience})
        session.commit()
        return SSOAuthorizationResponse(code=code, state=payload.state, redirect_uri=payload.redirect_uri, expires_in=int(self.code_ttl.total_seconds()), tenant_id=tenant.id, organization_id=tenant.organization_id)

    def exchange(self, session: Session, payload: SSOTokenRequest) -> SSOTokenResponse:
        if not self.enabled():
            raise SSOBrokerError("Central ERP sign-in is not enabled.", 404, audit_action="sso_disabled")
        try:
            self._require_exchange_secret(payload.client_secret)
        except SSOBrokerError:
            raise
        code_record = session.execute(select(SSOAuthorizationCode).where(SSOAuthorizationCode.code_hash == self._hash(payload.code))).scalar_one_or_none()
        if code_record is None:
            raise SSOBrokerError("The authorization code is invalid or expired.", 400, audit_action="sso_code_invalid")
        now = self._now()
        if code_record.consumed_at is not None:
            self._audit(session, action="sso_code_replay", organization_id=code_record.organization_id, tenant_id=code_record.tenant_id, entity_id=code_record.request_id)
            session.commit()
            raise SSOBrokerError("The authorization code is invalid or expired.", 400, audit_action="sso_code_replay")
        expires_at = code_record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        else:
            expires_at = expires_at.astimezone(timezone.utc)
        if expires_at <= now:
            self._audit(session, action="sso_code_expired", organization_id=code_record.organization_id, tenant_id=code_record.tenant_id, entity_id=code_record.request_id)
            session.commit()
            raise SSOBrokerError("The authorization code is invalid or expired.", 400, audit_action="sso_code_expired")
        if payload.client_id != code_record.client_id or payload.audience != code_record.audience or payload.redirect_uri != code_record.redirect_uri:
            self._audit(session, action="sso_exchange_wrong_client", organization_id=code_record.organization_id, tenant_id=code_record.tenant_id, entity_id=code_record.request_id)
            session.commit()
            raise SSOBrokerError("The authorization code is invalid for this ERP client.", 400, audit_action="sso_exchange_wrong_client")
        try:
            verifier_bytes = payload.code_verifier.encode("ascii")
        except UnicodeEncodeError as exc:
            self._audit(
                session,
                action="sso_exchange_pkce_denied",
                organization_id=code_record.organization_id,
                tenant_id=code_record.tenant_id,
                entity_id=code_record.request_id,
            )
            session.commit()
            raise SSOBrokerError(
                "The authorization code is invalid for this session.",
                400,
                audit_action="sso_exchange_pkce_denied",
            ) from exc
        verifier_digest = base64.urlsafe_b64encode(hashlib.sha256(verifier_bytes).digest()).rstrip(b"=").decode("ascii")
        if not hmac.compare_digest(verifier_digest, code_record.code_challenge):
            self._audit(session, action="sso_exchange_pkce_denied", organization_id=code_record.organization_id, tenant_id=code_record.tenant_id, entity_id=code_record.request_id)
            session.commit()
            raise SSOBrokerError("The authorization code is invalid for this session.", 400, audit_action="sso_exchange_pkce_denied")
        user = session.get(SaaSUser, code_record.user_id)
        tenant = session.get(Tenant, code_record.tenant_id)
        if user is None or tenant is None:
            raise SSOBrokerError("The authorization code is invalid or expired.", 400, audit_action="sso_code_invalid")
        try:
            self._validate_membership(session, user, tenant)
        except SSOBrokerError as exc:
            self._audit(session, action="sso_exchange_membership_denied", user_id=user.id, organization_id=tenant.organization_id, tenant_id=tenant.id, entity_id=code_record.request_id)
            session.commit()
            raise exc
        consumed = session.execute(
            update(SSOAuthorizationCode)
            .where(
                SSOAuthorizationCode.id == code_record.id,
                SSOAuthorizationCode.consumed_at.is_(None),
            )
            .values(consumed_at=now)
        )
        if consumed.rowcount != 1:
            self._audit(
                session,
                action="sso_code_replay",
                organization_id=code_record.organization_id,
                tenant_id=code_record.tenant_id,
                entity_id=code_record.request_id,
            )
            session.commit()
            raise SSOBrokerError("The authorization code is invalid or expired.", 400, audit_action="sso_code_replay")
        request = session.get(SSOAuthorizationRequestRecord, code_record.request_id)
        if request is not None:
            request.status = "exchanged"
            request.completed_at = now
        mapping_handle = secrets.token_urlsafe(32)
        code_record.mapping_handle_hash = self._hash(mapping_handle)
        code_record.mapping_handle_expires_at = now + self.code_ttl
        self._audit(session, action="sso_exchange_succeeded", user_id=user.id, organization_id=tenant.organization_id, tenant_id=tenant.id, entity_id=code_record.request_id, metadata={"client_id": payload.client_id, "audience": payload.audience})
        session.commit()
        return SSOTokenResponse(issuer=settings.frontend_base_url.rstrip("/"), audience=code_record.audience, client_id=code_record.client_id, control_plane_user_id=user.id, email=user.email, full_name=user.full_name, organization_id=tenant.organization_id, tenant_id=tenant.id, erp_user_key=user.email.lower(), role_profile_version=tenant.erp_role_profile_version or "", mapping_handle=mapping_handle, expires_in=60)

    def record_mapping(self, session: Session, payload: SSOIdentityMappingRequest) -> SSOIdentityMappingResponse:
        self._require_exchange_secret(payload.client_secret)
        if not self.enabled():
            raise SSOBrokerError("Central ERP sign-in is not enabled.", 404, audit_action="sso_disabled")
        code_record = session.execute(select(SSOAuthorizationCode).where(SSOAuthorizationCode.mapping_handle_hash == self._hash(payload.exchange_handle))).scalar_one_or_none()
        if code_record is None or code_record.consumed_at is None:
            raise SSOBrokerError("The ERP identity mapping is invalid or expired.", 400, audit_action="sso_mapping_denied")
        handle_expires_at = code_record.mapping_handle_expires_at
        if handle_expires_at is None or (handle_expires_at.replace(tzinfo=timezone.utc) if handle_expires_at.tzinfo is None else handle_expires_at) <= self._now():
            raise SSOBrokerError("The ERP identity mapping is invalid or expired.", 400, audit_action="sso_mapping_expired")
        user = session.get(SaaSUser, code_record.user_id)
        tenant = session.get(Tenant, code_record.tenant_id)
        if user is None or tenant is None or code_record.client_id != settings.sso_client_id:
            raise SSOBrokerError("The ERP identity mapping is not valid.", 400, audit_action="sso_mapping_denied")
        erp_site = tenant.erpnext_site_name
        if not erp_site:
            raise SSOBrokerError("The ERP site identity is not approved.", 409, audit_action="sso_site_denied")
        if payload.erp_user != user.email.lower():
            raise SSOBrokerError("The ERP identity mapping is not valid.", 400, audit_action="sso_mapping_identity_denied")
        try:
            self._validate_membership(session, user, tenant)
        except SSOBrokerError:
            revoked = self._revoke_mappings(session, user.id, tenant.id)
            self._audit(
                session,
                action="sso_mapping_revoked",
                user_id=user.id,
                organization_id=tenant.organization_id,
                tenant_id=tenant.id,
                entity_id=tenant.id,
                metadata={"count": revoked, "reason": "membership_or_readiness_denied"},
            )
            session.commit()
            raise
        existing = session.execute(select(ERPIdentityMapping).where(ERPIdentityMapping.user_id == user.id, ERPIdentityMapping.organization_id == tenant.organization_id, ERPIdentityMapping.tenant_id == tenant.id)).scalar_one_or_none()
        conflicting = session.execute(select(ERPIdentityMapping).where(ERPIdentityMapping.tenant_id == tenant.id, ERPIdentityMapping.erp_user == payload.erp_user, ERPIdentityMapping.user_id != user.id)).scalar_one_or_none()
        if conflicting is not None:
            raise SSOBrokerError("The ERP identity is already mapped to another central user.", 409, audit_action="sso_mapping_conflict")
        role_profile_version = tenant.erp_role_profile_version or ""
        replayed = existing is not None and existing.erp_user == payload.erp_user and existing.role_profile_version == role_profile_version and existing.mapping_status == "active"
        if code_record.mapping_handle_consumed_at is not None:
            if replayed:
                return SSOIdentityMappingResponse(mapping_id=existing.id, mapping_status=existing.mapping_status, role_profile_version=existing.role_profile_version, replayed=True)
            raise SSOBrokerError("The ERP identity mapping is invalid or expired.", 400, audit_action="sso_mapping_replay")
        consumed = session.execute(update(SSOAuthorizationCode).where(SSOAuthorizationCode.id == code_record.id, SSOAuthorizationCode.mapping_handle_consumed_at.is_(None)).values(mapping_handle_consumed_at=self._now()))
        if consumed.rowcount != 1:
            raise SSOBrokerError("The ERP identity mapping is invalid or expired.", 400, audit_action="sso_mapping_replay")
        previous_profile = existing.role_profile_version if existing else None
        if existing is None:
            existing = ERPIdentityMapping(user_id=user.id, organization_id=tenant.organization_id, tenant_id=tenant.id, erp_site=erp_site, erp_user=payload.erp_user, role_profile_version=role_profile_version)
            session.add(existing)
        else:
            existing.erp_site = erp_site
            existing.erp_user = payload.erp_user
            existing.role_profile_version = role_profile_version
            existing.mapping_status = "active"
            existing.revoked_at = None
        existing.last_login_at = self._now()
        session.flush()
        self._audit(session, action="sso_role_reconciled" if previous_profile and previous_profile != role_profile_version else "sso_mapping_upserted", user_id=user.id, organization_id=tenant.organization_id, tenant_id=tenant.id, entity_id=existing.id, metadata={"role_profile_version": role_profile_version, "replayed": replayed})
        session.commit()
        return SSOIdentityMappingResponse(mapping_id=existing.id, mapping_status=existing.mapping_status, role_profile_version=existing.role_profile_version, replayed=replayed)

    def revoke_for_membership(self, session: Session, user_id: str, tenant_id: str) -> int:
        count = self._revoke_mappings(session, user_id, tenant_id)
        self._audit(session, action="sso_mapping_revoked", user_id=user_id, tenant_id=tenant_id, entity_id=tenant_id, metadata={"count": count})
        session.commit()
        return count

    def readiness(self, session: Session, user: SaaSUser, tenant_id: str):
        from app.schemas.sso import SSOReadinessResponse

        tenant = session.get(Tenant, tenant_id)
        if tenant is None:
            raise SSOBrokerError("ERP destination unavailable.", 404)
        membership = session.execute(select(OrganizationMembership).where(OrganizationMembership.organization_id == tenant.organization_id, OrganizationMembership.user_id == user.id)).scalar_one_or_none()
        if membership is None:
            raise SSOBrokerError("ERP destination unavailable.", 404)
        organization = session.get(Organization, tenant.organization_id)
        if organization is None:
            raise SSOBrokerError("ERP destination unavailable.", 404)
        enabled_for_site = self.enabled() and tenant.sso_rollout_enabled
        explanation = "Ready for central sign-in."
        ready = False
        if not self.enabled():
            explanation = "Central ERP sign-in is disabled for this environment."
        elif not tenant.sso_rollout_enabled:
            explanation = "Central ERP sign-in is not enabled for this site."
        elif tenant.status != "ready" or tenant.provisioning_status != "ready":
            explanation = "The ERP site is not ready for central sign-in."
        elif not tenant.erpnext_base_url:
            explanation = "The ERP destination is not configured."
        elif tenant.erp_role_profile_status != "ready" or not tenant.erp_role_profile_version:
            explanation = "An approved ERP role profile is not ready."
        else:
            ready = True
        return SSOReadinessResponse(tenant_id=tenant.id, organization_id=tenant.organization_id, organization_name=organization.name, tenant_slug=tenant.tenant_slug, environment=tenant.environment, destination=tenant.erpnext_base_url, enabled=enabled_for_site, ready=ready, explanation=explanation)

    @staticmethod
    def _revoke_mappings(session: Session, user_id: str, tenant_id: str) -> int:
        mappings = session.execute(select(ERPIdentityMapping).where(ERPIdentityMapping.user_id == user_id, ERPIdentityMapping.tenant_id == tenant_id, ERPIdentityMapping.mapping_status == "active")).scalars().all()
        now = datetime.now(timezone.utc)
        for mapping in mappings:
            mapping.mapping_status = "revoked"
            mapping.revoked_at = now
        return len(mappings)


sso_service = SSOService()
