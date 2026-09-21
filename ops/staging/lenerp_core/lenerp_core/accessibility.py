from __future__ import annotations


ASSET = "/assets/lenerp_core/js/accessibility.js"


def update_context(context):
    """Ensure the accessibility asset is present on public Frappe pages."""
    include_js = list(context.get("web_include_js") or [])
    if ASSET not in include_js:
        include_js.append(ASSET)
    return {"web_include_js": include_js}
