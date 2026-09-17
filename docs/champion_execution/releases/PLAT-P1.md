# PLAT-P1 — Phase 1 UX Shell and Menu Release Record

Status: **PASS — reviewed, remediated, and verified in production**
Release identity: `PLAT-P1`
Record date: 2026-09-17
Operator: Codex, working with the delivery owner
Approver: Required GitHub `production` environment reviewer; delivery owner acceptance recorded at the protected promotion gate
Production candidate: `12bc548056c59341d3ccc492a5353a696a7c0661`

## Scope and safety decision

Replace the authenticated SaaS App Shell presentation with a responsive LenERP
operator shell while preserving every existing URL and backend/database
behavior. This phase contains frontend navigation, shell state, runtime flag
consumption, route-state UI, and release smoke evidence only. No database
migration or business API change is included.

The existing shell remains available behind the same runtime flag. The flag is
server-controlled through `FEATURE_FLAGS=platform_phase1_shell=on|off` and is
read from `GET /runtime/release`. The protected flag-only workflow proved both
off and on while the exact current release remained unchanged.

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
6. The canonical SaaS hostname `lenerp.lengrowth.com` and the non-`lengrowth.com`
   staging host-header lane return the same route and flag behavior. The
   separate ERPNext hostname `erp.lengrowth.com` is not a SaaS-shell acceptance
   target.

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
- Reconciled the hostname acceptance wording with the deployed topology:
  `lenerp.lengrowth.com` is the SaaS control-plane hostname, while
  `erp.lengrowth.com` is intentionally reserved for Frappe/ERPNext.
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
| Frontend production build | PASS | `npm run build`; 34 routes generated |
| Frontend/unit tests | PASS | `npm test`; 10 tests passed |
| Backend suite | PASS | `python -m pytest backend/tests -q`; 36 passed |
| Secret scan | PASS | `python scripts/release/secret_scan.py` |
| Diff whitespace | PASS | `git diff --check` |
| Authenticated route matrix | PASS | Exact post-merge candidate browser artifact [10498661711](https://github.com/Lengrowth/crm/actions/runs/35223932797/artifacts/10498661711); 11 routes returned HTTP 200 |
| Mobile drawer/breadcrumb evidence | PASS | Exact post-merge candidate run [35223932797](https://github.com/Lengrowth/crm/actions/runs/35223932797) used shell `on`, retained desktop/mobile screenshots, and recorded zero serious/critical violations and zero serious/critical incomplete checks |
| Runtime flag fallback | PASS | Current-candidate protected flag-only off run [35227147798](https://github.com/Lengrowth/crm/actions/runs/35227147798) with [readback 10499287799](https://github.com/Lengrowth/crm/actions/runs/35227147798/artifacts/10499287799), followed by on run [35227246158](https://github.com/Lengrowth/crm/actions/runs/35227246158) with [readback 10499237979](https://github.com/Lengrowth/crm/actions/runs/35227246158/artifacts/10499237979), preserved the exact current release pointer |
| Hostname routing interpretation | PASS | Live checks on 2026-09-17 confirmed `erp.lengrowth.com/` is the Frappe login surface and `/app` redirects to Frappe `/login`; `lenerp.lengrowth.com/` is the SaaS surface and unauthenticated `/app` redirects to its SaaS `/login`; `lenerp-api.lengrowth.com/health` returned HTTP 200. The staging browser artifact uses `staging.example.test`. | The Phase 1 shell hostname requirement is explicitly interpreted as the SaaS hostname plus staging lane; no ERP hostname reroute is required. |

## Hostname acceptance reconciliation

The earlier phrase “temporary implementation hostname” was ambiguous in the
Phase 1 acceptance text. The deployed architecture intentionally separates the
two applications:

- `erp.lengrowth.com` is the temporary ERPNext implementation hostname. A live
  `curl -L` check on 2026-09-17 returned HTTP 200 with the Frappe `Login` page,
  and `/app` resolved to `https://erp.lengrowth.com/login?redirect-to=%2Fapp`.
- `lenerp.lengrowth.com` is the SaaS control-plane hostname. The same live
  check returned HTTP 200 for `/` and `/app` resolved to
  `https://lenerp.lengrowth.com/login?next=%2Fapp`; the canonical API health
  endpoint returned HTTP 200.
- The exact-candidate staging browser evidence [35223932797](https://github.com/Lengrowth/crm/actions/runs/35223932797)
  uses `staging.example.test` and records the enabled shell, route matrix, and
  accessibility results.

Therefore the Phase 1 shell acceptance is now explicit: validate the SaaS
shell under `lenerp.lengrowth.com` and the non-public staging lane, while
validate ERPNext separately under `erp.lengrowth.com`. No DNS or nginx change
is required, and routing the ERP hostname to the SaaS shell would violate the
documented application separation.

## Staging and production evidence

The authoritative post-merge candidate-bound staging run [35223932797](https://github.com/Lengrowth/crm/actions/runs/35223932797)
retained artifact [10498661711](https://github.com/Lengrowth/crm/actions/runs/35223932797/artifacts/10498661711).
It tested the exact `main` candidate `12bc548056c59341d3ccc492a5353a696a7c0661`
with the shell explicitly enabled. The artifact records runtime release and
commit identity equal to that candidate, synthetic operator-validation
provenance using a disposable authenticated platform-admin fixture, 11
authenticated routes, desktop/mobile screenshots, zero serious/critical axe
violations and zero serious/critical incomplete checks, plus non-admin
implementation denial.

The earlier candidate `0db050931933f7d8f0a4295121f3337edc135778` is retained as
the previous production release only. Its exact enabled-shell evidence run
failed the now-enforced serious-incomplete gate on `aria-prohibited-attr`, so
it is not the authoritative P1 candidate and must not be promoted again.

Protected production evidence and fallback evidence:

| Action | Run | Artifact / result |
|---|---|---|
| Prior-candidate flag-only fallback | [35204249048](https://github.com/Lengrowth/crm/actions/runs/35204249048) | [readback artifact 10489067913](https://github.com/Lengrowth/crm/actions/runs/35204249048/artifacts/10489067913); prior exact release pointer preserved, flag `false` |
| Exact candidate staging evidence with shell enabled | [35223932797](https://github.com/Lengrowth/crm/actions/runs/35223932797) | [browser artifact 10498661711](https://github.com/Lengrowth/crm/actions/runs/35223932797/artifacts/10498661711); exact candidate/runtime identity matched, synthetic operator-validation provenance recorded, strict desktop/mobile axe gate passed |
| Protected production promotion of `12bc548…` | [35224283218](https://github.com/Lengrowth/crm/actions/runs/35224283218) | [production readback artifact 10498031884](https://github.com/Lengrowth/crm/actions/runs/35224283218/artifacts/10498031884); exact release promoted, shell flag `true`, authenticated production smoke and cleanup passed |
| Current-candidate flag-only fallback | [35227147798](https://github.com/Lengrowth/crm/actions/runs/35227147798) then [35227246158](https://github.com/Lengrowth/crm/actions/runs/35227246158) | [off readback 10499287799](https://github.com/Lengrowth/crm/actions/runs/35227147798/artifacts/10499287799) showed current/previous unchanged and flag `false`; [on readback 10499237979](https://github.com/Lengrowth/crm/actions/runs/35227246158/artifacts/10499237979) restored flag `true` with current/previous unchanged |

The final readback recorded for the currently serving candidate:

- `current`: `/opt/saas-control/releases/12bc548056c59341d3ccc492a5353a696a7c0661`
- `previous`: `/opt/saas-control/releases/0db050931933f7d8f0a4295121f3337edc135778`
- backend, frontend, nginx, and R2 backup timer active; R2 timer enabled
- R2 lifecycle query succeeded with 17 objects present
- local production health HTTP `200`; clean Frappe/ERPNext source trees
- zero temporary smoke users, organizations, or active sessions

Post-release observation produced three consecutive samples with the public
root and canonical API at HTTP `200`, the runtime release fixed at the final
candidate with `platform_phase1_shell=true`, and the retired
`api.lenerp.lengrowth.com` unavailable. The protected flag-only enablement
readback recorded local health `200`, active backend/frontend/nginx/R2 timer,
R2 lifecycle verification, and zero temporary smoke users, organizations, or
sessions. The candidate-bound browser artifact covered the full dynamic route
matrix, desktop/mobile shell states, authorization denial, and strict WCAG
results. The runtime manifest intentionally reports `environment: staging`:
the immutable artifact is built in the staging lane and promoted unchanged to
production; release identity and production readback are authoritative for
where it is serving.
Automated component coverage includes persistent preferences, mobile drawer
behavior, active links, skip-link/main focus semantics, breadcrumbs, and
keyboard close behavior.

## Gate checklist

The generic checklist in `docs/champion_execution/PHASE_DEPLOYMENT_GATE.md`
applies. The P1 gate is closed: server-side restricted-route authorization,
candidate-bound CI/browser/WCAG artifacts, runtime fail-closed behavior, mobile
focus management, legacy permission filtering, and pointer-preserving flag
fallback evidence are recorded above.

## Accepted waivers and follow-up

The existing credential-rotation waiver from Phase 0 remains explicitly
accepted. No credentials were rotated or invalidated, no production Frappe or
ERPNext worktree was modified, and no database migration or business API change
was introduced. The GitHub Actions Node.js 20 deprecation annotation is an
upstream runner warning only. The independent frontend dependency audit
inventory is seven vulnerabilities (1 low, 1 moderate, 4 high, 1 critical)
and remains a separately tracked dependency-owner review item; it is not
silently treated as zero risk or conflated with the functional/browser gate.
