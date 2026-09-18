# LenERP UX and Screen Blueprint

Status: **Target-state UX specification**  
Scope: Public reseller experience, LenERP operator control plane, and Champion ERP experience after complete program delivery

## Purpose

This document defines what users will see, understand, and do in the completed
LenERP platform. It is a screen blueprint, not a statement that every screen is
already deployed. Final Champion terminology, fields, workflow transitions,
permissions, reports, and branding remain subject to approved package inputs and
acceptance.

## Experience model

LenERP presents three deliberately separate experiences:

| Experience | Audience | Primary job |
|---|---|---|
| Public/reseller | Prospective companies and applicants | Understand the product and submit a reviewable request |
| Operator control plane | LenERP platform and implementation operators | Manage companies, sites, modules, onboarding, provisioning, health, and delivery |
| Champion ERP | Champion office, field, sales, accounting, inventory, management, and administrators | Run the approved drilling and business workflows |

The visual language is shared, but permissions and terminology differ. A public
applicant never sees internal entitlement or infrastructure controls. A
Champion field user never sees platform-operator administration merely because
the route exists.

## UX principles

1. **State before action.** Every screen makes current state, blockers, and next action clear.
2. **No false readiness.** Requested, approved, entitled, applied, verified, and ready are visibly distinct.
3. **Progressive disclosure.** Lists show the operational summary; detail screens expose history, dependencies, evidence, and advanced actions.
4. **Safe mutation.** Destructive, irreversible, external, or high-risk actions show impact and require confirmation.
5. **Actionable failure.** Errors explain what the user can do next without exposing raw exceptions or secrets.
6. **Role-shaped navigation.** Users see relevant destinations, while backend authorization protects direct access.
7. **Environment clarity.** Staging, production, and implementation contexts are always distinguishable.
8. **Responsive by design.** Desktop, tablet, and mobile web retain the same information hierarchy and supported actions.
9. **Accessible interaction.** Keyboard operation, visible focus, semantic structure, status announcements, contrast, and reduced motion are default behavior.
10. **Traceability.** Important decisions and state changes link to actor, time, reason, and evidence.

## Shared shell

### Desktop

The desktop application uses a persistent left sidebar and a compact top/page
header.

Sidebar structure:

| Group | Destination | Purpose |
|---|---|---|
| Work | Home | Portfolio status, alerts, next actions, recent activity |
| Customers | Companies | Company lifecycle and related sites |
| Customers | ERP Sites | Site environment, health, domains, and provisioning |
| Delivery | Implementations | Projects, tasks, blockers, and go-live readiness |
| Delivery | Onboarding | Submitted requests, review, decisions, and conversion |
| Delivery | Provisioning | Durable jobs, steps, failures, recovery, and validation |
| Product | Modules | Catalog, bundles, entitlements, dependencies, and audit |
| System | Settings | Product, environment, security, support, and operations |

The sidebar supports:

- grouped navigation;
- permission and feature-flag filtering;
- active parent/child state;
- collapsible groups;
- compact mode;
- persisted preference;
- optional status/count badges;
- Champion package extension points.

### Header

The header contains:

- page title and breadcrumb trail;
- environment badge;
- release/health indicator;
- relevant status or notification summary;
- theme control;
- support entry point;
- session menu with identity and sign-out.

### Mobile and tablet

- The sidebar becomes a focus-managed drawer.
- The top header retains title, environment, critical status, and session access.
- Tables become horizontal-scroll regions, prioritized cards, or stacked rows without losing labels.
- Primary actions remain reachable without overlapping browser controls.
- Drawers and dialogs close with Escape and restore focus to the invoking control.

### Global states

Every route provides:

- skeleton/loading state;
- empty state with a relevant next action;
- permission-denied state;
- not-found state;
- safe error state with retry where appropriate;
- partial-failure treatment for multi-panel pages;
- disabled state explaining the required permission, flag, dependency, or approval.

## Public/reseller screens

### 1. Product home

Purpose: explain LenERP outcomes and guide a visitor toward the relevant module
or onboarding path.

Key content:

- clear value proposition;
- supported industries and workflows;
- module and implementation overview;
- trust/operating model without sensitive infrastructure detail;
- calls to view modules, book a demo, contact the team, or start onboarding;
- sign-in for existing users.

### 2. Modules showcase

Purpose: show the marketed subset of the authoritative module catalog.

Screen behavior:

- search and category filters;
- module cards with approved public descriptions;
- bundle comparison;
- dependency explanation written in customer language;
- “Request this module” adds it to an onboarding draft only;
- internal, inactive, administrator-only, dependency-schema, and customer-entitlement fields remain hidden.

### 3. Industries and drilling solution

Purpose: show how LenERP supports drilling and field-service operations.

The screen connects outcomes rather than promising unapproved details:

- customer and well context;
- drilling/service jobs;
- crews, rigs, equipment, and materials;
- quoting through completion/invoice context;
- reports and field/office continuity.

### 4. Onboarding wizard

The wizard is resumable and versioned.

Suggested steps:

1. Company details.
2. Primary and proposed administrator contacts.
3. Module bundle and module requests.
4. Branding and product identity needs.
5. Users and role expectations.
6. Data-import categories and readiness.
7. Domain and infrastructure preferences.
8. Billing contact.
9. Review and submit.

Each step includes validation, save-and-return behavior, and a progress
indicator. The final screen states clearly:

- the request was submitted for review;
- no site or entitlement has been created;
- an operator must approve it;
- the applicant can use the scoped return path to view or revise permitted fields.

### 5. Applicant request status

Displays only applicant-safe information:

- request reference;
- version;
- draft/submitted/under-review/approved/rejected/cancelled status as appropriate;
- revision requested message;
- submitted selections;
- safe operator communication;
- revise or resubmit action when allowed.

It never exposes internal users, audit metadata, infrastructure targets, job
payloads, entitlement records, or provisioning credentials.

### 6. Contact and demo

Short forms provide clear success/failure feedback, spam protection, privacy
context, and no implication that a customer workspace has been created.

## Operator control-plane screens

### 1. Home dashboard — `/app`

Purpose: answer “What needs attention now?”

Primary sections:

- portfolio cards: companies, ERP sites, implementations, onboarding requests;
- provisioning summary: queued, running, failed, validation, ready;
- implementation blockers and overdue tasks;
- domain/SSL warnings;
- failed jobs and stale work;
- module/application verification gaps;
- prioritized next actions;
- recent significant activity.

Each card links to a filtered operational view. If one API fails, its panel
shows an error while the rest of the dashboard remains useful.

### 2. Companies list — `/app/organizations`

Columns/row content:

- company name and industry;
- lifecycle status;
- ERP-site count and health summary;
- implementation status;
- module readiness summary;
- critical blocker/warning;
- updated time;
- row actions.

Controls:

- search;
- status/industry/implementation filters;
- sorting;
- create company for authorized users;
- saved view/export only where approved.

### 3. Create company — `/app/organizations/new`

Sections:

- identity and legal information;
- industry, country, timezone;
- billing/primary contact;
- initial lifecycle state;
- onboarding request link when creation originates from approval.

The form uses inline validation, submission progress, duplicate warnings, and
safe conflict handling.

### 4. Company detail — `/app/organizations/[organizationId]`

Header:

- company identity;
- status badge;
- primary action;
- warnings and implementation owner.

Tabs:

| Tab | Content |
|---|---|
| Overview | Company details, contacts, status, recent activity, next actions |
| ERP Sites | Sites, environment, health, domain, provisioning |
| Implementation | Project, tasks, blockers, target dates |
| Modules | Effective modules, source, requested/entitled/applied/verified state |
| Users & roles | Approved memberships and role context where included |
| Audit | Significant company, entitlement, onboarding, and lifecycle changes |

Sensitive state-changing actions require confirmation and an optional/required
reason according to policy.

### 5. ERP Sites list — `/app/tenants`

Shows:

- site/tenant name;
- company;
- environment;
- lifecycle and provisioning status;
- primary/custom domain;
- DNS/SSL state;
- health and last verification;
- app/version summary;
- active warnings.

Filters cover company, environment, health, provisioning, domain, and status.

### 6. Create/planned ERP site — `/app/tenants/new`

This screen creates only the level of record authorized by the selected flow.
It does not silently bypass onboarding approval.

Fields include:

- company;
- requested slug/site name;
- environment;
- approved domain intent;
- module/onboarding source;
- implementation context.

Site-name and domain checks are preflight results, not proof of reservation
until the durable workflow records it.

### 7. ERP Site detail — `/app/tenants/[tenantId]`

Header:

- site identity and company;
- environment;
- health/readiness;
- domain/SSL summary;
- last verified time.

Tabs:

| Tab | Content |
|---|---|
| Overview | Lifecycle, URLs, environment, warnings, next actions |
| Provisioning | Current workflow and historical jobs |
| Modules | Entitled/applied/verified state per module |
| Domain & SSL | Mapping, DNS state, SSL state, approved actions |
| Health | App versions, checks, workers, last evidence |
| Audit | Operator actions and state transitions |

Suspend/reactivate, retry, rollback, or domain actions appear only when the
current state and user permission allow them.

### 8. Implementation portfolio — `/app/implementation`

Portfolio view:

- company/project;
- owner;
- current phase/status;
- progress derived from tasks;
- target date;
- blocker count;
- site/module/data readiness;
- next milestone.

Filters include owner, company, status, blocked state, due date, and package.

Project detail can show:

- tasks grouped by stage;
- dependencies;
- owners and due dates;
- blockers/decisions;
- package and migration readiness;
- acceptance/evidence links.

### 9. Modules administration — `/app/modules`

Catalog view:

- search and category/status filters;
- marketed, active, internal, or unavailable status;
- app/version requirement;
- dependency/incompatibility indicators;
- bundle membership.

Module detail drawer/page:

- public and internal descriptions;
- stable key and aliases;
- dependency graph/explanation;
- incompatible modules;
- required app/version;
- default roles/workspaces;
- configuration schema summary;
- organizations using/requesting the module, subject to access.

Assignment flow:

1. Select company and bundle/modules.
2. Preview effective change.
3. Review dependency additions/removals and conflicts.
4. Enter reason.
5. Confirm.
6. See persisted result and audit reference.

The result distinguishes requested, entitled, applied, and verified.

### 10. Onboarding queue — `/app/onboarding`

Queue columns:

- request/company name;
- version;
- state;
- requested bundle;
- submitted time;
- assigned reviewer;
- duplicate/preflight warnings;
- next action.

Filters cover state, reviewer, bundle, warning, submission date, and execution
readiness.

### 11. Onboarding review detail — `/app/onboarding/[requestId]`

Sections:

- applicant/company data;
- version history and comparison;
- requested modules and exact bundle/catalog version;
- users/roles, branding, data, domain, and billing needs;
- duplicate-company/site/domain warnings;
- module dependency validation;
- comments and decision history;
- conversion preview.

Actions:

- begin review;
- request revision;
- approve exact version;
- reject;
- cancel;
- authorize conversion/execution when policy allows.

Approval dialogs state what approval does and does not do. Infrastructure work
never begins through an ambiguous primary button.

### 12. Provisioning portfolio — `/app/provisioning`

Shows all authorized workflows with:

- company/site;
- onboarding request/version;
- workflow version;
- current step;
- state;
- attempt/retry status;
- lease/worker health summary;
- failure category;
- updated time.

Filters cover state, step, environment, company, retry required, and operator
confirmation required.

### 13. Provisioning detail — `/app/provisioning/[jobId]`

Top summary:

- target company/site/environment;
- approval and request version;
- workflow state;
- readiness;
- safe next action.

Step timeline shows for each step:

- stable step name;
- pending/running/succeeded/failed/skipped/rollback state;
- attempts;
- start/end times;
- safe diagnostic;
- evidence reference;
- retry classification.

Operator actions:

- retry a safe step;
- confirm an ambiguous/irreversible retry;
- cancel where safe;
- start supported compensation/cleanup;
- inspect domain/SSL, health, and handoff evidence.

Raw payloads, secrets, provider responses, and stack traces are never displayed.

### 14. Settings — `/app/settings`

Grouped sections:

- Product: configured name, branding references, support details.
- Environment: environment and safe release/app versions.
- Security: session/security posture and administrative guidance without secret values.
- Feature availability: safe operational status of server-controlled features.
- Support and operations: support links, monitoring status, documentation.
- Domain transition: read-only current/final-domain readiness where applicable.

Unsupported controls remain absent instead of appearing disabled without a real
backend behavior.

## Champion ERP screens

Exact Frappe routes and labels may follow the approved Champion vocabulary, but
the following screen outcomes are required.

### 1. Role home/workspace

Each role lands on a focused workspace.

Examples:

- Office/dispatch: active jobs, scheduling conflicts, unassigned work, field exceptions.
- Field: assigned jobs, today’s work, required capture, sync/connection status where applicable.
- Sales: leads, opportunities, quotes awaiting action, customer follow-ups.
- Inventory: low stock, receiving, transfers, job demand, exceptions.
- Accounting: invoices, payments, receivables, approval exceptions.
- Management: KPI dashboard, operational blockers, financial/fulfillment summaries.
- Administrator: users, roles, modules, configuration, health, audit, and support.

Users do not see workspaces they cannot use, and direct access remains denied by
roles/document permissions.

### 2. Customers and contacts

Customer list:

- search, filters, status, owner, open jobs/wells, outstanding actions.

Customer detail:

- identity and contacts;
- related wells/sites;
- active and historical jobs;
- quotes/invoices/payments according to permission;
- notes, files, activity, and reports.

### 3. Sites/Wells list

Shows:

- approved well/site identifier;
- customer;
- location/status;
- active job;
- assigned crew/rig where relevant;
- latest activity;
- warnings or incomplete required data.

Search and filters support customer, status, location, assigned resource, and
operational state.

### 4. Site/Well detail

Header:

- canonical identity;
- customer;
- status;
- location/map action;
- primary operational action.

Sections/tabs:

| Section | Content |
|---|---|
| Overview | Approved fields, status, location, contacts, current work |
| Jobs | Current and historical drilling/service jobs |
| Map | Approved Well Mapping/location representation |
| Equipment | Assigned rigs, trucks, assets, and relevant history |
| Materials | Job/site-related inventory context where approved |
| Documents | Photos, forms, attachments, signatures, print outputs |
| Activity | Notes, changes, events, and audit context |

### 5. Well Mapping

The map provides:

- permission-scoped wells/sites;
- search and filters;
- status and active-job markers;
- selected-well summary;
- navigation to the canonical well detail;
- clear distinction between stored location and live GPS where live tracking is not approved.

### 6. Jobs list/dispatch view

Supports:

- list, board, calendar, or dispatch-oriented view as approved;
- customer, well/site, job type, state, priority, schedule, assignee/crew, rig/equipment, blocker, and completion readiness;
- filters and saved operational views;
- clear unassigned, overdue, blocked, and exception states.

### 7. Job detail

Core structure:

- customer and well/site context;
- job type and approved state machine;
- schedule and assignment;
- crew, rig, truck, and equipment;
- instructions/checklist;
- materials and stock activity;
- field notes, photos, forms, and signatures;
- exceptions and approvals;
- completion/reopen controls;
- related quote/invoice context where authorized;
- immutable history of key transitions.

Only valid actions for the current state and role are shown. Backend validation
rejects invalid transitions even through direct API access.

### 8. Field execution

Mobile-web layout prioritizes:

- today’s assigned jobs;
- job/well identity and directions/location context;
- start/check-in action where approved;
- required checklist and field capture;
- notes/photos/forms/signature;
- materials used;
- blocker/exception reporting;
- complete/submit-for-review action;
- visible saved/submitted state.

The interface avoids dense desktop tables and preserves large, reachable touch
targets.

### 9. Inventory and purchasing

Screens include, as approved:

- item list/detail;
- warehouse/location balances;
- stock movements and traceable history;
- receiving;
- transfers;
- picking/issue to job;
- purchasing requests/orders/receipts;
- low-stock and exception views.

Balances are not silently overwritten; corrections are recorded as controlled
movements or approved adjustments.

### 10. Trucks, rigs, equipment, and assets

List/detail screens show:

- identity and type;
- status/availability;
- assigned job/site/crew;
- maintenance context;
- documents and history;
- related stock/equipment assignments where approved.

### 11. CRM and quoting

Screens connect:

- lead/opportunity;
- customer/contact;
- well/site or requested work;
- quotation and approvals;
- resulting job/order context;
- follow-up activity.

Pricing and approval behavior follows the accepted Champion package rather than
generic placeholder rules.

### 12. Invoicing, payments, and accounting

Authorized roles can access:

- invoice preparation from approved completion/commercial context;
- invoice list/detail;
- payment and receivable state;
- accounting dimensions and approved chart-of-accounts behavior;
- exceptions and approval history;
- opening-balance and migration reconciliation evidence where appropriate.

Operational users see only the billing readiness/status necessary for their
work, not unrestricted accounting data.

### 13. Reports and dashboards

Every report states:

- title and purpose;
- filters and period;
- data freshness/as-of time;
- relevant totals;
- permission scope;
- export/print actions where approved.

Management dashboards may combine drilling, jobs, inventory, sales, and
financial KPIs only after KPI definitions and source rules are approved.

### 14. Forms, documents, and print outputs

Approved outputs use Champion branding and include the required:

- identifiers;
- customer/well/job context;
- dates and responsible users;
- signatures/photos where included;
- version/status;
- printable/exportable layout.

## Shared interaction patterns

### Status presentation

Statuses use text and shape/icon support, not color alone.

| Family | Typical states |
|---|---|
| Onboarding | Draft, Submitted, Under review, Approved, Provisioning, Validation, Ready, Rejected, Cancelled |
| Provisioning step | Pending, Running, Succeeded, Failed, Skipped, Retry scheduled, Confirmation required, Rolled back |
| Module | Marketed, Requested, Entitled, Pending application, Applied, Pending verification, Verified, Failed |
| Site | Planned, Provisioning, Validation, Ready, Suspended, Failed, Archived |
| Implementation | Discovery, Configuring, Validating, Blocked, Accepted, Released |
| Job | Uses the exact approved Champion workflow, never an invented generic transition set |

### Confirmation pattern

Confirmation dialogs show:

- the object being changed;
- current and resulting state;
- dependencies or downstream effects;
- whether the action is reversible;
- required reason;
- exact confirm action.

Typing arbitrary confirmation phrases is reserved for genuinely high-risk
operations, not routine actions.

### Audit/history pattern

History entries show:

- action;
- actor;
- timestamp;
- reason;
- before/after summary;
- source request, bundle, workflow, or release;
- evidence/reference when relevant.

Sensitive payloads and credentials never appear.

### Error pattern

User-facing errors contain:

- a safe summary;
- affected operation;
- whether anything changed;
- recommended next action;
- correlation/reference ID for support.

Raw provider messages, stack traces, SQL, filesystem paths, and credentials are
not shown.

## Primary end-to-end journeys

### Future-company onboarding

```text
Browse modules
  → create/revise request
  → submit exact version
  → operator review and validation
  → explicit approval
  → transactional control-plane conversion
  → durable isolated provisioning
  → health and configuration verification
  → first-login handoff
  → ready
```

At every arrow, the UI shows who can act, what prerequisite is missing, and
whether external state has changed.

### Champion operating flow

```text
Customer
  → Site/Well
  → approved quote or work request
  → Job and assignment
  → field execution and material use
  → completion and approval
  → invoice/payment/accounting context
  → reports and management visibility
```

The final exact transitions, required fields, and approvals come from accepted
packages `C04`–`C08`.

### Release flow

```text
Branch and tests
  → immutable candidate
  → staging migration and browser evidence
  → protected approval
  → promote the exact candidate
  → production smoke and observation
  → cleanup and readback evidence
  → release record and handover baseline
```

## Accessibility and responsive acceptance

Every supported screen is validated for:

- keyboard-only use;
- visible focus and logical order;
- semantic headings, forms, landmarks, tables, and status announcements;
- dialog/drawer focus trap and restoration;
- contrast in light and dark themes;
- reduced motion;
- desktop, tablet, and narrow mobile layouts;
- zoom/reflow and overflow behavior;
- clear validation association;
- no serious automated accessibility violations, with incomplete checks manually reviewed.

## Final-domain and handover experience

At go-live:

- the SaaS and ERP surfaces use the approved Champion-controlled domain model;
- generated links, cookies, callbacks, APIs, files, jobs, email links, webhooks, monitoring, and backups use approved configuration;
- the former implementation hostname follows the accepted redirect/compatibility policy;
- no independent Champion application or data remains exposed through the old hostname after transition;
- help/support content points to the receiving owner and delivered operating guides;
- administrators can identify the deployed release, obtain support evidence, and follow backup, recovery, update, and incident runbooks.

## Items that cannot be finalized without Champion approval

The following remain explicitly provisional until their package inputs are approved:

- final product/company branding and terminology;
- exact user list, role matrix, and approval limits;
- Champion module visibility and workspace matrix;
- Well/Site fields, identifiers, map behavior, and completion requirements;
- drilling/service job types, states, transitions, assignments, and reopen rules;
- warehouses, items, units, stock-use rules, rigs/trucks/assets, and maintenance workflows;
- quote/pricing, tax, payment, chart-of-accounts, and opening-balance rules;
- KPI definitions, reports, alerts, forms, signatures, and print formats;
- migrated data mappings, accepted variances, and final reconciliation;
- final domain, ownership accounts, trainers, validators, and acceptance authority.

These dependencies must appear as pending decisions or package states. The UX
must never disguise synthetic examples or provisional assumptions as accepted
Champion production behavior.

## Pre-kickoff demonstration surfaces

The synthetic demonstration uses business language in customer-facing surfaces:
Demo workspace, Company, Customers, Wells and sites, Jobs, Inventory,
Equipment, Quotes and invoices, and Reports. It may explain that records are
fictional and assumptions are provisional, but it must not expose package IDs,
phase labels, release pointers, commit hashes, or raw control-plane state.

The authenticated reseller/control-plane administrator may retain operational
diagnostics in restricted views. Champion ERP roles see only the workspace and
standard/custom DocTypes granted by their role. Direct routes and API calls
remain authorization checks; hiding a shortcut is not a permission boundary.
