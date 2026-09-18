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


def test_staging_workflow_verifies_the_installed_custom_app_candidate():
    workflow = (ROOT / ".github" / "workflows" / "deploy-saas-control.yml").read_text(encoding="utf-8")
    baseline = (ROOT / "ops" / "production" / "release-runtime-baseline.json").read_text(encoding="utf-8")
    assert 'CUSTOM_APP_VERSION: "0.2.0"' in workflow
    assert 'CUSTOM_APP_COMMIT: "b9343ac1eb95bc44b8f4bb2254e77047ade645e3"' in workflow
    assert '"version": "0.2.0"' in baseline
    assert '"commit": "b9343ac1eb95bc44b8f4bb2254e77047ade645e3"' in baseline
    assert "erp_staging_smoke.sh" in workflow
    assert "erp_demo_smoke.sh" in workflow
