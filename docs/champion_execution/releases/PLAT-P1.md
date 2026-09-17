# PLAT-P1 — Phase 1 UX Shell and Menu Release Record

Status: **REVIEW FAIL — remediation in progress; production gate not verified**
Release identity: `PLAT-P1`
Record date: 2026-09-17
Operator: Codex, working with the delivery owner
Approver: Required GitHub `production` environment reviewer; delivery owner acceptance recorded at the protected promotion gate
Production candidate: `c2b923a5550923749b4f4ade7599b4a96a8943f1`

## Scope and safety decision

Replace the authenticated SaaS App Shell presentation with a responsive LenERP
operator shell while preserving every existing URL and backend/database
behavior. This phase contains frontend navigation, shell state, runtime flag
consumption, route-state UI, and release smoke evidence only. No database
migration or business API change is included.

The existing shell remains available behind the same runtime flag. The flag is
server-controlled through `FEATURE_FLAGS=platform_phase1_shell=on|off` and is
read from `GET /runtime/release`. The earlier production fallback evidence is
not valid for this gate: run `35188091170` also materialized/promoted a
different candidate (`15268f8…`) and restarted production. Until the new
flag-only workflow proves off/on while the exact current release remains
unchanged, fallback is unverified.

## Acceptance scenarios and rollback triggers

Recorded before implementation:

1. An authenticated platform operator sees Work, Customers, Delivery, Product,
   and System groups with the required menu labels and route targets.
2. A non-admin authenticated user does not see platform-admin-only
   Implementations navigation and direct access presents Access denied; API
   authorization remains enforced by the existing backend dependencies.
3. `/app`, organization list/new/detail/tenant routes, tenant list/new/detail,
   implementation, modules, and settings work by direct navigation and refresh.
4. Nested organization and tenant routes show accurate active navigation and
   breadcrumbs; mobile drawer, compact sidebar, theme, keyboard escape, focus,
   session menu, and reduced-motion behavior remain usable.
5. Turning `platform_phase1_shell` off on the server restores the old shell
   without rebuilding or redeploying.
6. The temporary implementation hostname and the non-`lengrowth.com` staging
   host-header lane return the same route and flag behavior.

Rollback immediately if login/authenticated access is unavailable, any existing
critical route fails, repeated 5xx/health failures appear, authorization or
tenant isolation regresses, or the shell cannot be restored with the runtime
flag. Code rollback uses the existing immutable `current`/`previous` pointers;
shell fallback uses the server flag. Database/files recovery remains a
separate procedure and is not implied by this release.

## Implementation summary

- Added a typed grouped operator navigation model with permission metadata,
  server flag metadata, optional badge source, and Champion extension points.
- Added active nested-route matching, dynamic route titles, and stable
  breadcrumbs for organization and tenant detail paths.
- Added responsive desktop sidebar, collapsible groups, compact mode,
  persistent preferences, mobile drawer, skip link, page header, environment
  indicator, operational status, theme control, support link, and session menu.
- Added fail-closed runtime flag consumption requiring a complete release
  identity and retained the legacy shell as the immediate fallback.
- Added server-side platform-admin authorization before the implementation
  page renders, with a client loading state that does not render protected
  children while session resolution is pending.
- Added mobile drawer focus trapping, focus restoration, modal semantics, and
  inert background navigation.
- Added candidate-bound validation and durable staging browser/WCAG evidence
  workflows; production flag transitions now have a pointer-preserving,
  protected flag-only workflow.
- Added route-level loading, error, not-found, and access-denied surfaces.
- Added Vitest coverage for filtering, permissions, flags, active routes,
  titles, and breadcrumbs.
- Added `scripts/release/shell_smoke.sh` for authenticated route/flag checks;
  browser evidence remains responsible for hydrated shell and responsive UI
  assertions.

## Local validation

| Check | Result | Evidence |
|---|---|---|
| Frontend typecheck | PASS | `npm run typecheck` |
| Frontend production build | PASS | `npm run build`; 33 routes generated |
| Frontend/unit tests | PASS | `npm test`; 10 tests passed |
| Backend suite | PASS | `python -m pytest backend/tests -q`; 36 passed |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Authenticated route matrix | PARTIAL | Local direct-navigation evidence exists; candidate-bound staging browser artifact is required by the remediation workflow |
| Mobile drawer/breadcrumb evidence | PARTIAL | Component tests pass; durable desktop/mobile screenshots and axe results are pending the final-main staging run |
| Runtime flag fallback | FAIL / REOPENED | Prior production fallback run changed candidate and restarted services; same-candidate flag-only off/on evidence is required |

## Staging and production evidence

The earlier final-main staging run [35189053400](https://github.com/Lengrowth/crm/actions/runs/35189053400)
passed its then-current checks but emitted no durable artifact and did not run
the new candidate-bound browser/WCAG suite. The post-merge documentation run
[35189666162](https://github.com/Lengrowth/crm/actions/runs/35189666162) likewise
did not close that evidence gap. The production candidate remains `c2b923a…`
until a remediated candidate is tested and explicitly promoted.

Protected production evidence for the same release family:

| Action | Run | Artifact / result |
|---|---|---|
| Initial enablement on candidate `15268f8…` | [35186693396](https://github.com/Lengrowth/crm/actions/runs/35186693396) | [readback artifact 10483045169](https://github.com/Lengrowth/crm/actions/runs/35186693396/artifacts/10483045169); authenticated shell smoke passed, flag `true` |
| Claimed flag fallback (invalid for same-candidate gate) | [35188091170](https://github.com/Lengrowth/crm/actions/runs/35188091170) | [readback artifact 10483290012](https://github.com/Lengrowth/crm/actions/runs/35188091170/artifacts/10483290012); flag `false`, but candidate changed and production restarted |
| Final enablement on `c2b923a…` | [35189173434](https://github.com/Lengrowth/crm/actions/runs/35189173434) | [readback artifact 10483861183](https://github.com/Lengrowth/crm/actions/runs/35189173434/artifacts/10483861183); authenticated shell smoke passed, flag `true` |

The final readback recorded for the currently serving candidate:

- `current`: `/opt/saas-control/releases/c2b923a5550923749b4f4ade7599b4a96a8943f1`
- `previous`: `/opt/saas-control/releases/15268f8dad1187994f89256f5dc55a7e3c982586`
- backend, frontend, nginx, and R2 backup timer active; R2 timer enabled
- local production health HTTP `200`; clean Frappe/ERPNext source trees
- zero temporary smoke users, organizations, or active sessions

Post-release observation produced three consecutive samples with the public
root and canonical API at HTTP `200`, the runtime release fixed at the final
candidate with `platform_phase1_shell=true`, and the retired
`api.lenerp.lengrowth.com` unavailable. The final production promotion's shell
smoke covered 8 static authenticated operator routes; dynamic detail-route
coverage and durable browser evidence were not retained. Local browser evidence covered
the full dynamic route matrix, desktop/mobile shell states, keyboard Escape,
breadcrumbs, compact mode, theme, session menu, access denied, and the no-build
legacy-shell fallback. Automated component coverage now includes persistent
preferences, mobile drawer behavior, active links, skip-link/main focus
semantics, breadcrumbs, and keyboard close behavior (8 frontend tests total).

## Gate checklist

The generic checklist in `docs/champion_execution/PHASE_DEPLOYMENT_GATE.md`
applies. The production candidate is healthy, but the P1 gate is not closed:
server-side restricted-route authorization, candidate-bound CI/browser/WCAG
artifacts, runtime fail-closed behavior, mobile focus management, legacy
permission filtering, and same-candidate flag-only off/on evidence must all be
verified on the final candidate before this record can return to PASS.

## Accepted waivers and follow-up

The existing credential-rotation waiver from Phase 0 remains explicitly
accepted. No credentials were rotated or invalidated, no production Frappe or
ERPNext worktree was modified, and no database migration or business API change
was introduced. The GitHub Actions Node.js 20 deprecation annotation is an
upstream runner warning only. The inherited frontend dependency audit finding
(currently 8 vulnerabilities after adding the browser-test tooling, including a
critical advisory in the existing Next dependency chain) is tracked separately
and is not silently treated as a release pass; it requires dependency-owner
review before the final P1 gate is closed.
