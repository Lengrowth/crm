from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.models.domain import (
    ImplementationTaskStatus,
    ImplementationTemplate,
    Module,
    ModuleBundle,
    ModuleBundleItem,
    Plan,
)
from app.repositories.catalog_repository import CatalogRepository


DEFAULT_PLANS = [
    {
        "code": "starter",
        "name": "Starter",
        "description": "Local MVP plan with the smallest SaaS footprint.",
        "monthly_price_cents": 9900,
        "annual_price_cents": 99000,
        "default_modules_json": ["crm", "reporting"],
    },
    {
        "code": "growth",
        "name": "Growth",
        "description": "For teams that need more modules and tenant capacity.",
        "monthly_price_cents": 24900,
        "annual_price_cents": 249000,
        "default_modules_json": ["crm", "field_ops", "inventory", "reporting"],
    },
    {
        "code": "enterprise",
        "name": "Enterprise",
        "description": "Reserved for future manual-contract billing flows.",
        "monthly_price_cents": 0,
        "annual_price_cents": 0,
        "is_active": False,
        "default_modules_json": [],
    },
]

DEFAULT_TASK_STATUSES = [
    {"code": "todo", "name": "To Do", "sort_order": 10},
    {"code": "in_progress", "name": "In Progress", "sort_order": 20},
    {"code": "blocked", "name": "Blocked", "sort_order": 30},
    {"code": "review", "name": "In Review", "sort_order": 40},
    {"code": "done", "name": "Done", "sort_order": 50, "is_terminal": True},
    {"code": "cancelled", "name": "Cancelled", "sort_order": 60, "is_terminal": True},
]

DEFAULT_MODULES = [
    {"code": "accounting", "name": "Accounting", "category": "finance", "description": "General ledger, payables, receivables, and financial reporting.", "display_order": 10, "dependency_codes_json": [], "default_roles_json": ["accountant", "admin"], "default_workspaces_json": ["Accounting"], "required_app": "erpnext", "is_marketed": True},
    {"code": "buying", "name": "Buying", "category": "commercial", "description": "Supplier, purchasing, and procure-to-pay workflows.", "display_order": 20, "dependency_codes_json": ["accounting"], "default_roles_json": ["purchasing_manager", "admin"], "default_workspaces_json": ["Buying"], "required_app": "erpnext", "is_marketed": True},
    {"code": "selling", "name": "Selling", "category": "commercial", "description": "Quotes, orders, pricing, invoicing, and order-to-cash workflows.", "display_order": 30, "dependency_codes_json": ["accounting"], "default_roles_json": ["sales_user", "admin"], "default_workspaces_json": ["Selling"], "required_app": "erpnext", "is_marketed": True},
    {"code": "stock", "name": "Stock", "category": "operations", "description": "Items, warehouses, batches, serials, and stock movements.", "display_order": 40, "dependency_codes_json": [], "default_roles_json": ["stock_user", "admin"], "default_workspaces_json": ["Stock"], "required_app": "erpnext", "is_marketed": True},
    {"code": "assets", "name": "Assets", "category": "operations", "description": "Asset registers, maintenance, and lifecycle tracking.", "display_order": 50, "dependency_codes_json": ["accounting"], "default_roles_json": ["asset_manager", "admin"], "default_workspaces_json": ["Assets"], "required_app": "erpnext", "is_marketed": True},
    {"code": "hr", "name": "HR", "category": "people", "description": "People records, attendance, and human resources operations.", "display_order": 60, "dependency_codes_json": [], "default_roles_json": ["hr_user", "admin"], "default_workspaces_json": ["Human Resources"], "required_app": "hrms", "is_marketed": True},
    {"code": "payroll", "name": "Payroll", "category": "people", "description": "Payroll processing and employee compensation workflows.", "display_order": 70, "dependency_codes_json": ["hr", "accounting"], "default_roles_json": ["payroll_user", "admin"], "default_workspaces_json": ["Payroll"], "required_app": "hrms", "is_marketed": True},
    {"code": "manufacturing", "name": "Manufacturing", "category": "operations", "description": "Bills of materials, production plans, work orders, and job cards.", "display_order": 80, "dependency_codes_json": ["stock", "buying"], "default_roles_json": ["manufacturing_user", "admin"], "default_workspaces_json": ["Manufacturing"], "required_app": "erpnext", "is_marketed": True},
    {"code": "crm", "name": "CRM", "category": "commercial", "description": "Leads, opportunities, customer relationships, and sales pipeline.", "display_order": 90, "dependency_codes_json": [], "default_roles_json": ["sales_user", "admin"], "default_workspaces_json": ["CRM"], "required_app": "erpnext", "is_marketed": True},
    {"code": "quality", "name": "Quality", "category": "operations", "description": "Quality goals, inspections, reviews, and non-conformance tracking.", "display_order": 100, "dependency_codes_json": ["stock"], "default_roles_json": ["quality_user", "admin"], "default_workspaces_json": ["Quality"], "required_app": "erpnext", "is_marketed": True},
    {"code": "projects", "name": "Projects", "category": "delivery", "description": "Projects, tasks, timesheets, and delivery cost tracking.", "display_order": 110, "dependency_codes_json": [], "default_roles_json": ["projects_user", "admin"], "default_workspaces_json": ["Projects"], "required_app": "erpnext", "is_marketed": True},
    {"code": "support", "name": "Support", "category": "service", "description": "Support tickets, service levels, and customer helpdesk workflows.", "display_order": 120, "dependency_codes_json": ["crm"], "default_roles_json": ["support_user", "admin"], "default_workspaces_json": ["Support"], "required_app": "erpnext", "is_marketed": True},
    {"code": "well_mapping", "name": "Well Mapping", "category": "drilling", "description": "Well, site, location, and field mapping workflows.", "display_order": 130, "dependency_codes_json": ["field_ops"], "default_roles_json": ["field_supervisor", "admin"], "default_workspaces_json": ["Well Mapping"], "required_app": "lenerp_core", "is_marketed": True, "administrative_visibility": "operator"},
    {"code": "field_ops", "name": "Field Operations", "category": "operations", "description": "Dispatch, crew coordination, and work outside the office.", "display_order": 140, "dependency_codes_json": ["projects"], "default_roles_json": ["dispatcher", "field_supervisor", "admin"], "default_workspaces_json": ["Field Operations"], "is_marketed": True},
    {"code": "drilling", "name": "Drilling", "category": "drilling", "description": "Drilling-specific work coordination and field operations.", "display_order": 150, "dependency_codes_json": ["field_ops", "well_mapping"], "default_roles_json": ["field_supervisor", "admin"], "default_workspaces_json": ["Drilling"], "is_marketed": True},
    {"code": "fleet", "name": "Fleet", "category": "operations", "description": "Vehicles, rigs, equipment assignments, and fleet readiness.", "display_order": 160, "dependency_codes_json": ["assets"], "default_roles_json": ["fleet_manager", "admin"], "default_workspaces_json": ["Fleet"], "is_marketed": True},
    {"code": "reporting", "name": "Reporting", "category": "analytics", "description": "Operational reporting, dashboards, and bounded administrative visibility.", "display_order": 170, "dependency_codes_json": [], "default_roles_json": ["admin", "viewer"], "default_workspaces_json": ["Reports"], "is_marketed": True},
    {"code": "white_label", "name": "White Label", "category": "platform", "description": "Brand and reseller presentation controls.", "display_order": 180, "dependency_codes_json": [], "default_roles_json": ["owner", "admin"], "default_workspaces_json": ["Settings"], "is_marketed": False, "administrative_visibility": "operator"},
    {"code": "custom_domain", "name": "Custom Domain", "category": "platform", "description": "Custom domain mapping and activation controls.", "display_order": 190, "dependency_codes_json": [], "default_roles_json": ["owner", "admin"], "default_workspaces_json": ["Domains"], "is_marketed": False, "administrative_visibility": "operator"},
    {"code": "point_of_sale", "name": "Point of Sale", "category": "commercial", "description": "Point-of-sale profiles, shifts, collections, and retail invoicing.", "display_order": 200, "dependency_codes_json": ["selling", "stock"], "default_roles_json": ["pos_user", "admin"], "default_workspaces_json": ["Point of Sale"], "required_app": "erpnext", "is_marketed": True},
    {"code": "inventory", "name": "Inventory (legacy)", "category": "operations", "description": "Compatibility alias for the canonical Stock module.", "display_order": 40, "dependency_codes_json": [], "default_roles_json": ["stock_user", "admin"], "default_workspaces_json": ["Stock"], "required_app": "erpnext", "is_marketed": False, "alias_of": "stock", "administrative_visibility": "operator"},
]

DEFAULT_BUNDLES = [
    {"bundle_key": "champion-drilling", "version": 1, "name": "Champion Drilling", "description": "Initial synthetic Champion drilling profile; pending Champion role and acceptance decisions.", "modules": ["accounting", "buying", "selling", "stock", "assets", "crm", "projects", "field_ops", "well_mapping", "drilling", "fleet", "reporting"]},
    {"bundle_key": "generic-field-service", "version": 1, "name": "Generic Field Service", "description": "Reusable field service profile for future companies.", "modules": ["crm", "selling", "stock", "assets", "projects", "field_ops", "fleet", "reporting"]},
]

DEFAULT_TEMPLATES = [
    {
        "code": "drilling-mvp",
        "name": "Drilling Company MVP",
        "industry": "drilling",
        "description": "Simple local template for the first drilling client onboarding.",
        "default_modules_json": ["crm", "field_ops", "drilling", "fleet", "reporting"],
        "default_roles_json": ["owner", "admin", "dispatcher", "field_supervisor", "accountant"],
        "default_checklists_json": ["discovery", "logo", "users", "roles", "go_live"],
        "default_settings_json": {"tenant_type": "drilling", "white_label": "basic"},
    },
    {
        "code": "field-service-mvp",
        "name": "Field Service MVP",
        "industry": "field_service",
        "description": "General field service onboarding template.",
        "default_modules_json": ["crm", "field_ops", "fleet", "reporting"],
        "default_roles_json": ["owner", "admin", "dispatcher", "technician"],
        "default_checklists_json": ["discovery", "users", "roles", "training"],
        "default_settings_json": {"tenant_type": "field_service", "white_label": "basic"},
    },
]


def _ensure_plan(session: Session, repository: CatalogRepository, payload: dict[str, object]) -> bool:
    plan = repository.get_by_code(session, Plan, payload["code"])
    if plan is None:
        repository.add_and_refresh(session, Plan(**payload))
        return True
    for key, value in payload.items():
        if key != "code":
            setattr(plan, key, value)
    return False


def _ensure_module(session: Session, repository: CatalogRepository, payload: dict[str, object]) -> bool:
    module = repository.get_by_code(session, Module, payload["code"])
    if module is None:
        repository.add_and_refresh(session, Module(**payload))
        return True
    for key, value in payload.items():
        if key != "code":
            setattr(module, key, value)
    return False


def _ensure_bundle(session: Session, repository: CatalogRepository, payload: dict[str, object]) -> bool:
    bundle = session.query(ModuleBundle).filter_by(bundle_key=payload["bundle_key"], version=payload["version"]).one_or_none()
    if bundle is None:
        bundle = ModuleBundle(bundle_key=payload["bundle_key"], version=payload["version"], name=payload["name"], description=payload["description"], source="platform")
        session.add(bundle)
        session.flush()
        changed = True
    else:
        changed = False
        bundle.name = payload["name"]
        bundle.description = payload["description"]
    module_by_code = {item.code: item for item in session.query(Module).all()}
    desired = list(payload["modules"])
    existing = {item.module_id: item for item in session.query(ModuleBundleItem).filter_by(bundle_id=bundle.id).all()}
    for index, code in enumerate(desired):
        module = module_by_code[code]
        item = existing.pop(module.id, None)
        if item is None:
            session.add(ModuleBundleItem(bundle_id=bundle.id, module_id=module.id, sort_order=index * 10))
            changed = True
        elif item.sort_order != index * 10:
            item.sort_order = index * 10
            changed = True
    for item in existing.values():
        session.delete(item)
        changed = True
    return changed


def _ensure_template(session: Session, repository: CatalogRepository, payload: dict[str, object]) -> bool:
    if repository.get_by_code(session, ImplementationTemplate, payload["code"]) is None:
        repository.add_and_refresh(session, ImplementationTemplate(**payload))
        return True
    return False


def _ensure_task_status(session: Session, repository: CatalogRepository, payload: dict[str, object]) -> bool:
    if repository.get_by_code(session, ImplementationTaskStatus, payload["code"]) is None:
        repository.add_and_refresh(session, ImplementationTaskStatus(**payload))
        return True
    return False


def seed_reference_data(session: Session, repository: Optional[CatalogRepository] = None) -> dict[str, int]:
    repository = repository or CatalogRepository()
    counts = {"plans": 0, "modules": 0, "templates": 0, "task_statuses": 0, "bundles": 0}

    for payload in DEFAULT_PLANS:
        counts["plans"] += int(_ensure_plan(session, repository, payload))

    for payload in DEFAULT_MODULES:
        counts["modules"] += int(_ensure_module(session, repository, payload))

    for payload in DEFAULT_TEMPLATES:
        counts["templates"] += int(_ensure_template(session, repository, payload))

    for payload in DEFAULT_BUNDLES:
        counts["bundles"] += int(_ensure_bundle(session, repository, payload))

    for payload in DEFAULT_TASK_STATUSES:
        counts["task_statuses"] += int(_ensure_task_status(session, repository, payload))

    session.commit()
    return counts


def main() -> None:
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        counts = seed_reference_data(session)
        print(
            "Seed complete: "
            f"{counts['plans']} plan(s), {counts['modules']} module(s), {counts['templates']} template(s), "
            f"{counts['task_statuses']} task status(es), {counts['bundles']} bundle(s) changed."
        )


if __name__ == "__main__":
    main()
