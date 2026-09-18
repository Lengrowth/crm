# PLAT-P4 — Onboarding and Durable Provisioning Release Record

Status: **BLOCKED — local implementation and validation passed; staging execution and protected production promotion evidence are still required**
Release identity: `PLAT-P4`
Record date: 2026-09-18
Operator: Codex, working with the delivery owner
Implementation base: `2a697a831d04a41aaabb3e6f2413f53ce4e749c6` (`lengrowth/main`)
Candidate identity: **not yet immutable**; changes are currently uncommitted on `codex/plat-p4`

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
| Backend suite | PASS | `python -m pytest backend/tests -q` — 51 passed |
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

The repository now contains the guarded staging workflow input
`phase4_synthetic_state`, the non-secret evidence harness, and exact cleanup
logic. The actual staging deployment and synthetic smoke have not yet been run
from an immutable candidate in this execution. No protected production
promotion, production migration, production flag enablement, or production
Phase 4 execution has been performed.

The current production read-only baseline remains the Phase 3 candidate and its
Phase 3 flags. That is not Phase 4 evidence. Do not promote or enable Phase 4
until the candidate is committed, candidate validation and secret scan pass,
the isolated staging smoke artifact reports `passed` with cleanup complete, and
the protected production workflow records backup verification, additive
migration success, Phase 4 flags off, smoke/readback success, observation, and
cleanup.

Read-only observation on 2026-09-18: SaaS root `200`, canonical API
`/health` `200` with database `ready` and live ERP policy, ERP root `200`, and
`/runtime/release` `200` reporting the Phase 3 candidate
`86fcde5b822b06e40980f904d81b87854903dfc6`. The runtime exposes only the
previous Phase 1/3 flags; no Phase 4 flag is enabled.

## Open gate

The remaining gate is operational rather than an unverified code claim:

1. commit/materialize the candidate without modifying
   `frontend/tsconfig.tsbuildinfo`;
2. run the protected staging workflow with
   `phase4_synthetic_state=on` and retain the non-secret artifact;
3. review the artifact and migration/rollback evidence;
4. use the separately approved production promotion workflow with all Phase 4
   flags off; and
5. observe production and reconcile the final handover/risk records.

Final verdict: **PLAT-P4: BLOCKED**. Local implementation and validation are
complete, but the required immutable-candidate staging execution and protected
production evidence are not present, so a Phase 4 production PASS would be
unsupported.
