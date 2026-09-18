from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
DOCTYPE_ROOT = ROOT / "lenerp_core" / "doctype"


def read_doctype(name: str) -> dict:
    return json.loads((DOCTYPE_ROOT / name / f"{name}.json").read_text(encoding="utf-8"))


def test_champion_doctypes_are_persisted_and_permission_scoped():
    well = read_doctype("lenerp_well_site")
    job = read_doctype("lenerp_drilling_job")

    assert well["name"] == "LenERP Well Site"
    assert job["name"] == "LenERP Drilling Job"
    assert any(field["fieldname"] == "latitude" for field in well["fields"])
    assert any(field["fieldname"] == "well_site" for field in job["fields"])
    assert {permission["role"] for permission in well["permissions"]} >= {
        "Champion Administrator",
        "Champion Dispatcher",
        "Champion Field Technician",
    }
    assert "Champion Platform Operator" not in {
        permission["role"] for permission in well["permissions"]
    }


def test_seed_is_explicit_and_reset_is_demo_prefix_scoped():
    seed = (ROOT / "lenerp_core" / "demo_seed.py").read_text(encoding="utf-8")
    assert "def seed()" in seed
    assert "def reset()" in seed
    assert "def status()" in seed
    assert "bench --site <staging-site> execute" in seed
    assert "DEMO-CHAMPION-" in seed
    assert "real_data" not in seed.lower()


def test_dashboard_api_states_persisted_source_and_real_data_boundary():
    api = (ROOT / "lenerp_core" / "api.py").read_text(encoding="utf-8")
    assert "source\": \"persisted ERPNext records\"" in api
    assert "real_data_authorized\": False" in api
    assert "frappe.get_all" in api
