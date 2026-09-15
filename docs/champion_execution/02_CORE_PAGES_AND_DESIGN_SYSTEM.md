# Phase 2 — Core Pages and Design System

## Goal

Create the reusable shadcn-style component system and replace placeholder-heavy operator pages with clear operational views.

## Build scope

1. Add the approved shadcn/Radix primitives and Lucide icons needed now; avoid importing a large component catalog prematurely.
2. Consolidate LenERP tokens in the theme: surfaces, text, borders, accent, destructive/warning/success/info, spacing, radius, shadows, charts, and dark mode.
3. Create reusable Button, Card, Badge, Input, Select, Dialog, Sheet, Dropdown, Table, Tabs, Tooltip, Alert, Skeleton, EmptyState, ErrorState, PageHeader, Breadcrumb, and ConfirmAction components.
4. Rebuild `/app` as an operational dashboard with company/site counts, provisioning status, implementation blockers, failed jobs, domain/SSL warnings, and next actions from real APIs.
5. Rework Companies and ERP Sites list/detail/create pages with search, filters, status badges, clear primary action, validation, loading/empty/error states, and destructive-action confirmation.
6. Rework Implementation as a real portfolio view using existing implementation/project/task records instead of static milestones.
7. Rework Settings into grouped operational sections; hide unfinished settings behind flags.
8. Add reusable page layouts so Phase 3 module controls and Phase 4 provisioning use the same interaction model.
9. Remove explanatory developer copy from production pages and replace it with short operator guidance.
10. Make organization, implementation, tenant, module, domain, and package status components reusable by Champion solution packages without coupling them to one hostname or one customer's data.

## Acceptance tests

- Component states pass light/dark and responsive checks.
- Dashboard data comes from protected APIs and handles partial failures.
- Company/site create, read, update, validation error, permission denial, and empty states work.
- Existing records render without data migration.
- No page exposes raw exception text, internal credentials, or cross-tenant data.
- Old deep links remain compatible.
- Synthetic Champion and second-company records render with strict tenant separation and no production-only assumptions.

## Deployment

Ship page conversions in one phase release only after all existing route smoke tests pass. If implementation detail remains incomplete, keep only that panel behind a flag rather than shipping a broken whole page.

## Gate

Phase 2 passes when the production operator can understand system state and complete current company/site actions without placeholder content or broken legacy routes.
