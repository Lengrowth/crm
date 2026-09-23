# CHAMP-C09-R1 — Phase 02 HRMS and dependency-aware provisioning

## Release identity

- Package: `C09` — Office work, people, payroll, quality, and support
- Release type: Champion package / platform dependency implementation
- Initial state: `in_development`
- Candidate state: `phase02_production_verified`
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
- Local backend tests: PASS, 74 tests.
- Staging deployment/readback: the historical dirty/partial-site failure is not a compatibility verdict. Clean disposable proof passed with the exact install order and resolved `Expense Claim Type` to `HR/hrms`; final protected run `35506309957` / job `106066811682` passed the candidate-bound staging gates.
- Production backup/promotion: PASS. Main commit `44cb6a360d078d9520a8b14f138e03477af82d26` passed protected staging run `35913962740` and production workflow `35915114849`; deployment `6623549817` completed successfully.
- Champion acceptance: NOT CLAIMED.

Current AWS/Cloudflare state: production is serving the exact main release
`44cb6a360d078d9520a8b14f138e03477af82d26`. The production ERP readback
reports the exact pinned Frappe, ERPNext, HRMS, and `lenerp_core` identities;
the prior unpinned LenERP checkout is historical and superseded.
Both public Cloudflare hostnames returned HTTP 200; no DNS, tunnel, or edge
mutation was made.

Final Phase 02 evidence identity: reviewed head
`796ea2e0cd7aae0bd2b19bc88e6750b93f1a5642`, merge candidate
`9674a6a1b4adf9447af759458763b25721672272`, artifact
`staging-browser-evidence-9674a6a1b4adf9447af759458763b25721672272`, artifact
ID `10603752341`, digest
`sha256:bd808a20f5f9743e122dc064113160dbf60ad8bd073638b9dd132bf4c191a8ef`.
Production promotion was executed and verified; Phase 02 is PASS and Phase 03
may begin from the merged main baseline.

The first protected workflow for the corrected candidate
`cdae0535cb3af425b423f6858aaa779d4edf3b98` (`35483735652`) stopped before
deployment because the staging runner was full and npm returned `ENOSPC`.
No staging pointer or production resource was changed by that run. Twelve
unreferenced historical control-plane release directories were removed only
after validating that the active and previous rollback targets were preserved;
that historical candidate is superseded by the passing final candidate below.

The subsequent historical candidate `3793b9870461828a8421272ac7ace6fd17297561`
run `35484379236` captured the exact backup, deployed, and attempted to
install/migrate HRMS and `lenerp_core`. It failed at HRMS commit readback
because the smoke script used the runner user instead of `frappe`; the
historical result is superseded and production remains unchanged.

The earlier source investigation over-interpreted Issue #1639. Its traceback
shows a failed site resolving the fixture through `frappe.core`; it does not
prove that HRMS lacks the DocType. The new disposable proof is recorded in
`ops/staging/evidence/phase2-clean-disposable-install.json` and shows the
official pinned site resolving `Expense Claim Type` to module `HR` with
`Module Def.app_name = hrms`. No upstream source, fixture, or baseline was
patched; the exact pins remain unchanged.

## Corrected evidence sequence

1. Historical dirty/partial-site failure: run `35484379236` exposed a
   readback/ownership defect and the earlier replay exposed stale metadata;
   neither is compatibility evidence.
2. Successful protected run: `35484693593` / job `106008810882` completed
   pinned HRMS and LenERP staging verification for candidate
   `27f4907578f09e1f540c90e7e6d8fd30fd9aaeb5`.
3. New clean disposable proof: site
   `phase2-clean-20260920t095000z.example.test` passed one-time installation
   and migration of Frappe, ERPNext, HRMS, and `lenerp_core`, with exact source
   readbacks and HRMS metadata before/after installation.
4. Final candidate-bound staging result: protected run `35505538638` / job
   `106064600813` passed for release `fa137051b6675fbd09102c07942748ce68ea98b9`
   (PR head `cffe8f9e5499f0845fce2dbceec1767c7a3e5ee4`).

## Recovery

Code rollback uses the immutable staging/production pointer workflow. Site schema
and application recovery are separate: restore the verified ERP backup or run
the documented app correction procedure. The prior Phase 02 staging attempt was
rolled back from `/opt/saas-control-staging/shared/backups/phase2-20260919T214541Z/`;
the corrected final run has a fresh backup under
`/opt/saas-control-staging/shared/backups/phase2-fa137051b6675fbd09102c07942748ce68ea98b9-35505538638/`;
the staging pointer now records the passed candidate and production remains
unchanged. Roll back on
migration errors, authorization regressions, repeated worker failure, unhealthy
services, or failed critical smoke tests.

The final candidate-bound evidence artifact is
[staging-browser-evidence-fa137051b6675fbd09102c07942748ce68ea98b9](https://github.com/Lengrowth/crm/actions/runs/35505538638/artifacts/10603289709).
Phase 03 was not started by this correction; the Phase 02 browser run created
no Phase 3 synthetic records.

Full evidence is maintained in [Phase 02 implementation evidence](../../champion_showcase/10_PHASE_02_IMPLEMENTATION_EVIDENCE.md).
