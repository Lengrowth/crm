Phase 09 - Plans, Subscriptions, Invoices and Billing

This phase introduces lightweight billing models, a deterministic BillingService, API endpoints for plans/subscriptions/invoices, and webhook handling.

Models
- BillingPlan (table: billing_plans): id, name, slug, price_cents, currency, description, timestamps
- BillingSubscription (table: billing_subscriptions): id, organization_id, tenant_id (nullable), plan_id, status, started_at, current_period_end, ended_at, metadata, timestamps
- BillingInvoice (table: billing_invoices): id, organization_id, tenant_id (nullable), amount_cents, currency, status, due_date, issued_at, paid_at, lines (JSON array of items), metadata, timestamps

Service
- app.services.billing_service.BillingService
  - list_plans(session)
  - create_plan(session, name, slug, price_cents, currency, description)
  - get_plan_by_slug(session, slug)
  - subscribe_organization(session, organization_id, plan_slug, tenant_id=None)
  - get_subscription_for_organization(session, organization_id)
  - generate_invoice_for_subscription(session, subscription_id, amount_cents=None, lines=None)
  - mark_invoice_paid(session, invoice_id)
  - process_webhook(session, payload)  # handles invoice.paid and subscription.canceled

API
- GET  /billing/plans
- POST /billing/plans  (requires platform admin)
- POST /billing/organizations/{organization_id}/subscribe
- GET  /billing/organizations/{organization_id}/subscription
- POST /billing/organizations/{organization_id}/invoices
- GET  /billing/organizations/{organization_id}/invoices/{invoice_id}
- POST /billing/webhook

Notes & testing
- No external provider integration is included. Stripe is referenced as a placeholder only.
- Tests use in-memory SQLite and create tables at runtime.
- To run migrations:
  cd backend
  alembic upgrade head

- To run tests:
  python -m venv .venv
  source .venv/bin/activate   # or .venv\Scripts\activate on Windows
  pip install -e backend[dev]
  pytest backend/tests -q

Design choices
- Billing models use separate table names with Billing* class names to avoid colliding with existing domain.Plan/Subscription models.
- Invoice line items are stored as JSON in `billing_invoices.lines` as a list of {description, amount_cents, quantity}.
- Subscriptions default to a 30-day period for current_period_end from started_at.

Follow-ups
- Add billing reconciliation, scheduled invoice issuance, and provider integrations (Stripe) in later phases.
- Add authorization checks on subscription and invoice endpoints (currently minimal for testing).