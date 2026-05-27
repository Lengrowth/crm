from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.domain import ImplementationTemplate, Module, Organization, Plan, Tenant


class CatalogRepository:
    def list_organizations(self, session: Session) -> Sequence[Organization]:
        return self._list(session, select(Organization).order_by(Organization.created_at.desc()))

    def list_tenants(self, session: Session) -> Sequence[Tenant]:
        return self._list(session, select(Tenant).order_by(Tenant.created_at.desc()))

    def list_modules(self, session: Session) -> Sequence[Module]:
        return self._list(session, select(Module).order_by(Module.category.asc().nullslast(), Module.name.asc()))

    def list_plans(self, session: Session) -> Sequence[Plan]:
        return self._list(session, select(Plan).order_by(Plan.monthly_price_cents.asc(), Plan.name.asc()))

    def list_templates(self, session: Session) -> Sequence[ImplementationTemplate]:
        return self._list(session, select(ImplementationTemplate).order_by(ImplementationTemplate.name.asc()))

    def get_by_code(self, session: Session, model: type, code: str):
        statement = select(model).where(model.code == code)  # type: ignore[attr-defined]
        return session.execute(statement).scalar_one_or_none()

    def add_and_refresh(self, session: Session, entity):
        session.add(entity)
        session.flush()
        session.refresh(entity)
        return entity

    def _list(self, session: Session, statement):
        return session.execute(statement).scalars().all()
