# Phase 13 — Billing Provider Integration

Summary

This phase adds a pluggable billing provider abstraction and a Stripe adapter using the official Stripe SDK. The goal is to allow the BillingService to map SaaS billing actions to external providers while keeping the integration optional and test-friendly.

Files added/changed

- `backend/app/services/billing_provider.py` — New provider interface and two implementations:
  - `BillingProvider` (interface)
  - `MockBillingProvider` (in-memory test provider that records calls)
  - `StripeBillingProvider` (SDK-backed implementation that uses the official `stripe` package; best-effort calls — disabled when `STRIPE_API_KEY` is not set)

- `backend/app/services/billing_service.py` — Updated to accept an optional `BillingProvider` via dependency injection. Provider interactions (customer creation, subscription creation, invoice creation) are best-effort and will not break local database flows if they fail.

- `backend/tests/test_billing_service.py` — Updated to inject `MockBillingProvider` and assert provider calls are recorded during subscription and invoice flows.

Configuration

- Provider selection: pass a `BillingProvider` implementation to `BillingService` when constructing it. If no provider is supplied, `MockBillingProvider` is used by default (convenient for tests and local development).

- Stripe SDK-backed provider: `StripeBillingProvider` reads `STRIPE_API_KEY` from the environment. If the API key is present and the `stripe` package is installed (added to `backend/pyproject.toml`), the provider will call Stripe APIs for customer, subscription, invoice, and payment-intent operations. If the SDK or key is missing, the provider logs and behaves as disabled (best-effort).

  Do not place real secrets in repo files. Add `STRIPE_API_KEY` to your environment or local `.env` when ready.

  Example in `.env.example` (update as needed):

  STRIPE_API_KEY=

Migration notes

- Subscription and Invoice models include a `metadata` JSON field. The billing provider integration stores provider references under well-known keys in this metadata:
  - `provider_customer_id` — provider customer identifier
  - `provider_subscription_id` — provider subscription identifier
  - `provider_invoice_id` — provider invoice identifier

- These metadata fields are optional and are populated only when the provider returns identifiers. Because provider calls are best-effort, existing records without provider refs continue to work.

Testing notes

- Use `MockBillingProvider` in unit tests to assert provider interactions without needing network access or secrets.

Future work (Phase 14+)

- `StripeBillingProvider` has been replaced with an SDK-backed implementation in this phase.
- Next steps: Add secure configuration/secret storage (vault/secret manager) for provider API keys.
- Expand provider interface to support webhooks validation, refunds, and more advanced billing operations.

Design rationale

- Provider calls are isolated behind a small interface to minimize coupling and make them easy to mock in tests.
- Best-effort semantics prevent external provider outages from blocking local SaaS administration flows during early phases.
- No vendor SDKs or networked secrets are added in this phase to keep the repo safe and approvals simple.
