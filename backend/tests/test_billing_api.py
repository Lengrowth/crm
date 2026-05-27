from __future__ import annotations

import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models as _models  # noqa: F401
from app.api.dependencies import get_db_session
from app.db.base import Base
from app.main import app
from app.services.billing_service import BillingService


class BillingAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine(
            "sqlite://",
            future=True,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=cls.engine)
        cls.Session = sessionmaker(
            bind=cls.engine, autocommit=False, autoflush=False, future=True
        )

        def override_get_db_session():
            session = cls.Session()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_db_session] = override_get_db_session
        cls.client = TestClient(app)
        cls.service = BillingService()

    @classmethod
    def tearDownClass(cls) -> None:
        app.dependency_overrides.pop(get_db_session, None)

    def test_endpoints_subscribe_and_invoice(self) -> None:
        # create plan via service (bypass auth)
        session = self.Session()
        try:
            plan = self.service.create_plan(
                session, "Pro", "pro", 5000, "USD", "Pro plan"
            )
            from app.models.domain import Organization

            org = Organization(name="API Org")
            session.add(org)
            session.commit()
            session.refresh(org)

            # subscribe via API
            resp = self.client.post(
                f"/billing/organizations/{org.id}/subscribe", json={"plan_slug": "pro"}
            )
            self.assertEqual(resp.status_code, 201)
            body = resp.json()
            self.assertEqual(body["organization_id"], org.id)

            # create invoice via API
            resp2 = self.client.post(
                f"/billing/organizations/{org.id}/invoices", json={}
            )
            self.assertEqual(resp2.status_code, 201)
            inv = resp2.json()
            self.assertEqual(inv["amount_cents"], 5000)

            # get invoice
            inv_id = inv["id"]
            resp3 = self.client.get(
                f"/billing/organizations/{org.id}/invoices/{inv_id}"
            )
            self.assertEqual(resp3.status_code, 200)
            self.assertEqual(resp3.json()["id"], inv_id)
        finally:
            session.close()


if __name__ == "__main__":
    unittest.main()
