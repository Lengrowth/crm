from __future__ import annotations

from pathlib import Path
import tarfile


ROOT = Path(__file__).parents[2]
ERP_ARCHIVE = ROOT / "ops" / "staging" / f"lenerp_core-{(ROOT / 'ops' / 'staging' / 'lenerp_core' / 'SOURCE_COMMIT.txt').read_text(encoding='utf-8').strip()}.tar"


def erp_source(path: str) -> str:
    with tarfile.open(ERP_ARCHIVE) as archive:
        return archive.extractfile(f"lenerp_core/{path}").read().decode("utf-8")


def test_erp_callback_is_browser_bound_and_consumed_under_a_lock() -> None:
    source = erp_source("sso.py")
    assert "_STATE_COOKIE" in source
    assert "browser_binding" in source
    assert "secrets.compare_digest" in source
    assert "with frappe.db.advisory_lock" in source
    assert "manager.set_cookie" in source
    assert "samesite=\"Lax\"" in source


def test_mapping_schema_and_service_use_an_opaque_exchange_handle() -> None:
    schema = (ROOT / "backend" / "app" / "schemas" / "sso.py").read_text(encoding="utf-8")
    service = (ROOT / "backend" / "app" / "services" / "sso_service.py").read_text(encoding="utf-8")
    assert "exchange_handle" in schema
    assert "mapping_handle_hash" in service
    assert "mapping_handle_consumed_at" in service
    assert "payload.erp_user != user.email.lower()" in service
    assert "payload.organization_id" not in schema
    assert "payload.tenant_id" not in schema
    assert "payload.erp_site" not in schema


def test_jit_provisioning_has_duplicate_and_role_update_race_guards() -> None:
    source = erp_source("sso.py")
    assert "DuplicateEntryError" in source
    assert "FOR UPDATE" in source


def test_protected_staging_contract_covers_break_glass_and_rate_limit() -> None:
    source = (ROOT / "scripts" / "release" / "phase3_identity_staging.py").read_text(encoding="utf-8")
    workflow = (ROOT / ".github" / "workflows" / "deploy-saas-control.yml").read_text(encoding="utf-8")
    browser = (ROOT / "frontend" / "scripts" / "capture_phase3_identity_evidence.mjs").read_text(encoding="utf-8")
    assert '"sso_rate_limit_429"' in source
    assert '"concurrent_code_replay_single_winner"' in source
    assert '"before_enable"' in source
    assert '"sso_enabled"' in source
    assert '"after_rollback"' in source
    assert "session_isolation" in browser
    assert "victim_callback_denied" in browser
    assert "/app/asset-maintenance" in browser
    assert "--phase before_enable" in workflow
    assert "--phase sso_enabled" in workflow
    assert "--phase after_rollback" in workflow
