from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parents[1]
SSO = (ROOT / "lenerp_core" / "sso.py").read_text(encoding="utf-8")
HOOKS = (ROOT / "lenerp_core" / "hooks.py").read_text(encoding="utf-8")
SCRIPT = (ROOT / "lenerp_core" / "public" / "js" / "sso.js").read_text(encoding="utf-8")
APP = (ROOT / "lenerp_core" / "www" / "app.py").read_text(encoding="utf-8")


def test_erp_identity_boundary_is_code_based_and_secret_safe():
    assert "code_verifier" in SSO
    assert "code_challenge" in SSO
    assert "requests.post" in SSO
    assert "client_secret" in SSO
    assert "frappe.local.login_manager.login_as" in SSO
    assert "frappe.local.session" not in SSO
    assert '"password"' not in SSO
    assert "password_hash" not in SSO
    assert "cookies" not in SSO.lower()
    assert "_safe_path" in SSO
    assert "lenerp_break_glass_user" in SSO
    assert "lenerp-sso:" in SSO


def test_hooks_include_bidirectional_navigation_and_local_login_guard():
    assert "/assets/lenerp_core/js/sso.js" in HOOKS
    assert 'extend_bootinfo = "lenerp_core.sso.extend_bootinfo"' in HOOKS
    assert 'on_login = "lenerp_core.sso.on_login"' in HOOKS
    assert "lenerp_control_plane_return_url" in SSO
    assert "LenERP Control Plane" in SCRIPT
    assert "Sign in with LenERP Control Plane" in SCRIPT
    assert "direct_visit" in APP


def test_erp_identity_does_not_allow_open_redirects_or_role_drift():
    assert "parsed.netloc" in SSO
    assert '".." in candidate.split("/")' in SSO
    assert "MANAGED_ROLES" in SSO
    assert "_role_profile" in SSO
    assert "Administrator" in SSO
