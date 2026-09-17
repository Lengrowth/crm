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
from app.main import app
from app.models.domain import ModuleEntitlementAudit, OrganizationModule, SaaSUser
from app.schemas.auth import AuthRegisterRequest
from app.schemas.control import OrganizationCreateRequest
from app.schemas.modules import ModuleChangeRequest, ModuleReversalRequest
from app.services.auth_service import AuthService
from app.services.control_plane_service import ControlPlaneService
from app.services.module_entitlement_service import ModuleEntitlementService, ModuleEntitlementValidationError


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)()
    seed_reference_data(session)
    return session


def test_catalog_seed_is_complete_and_idempotent():
    session = make_session()
    first = seed_reference_data(session)
    second = seed_reference_data(session)
    codes = [row.code for row in session.execute(select(_models.Module).order_by(_models.Module.display_order)).scalars()]
    assert {"accounting", "buying", "selling", "stock", "assets", "hr", "payroll", "manufacturing", "crm", "quality", "projects", "support", "well_mapping"}.issubset(codes)
    assert "inventory" in codes
    assert second["modules"] == 0
    assert first["bundles"] == 0


def test_resolution_dependency_source_and_safe_existing_default():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="p3-admin@example.test", full_name="P3 Admin", password="local-password-123", organization_name="Admin Workspace", membership_role="owner", is_platform_admin=True))
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Synthetic P3"))
    service = ModuleEntitlementService()
    empty = service.resolve(session, organization.id)
    assert empty.effective_codes == []
    preview = service.preview(session, ModuleChangeRequest(organization_id=organization.id, enable_codes=["selling"], idempotency_key="preview-selling"), actor=actor)
    assert preview.dependency_additions == ["accounting"]
    assert preview.effective.effective_codes == ["accounting", "selling"]
    assert "organization override" in next(item for item in preview.effective.items if item.code == "selling").explanation


def test_transactional_apply_retry_dependency_disable_and_reversal():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="p3-write@example.test", full_name="P3 Writer", password="local-password-123", organization_name="Writer Workspace", membership_role="owner", is_platform_admin=True))
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Synthetic Apply"))
    service = ModuleEntitlementService()
    request = ModuleChangeRequest(organization_id=organization.id, enable_codes=["selling"], reason="synthetic apply", idempotency_key="apply-selling-1")
    preview = service.preview(session, request, actor=actor)
    request.preview_hash = preview.preview_hash
    result = service.apply(session, actor, request)
    replay = service.apply(session, actor, request)
    assert replay.replayed is True
    assert result.effective.effective_codes == ["accounting", "selling"]
    assert session.query(ModuleEntitlementAudit).filter_by(organization_id=organization.id).count() == 1
    assert session.query(OrganizationModule).filter_by(organization_id=organization.id).count() == 1
    with __import__("pytest").raises(ModuleEntitlementValidationError, match="preview_hash"):
        service.apply(session, actor, ModuleChangeRequest(organization_id=organization.id, enable_codes=["crm"], idempotency_key="missing-preview"))
    bad = ModuleChangeRequest(organization_id=organization.id, disable_codes=["accounting"], idempotency_key="disable-accounting")
    try:
        service.preview(session, bad)
    except ModuleEntitlementValidationError as exc:
        assert "depends" in str(exc)
    else:
        raise AssertionError("dependency disable must be rejected")
    reverse_request = ModuleReversalRequest(organization_id=organization.id, audit_id=result.audit_id or "", idempotency_key="reverse-selling-1")
    reversed_result = service.reverse(session, actor, reverse_request)
    assert reversed_result.operation == "reverse"
    assert reversed_result.effective.effective_codes == []
    assert session.query(OrganizationModule).filter_by(organization_id=organization.id).count() == 0
    assert session.query(ModuleEntitlementAudit).filter_by(organization_id=organization.id).count() == 2


def test_api_is_authorized_tenant_scoped_and_keeps_erp_state_read_only():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    admin_response = auth.register(session, AuthRegisterRequest(email="p3-api-admin@example.test", full_name="P3 API Admin", password="local-password-123", organization_name="API Admin", membership_role="owner", is_platform_admin=True))
    admin = auth.get_context(session, admin_response.access_token).user
    own = control.create_organization(session, admin, OrganizationCreateRequest(name="API Own"))
    other = control.create_organization(session, admin, OrganizationCreateRequest(name="API Other"))
    member = SaaSUser(email="p3-api-member@example.test", full_name="API Member", status="active")
    session.add(member)
    session.commit()
    from app.models.domain import OrganizationMembership
    session.add(OrganizationMembership(organization_id=own.id, user_id=member.id, role="viewer"))
    session.commit()

    def override_db():
        yield session
    app.dependency_overrides[get_db_session] = override_db
    app.dependency_overrides[get_current_user] = lambda: admin
    previous_flags = settings.feature_flags
    settings.feature_flags = "module_entitlement_writes=true,module_entitlement_operator_only=true"
    try:
        client = TestClient(app)
        catalog = client.get("/catalog/modules")
        assert catalog.status_code == 200
        assert {item["code"] for item in catalog.json()} >= {"accounting", "stock", "well_mapping", "inventory"}
        preview = client.post(f"/organizations/{own.id}/modules/preview", json={"organization_id": own.id, "enable_codes": ["selling"], "idempotency_key": "api-preview-1"})
        assert preview.status_code == 200
        apply_payload = {"organization_id": own.id, "enable_codes": ["selling"], "idempotency_key": "api-apply-1", "preview_hash": preview.json()["preview_hash"]}
        applied = client.post(f"/organizations/{own.id}/modules/apply", json=apply_payload)
        assert applied.status_code == 200
        assert applied.json()["effective"]["items"]
        assert client.get(f"/organizations/{other.id}/modules").status_code == 200
        app.dependency_overrides[get_current_user] = lambda: member
        assert client.get(f"/organizations/{other.id}/modules").status_code == 403
        assert client.post(f"/organizations/{own.id}/modules/apply", json={"organization_id": own.id, "enable_codes": ["crm"], "idempotency_key": "member-apply-1"}).status_code == 403
    finally:
        settings.feature_flags = previous_flags
        app.dependency_overrides.clear()


def test_dependency_cycles_and_incompatibilities_fail_closed():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="p3-rules@example.test", full_name="P3 Rules", password="local-password-123", organization_name="Rules Workspace", membership_role="owner", is_platform_admin=True))
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Rules Company"))
    from app.models.domain import Module
    crm = session.execute(select(Module).where(Module.code == "crm")).scalar_one()
    accounting = session.execute(select(Module).where(Module.code == "accounting")).scalar_one()
    original_crm_dependencies, original_accounting_incompatibilities = crm.dependency_codes_json, accounting.incompatibility_codes_json
    try:
        accounting.incompatibility_codes_json = ["crm"]
        with __import__("pytest").raises(ModuleEntitlementValidationError, match="incompatible"):
            ModuleEntitlementService().preview(session, ModuleChangeRequest(organization_id=organization.id, enable_codes=["selling", "crm"], idempotency_key="rules-incompat"))
        crm.dependency_codes_json = ["support"]
        session.commit()
        support = session.execute(select(Module).where(Module.code == "support")).scalar_one()
        support.dependency_codes_json = ["crm"]
        session.commit()
        with __import__("pytest").raises(ModuleEntitlementValidationError, match="cycle"):
            ModuleEntitlementService().preview(session, ModuleChangeRequest(organization_id=organization.id, enable_codes=["crm"], idempotency_key="rules-cycle"))
    finally:
        crm.dependency_codes_json = original_crm_dependencies
        accounting.incompatibility_codes_json = original_accounting_incompatibilities
        support = session.execute(select(Module).where(Module.code == "support")).scalar_one()
        support.dependency_codes_json = ["crm"] if support.code == "support" else support.dependency_codes_json
        session.commit()


def test_explicit_disable_cannot_be_reintroduced_by_dependency_closure():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="p3-disable@example.test", full_name="P3 Disable", password="local-password-123", organization_name="Disable Workspace", membership_role="owner", is_platform_admin=True))
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Disable Company"))
    accounting = session.execute(select(_models.Module).where(_models.Module.code == "accounting")).scalar_one()
    session.add(OrganizationModule(organization_id=organization.id, module_id=accounting.id, status="disabled", explicit_state="disabled", requested_state="disabled", entitled_state="not_entitled"))
    session.commit()
    with __import__("pytest").raises(ModuleEntitlementValidationError, match="Dependency conflict"):
        ModuleEntitlementService().preview(session, ModuleChangeRequest(organization_id=organization.id, enable_codes=["selling"], idempotency_key="disable-conflict"), actor=actor)


def test_stale_actor_bound_preview_is_rejected():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="p3-stale@example.test", full_name="P3 Stale", password="local-password-123", organization_name="Stale Workspace", membership_role="owner", is_platform_admin=True))
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Stale Company"))
    service = ModuleEntitlementService()
    first = ModuleChangeRequest(organization_id=organization.id, enable_codes=["crm"], idempotency_key="stale-first")
    preview = service.preview(session, first, actor=actor)
    second = ModuleChangeRequest(organization_id=organization.id, enable_codes=["stock"], idempotency_key="stale-second")
    second_preview = service.preview(session, second, actor=actor)
    second.preview_hash = second_preview.preview_hash
    service.apply(session, actor, second)
    first.preview_hash = preview.preview_hash
    with __import__("pytest").raises(ModuleEntitlementValidationError, match="stale"):
        service.apply(session, actor, first)


def test_bundle_is_versioned_proposal_and_persists_source():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="p3-bundle@example.test", full_name="P3 Bundle", password="local-password-123", organization_name="Bundle Workspace", membership_role="owner", is_platform_admin=True))
    actor = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, actor, OrganizationCreateRequest(name="Bundle Company"))
    service = ModuleEntitlementService()
    bundles = service.list_bundles(session)
    assert any(bundle.bundle_key == "champion-drilling" and bundle.version == 1 for bundle in bundles)
    request = ModuleChangeRequest(organization_id=organization.id, bundle_key="generic-field-service", bundle_version=1, idempotency_key="bundle-apply-1")
    preview = service.preview(session, request, actor=actor)
    request.preview_hash = preview.preview_hash
    result = service.apply(session, actor, request)
    assert result.effective.effective_codes
    audit = session.execute(select(ModuleEntitlementAudit).where(ModuleEntitlementAudit.organization_id == organization.id)).scalar_one()
    assert audit.source_type == "bundle"
    assert audit.source_ref == "generic-field-service@1"


def test_released_catalog_and_bundle_versions_are_seed_immutable():
    session = make_session()
    module = session.execute(select(_models.Module).where(_models.Module.code == "stock")).scalar_one()
    bundle = session.execute(select(_models.ModuleBundle).where(_models.ModuleBundle.bundle_key == "champion-drilling", _models.ModuleBundle.version == 1)).scalar_one()
    item = session.execute(select(_models.ModuleBundleItem).where(_models.ModuleBundleItem.bundle_id == bundle.id)).scalars().first()
    module.name = "Operator-owned Stock Metadata"
    module.is_active = False
    if item is not None:
        session.delete(item)
    session.commit()
    seed_reference_data(session)
    session.expire_all()
    assert session.execute(select(_models.Module).where(_models.Module.code == "stock")).scalar_one().name == "Operator-owned Stock Metadata"
    assert session.execute(select(_models.Module).where(_models.Module.code == "stock")).scalar_one().is_active is False
    if item is not None:
        assert session.execute(select(_models.ModuleBundleItem).where(_models.ModuleBundleItem.id == item.id)).scalar_one_or_none() is None
