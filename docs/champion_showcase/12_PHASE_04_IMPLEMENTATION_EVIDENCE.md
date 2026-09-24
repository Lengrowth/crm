# Phase 04 — Role-Based ERP Shell and Module Home Evidence

**Status:** IMPLEMENTED, protected-main merged, and protected synthetic staging
verified; production promotion is pending the required operational approvals.
**Production Champion workspace flag:** `off`.
**Real Champion data/payroll/identity cutover:** not enabled or used.

## Exact release inputs

- Control-plane Phase 04 implementation merge: `d367883927c6406b40b645d4e66eeb71aaf77d4f`.
- Current protected-main candidate: `30732f6eb0606fb08e14e155f5f669faf85eac94`.
- Canonical `lenerp_core` source: `6629ea60bd4093907a89bae8f3712ceb5c6a1cd6`.
- Canonical `lenerp_core` version: `0.3.0`.
- Immutable staged archive:
  `ops/staging/lenerp_core-6629ea60bd4093907a89bae8f3712ceb5c6a1cd6.tar`.
- Archive SHA-256:
  `EE4BAAEC71998D0EEF7F556D56BFCC6E47EA8FE56D8E62260FCDC4B1DA459753`.
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

- Canonical `lenerp_core` tests: `20 passed`.
- Staged mirror `lenerp_core` tests: `20 passed`.
- Staged mirror Python compilation: passed.
- ERP release smoke contract tests: `4 passed`.
- Backend full suite with `PYTHONPATH=backend`: `93 passed`, 25 existing
  deprecation warnings.
- Frontend Vitest: `12 passed` in 4 files.
- Frontend typecheck: passed.
- Frontend production build: passed.
- Protected staging browser, axe, 320 CSS-pixel, 200% zoom, direct-route/API
  denial, cross-navigation tenant context, empty/error-state, role, and
  installed-app/module readback: **passed** in the post-merge workflow run
  `35988056898`.
- Staging release ID: `30732f6eb0606fb08e14e155f5f669faf85eac94`.
- Staging candidate: `30732f6eb0606fb08e14e155f5f669faf85eac94`.
- Staging custom app commit: `6629ea60bd4093907a89bae8f3712ceb5c6a1cd6`.
- Staging HRMS: `15.64.1`; installed apps read back as `frappe`, `erpnext`,
  `lenerp_core`, and `hrms`; site `erp-staging.example.test`.
- Durable evidence artifact: `staging-browser-evidence-30732f6eb0606fb08e14e155f5f669faf85eac94`,
  artifact ID `10803711362` from workflow run `35988056898`.
- The synthetic staging run enabled the workspace flag only for staging,
  verified all nine role principals and permission denials, and removed the
  disposable synthetic principals and records during cleanup.

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
an approved decision to enable any synthetic role rollout. Protected staging
and the protected-main merge are complete, but production promotion and its
required operational approvals are not; the Phase 05 gate is therefore
**not open**.
