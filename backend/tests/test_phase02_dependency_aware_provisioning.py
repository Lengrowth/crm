from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.db.seed import seed_reference_data
from app.integrations.mock_erpnext import MockERPNextClient
from app.models.domain import Module
from app.services.application_resolver import calculate_required_applications
from app.services.module_entitlement_service import ModuleEntitlementService, ModuleEntitlementValidationError
from app.services.onboarding_service import STEP_DEFINITIONS, step_definitions_for_request


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
    assert [item.required_by for item in resolution.ordered if item.pin.name == "hrms"] == [("hr", "payroll")]


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
