import frappe

from frappe.www.app import get_context as _get_context
from lenerp_core.sso import direct_visit, enabled


def get_context(context):
	if enabled() and frappe.session.user == "Guest":
		direct_visit("/app")
		return context
	return _get_context(context)
