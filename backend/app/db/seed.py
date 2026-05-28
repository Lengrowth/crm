from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.models.domain import ImplementationTaskStatus, ImplementationTemplate, Module, Plan
from app.repositories.catalog_repository import CatalogRepository


DEFAULT_PLANS = [
    {
        "code": "starter",
        "name": "Starter",
        "description": "Local MVP plan with the smallest SaaS footprint.",
        "monthly_price_cents": 9900,
        "annual_price_cents": 99000,
    },
    {
        "code": "growth",
        "name": "Growth",
        "description": "For teams that need more modules and tenant capacity.",
        "monthly_price_cents": 24900,
        "annual_price_cents": 249000,
    },
    {
        "code": "enterprise",
        "name": "Enterprise",
        "description": "Reserved for future manual-contract billing flows.",
        "monthly_price_cents": 0,
        "annual_price_cents": 0,
        "is_active": False,
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
    {"code": "crm", "name": "CRM", "category": "core"},
    {"code": "field_ops", "name": "Field Operations", "category": "operations"},
    {"code": "drilling", "name": "Drilling", "category": "operations"},
    {"code": "fleet", "name": "Fleet", "category": "operations"},
    {"code": "inventory", "name": "Inventory", "category": "core"},
    {"code": "reporting", "name": "Reporting", "category": "analytics"},
    {"code": "white_label", "name": "White Label", "category": "platform"},
    {"code": "custom_domain", "name": "Custom Domain", "category": "platform"},
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
    if repository.get_by_code(session, Plan, payload["code"]) is None:
        repository.add_and_refresh(session, Plan(**payload))
        return True
    return False


def _ensure_module(session: Session, repository: CatalogRepository, payload: dict[str, object]) -> bool:
    if repository.get_by_code(session, Module, payload["code"]) is None:
        repository.add_and_refresh(session, Module(**payload))
        return True
    return False


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
    counts = {"plans": 0, "modules": 0, "templates": 0, "task_statuses": 0}

    for payload in DEFAULT_PLANS:
        counts["plans"] += int(_ensure_plan(session, repository, payload))

    for payload in DEFAULT_MODULES:
        counts["modules"] += int(_ensure_module(session, repository, payload))

    for payload in DEFAULT_TEMPLATES:
        counts["templates"] += int(_ensure_template(session, repository, payload))

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
            f"{counts['task_statuses']} task status(es) added."
        )


if __name__ == "__main__":
    main()
