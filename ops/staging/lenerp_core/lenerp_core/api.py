"""Small, permission-aware read API for the Champion demonstration dashboard."""

from __future__ import annotations

import frappe

from lenerp_core.demo_seed import (
    DEMO_COMPANY,
    DEMO_ITEM_PUMP,
    DEMO_ITEM_RIG,
    DEMO_JOB_IDS,
    DEMO_PREFIX,
    DEMO_WELL_IDS,
)


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
        filters={"job_id": ["in", DEMO_JOB_IDS]},
        fields=["name", "customer", "well_site", "job_type", "status", "scheduled_date", "priority"],
        order_by="scheduled_date asc",
    )
    wells = frappe.get_all(
        "LenERP Well Site",
        filters={"well_id": ["in", DEMO_WELL_IDS]},
        fields=["name", "well_id", "site_name", "customer", "city", "latitude", "longitude", "depth_m", "status"],
        order_by="site_name asc",
    )
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={"customer": ["like", "DEMO-%"]},
        fields=["name", "customer", "grand_total", "status", "outstanding_amount", "posting_date"],
        order_by="posting_date desc",
    )
    inventory_bins = frappe.get_all(
        "Bin",
        filters={"item_code": ["in", [DEMO_ITEM_PUMP, DEMO_ITEM_RIG]]},
        fields=["item_code", "warehouse", "actual_qty", "reserved_qty", "ordered_qty", "projected_qty"],
        order_by="item_code asc, warehouse asc",
    )
    inventory_exceptions = [
        {
            "item_code": row.item_code,
            "warehouse": row.warehouse,
            "actual_qty": row.actual_qty,
            "reserved_qty": row.reserved_qty,
            "projected_qty": row.projected_qty,
            "exception_type": "projected stock below zero",
        }
        for row in inventory_bins
        if (row.projected_qty or 0) < 0
        or (row.actual_qty or 0) < (row.reserved_qty or 0)
    ]
    assets = frappe.get_all(
        "Asset",
        filters={"company": DEMO_COMPANY},
        fields=["name", "asset_name", "status", "maintenance_required", "location"],
        order_by="asset_name asc",
    )
    maintenance_records = frappe.get_all(
        "Asset Maintenance",
        filters={"company": DEMO_COMPANY},
        fields=["name", "asset_name", "maintenance_team"],
        order_by="creation desc",
    )
    maintenance_status = []
    for record in maintenance_records:
        maintenance_doc = frappe.get_doc("Asset Maintenance", record.name)
        tasks = [
            {
                "task": task.maintenance_task,
                "status": task.maintenance_status,
                "start_date": task.start_date,
                "periodicity": task.periodicity,
            }
            for task in maintenance_doc.get("asset_maintenance_tasks", [])
        ]
        maintenance_status.append(
            {
                "name": record.name,
                "asset_name": record.asset_name,
                "maintenance_team": record.maintenance_team,
                "status": next(
                    (task["status"] for task in tasks if task["status"]),
                    "Planned",
                ),
                "tasks": tasks,
            }
        )

    well_history = []
    for well in wells:
        linked_jobs = [
            {
                "name": job.name,
                "job_type": job.job_type,
                "status": job.status,
                "scheduled_date": job.scheduled_date,
                "priority": job.priority,
            }
            for job in jobs
            if job.well_site == well.name
        ]
        well_history.append(
            {
                "well": well.name,
                "well_id": well.well_id,
                "site_name": well.site_name,
                "customer": well.customer,
                "status": well.status,
                "events": linked_jobs,
                "event_count": len(linked_jobs),
            }
        )

    alerts = []
    for job in jobs:
        if job.status in {"In Progress", "Reopened"} or job.priority in {"High", "Emergency"}:
            alerts.append(
                {
                    "type": "job attention",
                    "severity": "warning" if job.status != "Reopened" else "danger",
                    "source": job.name,
                    "message": f"{job.name} is {job.status.lower()} and needs operational follow-up.",
                }
            )
    for well in wells:
        if well.status != "Active":
            alerts.append(
                {
                    "type": "well review",
                    "severity": "warning",
                    "source": well.name,
                    "message": f"{well.site_name} is marked {well.status.lower()}.",
                }
            )
    for record in maintenance_status:
        planned_tasks = [task for task in record["tasks"] if task["status"] not in {"Completed", "Cancelled"}]
        if planned_tasks:
            alerts.append(
                {
                    "type": "maintenance due",
                    "severity": "warning",
                    "source": record["name"],
                    "message": f"{record['asset_name']} has {len(planned_tasks)} maintenance task(s) requiring review.",
                }
            )
    for exception in inventory_exceptions:
        alerts.append(
            {
                "type": "inventory exception",
                "severity": "danger",
                "source": exception["item_code"],
                "message": f"{exception['item_code']} is below available stock at {exception['warehouse']}.",
            }
        )
    return {
        "dashboard_version": 2,
        "status": "synthetic",
        "source": "persisted ERPNext records",
        "real_data_authorized": False,
        "jobs": jobs,
        "wells": wells,
        "invoices": invoices,
        "inventory_exceptions": inventory_exceptions,
        "asset_status": assets,
        "maintenance_status": maintenance_status,
        "well_history": well_history,
        "alerts": alerts,
        "counts": {
            "jobs": len(jobs),
            "wells": len(wells),
            "invoices": len(invoices),
            "completed_jobs": sum(job.status == "Completed" for job in jobs),
            "inventory_exceptions": len(inventory_exceptions),
            "assets": len(assets),
            "maintenance_records": len(maintenance_status),
            "wells_with_history": sum(bool(item["events"]) for item in well_history),
            "alerts": len(alerts),
        },
    }
