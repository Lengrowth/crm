# LenERP Post-Program Features and Controls

Status: **Target-state blueprint**  
Applies after: `PLAT-P0`–`PLAT-P4`, all required Champion solution packages, migration stages `D01`–`D09`, and `FINAL-P7` have passed or received explicit written exceptions

## Purpose

This document describes what LenERP will contain when the complete delivery
program is finished. It is a product and operating-model specification, not a
claim that every item is already deployed.

The finished system has three connected surfaces:

1. A public reseller experience for product discovery and controlled onboarding requests.
2. A LenERP control plane for companies, ERP sites, implementations, modules, onboarding, provisioning, domains, and operational health.
3. A Champion ERP experience for drilling, service, inventory, commercial, accounting, reporting, and administration workflows.

The control plane determines what has been requested and approved. ERPNext and
`lenerp_core` execute the business workflows. An entitlement in the control
plane never, by itself, proves that the corresponding ERP configuration has
been applied or verified.

## Completion boundary

The target state is complete only when all of the following are true:

- Fixed platform releases `PLAT-P0` through `PLAT-P4` have passed.
- Every Included Champion package `C01`–`C08` is released and accepted, or has a written exception.
- Every included data category has completed `D01`–`D09`, including production reconciliation.
- The final Champion-controlled domain, infrastructure, repositories, backups, monitoring, and administrative accounts have been transferred.
- Training, acceptance, known limitations, warranty intake, and operational ownership are recorded.

Synthetic demonstrations prove platform behavior, but do not substitute for
Champion approval of field names, workflows, permissions, reports, accounting
rules, migrated data, or final production output.

## Users and authority boundaries

| User | Primary capabilities | Explicit limits |
|---|---|---|
| Public applicant | Browse marketed modules; prepare, revise, submit, and resubmit an onboarding request | Cannot grant entitlements, create a company/site, trigger billing, change DNS, provision infrastructure, or mark work ready |
| Platform operator | Review requests; manage companies/sites; administer modules; approve and supervise provisioning; inspect health and audit evidence | Cannot bypass dependency, approval, environment, migration, or verification gates |
| Company administrator | Manage approved company users and permitted company settings; view company sites and effective modules | Cannot access another company or self-grant platform-level capabilities |
| Implementation manager | Manage implementation projects, tasks, blockers, validation, and handoffs | Cannot provision or change entitlements unless separately authorized |
| Champion office/dispatch user | Manage customers, wells/sites, jobs, schedules, assignments, and operational exceptions within role permissions | No unrestricted accounting, security, or platform administration |
| Champion field user | View assigned work; record field activity, status, notes, photos, materials, and completion evidence | Sees only assigned/authorized operational data |
| Sales/accounting/inventory user | Performs the approved workflow for the assigned functional area | Access is constrained by role, company, document, and approval rules |
| Champion administrator | Manages the transferred Champion environment, users, supported configuration, backups, and routine operations | Destructive infrastructure or data operations still require the documented runbook and recovery controls |

## Public reseller and onboarding capabilities

### Product and module discovery

- Public pages present the approved LenERP value proposition, industries, module catalog, pricing/engagement guidance, and contact/demo actions.
- Public and internal module descriptions resolve to the same stable catalog identities.
- Only modules marked as marketed appear publicly; internal metadata, dependency implementation details, credentials, and customer entitlements remain protected.
- Module bundles such as Champion Drilling and Generic Field Service can be explained publicly without automatically applying them to a company.

### Versioned onboarding request

The public onboarding flow captures:

- company and business-contact details;
- proposed administrator contact;
- requested module bundle and module selections;
- branding and user/role needs;
- data-import categories and readiness, but not confidential source files;
- desired domain and infrastructure information;
- billing contact and implementation notes.

Each submission is versioned. Applicants can save, revise, submit, and, when
permitted, resubmit. Repeated submission with the same idempotency key does not
create duplicate records.

Public submission creates only an onboarding request. It does not create a
company, tenant, invoice, entitlement, domain, provisioning job, ERP site, or
administrator account.

## Operator control-plane capabilities

### Application shell

- Responsive desktop sidebar and mobile drawer.
- Grouped, permission-aware navigation with active states and breadcrumbs.
- Compact-mode and theme preferences.
- Environment and release identification, operational status, notifications, support access, and session controls.
- Loading, empty, error, not-found, access-denied, and disabled states.
- Keyboard operation, focus management, skip link, readable contrast, reduced-motion support, and responsive layouts.
- Server-controlled feature flags with fail-closed behavior.

### Operational dashboard

The Home dashboard summarizes protected API data:

- company and ERP-site counts;
- provisioning state and failures;
- implementation blockers and overdue work;
- failed jobs;
- domain and SSL warnings;
- prioritized next actions.

Partial API failure affects only the relevant panel. It is not displayed as a
misleading zero or healthy state.

### Companies

Operators can:

- search and filter companies;
- create and update company records;
- inspect lifecycle status, billing contact, implementation, sites, effective modules, and audit context;
- navigate from a company to its ERP sites, implementation work, module state, and onboarding source;
- see safe validation, permission, not-found, loading, empty, and error states.

Company records are tenant isolated. Public IDs and APIs do not expose another
company's data through direct object references.

### ERP sites

Operators can:

- search and filter sites by company, environment, health, provisioning, domain, and lifecycle status;
- create/update planned site records through approved flows;
- inspect Frappe, ERPNext, and LenERP app/version evidence;
- view domain, DNS, SSL, provisioning, worker, health, and verification state;
- suspend/reactivate or perform other supported sensitive actions with confirmation;
- open provisioning history and implementation context.

A site is not shown as ready until mandatory health and verification steps pass.

### Implementation portfolio

- Portfolio view across companies, implementation projects, tasks, owners, target dates, blockers, and status.
- Search and filters for company, owner, phase, blocker state, and target date.
- Progress is derived from persisted records rather than static milestones.
- Partial failures and missing information remain visible and actionable.

### Module control

The authoritative catalog contains stable entries for Accounting, Buying,
Selling, Stock, Assets, HR, Payroll, Manufacturing, CRM, Quality, Projects,
Support, Well Mapping, and approved supporting modules.

Operators can:

- browse and filter the catalog;
- inspect descriptions, category, active/marketed status, dependencies, incompatibilities, app/version requirements, roles, workspaces, and configuration schema;
- preview a bundle or organization change before applying it;
- see dependency additions/removals and validation conflicts;
- apply an authorized, transactional, idempotent entitlement change;
- reverse a supported change;
- inspect exact before/after audit history.

Module state is explicitly separated:

| State | Meaning |
|---|---|
| Marketed | Available in the approved public catalog |
| Requested | Included in an onboarding or operator request |
| Entitled | Approved for the organization in the control plane |
| Applied | Configuration was applied to the target ERP site by a trusted process |
| Verified | The ERP site was checked and matches the expected state |

No screen collapses these states into a generic `enabled` or `ready` label.

### Onboarding review

Operators have a queue for draft/submitted work and can:

- compare request versions;
- validate company, site, domain, modules, bundle versions, users, and implementation inputs;
- detect likely duplicates;
- move a request under review;
- request revisions where supported;
- approve, reject, or cancel with a reason;
- authorize conversion and execution only under the approved policy.

Approval binds to one exact request version and catalog/bundle version. A
material revision invalidates stale approval.

### Durable provisioning

An approved request converts transactionally into one coherent set of control-plane records:

- organization;
- initial membership/administrator handoff record;
- implementation project and initial tasks;
- tenant;
- module entitlement set;
- approved subscription/billing intent;
- domain reservation/mapping;
- provisioning workflow.

Provisioning is durable and step based:

1. Validate approved request and version.
2. Reserve and revalidate the site name.
3. Create or register the isolated site.
4. Install pinned Frappe and ERPNext versions when applicable.
5. Install the pinned LenERP app.
6. Apply modules.
7. Apply roles and workspaces.
8. Apply branding and approved settings.
9. Prepare and bind the domain/SSL under explicit authority.
10. Create or invite the administrator securely.
11. Run health checks.
12. Verify apps, modules, and configuration.
13. Prepare first-login handoff.
14. Mark ready only when mandatory verification passes.

Every step records status, attempts, timestamps, worker lease, sanitized events,
evidence, failure classification, and rollback/compensation state. Worker death
or restart does not duplicate external resources. Unsafe retries require an
operator confirmation.

### Settings and administration

Settings are grouped into product, environment, security, support, and
operational sections. Read-only values are visibly read-only. Incomplete
settings remain hidden behind server-controlled flags. Secrets and secret-derived
values are never rendered.

## Champion ERP capabilities

All Champion-specific work is version controlled in `lenerp_core` or another
explicitly transferred repository. Upstream Frappe and ERPNext remain clean and
pinned.

### C01 — Company, product name, and branding

- Approved company identity, product name, logo, colors, timezone, currency, fiscal year, and supported document branding.
- Replaceable assets and environment-driven hostnames.
- No reusable component or business rule depends permanently on `lengrowth.com`.

### C02 — Users, roles, and permissions

- Approved users, role profiles, workspaces, approval limits, and document permissions.
- Separate platform, company-administration, office/dispatch, field, sales, accounting, inventory, management, and support boundaries as approved.
- Direct UI route, API, report, and document-access negative tests.
- Hiding a workspace never substitutes for authorization.

### C03 — Module profile and navigation

- Champion modules classified as enabled, administrator-only, hidden/preserved, or pending configuration.
- Included platform modules remain installed/preserved even when hidden from daily roles.
- Role-specific workspaces and navigation reflect effective, applied, and verified module state.

### C04 — Customer, Site/Well, and Well Mapping

- Customer and contact context connected to canonical Site/Well records.
- Approved identifiers, location/GPS fields, ownership/status, drilling context, notes, attachments, and completion requirements.
- Searchable list and detail views plus approved Well Mapping/map experience.
- Links from customer to wells, jobs, documents, reports, and exports.

### C05 — Drilling and service jobs

- Approved job types, states, assignments, schedules, crews, rigs/equipment, field notes/photos, materials, completion, reopen, and exception rules.
- Office-to-field handoff and field-to-office completion workflow.
- Role-specific actions, transition validation, and audit history.
- Customer → Well → Job → Completion continuity.

### C06 — Inventory, purchasing, trucks, rigs, and assets

- Approved warehouses/locations, items, units of measure, stock balances and movements.
- Purchasing and receiving workflows.
- Assignment and consumption of stock against jobs where approved.
- Trucks, rigs, equipment, assets, and maintenance context.
- Traceable custody/movement rather than manually overwritten balances.

### C07 — CRM, quoting, invoicing, payments, and accounting

- Lead/opportunity/customer context.
- Approved quote and pricing workflow.
- Connection between quote, customer, well/job, completion, invoice, payment, and accounting records.
- Approved chart of accounts, taxes, terms, opening balances, and approval controls.
- QuickBooks or other integration behavior only where separately approved and evidenced.

### C08 — Dashboards, reports, alerts, forms, and print formats

- Role-appropriate operational and management dashboards.
- Approved KPI definitions and source rules.
- Reports with permission-aware filters, totals, exports, and data provenance.
- Alerts and notifications tied to real workflow events.
- Approved field/office forms, signatures/photos where required, and branded print formats.

## Data migration controls

Every included category—customers, contacts, wells/sites, jobs, quotes,
invoices/opening balances, payments, vendors, items, stock, assets, users,
notes, and documents—moves through `D01`–`D09`.

The finished migration system provides:

- a source/owner/validator register;
- secure-transfer and retention rules;
- source checksums and untouched originals;
- target data dictionary and versioned mapping;
- dry-run and clean-staging import modes;
- batch IDs and target schema/app versions;
- accepted, imported, updated, rejected, held, duplicate, and variance counts;
- deterministic retry without duplicate accepted rows;
- rejection and correction outputs;
- relationship and control-total reconciliation;
- workflow UAT using migrated data;
- production freeze, delta, backup, cutover, and correction plans;
- final production reconciliation and Champion validator approval.

No Champion source data appears in Git, public/reseller pages, synthetic tenants,
ordinary logs, or another tenant.

## Deployment and operational controls

### Repository boundaries

| Repository/data area | Responsibility |
|---|---|
| `crm` | Public website, operator frontend, control-plane backend, workflows, deployment and release tooling |
| `lenerp_core` | Champion/LenERP DocTypes, roles, permissions, workspaces, reports, print formats, fixtures, hooks, patches, and ERP UX |
| `frappe` | Clean, pinned upstream framework |
| `erpnext` | Clean, pinned upstream ERP application |
| Site database/files | Business records and attachments; never stored in Git |

Automated checks fail when tracked changes appear in upstream Frappe or ERPNext.

### Staging-first delivery

- A merge to `main` builds an immutable candidate and deploys that exact candidate to staging.
- Frontend, backend, custom app, migrations, manifests, and tests are completed before traffic changes.
- Production promotion is separate, explicit, protected, and uses the exact staging-tested artifact.
- Candidate manifests record commits, dependency hashes, database revisions, installed apps, feature flags, environment, build time, and operator.
- Existing routes and APIs remain compatible until replacements are verified.

### Feature rollout

- Incomplete pages/actions default off.
- Mutating capabilities use granular, server-controlled, fail-closed flags.
- High-risk releases progress through read-only, operator-only, synthetic verification, then approved general availability.
- Public requests never bypass operator approval through a frontend flag.

### Schema and data change

- Expand/migrate/contract releases keep rollback compatibility.
- Additive schema precedes compatible code; destructive cleanup occurs only in a later release.
- Code rollback, database restore, and batch correction are separate procedures.
- External effects use durable jobs/outbox-style boundaries rather than occurring inside a database transaction.

### Recovery

- Current and previous immutable releases are retained.
- Failed preflight never receives traffic.
- Failed post-switch health restores the previous compatible pointer.
- ERP database, site configuration, public files, private files, and control-plane data are backed up off host.
- Backup hashes, retention, restore rehearsal, and receiving operator are recorded.
- After users resume work, targeted batch correction is preferred over a restore that would erase new records.

### Security and audit

- Authentication, organization membership, role, document, and API authorization are enforced server-side.
- Cross-company read and mutation tests are mandatory.
- Sensitive actions require confirmation and append-only audit context.
- Logs and artifacts are sanitized; secrets are referenced through approved secret storage rather than persisted in records.
- Known exposed credentials must be rotated before Champion confidential data is received or imported.
- Temporary users, tokens, sessions, synthetic records, sites, jobs, and credentials are removed and counted after release tests.

### Domains and environment independence

- Product names, base URLs, callbacks, cookies, CSRF/CORS, generated links, email links, webhooks, monitoring, and backup references are configurable.
- The final Champion-controlled domain is tested in staging before cutover.
- DNS/TLS cutover has an exact rollback.
- The former implementation hostname remains only for the approved compatibility period and exposes no independent Champion data afterward.

### Monitoring and evidence

- Public root, login, authenticated app, backend health, ERP runtime, app versions, critical routes, jobs, and logs are checked for every release.
- Release artifacts contain exact-candidate browser, authorization, tenant-isolation, mutation, cleanup, and readback evidence appropriate to the phase.
- Monitoring and alert ownership transfers to Champion at handover.

## Codebase changes in the finished system

### Control-plane backend

The backend contains durable domain models and services for:

- organizations, memberships, tenants, subscriptions, implementations, and domains;
- module catalog, bundles, entitlement resolution, application status, and audit;
- versioned onboarding requests, approvals, conversion, and applicant credentials;
- durable provisioning workflows, steps, leases, retries, events, evidence, and compensation;
- release metadata, feature flags, health, and operational summaries;
- migration/import batch controls where implemented in the control plane.

APIs use typed request/response schemas, stable public identifiers, bounded
collections, safe errors, server-side authorization, idempotency, and explicit
state transitions.

### Control-plane frontend

The Next.js application contains:

- the responsive operator shell;
- a reusable accessible component/design-token system;
- API-driven operational pages rather than hardcoded arrays or static milestones;
- public catalog and versioned onboarding screens;
- company, site, implementation, module, onboarding, provisioning, domain, health, audit, and settings views;
- consistent loading, empty, partial-failure, validation, denied, not-found, and error states;
- automated unit/component and candidate-bound browser/accessibility coverage.

### LenERP custom app

`lenerp_core` contains the transferable ERP product layer:

- Champion DocTypes and schema extensions;
- fixtures and patches;
- roles and permission rules;
- workspaces and navigation;
- reports, dashboards, alerts, print formats, and forms;
- branding and approved client configuration;
- integration hooks and versioned ERP verification logic;
- clean-install, migration, export, and package tests.

No required Champion behavior exists only as an undocumented production edit.

### Tests and release automation

The delivered repositories include:

- backend unit/integration and authorization tests;
- frontend unit/component, typecheck, build, browser, responsive, and accessibility tests;
- migration upgrade/recovery tests;
- deterministic failure injection for durable jobs;
- tenant-isolation and negative-permission suites;
- staging, production, rollback, cleanup, backup, and readback scripts;
- secret and dependency scanning;
- reproducible manifests and evidence collection.

## Final handover and independent operation

At `FINAL-P7`, Champion receives or controls:

- production infrastructure and Champion-controlled domain;
- repositories and complete history/tags;
- SSL, backups, monitoring, and service accounts;
- schemas, migrations, dependencies/licenses, tests, configuration templates, and release tooling;
- accepted data exports, mappings, batch records, reconciliations, and exceptions;
- administrator, user, deployment, update, rollback, incident, backup, restore, module, onboarding, provisioning, and migration guides;
- role-based training and administrator/developer demonstrations;
- issue, limitation, advisory, deferred, and warranty registers.

The program is complete when Champion can operate the system independently,
the acceptance authority signs the outcome, and the 30-day contractual defect
warranty intake process is active.

## Pre-kickoff boundary

Before Project Start, the reproducible synthetic demonstration is an evidence
and conversation aid. It does not change the commercial scope, the agreed
`$30,000` price, the `$55/hour` additional-work rate, or the acceptance
criteria. Project Start answers confirm or replace its provisional company,
roles, workflows, accounting, report, branding, and migration assumptions.

No Champion confidential data may enter while credential rotation and data
authorization remain unresolved. The demonstration therefore stays reversible,
uses an explicit seed/reset boundary, and remains `in_development` or
`in_staging` until Champion-specific acceptance is recorded.
