from __future__ import annotations

import frappe


def execute(filters=None):
    columns = [
        {"label": "Job", "fieldname": "name", "fieldtype": "Link", "options": "LenERP Drilling Job", "width": 160},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 180},
        {"label": "Well / site", "fieldname": "well_site", "fieldtype": "Link", "options": "LenERP Well Site", "width": 170},
        {"label": "Type", "fieldname": "job_type", "fieldtype": "Data", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Scheduled", "fieldname": "scheduled_date", "fieldtype": "Date", "width": 110},
        {"label": "Priority", "fieldname": "priority", "fieldtype": "Data", "width": 100},
    ]
    data = frappe.get_all(
        "LenERP Drilling Job",
        filters={"name": ["like", "DEMO-%"]},
        fields=[column["fieldname"] for column in columns],
        order_by="scheduled_date asc",
    )
    return columns, data
