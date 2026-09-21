import frappe

from frappe.www.app import get_context as _get_context
from lenerp_core.sso import direct_visit, enabled


def get_context(context):
	if enabled() and frappe.session.user == "Guest":
		requested_path = getattr(getattr(frappe.local, "request", None), "path", "/app") or "/app"
		direct_visit(requested_path if requested_path.startswith("/app") else "/app")
		return context
	return _get_context(context)
