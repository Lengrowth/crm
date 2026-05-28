# Phase 18 — Live SaaS ↔ ERPNext Integration Cutover

## Date
2026-05-28

## Goal
Complete the first safe live SaaS-to-ERPNext cutover path now that Phase 16 (SaaS control-plane deployment) and Phase 17 (ERPNext runtime deployment) are already online.

## What changed

### Live ERPNext client activation
- Updated `backend/app/integrations/erpnext_runtime.py` so `ERPNEXT_MODE=live` now activates the real `ERPNextHTTPClient` instead of remaining hard-gated.
- Added explicit live configuration validation for:
  - `ERPNEXT_BASE_URL`
  - ERPNext auth material (`ERPNEXT_API_KEY` with optional `ERPNEXT_API_SECRET`, depending on upstream auth style)
- Kept safe behavior intact:
  - local/test can still use mock mode
  - non-local mock usage still requires explicit override
  - production-like environments still do not silently fall back to mock mode

### Runtime visibility and cutover observability
- Expanded the runtime summary returned by `GET /integrations/erpnext/runtime` to expose:
  - active environment
  - current ERPNext mode
  - live/disabled/configuration policy
  - safe target host display
  - active auth mode when live
- Updated backend logging to record whether the ERPNext client selection is using mock or live mode.

### Tenant-to-site mapping for already-created ERPNext sites
- Added `GET /tenants/{tenant_id}/integration/erpnext` to inspect the current SaaS-side ERPNext link state for a tenant.
- Added `PUT /tenants/{tenant_id}/integration/erpnext` to upsert manual cutover mapping data for an already-existing ERPNext site.
- The mapping endpoint stores and exposes:
  - ERPNext site ID
  - ERPNext site name
  - ERPNext base URL
  - API key / secret references
  - cutover metadata for operator notes and traceability
- This closes the gap where live tenants created during Phase 17 existed in ERPNext but could not be linked cleanly into the SaaS layer without re-running provisioning.

### SaaS-side persistence alignment
- Updated persistent provisioning success/failure handling in `backend/app/services/erpnext_service.py` so tenant records now stay in sync with provisioning results.
- Successful provisioning now updates tenant state to:
  - `status=ready`
  - `provisioning_status=ready`
  - `erpnext_site_name`
  - `erpnext_base_url` when available
- Failed provisioning now updates tenant state to:
  - `status=failed`
  - `provisioning_status=failed`
- Provisioning start now marks the tenant as `provisioning` / `running`.

### Documentation sync
- Updated `backend/README.md` to reflect that Phase 18 now supports an explicit live ERPNext cutover path rather than remaining mock-only.
- Added this Phase 18 summary to `docs/00_Master_Index.md`.

## Validation run
- Ran targeted backend tests successfully:
  - `backend/tests/test_erpnext_runtime.py`
  - `backend/tests/test_erpnext_cutover_mapping_api.py`
  - `backend/tests/test_erpnext_provision_persistence.py`
- Command used:
  - `backend/.venv311/Scripts/python.exe -c "import sys, pytest; sys.path.insert(0, r'C:\\Users\\smikl\\Desktop\\Work\\crm\\backend'); raise SystemExit(pytest.main(['backend/tests/test_erpnext_runtime.py', 'backend/tests/test_erpnext_cutover_mapping_api.py', 'backend/tests/test_erpnext_provision_persistence.py']))"`

## What remains for later phases

### Operational hardening still belongs to Phase 19
- broader audit logging for every live ERP action
- operator-facing monitoring/alerting
- rate limiting and stronger guardrails around dangerous mutation endpoints
- recovery and incident-response workflow hardening

### Pilot go-live work still belongs to Phase 20
- first real client onboarding end to end
- live user setup and training
- initial data import and operational handoff
- support escalation and pilot success criteria
