# `lenerp_core`

LenERP Core is the business application layer that elevates Frappe and ERPNext
into a complete, industry-ready ERP platform for drilling, field service,
office operations, people, finance, and commercial workflows.

LenERP is built on top of Frappe and ERPNext. The upstream applications provide
the reliable ERP foundation; `lenerp_core` adds the LenERP business layer,
workflows, permissions, user experience, integrations, and industry-specific
features that turn that foundation into a unified operating system for the
business.
All LenERP-owned DocTypes, hooks, fixtures, patches, roles, workspaces,
reports, print formats, styling, and tests belong here. Upstream Frappe and
ERPNext source trees remain clean, pinned, and upgradeable.

## How LenERP takes Frappe and ERPNext to a new level

LenERP keeps the proven Frappe/ERPNext foundation and expands it into a
connected, role-aware, field-ready ERP. The major updates delivered are:

- **From generic ERP to an industry operating system:** the platform now joins
  the full journey from customer and well/site to quote, drilling or service
  job, crew, materials, completion, invoice, payment, and management reporting.
- **From separate modules to connected operations:** shared workflows,
  permissions, terminology, reports, and document links make Accounting,
  CRM, Sales, Buying, Stock, Assets, HR, Payroll, Projects, Quality, Support,
  and field operations work together.
- **From desktop administration to role-based work:** dedicated experiences
  for office, dispatch, sales, accounting, inventory, field technicians,
  managers, and administrators show each user the work and actions relevant to
  their role.
- **From standard records to real field execution:** well mapping, drilling and
  service jobs, scheduling, crews, rigs, trucks, materials, completion notes,
  maintenance, and operational exceptions are now first-class workflows.
- **From a technical framework to a usable product:** LenERP adds a consistent
  brand, accessible and responsive interfaces, focused workspaces, SSO hooks,
  role profiles, and permission-aware navigation across the ERP.
- **From one-off customization to a scalable product layer:** LenERP-owned
  DocTypes, hooks, reports, workspaces, tests, and migrations are organized in
  a dedicated application so new modules and customer capabilities can be
  added without modifying or destabilizing upstream Frappe and ERPNext.

The result is a broader and more cohesive ERP experience while preserving the
upgrade path to newer Frappe and ERPNext releases.

### Key platform improvements

- **Business-specific workflows:** connects customers, sites and wells, jobs,
  crews, equipment, materials, completion, invoicing, and payment follow-up in
  one operating flow.
- **Drilling and field-service operations:** adds well/site records, drilling
  and service jobs, job statuses, scheduling, priorities, assigned personnel,
  rigs, trucks, completion notes, and material allocation.
- **A clearer role-based experience:** provides LenERP/Champion roles,
  focused workspaces, permission-aware navigation, and access boundaries for
  office, dispatch, sales, accounting, inventory, field, and administrator
  users.
- **Better usability and accessibility:** applies consistent terminology,
  branding, responsive layouts, keyboard support, focus handling, reduced
  motion, and accessible status messaging across desk and public pages.
- **Branding and configuration controls:** adds a safe branding settings
  boundary for company, product, domain, logo, color, and document settings
  without hard-coding customer values into the application.
- **Operations visibility:** adds the Champion ERP workspace and the Champion
  Operations Summary report, with shortcuts for wells, drilling jobs,
  customers, quotes, invoices, and equipment.
- **Safer delivery and maintenance:** includes install/migration hooks, SSO
  integration points, opt-in synthetic demo data, permission checks, contract
  tests, and a versioned application boundary so upstream updates can be
  applied without losing LenERP customizations.

## Complete module improvement and new LenERP capabilities

LenERP improves every module used in the operating model—not only the drilling
features. Improvements include common navigation and terminology, role-based
access, consistent workflows, cross-module links, accessible screens,
operational reports, and integration with the LenERP customer-to-job lifecycle.

In addition to the standard Frappe and ERPNext foundation, LenERP adds or
integrates the following capabilities:

- **HR and people operations:** employee-facing workflows, time off,
  timesheets, role-aware office work, and confidential people data.
- **Payroll:** payroll preparation and payroll-related workflows with
  restricted access for authorized users.
- **Drilling and field service:** well mapping, well/site management, drilling
  jobs, service calls, pump installation, water testing, maintenance,
  dispatch, field execution, and job completion.
- **Accounting and finance:** quotations, sales invoices, payments,
  receivables, accounting controls, and the commercial flow from completed work
  to payment.
- **CRM and sales:** customer and contact management, leads and opportunities,
  quoting, follow-up, and links from commercial activity to operational jobs.
- **Buying, inventory, and purchasing:** items, units, warehouses, receiving,
  transfers, job material usage, purchasing, low-stock visibility, and traceable
  stock movements.
- **Assets and maintenance:** rigs, trucks, equipment, assignments, asset
  status, maintenance history, and field-resource availability.
- **Projects, quality, and support:** office task coordination, quality and
  callback workflows, support issues, product-change requests, and operational
  handoffs.
- **Manufacturing and related ERP modules:** improved navigation, permissions,
  reporting, terminology, and integration patterns where those modules are
  enabled for a LenERP deployment.

The result is a unified LenERP experience rather than a collection of isolated
ERP screens. Standard ERPNext documents remain available, while LenERP adds the
industry context and controls needed to run the business day to day.

### Current app-owned implementation

The current app includes these LenERP-owned building blocks:

- `LenERP Branding Settings` for controlled company and product configuration;
- `LenERP Well Site` for well/site identity, location, equipment notes, and
  operational context;
- `LenERP Drilling Job` for drilling and service work, scheduling, assignment,
  status, completion, and materials;
- `LenERP Job Material` for item, quantity, unit, and warehouse allocation;
- the `Champion ERP` workspace;
- the `Champion Operations Summary` report;
- accessibility, SSO, install, migration, demo-seed, and permission-supporting
  application hooks.

Some capabilities are implemented directly in this app, while others are
configured or integrated from ERPNext and HRMS. The intended contract is that
LenERP-owned changes live here, so the platform can grow without forking or
destabilizing the upstream Frappe/ERPNext applications.

## Drilling, wells, and field operations

Drilling is a first-class LenERP operating area rather than a collection of
generic ERP records. The application connects the customer, well, job, crew,
equipment, materials, completion, and commercial records that teams need to
run field work from the office through the job site.

### Well and site management

`LenERP Well Site` is the canonical operational record for a customer-owned
well or service location. It includes:

- a unique well/site identifier and site name;
- customer and primary contact links;
- active, needs-review, and inactive status;
- street address, city, region, postal code, latitude, and longitude;
- measured depth in meters;
- pump and equipment specifications;
- operational notes and searchable site context.

Validation prevents invalid latitude/longitude values and negative well depth.
The well/site record is the anchor for current and historical drilling and
service jobs, equipment assignments, materials, notes, and reports.

### Drilling and service jobs

`LenERP Drilling Job` models the work performed for a customer and well/site.
It supports:

- automatic `JOB-####` job references;
- new well drilling, pump installation, service calls, water testing, and
  maintenance job types;
- planned, scheduled, in-progress, completed, and reopened states;
- scheduled date, priority, assigned crew/personnel, rig, and truck;
- work notes, completion details, and completion date;
- links to allocated materials through `LenERP Job Material`;
- change tracking and permission-scoped access for office, dispatch, and field
  roles.

The standard job workflow is:

```text
Planned → Scheduled → In Progress → Completed
                                      ↓
                                   Reopened
```

Dispatch schedules the work, field personnel start and execute it, and
completion requires completion details. A completion date cannot be earlier
than the scheduled date. Dispatch can reopen a completed job when follow-up
work is required.

### Job materials, equipment, and completion

`LenERP Job Material` is the child table that connects a job to the ERPNext
item, unit of measure, and warehouse model. This gives field work a traceable
material path instead of free-text material notes. The job can also reference
ERPNext `Asset` records for drilling rigs, trucks, and other equipment.

The generated `Champion Job Completion` print format brings the job reference,
job type, status, schedule, customer, well/site, crew, work notes, and
completion details into one printable record for office and field handoff.

### Operations reporting

The `Champion Operations Summary` report provides an operational view of demo
and staged drilling jobs, including:

- job reference;
- customer;
- well/site;
- job type;
- status;
- scheduled date;
- priority.

The `Champion ERP` workspace exposes direct shortcuts for Well Sites, Drilling
Jobs, the Operations Summary, Customers, Quotes, Invoices, and Equipment.

## End-to-end LenERP business flow

LenERP turns the standard ERPNext documents into a connected process:

```text
Lead / customer
  → Contact and well/site
  → Quote and approval
  → Drilling or service job
  → Crew, rig, truck, and materials
  → Field execution and completion
  → Invoice and payment
  → Inventory, asset, maintenance, and management reporting
```

The same operating model extends to office work, HR, payroll, support,
quality, projects, and future module bundles. This is how LenERP scales the
ERPNext foundation: each module keeps its standard ERPNext records while
sharing LenERP roles, workflows, terminology, customer context, reporting,
and audit expectations.

## Module-by-module improvements

The LenERP product layer improves every module used by the business. The table
below summarizes the added business value on top of the corresponding Frappe,
ERPNext, and HRMS capabilities.

| Module area | LenERP improvements |
| --- | --- |
| **CRM and customers** | Customer and contact context, leads, opportunities, follow-up, and links from commercial activity to wells and jobs. |
| **Selling and quoting** | Quotes, approvals, customer work requests, job context, and handoff into invoicing and payment. |
| **Accounting and finance** | Invoice readiness, payment state, receivables, accounting permissions, commercial traceability, and management visibility. |
| **Buying and purchasing** | Suppliers, purchasing requests, receipts, item availability, and purchasing connected to field demand. |
| **Stock and inventory** | Items, units, warehouses, receiving, transfers, job issue/usage, low-stock exceptions, and traceable stock movements. |
| **Assets and maintenance** | Rigs, trucks, equipment, assignment, availability, maintenance schedules, service history, and field-resource status. |
| **HR and people** | Employee workflows, office work, time off, timesheets, confidentiality, manager access, and role-aware people operations. |
| **Payroll** | Payroll preparation, payroll-related workflows, controlled visibility, and integration with people and accounting processes. |
| **Drilling and field service** | Well mapping, well/site records, drilling jobs, service calls, scheduling, crews, equipment, materials, completion, and reopen handling. |
| **Projects and office work** | Task coordination, implementation handoffs, ownership, deadlines, blockers, and operational follow-up. |
| **Quality and support** | Quality classifications, callback and rework handling, support issues, product-change requests, and escalation context. |
| **Manufacturing and related ERP modules** | Shared LenERP navigation, permissions, terminology, reporting, and integration patterns when enabled for a deployment. |
| **Reports and dashboards** | Business-facing reports that combine jobs, wells, inventory, assets, maintenance, sales, finance, and operational exceptions. |
| **User experience** | Focused workspaces, responsive layouts, accessible controls, keyboard support, clear statuses, and permission-aware navigation. |

This approach means a company can start with the core drilling flow and expand
into finance, inventory, HR, payroll, support, quality, projects, and other
ERPNext modules without changing the underlying operating language or user
experience.

## Roles, permissions, and sign-in

LenERP adds role profiles that map the platform to real responsibilities:

- **Champion Administrator:** full operational configuration and administration;
- **Champion Dispatcher:** customer, well, scheduling, job, and dispatch work;
- **Champion Sales User:** customers, leads, opportunities, quotes, and sales;
- **Champion Accounting User:** customers, invoices, payments, and finance;
- **Champion Inventory Manager:** items, suppliers, warehouses, stock, and
  equipment;
- **Champion Field Technician:** assigned field work, assets, maintenance, and
  execution context;
- **Champion Platform Operator:** restricted platform operations where enabled.

The app creates and maintains the role set, prepares the drilling workflow,
and applies least-privilege permissions to standard ERPNext documents. The
SSO integration supports a central LenERP sign-in flow, safe authorization-code
exchange, role-profile mapping, just-in-time ERP user provisioning when
enabled, and protection for the break-glass administrator account.

## Accessibility and product experience

LenERP improves the ERPNext interface at the application layer so the same
experience is available on authenticated desk pages and public pages. The
included assets and templates provide:

- responsive viewport behavior for desktop, tablet, and mobile;
- semantic main content and heading structure;
- accessible labels for images, logos, and controls;
- keyboard navigation and visible focus behavior;
- reduced-motion support;
- accessible status messaging and form interactions;
- consistent LenERP branding and public-page shell behavior.

These improvements are applied through LenERP-owned hooks and assets, keeping
the upstream Frappe and ERPNext source trees untouched.

## Synthetic demonstration and verification

The opt-in demo seed builds a complete synthetic business scenario without
reading external files or credentials. It can create and reconcile:

- a company, fiscal year, address, customer, and contacts;
- three well/site records and four drilling jobs;
- leads, opportunities, suppliers, items, and price lists;
- quotation, sales invoice, payment entry, and purchase receipt;
- warehouses, stock issue, rig and truck assets, and maintenance tasks;
- supporting accounts, cost centers, groups, units, and locations.

Demo data is clearly prefixed with `DEMO-CHAMPION-`, is never created by a
normal install or migration, and can be inspected or reset by explicit bench
commands. Reset operations are scoped to synthetic records and do not delete
customer data.

The test suite covers the C01 configuration contract, persisted LenERP
DocTypes, drilling workflow metadata, demo seed boundaries, permissions, SSO
contracts, accessibility assets, and public/authenticated shell behavior.

## Configuration and branding foundation

The `0.2.0` implementation adds the value-free company and product
configuration layer (`LenERP Branding Settings`). It stores no default
customer values and does not change ERPNext branding until the approved
company, product, asset, domain, and ownership decisions are recorded. The
package release identity is `CHAMP-C01-R1`; release acceptance still requires
those inputs, clean staging installation/migration, browser/print evidence,
and Champion acceptance.

The settings document is intentionally restricted to System Manager. It
provides LenERP-specific configuration while continuing to use the standard
ERPNext Company, System Settings, Website Settings, and approved domain
cutover processes where appropriate.

## Release and deployment status

The local repository contains no Champion data, secrets, or brand assets.
The private remote destination is intentionally not configured until the
approved GitHub organization/account is recorded. Install, migrate, list, and
uninstall must be run on a disposable Frappe v15 bench before this app can be
treated as release-ready.

## Planned verification

```bash
bench --site <disposable-site> install-app lenerp_core
bench --site <disposable-site> migrate
bench --site <disposable-site> list-apps
bench --site <disposable-site> uninstall-app lenerp_core --yes
```

Do not place passwords, API keys, private keys, tokens, or Champion records in
this repository.

## Phase 04 role-based workspace

Version `0.3.0` adds the version-controlled Champion role/home registry and
the `/champion-home` presentation route. It is server-controlled and remains
off unless the ERP site configuration explicitly sets
`lenerp_phase4_workspace_enabled=1`. An optional JSON object in
`lenerp_phase4_role_rollout` enables named roles independently, for example
`{"Champion Dispatcher": true}`. With the flag off, the existing
`Champion ERP` Workspace remains the rollback surface.

The home API reads authorized ERPNext/HRMS records in place. It does not copy
operational records into LenERP or create a second task, employee, payroll, or
inventory system. Missing optional applications are rendered as
`Pending configuration`.
