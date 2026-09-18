from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parents[2]


def test_erp_demo_smoke_is_staging_only_and_explicitly_seeded():
    script = (ROOT / "scripts" / "release" / "erp_demo_smoke.sh").read_text(encoding="utf-8")
    assert "erp-staging.example.test" in script
    assert "lenerp_core.demo_seed.seed" in script
    assert "lenerp_core.demo_seed.reset" in script
    assert "KEEP_DEMO" in script
    assert "lenerp.lengrowth.com" not in script
    assert "erp.lengrowth.com" not in script


def test_staging_smoke_defaults_to_the_synthetic_demo_app_version():
    script = (ROOT / "scripts" / "release" / "erp_staging_smoke.sh").read_text(encoding="utf-8")
    assert "EXPECTED_CUSTOM_APP_VERSION:-0.2.0" in script


def test_staging_workflow_installs_the_exact_custom_app_ref():
    workflow = (ROOT / ".github" / "workflows" / "deploy-saas-control.yml").read_text(encoding="utf-8")
    assert "Len-OS/lenerp_core" in workflow
    assert "custom_app_ref" in workflow
    assert "bench --site erp-staging.example.test migrate" in workflow
    assert "erp_demo_smoke.sh" in workflow
