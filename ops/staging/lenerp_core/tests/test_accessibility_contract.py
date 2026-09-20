from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).parents[1]
HOOKS = (ROOT / "lenerp_core" / "hooks.py").read_text(encoding="utf-8")
SCRIPT = (ROOT / "lenerp_core" / "public" / "js" / "accessibility.js").read_text(
    encoding="utf-8"
)
APP_TEMPLATE = (ROOT / "lenerp_core" / "www" / "app.html").read_text(encoding="utf-8")


def test_accessibility_asset_is_included_on_authenticated_and_public_shells():
    assert '"/assets/lenerp_core/js/accessibility.js"' in HOOKS
    assert '"/assets/lenerp_core/js/sso.js"' in HOOKS
    assert 'update_website_context = ["lenerp_core.accessibility.update_context"]' in HOOKS
    assert 'base_template = "lenerp_core/templates/base.html"' in HOOKS
    bundle = (ROOT / "lenerp_core" / "public" / "js" / "lenerp_core.bundle.js").read_text(encoding="utf-8")
    assert 'setAttribute("alt", name)' in bundle
    assert 'setAttribute("alt", "")' in bundle
    assert 'name="viewport" content="width=device-width, initial-scale=1"' in APP_TEMPLATE
    assert 'include "lenerp_core/public/js/accessibility.js"' in APP_TEMPLATE
    template = (ROOT / "lenerp_core" / "templates" / "base.html").read_text(encoding="utf-8")
    assert 'include "lenerp_core/public/js/accessibility.js"' in template


def test_rendered_shell_contract_removes_zoom_restrictions_and_labels_logos():
    assert 'meta[name="viewport"]' in SCRIPT
    assert 'width=device-width, initial-scale=1' in SCRIPT
    assert "user-scalable=no" not in SCRIPT
    assert "minimum-scale" not in SCRIPT
    assert 'setAttribute("alt", name)' in SCRIPT
    assert 'setAttribute("alt", "")' in SCRIPT
    assert 'setAttribute("aria-label", label || "Select option")' in SCRIPT
    assert ".app-logo" in SCRIPT
    assert ".splash img" in SCRIPT
