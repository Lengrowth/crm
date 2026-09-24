from __future__ import annotations

import frappe

from lenerp_core.phase4 import page_context


no_cache = 1


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw("Sign in through LenERP Control Plane to open the Champion workspace.", frappe.PermissionError)
    context.update(page_context())
    return context
