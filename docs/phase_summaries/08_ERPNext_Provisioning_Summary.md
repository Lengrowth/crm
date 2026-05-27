# Phase 08 — ERPNext Provisioning and Live HTTP Client

This phase implements the concrete control-plane HTTP client and persistent provisioning worker so the SaaS control plane can talk to a live ERPNext/Frappe provisioning API (or a canonical control-plane contract defined by this repo).

What changed

- A concrete HTTP client implemented: `backend/app/integrations/erpnext/http.py` (ERPNextHTTPClient). It speaks to a REST contract under `/api/v1/sites` and related resources.
- Persistence added to the service layer: `PersistentERPNextService` in `backend/app/services/erpnext_service.py` persists provisioning runs to `tenant_provisioning` and records integration metadata in `erpnext_integration_metadata`.
- A synchronous provisioning worker: `backend/app/workers/provisioning_worker.py` creates a DB-backed provisioning record and runs provisioning in-process (idempotent-safe guard included).
- Tests: unit tests for the HTTP client and integration tests that exercise provisioning using the in-memory `MockERPNextClient` against a transient SQLite DB are included under `backend/tests/`.
- Docs: this phase summary plus `docs/07_ERPNext_Integration_Abstraction.md` updated with contract details.
- `.env.example` updated with ERPNext-related environment variables.

Canonical control-plane REST contract (adopted by the HTTP client)

- POST /api/v1/sites
  - Request: { organization_id: str, tenant_id: str, options?: dict }
  - Success (200/201): { status: "success", site_id: str, site_name: str, base_url?: str, created_at?: ISO8601 }
  - Failure: { status: "failed", error: str }

- GET /api/v1/sites/{site_id}/status
  - Success: { status: "healthy" | "creating" | "failed" | "not_found", site_id: str, site_name?: str, error?: str }

- POST /api/v1/sites/{site_id}/apps
  - Request: { app_name: str }
  - Success: { status: "success", site_id: str, app_name?: str }

- POST /api/v1/sites/{site_id}/domains
  - Request: { domain: str }
  - Success: { status: "success", site_id: str, domain: str }

- POST /api/v1/sites/{site_id}/domains/{domain}/ssl
  - Success: { status: "success", site_id: str, domain: str, ssl: "issued" }

- POST /api/v1/sites/{site_id}/backups
  - Success: { status: "success", backup_id: str, site_id: str }

- POST /api/v1/sites/{site_id}/backups/{backup_id}/restore
  - Success: { status: "success", site_id: str, backup_id: str }

- DELETE /api/v1/sites/{site_id}
  - Success: { status: "success", site_id: str }

Auth header semantics

- If `ERPNEXT_API_KEY` and `ERPNEXT_API_SECRET` are provided, the client will send:
  - Authorization: token <key>:<secret>
- Otherwise no auth header is sent.

Behavioral notes for the HTTP client

- Retries: the client has a small retry/backoff for transient errors (idempotent reads and safe POSTs are retried a few times).
- Timeouts: network calls use conservative timeouts to avoid blocking the worker forever.
- Errors: network and HTTP errors are mapped to structured return values with `status: "failed"` and an `error` string; the client does not raise in normal failure paths.
- Defensive parsing: JSON responses are parsed defensively and unexpected raw responses are included under `_raw` or stored in `details` where helpful.

Environment variables (add to `backend/.env` locally)

- ERPNEXT_MOCK_ENABLED=true|false  (default in `.env.example` is true)
- ERPNEXT_BASE_URL=https://erp.example
- ERPNEXT_API_KEY=
- ERPNEXT_API_SECRET=

How to run tests locally

- Create a virtualenv and install dependencies (project uses SQLAlchemy, FastAPI, pytest, etc):
  - pip install -e backend[dev]  # or use your preferred method
- Run tests:
  - pytest backend/tests

Next steps / considerations

- Consider adopting `httpx` + `respx` for richer async HTTP client and deterministic tests; the current client uses stdlib `urllib` and is adequate for the canonical contract.
- Add a durable background queue (RQ/Celery/FastAPI background tasks) to run provisioning asynchronously rather than inline.
- Add additional logging and observability for provisioning runs and external API calls.

If you'd like, I can switch the HTTP client to `httpx` and update tests to use `respx` for cleaner mocks. That will require adding the packages to `backend/requirements.txt` or `pyproject.toml` and updating tests accordingly.
