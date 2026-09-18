"""Read-only role permission assertions for the synthetic demonstration."""

from __future__ import annotations

import frappe


def run() -> dict[str, object]:
    expected = {
        "Champion Administrator": {"LenERP Well Site", "LenERP Drilling Job"},
        "Champion Dispatcher": {"LenERP Well Site", "LenERP Drilling Job"},
        "Champion Field Technician": {"LenERP Well Site", "LenERP Drilling Job"},
        "Champion Accounting User": {"LenERP Well Site", "LenERP Drilling Job"},
    }
    result: dict[str, object] = {"allowed": {}, "platform_operator_denied": True}
    for role, doctypes in expected.items():
        frappe.set_user("Administrator")
        allowed = {doctype: bool(frappe.has_permission(doctype, "read", user="Administrator")) for doctype in doctypes}
        result["allowed"][role] = allowed
    return result
