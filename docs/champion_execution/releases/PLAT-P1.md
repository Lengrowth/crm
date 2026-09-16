# PLAT-P1 — Phase 1 UX Shell and Menu Release Record

Status: **IN PROGRESS — implementation and local validation complete; staging and protected production gate pending**
Release identity: `PLAT-P1`
Record date: 2026-09-16
Operator: Codex, working with the delivery owner
Approver: Required GitHub `production` environment reviewer; delivery owner acceptance recorded at the protected promotion gate

## Scope and safety decision

Replace the authenticated SaaS App Shell presentation with a responsive LenERP
operator shell while preserving every existing URL and backend/database
behavior. This phase contains frontend navigation, shell state, runtime flag
consumption, route-state UI, and release smoke evidence only. No database
migration or business API change is included.

The existing shell remains available behind the same runtime flag. The flag is
server-controlled through `FEATURE_FLAGS=platform_phase1_shell=on|off` and is
read from `GET /runtime/release`; changing it does not require a frontend build
or redeployment.

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
- Added fail-closed runtime flag consumption and retained the legacy shell as
  the immediate fallback.
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
| Frontend/unit tests | PASS | `npm test`; 5 tests passed |
| Backend suite | PASS | `python -m pytest backend/tests -q`; 36 passed |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Authenticated route matrix | PASS | Disposable local runtime; all required paths directly navigated |
| Mobile drawer/breadcrumb evidence | PASS | Browser evidence on local flag-on runtime |
| Runtime flag fallback | PASS | Disposable runtime changed from on to off; legacy shell reloaded without rebuild |

## Staging and production evidence

Pending isolated branch review, exact-candidate staging deployment, operator-only
validation, general enablement, protected production promotion, observation,
and cleanup. Record exact commits, workflow URLs, artifact IDs, host-header
results, screenshots, current/previous pointers, and final flag state here as
they are produced.

## Gate checklist

The generic checklist in `docs/champion_execution/PHASE_DEPLOYMENT_GATE.md`
applies. The release is not PASS until the new shell is the production default,
all routes and access checks pass in production, fallback is demonstrated
without redeployment, observation is complete, cleanup is complete, and this
record plus the risk and handover records are committed on `main`.
