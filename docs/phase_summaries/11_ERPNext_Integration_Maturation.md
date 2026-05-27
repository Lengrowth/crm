# Phase 11 — ERPNext Integration Maturation

Goal
----
Replace the mock ERPNext client with a clear integration abstraction and a pluggable mock + real HTTP client. Provide an interface for future live connection handling while maintaining no live ERPNext requirement for tests.

What I added
------------
- `backend/app/integrations/erpnext/interfaces.py` — Protocol `ERPNextClient` describing the adapter interface with async methods:
  - `create_site(site_name: str, admin_password: str, config: Optional[Dict]) -> Dict`
  - `create_user(site_name: str, user_payload: Dict) -> Dict`
  - `get_site_status(site_name: str) -> Dict`

- `backend/app/integrations/erpnext/mock.py` — `MockERPNextClient` deterministic in-memory mock used for development and tests. No network I/O.

- `backend/app/integrations/erpnext/http.py` — `HttpERPNextClient` thin wrapper around `httpx.AsyncClient`. Reads `ERPNEXT_BASE_URL` and `ERPNEXT_API_KEY` from environment by default. Defensive JSON parsing and simple helpers; intentionally small and safe.

- `backend/app/services/erpnext_integration_service.py` — Service-level factory and convenience functions:
  - `get_erpnext_client()` selects adapter based on `ERPNEXT_MOCK_ENABLED` (defaults to enabled)
  - `provision_tenant(...)`, `create_site_user(...)`, `get_site_status(...)` convenience async functions delegating to adapter

- Tests in `backend/tests/integrations`:
  - `test_erpnext_mock.py` — exercises `MockERPNextClient` deterministically
  - `test_erpnext_http_respx.py` — exercises `HttpERPNextClient` using `respx` to mock HTTP endpoints (no live network calls)

Why this design
----------------
- The `ERPNextClient` protocol keeps the contract explicit and small so callers don't rely on anything beyond the three core operations.
- The mock client ensures tests and local development never require a live ERPNext server.
- The HTTP client is intentionally thin: it only encapsulates httpx usage and reads credentials from env. Integration secrets should be provided via environment variables or a secret manager in real deployments (out-of-scope for this phase).
- The service factory uses an env var toggle so switching from mock to HTTP is a simple configuration change.

How to enable/disable the mock
------------------------------
- By default the mock client is enabled. To use the HTTP client instead set:

  - `ERPNEXT_MOCK_ENABLED=0` (or `false` / `no`)
  - `ERPNEXT_BASE_URL=https://erp.example`
  - `ERPNEXT_API_KEY=<your_api_key>`

  Note: Do NOT commit secrets to the repo. Use environment variables in deployment or a secret manager. The HTTP client accepts `ERPNEXT_API_KEY` for bearer-style auth; adapt to your real auth mechanism later.

Running tests
-------------
- The HTTP client tests use `respx` to mock HTTP endpoints, so they don't perform real network calls.
- Example commands (from repo root):

  - Install test deps if needed: `pip install -r requirements-dev.txt` (or `pip install pytest pytest-asyncio respx httpx`)
  - Run tests: `pytest backend/tests/integrations -q`

Safety guidance for enabling a real client
----------------------------------------
- Do not place secrets in code or commit `.env` files containing real credentials.
- Prefer passing credentials via environment variables managed by your deployment system or a secrets manager.
- Consider adding integration-specific configuration records to the DB that reference secret manager keys rather than storing secrets directly.
- When connecting to a real ERPNext instance, add rate limiting, retries, and observability (request IDs, logs) appropriate for your SLA.

Next steps (optional)
---------------------
- Expand the HTTP client with retry/backoff and better error modeling.
- Add data models/DTOs for the responses to avoid loosely-shaped dicts across the codebase.
- Add tests that exercise failure modes (4xx/5xx) and ensure service-level error handling is appropriate.

Files changed/created
---------------------
- `backend/app/integrations/erpnext/interfaces.py`
- `backend/app/integrations/erpnext/mock.py`
- `backend/app/integrations/erpnext/http.py`
- `backend/app/services/erpnext_integration_service.py`
- `backend/tests/integrations/test_erpnext_mock.py`
- `backend/tests/integrations/test_erpnext_http_respx.py`
- `docs/phase_summaries/11_ERPNext_Integration_Maturation.md`

If you'd like I can:
- Add stronger HTTP client error handling and retries,
- Replace the simple env-var toggle with dependency injection wiring used by the app framework,
- Or implement a small IntegrationCredential model + loader that reads DB records and resolves secrets from a secret manager (next-phase work).
