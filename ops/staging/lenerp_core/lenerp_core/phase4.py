"""Server-controlled Champion Phase 04 workspace boundary."""

from __future__ import annotations

import json
from typing import Any

import frappe

from lenerp_core.workspace_config import (
    PHASE4_FLAG,
    PHASE4_ROLE_ROLLOUT,
    ROLE_HOMES,
    navigation_for_role,
    role_for_roles,
)


def _truthy(value: object) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on", "enabled"}


def current_role(roles: list[str] | None = None) -> str | None:
    return role_for_roles(roles or list(frappe.get_roles()))


def enabled_for_roles(roles: list[str] | None = None) -> bool:
    if not _truthy(frappe.conf.get(PHASE4_FLAG, "0")):
        return False
    role = current_role(roles)
    if role is None:
        return False
    raw_rollout = frappe.conf.get(PHASE4_ROLE_ROLLOUT)
    if not raw_rollout:
        return True
    try:
        rollout = json.loads(raw_rollout) if isinstance(raw_rollout, str) else raw_rollout
    except (TypeError, ValueError, json.JSONDecodeError):
        return False
    if not isinstance(rollout, dict):
        return False
    return rollout.get(role) is True


def _require_enabled() -> str:
    role = current_role()
    if not enabled_for_roles():
        frappe.throw("The Champion workspace is not enabled for this role.", frappe.PermissionError)
    if role is None:
        frappe.throw("A Champion role is required for this workspace.", frappe.PermissionError)
    return role


def extend_bootinfo(bootinfo: dict[str, Any]) -> None:
    role = current_role()
    bootinfo["lenerp_phase4_workspace"] = {
        "enabled": bool(role and enabled_for_roles()),
        "role": role,
        "flag": PHASE4_FLAG,
    }

def page_context() -> dict[str, object]:
    role = _require_enabled()
    home = ROLE_HOMES[role]
    organization = str(frappe.conf.get("lenerp_control_plane_organization_name") or "").strip()
    environment = str(frappe.conf.get("lenerp_environment") or "").strip()
    return {
        "product": str(frappe.conf.get("lenerp_product_name") or "LenERP"),
        "organization": organization or "Pending configuration",
        "environment": environment or "Pending configuration",
        "role": role,
        "role_label": home["label"],
        "destination": "Champion ERP",
        "help_url": str(frappe.conf.get("lenerp_help_url") or "https://docs.frappe.io/erpnext/user/manual/en"),
        "navigation": navigation_for_role(role),
        "home": {key: home[key] for key in ("key", "label", "purpose", "actions")},
    }
