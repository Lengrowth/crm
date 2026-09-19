# PLAT-P4 — Onboarding and Durable Provisioning Release Record

Status: **PASS — corrected candidate-bound Phase 4 evidence completed before a newly protected production promotion**
Release identity: `PLAT-P4`
Record date: 2026-09-18
Operator: Codex, working with the delivery owner
Implementation commit: `9432a354f0e0ac960c50751369c4bff6754e37c4`
Original release candidate (reconciled, not credited): `2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`
Original main merge containing the implementation: `c5f3989b77dfb21c01bbc94c458a2a0c04de20b3`
Gate enforcement commits: `9f39f9c754b2c954c82315e49e8c6410133b44aa`, `560f4e1c2d4253dfa69472c54d85a4ee936c85ab`
Corrected exact tested and promoted release candidate: `27ede631c667c67f45d534108abeb975816ee83e`

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
| Phase 4 evidence gate tests | PASS | `scripts/release/test_verify_phase4_evidence.py` — candidate binding, success/recovery cleanup, and pre-promotion chronology |

## Staging and production evidence

### Reconciliation and corrected sequence

The previous promotion was correctly rejected as a Phase 4 gate result:
promotion run `35370954773` started at `16:51:40Z` and completed at
`16:54:33Z`, while its cited synthetic run `35371519119` started at
`16:57:38Z`; the old materializer also bypassed evidence verification for an
already-materialized candidate.

The remediation is now enforced in every path. The materializer verifies a
candidate-bound artifact before either reusing an existing production
candidate or building/copying one. The artifact must contain successful
success and recovery payloads, exact candidate metadata, full cleanup
readback, and a staging run that both started and completed before the
promotion request. The final promotion script also requires the materializer's
candidate-bound evidence marker.

The corrected sequence is:

- Gate enforcement merged in `9f39f9c…` and redirect-safe artifact download
  merged in `560f4e1…`; final main candidate is `27ede631…`.
- [Final exact-candidate staging run 35379590876](https://github.com/Lengrowth/crm/actions/runs/35379590876) ran from `18:20:19Z` through `18:29:05Z` for candidate `27ede631c667c67f45d534108abeb975816ee83e` with `phase4_synthetic_state=on`.
- Its [candidate-bound Phase 4 artifact `10561738710`](https://github.com/Lengrowth/crm/actions/runs/35379590876/artifacts/10561738710) contains metadata binding the candidate SHA and staging run ID, plus success and injected-recovery evidence. Both report `status=passed`, `state=ready`, `worker_status=success`, 15 steps, isolated Frappe readback, and verified cleanup; recovery intentionally failed at `health_checks` and recovered.
- The protected promotion request [35380532779](https://github.com/Lengrowth/crm/actions/runs/35380532779) was created at `18:30:03Z`, after the evidence run completed, and finished successfully at `18:31:55Z`. The materialization step passed the live verifier; an independent post-run verifier also resolved `35379590876` for this promotion run.
- The [production readback artifact `10561369795`](https://github.com/Lengrowth/crm/actions/runs/35380532779/artifacts/10561369795) reports current release `27ede631c667c67f45d534108abeb975816ee83e`, previous release `2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`, production environment, database revision `20260918_0011` before and after, local health `200`, active backend/frontend/nginx/R2 timer services, all Phase 4 flags off, and zero production ERP Phase 4 sites. All reported Phase 4 cleanup counts are zero; the domain count is unavailable (`null`) in this readback, not a surviving resource.
- Production Phase 4 execution was not enabled; all Phase 4 testing remained isolated synthetic staging activity.

### Readback hardening follow-up

The earlier production readback's `domains: null` was an observability defect:
the readback query used `domain_mappings`, while the deployed
`DomainMapping` model uses the `domains` table. The fix was merged in [PR
70](https://github.com/Lengrowth/crm/pull/70) as `bc7e2be…` and promoted in
the new immutable candidate `4a63264e1e8cb7c998c767262a6e1022647ff7b0`.

- [Candidate-bound Phase 4 staging run 35386558041](https://github.com/Lengrowth/crm/actions/runs/35386558041) passed success and recovery evidence for the exact candidate.
- [Protected follow-up promotion 35387316160](https://github.com/Lengrowth/crm/actions/runs/35387316160) completed successfully after the evidence run.
- [Production readback artifact 10564711145](https://github.com/Lengrowth/crm/actions/runs/35387316160/artifacts/10564711145) reports `domains: 0`, `all_remaining_counts_zero: true`, release `4a63264e1e8cb7c998c767262a6e1022647ff7b0`, environment `production`, health `200`, and every Phase 4 flag disabled.

The read-only AWS audit found no temporary `TempSSMSendCommandPolicy`,
`TempSSMSendCommandGroup`, or temporary security-group rule. The intended
`LenGrowthStagingSSMRole` instance profile remains attached to the staging
instance. An existing baseline SSH ingress rule for `188.169.243.84/32` also
remains; it was not changed because its ownership and operational purpose were
not established, and removing it could break administrator access.

## Closed gate and handover

The corrected immutable-candidate staging run, recovery run, evidence review,
protected production promotion, read-only observation, and cleanup are
complete. The
working-tree-only `frontend/tsconfig.tsbuildinfo` change was preserved and was
not staged, reset, or overwritten. Rollback remains available through the
immutable `current`/`previous` release pointers, with the prior production
release retained as `2cfc9aa71c13a09e41ef42c7484d5aafbe5e51b9`.

Final verdict: **PLAT-P4 REVIEW: PASS**.
