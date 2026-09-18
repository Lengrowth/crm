"""Small, permission-aware read API for the Champion demonstration dashboard."""

from __future__ import annotations

import frappe

from lenerp_core.demo_seed import DEMO_PREFIX


ALLOWED_ROLES = {
    "Champion Administrator",
    "Champion Dispatcher",
    "Champion Sales User",
    "Champion Accounting User",
    "Champion Inventory Manager",
    "Champion Field Technician",
}


def _require_demo_role() -> None:
    if not ALLOWED_ROLES.intersection(set(frappe.get_roles())):
        frappe.throw("You do not have access to the Champion demonstration.", frappe.PermissionError)


@frappe.whitelist()
def demo_status() -> dict:
    _require_demo_role()
    return {"demo_prefix": DEMO_PREFIX, "status": "synthetic", "real_data_authorized": False}


@frappe.whitelist()
def dashboard_summary() -> dict:
    _require_demo_role()
    jobs = frappe.get_all(
        "LenERP Drilling Job",
        filters={"name": ["like", "DEMO-%"]},
        fields=["name", "customer", "well_site", "job_type", "status", "scheduled_date", "priority"],
        order_by="scheduled_date asc",
    )
    wells = frappe.get_all(
        "LenERP Well Site",
        filters={"name": ["like", "DEMO-%"]},
        fields=["name", "well_id", "site_name", "customer", "city", "latitude", "longitude", "depth_m", "status"],
        order_by="site_name asc",
    )
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={"name": ["like", "DEMO-%"]},
        fields=["name", "customer", "grand_total", "status", "outstanding_amount", "posting_date"],
        order_by="posting_date desc",
    )
    return {
        "status": "synthetic",
        "source": "persisted ERPNext records",
        "real_data_authorized": False,
        "jobs": jobs,
        "wells": wells,
        "invoices": invoices,
        "counts": {
            "jobs": len(jobs),
            "wells": len(wells),
            "invoices": len(invoices),
            "completed_jobs": sum(job.status == "Completed" for job in jobs),
        },
    }
