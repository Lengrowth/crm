from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from app.db.seed import seed_reference_data
from app.repositories.catalog_repository import CatalogRepository


class CatalogService:
    def __init__(self, repository: Optional[CatalogRepository] = None) -> None:
        self.repository = repository or CatalogRepository()

    def list_organizations(self, session: Session):
        return self.repository.list_organizations(session)

    def list_tenants(self, session: Session):
        return self.repository.list_tenants(session)

    def list_modules(self, session: Session):
        return self.repository.list_modules(session)

    def list_plans(self, session: Session):
        return self.repository.list_plans(session)

    def list_templates(self, session: Session):
        return self.repository.list_templates(session)

    def seed_reference_data(self, session: Session) -> dict[str, int]:
        return seed_reference_data(session, self.repository)
