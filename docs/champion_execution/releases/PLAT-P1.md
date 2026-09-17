# PLAT-P1 — Phase 1 UX Shell and Menu Release Record

Status: **PASS — production default enabled and post-release observation complete**
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

The final follow-up was reviewed and merged through PR [#17](https://github.com/Lengrowth/crm/pull/17).
The exact post-merge `main` candidate was tested in staging by run
[35189053400](https://github.com/Lengrowth/crm/actions/runs/35189053400), with
the existing staging workflow's secret scan, immutable candidate build,
preflight, public/API/authenticated smoke, and deployment checks passing. The
workflow does not emit a staging artifact; its immutable candidate ID and run
log are the staging evidence. Earlier UI candidate staging evidence is retained
in run [35117700699](https://github.com/Lengrowth/crm/actions/runs/35117700699).
Operator validation also covered the non-`lengrowth.com` host-header lane
(`staging.example.test`) and the temporary implementation lane.

Protected production evidence for the same release family:

| Action | Run | Artifact / result |
|---|---|---|
| Initial enablement on candidate `15268f8…` | [35186693396](https://github.com/Lengrowth/crm/actions/runs/35186693396) | [readback artifact 10483045169](https://github.com/Lengrowth/crm/actions/runs/35186693396/artifacts/10483045169); authenticated shell smoke passed, flag `true` |
| Flag fallback on the same candidate | [35188091170](https://github.com/Lengrowth/crm/actions/runs/35188091170) | [readback artifact 10483290012](https://github.com/Lengrowth/crm/actions/runs/35188091170/artifacts/10483290012); authenticated shell smoke passed, flag `false` |
| Final enablement on `c2b923a…` | [35189173434](https://github.com/Lengrowth/crm/actions/runs/35189173434) | [readback artifact 10483861183](https://github.com/Lengrowth/crm/actions/runs/35189173434/artifacts/10483861183); authenticated shell smoke passed, flag `true` |

The final readback recorded:

- `current`: `/opt/saas-control/releases/c2b923a5550923749b4f4ade7599b4a96a8943f1`
- `previous`: `/opt/saas-control/releases/15268f8dad1187994f89256f5dc55a7e3c982586`
- backend, frontend, nginx, and R2 backup timer active; R2 timer enabled
- local production health HTTP `200`; clean Frappe/ERPNext source trees
- zero temporary smoke users, organizations, or active sessions

Post-release observation produced three consecutive samples with the public
root and canonical API at HTTP `200`, the runtime release fixed at the final
candidate with `platform_phase1_shell=true`, and the retired
`api.lenerp.lengrowth.com` unavailable. The final production promotion's shell
smoke covered 8 authenticated operator routes. Local browser evidence covered
the full dynamic route matrix, desktop/mobile shell states, keyboard Escape,
breadcrumbs, compact mode, theme, session menu, access denied, and the no-build
legacy-shell fallback. Automated component coverage now includes persistent
preferences, mobile drawer behavior, active links, skip-link/main focus
semantics, breadcrumbs, and keyboard close behavior (8 frontend tests total).

## Gate checklist

The generic checklist in `docs/champion_execution/PHASE_DEPLOYMENT_GATE.md`
applies. The new shell is the production default, the protected smoke and
observation passed, flag fallback was demonstrated without a rebuild, cleanup
is complete, and this record plus the risk and handover records are being
committed on `main` by the evidence PR that follows the deployed candidate.

## Accepted waivers and follow-up

The existing credential-rotation waiver from Phase 0 remains explicitly
accepted. No credentials were rotated or invalidated, no production Frappe or
ERPNext worktree was modified, and no database migration or business API change
was introduced. The GitHub Actions Node.js 20 deprecation annotation is an
upstream runner warning only; it did not affect the passing release checks.
