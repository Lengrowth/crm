from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class BillingProviderError(Exception):
    pass


class BillingProvider:
    """Interface for billing providers.

    Implementations should provide best-effort network calls and return
    provider-specific identifiers where applicable.
    """

    def create_customer(self, organization: Dict[str, Any]) -> Optional[str]:
        """Create a customer record in the provider and return provider customer id."""
        raise NotImplementedError

    def create_subscription(
        self,
        customer_id: str,
        plan: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create a subscription for a customer and return provider subscription id."""
        raise NotImplementedError

    def create_invoice(
        self, customer_id: str, invoice_payload: Dict[str, Any]
    ) -> Optional[str]:
        """Create an invoice in the provider and return provider invoice id."""
        raise NotImplementedError

    def charge(
        self, customer_id: str, amount_cents: int, currency: str = "USD"
    ) -> Dict[str, Any]:
        """Attempt an on-demand charge. Returns a dict with status and provider ids as available."""
        raise NotImplementedError


class MockBillingProvider(BillingProvider):
    """Simple in-memory mock provider used for tests.

    Records calls and returns deterministic fake ids.
    """

    def __init__(self) -> None:
        self.calls = []
        self._next_id = 1

    def _fake_id(self, prefix: str) -> str:
        id_ = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return id_

    def create_customer(self, organization: Dict[str, Any]) -> Optional[str]:
        cid = self._fake_id("cust")
        self.calls.append(("create_customer", organization, cid))
        return cid

    def create_subscription(
        self,
        customer_id: str,
        plan: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        sid = self._fake_id("sub")
        self.calls.append(("create_subscription", customer_id, plan, metadata, sid))
        return sid

    def create_invoice(
        self, customer_id: str, invoice_payload: Dict[str, Any]
    ) -> Optional[str]:
        iid = self._fake_id("inv")
        self.calls.append(("create_invoice", customer_id, invoice_payload, iid))
        return iid

    def charge(
        self, customer_id: str, amount_cents: int, currency: str = "USD"
    ) -> Dict[str, Any]:
        charge_id = self._fake_id("charge")
        self.calls.append(("charge", customer_id, amount_cents, currency, charge_id))
        return {"status": "succeeded", "charge_id": charge_id}


class StripeBillingProvider(BillingProvider):
    """Stripe adapter using the official stripe SDK.

    This implementation uses the `stripe` package and reads `STRIPE_API_KEY` from
    the environment. All calls are best-effort: SDK errors are caught and
    logged, and methods return None or error information instead of raising.
    """

    def __init__(self) -> None:
        self.api_key = os.environ.get("STRIPE_API_KEY")
        self._stripe = None
        if not self.api_key:
            logger.warning(
                "StripeBillingProvider initialized without STRIPE_API_KEY; provider will be disabled"
            )
            return
        try:
            import stripe

            stripe.api_key = self.api_key
            self._stripe = stripe
            logger.info("StripeBillingProvider initialized with STRIPE_API_KEY")
        except Exception as e:  # ImportError or other
            logger.exception("Failed to initialize stripe SDK: %s", e)
            self._stripe = None

    def _is_enabled(self) -> bool:
        return bool(self._stripe)

    def create_customer(self, organization: Dict[str, Any]) -> Optional[str]:
        if not self._is_enabled():
            logger.info("Stripe provider not enabled; skipping create_customer")
            return None
        try:
            customer = self._stripe.Customer.create(
                name=organization.get("name"),
                email=organization.get("billing_email"),
                metadata={"organization_id": organization.get("id")},
            )
            return getattr(customer, "id", None) or customer.get("id")
        except Exception as e:
            logger.exception("Stripe create_customer failed: %s", e)
            return None

    def create_subscription(
        self,
        customer_id: str,
        plan: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        if not self._is_enabled():
            logger.info("Stripe provider not enabled; skipping create_subscription")
            return None
        try:
            # Use price_data to create an on-the-fly price for the subscription
            price_item = {
                "price_data": {
                    "currency": plan.get("currency", "USD"),
                    "unit_amount": int(plan.get("price_cents", 0)),
                    "product_data": {"name": plan.get("slug") or plan.get("id")},
                },
                "quantity": 1,
            }
            sub = self._stripe.Subscription.create(
                customer=customer_id,
                items=[price_item],
                metadata=metadata or {},
            )
            return getattr(sub, "id", None) or sub.get("id")
        except Exception as e:
            logger.exception("Stripe create_subscription failed: %s", e)
            return None

    def create_invoice(
        self, customer_id: str, invoice_payload: Dict[str, Any]
    ) -> Optional[str]:
        if not self._is_enabled():
            logger.info("Stripe provider not enabled; skipping create_invoice")
            return None
        try:
            # Add an invoice item and then create/finalize an invoice
            amount = int(invoice_payload.get("amount_cents", 0))
            currency = invoice_payload.get("currency", "USD")
            description = invoice_payload.get("description") or invoice_payload.get(
                "lines"
            )
            self._stripe.InvoiceItem.create(
                customer=customer_id,
                amount=amount,
                currency=currency,
                description=str(description),
            )
            invoice = self._stripe.Invoice.create(
                customer=customer_id,
                metadata={"local_invoice_id": invoice_payload.get("local_invoice_id")},
            )
            # Optionally finalize — best-effort
            try:
                finalized = (
                    self._stripe.Invoice.finalize_invoice(invoice["id"])
                    if isinstance(invoice, dict)
                    else self._stripe.Invoice.finalize_invoice(
                        getattr(invoice, "id", None)
                    )
                )
                inv_id = (
                    finalized.get("id")
                    if isinstance(finalized, dict)
                    else getattr(finalized, "id", None)
                )
                return inv_id
            except Exception:
                # If finalize fails, return the created invoice id
                return getattr(invoice, "id", None) or invoice.get("id")
        except Exception as e:
            logger.exception("Stripe create_invoice failed: %s", e)
            return None

    def charge(
        self, customer_id: str, amount_cents: int, currency: str = "USD"
    ) -> Dict[str, Any]:
        if not self._is_enabled():
            logger.info("Stripe provider not enabled; skipping charge")
            return {"status": "skipped"}
        try:
            # Create a PaymentIntent. Without a payment method this will typically require further action.
            intent = self._stripe.PaymentIntent.create(
                amount=int(amount_cents), currency=currency, customer=customer_id
            )
            intent_id = getattr(intent, "id", None) or intent.get("id")
            status = getattr(intent, "status", None) or intent.get("status")
            return {"status": status, "payment_intent_id": intent_id}
        except Exception as e:
            logger.exception("Stripe charge failed: %s", e)
            return {"status": "error", "error": str(e)}


def get_billing_provider(provider_name: Optional[str] = None) -> BillingProvider:
    """Factory helper to instantiate a provider by name.

    - If provider_name is provided it is used. Otherwise the environment variable
      `BILLING_PROVIDER` is read (default: "mock").
    - Supported names: "mock", "stripe".
    """
    name = provider_name or os.environ.get("BILLING_PROVIDER", "mock")
    name = name.strip().lower()
    if name == "mock":
        return MockBillingProvider()
    if name == "stripe":
        return StripeBillingProvider()
    raise ValueError(f"unknown billing provider: {name}")
