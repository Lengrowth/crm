from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.domain import ImplementationTemplate, Module, ModuleBundle, ModuleBundleItem, Organization, Plan, Tenant


class CatalogRepository:
    def list_organizations(self, session: Session) -> Sequence[Organization]:
        return self._list(session, select(Organization).order_by(Organization.created_at.desc()))

    def list_tenants(self, session: Session) -> Sequence[Tenant]:
        return self._list(session, select(Tenant).order_by(Tenant.created_at.desc()))

    def list_modules(self, session: Session) -> Sequence[Module]:
        return self._list(session, select(Module).order_by(Module.display_order.asc(), Module.code.asc()))

    def list_bundles(self, session: Session) -> Sequence[ModuleBundle]:
        return self._list(session, select(ModuleBundle).where(ModuleBundle.is_active.is_(True)).order_by(ModuleBundle.bundle_key.asc(), ModuleBundle.version.desc()))

    def list_bundle_items(self, session: Session, bundle_id: str) -> Sequence[ModuleBundleItem]:
        return self._list(session, select(ModuleBundleItem).where(ModuleBundleItem.bundle_id == bundle_id).order_by(ModuleBundleItem.sort_order.asc(), ModuleBundleItem.module_id.asc()))

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
