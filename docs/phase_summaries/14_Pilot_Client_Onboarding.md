# Phase 14 — Pilot Client Onboarding (Summary)

This phase adds an in-repo orchestration for a deterministic pilot onboarding flow, an integration test that runs the full flow in-memory without external services, and a short runbook for running the end-to-end test locally.

What changed

- `backend/app/services/onboarding_service.py` — new orchestration service that composes ControlPlaneService, BillingService, and ProvisioningService to implement `onboard_pilot_organization`.
- `backend/app/workers/provisioning_worker.py` — small improvement: worker now updates the `Tenant` record to `provisioning_status: ready` and `status: ready` when provisioning succeeds.
- `backend/tests/test_onboarding_flow.py` — new integration test that creates an organization, plan, subscription, queues provisioning, runs the worker (Mock ERPNext), and simulates an `invoice.paid` webhook. The test asserts final tenant status and paid invoice state.

Goals achieved

- The sample onboarding flow creates Organization, Tenant, subscribes the organization to a plan, queues and runs provisioning against the mock ERPNext client, issues an invoice and accepts a simulated `invoice.paid` webhook.
- All steps run in-memory (SQLite `:memory:`) and rely on `MockBillingProvider` and `MockERPNextClient`. No live providers or secrets used.

How to run the end-to-end test locally

1. From the repository root run:

   cd backend
   python -m pytest backend/tests/test_onboarding_flow.py -q

   (If your environment runs `pytest` directly ensure you run it from the repo root so imports resolve.)

2. The test suite uses in-memory SQLite and the mock integrations so it is deterministic and fast.

Runbook / Checklist for pilot onboarding

- Create an Organization and an owner SaaSUser (the test creates one automatically).
- Create or choose a Billing Plan for the pilot client.
- Create a Tenant record tied to the Organization.
- Subscribe the Organization to the plan (BillingSubscription created).
- Generate an invoice for the subscription (BillingInvoice with status `issued`).
- Queue a provisioning job for the Tenant. The provisioning worker will run against a mock ERPNext client in tests, or the real HTTP client in production mode.
- When provisioning succeeds, the worker updates Tenant provisioning state to `ready`.
- Simulate or handle the billing provider webhook `invoice.paid` to mark the invoice paid. The application exposes a provider-agnostic `BillingService.process_webhook` helper to handle basic events in tests.

Notes / Next steps for production readiness

- Webhooks: wire real provider webhooks (Stripe) into `app/api` endpoints and validate signatures.
- Provider safety: the billing provider integrations are best-effort to avoid breaking control-plane flows. For production, add retry policies and observability for provider failures.
- Provisioning: the mock ERPNext client provides deterministic behavior for tests. For production, ensure `ERPNextHTTPClient` is hardened, idempotent, and has timeouts/retries.
- Notifications & visibility: add audit logs and admin notifications for failed provisioning or unpaid invoices.
- Security: do not commit secrets. Use environment variables and secret stores for provider keys.

That's it — the repo includes an end-to-end sample onboarding flow and an integration test you can run locally without external services.
