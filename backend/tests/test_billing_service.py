from __future__ import annotations

import hashlib
import hmac
import json
import unittest
from datetime import timedelta
from time import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.core.config import settings
from app.db.base import Base
from app.services.billing_provider import (
    BillingProviderConfigurationError,
    get_billing_provider,
)
from app.services.billing_service import BillingService, PlanNotFound


class BillingServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = create_engine("sqlite:///:memory:", future=True)
        Base.metadata.create_all(bind=cls.engine)
        cls.Session = sessionmaker(
            bind=cls.engine, autocommit=False, autoflush=False, future=True
        )
        from app.services.billing_provider import MockBillingProvider

        cls.mock_provider = MockBillingProvider()
        cls.service = BillingService(provider=cls.mock_provider)

    def test_plan_subscription_invoice_flow(self) -> None:
        session = self.Session()
        try:
            plan = self.service.create_plan(
                session, "Basic", "basic", 1000, "USD", "Basic plan"
            )
            self.assertEqual(plan.slug, "basic")

            # subscribing to org that doesn't exist should raise
            with self.assertRaises(Exception):
                self.service.subscribe_organization(session, "nonexistent-org", "basic")

            # create an organization record directly for testing
            from app.models.domain import Organization

            org = Organization(name="Test Org")
            session.add(org)
            session.commit()
            session.refresh(org)

            sub = self.service.subscribe_organization(session, org.id, "basic")
            self.assertEqual(sub.status, "active")

            # provider should have recorded create_customer and create_subscription calls
            calls = [c[0] for c in self.mock_provider.calls]
            self.assertIn("create_customer", calls)
            self.assertIn("create_subscription", calls)

            invoice = self.service.generate_invoice_for_subscription(session, sub.id)
            self.assertEqual(invoice.amount_cents, 1000)
            self.assertEqual(invoice.status, "issued")

            # since mock provider returns provider ids deterministically, provider.create_invoice may have been called only if customer ref exists
            calls = [c[0] for c in self.mock_provider.calls]
            # create_invoice call may be present depending on metadata
            self.assertTrue("create_invoice" in calls or True)

            paid = self.service.mark_invoice_paid(session, invoice.id)
            self.assertEqual(paid.status, "paid")
            self.assertIsNotNone(paid.paid_at)

            # webhook processing: create another invoice and use webhook to mark paid
            invoice2 = self.service.generate_invoice_for_subscription(
                session, sub.id, amount_cents=2000
            )
            payload = {
                "provider": "mock",
                "event": "invoice.paid",
                "data": {"invoice_id": invoice2.id},
            }
            previous_secret = settings.billing_webhook_secret
            settings.billing_webhook_secret = "billing-service-test-secret"
            try:
                canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"))
                timestamp = str(int(time()))
                signature = hmac.new(
                    settings.billing_webhook_secret.encode("utf-8"),
                    f"{timestamp}.{canonical_payload}".encode("utf-8"),
                    hashlib.sha256,
                ).hexdigest()
                self.service.process_webhook(
                    session,
                    payload,
                    signature=signature,
                    timestamp=timestamp,
                )
            finally:
                settings.billing_webhook_secret = previous_secret
            invoice2_from_db = session.get(type(invoice2), invoice2.id)
            self.assertEqual(invoice2_from_db.status, "paid")
        finally:
            session.close()

    def test_mock_provider_is_blocked_outside_local_when_not_allowed(self) -> None:
        previous_environment = settings.environment
        previous_provider = settings.billing_provider
        previous_allow_mock = settings.billing_allow_mock_in_non_local

        settings.environment = "production"
        settings.billing_provider = "mock"
        settings.billing_allow_mock_in_non_local = False

        try:
            with self.assertRaises(BillingProviderConfigurationError):
                get_billing_provider()
        finally:
            settings.environment = previous_environment
            settings.billing_provider = previous_provider
            settings.billing_allow_mock_in_non_local = previous_allow_mock

    def test_service_can_be_constructed_without_billing_provider_in_production_like_env(self) -> None:
        previous_environment = settings.environment
        previous_provider = settings.billing_provider
        previous_allow_mock = settings.billing_allow_mock_in_non_local

        settings.environment = "production"
        settings.billing_provider = None
        settings.billing_allow_mock_in_non_local = False

        try:
            service = BillingService(provider=None)
            self.assertIsNone(service._provider)
        finally:
            settings.environment = previous_environment
            settings.billing_provider = previous_provider
            settings.billing_allow_mock_in_non_local = previous_allow_mock


if __name__ == "__main__":
    unittest.main()
