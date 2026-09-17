# PLAT-P2 — Core Pages and Design System Release Record

Status: **IN PROGRESS — local validation passed; staging and production evidence pending**
Release identity: `PLAT-P2`
Record date: 2026-09-17
Operator: Codex, working with the delivery owner
Approver: Required GitHub `production` environment reviewer
Previous known-good production candidate: `851302efc617f8a6587b30694a5c65a3e06de20a`
Previous rollback candidate: `12bc548056c59341d3ccc492a5353a696a7c0661`

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
   updates one company, verifies both reads for the admin, verifies second-
   company denial for the non-admin, and removes exact identifiers afterward.

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
  authorization and tenant-scoped queries.
- Extended candidate browser evidence with empty/partial dashboard states,
  theme/focus checks, CRUD/isolation evidence, and exact-ID cleanup.

## Local validation

| Check | Result | Evidence |
|---|---|---|
| Frontend dependency install | PASS | `npm install` completed; lockfile updated |
| Frontend dependency audit | PASS | `npm audit --omit=optional --audit-level=low` — 0 vulnerabilities |
| Frontend unit/component tests | PASS | `npm test` — 12 tests passed |
| Frontend typecheck | PASS | `npm run typecheck` |
| Frontend production build | PASS | `npm run build` — 34 routes generated |
| Backend suite | PASS | `python -m pytest backend/tests -q` — 36 existing tests plus Phase 2 read-model coverage |
| Python compilation | PASS | `python -m compileall -q backend/app backend/tests` |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Local smoke | PASS | `python scripts/release/local_smoke.py` with explicit `LOCAL_SMOKE_PYTHON` and `LOCAL_SMOKE_ALEMBIC_AS_MODULE=true`; synthetic DB/services cleaned up |

## Staging validation

Pending exact candidate. The required workflow must run the candidate-bound
validation, Phase 1 shell smoke, authenticated route matrix, CRUD/isolation
browser artifact, WCAG checks, and exact synthetic cleanup before promotion.

## Production promotion and observation

Pending. Promotion must use the protected `production` environment with exact
staging-tested candidate `release_id`, verified backups, and final shell flag
`platform_phase1_shell=true`. No production Frappe/ERPNext worktree, DNS, or
credential rotation is in scope.

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
applies. The final PASS verdict will be written only after exact-candidate
staging, browser, protected promotion, production readback, observation,
cleanup, and documentation reconciliation are complete.
