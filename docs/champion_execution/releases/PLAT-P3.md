# PLAT-P3 — Module Control Release Record

Status: **PASS — exact candidate staged, protected production promotion completed, staged rollout verified, production observed, and synthetic cleanup verified**
Release identity: `PLAT-P3`
Record date: 2026-09-18
Operator: Codex, working with the delivery owner
Approver: GitHub `production` environment reviewer; approvals recorded on protected runs
Production candidate: `86fcde5b822b06e40980f904d81b87854903dfc6`
Previous production candidate: `68926c22aab01079f17c2cebe21edeeff8ca2c75`

## Scope and safety decision

Phase 3 replaces the static admin Modules page and placeholder entitlement
service with a persisted authoritative catalog, versioned bundle proposals,
deterministic entitlement resolution, transactional idempotent writes, scoped
authorization, append-only module audit history, and separate trusted ERP
application/verification state. The rollout is additive and uses synthetic
data only. It does not customize or migrate a production ERP site.

`inventory` remains a valid legacy key and is explicitly aliased to canonical
`stock`; no saved assignment is deleted. The safe existing-organization default
is empty unless an active plan or implementation template supplies modules.

## Acceptance scenarios and rollback triggers

1. Catalog and public catalog resolve the same stable identities, including the
   promised ERP modules and preserved legacy codes.
2. A platform operator previews and applies a versioned bundle; dependencies,
   sources, audit before/after state, retry replay, and reversal are visible.
3. Missing, inactive, cyclic, incompatible, or dependent-disable selections
   fail before any assignment or audit row is committed.
4. Anonymous, ordinary-member, and cross-company reads/mutations are denied
   according to the policy below; authorized organization roles are narrow and
   feature-flagged.
5. Entitled modules remain pending until trusted ERP integration evidence marks
   application and verification separately.
6. Existing Phase 1/2 routes, CRUD, bounded reads, shell fallback, and tenant
   isolation remain intact.

Rollback immediately for authorization/isolation regression, partial writes,
incorrect dependency resolution, duplicate retries, catalog mismatch, a module
reported verified without trusted evidence, migration failure, repeated 5xx,
broken existing routes, or inability to disable writes. Code rollback uses the
immutable `current`/`previous` production pointers. Entitlement reversal/data
correction is separate and uses the exact module audit snapshot or database
restore procedure.

## Implementation and data model

- `modules` is the authoritative catalog with stable code, public/internal
  descriptions, active/marketed/administrative visibility, ordering,
  dependencies, incompatibilities, app/version metadata, roles/workspaces,
  non-secret configuration schema, and alias/deprecation metadata.
- `plans.default_modules_json`, existing implementation-template defaults, and
  organization overrides feed the resolver.
- `module_bundles` and `module_bundle_items` store versioned proposals. Bundles
  do not prove ERP application and do not mutate future companies.
- `organization_modules` retains legacy `status` and adds explicit/requested/
  entitled state, source, reason, and idempotency reference.
- `module_entitlement_requests` makes applies replay-safe per organization and
  idempotency key.
- `module_entitlement_audits` stores append-only actor, organization,
  operation, requested/effective before/after state, source/bundle, reason,
  idempotency key, timestamp, and result.
- `module_application_statuses` is tenant-scoped trusted integration state;
  browser entitlement actions cannot write it.

Precedence is deterministic: safe empty base → active plan defaults → latest
implementation-template defaults → requested bundle → explicit organization
overrides, with explicit disables winning over inherited sources and dependency
closure applied last. The resolver detects cycles, missing/inactive dependencies,
incompatibilities, and dependent disables, and emits source explanations in
display-order-stable results.

## Authorization and rollout

Catalog public fields are available through `/public/modules`. Internal catalog
metadata requires authentication. Effective entitlements and audit history are
organization-scoped. Platform admins may operate across organizations; ordinary
members may read only organizations where they belong. Preview/apply mutation
policy is limited to platform admins or organization roles `owner`, `admin`, or
`implementation_manager`, with backend dependency enforcement. Apply writes are
fail-closed until `module_entitlement_writes` is on; operator-only rollout
requires platform admin and general rollout additionally requires
`module_entitlement_general`.

Production sequence: promote with writes off; verify read paths; enable
operator-only through `toggle_module_entitlement_rollout.sh`; run the uniquely
named synthetic operator/member/second-company scenario; reverse and clean it;
then enable general authorized-role rollout only after evidence review. A
normal browser action has no ERP verification control.

## Local and migration validation

| Check | Result | Evidence |
|---|---|---|
| Backend suite | PASS | `python -m pytest backend/tests -q` — 48 passed |
| Phase 3 service/API tests | PASS | 10 focused tests: catalog/seed immutability, safe default, status-derived legacy state, dependencies, explicit-disable conflict, stale preview, retry, reversal, authorization/isolation, rules, and bundle audit |
| Python compilation | PASS | `python -m compileall -q backend/app backend/tests scripts/release/production_phase3_smoke.py` |
| Frontend tests | PASS | `npm test` — 12 passed |
| Frontend typecheck | PASS | `npm run typecheck` |
| Frontend production build | PASS | `npm run build` — 34 routes, including company Modules route |
| Dependency audit | PASS | `npm audit --omit=optional --audit-level=low` — 0 vulnerabilities |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Migration upgrade/downgrade rehearsal | PASS | exact current revision `20260528_0007` upgraded through `20260918_0009`, downgraded, and upgraded again on disposable SQLite; enabled and disabled legacy assignments preserve state |
| Seed synchronization | PASS | Released catalog and bundle versions are insert-only; operator-owned metadata and bundle membership are not overwritten; second sync is zero-change |

## Staging and production evidence

- Exact candidate and ancestry: `86fcde5b822b06e40980f904d81b87854903dfc6`; it is
  the protected merge of remediation PR [#54](https://github.com/Lengrowth/crm/pull/54)
  on top of the earlier Phase 3 implementation/tooling PRs [#49](https://github.com/Lengrowth/crm/pull/49),
  [#50](https://github.com/Lengrowth/crm/pull/50), and documentation PRs
  [#51](https://github.com/Lengrowth/crm/pull/51), [#52](https://github.com/Lengrowth/crm/pull/52),
  [#53](https://github.com/Lengrowth/crm/pull/53). The verified baseline
  `7cd9c2d2cc3e5a4507e380f8b122983a3ad76d9d` is an ancestor.
- Candidate-bound staging for production candidate `86fcde5b822b06e40980f904d81b87854903dfc6`:
  run [35278665942](https://github.com/Lengrowth/crm/actions/runs/35278665942),
  browser artifact
  [10521149490](https://github.com/Lengrowth/crm/actions/runs/35278665942/artifacts/10521149490).
  Runtime identity matched the candidate. The Phase 3 artifact records backend
  catalog loading, public/internal identity agreement, module search/detail,
  bundle preview/apply/retry, invalid and dependent-disable rejection, company
  Modules view, audit before/after, reversal, non-admin denial, and cleanup
  manifest; accessibility reported zero violations.
- Final remote-main staging for the documentation-bearing sign-off content:
  run [35281045275](https://github.com/Lengrowth/crm/actions/runs/35281045275),
  browser artifact
  [10522837696](https://github.com/Lengrowth/crm/actions/runs/35281045275/artifacts/10522837696).
  The run head is `6bb59b2ab1349351ee8e9fc80a06f454a8f8b772`, the final remote
  `main` at sign-off. Its staging artifact reports
  `platform_phase1_shell=false` because staging workflow flags are isolated;
  protected production readback [35279102175](https://github.com/Lengrowth/crm/actions/runs/35279102175)
  / artifact [10522240159](https://github.com/Lengrowth/crm/actions/runs/35279102175/artifacts/10522240159)
  and live production observations independently verify
  `platform_phase1_shell=true` for the production candidate.
- Database migration: staging rehearsal upgraded representative legacy schema
  `20260528_0007` through `20260918_0009`, downgraded, and upgraded again while
  preserving a legacy `inventory` assignment. The protected production
  promotion run applied `20260917_0008 -> 20260918_0009`; catalog seed then
  completed with zero existing catalog/bundle mutations.
- Protected production promotion: run
  [35279102175](https://github.com/Lengrowth/crm/actions/runs/35279102175),
  readback artifact
  [10522240159](https://github.com/Lengrowth/crm/actions/runs/35279102175/artifacts/10522240159).
  It reports current `/opt/saas-control/releases/86fcde5b...`, previous
  `/opt/saas-control/releases/68926c22...`, active backend/frontend/nginx/R2
  timer services, local health `200`, `platform_phase1_shell=true`, clean upstream trees, and zero Phase 0
  smoke records.
- Rollout evidence: protected read-only run
  [35279338775](https://github.com/Lengrowth/crm/actions/runs/35279338775) was
  followed by operator-only run
  [35279271616](https://github.com/Lengrowth/crm/actions/runs/35279271616)
  passed with artifact
  [10522300063](https://github.com/Lengrowth/crm/actions/runs/35279271616/artifacts/10522300063);
  general rollout run
  [35279384713](https://github.com/Lengrowth/crm/actions/runs/35279384713)
  passed and restored the final authorized-role state.
- Production synthetic verification: artifact
  [10522300063](https://github.com/Lengrowth/crm/actions/runs/35279271616/artifacts/10522300063)
  reports catalog counts `21/17`, preview/apply/retry/reversal success,
  authorization isolation, no untrusted verification, and zero remaining
  organizations, users, memberships, tenants, sessions, assignments,
  entitlement requests, audits, application statuses, or token files.
- Observation: final live samples returned health `200`, exact candidate
  release `86fcde5b...`, `platform_phase1_shell=true`, and stable final flags
  `module_entitlement_writes=true`, `module_entitlement_operator_only=false`,
  `module_entitlement_general=true`.
- Cleanup: the protected production artifact and staging workflow both report
  complete synthetic cleanup; legitimate catalog/reference data was preserved.

## C03 and limitations

C03 is recorded at lifecycle state `defined` in `packages/C03.md`. The
`champion-drilling@1` bundle is a synthetic proposal. Champion role matrices,
chart of accounts, field mappings, final domain/branding, and acceptance/
verification decisions remain unresolved. The Phase 0 credential-rotation
waiver remains accepted; no Champion confidential data may enter the
environment under that waiver.

Final verdict: **PLAT-P3: PASS**. Exact-final-main staging, migration rehearsal,
protected production promotion, read-only/operator-only/general rollout,
synthetic production preview/apply/retry/reversal, authorization and
tenant-isolation checks, ERP-state separation, cleanup, observation, and
documentation reconciliation are complete. C03 remains `defined` because
Champion-specific role/module decisions and ERP verification are unresolved;
that is an explicit package boundary, not a Phase 3 gate failure.
