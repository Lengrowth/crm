# PLAT-P4 — Onboarding and Durable Provisioning Release Record

Status: **PASS — exact-candidate staging evidence and protected production promotion completed**
Release identity: `PLAT-P4`
Record date: 2026-09-18
Operator: Codex, working with the delivery owner
Implementation commit: `9432a354f0e0ac960c50751369c4bff6754e37c4`
Exact tested and promoted release candidate: `2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`
Main merge containing the implementation: `c5f3989b77dfb21c01bbc94c458a2a0c04de20b3`

## Scope and safety decision

Phase 4 adds a public onboarding request lifecycle and an operator-controlled,
durable provisioning workflow. The public path stores a versioned, bounded
request snapshot and a hash-only management credential. It does not create an
organization, tenant, entitlement, invoice, subscription, ERP site, DNS
record, password, or external provider object.

Only an exact approved request version can be converted. Conversion creates the
control-plane organization, invited administrator, staging tenant,
implementation project, approved entitlement records, a persisted 15-step job,
an outbox record, and a disabled first-login handoff. Execution requires a
separate platform-operator authorization and is limited to the isolated
synthetic target. Billing and real provider execution are not part of this
phase.

No Champion data, credentials, production ERP edits, DNS mutations, real
billing, or real customer provisioning were used in the local validation.

## Acceptance scenarios and rollback triggers

1. Public onboarding accepts only bounded safe fields, rejects unknown fields,
   supports idempotent replay, rejects conflicting idempotency payloads, and
   exposes only safe applicant status.
2. Applicant revisions create a new immutable request version and invalidate
   stale approvals. Submit validates the exact module/bundle selection before
   entering review.
3. Platform operators must review and approve the exact version and bundle;
   conversion is atomic and creates no billing or provider side effect.
4. Generic direct provisioning endpoints are disabled. The operator queue is
   feature-flagged and platform-admin protected.
5. Execution requires the approved version, an explicit confirmation,
   `onboarding_synthetic_allowlist=on`, `onboarding_real_execution=off`, and
   `desired_infrastructure=isolated_synthetic`.
6. The worker claims jobs with a compare-and-set lease, persists every stable
   step, heartbeats/renews leases, retries with bounded backoff, records safe
   events, and never marks a failed or incomplete job ready.
7. Site/domain steps are explicit and reversible at the control-plane level;
   DNS and SSL remain manual/deferred in the synthetic lane. First-login
   delivery remains disabled and only a hash/ref is stored.
8. Exact-record cleanup removes synthetic request, organization, tenant,
   project, steps, events, outbox, handoff, module records, membership, and
   synthetic administrator records without touching catalog/reference data.

Rollback immediately for an authorization or tenant-isolation regression,
unknown payload persistence, raw secret/provider response in logs, duplicate
conversion, stale-version execution, an unapproved external side effect,
incorrect module resolution, lease/CAS contention failure, false readiness,
migration failure, repeated 5xx, or inability to return all Phase 4 flags to
off. Code rollback uses the immutable `current`/`previous` release pointers.
Database/files recovery is a separately approved restore procedure; code
rollback does not imply data rollback.

## Data model and workflow contract

Migration `20260918_0010_phase4_onboarding_and_durable_provisioning` adds:

- `onboarding_requests`, `onboarding_request_versions`,
  `onboarding_management_credentials`, and `onboarding_decisions`;
- `provisioning_steps`, `provisioning_events`, `provisioning_outbox_events`,
  and `first_login_handoffs`;
- lease, retry, cancellation, workflow-version, external-reference, target
  environment, and isolation metadata on `provisioning_jobs`.

Workflow version: `phase4-1`.

Stable step keys, in order:

1. `validate_approved_request`
2. `reserve_site_name`
3. `create_isolated_site`
4. `install_pinned_erpnext`
5. `install_lenerp_custom_app`
6. `apply_approved_modules`
7. `apply_roles_workspaces`
8. `apply_branding_configuration`
9. `prepare_domain_binding`
10. `bind_domain_ssl`
11. `create_admin_handoff`
12. `health_checks`
13. `verify_apps_modules`
14. `prepare_first_login`
15. `mark_ready`

Runtime flags are fail-closed by default:

`onboarding_public_intake`, `onboarding_operator_view`,
`onboarding_conversion`, `onboarding_execution`, and
`onboarding_synthetic_allowlist` default off. `onboarding_real_execution` is
always off for this phase. Staging workflow dispatch can explicitly enable the
synthetic set and runs `scripts/release/phase4_synthetic_smoke.py`; production
promotion explicitly writes every Phase 4 flag to off.

## Local validation evidence

| Check | Result | Evidence |
|---|---|---|
| Backend suite | PASS | `python -m pytest backend/tests -q` — 56 passed, 21 warnings |
| Phase 4 workflow/recovery tests | PASS | public idempotency/conflict/revision, 15-step synthetic success, CAS contention, secret-safe logs, injected failure, retry, and recovery |
| Migration rehearsal | PASS | `backend/tests/test_phase3_migration_rehearsal.py` upgrades/downgrades through `20260918_0010` on disposable SQLite |
| Python compilation | PASS | `python -m compileall -q backend/app backend/tests` |
| Frontend tests | PASS | `npm test` — 12 passed |
| Frontend typecheck | PASS | `npm run typecheck` |
| Frontend production build | PASS | `npm run build` — 36 routes, including public and operator onboarding/job recovery routes |
| Diff whitespace | PASS | `git diff --check` |
| Direct provisioning regression | PASS | legacy API test now asserts `403` and the approved onboarding guidance |
| Secret scan | PASS | `python scripts/release/secret_scan.py` — no high-confidence credential patterns |

## Staging and production evidence

The guarded workflow was run against the exact promoted release candidate with
`phase4_synthetic_state=on` in staging:

- [Exact-candidate staging run 35371519119](https://github.com/Lengrowth/crm/actions/runs/35371519119) completed successfully for release `2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`.
- Synthetic success and injected-recovery evidence were uploaded as artifact
  `10558804260` (`phase4-synthetic-evidence-35371519119`). Both records report
  `status=passed`, `state=ready`, `worker_status=success`, and 15 persisted
  steps. The real Frappe provider readback confirms the isolated bench,
  database, files, queues, installed `frappe`/`erpnext`/`lenerp_core` apps, and
  the approved `crm`/`projects`/`field_ops` module set.
- Recovery intentionally failed at `health_checks`, recovered through the
  durable retry path, and reached `ready`. Each run deleted one isolated ERP
  site and removed the exact synthetic records: 1 request, 1 version, 1
  management credential, 3 decisions, 1 organization, 1 membership, 1 tenant,
  1 project, 5 tasks, 1 domain, 3 organization modules, 1 entitlement audit,
  3 module application statuses, 1 job, 15 steps, 15 events, 1 outbox event,
  1 first-login handoff, and 1 synthetic administrator.
- Browser/accessibility evidence was uploaded as artifact `10558549671`
  (`staging-browser-evidence-2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`).

The separately approved protected production promotion was then completed:

- [Protected production run 35370954773](https://github.com/Lengrowth/crm/actions/runs/35370954773) promoted the exact tested candidate with verified application/off-host backups, additive Phase 3 migration/catalog sync successful, Phase 4 flags explicitly off, authorized Phase 2 CRUD/tenant-isolation smoke successful, disposable identity removed, and non-secret readback artifact `10558687851` uploaded.
- Production readback reports `current_release=/opt/saas-control/releases/2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`, `previous_release=/opt/saas-control/releases/82e7b4e3600aedf37d24dbb9273a3dba408a0746`, database revision `20260918_0011` before and after, backend/frontend/nginx and the R2 backup timer active, R2 lifecycle rules enabled, and zero Phase 2/smoke resources remaining. Phase 4 production counts are zero for requests, versions, decisions, organizations, tenants, jobs, steps, events, outbox events, handoffs, credentials, memberships, projects, tasks, module state, and leases; the domain count is unavailable in this readback (`null`), not a surviving resource.
- Read-only observation on 2026-09-18: local health HTTP `200`, `/runtime/release` reports commit `2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9` with `environment=production` and staging build metadata, and the production ERP Phase 4 site count is `0`. Runtime flags show `platform_phase1_shell=true`, all Phase 3 entitlement-write flags false, and `onboarding_public_intake=false`, `onboarding_operator_view=false`, `onboarding_conversion=false`, `onboarding_execution=false`, `onboarding_synthetic_allowlist=false`, and `onboarding_real_execution=false`.
- Production Phase 4 execution was not enabled; all Phase 4 testing remained isolated synthetic staging activity.

## Closed gate and handover

The immutable-candidate staging run, recovery run, evidence review, protected
production promotion, read-only observation, and cleanup are complete. The
working-tree-only `frontend/tsconfig.tsbuildinfo` change was preserved and was
not staged, reset, or overwritten. Rollback remains available through the
immutable `current`/`previous` release pointers, with the prior production
release retained as `82e7b4e3600aedf37d24dbb9273a3dba408a0746`.

Final verdict: **PLAT-P4: PASS**.
