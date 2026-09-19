from __future__ import annotations

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.db.seed import seed_reference_data
from app.api.dependencies import get_current_user, get_db_session
from app.core.config import settings
from app.integrations.erpnext_client import OperationResult
from app.integrations.mock_erpnext import MockERPNextClient
from app.main import app
from app.models.domain import ModuleApplicationStatus, ModuleBundle, ModuleBundleItem, ModuleEntitlementAudit, ModuleEntitlementRequest, OrganizationMembership, ProvisioningJob, SaaSUser, Tenant
from app.schemas.auth import AuthRegisterRequest
from app.schemas.control import OrganizationCreateRequest
from app.schemas.modules import ModuleChangeRequest
from app.schemas.onboarding import OnboardingPayload, OperatorExecutionAuthorization, OperatorReviewAction, PublicOnboardingCreate
from app.services.auth_service import AuthService
from app.services.control_plane_service import ControlPlaneService
from app.services.module_entitlement_service import ModuleDependencyConflictError, ModuleEntitlementService
from app.services.onboarding_service import phase4_onboarding_service
from app.workers.provisioning_worker import run_next_job


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)()
    seed_reference_data(session)
    return session


def actor_and_org(session):
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(
        session,
        AuthRegisterRequest(
            email="phase01-owner@example.test",
            full_name="Phase 01 Owner",
            password="local-password-123",
            organization_name="Phase 01 Synthetic",
            membership_role="owner",
            is_platform_admin=True,
        ),
    )
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Phase 01 Company"))
    return actor, organization


def bundle_codes(session, bundle_key: str, version: int) -> list[str]:
    bundle = session.execute(select(ModuleBundle).where(ModuleBundle.bundle_key == bundle_key, ModuleBundle.version == version)).scalar_one()
    return [
        code
        for code in session.execute(
            select(_models.Module.code)
            .join(ModuleBundleItem, ModuleBundleItem.module_id == _models.Module.id)
            .where(ModuleBundleItem.bundle_id == bundle.id)
            .order_by(ModuleBundleItem.sort_order.asc(), _models.Module.code.asc())
        ).scalars()
    ]


def test_champion_v2_is_additive_and_seed_immutable():
    session = make_session()
    v1_before = bundle_codes(session, "champion-drilling", 1)
    v2 = bundle_codes(session, "champion-drilling", 2)
    bundles = {f"{bundle.bundle_key}@{bundle.version}": bundle for bundle in ModuleEntitlementService().list_bundles(session)}

    assert v1_before == ["accounting", "buying", "selling", "stock", "assets", "crm", "projects", "field_ops", "well_mapping", "drilling", "fleet", "reporting"]
    assert v2 == v1_before + ["hr", "payroll", "quality", "support"]
    assert bundles["champion-drilling@2"].supersedes_version == 1
    assert bundles["champion-drilling@2"].added_module_codes == ["hr", "payroll", "quality", "support"]
    assert bundles["champion-drilling@2"].removed_module_codes == []
    assert seed_reference_data(session)["bundles"] == 0
    assert bundle_codes(session, "champion-drilling", 1) == v1_before


def test_v2_preview_closes_dependencies_and_exposes_backing_apps_and_states():
    session = make_session()
    actor, organization = actor_and_org(session)
    service = ModuleEntitlementService()
    payload = ModuleChangeRequest(organization_id=organization.id, enable_codes=["payroll", "quality", "support"], idempotency_key="phase01-preview-1")

    preview = service.preview(session, payload, actor=actor)
    assert preview.dependency_additions == ["accounting", "crm", "hr", "stock"]
    assert preview.required_applications == ["erpnext", "hrms"]
    by_code = {item.code: item for item in preview.effective.items}
    assert by_code["payroll"].states == ["requested", "entitled", "hidden", "needs_attention"]
    assert by_code["payroll"].hidden is True
    assert by_code["payroll"].needs_attention is True
    assert by_code["quality"].states == ["requested", "entitled", "needs_attention"]
    assert by_code["quality"].hidden is False
    assert by_code["payroll"].required_app == "hrms"


def test_v2_apply_is_operator_bound_audited_and_replay_safe():
    session = make_session()
    actor, organization = actor_and_org(session)
    service = ModuleEntitlementService()
    request = ModuleChangeRequest(organization_id=organization.id, bundle_key="champion-drilling", bundle_version=2, idempotency_key="phase01-apply-1")
    preview = service.preview(session, request, actor=actor)
    request.preview_hash = preview.preview_hash

    applied = service.apply(session, actor, request)
    replay = service.apply(session, actor, request)

    assert applied.replayed is False
    assert replay.replayed is True
    assert set(applied.effective.effective_codes) >= {"hr", "payroll", "quality", "support"}
    assert session.query(ModuleEntitlementAudit).filter_by(organization_id=organization.id).count() == 1
    audit = session.query(ModuleEntitlementAudit).filter_by(organization_id=organization.id).one()
    assert audit.actor_user_id == actor.id
    assert audit.organization_id == organization.id
    assert audit.new_bundle_key == "champion-drilling"
    assert audit.new_bundle_version == 2
    assert audit.source_ref == "champion-drilling@2"


def test_v2_preview_and_apply_deny_cross_organization_or_viewer_access():
    session = make_session()
    admin, own = actor_and_org(session)
    other = ControlPlaneService().create_organization(session, admin, OrganizationCreateRequest(name="Phase 01 Other Company"))
    viewer = SaaSUser(email="phase01-viewer@example.test", full_name="Phase 01 Viewer", status="active")
    session.add(viewer)
    session.flush()
    session.add(OrganizationMembership(organization_id=own.id, user_id=viewer.id, role="viewer"))
    session.commit()

    def override_db():
        yield session

    app.dependency_overrides[get_db_session] = override_db
    app.dependency_overrides[get_current_user] = lambda: viewer
    previous_flags = settings.feature_flags
    settings.feature_flags = "module_entitlement_writes=true,module_entitlement_general=true"
    try:
        client = TestClient(app)
        payload = {"organization_id": own.id, "bundle_key": "champion-drilling", "bundle_version": 2, "idempotency_key": "phase01-auth-1"}
        assert client.post(f"/organizations/{own.id}/modules/preview", json=payload).status_code == 403
        assert client.get(f"/organizations/{other.id}/modules").status_code == 403
        assert client.post(f"/organizations/{other.id}/modules/apply", json={**payload, "organization_id": other.id}).status_code == 403
    finally:
        settings.feature_flags = previous_flags
        app.dependency_overrides.clear()


def test_invalid_apply_is_atomic_and_does_not_create_audit_or_request():
    session = make_session()
    actor, organization = actor_and_org(session)
    service = ModuleEntitlementService()
    before_modules = session.query(_models.OrganizationModule).filter_by(organization_id=organization.id).count()
    before_audits = session.query(ModuleEntitlementAudit).filter_by(organization_id=organization.id).count()
    before_requests = session.query(ModuleEntitlementRequest).filter_by(organization_id=organization.id).count()
    invalid = ModuleChangeRequest(organization_id=organization.id, enable_codes=["payroll"], disable_codes=["hr"], preview_hash="a" * 64, idempotency_key="phase01-invalid-apply")

    try:
        service.apply(session, actor, invalid)
    except ModuleDependencyConflictError as exc:
        assert "depends" in str(exc)
    else:
        raise AssertionError("invalid dependency apply must be rejected")
    assert session.query(_models.OrganizationModule).filter_by(organization_id=organization.id).count() == before_modules
    assert session.query(ModuleEntitlementAudit).filter_by(organization_id=organization.id).count() == before_audits
    assert session.query(ModuleEntitlementRequest).filter_by(organization_id=organization.id).count() == before_requests


def test_audit_records_tenant_and_previous_current_bundle_attribution():
    session = make_session()
    actor, organization = actor_and_org(session)
    tenant = Tenant(organization_id=organization.id, tenant_slug="phase01-tenant", environment="staging", status="planned", provisioning_status="pending")
    session.add(tenant)
    session.commit()
    service = ModuleEntitlementService()

    first = ModuleChangeRequest(organization_id=organization.id, bundle_key="champion-drilling", bundle_version=1, idempotency_key="phase01-bundle-v1")
    first.preview_hash = service.preview(session, first, actor=actor).preview_hash
    service.apply(session, actor, first)
    second = ModuleChangeRequest(organization_id=organization.id, bundle_key="champion-drilling", bundle_version=2, idempotency_key="phase01-bundle-v2")
    second.preview_hash = service.preview(session, second, actor=actor).preview_hash
    service.apply(session, actor, second)

    audit = session.execute(select(ModuleEntitlementAudit).where(ModuleEntitlementAudit.organization_id == organization.id).order_by(ModuleEntitlementAudit.created_at.desc())).scalars().first()
    assert audit is not None
    assert audit.tenant_id == tenant.id
    assert audit.tenant_ids_json == [tenant.id]
    assert audit.previous_bundle_key == "champion-drilling"
    assert audit.previous_bundle_version == 1
    assert audit.new_bundle_key == "champion-drilling"
    assert audit.new_bundle_version == 2


def test_provider_and_worker_keep_hrms_modules_pending_without_hrms_readback():
    client = MockERPNextClient()
    created = client.create_site("org", "tenant", {})
    site_id = str(created["site_id"])
    client.install_app(site_id, "erpnext")
    client.install_app(site_id, "lenerp_core")
    client.apply_site_configuration(site_id, {"modules": ["hr", "payroll"], "roles": ["hr_user", "payroll_user", "admin"], "workspaces": ["Human Resources", "Payroll"]})
    missing = client.verify_site_configuration(site_id, ["hr", "payroll"], required_apps={"hr": "hrms", "payroll": "hrms"}, required_roles=["hr_user", "payroll_user", "admin"], required_workspaces=["Human Resources", "Payroll"])
    assert missing["provider_verified"] is False
    assert missing["missing_required_apps"] == ["hrms"]
    client.install_app(site_id, "hrms")
    verified = client.verify_site_configuration(site_id, ["hr", "payroll"], required_apps={"hr": "hrms", "payroll": "hrms"}, required_roles=["hr_user", "payroll_user", "admin"], required_workspaces=["Human Resources", "Payroll"])
    assert verified["provider_verified"] is True

    session = make_session()
    original_flags = settings.feature_flags
    settings.feature_flags = "onboarding_public_intake=true,onboarding_conversion=true,onboarding_execution=true,onboarding_synthetic_allowlist=true,onboarding_real_execution=false"
    try:
        operator = SaaSUser(email="phase01-worker@example.test", full_name="Phase 01 Worker", status="active", is_platform_admin=True)
        session.add(operator)
        session.commit()
        request = phase4_onboarding_service.create_public(session, PublicOnboardingCreate(idempotency_key="phase01-worker-request", payload=OnboardingPayload(company_name="Phase 01 HRMS Gate", legal_name="Phase 01 HRMS Gate", industry="drilling", administrator_name="Phase 01 Admin", administrator_email="phase01-admin@acmephase4.com", requested_modules=["hr", "payroll", "quality", "support"], desired_domain="phase01-hrms.example.test", desired_infrastructure="isolated_synthetic", implementation_notes="Phase 01 negative verification.")))
        phase4_onboarding_service.submit_public(session, request.request_id, request.management_token or "")
        phase4_onboarding_service.begin_review(session, operator, request.request_id, OperatorReviewAction(version=1, reason="Review HRMS gate."))
        phase4_onboarding_service.approve(session, operator, request.request_id, OperatorReviewAction(version=1, reason="Approve synthetic HRMS gate."))
        converted = phase4_onboarding_service.convert(session, operator, request.request_id)
        phase4_onboarding_service.authorize_execution(session, operator, request.request_id, OperatorExecutionAuthorization(version=1, confirmation="authorize_isolated_synthetic_execution", reason="Confirm synthetic HRMS gate."))
        class MissingHRMSReadbackClient(MockERPNextClient):
            def install_app(self, site_id: str, app_name: str) -> OperationResult:
                if app_name == "hrms":
                    return OperationResult({"status": "success", "site_id": site_id, "app": app_name, "provider_verified": True})
                return super().install_app(site_id, app_name)

        result = run_next_job(session, client=MissingHRMSReadbackClient())
        assert result is not None and result.status == "queued"
        tenant = session.get(Tenant, converted.tenant_id)
        assert tenant is not None
        statuses = session.query(ModuleApplicationStatus).filter_by(tenant_id=tenant.id).all()
        by_module = {session.get(_models.Module, row.module_id).code: row for row in statuses}
        assert by_module["hr"].application_state == "pending"
        assert by_module["hr"].verification_state == "pending"
        assert "hrms" in (by_module["hr"].failure_reason or "")
        assert by_module["payroll"].verification_state == "pending"
        assert all(row.verification_state != "verified" for row in statuses if session.get(_models.Module, row.module_id).code in {"hr", "payroll"})
    finally:
        settings.feature_flags = original_flags
