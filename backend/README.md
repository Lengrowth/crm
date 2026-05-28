# Backend

This is the Python API for the SaaS control layer.

## Purpose

- Store SaaS metadata and future domain models.
- Expose API endpoints for the frontend.
- Host service abstractions for billing, onboarding, and ERPNext integration.
- Keep ERPNext/Frappe abstract until live tenant infrastructure exists.

## Folder Layout

- `app/api/` - HTTP routers.
- `app/core/` - settings and shared utilities.
- `app/db/` - future persistence helpers.
- `app/models/` - placeholder domain models.
- `app/schemas/` - API schemas and request/response shapes.
- `app/services/` - service-layer abstractions.
- `app/integrations/` - external system adapters.
- `app/workers/` - future background job entry points.

## Local Development

Use Python 3.11 or newer for the backend environment.

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Environment

Copy `./.env.example` to `.env` before running the backend.

## Notes

- Phase 02 introduces the local SaaS data model, Alembic migrations, and seeded reference data.
- Phase 03 adds local SaaS auth with opaque sessions, password hashing, membership awareness, and current-user route protection scaffolding.
- Phase 05 adds protected organization and tenant CRUD with membership-aware access checks while keeping ERPNext mocked.
- The default database is a local SQLite file for MVP simplicity, but the `DATABASE_URL` stays configurable for PostgreSQL later.
- ERPNext/Frappe is still not required for local development; local/test can continue using mock mode.
- Phase 18 enables the explicit live ERPNext client path when `ERPNEXT_MODE=live` and live credentials/base URL are configured intentionally.
- Phase 19 adds the production-hardening runtime layer: security headers, lightweight rate limiting, tenant suspend/reactivate actions, and audit-log inspection for platform admins.
- Phase 20 expands local auth into a production-minded flow with password reset requests, one-time reset tokens, email verification, resend support, hashed auth-token storage, and session revocation on password reset.
