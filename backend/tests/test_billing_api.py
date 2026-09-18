from __future__ import annotations

import hashlib
import hmac
import json
import unittest
from time import time

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models as _models  # noqa: F401
from app.api.dependencies import get_current_user, get_db_session
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.schemas.auth import AuthRegisterRequest
from app.services.auth_service import AuthService
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
        cls.auth_service = AuthService()

    @classmethod
    def tearDownClass(cls) -> None:
        app.dependency_overrides.pop(get_db_session, None)
        app.dependency_overrides.pop(get_current_user, None)

    def setUp(self) -> None:
        self.session = self.Session()
        self._previous_feature_flags = settings.feature_flags
        settings.feature_flags = f"{settings.feature_flags},legacy_billing_mutations=true"
        register_response = self.auth_service.register(
            self.session,
            AuthRegisterRequest(
                email=f"billing-admin+{self._testMethodName}@example.test",
                full_name="Billing Admin",
                password="local-password-123",
                organization_name="Billing Workspace",
                membership_role="owner",
                is_platform_admin=True,
            ),
        )
        context = self.auth_service.get_context(self.session, register_response.access_token)
        self.user = context.user

        def override_get_current_user():
            return self.user

        app.dependency_overrides[get_current_user] = override_get_current_user

    def tearDown(self) -> None:
        app.dependency_overrides.pop(get_current_user, None)
        settings.feature_flags = self._previous_feature_flags
        self.session.close()

    def test_endpoints_subscribe_and_invoice(self) -> None:
        # create plan via service (bypass auth)
        self.service.create_plan(self.session, "Pro", "pro", 5000, "USD", "Pro plan")
        from app.models.domain import Organization

        org = Organization(name="API Org")
        self.session.add(org)
        self.session.commit()
        self.session.refresh(org)

        # subscribe via API
        resp = self.client.post(
            f"/billing/organizations/{org.id}/subscribe", json={"plan_slug": "pro"}
        )
        self.assertEqual(resp.status_code, 201)
        body = resp.json()
        self.assertEqual(body["organization_id"], org.id)

        # create invoice via API
        resp2 = self.client.post(f"/billing/organizations/{org.id}/invoices", json={})
        self.assertEqual(resp2.status_code, 201)
        inv = resp2.json()
        self.assertEqual(inv["amount_cents"], 5000)

        # get invoice
        inv_id = inv["id"]
        resp3 = self.client.get(f"/billing/organizations/{org.id}/invoices/{inv_id}")
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp3.json()["id"], inv_id)

    def test_webhook_requires_signature_when_secret_is_configured(self) -> None:
        plan = self.service.create_plan(
            self.session, "Webhook", "webhook", 2500, "USD", "Webhook plan"
        )
        from app.models.domain import Organization

        org = Organization(name="Webhook Org")
        self.session.add(org)
        self.session.commit()
        self.session.refresh(org)

        self.client.post(f"/billing/organizations/{org.id}/subscribe", json={"plan_slug": "webhook"})
        invoice = self.client.post(f"/billing/organizations/{org.id}/invoices", json={}).json()

        payload = {"provider": "mock", "event": "invoice.paid", "data": {"invoice_id": invoice["id"]}}
        previous_secret = settings.billing_webhook_secret
        settings.billing_webhook_secret = "billing-api-test-secret"
        try:
            unsigned_response = self.client.post("/billing/webhook", json=payload)
            self.assertEqual(unsigned_response.status_code, 401)

            canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"))
            timestamp = str(int(time()))
            signature = hmac.new(
                settings.billing_webhook_secret.encode("utf-8"),
                f"{timestamp}.{canonical_payload}".encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            signed_response = self.client.post(
                "/billing/webhook",
                json=payload,
                headers={
                    "X-Billing-Signature": signature,
                    "X-Billing-Timestamp": timestamp,
                },
            )
            self.assertEqual(signed_response.status_code, 200)
            self.assertTrue(signed_response.json()["handled"])
        finally:
            settings.billing_webhook_secret = previous_secret


if __name__ == "__main__":
    unittest.main()
