# Phase 1 — UX Shell and Menu

## Goal

Replace the current “SaaS App Shell” presentation with a polished, responsive LenERP operator experience while preserving all routes and functionality.

## Menu information architecture

Use plain customer-facing labels while retaining current URLs initially:

| Menu group | Label | Existing route | Purpose |
|---|---|---|---|
| Work | Home | `/app` | Portfolio health, alerts, next actions, recent activity |
| Customers | Companies | `/app/organizations` | Customer organizations and lifecycle |
| Customers | ERP Sites | `/app/tenants` | Environments, domains, health, and provisioning |
| Delivery | Implementations | `/app/implementation` | Discovery-to-go-live status and blockers |
| Product | Modules | `/app/modules` | Catalog, bundles, entitlements, compatibility |
| System | Settings | `/app/settings` | Product, security, environment, and operator configuration |

The menu definition must support required role/permission metadata even before all roles use it. Do not render links a user cannot access.

## Build scope

1. Replace static navigation with a typed grouped navigation model containing label, route, icon, permissions, feature flag, and optional badge source.
2. Build a desktop sidebar with active route, collapsible groups, compact mode, and persistent preference.
3. Build a mobile drawer and compact top header with page title, breadcrumbs, environment indicator, notifications/status area, and session menu.
4. Remove “Control Layer,” “SaaS App Shell,” and “local-only” production copy.
5. Add consistent active, hover, focus, disabled, and permission-denied behavior.
6. Preserve all current URLs. Add aliases/redirects only after the new shell is stable.
7. Put the new shell behind a server-controlled feature flag; allow instant fallback to the old shell during the release.
8. Add a route-level error boundary, loading state, not-found behavior, and access-denied page.
9. Ensure keyboard navigation, focus order, skip link, readable contrast, and narrow-screen behavior.
10. Read product name, environment label, support links, and application base URLs from configuration; do not embed `lengrowth.com` or the provisional product name in reusable shell logic.
11. Reserve navigation extension points for Champion solution packages without showing unfinished or unauthorized pages.

## Acceptance tests

- Every existing dashboard route opens from the new menu.
- Direct navigation and refresh work on every route.
- Active state and breadcrumbs match nested organization/tenant pages.
- Restricted links are absent and direct access remains denied server-side.
- Sidebar, compact mode, mobile drawer, theme, and session actions work.
- No API or database behavior changes in this phase.
- Disabling the flag restores the old shell without a redeploy.
- The SaaS shell operates correctly under the canonical SaaS hostname `lenerp.lengrowth.com` (the current temporary control-plane hostname) and a staging hostname representing the future Champion domain. The separate ERPNext hostname `erp.lengrowth.com` is not a SaaS-shell acceptance target.

## Deployment

Run the generic deployment gate. Deploy with the flag off, smoke test, enable for the operator account, complete the route matrix, then enable generally. Keep the previous shell available for one full subsequent phase.

## Gate

Phase 1 passes when the new shell is the production default, every old route remains usable, there is no authorization regression, and flag-based fallback has been tested.
