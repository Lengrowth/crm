"""Installation-time configuration for the reusable LenERP Core app."""

from __future__ import annotations

import frappe


DEMO_ROLES = (
    "Champion Administrator",
    "Champion Dispatcher",
    "Champion Sales User",
    "Champion Accounting User",
    "Champion Inventory Manager",
    "Champion Field Technician",
    "Champion Platform Operator",
)


def _ensure_roles() -> None:
    for role in DEMO_ROLES:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert(
                ignore_permissions=True
            )


def _ensure_workflow_links() -> None:
    """Create linked workflow metadata before Frappe validates existing workflows."""
    states = {
        "Planned": "Primary",
        "Scheduled": "Info",
        "In Progress": "Warning",
        "Completed": "Success",
        "Reopened": "Danger",
    }
    for state, style in states.items():
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc(
                {
                    "doctype": "Workflow State",
                    "workflow_state_name": state,
                    "style": style,
                }
            ).insert(ignore_permissions=True)

    for action in ("Schedule", "Start work", "Complete", "Reopen"):
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc(
                {
                    "doctype": "Workflow Action Master",
                    "workflow_action_name": action,
                }
            ).insert(ignore_permissions=True)


def _ensure_workflow() -> None:
    """Create the job workflow only when the standard workflow is absent."""
    if frappe.db.exists("Workflow", "Champion Drilling Job"):
        return
    workflow = frappe.get_doc(
        {
            "doctype": "Workflow",
            "workflow_name": "Champion Drilling Job",
            "document_type": "LenERP Drilling Job",
            "workflow_state_field": "workflow_state",
            "is_active": 1,
            "send_email_alert": 0,
            "states": [
                {"state": "Planned", "doc_status": "0", "allow_edit": "Champion Dispatcher"},
                {"state": "Scheduled", "doc_status": "0", "allow_edit": "Champion Dispatcher"},
                {"state": "In Progress", "doc_status": "0", "allow_edit": "Champion Field Technician"},
                {"state": "Completed", "doc_status": "0", "allow_edit": "Champion Dispatcher"},
                {"state": "Reopened", "doc_status": "0", "allow_edit": "Champion Dispatcher"},
            ],
            "transitions": [
                {"state": "Planned", "action": "Schedule", "allow_self_approval": 1, "next_state": "Scheduled", "allowed": "Champion Dispatcher"},
                {"state": "Scheduled", "action": "Start work", "allow_self_approval": 1, "next_state": "In Progress", "allowed": "Champion Field Technician"},
                {"state": "In Progress", "action": "Complete", "allow_self_approval": 1, "next_state": "Completed", "allowed": "Champion Field Technician"},
                {"state": "Completed", "action": "Reopen", "allow_self_approval": 1, "next_state": "Reopened", "allowed": "Champion Dispatcher"},
            ],
        }
    )
    workflow.insert(ignore_permissions=True)


def _ensure_print_format() -> None:
    if frappe.db.exists("Print Format", "Champion Job Completion"):
        return
    frappe.get_doc(
        {
            "doctype": "Print Format",
            "name": "Champion Job Completion",
            "doc_type": "LenERP Drilling Job",
            "standard": "No",
            "custom_format": 1,
            "disabled": 0,
            "html": """
                <div style=\"font-family: sans-serif; max-width: 760px; margin: 0 auto;\">
                  <h1>{{ doc.name }}</h1>
                  <p><strong>{{ doc.job_type }}</strong> · {{ doc.status }} · {{ doc.scheduled_date }}</p>
                  <hr>
                  <p><strong>Customer:</strong> {{ doc.customer }}</p>
                  <p><strong>Well / site:</strong> {{ doc.well_site }}</p>
                  <p><strong>Crew:</strong> {{ doc.assigned_personnel or 'Not assigned' }}</p>
                  <h3>Work notes</h3><div>{{ doc.work_notes or '' }}</div>
                  <h3>Completion details</h3><div>{{ doc.completion_details or 'Not completed' }}</div>
                  <p style=\"margin-top: 3rem; color: #667085;\">Synthetic demonstration record. Confirm approved company and accounting values at Project Start.</p>
                </div>
            """,
        }
    ).insert(ignore_permissions=True)


def _ensure_standard_permissions() -> None:
    """Grant least-privilege demo roles access to standard ERPNext records."""
    doctypes = (
        "Customer", "Contact", "Address", "Lead", "Opportunity", "Quotation",
        "Sales Invoice", "Payment Entry", "Item", "Supplier", "Warehouse", "Asset",
        "Purchase Receipt", "Stock Entry", "Asset Maintenance", "Asset Maintenance Team",
    )
    permissions = {
        "read": 1,
        "write": 1,
        "create": 1,
        "submit": 1,
        "delete": 0,
        "cancel": 0,
        "print": 1,
        "export": 1,
        "share": 0,
    }
    allowed_doctypes = {
        "Champion Administrator": set(doctypes),
        "Champion Dispatcher": {"Customer", "Contact"},
        "Champion Sales User": {"Customer", "Contact", "Lead", "Opportunity", "Quotation", "Sales Invoice"},
        "Champion Accounting User": {"Customer", "Contact", "Sales Invoice", "Payment Entry"},
        "Champion Inventory Manager": {"Item", "Supplier", "Warehouse", "Purchase Receipt", "Stock Entry", "Asset"},
        "Champion Field Technician": {"Asset", "Asset Maintenance"},
    }
    for role, role_doctypes in allowed_doctypes.items():
        for parent in doctypes:
            if not frappe.db.exists("DocType", parent):
                continue
            existing = frappe.db.get_value(
                "Custom DocPerm",
                {"parent": parent, "role": role, "permlevel": 0},
                "name",
            )
            if parent not in role_doctypes:
                if existing:
                    frappe.db.set_value(
                        "Custom DocPerm",
                        existing,
                        {field: 0 for field in permissions},
                        update_modified=False,
                    )
                continue
            if existing:
                frappe.db.set_value(
                    "Custom DocPerm",
                    existing,
                    permissions,
                    update_modified=False,
                )
            else:
                frappe.get_doc({
                    "doctype": "Custom DocPerm",
                    "parent": parent,
                    "parenttype": "DocType",
                    "parentfield": "permissions",
                    "role": role,
                    "permlevel": 0,
                    **permissions,
                }).insert(ignore_permissions=True)


def after_install() -> None:
    _ensure_roles()
    _ensure_workflow_links()
    _ensure_workflow()
    _ensure_print_format()
    _ensure_standard_permissions()
    frappe.db.commit()


def before_migrate() -> None:
    _ensure_roles()
    _ensure_workflow_links()
    frappe.db.commit()


def after_migrate() -> None:
    _ensure_roles()
    _ensure_workflow_links()
    _ensure_workflow()
    _ensure_print_format()
    _ensure_standard_permissions()
    frappe.db.commit()
