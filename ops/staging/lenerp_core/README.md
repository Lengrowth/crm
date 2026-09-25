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

## LenERP product

LenERP is a complete operating system for a field-service and drilling company.
It covers the entire business, including the accounting, operational,
administrative, people, and customer-facing sides of an ERP:

```text
Customer and contact
  → Well / site and location
  → Request, opportunity, or quotation
  → Drilling or service job
  → Schedule, crew, rig, truck, and materials
  → Field execution and required capture
  → Completion review and approval
  → Invoice, payment, and accounting context
  → Inventory, maintenance, dashboards, alerts, and history
```

Every step preserves the relationships created earlier in the process. A
customer is not disconnected from its wells. A job is not disconnected from
the quote that created it. Materials and equipment are not free-text notes.
Completion is not merely a status change. It becomes the source for office
review, invoice readiness, asset history, reporting, and future service work.

This is the level at which LenERP scales Frappe and ERPNext: the standard ERP
modules remain the system of record, while LenERP supplies the operating model
that joins them into one product.

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

## Detailed field-job operating model

The field-job experience is built around a single chain of responsibility. The
office, dispatcher, salesperson, accountant, inventory manager, and field
technician work from the same customer, site, and job records, with different
permissions and views.

### 1. Customer and work intake

The process begins with a lead, customer, contact, service request, or new
well request. The intake record can carry:

- customer identity and contacts;
- requested service or drilling type;
- requested well/site or a new-site requirement;
- location and access information;
- supporting notes, documents, photos, and communication history;
- commercial owner and follow-up status.

Sales and office users can convert an opportunity into a quotation or an
approved work request. The operational job retains the commercial context so
the field team knows what work was requested and the accounting team can trace
what was completed.

### 2. Well and site preparation

Before work is scheduled, the customer is linked to a canonical `LenERP Well
Site` record. The site record is designed to hold the durable identity and
history of the location rather than duplicating site data on every job.

The well/site experience includes:

- a unique approved well/site identifier;
- site name and customer ownership;
- primary contact and communication details;
- address, city, state/region, postal code, latitude, and longitude;
- well depth and pump/equipment specifications;
- active, needs-review, and inactive operating states;
- current job, historical jobs, assigned equipment, materials, documents, and
  activity history;
- list and map views with search, filters, status markers, and navigation to
  the canonical site record;
- role-scoped exports, print outputs, and linked job history.

The map distinguishes stored site coordinates from live GPS or live tracking.
LenERP does not imply that a technician is being tracked merely because a
well has latitude and longitude. Live tracking, photos, signatures, and other
field capture are enabled only when the approved operating rules support them.

### 3. Job creation and planning

`LenERP Drilling Job` is the operational work order for a customer and
well/site. It is intended to answer five questions immediately:

1. What customer and site are we serving?
2. What type of work is required?
3. When is it scheduled and what is its priority?
4. Who and what are assigned to complete it?
5. What evidence is required before the work can be closed?

The job record includes:

- automatic job reference, for example `JOB-0001`;
- customer and `LenERP Well Site` links;
- new well drilling, pump installation, service call, water testing, and
  maintenance job types;
- planned, scheduled, in-progress, completed, and reopened states;
- scheduled date and priority, including routine, high, and emergency work;
- assigned crew or personnel;
- assigned drilling rig, truck, or other ERPNext assets;
- instructions, work notes, exception notes, and completion details;
- materials allocated to the work;
- completed date, change history, print output, and related commercial
  context.

The job is not considered complete merely because a user selects `Completed`.
LenERP requires completion details and rejects a completion date that precedes
the scheduled date. Additional approved rules can be added without changing
the core customer/site/job relationship.

### 4. Dispatch and assignment

Dispatch is the coordination layer between office planning and field
execution. The dispatch view is designed to expose:

- jobs waiting to be scheduled;
- scheduled work by date and priority;
- unassigned jobs and crew conflicts;
- jobs missing a rig, truck, material, or required information;
- overdue, blocked, emergency, and reopened jobs;
- current field work and expected completion;
- customer, well/site, and location context before assignment.

The dispatcher assigns the right crew and equipment while preserving the
history of the decision. Field technicians see their assigned work and the
information needed to execute it; they do not need unrestricted access to
accounting, payroll, or unrelated customer records.

### 5. Field execution

The field experience is mobile-first and task-oriented. A technician should be
able to open today’s work, confirm the customer and well, understand the job,
record the work, report an exception, and submit completion without navigating
through unrelated ERP screens.

The field execution flow includes:

- today’s assigned jobs and clear job priority;
- customer, well/site, address, map, and directions context;
- start or check-in action;
- job instructions and required checklist;
- work notes and structured field capture;
- photos, forms, signatures, and supporting documents;
- materials used and stock issue context;
- rig, truck, and equipment confirmation;
- blocker, safety, quality, or customer exception reporting;
- save/submitted state that is visible to the technician;
- complete or submit-for-review action;
- clear offline/sync behavior if an offline field experience is approved.

The interface uses large reachable controls, readable status text, and clear
error recovery instead of forcing field staff to use dense accounting tables.

### 6. Job completion and office review

Completion closes the operational loop but does not hide the evidence needed by
the office. The completion record includes the job, customer, well/site, dates,
crew, equipment, materials, work notes, completion details, and any approved
photos, forms, or signatures.

The office or dispatcher can review the submitted work, reopen it when follow-
up is required, and release it for invoice-ready processing according to the
approved business rules. The same completion event becomes part of the
well/site history, customer history, asset history, dashboards, alerts, and
future maintenance planning.

### 7. Job history and reporting

Users can see the current state and historical story of work without merging
records manually. The history includes:

- job state transitions and responsible users;
- schedule and assignment changes;
- materials issued or consumed;
- equipment and asset assignment;
- field notes and completion evidence;
- reopened work and follow-up reasons;
- quote, invoice, and payment references where authorized;
- report/export timestamps and permission scope.

This makes the well/site a durable operational history, not just a pin on a
map, and makes the job a traceable business event, not just a task card.

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

The broader dashboard and reporting experience includes persisted,
permission-aware operational outputs for:

- active and historical well/job activity;
- unassigned, overdue, blocked, emergency, and reopened work;
- inventory exceptions and low-stock demand;
- asset availability and maintenance status;
- field completion and invoice-ready exceptions;
- customer, sales, quote, invoice, and payment summaries;
- operational alerts with source, audience, timestamp, and next action.

Every report and dashboard is expected to state its source, filters, period,
as-of time, freshness, calculation rules, permission scope, and export/print
behavior. This keeps management visibility useful without presenting synthetic
or unverified values as production KPIs.

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
quality, projects, and additional module bundles. This is how LenERP scales the
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
| **Manufacturing and related ERP modules** | Shared LenERP navigation, permissions, terminology, reporting, and integration patterns across deployments. |
| **Reports and dashboards** | Business-facing reports that combine jobs, wells, inventory, assets, maintenance, sales, finance, and operational exceptions. |
| **User experience** | Focused workspaces, responsive layouts, accessible controls, keyboard support, clear statuses, and permission-aware navigation. |

### LenERP solution package map

The complete product is organized into modular solution packages. This keeps
the platform extensible while still delivering one connected ERP:

| Package | Product area | Finished-product outcome |
| --- | --- | --- |
| **C01** | Company, product, and branding | Configurable legal/operating identity, timezone, currency, fiscal year, product name, approved assets, document branding, and domain readiness. |
| **C02** | Users, roles, permissions, and approvals | Role-specific workspaces, confidential-data boundaries, approval limits, direct-route/API denial, linked-record security, and cross-company isolation. |
| **C03** | Module profile and navigation | One authoritative module catalog, bundles such as Champion Drilling and Generic Field Service, dependency rules, role/workspace defaults, and visible requested/entitled/applied/verified states. |
| **C04** | Customer, Site/Well, and Well Mapping | Canonical customer-owned wells/sites, identifiers, location validation, list/map views, duplicate handling, documents, search, exports, and linked job history. |
| **C05** | Drilling and service jobs | Customer-to-site-to-job workflow, scheduling, assignment, field capture, materials, completion review, invoice-ready event, reopen handling, and print output. |
| **C06** | Inventory, purchasing, trucks, rigs, and assets | Traceable receive/transfer/issue/adjustment flow, warehouse and item control, low-stock exceptions, rig/truck assignment, asset history, and maintenance planning. |
| **C07** | CRM, quoting, invoicing, payments, and accounting | Lead-to-opportunity-to-customer flow, quote approval, job linkage, approved completion to invoice, payment reconciliation, accounting context, and permission-controlled financial data. |
| **C08** | Dashboards, reports, alerts, forms, and print | Source-backed KPIs, well/job history, inventory exceptions, asset and maintenance status, operational alerts, forms, signatures/photos, exports, and branded print outputs. |
| **C09** | Office work, people, payroll, quality, and support | Office task board, employees, time off, timesheets, payroll preview, confidential HR data, callback/rework classification, support issues, and product-change requests. |

This approach means a company can start with the core drilling flow and expand
into finance, inventory, HR, payroll, support, quality, projects, and other
ERPNext modules without changing the underlying operating language or user
experience.

## Office, people, payroll, quality, and support

LenERP is not limited to field operations. The back office uses the same role
and workflow model for the work that makes field service possible:

- **Office work:** tasks have owners, managers, due dates, states, blockers,
  dependencies, and handoffs instead of living in disconnected notes or email.
- **People operations:** employees, time off, timesheets, manager visibility,
  and office responsibilities are available through role-appropriate
  workspaces.
- **Payroll:** payroll preparation and previews connect approved people and
  time data with restricted payroll visibility. Tax, deduction, bonus, and
  approval rules remain configurable rather than being invented by a generic
  demo.
- **Quality and callbacks:** a quality concern, callback, rework request, or
  field exception retains its customer, site, job, asset, and responsible-user
  context.
- **Support:** support issues and product-change requests have routing,
  ownership, status, history, and escalation context.

Confidential HR and payroll information is never treated as ordinary module
data. Direct routes, searches, reports, exports, and linked records follow the
approved role and confidentiality matrix.

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

## Configuration and branding

`LenERP Branding Settings` provides the product-level configuration used to
adapt ERPNext to each LenERP business. System Managers can configure legal and
operating names, timezone, currency, fiscal year, address, contact details,
product name, brand mode, logo, favicon, colors, document footer, final domain,
and domain ownership information.

The settings are kept in a dedicated LenERP record and work alongside the
standard ERPNext Company, System Settings, Website Settings, and domain
configuration. This keeps branding and product configuration consistent across
the ERP workspace, public pages, print formats, and customer documents.

## Application foundation

The `lenerp_core` application contains the product layer that makes these
workflows reusable across LenERP deployments:

- app-owned DocTypes, child tables, workflows, permissions, and role profiles;
- customer, well/site, drilling-job, material, asset, and report integrations;
- install and migration hooks that create the required workflow and permission
  metadata;
- central sign-in integration and role-profile mapping;
- accessible public and authenticated page templates and JavaScript assets;
- synthetic business data for demonstrations and repeatable verification;
- print formats, reports, dashboards, alerts, and operational summaries;
- contract tests for data models, permissions, accessibility, and integrations.

The application is deliberately additive. Standard Frappe and ERPNext records
remain available, and LenERP connects them through its own product layer so
upgrades and new module capabilities can be introduced without rewriting the
upstream applications.

## Installation

```bash
bench --site <disposable-site> install-app lenerp_core
bench --site <disposable-site> migrate
bench --site <disposable-site> list-apps
bench --site <disposable-site> uninstall-app lenerp_core --yes
```

Do not place passwords, API keys, private keys, tokens, or Champion records in
this repository.
