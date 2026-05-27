# Phase 07 — ERPNext Integration Abstraction & Mock Client

This document describes the Phase 07 deliverables: a small ERPNext integration abstraction, a deterministic mock ERPNext client for local development and tests, the service layer that coordinates provisioning flows, API endpoints, database migrations for integration metadata/provisioning records, and guidance for testing and next steps.

Summary of changes

- New abstraction: `backend/app/integrations/erpnext_client.py` — defines `ERPNextClient` interface and lightweight return-types.
- Mock client: `backend/app/integrations/mock_erpnext.py` — in-memory deterministic mock with configurable failure modes.
- Service: `backend/app/services/erpnext_service.py` — high-level flows (provision, backup/restore, status, domain binding).
- API routes: `backend/app/api/integrations.py` — endpoints for provisioning, status polling, backup/restore, and domain binding.
- Models: `backend/app/models/erpnext.py` — SQLAlchemy models `erpnext_integration_metadata` and `tenant_provisioning`.
- Alembic migration: `backend/alembic/versions/20260527_0004_erpnext_integration.py` — adds the two tables.
- Tests: `backend/tests/test_erpnext_integration.py` — unit tests for client, service, and basic API interactions.
- Docs: `docs/07_ERPNext_Integration_Abstraction.md` and `docs/phase_summaries/07_ERPNext_Integration_Summary.md` (phase summary added).
- `docs/00_Master_Index.md` updated to include the new phase summary.

Design notes

- The ERPNextClient interface is intentionally small and sync-friendly. Methods return simple dict-like records to keep the abstraction testable.
- The mock client simulates site creation, site status, app installation, domain binding, SSL issuance, backups and restores. It supports `failures` injection for deterministic failure testing.
- The service layer (`ERPNextService`) orchestrates the provisioning plan and stores lightweight in-memory provisioning records. This keeps tests DB-free. The models/migrations provide DB persistence options for a future enhancement that writes records to `tenant_provisioning` and integration metadata to `erpnext_integration_metadata`.
- API endpoints are minimal and wired to the mock by default. For local development you can replace `erp_service` with a different client implementation.

API summary

- POST /organizations/{organization_id}/tenants/{tenant_id}/provision
  - Body: ProvisionRequest { custom_app?, domain?, options: {} }
  - Returns: ProvisionResponse (202 Accepted)
  - Starts a provisioning run and returns a provisioning record with `id`.

- GET /provisioning/{provision_id}
  - Returns: ProvisionResponse
  - Poll to check provision progress and final status.

- GET /tenants/{tenant_id}/site-status?site_id={site_id}
  - Returns: SiteStatus
  - For the mock API the `site_id` query parameter is required so the controller can locate the in-memory site.

- POST /tenants/{tenant_id}/backup?site_id={site_id}
  - Returns: BackupRecord

- POST /tenants/{tenant_id}/restore
  - Body: { backup_id }
  - Query: site_id
  - Returns: OperationResult

- POST /tenants/{tenant_id}/bind-domain
  - Body: { domain }
  - Query: site_id
  - Returns: OperationResult

Database and migrations

- Alembic migration `20260527_0004_erpnext_integration.py` creates:
  - `erpnext_integration_metadata` - stores per-tenant site metadata and integration JSON.
  - `tenant_provisioning` - stores provisioning records and details.

Manual testing checklist

1. Generate and run Alembic migrations locally (example):
   - alembic upgrade head (do this locally; migrations are added but not executed in this repo change).
2. Start the backend locally (it uses the mock client by default).
3. POST to `/organizations/{org}/tenants/{tenant}/provision` and get a `provision_id`.
4. Poll GET `/provisioning/{provision_id}` until `status` is `success` or `failed`.
5. Create or read `site_id` from the provision record and call `/tenants/{tenant}/site-status?site_id={site_id}`.
6. Call `/tenants/{tenant}/bind-domain` and `/tenants/{tenant}/backup`, `/tenants/{tenant}/restore` using `site_id`.
7. Run unit tests: `pytest backend/tests/test_erpnext_integration.py`.

Limitations and known decisions

- This phase provides a mock client and abstraction. It does not implement a live ERPNext client — that will be Phase 08/09.
- Provisioning records in the service are kept in-memory to keep tests simple and deterministic. The DB models and migration are included for teams who want to persist them; wiring persistence is left as an integration step.
- The mock uses simple deterministic rules and a `failures` injection map for testing failure paths.
- The API expects `site_id` for status/backup/restore/bind-domain calls in the mock. A real implementation would look up the site_id from tenant metadata stored in DB.

Next recommended steps (Phase 08)

- Implement a concrete ERPNext HTTP client that talks to a real Frappe bench / API and conforms to `ERPNextClient`.
- Wire the `ERPNextService` to persist provisioning and integration metadata to the DB tables added by the migration.
- Add durable provisioning workers with retries and logging instead of in-memory synchronous flows.

Phase 08 (what we added)

- A concrete HTTP client implementation that reads these environment variables:
  - `ERPNEXT_BASE_URL` - base URL for the ERPNext/Frappe host (example: `https://erp.example`)
  - `ERPNEXT_API_KEY` and `ERPNEXT_API_SECRET` - optional API token credentials (used in the `Authorization: token <key>:<secret>` header)
- The HTTP client implementation is available at `backend/app/integrations/erpnext/http.py` and is used when `erpnext_mock_enabled` is set to `false` in the backend settings.
- Service persistence: a `PersistentERPNextService` was added that writes `tenant_provisioning` records and `erpnext_integration_metadata` rows during provisioning.
- A simple synchronous provisioning worker (`backend/app/workers/provisioning_worker.py`) that creates a DB provisioning record and runs the provisioning plan, updating details and final status.
- API change: the provisioning endpoint now uses the DB-backed worker and returns a provisioning id immediately. For now the worker runs synchronously; later it can be replaced with a background job queue.
- Tests: added unit tests for the HTTP client and an integration-style test that runs provisioning against an in-memory SQLite DB using the mock client.

Configuration / environment variables

- Add these values to your `backend/.env` (or set in your environment) to enable the HTTP client:
  - `ERPNEXT_BASE_URL=https://erp.example`
  - `ERPNEXT_API_KEY=` (optional)
  - `ERPNEXT_API_SECRET=` (optional)
  - `ERPNEXT_MOCK_ENABLED=true|false` (the project uses `erpnext_mock_enabled` in `app.core.config.settings` - set to `false` to use the HTTP client)

Manual testing steps (Phase 08)

1. Ensure your DB has the new `tenant_provisioning` and `erpnext_integration_metadata` tables (run alembic upgrade head or create tables locally).
2. Configure `ERPNEXT_BASE_URL` (and optionally API key/secret) in your `.env` used by the backend.
3. Start the backend and POST to `/organizations/{org}/tenants/{tenant}/provision` with a `ProvisionRequest` body.
4. The endpoint returns a `provision_id` (202). For now the worker runs synchronously and the record should be updated to `success` before the response completes.
5. Poll `/provisioning/{provision_id}` to inspect `details` and final `status`.

Run instructions for tests

- From repository root run:
  - pip install -e backend[dev]  # or your chosen virtualenv setup
  - pytest backend/tests


If you want, I can now:
- Add an integration that uses respx/httpx for more realistic HTTP client tests.
- Add a background job adapter (e.g., FastAPI BackgroundTasks, RQ, or Celery) to run provisioning asynchronously.
- Harden retries, logging, and idempotency checks for the worker.
