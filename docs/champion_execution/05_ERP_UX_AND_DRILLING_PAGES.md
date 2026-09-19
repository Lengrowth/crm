# Champion Solution Packages and ERP UX

## Goal

Deliver Champion's focused ERP experience through independently defined and accepted solution packages. Champion-specific pages, modules, roles, workflows, reports, and forms may enter the release stream whenever their requirements and platform dependencies are ready; they are not forced into one late calendar phase.

This document governs the workstream. [`CHAMPION_SOLUTION_REGISTER.md`](CHAMPION_SOLUTION_REGISTER.md) contains the package decomposition and record template.

## Relationship to the fixed phases

- Phase 0 is always required before a Champion package reaches production.
- Packages may be designed and implemented in development while platform Phases 1–4 continue.
- A package may be promoted after its actual dependencies are released; it does not have to wait for Phase 4.
- Phase 1 provides the shell/navigation extension points.
- Phase 2 provides reusable page and design primitives.
- Phase 3 is required before the Champion module profile can be authoritative.
- Phase 4 is required only for packages that depend on onboarding/provisioning.
- Phase 7 cannot begin until every required Champion package is accepted in staging.

## Initial package set

| ID | Outcome |
|---|---|
| C01 | Company settings, final product name, and branding |
| C02 | Users, roles, permissions, and approval boundaries |
| C03 | Champion module profile, role workspaces, and navigation |
| C04 | Customer, Site/Well, and Well Mapping |
| C05 | Drilling and service job workflow |
| C06 | Inventory, purchasing, trucks, rigs, and assets |
| C07 | CRM, quoting, invoicing, payments, and accounting |
| C08 | Dashboards, reports, alerts, forms, and print formats |
| C09 | Office work, people, payroll, quality, and support |

## Common build rules

1. Inventory installed apps, custom fields/scripts/workspaces, and any Well Mapping code before creating replacements.
2. Put all workspaces, roles, permissions, DocTypes, fixtures, reports, print formats, CSS/JS, and patches in the version-controlled LenERP custom app or another explicitly transferred repository.
3. Keep upstream Frappe and ERPNext source clean and pinned.
4. Define success, authorization failure, validation failure, and recovery scenarios before implementation.
5. Use additive schemas and compatibility releases; do not combine destructive cleanup with the first release of a replacement.
6. Use synthetic records when Champion information is unavailable and visibly mark the package as synthetic/unaccepted.
7. Hide unfinished package entry points behind server-controlled flags.
8. Hide irrelevant workspaces by role and entitlement, but enforce access through roles, user/document permissions, and APIs rather than CSS.
9. Preserve included platform modules even when they are hidden or administrator-only for Champion.
10. Export fixtures/customizations and prove clean installation on another staging site.
11. Record package ID, version, source commit, schema revision, feature flags, tests, approver, code rollback, and data correction in every release.
12. Apply the generic deployment gate to each package or compatible package group.

## Synthetic foundation that can begin early

Before real data and final decisions, the team may:

- create the Well/Site and Job schema scaffolds;
- create synthetic customer-to-well-to-job-to-completion-to-invoice records;
- implement role-navigation prototypes and negative permission tests;
- create reusable list/form/dashboard/print layouts;
- link standard ERP Customer, Quotation, Project, Sales Invoice, Stock Entry, Asset, and related records;
- establish fixture, migration, test, export, and clean-install mechanics.

Synthetic work does not approve final field names, status transitions, accounting rules, inventory structure, reports, forms, or permissions.

## Package acceptance

Each required package passes when:

- its requirements and commercial classification are recorded;
- the approved roles can complete representative workflows;
- unauthorized direct URL and API access is denied;
- required data saves, searches, links, reports, prints, and exports correctly;
- desktop, tablet, and mobile-web views are usable where included;
- the exact package installs/migrates cleanly on staging;
- fallback, code rollback, and data correction are documented and tested in proportion to risk;
- Champion's acceptance authority approves the package or records accepted exceptions.

## Production release

Install or update the custom app through the staging-first release path. Deploy new package behavior disabled, run migrations and smoke tests, enable it for test roles, complete package acceptance, and then enable it for the approved production roles.

Keep previous workspaces/routes available until the replacement package is verified. Do not debug a failed package by making undocumented edits directly in production.

## Workstream gate

The Champion solution workstream is complete only when all Included packages are released or explicitly accepted/deferred in writing, the package register points to evidence, the final Champion module and role matrices match production, and no required behavior exists only as an undocumented production customization.
