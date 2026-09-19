"""Exercise ERP permissions with real synthetic principals.

The smoke is intentionally fail-closed: it creates one user per Champion role,
checks allowed and denied DocType reads as those users, and never treats
Administrator's permissions as evidence for another role.
"""

from __future__ import annotations

import os
from pathlib import Path

import frappe


ROLE_SPECS = {
    "Champion Administrator": {"LenERP Well Site", "LenERP Drilling Job", "Customer", "Contact", "Quotation", "Sales Invoice"},
    "Champion Dispatcher": {"LenERP Well Site", "LenERP Drilling Job", "Customer", "Contact"},
    "Champion Sales User": {"Customer", "Contact", "Lead", "Opportunity", "Quotation", "Sales Invoice"},
    "Champion Accounting User": {"Customer", "Contact", "Sales Invoice", "Payment Entry"},
    "Champion Inventory Manager": {"Item", "Supplier", "Warehouse", "Purchase Receipt", "Stock Entry", "Asset"},
    "Champion Field Technician": {"LenERP Well Site", "LenERP Drilling Job", "Asset", "Asset Maintenance"},
    "Champion Platform Operator": set(),
}

DENIED_DOCTYPES = ("LenERP Well Site", "LenERP Drilling Job", "Customer", "Sales Invoice")


def _prefix() -> str:
    return os.environ.get("DEMO_ROLE_EMAIL_PREFIX", "champion-demo-role")


def role_users() -> dict[str, str]:
    return {role: f"{_prefix()}-{role.lower().replace(' ', '-')}@example.test" for role in ROLE_SPECS}


def _password() -> str:
    path = os.environ.get("DEMO_ROLE_PASSWORD_FILE")
    if not path:
        raise RuntimeError("DEMO_ROLE_PASSWORD_FILE is required for role-principal smoke")
    password = Path(path).read_text(encoding="utf-8").strip()
    if len(password) < 16:
        raise RuntimeError("demo role password must be at least 16 characters")
    return password


def prepare() -> dict[str, str]:
    """Create deterministic, synthetic users for each Champion role."""
    password = _password()
    users = role_users()
    for role, email in users.items():
        if frappe.db.exists("User", email):
            user = frappe.get_doc("User", email)
            user.enabled = 1
            user.new_password = password
            user.set("roles", [])
        else:
            user = frappe.get_doc(
                {
                    "doctype": "User",
                    "email": email,
                    "first_name": role,
                    "enabled": 1,
                    "send_welcome_email": 0,
                    "new_password": password,
                    "roles": [],
                }
            )
        user.append("roles", {"role": role})
        user.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.set_user("Administrator")
    return users


def _assert_read(user: str, doctype: str, expected: bool) -> bool:
    actual = bool(frappe.has_permission(doctype, "read", user=user))
    if actual != expected:
        raise AssertionError(f"{user} read permission for {doctype}: expected {expected}, got {actual}")
    return actual


def run() -> dict[str, object]:
    users = prepare()
    result: dict[str, object] = {"users": users, "allowed": {}, "denied": {}}
    for role, allowed_doctypes in ROLE_SPECS.items():
        user = users[role]
        frappe.set_user(user)
        allowed = {doctype: _assert_read(user, doctype, doctype in allowed_doctypes) for doctype in (*allowed_doctypes, *DENIED_DOCTYPES)}
        result["allowed"][role] = allowed
    platform_user = users["Champion Platform Operator"]
    frappe.set_user(platform_user)
    result["platform_operator_denied"] = {
        doctype: _assert_read(platform_user, doctype, False) for doctype in DENIED_DOCTYPES
    }
    frappe.set_user("Administrator")
    return result


def cleanup() -> dict[str, int]:
    """Delete only users created by this smoke's deterministic email prefix."""
    deleted = 0
    for email in role_users().values():
        if frappe.db.exists("User", email):
            frappe.delete_doc("User", email, ignore_permissions=True, force=True)
            deleted += 1
    frappe.db.commit()
    frappe.set_user("Administrator")
    return {"users": deleted}
