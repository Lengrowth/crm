# Phase 15 — Production Website And Readiness Cleanup

## Date
2026-05-27

## Goal
Prepare the repository for Phase 15 launch/demo readiness without starting live ERPNext cutover or deployment.

## What changed

### Frontend launch cleanup
- Replaced public-facing placeholder marketing copy with launch/demo-ready content across:
  - homepage
  - pricing
  - contact
  - demo
  - industries
  - modules
  - drilling
- Added legal routes:
  - `frontend/app/(marketing)/privacy/page.tsx`
  - `frontend/app/(marketing)/terms/page.tsx`
- Added stronger site metadata and indexing rules:
  - root metadata updates in `frontend/app/layout.tsx`
  - `frontend/app/robots.ts`
- Added a marketing footer with legal/demo/contact links.

### Dashboard cleanup
- Reduced phase/scaffold-oriented copy in the protected shell.
- Reframed dashboard pages around operator workflows instead of earlier phase narration.
- Switched the tenant list page from hard-coded sample rows to the protected tenants API.
- Kept draft forms for new organizations/tenants honest about their current role while making the copy demo-ready.

### ERPNext mock/live safety cleanup
- Added explicit ERPNext runtime mode handling in `backend/app/integrations/erpnext_runtime.py`.
- Kept mock mode available for local/test environments.
- Changed production-like default behavior from implicit mock fallback to safe disabled mode unless explicitly configured.
- Kept live mode intentionally gated for a later cutover phase rather than pretending the repository is already ready for real ERPNext activation.
- Exposed runtime mode visibility through:
  - `GET /integrations/erpnext/runtime`
  - `GET /health` fields for ERPNext mode/policy

### Deprecated integration cleanup
- Removed older placeholder/duplicated ERPNext integration files that should no longer be used.
- Kept the active HTTP client implementation as a future-facing cutover asset while isolating it from production use in Phase 15.

## Validation run
- `PYTHONPATH=backend python -m pytest backend/tests/test_erpnext_runtime.py backend/tests/test_erpnext_http_client.py`
- `npm --prefix frontend run typecheck`
- `npm --prefix frontend run build`

All of the above passed after cleanup fixes.

## What remains for later phases

### Phase 16
- Production deployment topology on GCP
- runtime/service supervision
- reverse proxy and TLS
- smoke-test deployment workflow
- server-side environment configuration

### Phase 18
- real ERPNext credential/reference path
- live HTTP client activation in production flows
- tenant-to-site mapping validation against a real runtime
- live health/provisioning checks
- operator cutover and rollback procedures
