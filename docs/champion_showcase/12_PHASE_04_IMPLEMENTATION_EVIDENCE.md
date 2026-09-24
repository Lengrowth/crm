# Phase 04 — Role-Based ERP Shell and Module Home Evidence

**Status:** IMPLEMENTED LOCALLY; protected staging and production promotion are pending.
**Production Champion workspace flag:** `off`.
**Real Champion data/payroll/identity cutover:** not enabled or used.

## Exact release inputs

- Control-plane candidate: the Phase 04 branch commit recorded after the final
  protected-main merge.
- Canonical `lenerp_core` source: `5955cc8ac2aa0a2f0fb671aa2f25d3e8c5e7a5b4`.
- Canonical `lenerp_core` version: `0.3.0`.
- Immutable staged archive:
  `ops/staging/lenerp_core-5955cc8ac2aa0a2f0fb671aa2f25d3e8c5e7a5b4.tar`.
- Archive SHA-256:
  `9729D0B1230DCD08E8D0502EA622D58B2CB863FBDD0BDBDDCB4C72483B8CC8D1`.
- Staged application dependency baseline: Frappe `15.119.1`, ERPNext
  `15.120.0`, HRMS `15.64.1`, and `lenerp_core 0.3.0` at the exact source
  commit above.

## Implemented boundary

The version-controlled `lenerp_core` registry defines nine role homes and the
Champion-language navigation. `/champion-home` and
`lenerp_core.api.module_home` are server-gated by
`lenerp_phase4_workspace_enabled` plus the optional role rollout map. Every
record source is read through Frappe permission checks; the response contains
no financial or payroll totals and does not copy records into the control
plane. Missing optional DocTypes are rendered as `Pending configuration`.

The existing `Champion ERP` Workspace remains present as the rollback surface.
Phase 03’s authorized `Open ERP` and `LenERP Control Plane` handoff remains
unchanged, including the tenant and organization context.

## Local validation

- Canonical `lenerp_core` tests: `19 passed`.
- Staged mirror `lenerp_core` tests: `19 passed`.
- Staged mirror Python compilation: passed.
- ERP release smoke contract tests: `4 passed`.
- Backend full suite with `PYTHONPATH=backend`: `93 passed`, 25 existing
  deprecation warnings.
- Frontend Vitest: `12 passed` in 4 files.
- Frontend typecheck: passed.
- Frontend production build: passed.
- Protected staging browser, axe, 320 CSS-pixel, 200% zoom, and installed-
  app/module readback: **Pending protected staging run**.

## Required protected staging evidence

Run the candidate workflow with `phase4_champion_workspace_state=on` only in
the synthetic staging site. Retain the exact candidate SHA, installed-app
readback, roles/workspaces, representative records, role-by-role screenshots,
axe output, keyboard/zoom/responsive checks, direct-route/API denial results,
cross-navigation tenant context, empty/partial/slow/failed/access-denied
states, and rollback result with the workflow artifact ID and release ID.

The staging candidate must prove all nine roles before approval. Production
must remain at `lenerp_phase4_workspace_enabled=off`; no real Champion records,
payroll, identity cutover, or unapproved workflow rules may be enabled.

## Rollback

Set `lenerp_phase4_workspace_enabled=0` and clear
`lenerp_phase4_role_rollout`. Restart/clear the ERP site cache, verify `/app`
still opens the existing `Champion ERP` Workspace, and verify the standard
DocType/report routes and direct authorization denials. Preserve the package,
identity mappings, audit records, and backups; do not delete records as part
of rollback.

## Phase 05 entry gate

Phase 05 may begin only after the exact Phase 04 candidate has passed protected
staging evidence, protected-main merge, production code promotion with the
workspace flag still off, deployed-SHA/health/access-denial verification, and
an approved decision to enable any synthetic role rollout. The Phase 05 gate
is therefore **not open** from this local implementation alone.
