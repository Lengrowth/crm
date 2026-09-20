from __future__ import annotations

import tarfile
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
    assert "after 60s" in script


def test_staging_workflow_verifies_the_installed_custom_app_candidate():
    workflow = (ROOT / ".github" / "workflows" / "deploy-saas-control.yml").read_text(encoding="utf-8")
    baseline = (ROOT / "ops" / "staging" / "release-runtime-baseline.json").read_text(encoding="utf-8")
    bundle_commit = (ROOT / "ops" / "staging" / "lenerp_core" / "SOURCE_COMMIT.txt").read_text(encoding="utf-8").strip()
    assert 'CUSTOM_APP_VERSION: "0.2.0"' in workflow
    assert 'CUSTOM_APP_COMMIT="$core_commit"' in workflow
    assert 'SOURCE_COMMIT.txt' in workflow
    assert bundle_commit == "22af1680dd386d33c35641f7253048db4c40c051"
    assert "lenerp_core-${core_commit}.tar" in workflow
    assert 'staging.joinpath("lenerp_core.archive.sha256")' in workflow
    assert '"version": "0.2.0"' in baseline
    assert '"commit": "22af1680dd386d33c35641f7253048db4c40c051"' in baseline
    assert "erp_staging_smoke.sh" in workflow
    assert "erp_demo_smoke.sh" in workflow
    assert "erp_role_smoke.sh" in workflow
    assert "capture_erp_browser_evidence.mjs" in workflow
    assert "erp_demo_cleanup.sh" in workflow
    assert "bench build --app lenerp_core" in workflow
    assert "Verify candidate ancestry from authoritative main" in workflow
    assert 'CUSTOM_APP_COMMIT="$core_commit"' in workflow
    assert "Write candidate-bound protected staging evidence manifest" in workflow
    assert '"candidate-bound-evidence-manifest.json"' in workflow
    assert '"runtime_readback": runtime_readback' in workflow
    assert '"documentation": {' in workflow
    assert 'documentation_target = evidence_dir / "documentation"' in workflow
    archive = ROOT / "ops" / "staging" / "lenerp_core-22af1680dd386d33c35641f7253048db4c40c051.tar"
    with tarfile.open(archive, mode="r:*") as handle:
        assert "lenerp_core/public/js/accessibility.js" in handle.getnames()


def test_browser_evidence_is_route_bound_and_checks_zoom_logo_and_language_contracts():
    erp_script = (ROOT / "frontend" / "scripts" / "capture_erp_browser_evidence.mjs").read_text(encoding="utf-8")
    control_script = (ROOT / "frontend" / "scripts" / "capture_browser_evidence.mjs").read_text(encoding="utf-8")
    assert "renderedAccessibilityContract" in erp_script
    assert "viewport_count" in erp_script
    assert "logo_alternatives_present" in erp_script
    assert 'role: "unauthenticated"' in erp_script
    assert "Object.values(evidence.accessibility.routes)" in erp_script
    assert "incompleteReviewed" in erp_script
    assert "manual_review" in erp_script
    assert "dashboard_summary" in erp_script
    assert "inventory_exceptions" in erp_script
    assert "well_history" in erp_script
    assert "operational alerts" in erp_script
    assert "language_audit" in control_script
    assert "internalLanguagePatterns" in control_script
