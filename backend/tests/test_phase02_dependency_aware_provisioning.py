from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.db.seed import seed_reference_data
from app.integrations.mock_erpnext import MockERPNextClient
from app.integrations.frappe_bench import FrappeBenchERPNextClient
from app.models.domain import Module
from app.services.application_resolver import calculate_required_applications, compare_installed_applications
from app.services.module_entitlement_service import ModuleEntitlementService, ModuleEntitlementValidationError
from app.services.onboarding_service import STEP_DEFINITIONS, step_definitions_for_request
from app.workers.provisioning_worker import StepFailure, _application_resolution


def make_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, future=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autoflush=False, future=True)()
    seed_reference_data(session)
    return session


def test_application_resolver_omits_hrms_without_people_modules():
    resolution = calculate_required_applications([
        {"code": "stock", "required_app": "erpnext"},
        {"code": "well_mapping", "required_app": "lenerp_core"},
    ])

    assert resolution.applications == ("frappe", "erpnext", "lenerp_core")
    assert "hrms" not in resolution.applications
    assert resolution.platform_applications == ("frappe", "erpnext", "lenerp_core")


def test_application_resolver_adds_hrms_once_in_stable_order():
    resolution = calculate_required_applications([
        {"code": "payroll", "required_app": "hrms"},
        {"code": "hr", "required_app": "hrms"},
        {"code": "quality", "required_app": "erpnext"},
    ])

    assert resolution.applications == ("frappe", "erpnext", "hrms", "lenerp_core")
    assert resolution.exact_versions["hrms"] == "15.64.1"
    assert resolution.commits["hrms"] == "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1"
    assert resolution.unverified_applications == ()
    assert [item.required_by for item in resolution.ordered if item.pin.name == "hrms"] == [("hr", "payroll")]


def test_exact_application_commit_readback_is_required():
    resolution = calculate_required_applications([{"code": "stock", "required_app": "erpnext"}])
    installed = {"frappe": "15.119.1", "erpnext": "15.120.0", "lenerp_core": "0.2.0"}
    commits = {"frappe": "edae775dd36b6c4ad7acab10230262bd74040765", "erpnext": "wrong", "lenerp_core": "a7e47208baf6583295f5f2632f4787262cd3f475"}
    missing, incompatible = compare_installed_applications(installed, resolution, commits)
    assert missing == []
    assert any(item.startswith("erpnext commit") for item in incompatible)


def test_verified_hrms_pin_is_allowed_before_provider_mutation():
    session = make_session()
    resolution = _application_resolution(session, ["hr"])
    assert resolution.exact_versions["hrms"] == "15.64.1"


def test_cyclic_module_dependency_rejected_before_provider_mutation():
    session = make_session()
    session.add_all([
        Module(code="cycle_a", name="Cycle A", is_active=True, dependency_codes_json=["cycle_b"], default_roles_json=[], default_workspaces_json=[]),
        Module(code="cycle_b", name="Cycle B", is_active=True, dependency_codes_json=["cycle_a"], default_roles_json=[], default_workspaces_json=[]),
    ])
    session.commit()
    client = MockERPNextClient()

    with pytest.raises(ModuleEntitlementValidationError, match="Dependency cycle"):
        ModuleEntitlementService().resolve_requested_codes(session, ["cycle_a"])

    assert client.sites == {}


def test_hrms_step_is_only_added_for_effective_hrms_requirement():
    session = make_session()
    no_hr_steps = step_definitions_for_request(session, ["stock"], None, None)
    hr_steps = step_definitions_for_request(session, ["hr"], None, None)

    assert no_hr_steps == STEP_DEFINITIONS
    assert "install_pinned_hrms" not in {key for key, _ in no_hr_steps}
    assert "install_pinned_hrms" in {key for key, _ in hr_steps}
    assert hr_steps.index(("install_lenerp_custom_app", ("install_pinned_hrms",))) > hr_steps.index(("install_pinned_hrms", ("install_pinned_erpnext",)))


def test_mock_provider_install_and_migration_are_replay_safe_and_version_checked():
    client = MockERPNextClient()
    site_id = str(client.create_site("org", "tenant", {})["site_id"])
    assert client.install_app(site_id, "hrms")["status"] == "success"
    assert client.install_app(site_id, "hrms")["replayed"] is True
    assert client.migrate_site(site_id)["status"] == "success"
    assert client.migrate_site(site_id)["status"] == "success"

    inventory = client.get_site_inventory(site_id)
    assert inventory["installed_apps"]["hrms"] == "15.64.1"
    assert client.verify_site_configuration(site_id, [], required_app_versions={"hrms": "15.64.0"})["provider_verified"] is False


def test_native_role_workspace_and_commit_readback_controls_verification():
    client = MockERPNextClient()
    site_id = str(client.create_site("org", "tenant", {})["site_id"])
    client.install_app(site_id, "erpnext")
    client.install_app(site_id, "lenerp_core")
    client.apply_site_configuration(site_id, {"modules": ["stock"], "roles": ["stock_user"], "workspaces": ["Stock"]})
    verified = client.verify_site_configuration(
        site_id,
        ["stock"],
        required_apps={"stock": "erpnext"},
        required_roles=["stock_user"],
        required_workspaces=["Stock"],
        required_app_versions={"erpnext": "15.120.0"},
        required_app_commits={"erpnext": "945e825bee3d0d645f6cb59bcaab90fcbfb98ce3"},
    )
    assert verified["provider_verified"] is True
    client.sites[site_id]["app_commits"]["erpnext"] = "wrong"
    incompatible = client.verify_site_configuration(site_id, ["stock"], required_app_commits={"erpnext": "945e825bee3d0d645f6cb59bcaab90fcbfb98ce3"})
    assert incompatible["provider_verified"] is False
    assert any("945e825bee3d0d645f6cb59bcaab90fcbfb98ce3" in item for item in incompatible["incompatible_apps"])


def test_frappe_provider_fails_closed_after_upstream_fixture_failure(monkeypatch):
    client = object.__new__(FrappeBenchERPNextClient)
    calls: list[tuple[str, ...]] = []

    monkeypatch.setattr(client, "_site_exists", lambda site_id: True)
    monkeypatch.setattr(client, "_list_apps", lambda site_id: set())

    results = iter([False])

    def run(args, **kwargs):
        calls.append(tuple(args))
        return next(results), ""

    monkeypatch.setattr(client, "_run", run)

    result = client.install_app("phase4-synthetic.example.test", "hrms")

    assert result["status"] == "failed"
    assert result["provider_verified"] is False
    assert calls == [
        ("--site", "phase4-synthetic.example.test", "install-app", "hrms"),
    ]
