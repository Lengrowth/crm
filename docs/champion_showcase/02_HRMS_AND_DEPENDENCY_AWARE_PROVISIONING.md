# Phase 02 — HRMS and Dependency-Aware Provisioning

## AI goal

Make module-required applications real: pin HRMS for the existing Frappe/ERPNext v15 baseline, install it safely when an effective module requires it, and verify the actual site before marking HR or Payroll applied/verified.

## Architecture rule

Provisioning must derive applications from effective module metadata. Do not add a one-off UI flag that pretends HRMS exists, and do not rely forever on a hard-coded `install_hrms` branch. A deterministic resolver should produce the required set from modules and platform requirements.

## Build scope

1. Select and record an HRMS revision compatible with the pinned Frappe/ERPNext v15 revisions.
2. Add HRMS source/build/install ownership to release manifests, dependency checks, licenses and handover inventory.
3. Resolve required applications from the effective module set.
4. Extend provisioning with idempotent fetch/build availability, site installation, migration and readback for HRMS.
5. Preserve ordered dependencies: create site → install ERPNext → install HRMS when required → install `lenerp_core` → migrate → apply module/role/workspace configuration → verify.
6. Update verification to require the union of backing applications for selected modules, not only Frappe/ERPNext/`lenerp_core`.
7. Record actionable failure reasons without command output secrets.
8. Prove clean installation, migration, replay and rollback on the isolated staging site.
9. Keep upstream Frappe, ERPNext and HRMS trees clean; Champion behavior remains in `lenerp_core`.

## UX requirements

- Provisioning progress says “Installing People & Payroll capability” with expandable technical detail, rather than exposing only package names.
- Missing HRMS shows `Needs attention`, never `Verified`.
- Retry resumes from verified completed steps and does not reinstall or duplicate schema work.
- Operators can see exact app versions; ordinary Champion users see only understandable readiness state.

## Acceptance tests

- A bundle without HR/Payroll does not require HRMS.
- A bundle with HR or Payroll installs the pinned HRMS app.
- Existing installed HRMS is detected and replayed safely.
- Missing or incompatible HRMS blocks verification and preserves truthful module state.
- A clean disposable site can install ERPNext, HRMS and `lenerp_core`, migrate, list apps and load the required workspaces.
- Retry after an interrupted install converges without duplicate application or role records.
- Rollback/recovery instructions cover code, site schema and app availability separately.

## Non-goals

- Real employee or payroll data.
- Champion salary structures, tax rules or accounting approval.
- Production installation before protected staging evidence.

## Gate and rollback

Phase passes only with exact-candidate staging evidence. A production candidate must keep new HR/Payroll visibility disabled until installation and verification succeed. Rollback returns the code/configuration pointer and restores/corrects site state through the rehearsed app/schema procedure.

## Execution prompt

> Implement dependency-aware Frappe application provisioning and add a pinned HRMS v15 dependency for modules that require it. Update manifests, verification, tests and staging smoke evidence. Never mark HR or Payroll applied/verified without site readback, keep upstream repositories clean, use only synthetic records, and do not install anything on production without the protected gate.
