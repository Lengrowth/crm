Phase-by-Phase AI Task Prompts (Phases 10–14)

Purpose

This document provides concrete, repeatable AI (or human) task prompts for continuing the implementation roadmap after Phase 09. Each phase contains a short goal, a definition of done, suggested implementation steps mapped to repository files, testing guidance, and important design constraints. Use these as prompts for an AI assistant to implement the work in this repository's style (FastAPI backend, SQLAlchemy ORM, pydantic, conservative scope).

General rules to follow for all phases
- Follow the repository conventions in crm/AGENTS.md (FastAPI service, SQLAlchemy ORM, pydantic schemas, lightweight placeholder services until the phase calls for more integration).
- Keep changes minimal and localized to the files required by the phase. Update docs and tests as part of the same PR.
- Never commit secrets. Add env.example entries for required configuration.
- Tests must be deterministic and use in-memory SQLite where appropriate.
- Use existing patterns: app.db.base.Base, app.models.* TimestampMixin/UUIDMixin, app.api.router registration, app.services.* patterns.

Phase 10 — White-label and Domain Management (goal)
Goal
Add support for per-tenant white-label configuration and domain metadata, manual activation metadata and a UI-ready API so operations teams can manage tenant DNS/SSL metadata.

Definition of Done
- Models for domain records and white-label metadata exist and have migration.
- Router endpoints exist for listing/updating domain metadata and performing manual activation toggles.
- Tests exist for models, service logic, and API endpoints using in-memory SQLite.
- Docs updated (docs/phase_summaries/10_WhiteLabel_and_Domain_Management.md) describing API contracts and runbook for manual activation.

Concrete file tasks
1) Models
- Add `backend/app/models/domain_management.py` or extend `app/models/domain.py` with fields supporting white-label metadata: `tenant_id`, `domain`, `is_active`, `manual_activation_required`, `dns_verified_at`, `ssl_status`, `manual_activation_by`, `manual_activation_at`, `notes_json`.
- Use UUIDMixin and TimestampMixin.

2) Alembic migration
- Add migration under `backend/alembic/versions` creating/updating tables and indexes.

3) Schemas
- Add `backend/app/schemas/domain_management.py` with `DomainOut`, `DomainUpdateRequest`, `ManualActivationRequest`.

4) Service
- Add `backend/app/services/domain_service.py` with logic to validate domains, mark DNS verified, mark SSL status, and toggle manual activation.

5) API router
- Add `backend/app/api/domain_management.py` and include in `app/api/router.py`. Expose endpoints:
  - GET /tenants/{tenant_id}/domains
  - POST /tenants/{tenant_id}/domains  (create)
  - PATCH /tenants/{tenant_id}/domains/{domain_id}
  - POST /tenants/{tenant_id}/domains/{domain_id}/manual_activate

6) Tests
- Unit tests for service domain verification logic.
- API tests using TestClient for create/update/manual activate flows.

7) Docs & env
- docs/phase_summaries/10_WhiteLabel_and_Domain_Management.md with runbook for DNS/SSL and field definitions.
- Add any env.example entries if needed (none expected for manual flows).

Design notes
- Domain verification is an operational process — keep the API purely metadata-driven (status flags), do NOT attempt DNS queries or SSL provisioning in this phase. Provide hooks (future worker tasks) for automated checks.


Phase 11 — ERPNext Integration Maturation (goal)
Goal
Replace the mock ERPNext client with a clear integration abstraction and a pluggable mock + real HTTP client. Provide an interface for future live connection handling while maintaining no live ERPNext requirement for tests.

Definition of Done
- Clear adapter interface `ERPNextClient` with methods for tenant/site creation, user creation, and configuration.
- Implement a `MockERPNextClient` and an `HttpERPNextClient` (the latter must be a thin wrapper around httpx but can be no-op or prepared for later use). Do not attempt a live connection in tests.
- Add service `app.services.erpnext_integration` that depends on `ERPNextClient` via simple factory selected by config (env var ERPNEXT_MOCK_ENABLED).
- Tests for integration adapters: mock adapter is exercised; HTTP adapter tested with respx/respx mocking.
- Docs update describing how to switch to real client and safety guidance.

Concrete file tasks
1) Interfaces and adapters
- Create: `backend/app/integrations/erpnext/interfaces.py` with `class ERPNextClient(Protocol):` (methods signatures).
- Create: `backend/app/integrations/erpnext/mock.py` implementing the protocol.
- Create: `backend/app/integrations/erpnext/http.py` implementing the protocol with httpx client and placeholders.

2) Service
- `backend/app/services/erpnext_integration_service.py` selects adapter based on config and exposes `provision_tenant`, `create_site_user`, `get_site_status`.

3) Tests
- Unit tests using respx to simulate HTTP responses for the HTTP client.
- Tests for the mock client ensuring deterministic return values for provisioning steps.

4) Docs
- docs/phase_summaries/11_ERPNext_Integration_Maturation.md: interface description, how to enable/disable mock, guidance for adding secrets to env, and how to run respx-based tests.

Design notes
- Keep the production HTTP client slender and safe (no secrets in code). The HTTP client should accept credentials via environment or IntegrationCredential records in DB; storing secrets as references to secret managers is preferrable (out-of-scope now).


Phase 12 — Durable Provisioning Jobs and Observability (goal)
Goal
Implement a durable provisioning job table, a simple worker pattern for retries, status tracking, and logs; provide APIs to kick off and inspect provisioning jobs for tenants.

Definition of Done
- Models: ProvisioningJob (if not already present) with status queueing and attempt_count, logs JSON.
- API endpoints to queue a provisioning job, get job status and logs.
- Worker skeleton: a simple `app.workers.provisioning_worker` that can be invoked directly in tests to run a job (no external queue system required for Phase 12).
- Tests: create a job, run worker, observe status changes and logs, test retry semantics.
- Docs: runbook and how to inspect job table and logs.

Concrete file tasks
1) Models
- Confirm or add `ProvisioningJob` in `app/models/domain.py` (already exists but may need small extension: `logs_json` is already present — use it). If missing fields, add migration.

2) Service & Worker
- Add `backend/app/services/provisioning_service.py` with `queue_provisioning_job`, `get_job_status`, `append_job_log`.
- Add `backend/app/workers/provisioning_worker.py` with an executable function `run_next_job(session)` that picks queued job, runs a simulated provisioning algorithm (call to ERPNext integration mock), marks job finished or failed and appends logs and increments attempts. Keep deterministic behavior in tests.

3) API
- Add endpoints under `/tenants/{tenant_id}/provisioning_jobs` for POST (queue) and GET (list jobs) and GET /jobs/{job_id}

4) Tests
- End-to-end test: queue job, call worker.run_next_job(session) directly, assert job status, logs and attempt_count.

5) Docs
- docs/phase_summaries/12_Durable_Provisioning_Jobs.md describing the worker, retry policy, and how to operationally re-run failed jobs.

Design notes
- Do not introduce Celery/Kafka/Kubernetes at this stage; keep worker invokable synchronously for Phase 12 and provide later hooks for scheduling/queueing.


Phase 13 — Billing Provider Integration (goal)
Goal
Add a pluggable billing provider adapter and a Stripe placeholder adapter to map BillingService actions to provider calls. Keep provider calls isolated and easily disabled for tests.

Definition of Done
- Provider interface (BillingProvider) with charge, create_customer, create_subscription, invoice actions.
- Implement `MockBillingProvider` for tests and `StripeBillingProvider` as a placeholder (no SDK; build HTTP wrapper or a stub that logs intended calls — do not commit secrets).
- BillingService updated to call BillingProvider for relevant flows (customer creation, subscription creation, invoice issuance). For Phase 13, provider interactions should be best-effort: failures should not break local manual flows (graceful degradation).
- Tests: provider mocked to assert calls are made; unit tests for BillingService now verify provider interactions via a test provider instance.
- Docs: how to configure provider via env, placeholder for STRIPE_API_KEY, and migration notes if provider metadata is stored.

Concrete file tasks
1) Provider interface
- Add `backend/app/services/billing_provider.py` with interface and two implementations `mock` and `stripe_placeholder`.

2) Integrate
- Update `backend/app/services/billing_service.py` to accept optional provider (constructor DI or get via factory). Add tests that pass a `MockBillingProvider` into the service.

3) Tests
- New tests to assert provider calls (e.g., when subscribing, provider.create_subscription should be called with expected payload).

4) Docs
- docs/phase_summaries/13_Billing_Provider_Integration.md describing provider interface and configuration.

Design notes
- Avoid adding real Stripe SDK in this phase until the team approves adding a vendor SDK. Using HTTP calls with HMAC signing or secure secret storage is out of scope; use provider wrappers and leave final integration for Phase 14.


Phase 14 — Pilot Client Onboarding End-To-End (goal)
Goal
Implement the final bits for an end-to-end pilot onboarding: tenant provisioning flow tied to subscription and billing, pilot-ready checklists, and a sample integration test that simulates full onboarding without real external services.

Definition of Done
- A sample onboarding flow that creates an Organization, Tenant, subscribes the organization, provisions the tenant (via the provisioning worker + ERPNext mock), issues an invoice and marks it paid (via MockBillingProvider or webhook simulation). All steps must be covered by automated tests.
- Add a comprehensive integration test that runs the full flow in-memory (no real external services) and asserts final tenant status and billing state.
- Docs: Phase 14 summary with step-by-step pilot onboarding runbook and next steps for production readiness.

Concrete file tasks
1) Orchestration
- Add `backend/app/services/onboarding_service.py` that composes ControlPlaneService, BillingService, ERPNext integration, and ProvisioningService to implement `onboard_pilot_organization` which runs the steps and returns a status object.

2) Tests
- An integration test `backend/tests/test_onboarding_flow.py` that creates an organization, sets up plan, subscribes, provisions tenant (worker invoked), generates invoice, simulates invoice.paid webhook, and asserts final tenant status (ready) and subscription status active/paid invoice.

3) Docs
- docs/phase_summaries/14_Pilot_Client_Onboarding.md with checklist and commands to run the end-to-end test locally.

Design notes
- Keep this phase focused on in-repo orchestration and deterministic test flows. Do not wire live provider keys or live ERPNext servers in tests. Emphasize safe staging practices in the docs.


Appendix: How to convert these prompts into an AI task
- For each phase file list, instruct the agent to:
  1) Read relevant files in the repository (models, services, existing APIs) before making changes.
  2) Add models consistent with existing patterns (UUIDMixin, TimestampMixin, mapped_column types).
  3) Add Alembic migrations for DB changes and keep down_revision consistent with latest revision.
  4) Add pydantic schemas under `backend/app/schemas/` and router under `backend/app/api/` and include it in `app/api/router.py`.
  5) Add tests under `backend/tests` that use `sqlite:///:memory:` and call `Base.metadata.create_all(bind=engine)` in setup.
  6) Update docs under `docs/phase_summaries` and `.env.example` when new env keys are required.
  7) Run `pytest backend/tests -q` and `alembic upgrade head` locally to validate; report back failing tests and fix them.

- Provide the AI with the project root (C:\Users\smikl\Desktop\Work\crm) and the repository rules found in crm/AGENTS.md.

If you'd like, I can now scaffold Phase 10 (create models, migration, API, tests and docs) following this prompt set. Which phase should I implement next? If you want them all scaffolded as individual PR-ready changes, tell me whether to proceed strictly sequentially (phase 10 then 11 then 12...) or work in parallel on multiple phases (I can create disjoint write sets for each phase and run them in parallel where appropriate).