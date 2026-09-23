from __future__ import annotations

import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models as _models  # noqa: F401
from app.core.config import settings
from app.db.base import Base
from app.models.domain import ERPIdentityMapping, OrganizationMembership, SSOAuthorizationCode, Tenant
from app.schemas.auth import AuthRegisterRequest
from app.schemas.control import OrganizationCreateRequest, TenantCreateRequest
from app.schemas.sso import SSOAuthorizationRequest, SSOIdentityMappingRequest, SSOTokenRequest
from app.services.auth_service import AuthService
from app.services.control_plane_service import ControlPlaneService
from app.services.sso_service import SSOBrokerError, sso_service


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, future=True)()


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return verifier, challenge


@pytest.fixture(autouse=True)
def sso_settings():
    original_flags = settings.feature_flags
    original_secret = settings.sso_exchange_secret
    settings.feature_flags = "phase3_unified_identity=on"
    settings.sso_exchange_secret = "synthetic-exchange-secret"
    yield
    settings.feature_flags = original_flags
    settings.sso_exchange_secret = original_secret


def ready_fixture():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="champion@example.test", full_name="Champion User", password="local-password-123", organization_name="Champion Org", membership_role="owner", is_platform_admin=False))
    user = auth.get_context(session, response.access_token).user
    user.email_verified_at = datetime.now(timezone.utc)
    session.commit()
    organization = control.create_organization(session, user, OrganizationCreateRequest(name="Champion Org 2"))
    tenant = control.create_tenant(session, user, TenantCreateRequest(organization_id=organization.id, tenant_slug="champion-synthetic", environment="staging", erpnext_site_name="erp.synthetic.example", erpnext_base_url="https://erp.synthetic.example"), organization.id)
    tenant.status = "ready"
    tenant.provisioning_status = "ready"
    tenant.erp_role_profile_version = "champion-v1"
    tenant.erp_role_profile_status = "ready"
    tenant.sso_rollout_enabled = True
    session.commit()
    return session, user, organization, tenant


def request_payload(tenant: Tenant, state: str | None = None):
    verifier, challenge = pkce_pair()
    return verifier, SSOAuthorizationRequest(tenant_id=tenant.id, client_id=settings.sso_client_id, audience=settings.sso_audience, redirect_uri=f"{tenant.erpnext_base_url}{settings.sso_callback_path}", state=state or secrets.token_urlsafe(24), code_challenge=challenge, code_challenge_method="S256", requested_path="/app")


def test_successful_exchange_is_single_use_and_mapping_replay_is_idempotent():
    session, user, organization, tenant = ready_fixture()
    verifier, payload = request_payload(tenant)
    authorization = sso_service.authorize(session, user, payload)
    token = sso_service.exchange(session, SSOTokenRequest(code=authorization.code, client_id=payload.client_id, audience=payload.audience, redirect_uri=payload.redirect_uri, code_verifier=verifier, client_secret=settings.sso_exchange_secret))
    assert token.issuer == settings.frontend_base_url
    mapping_payload = SSOIdentityMappingRequest(exchange_handle=token.mapping_handle, client_secret=settings.sso_exchange_secret, erp_user="champion@example.test")
    first = sso_service.record_mapping(session, mapping_payload)
    replay = sso_service.record_mapping(session, mapping_payload)
    assert first.mapping_id == replay.mapping_id
    assert replay.replayed is True
    assert session.execute(select(ERPIdentityMapping).where(ERPIdentityMapping.id == first.mapping_id)).scalar_one().mapping_status == "active"
    with pytest.raises(SSOBrokerError, match="invalid or expired"):
        sso_service.exchange(session, SSOTokenRequest(code=authorization.code, client_id=payload.client_id, audience=payload.audience, redirect_uri=payload.redirect_uri, code_verifier=verifier, client_secret=settings.sso_exchange_secret))


def test_non_ascii_code_verifier_is_rejected_as_a_client_error():
    session, user, organization, tenant = ready_fixture()
    verifier, payload = request_payload(tenant)
    authorization = sso_service.authorize(session, user, payload)
    bad_payload = SSOTokenRequest.model_construct(
        code=authorization.code,
        client_id=payload.client_id,
        audience=payload.audience,
        redirect_uri=payload.redirect_uri,
        code_verifier="é" * 43,
        client_secret=settings.sso_exchange_secret,
    )

    with pytest.raises(SSOBrokerError) as error:
        sso_service.exchange(session, bad_payload)

    assert error.value.status_code == 400
    assert error.value.audit_action == "sso_exchange_pkce_denied"


def test_non_ascii_code_verifier_is_rejected_by_the_request_schema():
    with pytest.raises(ValidationError, match="ASCII"):
        SSOTokenRequest(
            code="c" * 16,
            client_id="client",
            audience="audience",
            redirect_uri="https://erp.example.test/callback",
            code_verifier="é" * 43,
        )


@pytest.mark.parametrize("mutation", ["state", "pkce", "audience", "redirect", "path"])
def test_authorization_and_exchange_bind_state_pkce_audience_redirect_and_path(mutation: str):
    session, user, _, tenant = ready_fixture()
    verifier, payload = request_payload(tenant)
    if mutation == "path":
        payload.requested_path = "/safe/%252e%252e/other"
        with pytest.raises(SSOBrokerError):
            sso_service.authorize(session, user, payload)
        return
    authorization = sso_service.authorize(session, user, payload)
    exchange = SSOTokenRequest(code=authorization.code, client_id=payload.client_id, audience=payload.audience, redirect_uri=payload.redirect_uri, code_verifier=verifier, client_secret=settings.sso_exchange_secret)
    if mutation == "state":
        payload.state = authorization.state
        with pytest.raises(SSOBrokerError):
            sso_service.authorize(session, user, payload)
        return
    elif mutation == "pkce":
        exchange.code_verifier = secrets.token_urlsafe(48)
    elif mutation == "audience":
        exchange.audience = "wrong-audience"
    elif mutation == "redirect":
        exchange.redirect_uri = "https://evil.example/callback"
    with pytest.raises(SSOBrokerError):
        sso_service.exchange(session, exchange)


def test_expired_code_wrong_org_admin_and_removed_membership_are_denied():
    session, user, _, tenant = ready_fixture()
    verifier, payload = request_payload(tenant)
    authorization = sso_service.authorize(session, user, payload)
    code = session.execute(select(SSOAuthorizationCode).where(SSOAuthorizationCode.code_hash == sso_service._hash(authorization.code))).scalar_one()
    code.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    session.commit()
    with pytest.raises(SSOBrokerError, match="invalid or expired"):
        sso_service.exchange(session, SSOTokenRequest(code=authorization.code, client_id=payload.client_id, audience=payload.audience, redirect_uri=payload.redirect_uri, code_verifier=verifier, client_secret=settings.sso_exchange_secret))

    session, user, _, tenant = ready_fixture()
    user.is_platform_admin = True
    session.delete(session.execute(select(OrganizationMembership).where(OrganizationMembership.user_id == user.id, OrganizationMembership.organization_id == tenant.organization_id)).scalar_one())
    session.commit()
    _, payload = request_payload(tenant)
    with pytest.raises(SSOBrokerError):
        sso_service.authorize(session, user, payload)


def test_missing_role_profile_and_feature_flag_fail_closed_without_codes():
    session, user, _, tenant = ready_fixture()
    tenant.erp_role_profile_status = "pending"
    session.commit()
    _, payload = request_payload(tenant)
    with pytest.raises(SSOBrokerError):
        sso_service.authorize(session, user, payload)
    settings.feature_flags = "phase3_unified_identity=off"
    with pytest.raises(SSOBrokerError):
        sso_service.authorize(session, user, payload)
    assert session.execute(select(SSOAuthorizationCode)).scalars().all() == []


def test_platform_admin_without_membership_cannot_probe_readiness_and_mapping_handle_is_exact():
    session, user, _, tenant = ready_fixture()
    user.is_platform_admin = True
    session.delete(session.execute(select(OrganizationMembership).where(OrganizationMembership.user_id == user.id, OrganizationMembership.organization_id == tenant.organization_id)).scalar_one())
    session.commit()
    with pytest.raises(SSOBrokerError, match="unavailable"):
        sso_service.readiness(session, user, tenant.id)

    session, user, _, tenant = ready_fixture()
    verifier, payload = request_payload(tenant)
    authorization = sso_service.authorize(session, user, payload)
    token = sso_service.exchange(session, SSOTokenRequest(code=authorization.code, client_id=payload.client_id, audience=payload.audience, redirect_uri=payload.redirect_uri, code_verifier=verifier, client_secret=settings.sso_exchange_secret))
    mapping_payload = SSOIdentityMappingRequest(exchange_handle=secrets.token_urlsafe(32), client_secret=settings.sso_exchange_secret, erp_user="champion@example.test")
    with pytest.raises(SSOBrokerError, match="invalid or expired"):
        sso_service.record_mapping(session, mapping_payload)
    valid_handle_payload = SSOIdentityMappingRequest(exchange_handle=token.mapping_handle, client_secret=settings.sso_exchange_secret, erp_user="another-user@example.test")
    with pytest.raises(SSOBrokerError, match="not valid"):
        sso_service.record_mapping(session, valid_handle_payload)


def test_membership_removal_revokes_existing_mapping_during_next_exchange_boundary():
    session, user, _, tenant = ready_fixture()
    verifier, payload = request_payload(tenant)
    authorization = sso_service.authorize(session, user, payload)
    token = sso_service.exchange(session, SSOTokenRequest(code=authorization.code, client_id=payload.client_id, audience=payload.audience, redirect_uri=payload.redirect_uri, code_verifier=verifier, client_secret=settings.sso_exchange_secret))
    mapping_payload = SSOIdentityMappingRequest(exchange_handle=token.mapping_handle, client_secret=settings.sso_exchange_secret, erp_user="champion@example.test")
    mapping = sso_service.record_mapping(session, mapping_payload)
    membership = session.execute(select(OrganizationMembership).where(OrganizationMembership.user_id == user.id, OrganizationMembership.organization_id == tenant.organization_id)).scalar_one()
    session.delete(membership)
    session.commit()
    with pytest.raises(SSOBrokerError):
        sso_service.record_mapping(session, mapping_payload)
    stored = session.execute(select(ERPIdentityMapping).where(ERPIdentityMapping.id == mapping.mapping_id)).scalar_one()
    assert stored.mapping_status == "revoked"
