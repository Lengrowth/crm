# CHAMP-C09-R1 — Phase 02 HRMS and dependency-aware provisioning

## Release identity

- Package: `C09` — Office work, people, payroll, quality, and support
- Release type: Champion package / platform dependency implementation
- Initial state: `in_development`
- Candidate state: `corrected_candidate_pending_staging_after_runner_capacity_failure`
- Feature flag: synthetic onboarding execution remains server-controlled and off by default
- Previous known-good control-plane candidate: `802f1bdb0f7642ea627b08235dfa3aa16e7b9eda` (staging readback)
- ERP baseline: Frappe `edae775dd36b6c4ad7acab10230262bd74040765`; ERPNext `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`
- HRMS: `v15.64.1` / `e68a3deaa95ae5b2c3d743297d0a4ab505733fc1`

## Scope

- Derive required applications from effective module metadata.
- Pin HRMS and verify exact application versions by direct provider readback.
- Add idempotent HRMS installation, migration, roles/workspaces, and truthful verification.
- Preserve non-HRMS provisioning and operator/tenant authorization boundaries.
- Use synthetic data only; no payroll calculation or employee creation.

## Gate status

- Local implementation: PASS.
- Local backend tests: PASS, 68 tests.
- Staging deployment/readback: PENDING protected run for the corrected candidate. The workflow now uses the exact official HRMS `v15.64.1` revision and one bounded uninstall/clear-cache/reinstall replay for the upstream fixture failure documented in [HRMS issue #1639](https://github.com/frappe/hrms/issues/1639), followed by migration and candidate-bound installed-app/version/commit/role/workspace readback.
- Production backup/promotion: BLOCKED until staging passes.
- Champion acceptance: NOT CLAIMED.

The first protected workflow for corrected candidate
`cdae0535cb3af425b423f6858aaa779d4edf3b98` (`35483735652`) stopped before
deployment because the staging runner was full and npm returned `ENOSPC`.
No staging pointer or production resource was changed by that run. Twelve
unreferenced historical control-plane release directories were removed only
after validating that the active and previous rollback targets were preserved;
the next candidate must be independently staged and reviewed.

The subsequent candidate `3793b9870461828a8421272ac7ace6fd17297561` run
`35484379236` captured the exact backup, deployed, installed/migrated HRMS and
`lenerp_core`, and passed HTTP/service checks, but its HRMS commit readback
failed on Git dubious ownership because the smoke script used the runner user
instead of `frappe`. The readback is corrected in the next immutable candidate;
production remains unchanged.

## Recovery

Code rollback uses the immutable staging/production pointer workflow. Site schema
and application recovery are separate: restore the verified ERP backup or run
the documented app correction procedure. The prior Phase 02 staging attempt was
rolled back from `/opt/saas-control-staging/shared/backups/phase2-20260919T214541Z/`;
the corrected run has a fresh backup under
`/opt/saas-control-staging/shared/backups/phase2-20260920T020224Z/`; the
control-plane pointer remains unchanged until all gates pass. Roll back on
migration errors, authorization regressions, repeated worker failure, unhealthy
services, or failed critical smoke tests.

Full evidence is maintained in [Phase 02 implementation evidence](../../champion_showcase/10_PHASE_02_IMPLEMENTATION_EVIDENCE.md).
