# PLAT-P3 — Module Control Release Record

Status: **IN DEVELOPMENT — local implementation and migration rehearsal passed; exact staging and protected production evidence pending**
Release identity: `PLAT-P3`
Record date: 2026-09-17
Operator: Codex, working with the delivery owner
Approver: Required GitHub `production` environment reviewer

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
| Backend suite | PASS | `python -m pytest backend/tests -q` — 42 passed |
| Phase 3 service/API tests | PASS | 4 passed: safe default, dependencies, disable safety, retry, reversal, authorization/isolation |
| Python compilation | PASS | `python -m compileall -q backend/app backend/tests scripts/release/production_phase3_smoke.py` |
| Frontend tests | PASS | `npm test` — 12 passed |
| Frontend typecheck | PASS | `npm run typecheck` |
| Frontend production build | PASS | `npm run build` — 34 routes, including company Modules route |
| Dependency audit | PASS | `npm audit --omit=optional --audit-level=low` — 0 vulnerabilities |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Migration upgrade/downgrade rehearsal | PASS | exact current revision `20260528_0007` upgraded to `20260917_0008`, downgraded, and upgraded again on disposable SQLite |
| Seed synchronization | PASS | Phase 3 test seeds twice; second module/catalog sync is zero-change |

## Staging and production evidence

To be filled only from matching artifacts and readback:

- Exact candidate SHA and ancestry:
- Staging deployment run and browser artifact:
- Catalog/search/filter/detail and public/internal identity evidence:
- Bundle preview/apply/retry/reversal and invalid-selection evidence:
- Authorization and tenant-isolation evidence:
- Database revision before/after:
- Protected production promotion/readback artifact:
- Read-only/operator-only/general rollout evidence:
- Synthetic cleanup zero counts:
- Production current/previous pointers and observation window:

## C03 and limitations

C03 is recorded at lifecycle state `defined` in `packages/C03.md`. The
`champion-drilling@1` bundle is a synthetic proposal. Champion role matrices,
chart of accounts, field mappings, final domain/branding, and acceptance/
verification decisions remain unresolved. The Phase 0 credential-rotation
waiver remains accepted; no Champion confidential data may enter the
environment under that waiver.

Final verdict: **PLAT-P3: BLOCKED** until exact-candidate staging, protected
production promotion, synthetic production reversal/cleanup, observation, and
matching artifacts are complete. This is a gate status, not a claim that the
local implementation is complete.
