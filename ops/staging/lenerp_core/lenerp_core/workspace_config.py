"""Version-controlled Champion workspace and role-home configuration.

This module is deliberately data-only. It describes presentation and route
intent; Frappe remains the authorization source for every DocType and report.
"""

from __future__ import annotations

PHASE4_FLAG = "lenerp_phase4_workspace_enabled"
PHASE4_ROLE_ROLLOUT = "lenerp_phase4_role_rollout"

ROLE_HOMES: dict[str, dict[str, object]] = {
    "Champion Administrator": {
        "key": "administration",
        "label": "Administration",
        "purpose": "Keep the Champion workspace, people, records, and configuration moving safely.",
        "actions": [
            {"label": "Open Office Board", "nav": "office"},
            {"label": "Review Customers & Sales", "nav": "sales"},
            {"label": "Open Reports", "nav": "reports"},
        ],
        "sources": ["customers", "jobs", "issues"],
        "nav": "all",
    },
    "Champion Dispatcher": {
        "key": "office-dispatch",
        "label": "Office / Dispatch",
        "purpose": "Coordinate customers, jobs, and the work that needs an office decision.",
        "actions": [
            {"label": "Open Office Board", "nav": "office"},
            {"label": "Schedule a job", "nav": "jobs"},
            {"label": "Find a customer", "nav": "sales"},
        ],
        "sources": ["jobs", "customers", "issues"],
        "nav": ["home", "office", "sales", "jobs", "equipment", "quality", "support", "reports"],
    },
    "Champion Sales User": {
        "key": "sales",
        "label": "Sales",
        "purpose": "Move customer conversations and quotes forward with the records already in ERPNext.",
        "actions": [
            {"label": "Find customers", "nav": "sales"},
            {"label": "Open a quote", "nav": "quotes"},
            {"label": "Review reports", "nav": "reports"},
        ],
        "sources": ["customers", "quotes", "issues"],
        "nav": ["home", "sales", "jobs", "support", "reports"],
    },
    "Champion Accounting User": {
        "key": "accounting",
        "label": "Accounting",
        "purpose": "Review accounting work in the standard ERPNext records you are authorized to see.",
        "actions": [
            {"label": "Open invoices", "nav": "accounting"},
            {"label": "Review payments", "nav": "accounting"},
            {"label": "Open reports", "nav": "reports"},
        ],
        "sources": ["invoices", "payments", "customers"],
        "nav": ["home", "sales", "accounting", "reports"],
    },
    "Champion Inventory Manager": {
        "key": "inventory",
        "label": "Inventory",
        "purpose": "Keep items, purchasing, stock movements, and equipment work visible in one place.",
        "actions": [
            {"label": "Open inventory", "nav": "inventory"},
            {"label": "Review purchasing", "nav": "inventory"},
            {"label": "Check equipment", "nav": "equipment"},
        ],
        "sources": ["items", "purchasing", "assets"],
        "nav": ["home", "inventory", "equipment", "reports"],
    },
    "Champion Field Technician": {
        "key": "field",
        "label": "Field",
        "purpose": "See assigned wells, jobs, and equipment work without leaving the operational records.",
        "actions": [
            {"label": "Open Wells & Jobs", "nav": "jobs"},
            {"label": "Review equipment", "nav": "equipment"},
            {"label": "Record work", "nav": "jobs"},
        ],
        "sources": ["jobs", "wells", "assets"],
        "nav": ["home", "jobs", "equipment", "crew", "quality", "reports"],
    },
    "Champion HR Payroll User": {
        "key": "hr-payroll",
        "label": "HR / Payroll",
        "purpose": "Open authorized people, hours, leave, and payroll records when HRMS is configured for this site.",
        "actions": [
            {"label": "Open Crew & Hours", "nav": "crew"},
            {"label": "Review leave", "nav": "crew"},
            {"label": "Open payroll", "nav": "accounting"},
        ],
        "sources": ["employees", "attendance", "leave", "payroll"],
        "nav": ["home", "crew", "accounting", "reports"],
    },
    "Champion Quality Support User": {
        "key": "quality-support",
        "label": "Quality / Support",
        "purpose": "Track issues, callbacks, and requests using standard support records and approved extensions.",
        "actions": [
            {"label": "Open Quality & Callbacks", "nav": "quality"},
            {"label": "Review Support & Requests", "nav": "support"},
            {"label": "Open reports", "nav": "reports"},
        ],
        "sources": ["issues", "jobs", "customers"],
        "nav": ["home", "sales", "jobs", "quality", "support", "reports"],
    },
    "Champion Read Only User": {
        "key": "read-only",
        "label": "Read-only",
        "purpose": "Review authorized operational records without editing or creating work.",
        "actions": [
            {"label": "Review customers", "nav": "sales"},
            {"label": "Review Wells & Jobs", "nav": "jobs"},
            {"label": "Open reports", "nav": "reports"},
        ],
        "sources": ["customers", "wells", "jobs"],
        "nav": ["home", "sales", "jobs", "equipment", "reports"],
    },
}

NAVIGATION: dict[str, dict[str, object]] = {
    "home": {"label": "Home", "route": "/champion-home"},
    "office": {"label": "Office Board", "route": "/app/project", "doctype": "Project"},
    "sales": {"label": "Customers & Sales", "route": "/app/selling", "doctype": "Customer"},
    "jobs": {"label": "Wells & Jobs", "route": "/app/len-erp-drilling-job", "doctype": "LenERP Drilling Job"},
    "inventory": {"label": "Inventory & Purchasing", "route": "/app/stock", "doctype": "Item"},
    "equipment": {"label": "Trucks & Equipment", "route": "/app/asset", "doctype": "Asset"},
    "crew": {"label": "Crew & Hours", "route": "/app/employee", "doctype": "Employee"},
    "quality": {"label": "Quality & Callbacks", "route": "/app/issue", "doctype": "Issue"},
    "support": {"label": "Support & Requests", "route": "/app/issue", "doctype": "Issue"},
    "accounting": {"label": "Accounting & Payroll", "route": "/app/accounts", "doctype": "Sales Invoice"},
    "reports": {"label": "Reports", "route": "/app/query-report", "doctype": "Report"},
}

ROLE_ALIASES: dict[str, str] = {
    "System Manager": "Champion Administrator",
    "Projects User": "Champion Dispatcher",
    "Sales User": "Champion Sales User",
    "Accounts User": "Champion Accounting User",
    "Stock User": "Champion Inventory Manager",
    "Employee": "Champion Read Only User",
}


def role_for_roles(roles: list[str] | tuple[str, ...] | set[str]) -> str | None:
    """Return the deterministic Champion role with the narrowest ambiguity."""
    for role in ROLE_HOMES:
        if role in roles:
            return role
    for role, champion_role in ROLE_ALIASES.items():
        if role in roles:
            return champion_role
    return None


def navigation_for_role(role: str) -> list[dict[str, object]]:
    home = ROLE_HOMES[role]
    configured = home["nav"]
    keys = list(NAVIGATION) if configured == "all" else list(configured)
    return [{"id": key, **NAVIGATION[key]} for key in keys]
