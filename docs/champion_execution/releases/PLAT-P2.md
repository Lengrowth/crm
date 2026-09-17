# PLAT-P2 — Core Pages and Design System Release Record

Status: **PASS — exact candidate staged, protected promotion completed, production observed, and synthetic CRUD/isolation cleanup verified**
Release identity: `PLAT-P2`
Record date: 2026-09-17
Operator: Codex, working with the delivery owner
Approver: Required GitHub `production` environment reviewer
Current production candidate: `41ac76500a6a502ac78f22d6dbefbf90996ee46a`
Previous production candidate: `f1d54e9af4fe620d4c565038f64f989c37e36d6f`

## Scope and safety decision

Phase 2 supplies a focused reusable operator design system and replaces
placeholder-heavy authenticated pages with real, protected control-plane data.
It does not implement module entitlement controls, redesign provisioning,
receive Champion data, change final-domain routing, modify Frappe/ERPNext, or
introduce a database migration. The existing Phase 1 shell and its global
server-controlled fallback remain intact.

The release adds two backward-compatible protected read models:

- `GET /dashboard/summary` — bounded company, ERP-site, provisioning,
  implementation-attention, and domain-warning data scoped to the authenticated
  operator.
- `GET /implementation/portfolio` — bounded platform-admin portfolio data with
  project/task progress and company/site labels.

No secret, credential, provider response, or Champion data is returned by these
read models.

## Acceptance scenarios and rollback triggers

Recorded for candidate validation:

1. Authenticated operators can understand current company/site/provisioning and
   delivery state from `/app`, with data from protected APIs and safe partial,
   empty, loading, permission, and error states.
2. Company and ERP-site list/detail/create/update flows preserve existing URLs,
   identifiers, authorization, validation behavior, and tenant boundaries.
3. Site suspension/reactivation, domain activation, and provisioning actions
   require explicit confirmation and do not display credentials or raw provider
   errors.
4. Platform administrators see the real implementation portfolio; non-admins
   remain denied at both navigation and direct route access.
5. Shared primitives and tokens work in light/dark themes, desktop/mobile
   layouts, keyboard navigation, reduced motion, and axe checks.
6. Candidate-bound browser evidence creates two synthetic companies and sites,
   exercises UI validation/create/update flows, verifies both reads for the
   admin, verifies second-company read and mutation denial for the non-admin,
   and removes exact identifiers afterward.

Rollback immediately if login/authenticated access, existing deep links,
authorization/tenant isolation, the dashboard critical path, company/site CRUD,
health checks, or background jobs regress. Code rollback uses immutable
`current`/`previous` pointers. The Phase 1 shell flag remains the fallback for
the legacy shell; database/data recovery is separate and no migration is part
of this release.

## Implementation summary

- Added the small Radix/Lucide primitive set required by Phase 2: Button, Card,
  Badge, Input, Select, Dialog, Sheet, Dropdown, Table, Tabs, Tooltip, Alert,
  Skeleton, EmptyState, ErrorState, PageHeader, Breadcrumb, and ConfirmAction.
- Consolidated operator tokens for surfaces, text, borders, focus, semantic
  states, radius, shadows, and reduced motion across light and dark themes.
- Rebuilt `/app`, company routes, ERP-site routes, implementation, and settings
  with typed data, safe errors, search/filter controls, confirmations, and
  operator-oriented copy.
- Added bounded dashboard and implementation portfolio API read models with
  authorization, tenant-scoped queries, independent totals, and explicit
  detail truncation indicators.
- Extended candidate browser evidence with empty/partial dashboard states,
  theme/focus checks, UI validation/create/update CRUD, mutation-denial and
  isolation evidence, and exact-ID cleanup.

## Local validation

| Check | Result | Evidence |
|---|---|---|
| Frontend dependency install | PASS | `npm install` completed; lockfile updated |
| Frontend dependency audit | PASS | `npm audit --omit=optional --audit-level=low` — 0 vulnerabilities |
| Frontend unit/component tests | PASS | `npm test` — 12 tests passed |
| Frontend typecheck | PASS | `npm run typecheck` |
| Frontend production build | PASS | `npm run build` — 34 routes generated |
| Backend suite | PASS | `python -m pytest backend/tests -q` — 38 passed |
| Python compilation | PASS | `python -m compileall -q backend/app backend/tests` |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Local smoke | PASS | `python scripts/release/local_smoke.py` with explicit `LOCAL_SMOKE_PYTHON` and `LOCAL_SMOKE_ALEMBIC_AS_MODULE=true`; disposable platform-admin fixture exercised the admin-only portfolio route and synthetic DB/services were cleaned up |

## Staging validation

PASS. Remediation PR #47 validated the corrected implementation in run
[35257247863](https://github.com/Lengrowth/crm/actions/runs/35257247863),
with browser artifact
[10512978308](https://github.com/Lengrowth/crm/actions/runs/35257247863/artifacts/10512978308).
The exact post-merge main candidate is
`41ac76500a6a502ac78f22d6dbefbf90996ee46a`; its final staging validation
passed in run [35257785806](https://github.com/Lengrowth/crm/actions/runs/35257785806)
with browser artifact
[10513394070](https://github.com/Lengrowth/crm/actions/runs/35257785806/artifacts/10513394070).
The candidate-bound artifacts record UI company/site create and update,
validation failures, non-admin read and cross-company mutation denial, all
required routes/states/themes/responsive widths, zero serious/critical axe
violations, and the reviewed contrast-only incomplete checks. The corrected
dashboard reports independent warning totals with truncation indicators, and
the portfolio uses bounded aggregate/detail queries with project/task
truncation signals. Exact synthetic records were removed after capture.

## Production promotion and observation

PASS. Protected workflow run
[35258252240](https://github.com/Lengrowth/crm/actions/runs/35258252240)
approved and promoted exact candidate `41ac765…` with verified backups and
`platform_phase1_shell=true`. Its production readback artifact is
[10513034032](https://github.com/Lengrowth/crm/actions/runs/35258252240/artifacts/10513034032).
The authorized production Phase 2 smoke passed organization and tenant
create/read/update, non-admin cross-company read and mutation denial, and
cleanup. Readback reported current `41ac765…`, previous `f1d54e9…`, local
health `200`, active backend/frontend/nginx/R2 timer services, R2
query/lifecycle success, clean upstream source trees, and zero Phase 0 smoke
users, organizations, or active sessions. The Phase 2 cleanup manifest was
available in readback, status `passed`, and zero for organizations, tenants,
users, sessions, tokens, memberships, audit logs, provisioning jobs, domain
mappings, implementation projects/tasks, tenant provisioning records, and
ERPNext integration metadata. Runtime release identity matched `41ac765…`
and the Phase 1 shell remained enabled.

The initial rerun stopped before mutation when staging retention had pruned the
candidate directory; the subsequent exact re-stage passed. A later smoke
diagnostic isolated an API-edge rejection of Python's default user agent; the
protected tooling was corrected to use an explicit service user agent, then
revalidated in staging and production. Both failed attempts ran cleanup and
readback paths; no Champion data, upstream worktree, DNS, or credential state
was changed.

## Accepted waivers and limitations

- The Phase 0 credential-rotation waiver remains accepted. No Champion data may
  enter the environment under that waiver.
- The runtime manifest may continue to report `environment: staging` because
  candidates are built in staging and promoted unchanged; production readback
  is authoritative for serving state.
- Local smoke uses an explicit valid Python/Alembic module command because this
  workstation has no repository-local `backend/.venv`; the tooling now records
  that environment explicitly rather than silently claiming the default path.

## Gate checklist

The generic checklist in `docs/champion_execution/PHASE_DEPLOYMENT_GATE.md`
applies. Final verdict: **PLAT-P2: PASS**. Exact-candidate staging, browser,
protected promotion, production readback, observation, cleanup, and documentation
reconciliation are complete. Rollback target remains `f1d54e9…`; the prior
Phase 1 candidate `851302ef…` and older `12bc548…` remain available through
the protected release pointers.
