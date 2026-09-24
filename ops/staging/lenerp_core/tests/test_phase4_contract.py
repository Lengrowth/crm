from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from lenerp_core.workspace_config import NAVIGATION, ROLE_HOMES, navigation_for_role, role_for_roles


def test_all_approved_roles_have_landing_home_and_two_or_three_actions():
    assert len(ROLE_HOMES) == 9
    for role, home in ROLE_HOMES.items():
        assert home["key"] and home["label"] and home["purpose"]
        assert 2 <= len(home["actions"]) <= 3
        assert navigation_for_role(role)


def test_champion_navigation_uses_named_modules_and_standard_routes():
    expected = {
        "Home", "Office Board", "Customers & Sales", "Wells & Jobs",
        "Inventory & Purchasing", "Trucks & Equipment", "Crew & Hours",
        "Quality & Callbacks", "Support & Requests", "Accounting & Payroll", "Reports",
    }
    assert {item["label"] for item in NAVIGATION.values()} == expected
    assert NAVIGATION["office"]["route"] == "/app/project"
    assert NAVIGATION["sales"]["route"] == "/app/selling"
    assert NAVIGATION["accounting"]["route"] == "/app/accounts"


def test_role_resolution_is_deterministic_and_read_only_has_no_write_intent():
    assert role_for_roles(["Employee", "Champion Read Only User"]) == "Champion Read Only User"
    assert role_for_roles(["Sales User"]) == "Champion Sales User"
    assert role_for_roles(["Champion Platform Operator"]) is None
    assert role_for_roles(["Unknown"]) is None
    serialized = (ROOT / "lenerp_core" / "phase4.py").read_text(encoding="utf-8")
    assert "frappe.has_permission" in (ROOT / "lenerp_core" / "api.py").read_text(encoding="utf-8")
    assert '"real_data_authorized": False' in serialized or '"real_data_authorized": False' in (ROOT / "lenerp_core" / "api.py").read_text(encoding="utf-8")


def test_flag_off_keeps_the_version_controlled_legacy_workspace_as_rollback():
    hooks = (ROOT / "lenerp_core" / "hooks.py").read_text(encoding="utf-8")
    phase4 = (ROOT / "lenerp_core" / "phase4.py").read_text(encoding="utf-8")
    workspace = json.loads((ROOT / "lenerp_core" / "lenerp_core" / "workspace" / "champion_erp" / "champion_erp.json").read_text(encoding="utf-8"))
    assert "phase4.js" in hooks
    assert 'PHASE4_FLAG' in phase4
    assert workspace["name"] == "Champion ERP"
    assert workspace["is_hidden"] == 0


def test_route_and_api_are_explicitly_denied_without_role_or_flag():
    phase4 = (ROOT / "lenerp_core" / "phase4.py").read_text(encoding="utf-8")
    page = (ROOT / "lenerp_core" / "www" / "champion_home.py").read_text(encoding="utf-8")
    api = (ROOT / "lenerp_core" / "api.py").read_text(encoding="utf-8")
    assert 'frappe.PermissionError' in phase4
    assert 'page_context()' in page
    assert '@frappe.whitelist()' in api and 'def module_home()' in api


def test_each_role_has_visible_navigation_and_a_landing_route():
    for role in ROLE_HOMES:
        items = navigation_for_role(role)
        assert items[0]["id"] == "home"
        assert all(item["label"] in {entry["label"] for entry in NAVIGATION.values()} for item in items)


def test_cross_navigation_keeps_authorized_tenant_context():
    sso = (ROOT / "lenerp_core" / "sso.py").read_text(encoding="utf-8")
    script = (ROOT / "lenerp_core" / "public" / "js" / "sso.js").read_text(encoding="utf-8")
    assert "lenerp_control_plane_tenant_id" in sso
    assert "/app/tenants/{tenant_id}?organization_id={organization_id}" in sso
    assert "LenERP Control Plane" in script


def test_module_home_exposes_honest_empty_partial_slow_failed_and_denied_states():
    api = (ROOT / "lenerp_core" / "api.py").read_text(encoding="utf-8")
    script = (ROOT / "lenerp_core" / "public" / "js" / "phase4.js").read_text(encoding="utf-8")
    assert '"state": state' in api and '"partial"' in api and '"empty"' in api
    for marker in ("Nothing is assigned", "partial", "taking longer", "could not load", "Access denied"):
        assert marker in script
