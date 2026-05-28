from __future__ import annotations

import hashlib
import hmac
import json
from datetime import timedelta
from typing import List, Optional
from time import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.billing import BillingInvoice, BillingPlan, BillingSubscription
from app.models.domain import Organization
from app.core.config import settings
from app.models.erpnext import utcnow


class BillingError(Exception):
    pass


class BillingWebhookVerificationError(BillingError):
    pass


class PlanNotFound(BillingError):
    pass


class SubscriptionNotFound(BillingError):
    pass


class InvoiceNotFound(BillingError):
    pass


from app.services.billing_provider import BillingProvider, get_billing_provider


class BillingService:
    """Simple deterministic billing service with optional billing provider integration.

    Provider interactions are best-effort and will not fail local flows.
    """

    def __init__(self, provider: Optional[BillingProvider] = None) -> None:
        self._provider = provider

    @property
    def provider(self) -> BillingProvider:
        if self._provider is None:
            self._provider = get_billing_provider()
        return self._provider

    def list_plans(self, session: Session) -> List[BillingPlan]:
        statement = select(BillingPlan).order_by(BillingPlan.created_at)
        return session.execute(statement).scalars().all()

    def create_plan(
        self,
        session: Session,
        name: str,
        slug: str,
        price_cents: int,
        currency: str = "USD",
        description: Optional[str] = None,
    ) -> BillingPlan:
        plan = BillingPlan(
            name=name.strip(),
            slug=slug.strip(),
            price_cents=price_cents,
            currency=currency,
            description=description,
        )
        session.add(plan)
        session.commit()
        session.refresh(plan)
        return plan

    def get_plan_by_slug(self, session: Session, slug: str) -> Optional[BillingPlan]:
        statement = select(BillingPlan).where(BillingPlan.slug == slug)
        return session.execute(statement).scalar_one_or_none()

    def subscribe_organization(
        self,
        session: Session,
        organization_id: str,
        plan_slug: str,
        tenant_id: Optional[str] = None,
    ) -> BillingSubscription:
        plan = self.get_plan_by_slug(session, plan_slug)
        if plan is None:
            raise PlanNotFound("Plan not found")
        # ensure organization exists
        org = session.get(Organization, organization_id)
        if org is None:
            raise BillingError("Organization not found")

        now = utcnow()
        subscription = BillingSubscription(
            organization_id=organization_id,
            tenant_id=tenant_id,
            plan_id=plan.id,
            status="active",
            started_at=now,
            current_period_end=now + timedelta(days=30),
        )
        session.add(subscription)
        session.commit()
        session.refresh(subscription)

        # Best-effort provider integration: create provider customer and subscription
        try:
            org_payload = {
                "id": org.id,
                "name": org.name,
                "billing_email": org.billing_email,
            }
            provider_customer_id = None
            try:
                provider_customer_id = self.provider.create_customer(org_payload)
            except Exception as e:  # provider errors should not break local flow
                # log and continue
                import logging

                logging.getLogger(__name__).exception(
                    "billing provider create_customer failed: %s", e
                )

            provider_subscription_id = None
            try:
                # pass a minimal plan payload
                plan_payload = {
                    "id": plan.id,
                    "slug": plan.slug,
                    "price_cents": plan.price_cents,
                }
                provider_subscription_id = self.provider.create_subscription(
                    provider_customer_id or org.id,
                    plan_payload,
                    metadata={"local_subscription_id": subscription.id},
                )
            except Exception as e:
                import logging

                logging.getLogger(__name__).exception(
                    "billing provider create_subscription failed: %s", e
                )

            # persist provider refs into subscription metadata if available
            metadata = subscription.metadata_json or {}
            if provider_customer_id:
                metadata["provider_customer_id"] = provider_customer_id
            if provider_subscription_id:
                metadata["provider_subscription_id"] = provider_subscription_id
            if metadata:
                subscription.metadata_json = metadata
                session.add(subscription)
                session.commit()
                session.refresh(subscription)
        except Exception:
            # any unexpected error here should not break the main flow
            pass

        return subscription

    def get_subscription_for_organization(
        self, session: Session, organization_id: str
    ) -> Optional[BillingSubscription]:
        statement = select(BillingSubscription).where(
            BillingSubscription.organization_id == organization_id
        )
        return session.execute(statement).scalar_one_or_none()

    def generate_invoice_for_subscription(
        self,
        session: Session,
        subscription_id: str,
        amount_cents: Optional[int] = None,
        lines: Optional[List[dict]] = None,
    ) -> BillingInvoice:
        subscription = session.get(BillingSubscription, subscription_id)
        if subscription is None:
            raise SubscriptionNotFound("Subscription not found")

        plan = session.get(BillingPlan, subscription.plan_id)
        if plan is None:
            raise PlanNotFound("Plan not found for subscription")

        if lines is None:
            # default single-line for plan price
            lines = [
                {
                    "description": f"{plan.name} subscription",
                    "amount_cents": amount_cents or plan.price_cents,
                    "quantity": 1,
                }
            ]

        total = (
            amount_cents
            if amount_cents is not None
            else sum(
                int(l.get("amount_cents", 0)) * int(l.get("quantity", 1)) for l in lines
            )
        )

        invoice = BillingInvoice(
            organization_id=subscription.organization_id,
            tenant_id=subscription.tenant_id,
            amount_cents=total,
            currency=plan.currency,
            status="issued",
            issued_at=utcnow(),
            due_date=None,
            lines=lines,
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)

        # Best-effort: create invoice in provider if subscription has provider customer ref
        try:
            provider_customer_id = None
            try:
                provider_customer_id = (
                    subscription.metadata_json.get("provider_customer_id")
                    if subscription.metadata_json
                    else None
                )
            except Exception:
                provider_customer_id = None

            if provider_customer_id:
                try:
                    invoice_payload = {
                        "amount_cents": invoice.amount_cents,
                        "currency": invoice.currency,
                        "lines": invoice.lines,
                        "local_invoice_id": invoice.id,
                    }
                    provider_invoice_id = self.provider.create_invoice(
                        provider_customer_id, invoice_payload
                    )
                    if provider_invoice_id:
                        inv_meta = invoice.metadata_json or {}
                        inv_meta["provider_invoice_id"] = provider_invoice_id
                        invoice.metadata_json = inv_meta
                        session.add(invoice)
                        session.commit()
                        session.refresh(invoice)
                except Exception as e:
                    import logging

                    logging.getLogger(__name__).exception(
                        "billing provider create_invoice failed: %s", e
                    )
        except Exception:
            pass

        return invoice

    def mark_invoice_paid(self, session: Session, invoice_id: str) -> BillingInvoice:
        invoice = session.get(BillingInvoice, invoice_id)
        if invoice is None:
            raise InvoiceNotFound("Invoice not found")
        invoice.status = "paid"
        invoice.paid_at = utcnow()
        session.commit()
        session.refresh(invoice)
        return invoice

    def process_webhook(
        self,
        session: Session,
        payload: dict,
        *,
        signature: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> dict:
        self._verify_webhook_signature(payload, signature=signature, timestamp=timestamp)

        # Minimal provider-agnostic processing for two events: invoice.paid and subscription.canceled
        event = payload.get("event")
        data = payload.get("data") or {}
        if event == "invoice.paid":
            invoice_id = data.get("invoice_id")
            if not invoice_id:
                raise BillingError("invoice_id is required for invoice.paid")
            self.mark_invoice_paid(session, invoice_id)
            return {"handled": True}
        if event == "subscription.canceled":
            subscription_id = data.get("subscription_id")
            if not subscription_id:
                raise BillingError(
                    "subscription_id is required for subscription.canceled"
                )
            subscription = session.get(BillingSubscription, subscription_id)
            if subscription is None:
                raise SubscriptionNotFound("Subscription not found")
            subscription.status = "canceled"
            subscription.ended_at = utcnow()
            session.commit()
            return {"handled": True}

        return {"handled": False}

    def _verify_webhook_signature(
        self,
        payload: dict,
        *,
        signature: Optional[str],
        timestamp: Optional[str],
    ) -> None:
        secret = settings.billing_webhook_secret
        if not secret:
            if settings.is_local_environment:
                return
            raise BillingWebhookVerificationError(
                "Billing webhook secret is not configured for this environment."
            )

        if not signature or not timestamp:
            raise BillingWebhookVerificationError(
                "Billing webhook signature and timestamp headers are required."
            )

        try:
            timestamp_int = int(timestamp)
        except ValueError as exc:
            raise BillingWebhookVerificationError("Billing webhook timestamp is invalid.") from exc

        current_time = int(time())
        if abs(current_time - timestamp_int) > 300:
            raise BillingWebhookVerificationError("Billing webhook timestamp is outside the allowed window.")

        canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signed_message = f"{timestamp}.{canonical_payload}".encode("utf-8")
        expected_signature = hmac.new(
            secret.encode("utf-8"), signed_message, hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature.strip(), expected_signature):
            raise BillingWebhookVerificationError("Billing webhook signature is invalid.")
