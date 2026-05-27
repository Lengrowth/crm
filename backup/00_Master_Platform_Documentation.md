# Master CRM + Field Operations Platform Documentation

**Document type:** Master product, architecture, and delivery specification
**Format:** Markdown
**Status:** Expanded working draft
**Prepared for:** Product, engineering, design, implementation, QA, and rollout planning
**Primary system:** Multi-company SaaS CRM + outbound sales + drilling field operations + logistics + warehouse + fleet platform
**Source basis:** Expanded from the original master platform design spec provided by the product owner.

---

## 0. How To Use This Document

- Use this document as the master baseline before creating detailed phase documents.
- Use the phase sections as the table of contents for future design, requirements, engineering, QA, and rollout documents.
- Treat every requirement marked **MVP** as part of the first usable operational release unless explicitly deferred.
- Treat every requirement marked **Later** as intentionally supported by the architecture but not required in the first release.
- When scope conflicts arise, prioritize tenant safety, reliable workflows, auditability, and mobile data capture over visual polish.
- Do not design CRM, dispatch, inventory, and tracking as disconnected products; they must share account, activity, task, and audit foundations.
- Use this master document to align stakeholders before drilling down into phase-level UX, data model, API, and acceptance criteria.

## 1. Executive Product Summary

- The platform is a modular multi-company SaaS operating system for companies that sell, dispatch, track, deliver, service, and report on field work.
- The first target operating model combines outbound sales, field sales, drilling operations, inventory, depots, warehouses, trucks, crews, service jobs, and accounting sync.
- The system must support office users on desktop, field users on mobile, and managers who need cross-module visibility.
- The product should feel like one unified platform rather than separate CRM, warehouse, and dispatch tools stitched together.
- The platform must support optional modules per company so one customer can use only CRM while another uses CRM, inventory, dispatch, fleet, and QuickBooks.
- The product must be designed for long-term expansion into enterprise permissions, route optimization, barcode scanning, advanced reporting, and integration marketplace capabilities.

### 1.1 Primary Product Promise

- Give management a single source of truth for what was sold, what was promised, what is scheduled, what is being delivered, where field resources are, what inventory is available, and what must be invoiced.
- Give sales teams structured outbound tools without losing human relationship context.
- Give field teams fast mobile workflows that work in weak connectivity environments.
- Give dispatch and operations teams live visibility into vehicles, drivers, crews, stops, delays, site work, and completion proof.
- Give warehouse teams accurate stock movement, transfer, picking, receiving, depot, and inventory history workflows.
- Give finance and administration reliable sync visibility, especially for QuickBooks.

### 1.2 Success Definition

- A manager can answer who owns an account, what was promised, what work is scheduled, where the crew is, what inventory is assigned, and whether the job is ready for billing without using spreadsheets.
- A field user can view assigned work, check in, add notes, upload photos, complete tasks, and sync later if offline.
- A dispatcher can assign jobs, vehicles, drivers, equipment, routes, stops, and monitor exceptions from one operational workspace.
- A warehouse operator can receive, adjust, pick, transfer, and load stock while preserving audit history.
- A sales rep can import leads, follow cadences, log calls, SMS, email, LinkedIn activity, appointments, site visits, and follow-ups.
- An admin can enable modules, manage roles, configure custom fields, review audit logs, and monitor integrations.

## 2. Product Vision

- The platform should become the operational backbone for companies that combine sales, field execution, logistics, inventory, and service workflows.
- The system must support a sales-first workflow where outbound teams generate pipeline and a delivery-first workflow where field operations fulfill customer commitments.
- The product should reduce dependency on disconnected spreadsheets, phone calls, manual checklists, and ad hoc messaging.
- Every important operational event should produce searchable, reportable, permission-aware history.
- Every module should contribute to a shared activity timeline and reporting model.

### 2.1 North Star Outcomes

- Increase revenue conversion by improving outbound follow-up discipline and visibility.
- Reduce operational delays by connecting sales promises to dispatch, warehouse, and field execution.
- Reduce inventory uncertainty by recording movements across warehouses, depots, trucks, and job sites.
- Improve customer trust by capturing proof, status, photos, arrival events, check-ins, and completion records.
- Improve management visibility with dashboards that are designed from day one rather than added after launch.

## 3. Guiding Principles

| Principle | Meaning |
| --- | --- |
| Multi-tenant first | Every record must belong to a tenant and normally a company. Tenant isolation is a product, security, and architecture requirement. |
| Modular but unified | Modules can be enabled independently, but shared entities and timelines must remain consistent. |
| Desktop operators, mobile field teams | Complex planning and review happen on desktop; capture and execution happen on mobile. |
| Audit everything important | Operational actions, permissions, inventory movements, dispatch changes, and sync events must be traceable. |
| Offline-friendly by default | Field users must not lose work when connectivity drops. |
| Reporting-aware data design | Important states, timestamps, owners, and rollups must be stored deliberately. |
| Real-time where valuable | Live maps, dispatch status, alerts, and collaboration benefit from real-time updates; other areas can use eventual consistency. |
| Clear extension seams | Integrations, modules, custom fields, webhooks, and permissions must be extensible without rewriting core workflows. |
| Operational simplicity | The first release should avoid over-automating workflows that users still need to control manually. |
| No silent failure | Sync failures, offline conflicts, GPS permission issues, and data validation errors must be visible and recoverable. |

## 4. Confirmed Assumptions

- The product is one core system with optional modules.
- The product is a multi-company SaaS platform.
- The first strong vertical focus is outbound sales and field sales for drilling-related operations.
- Outbound channels include phone, email, SMS, WhatsApp where enabled, and LinkedIn activity logging.
- Inventory and warehouse management are required platform domains.
- QuickBooks is the first accounting integration and must not be treated as an afterthought.
- Multiple warehouses, multiple truck depots, and multiple field operating locations must be supported.
- Geofencing and check-ins are required.
- Permissions are company-scoped first, with deeper segmentation supported later.
- Basic offline mobile support is required for field workflows.
- The preferred backend stack is Python, FastAPI, MongoDB, Redis where needed, and workers for async jobs.
- The preferred frontend stack is Next.js, Tailwind CSS, and shadcn/ui.

## 5. Scope Boundaries

### 5.1 In Scope For The Platform

- Tenant and company administration.
- User, team, role, membership, and permission management.
- CRM accounts, contacts, leads, opportunities, pipelines, and activities.
- Outbound campaign, sequence, call, email, SMS, WhatsApp, and LinkedIn logging workflows.
- Field visits, site records, job requests, check-ins, photos, notes, and assignment workflows.
- Warehouse, depot, product catalog, stock movement, receiving, picking, transfers, and adjustments.
- Orders, shipments, dispatching, routes, stops, proof of delivery, and exceptions.
- Vehicles, drivers, tracking devices, GPS pings, geofences, route replay, and alerts.
- Service requests, work orders, maintenance, parts, labor, and service history.
- Calendar, task, recurring work, reminders, and SLA workflows.
- Reporting dashboards and custom report foundations.
- QuickBooks integration foundation and sync monitoring.
- Open REST API, webhooks, import/export jobs, and integration connections.

### 5.2 Out Of Scope For First MVP Unless Reprioritized

- Full route optimization engine with advanced constraints.
- AI-generated dispatch planning.
- Full LinkedIn automation that performs actions inside LinkedIn automatically.
- Advanced warehouse robotics, automated conveyor integration, or WMS-grade wave planning.
- Full accounting ledger replacement.
- Complex payroll processing.
- Native ELD compliance unless explicitly required.
- Advanced IoT telemetry beyond basic device location, health, and last-seen status.
- Enterprise SSO for MVP unless required by an early customer.
- Customer-facing portal unless included in a later phase.

## 6. Product Modules

| Module | Primary Responsibility |
| --- | --- |
| Core Platform | Tenancy, users, teams, permissions, audit logs, notifications, files, custom fields, tags, search, import/export, settings. |
| CRM | Accounts, contacts, leads, opportunities, pipelines, activity timelines, notes, ownership, relationship mapping. |
| Outbound Sales | Lists, campaigns, cadences, sequences, calling, emails, SMS, LinkedIn logging, appointment scheduling, rep performance. |
| Field Sales / Drilling | Site records, visits, check-ins, job requests, quotes, photos, notes, crews, equipment, territories. |
| Calendar / Tasks | Appointments, tasks, recurring tasks, reminders, SLA due dates, team calendars, assignment rules. |
| Inventory / Warehouse | Products, warehouses, depots, bins, stock units, receiving, picking, adjustments, transfers, low-stock alerts. |
| Orders / Dispatch / Logistics | Orders, jobs, shipments, route plans, stops, exceptions, handoffs, proof of delivery. |
| Fleet / GPS / Geofencing | Vehicles, drivers, devices, live map, location history, geofences, check-in events, route replay, alerts. |
| Service / Work Orders | Service requests, work orders, maintenance schedules, parts used, labor tracking, service history. |
| Reporting / Analytics | Sales, outreach, field, fleet, inventory, delivery, service, team productivity, and custom reports. |
| Integrations | QuickBooks, email, SMS, WhatsApp, LinkedIn logging, REST API, webhooks, CSV, Excel import/export. |

## 7. Detailed Module Requirements

### 7.1 Core Platform Module

- **REQ-01-001:** Tenant records must define the highest isolation boundary.
- **REQ-01-002:** Company records must define customer organizations inside the tenant structure.
- **REQ-01-003:** Users may belong to one or more companies when allowed by tenant configuration.
- **REQ-01-004:** Membership records must store company, role, team, status, and effective permissions.
- **REQ-01-005:** Feature flags must enable or disable modules per company.
- **REQ-01-006:** Audit logs must record administrative and operational changes.
- **REQ-01-007:** Notification preferences must be configurable by user and company.
- **REQ-01-008:** Files and attachments must support record-level association and access checks.
- **REQ-01-009:** Tags must be configurable per company and usable across major entities.
- **REQ-01-010:** Custom fields must support type, validation, visibility, and module scope.
- **REQ-01-011:** Global search must respect company, role, module, and record permissions.
- **REQ-01-012:** Import/export jobs must be asynchronous for large files.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.2 CRM Module

- **REQ-02-001:** Accounts must represent customer companies, prospects, vendors where enabled, and operational entities where appropriate.
- **REQ-02-002:** Contacts must support multiple emails, phones, roles, influence level, and relationship context.
- **REQ-02-003:** Leads must support source, status, owner, assignment, score, and qualification workflow.
- **REQ-02-004:** Opportunities must support pipeline, stage, value, close date, probability, owner, products, and next action.
- **REQ-02-005:** Activities must include calls, emails, SMS, meetings, LinkedIn logs, notes, site visits, tasks, status changes, and system events.
- **REQ-02-006:** Account timelines must show CRM and field activity together when permissions allow.
- **REQ-02-007:** Duplicate detection should exist for accounts, contacts, and leads.
- **REQ-02-008:** Ownership and team visibility must be reportable.
- **REQ-02-009:** Pipelines must be configurable by company.
- **REQ-02-010:** CRM views must include list, table, detail, kanban, timeline, and map where location exists.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.3 Outbound Sales Module

- **REQ-03-001:** Prospect lists must support imports, segmentation, ownership, source, and compliance metadata.
- **REQ-03-002:** Campaigns must define target audience, channels, cadence steps, owners, start/end dates, and success metrics.
- **REQ-03-003:** Sequences must support manual tasks and logged activity even if automated sending is deferred.
- **REQ-03-004:** Call tasks must support disposition, outcome, next step, callback date, and voicemail flag.
- **REQ-03-005:** Email logs must store subject, direction, timestamp, participants, result, and thread reference where available.
- **REQ-03-006:** SMS logs must store direction, status, phone number, linked record, and compliance status where relevant.
- **REQ-03-007:** LinkedIn logging must capture connection request, message sent, profile viewed, comment, note, and manual follow-up.
- **REQ-03-008:** Follow-up queues must prioritize overdue, due today, high-value, and recently engaged prospects.
- **REQ-03-009:** Rep performance must be measurable by activities, conversions, meetings, opportunities created, and revenue influenced.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.4 Field Sales / Drilling Module

- **REQ-04-001:** Sites must store customer, location, coordinates, access notes, contact, hazards, equipment needs, and site status.
- **REQ-04-002:** Site visits must support scheduled, in-progress, completed, missed, cancelled, and needs-follow-up states.
- **REQ-04-003:** Check-ins must capture user, timestamp, coordinates, device, geofence status, and offline sync metadata.
- **REQ-04-004:** Field notes must support text, photos, attachments, categories, follow-up tasks, and visibility controls.
- **REQ-04-005:** Job requests must capture scope, requested date, priority, site constraints, required equipment, and customer commitments.
- **REQ-04-006:** Crew assignments must connect workers, vehicles, equipment, and scheduled windows.
- **REQ-04-007:** Territory coverage must allow sales managers to see visit density and account coverage.
- **REQ-04-008:** Drilling-specific data must remain extensible through custom fields before hardcoding niche attributes.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.5 Inventory / Warehouse Module

- **REQ-05-001:** Products must support SKU, name, category, unit of measure, active status, accounting reference, and reorder rules.
- **REQ-05-002:** Warehouses and depots must be modeled as inventory locations with type and hierarchy.
- **REQ-05-003:** Bin locations must support aisle, rack, shelf, zone, and barcode later.
- **REQ-05-004:** Stock balances must be queryable by product, location, bin, lot, serial, reserved, available, and committed quantities.
- **REQ-05-005:** Receiving workflows must capture supplier, purchase reference, quantities, condition, receiving user, and timestamp.
- **REQ-05-006:** Picking workflows must reserve stock before shipment, job, or truck load where applicable.
- **REQ-05-007:** Transfers must support source, destination, in-transit status, confirmation, discrepancy, and audit trail.
- **REQ-05-008:** Adjustments must require reason codes and permissions.
- **REQ-05-009:** Low-stock alerts must support thresholds per location.
- **REQ-05-010:** Stock movement history must be append-only and reportable.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.6 Orders / Dispatch / Logistics Module

- **REQ-06-001:** Orders must connect customer, account, site, products, services, delivery windows, and billing state.
- **REQ-06-002:** Shipments must connect orders, stops, vehicles, drivers, inventory, and proof of delivery.
- **REQ-06-003:** Dispatch boards must support unassigned, assigned, in progress, delayed, completed, exception, and cancelled work.
- **REQ-06-004:** Routes must support ordered stops, planned times, actual times, distance estimates, and manual resequencing.
- **REQ-06-005:** Stops must support arrival, departure, check-in, check-out, signature/photo proof, and exception notes.
- **REQ-06-006:** Exception management must cover delay, customer unavailable, inventory missing, vehicle issue, weather, site blocked, and safety issue.
- **REQ-06-007:** Handoffs between warehouse and truck must be auditable.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.7 Fleet / GPS / Geofencing Module

- **REQ-07-001:** Vehicles must support type, plate, VIN where applicable, depot, capacity, status, assigned driver, and maintenance status.
- **REQ-07-002:** Drivers must link to user profiles but may also exist as operational resources before full user accounts are created.
- **REQ-07-003:** Devices must support identifier, source, assigned vehicle or person, status, battery where available, and last seen.
- **REQ-07-004:** Location pings must store coordinates, timestamp, accuracy, speed, heading, source, and ingestion metadata.
- **REQ-07-005:** Live maps must show current location, stale location state, status, route, assigned job, and alerts.
- **REQ-07-006:** Route replay must query historical pings and overlay stops, geofence events, and check-ins.
- **REQ-07-007:** Geofences must support circle and polygon later; MVP may start with radius-based geofences.
- **REQ-07-008:** Geofence events must capture enter, exit, dwell, missed arrival, late arrival, and unauthorized departure where configured.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.8 Service / Work Orders Module

- **REQ-08-001:** Service requests must capture requester, customer, site, issue, priority, photos, desired date, and source.
- **REQ-08-002:** Work orders must include assigned technician, parts, labor, checklist, status, completion notes, and customer sign-off.
- **REQ-08-003:** Maintenance schedules must support vehicles, equipment, assets, intervals, reminders, and service history.
- **REQ-08-004:** Parts used must decrement or reserve inventory when inventory module is enabled.
- **REQ-08-005:** Service history must be visible from account, site, asset, vehicle, and product contexts where relevant.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.9 Reporting / Analytics Module

- **REQ-09-001:** Dashboards must be role-aware and module-aware.
- **REQ-09-002:** Reports must use materialized rollups for expensive operational metrics where needed.
- **REQ-09-003:** Users must be able to filter reports by date range, company, branch, team, user, module, status, owner, territory, location, product, and job type where applicable.
- **REQ-09-004:** Saved reports must store filters, columns, grouping, sorting, permissions, and schedule later.
- **REQ-09-005:** Operational reports must reconcile status history, event timestamps, and current record state.
- **REQ-09-006:** Exported reports must preserve filters and timestamps.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

### 7.10 Integrations Module

- **REQ-10-001:** Integration connections must store provider, company, credentials reference, status, scopes, and last sync.
- **REQ-10-002:** QuickBooks must store external IDs and sync state on synced records.
- **REQ-10-003:** Sync jobs must support queued, running, succeeded, failed, partially failed, skipped, and retry states.
- **REQ-10-004:** Webhook events must be configurable per company and module.
- **REQ-10-005:** API keys must be scoped, revocable, auditable, and rate-limited.
- **REQ-10-006:** CSV and Excel imports must validate data and produce row-level errors.

**Baseline views**
- List/table view with saved filters and column configuration.
- Detail view with record header, status, ownership, timeline, files, related records, and audit summary.
- Create/edit drawer or page depending on workflow complexity.
- Bulk action support where safe and permission-appropriate.
- Export support where user role allows data extraction.

**Baseline acceptance criteria**
- Users only see records allowed by company, module, role, and record access rules.
- Every create, update, delete, status transition, assignment, and high-impact action is auditable.
- All required fields have validation and useful error messaging.
- Record detail pages expose related activity and next action.
- Search and filters return consistent results across desktop views.

## 8. Personas And Primary Jobs To Be Done

### 8.1 Super Admin

- Job: Configure global platform behavior.
- Job: Manage tenants and companies.
- Job: Monitor system-wide health.
- Job: Troubleshoot cross-company issues without violating access controls.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.2 Company Admin

- Job: Configure company modules.
- Job: Invite users and manage roles.
- Job: Configure tags, custom fields, pipelines, locations, and notification rules.
- Job: Review audit logs and integration status.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.3 Sales Manager

- Job: Monitor pipeline and rep activity.
- Job: Assign leads and territories.
- Job: Review campaign effectiveness.
- Job: Forecast revenue and coach reps.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.4 Sales Rep

- Job: Work leads and accounts.
- Job: Log calls, emails, SMS, LinkedIn activity, meetings, and site visits.
- Job: Create opportunities and follow-ups.
- Job: Schedule appointments and manage daily tasks.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.5 Field Manager

- Job: Assign visits, crews, equipment, and work.
- Job: Monitor field activity and site status.
- Job: Review exceptions and completion evidence.
- Job: Coordinate with dispatch and warehouse.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.6 Dispatcher

- Job: Assign vehicles, drivers, routes, jobs, and stops.
- Job: Monitor live movement and delays.
- Job: Update route plans.
- Job: Handle exceptions and notify stakeholders.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.7 Driver

- Job: View assigned route and stops.
- Job: Check in/out.
- Job: Capture proof of delivery or job progress.
- Job: Report delays and issues.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.8 Warehouse Manager

- Job: Manage stock, receiving, transfers, picking, and adjustments.
- Job: Monitor low stock.
- Job: Approve inventory corrections.
- Job: Coordinate truck loading and depot movements.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.9 Warehouse Operator

- Job: Receive items.
- Job: Pick and pack stock.
- Job: Move inventory.
- Job: Confirm truck loads and transfers.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.10 Service Manager

- Job: Triage service requests.
- Job: Assign work orders.
- Job: Track parts and labor.
- Job: Review completion and follow-up.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.11 Service Technician

- Job: View assigned work orders.
- Job: Log labor and parts.
- Job: Capture photos and notes.
- Job: Complete service checklists offline if needed.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.12 Analyst / Reporting User

- Job: Build and view dashboards.
- Job: Export reports.
- Job: Analyze trends across sales, field, fleet, inventory, and service operations.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

### 8.13 Read-only Viewer

- Job: View permitted records and reports.
- Job: Search historical information.
- Job: Avoid making changes.

**Common screens needed**
- Dashboard
- Global search
- Record list views
- Record detail pages
- Notifications
- Profile and preferences

**Important permissions**
- View own records
- View team records where applicable
- Create/update assigned workflow records
- Export only if explicitly granted
- Admin configuration only for administrative roles

## 9. Information Architecture

| Navigation Area | Purpose |
| --- | --- |
| Home | Role-based dashboard, alerts, recent records, upcoming tasks. |
| CRM | Accounts, contacts, leads, opportunities, pipelines, activities. |
| Outbound | Lists, campaigns, sequences, queues, activity performance. |
| Calendar & Tasks | Calendar, task board, reminders, recurring work. |
| Field Operations | Sites, visits, jobs, crews, check-ins, photos, field notes. |
| Dispatch | Dispatch board, orders, shipments, routes, stops, exceptions. |
| Fleet | Vehicles, drivers, devices, live map, location history, geofences. |
| Inventory | Products, warehouses, depots, bins, stock balances, movements. |
| Service | Service requests, work orders, maintenance, parts, labor. |
| Reports | Dashboards, custom reports, saved reports, exports. |
| Admin | Users, teams, roles, modules, fields, tags, integrations, audit logs. |

## 10. Global UX Standards

- Every major module must have a table view optimized for desktop users.
- Every table view must support search, filters, sorting, pagination, saved views, and column customization when appropriate.
- Every important record must have a detail page with header, status, owner, key fields, activity timeline, related records, files, and audit access.
- Every status-driven workflow must show current status, allowed next statuses, and why a transition is blocked if unavailable.
- Mobile screens must focus on daily execution: assigned work, check-ins, notes, photos, route/stops, and completion.
- Long forms must be broken into sections with progressive disclosure.
- Destructive actions must require confirmation and permissions.
- Bulk actions must show preview count, permission limitations, and undo strategy where feasible.
- Offline mobile actions must show pending sync, failed sync, and conflict state clearly.
- Error messages must explain what failed and what the user can do next.

## 11. Standard Filters And Views

### 11.1 Global Filter Patterns

- **Company:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Branch:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Team:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Owner:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Assigned user:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Created by:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Created date:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Updated date:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Status:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Priority:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Source:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Tag:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Custom field:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Territory:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Location:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Date range:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Due date:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Overdue flag:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Module:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Archived flag:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Has attachment:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Has open task:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Last activity date:** Available where relevant and permission-safe; saved view support should preserve this filter.
- **Next action date:** Available where relevant and permission-safe; saved view support should preserve this filter.

### 11.2 CRM Filters

- **Account type:** Must be supported in CRM list/report contexts where the data exists.
- **Industry:** Must be supported in CRM list/report contexts where the data exists.
- **Lifecycle stage:** Must be supported in CRM list/report contexts where the data exists.
- **Account owner:** Must be supported in CRM list/report contexts where the data exists.
- **Contact role:** Must be supported in CRM list/report contexts where the data exists.
- **Lead source:** Must be supported in CRM list/report contexts where the data exists.
- **Lead status:** Must be supported in CRM list/report contexts where the data exists.
- **Lead score:** Must be supported in CRM list/report contexts where the data exists.
- **Pipeline:** Must be supported in CRM list/report contexts where the data exists.
- **Opportunity stage:** Must be supported in CRM list/report contexts where the data exists.
- **Deal value range:** Must be supported in CRM list/report contexts where the data exists.
- **Expected close date:** Must be supported in CRM list/report contexts where the data exists.
- **Lost reason:** Must be supported in CRM list/report contexts where the data exists.
- **Last outreach date:** Must be supported in CRM list/report contexts where the data exists.
- **No activity in X days:** Must be supported in CRM list/report contexts where the data exists.
- **Meeting booked:** Must be supported in CRM list/report contexts where the data exists.
- **Site visit completed:** Must be supported in CRM list/report contexts where the data exists.

### 11.3 Operations Filters

- **Job status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Job type:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Site status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Geofence status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Check-in state:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Crew:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Vehicle:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Driver:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Device last seen:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Route status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Stop status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Late flag:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Exception type:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Warehouse:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Depot:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Bin location:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **SKU:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Product category:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Stock availability:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Reserved quantity:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Transfer status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.
- **Receiving status:** Must be available for field, dispatch, fleet, warehouse, and reporting workspaces where applicable.

### 11.4 Saved Views

- Saved views must store filters, columns, sort order, grouping, density, and default date range.
- Saved views may be private, team-shared, role-shared, or company-shared depending on permissions.
- Admins should be able to set default views per role or module.
- Users should be able to duplicate a saved view and personalize it.
- Changes to shared views must be audited.

## 12. Data Domains And Entity Model

### 12.1 Tenant

- **Purpose:** Defines the tenant domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `name`
  - `status`
  - `plan`
  - `created_at`
  - `updated_at`
  - `region`
  - `settings`
  - `feature_flags`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.2 Company

- **Purpose:** Defines the company domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `name`
  - `legal_name`
  - `status`
  - `modules_enabled`
  - `billing_profile`
  - `timezone`
  - `locale`
  - `settings`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.3 Branch

- **Purpose:** Defines the branch domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `type`
  - `address`
  - `timezone`
  - `manager_user_id`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.4 User

- **Purpose:** Defines the user domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `email`
  - `name`
  - `phone`
  - `status`
  - `profile`
  - `last_login_at`
  - `mfa_status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.5 Membership

- **Purpose:** Defines the membership domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `user_id`
  - `role_ids`
  - `team_ids`
  - `status`
  - `effective_from`
  - `effective_to`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.6 Team

- **Purpose:** Defines the team domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `type`
  - `manager_user_id`
  - `member_user_ids`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.7 Role

- **Purpose:** Defines the role domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `description`
  - `permission_keys`
  - `scope_rules`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.8 Account

- **Purpose:** Defines the account domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `type`
  - `status`
  - `owner_user_id`
  - `industry`
  - `address`
  - `coordinates`
  - `tags`
  - `custom_fields`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.9 Contact

- **Purpose:** Defines the contact domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `account_id`
  - `first_name`
  - `last_name`
  - `emails`
  - `phones`
  - `role_title`
  - `influence_level`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.10 Lead

- **Purpose:** Defines the lead domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `source`
  - `status`
  - `owner_user_id`
  - `score`
  - `account_id`
  - `contact_id`
  - `qualification`
  - `next_action_at`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.11 Opportunity

- **Purpose:** Defines the opportunity domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `account_id`
  - `contact_ids`
  - `pipeline_id`
  - `stage_id`
  - `value`
  - `probability`
  - `expected_close_date`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.12 Pipeline

- **Purpose:** Defines the pipeline domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `stages`
  - `default_probability`
  - `active`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.13 Activity

- **Purpose:** Defines the activity domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `record_refs`
  - `type`
  - `direction`
  - `body`
  - `outcome`
  - `occurred_at`
  - `created_by_user_id`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.14 Task

- **Purpose:** Defines the task domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `title`
  - `type`
  - `status`
  - `priority`
  - `assignee_user_id`
  - `due_at`
  - `related_records`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.15 CalendarEvent

- **Purpose:** Defines the calendarevent domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `title`
  - `start_at`
  - `end_at`
  - `location`
  - `attendees`
  - `related_records`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.16 Site

- **Purpose:** Defines the site domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `account_id`
  - `name`
  - `address`
  - `coordinates`
  - `access_notes`
  - `hazards`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.17 SiteVisit

- **Purpose:** Defines the sitevisit domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `site_id`
  - `assigned_user_id`
  - `scheduled_start`
  - `scheduled_end`
  - `status`
  - `check_in_id`
  - `check_out_id`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.18 Job

- **Purpose:** Defines the job domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `account_id`
  - `site_id`
  - `type`
  - `status`
  - `priority`
  - `requested_date`
  - `assigned_team_id`
  - `dispatch_status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.19 ServiceRequest

- **Purpose:** Defines the servicerequest domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `account_id`
  - `site_id`
  - `source`
  - `priority`
  - `status`
  - `description`
  - `requested_by`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.20 WorkOrder

- **Purpose:** Defines the workorder domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `service_request_id`
  - `technician_user_id`
  - `status`
  - `parts`
  - `labor_entries`
  - `checklist`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.21 Product

- **Purpose:** Defines the product domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `sku`
  - `name`
  - `category`
  - `unit_of_measure`
  - `active`
  - `quickbooks_item_id`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.22 InventoryLocation

- **Purpose:** Defines the inventorylocation domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `type`
  - `name`
  - `address`
  - `parent_location_id`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.23 BinLocation

- **Purpose:** Defines the binlocation domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `location_id`
  - `zone`
  - `aisle`
  - `rack`
  - `shelf`
  - `bin_code`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.24 StockBalance

- **Purpose:** Defines the stockbalance domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `product_id`
  - `location_id`
  - `bin_id`
  - `on_hand_qty`
  - `reserved_qty`
  - `available_qty`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.25 StockMovement

- **Purpose:** Defines the stockmovement domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `product_id`
  - `quantity`
  - `movement_type`
  - `source_location_id`
  - `destination_location_id`
  - `reason_code`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.26 Order

- **Purpose:** Defines the order domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `account_id`
  - `site_id`
  - `status`
  - `line_items`
  - `delivery_window`
  - `billing_status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.27 Shipment

- **Purpose:** Defines the shipment domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `order_id`
  - `route_id`
  - `vehicle_id`
  - `driver_user_id`
  - `status`
  - `proof`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.28 Route

- **Purpose:** Defines the route domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `date`
  - `vehicle_id`
  - `driver_user_id`
  - `status`
  - `planned_distance`
  - `actual_distance`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.29 Stop

- **Purpose:** Defines the stop domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `route_id`
  - `sequence`
  - `site_id`
  - `planned_arrival`
  - `actual_arrival`
  - `status`
  - `exception_type`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.30 Vehicle

- **Purpose:** Defines the vehicle domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `depot_id`
  - `name`
  - `type`
  - `plate`
  - `vin`
  - `status`
  - `capacity`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.31 Driver

- **Purpose:** Defines the driver domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `user_id`
  - `license_reference`
  - `status`
  - `assigned_vehicle_id`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.32 TrackingDevice

- **Purpose:** Defines the trackingdevice domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `provider`
  - `external_device_id`
  - `assigned_to_type`
  - `assigned_to_id`
  - `status`
  - `last_seen_at`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.33 LocationPing

- **Purpose:** Defines the locationping domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `device_id`
  - `tracked_subject_type`
  - `tracked_subject_id`
  - `coordinates`
  - `accuracy`
  - `speed`
  - `heading`
  - `recorded_at`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.34 Geofence

- **Purpose:** Defines the geofence domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `shape_type`
  - `coordinates`
  - `radius`
  - `record_refs`
  - `status`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.35 GeofenceEvent

- **Purpose:** Defines the geofenceevent domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `geofence_id`
  - `subject_type`
  - `subject_id`
  - `event_type`
  - `occurred_at`
  - `location_ping_id`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.36 Report

- **Purpose:** Defines the report domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `name`
  - `type`
  - `filters`
  - `columns`
  - `owner_user_id`
  - `visibility`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.37 IntegrationConnection

- **Purpose:** Defines the integrationconnection domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `provider`
  - `status`
  - `scopes`
  - `last_sync_at`
  - `settings`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.38 SyncJob

- **Purpose:** Defines the syncjob domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `provider`
  - `entity_type`
  - `entity_id`
  - `status`
  - `attempt_count`
  - `error_summary`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

### 12.39 AuditLogEntry

- **Purpose:** Defines the auditlogentry domain record used by the platform.
- **Required baseline fields:**
  - `id`
  - `tenant_id`
  - `company_id`
  - `actor_user_id`
  - `action`
  - `entity_type`
  - `entity_id`
  - `before`
  - `after`
  - `occurred_at`
- **Common metadata:** `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`, `deleted_at` where soft delete applies.
- **Tenant safety:** Must include `tenant_id` unless the entity is truly global and platform-owned.
- **Company safety:** Must include `company_id` for company-scoped records unless intentionally tenant-wide.
- **Audit behavior:** Create, update, delete, status transition, assignment, and permission-impacting changes must be logged.

## 13. Status Models

### 13.1 Lead Statuses

- `new`
- `assigned`
- `working`
- `contacted`
- `qualified`
- `disqualified`
- `converted`
- `archived`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.2 Opportunity Statuses

- `open`
- `won`
- `lost`
- `stalled`
- `archived`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.3 Task Statuses

- `open`
- `in_progress`
- `blocked`
- `completed`
- `cancelled`
- `overdue`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.4 Site Visit Statuses

- `scheduled`
- `traveling`
- `checked_in`
- `completed`
- `missed`
- `cancelled`
- `needs_follow_up`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.5 Job Statuses

- `requested`
- `reviewing`
- `approved`
- `scheduled`
- `dispatched`
- `in_progress`
- `blocked`
- `completed`
- `cancelled`
- `ready_for_billing`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.6 Order Statuses

- `draft`
- `confirmed`
- `ready_to_pick`
- `picking`
- `ready_to_dispatch`
- `dispatched`
- `delivered`
- `completed`
- `cancelled`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.7 Shipment Statuses

- `planned`
- `assigned`
- `loading`
- `in_transit`
- `delayed`
- `delivered`
- `exception`
- `cancelled`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.8 Route Statuses

- `planned`
- `assigned`
- `started`
- `in_progress`
- `completed`
- `cancelled`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.9 Stop Statuses

- `planned`
- `en_route`
- `arrived`
- `servicing`
- `completed`
- `skipped`
- `failed`
- `exception`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.10 Vehicle Statuses

- `available`
- `assigned`
- `in_use`
- `maintenance`
- `out_of_service`
- `inactive`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.11 Inventory Transfer Statuses

- `draft`
- `requested`
- `picked`
- `in_transit`
- `received`
- `partially_received`
- `cancelled`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.12 Work Order Statuses

- `new`
- `triaged`
- `assigned`
- `in_progress`
- `waiting_parts`
- `completed`
- `cancelled`
- `closed`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

### 13.13 Sync Job Statuses

- `queued`
- `running`
- `succeeded`
- `failed`
- `partially_failed`
- `skipped`
- `retry_scheduled`

**Transition rules**
- Allowed transitions must be centrally defined for each module.
- Blocked transitions must show a reason to the user.
- Important transitions must write activity timeline entries.
- Transitions that affect inventory, dispatch, billing, or sync must be idempotent and auditable.

## 14. Permission Model

- Use company-level access as the primary boundary.
- Layer module-level permissions inside the company boundary.
- Layer action-level permissions for create, read, update, delete, export, import, assign, approve, configure, and administer actions.
- Layer record-level permissions only where business value justifies complexity.
- Support role inheritance later, but keep MVP roles explicit and understandable.
- Support policy-based authorization using Cerbos if record-level or attribute-based access becomes complex.

### 14.1 Permission Layers

| Layer | Definition |
| --- | --- |
| Tenant access | Determines whether a user can access the tenant at all. |
| Company access | Determines which customer companies the user can access. |
| Module access | Determines which product modules appear and are usable. |
| Action access | Determines what the user can do inside a module. |
| Record access | Determines which records the user can see or modify. |
| Field access | Determines whether sensitive fields are hidden, read-only, or editable. |
| Export access | Determines whether data can leave the system. |
| Admin access | Determines whether a user can configure settings, roles, modules, integrations, and fields. |

### 14.2 Baseline Permission Actions

- `view`
- `create`
- `edit`
- `delete`
- `archive`
- `restore`
- `assign`
- `reassign`
- `approve`
- `reject`
- `transition_status`
- `import`
- `export`
- `bulk_update`
- `configure`
- `view_audit`
- `manage_permissions`
- `manage_integrations`

### 14.3 Role Permission Matrix Draft

| Role | Admin | CRM | Outbound | Calendar | Field | Dispatch | Fleet | Inventory | Service | Reports | Integrations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Super Admin | Admin | Admin | Admin | Admin | Admin | Admin | Admin | Admin | Admin | Admin | Admin |
| Company Admin | Admin | Full | Full | Full | Full | Full | Full | Full | Full | Full | Admin |
| Sales Manager | - | Full | Full | Full | View | View | - | View | - | Full | - |
| Sales Rep | - | Own/Team | Own/Team | Own/Team | Own/Team | - | - | - | - | - | - |
| Field Manager | - | View | - | Full | Full | Full | Full | View | - | Full | - |
| Dispatcher | - | View | - | Full | View | Full | Full | View | - | - | - |
| Driver | - | - | - | Own | Own | Own | Own | - | - | - | - |
| Warehouse Manager | - | View | - | - | - | View | - | Full | - | Full | - |
| Warehouse Operator | - | - | - | - | - | View | - | Execute | - | - | - |
| Service Manager | - | View | - | Full | View | - | - | View | Full | Full | - |
| Service Technician | - | - | - | Own | - | - | - | Own | Own | - | - |
| Analyst | - | View | View | View | View | View | View | View | View | View/Export | - |
| Read-only Viewer | - | View | View | View | View | View | View | View | View | View | - |

## 15. Core Workflows

### 15.1 Outbound Sales Workflow

1. Lead is imported, created manually, captured from integration, or converted from an event.
2. Lead is validated for duplicates and minimum required data.
3. Lead is assigned to a rep, team, territory, or queue.
4. Rep receives task or campaign step.
5. Rep performs outreach using call, email, SMS, WhatsApp, or LinkedIn manual action.
6. Activity is logged with outcome, timestamp, notes, and next step.
7. Lead status updates based on outcome.
8. Opportunity is created if qualification criteria are met.
9. Follow-up tasks and appointment are scheduled.
10. Manager reviews conversion and activity metrics.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

### 15.2 Field Sales Workflow

1. Sales manager assigns account, site, or visit to field rep.
2. Rep sees visit on calendar and mobile daily list.
3. Rep navigates to site and checks in with location capture.
4. System validates geofence when configured.
5. Rep captures notes, photos, contact outcome, and next steps.
6. Rep creates quote request, job request, or follow-up task when needed.
7. Rep checks out and marks visit outcome.
8. Timeline updates account, site, and user activity views.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

### 15.3 Drilling Operations Workflow

1. Customer request or won opportunity becomes operational job request.
2. Operations reviews site, access, scope, hazards, schedule, inventory, equipment, and crew requirements.
3. Warehouse confirms product and equipment availability.
4. Dispatcher assigns truck, driver, crew, and route.
5. Geofence and planned arrival window are created where applicable.
6. Field team travels to site and checks in.
7. Job progress, exceptions, photos, notes, and completion proof are recorded.
8. Inventory consumption and parts used are posted.
9. Completion state triggers billing review or QuickBooks sync where configured.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

### 15.4 Dispatch And Tracking Workflow

1. Order, shipment, or job becomes ready for dispatch.
2. Dispatcher assigns vehicle, driver, device, equipment, and route.
3. Route appears on driver mobile view.
4. Vehicle and/or driver location updates are ingested.
5. Map displays live location and stale-location warnings.
6. Geofence entry/exit and stop check-in events are captured.
7. Dispatcher handles delays, route deviations, exceptions, and reassignment.
8. Completion proof is captured and linked to route, stop, shipment, and account timeline.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

### 15.5 Warehouse Workflow

1. Product arrives, is transferred, or is adjusted into stock.
2. Operator selects warehouse, depot, bin, SKU, quantity, and reason.
3. Stock movement is created as append-only event.
4. Stock balance updates idempotently.
5. Pick list is generated for order, shipment, job, or truck load.
6. Operator picks, confirms, and handles discrepancies.
7. Transfer or dispatch handoff is confirmed.
8. Low stock, exceptions, and movement history update reports.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

### 15.6 Service Workflow

1. Service request is created from customer call, field note, job exception, maintenance schedule, or admin entry.
2. Service manager triages priority, location, asset, and required parts.
3. Technician is assigned with due date and work order checklist.
4. Technician reviews work on mobile, checks in if on site, and records parts/labor.
5. Technician captures photos, notes, customer sign-off, and completion result.
6. Manager reviews work order and closes it.
7. Parts, labor, service history, and reporting rollups update.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

### 15.7 QuickBooks Sync Workflow

1. Record becomes eligible for sync based on configuration and status.
2. Sync job is queued with idempotency key.
3. Worker validates required accounting fields.
4. Worker creates or updates external record.
5. External ID and sync timestamp are stored.
6. Errors are visible with retry action and row-level detail when applicable.
7. Admin can review sync history and resolve mapping issues.

**Exceptions to handle**
- Required data missing.
- User lacks permission for requested transition.
- Record is archived or locked.
- Offline action conflicts with server state.
- Integration or external provider fails.
- Related inventory, vehicle, user, route, or accounting mapping is unavailable.

**Acceptance criteria**
- Workflow can be completed by the intended role without admin intervention.
- Every status change is visible in timeline and audit history.
- Notifications trigger only for useful state changes.
- Reports can measure cycle time, owner, status, exceptions, and completion.
- Failed operations are recoverable and visible.

## 16. Technical Architecture

### 16.1 Backend Architecture

- Use Python and FastAPI for API services.
- Use Uvicorn or equivalent ASGI runtime in production behind a reverse proxy or container platform.
- Use MongoDB as the primary operational database.
- Use Redis for caching, rate limiting, locks, ephemeral queues, and WebSocket fanout where appropriate.
- Use Celery or a similar worker model for asynchronous jobs such as imports, exports, syncs, notifications, geofence evaluation, and report rollups.
- Separate API request handling from long-running background work.
- Use idempotency keys for high-impact create/update/sync actions.
- Use structured logging and correlation IDs across API and worker flows.

### 16.2 Frontend Architecture

- Use Next.js for web application architecture.
- Use Tailwind CSS and shadcn/ui for consistent layouts and components.
- Use server-side data fetching where appropriate for secure initial pages and client-side fetching for interactive workspaces.
- Use role-aware navigation and module-aware route guards.
- Use table components that support large datasets with pagination, filters, sorting, and saved views.
- Use map components with clustering, geofence overlays, route polylines, vehicle status markers, and stale-location indicators.
- Use mobile-optimized layouts for field execution screens, not just responsive shrinkage of desktop tables.

### 16.3 Integration Architecture

- Use a provider abstraction for QuickBooks, email, SMS, WhatsApp, tracking providers, and future integrations.
- Store external IDs in explicit mapping fields or integration mapping records.
- Use sync logs for all external operations.
- Use retry policies with backoff and maximum attempt limits.
- Expose admin tools for reconnecting accounts, retrying failed syncs, and reviewing errors.
- Do not perform external sync inside the main API request if the external call can be delayed safely.

### 16.4 Real-Time Architecture

- Use real-time updates for live maps, dispatch boards, notifications, and selected operational status changes.
- Use polling where real-time complexity is not justified.
- Use Redis pub/sub or a managed message layer for WebSocket fanout where needed.
- Do not require real-time consistency for reporting dashboards that use rollups.
- Clearly display stale location and stale data states.

## 17. MongoDB Data Design Guidance

- Use stable generated IDs for all primary entities.
- Store tenant and company IDs on almost every record for query safety and sharding optionality.
- Avoid deep nesting for records that need independent permissions, reporting, search, or updates.
- Embed small immutable snapshots where they improve history readability.
- Use append-only event collections for inventory movements, location pings, geofence events, audit logs, activities, and sync logs.
- Use denormalized snapshots for dashboards and frequently displayed summary fields.
- Use indexes deliberately for tenant, company, status, owner, date, location, and search patterns.
- Use TTL indexes only for data that is legally and operationally safe to expire.
- Design for data retention policies before storing large volumes of GPS and audit data.

### 17.1 Suggested Collection Groups

- **Identity:** `tenants`, `companies`, `branches`, `users`, `memberships`, `teams`, `roles`, `sessions`
- **CRM:** `accounts`, `contacts`, `leads`, `opportunities`, `pipelines`, `activities`
- **Work Management:** `tasks`, `calendar_events`, `notifications`, `files`, `comments`
- **Field Operations:** `sites`, `site_visits`, `jobs`, `job_events`, `field_notes`
- **Inventory:** `products`, `inventory_locations`, `bin_locations`, `stock_balances`, `stock_movements`, `inventory_transfers`
- **Dispatch:** `orders`, `shipments`, `routes`, `stops`, `dispatch_events`
- **Fleet:** `vehicles`, `drivers`, `tracking_devices`, `location_pings`, `geofences`, `geofence_events`
- **Service:** `service_requests`, `work_orders`, `maintenance_schedules`, `labor_entries`
- **Reporting:** `report_definitions`, `dashboard_rollups`, `metric_snapshots`, `export_jobs`
- **Integrations:** `integration_connections`, `integration_mappings`, `sync_jobs`, `webhook_subscriptions`, `webhook_deliveries`
- **Audit:** `audit_logs`, `security_events`

### 17.2 Index Strategy

| Use Case | Index Pattern |
| --- | --- |
| All company-scoped collections | `tenant_id`, `company_id`, `created_at` |
| Owner-based work queues | `tenant_id`, `company_id`, `owner_user_id`, `status`, `next_action_at` |
| Tasks | `tenant_id`, `company_id`, `assignee_user_id`, `status`, `due_at` |
| Opportunities | `tenant_id`, `company_id`, `pipeline_id`, `stage_id`, `expected_close_date` |
| Inventory balances | `tenant_id`, `company_id`, `product_id`, `location_id`, `bin_id` |
| Stock movements | `tenant_id`, `company_id`, `product_id`, `occurred_at` |
| Routes and stops | `tenant_id`, `company_id`, `date`, `status`, `driver_user_id` |
| Location pings | `tenant_id`, `company_id`, `tracked_subject_id`, `recorded_at` |
| Geofence events | `tenant_id`, `company_id`, `geofence_id`, `event_type`, `occurred_at` |
| Audit logs | `tenant_id`, `company_id`, `entity_type`, `entity_id`, `occurred_at` |
| Sync jobs | `tenant_id`, `company_id`, `provider`, `status`, `created_at` |

## 18. API Design Standards

- All APIs must enforce tenant and company scope on the server, never only in the client.
- Use consistent REST naming for resources and nested relationships.
- Use cursor pagination for large operational lists.
- Use explicit filter parameters instead of ambiguous search-only APIs.
- Return validation errors with field-level details.
- Return authorization errors without leaking existence of inaccessible records when needed.
- Support idempotency headers for create operations that can be retried.
- Support bulk APIs only when permission and partial failure handling are clear.
- Expose audit-safe admin APIs for configuration changes.

### 18.1 API Endpoint Families

- `/auth/*`
- `/tenants/*`
- `/companies/*`
- `/users/*`
- `/memberships/*`
- `/roles/*`
- `/teams/*`
- `/accounts/*`
- `/contacts/*`
- `/leads/*`
- `/opportunities/*`
- `/activities/*`
- `/tasks/*`
- `/calendar-events/*`
- `/sites/*`
- `/site-visits/*`
- `/jobs/*`
- `/products/*`
- `/inventory-locations/*`
- `/stock-balances/*`
- `/stock-movements/*`
- `/orders/*`
- `/shipments/*`
- `/routes/*`
- `/vehicles/*`
- `/drivers/*`
- `/tracking-devices/*`
- `/location-pings/*`
- `/geofences/*`
- `/service-requests/*`
- `/work-orders/*`
- `/reports/*`
- `/integrations/*`
- `/sync-jobs/*`
- `/audit-logs/*`
- `/files/*`
- `/notifications/*`

## 19. Offline Mobile Requirements

- Offline support is required for check-ins, notes, photos, task completion, site visits, and selected work order actions.
- Offline support should start with assigned work rather than full database replication.
- The mobile app must cache recent assigned records, route/stops, customer/site basics, and required form metadata.
- The app must maintain an offline action queue with local IDs and sync status.
- The UI must show pending, synced, failed, and conflict states.
- Photos captured offline must remain available locally until safely uploaded.
- Conflict handling must be deterministic and explainable.
- Server APIs must accept idempotent offline submissions.

### 19.1 Offline Action Types

- `create_check_in`
- `create_check_out`
- `complete_task`
- `add_field_note`
- `attach_photo`
- `update_visit_status`
- `update_stop_status`
- `capture_proof`
- `log_work_order_labor`
- `record_parts_used`

### 19.2 Conflict Strategy

- If server record was deleted or archived, preserve offline action as failed with admin-visible recovery option.
- If status moved forward but offline action is compatible, apply action as historical event without rolling back server state.
- If inventory quantity conflicts, require review rather than silently adjusting stock.
- If duplicate check-in occurs, merge when same user/site/time window is clearly the same action; otherwise keep both with review flag.
- If photo upload fails, retry without duplicating activity entries.

## 20. Maps, GPS, And Geofencing

- Live map must show vehicles, drivers, field users, active jobs, route stops, and geofence overlays where enabled.
- Location points must include accuracy and source so low-confidence pings can be handled properly.
- Stale locations must be visually and textually identified.
- Geofence events must be generated by reliable server-side evaluation where possible.
- Manual check-ins must remain available even when GPS is unavailable, but should be flagged for review if policy requires location validation.
- Historical route replay must support date range, vehicle, driver, route, and job filters.
- Alerts must avoid noise by supporting thresholds, quiet periods, and role-specific notification rules.

### 20.1 Geofence Types

- Customer site geofence
- Warehouse geofence
- Depot geofence
- Job site geofence
- Restricted area geofence
- Route corridor geofence later
- Temporary event geofence later

### 20.2 GPS Event Types

- `location_ping_received`
- `device_stale`
- `device_recovered`
- `geofence_entered`
- `geofence_exited`
- `late_arrival_detected`
- `route_deviation_detected`
- `unauthorized_stop_detected`
- `manual_check_in_created`
- `manual_check_out_created`

## 21. QuickBooks Integration Requirements

- QuickBooks must be treated as a core integration from the platform design stage.
- The system must store QuickBooks connection status per company.
- The system must store external IDs for synced customers, items, invoices, payments, and related references.
- The system must provide sync logs with status, timestamps, payload references, error summaries, and retry actions.
- The system must avoid silent mismatches by showing unmapped required fields.
- The system must define whether invoices are created in-app, synced to QuickBooks, or created only in QuickBooks.
- The system must support retrying failed sync jobs safely.
- The system must avoid duplicate external records by using idempotency and external ID mapping.

### 21.1 Likely Sync Objects

- Customers
- Vendors later if needed
- Products and services
- Invoices
- Payments
- Tax codes or tax-related fields
- Terms
- Accounts or income references
- Classes or locations if configured
- Sync status and error logs

## 22. Reporting And Analytics

- Reporting must be designed from day one.
- Dashboards must use role-aware defaults.
- Operational metrics must be derived from clear timestamps and status events.
- Reports must support saved filters, export, grouping, sorting, and scheduled delivery later.
- Custom report builder should start with curated datasets rather than unrestricted raw database access.
- Report definitions must be permission-aware.

### 22.1 Sales Dashboard

- **Metric:** New leads
- **Metric:** Contacted leads
- **Metric:** Qualified leads
- **Metric:** Opportunities created
- **Metric:** Pipeline value
- **Metric:** Win rate
- **Metric:** Lost reason breakdown
- **Metric:** Activity volume

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.2 Outbound Dashboard

- **Metric:** Calls made
- **Metric:** Emails logged
- **Metric:** SMS logged
- **Metric:** LinkedIn actions logged
- **Metric:** Meetings booked
- **Metric:** Sequence step completion
- **Metric:** Follow-up overdue

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.3 Field Activity Dashboard

- **Metric:** Visits scheduled
- **Metric:** Visits completed
- **Metric:** Missed visits
- **Metric:** Check-in compliance
- **Metric:** Photos captured
- **Metric:** Follow-ups created

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.4 Dispatch Dashboard

- **Metric:** Jobs ready
- **Metric:** Routes active
- **Metric:** Stops completed
- **Metric:** Late stops
- **Metric:** Exceptions
- **Metric:** Average delay
- **Metric:** Unassigned work

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.5 Fleet Dashboard

- **Metric:** Vehicles active
- **Metric:** Vehicles stale
- **Metric:** Miles traveled
- **Metric:** Idle time later
- **Metric:** Route completion
- **Metric:** Device health

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.6 Inventory Dashboard

- **Metric:** On hand quantity
- **Metric:** Available quantity
- **Metric:** Reserved quantity
- **Metric:** Low stock
- **Metric:** Transfers pending
- **Metric:** Adjustments by reason

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.7 Service Dashboard

- **Metric:** Open requests
- **Metric:** Work orders assigned
- **Metric:** Completed work orders
- **Metric:** Average resolution time
- **Metric:** Parts used
- **Metric:** Waiting on parts

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

### 22.8 Integration Dashboard

- **Metric:** Sync jobs queued
- **Metric:** Sync jobs failed
- **Metric:** Last successful sync
- **Metric:** Unmapped records
- **Metric:** Retry count
- **Metric:** Provider connection status

**Default filters**
- Date range
- Company
- Branch
- Team
- User/owner
- Status
- Module-specific filters

## 23. Notification Strategy

- Notifications must be useful, configurable, and role-aware.
- Notification channels may include in-app, email, SMS, and push where mobile app supports it.
- High-noise events such as GPS pings must not notify directly; only derived exceptions should notify.
- Notification preferences must support user-level and company-level defaults.
- Critical admin notifications include integration failures, security events, and permission changes.

- `task_assigned`
- `task_due_soon`
- `task_overdue`
- `lead_assigned`
- `opportunity_stage_changed`
- `visit_scheduled`
- `visit_missed`
- `check_in_completed`
- `job_ready_for_dispatch`
- `route_assigned`
- `stop_late`
- `geofence_exception`
- `inventory_low_stock`
- `transfer_received`
- `work_order_assigned`
- `sync_failed`
- `import_completed`
- `export_ready`
- `permission_changed`

## 24. Audit, Compliance, And Traceability

- Audit logs must capture who did what, when, from where, and what changed.
- Audit logs must be immutable from normal application flows.
- Audit access must be permission-controlled.
- High-volume telemetry such as raw GPS pings should not be treated the same as business audit logs, but derived operational events should be auditable.
- Inventory movements must be append-only and reversible through correction movements, not destructive edits.
- Permission changes must always be audited.
- Integration sync operations must always be auditable.

### 24.1 Audit Event Categories

- Authentication
- Authorization and permission changes
- Record creation
- Record update
- Record deletion or archive
- Status transition
- Assignment changes
- Inventory movement
- Dispatch action
- Check-in/check-out
- Geofence event
- File upload/delete
- Integration sync
- Import/export
- Configuration change

## 25. Security Requirements

- All API access must be authenticated except explicit public endpoints.
- Company and tenant boundaries must be enforced server-side.
- Passwords must be hashed using modern password hashing standards if password auth is used.
- MFA should be supported for admins and optionally for all users.
- Session management must support revocation.
- API keys must be scoped and revocable.
- Sensitive secrets must never be stored in plaintext application records.
- File access must be checked on every request.
- Exports must be permission-controlled and audited.
- Rate limiting must protect authentication, search, import, export, and public webhook endpoints.

## 26. Deployment And Operations

- Use separate environments for local, development, staging, and production.
- Use infrastructure as code where feasible.
- Use automated database backups with restore testing.
- Use structured logs, metrics, traces, and alerts.
- Track background worker queue health.
- Track integration sync failure rates.
- Track API latency and error rates by route.
- Track frontend error rates and mobile sync failures.
- Use feature flags for module rollout and risky new workflows.

## 27. Testing Strategy

- Test tenant isolation at the API, query, permission, and UI levels.
- Test role permissions for every module and critical action.
- Test data validation and status transition rules.
- Test import/export with success, partial failure, and invalid data cases.
- Test offline action queues with duplicate submissions and conflict cases.
- Test QuickBooks sync with retries and mapping failures.
- Test geofence calculations with edge cases around accuracy and boundary crossings.
- Test inventory movements with concurrent updates and rollback/correction flows.
- Test dispatch workflows with reassignment and exception cases.

- **Unit tests:** Required before production rollout for relevant modules.
- **API integration tests:** Required before production rollout for relevant modules.
- **Permission tests:** Required before production rollout for relevant modules.
- **End-to-end workflow tests:** Required before production rollout for relevant modules.
- **Offline sync tests:** Required before production rollout for relevant modules.
- **Load tests for location pings:** Required before production rollout for relevant modules.
- **Import/export tests:** Required before production rollout for relevant modules.
- **Worker retry tests:** Required before production rollout for relevant modules.
- **Security tests:** Required before production rollout for relevant modules.
- **Regression smoke tests:** Required before production rollout for relevant modules.
- **Mobile usability tests:** Required before production rollout for relevant modules.
- **Data migration tests:** Required before production rollout for relevant modules.

## 28. MVP Scope Recommendation

- MVP should deliver a usable operational system, not a thin demo.
- MVP should prioritize multi-company safety, CRM basics, outbound logging, tasks/calendar, field visits, check-ins, basic tracking, inventory basics, QuickBooks sync foundation, and essential dashboards.
- MVP should avoid advanced route optimization, advanced automation, full accounting, and overly complex record-level permissions unless required by launch customers.

### 28.1 MVP Included Capabilities

- Tenant and company authentication
- Company-level roles and permissions
- Core CRM accounts/contacts/leads/opportunities
- Activity timeline
- Outbound call/email/SMS/LinkedIn logging
- Tasks and calendar
- Site records and site visits
- Mobile check-ins and notes
- Photo attachments
- Basic vehicle and worker tracking
- Radius geofences
- Basic product catalog
- Warehouses and depots
- Stock balances and movements
- Receiving, transfer, and adjustment basics
- Basic dispatch assignment
- QuickBooks connection and sync log foundation
- Sales and operations dashboards
- Basic offline queue for field actions

### 28.2 MVP Deferred Capabilities

- Advanced route optimization
- Barcode scanning
- Lot and serial tracking unless immediately required
- Advanced customer portal
- Automated LinkedIn actions
- Full workflow automation builder
- Advanced BI semantic layer
- Marketplace integrations
- Enterprise SSO
- Native payroll
- Advanced IoT telemetry
- Complex ABAC permission rules

## 29. Phase Roadmap Overview

- **Phase 1:** Product Definition And Alignment
- **Phase 2:** Tenant, Identity, And Permission Foundation
- **Phase 3:** Core Platform Foundation
- **Phase 4:** CRM Data Model And Core UX
- **Phase 5:** Outbound Sales Workflows
- **Phase 6:** Calendar And Task System
- **Phase 7:** Field Sales And Site Work
- **Phase 8:** Products, Warehouses, Depots, And Inventory
- **Phase 9:** Orders, Dispatch, Routes, And Logistics
- **Phase 10:** Fleet, GPS Tracking, And Geofencing
- **Phase 11:** Service Requests And Work Orders
- **Phase 12:** Reporting And Dashboards
- **Phase 13:** QuickBooks And Integration Framework
- **Phase 14:** Offline Mobile And Sync Reliability
- **Phase 15:** Admin, Security, Monitoring, And Rollout
- **Phase 16:** Advanced Filters, Saved Views, And Custom Fields Hardening
- **Phase 17:** Automation And Workflow Rules
- **Phase 18:** Advanced Inventory And Barcode Expansion
- **Phase 19:** Advanced Dispatch Optimization
- **Phase 20:** Enterprise Readiness And Scale Hardening

## 30.1 Phase 1: Product Definition And Alignment

**Objective:** Create alignment around vision, personas, scope, non-goals, operating model, and success metrics before implementation begins.

**Key deliverables**
- Product vision brief
- Personas and role map
- MVP scope definition
- Non-goals list
- Success metrics
- Glossary
- Decision log

**Specific requirements**
- **P01-REQ-001:** Confirm first customer segment
- **P01-REQ-002:** Confirm drilling-specific workflows
- **P01-REQ-003:** Confirm module enablement strategy
- **P01-REQ-004:** Confirm deployment and tenancy assumptions
- **P01-REQ-005:** Confirm whether mobile is web-first or native later

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.2 Phase 2: Tenant, Identity, And Permission Foundation

**Objective:** Build safe multi-company identity, authentication, authorization, and membership foundations.

**Key deliverables**
- Tenant model
- Company model
- User model
- Membership model
- Role model
- Session handling
- Permission middleware
- Initial admin screens

**Specific requirements**
- **P02-REQ-001:** All records must be tenant scoped
- **P02-REQ-002:** Users can be invited to a company
- **P02-REQ-003:** Admins can assign roles
- **P02-REQ-004:** Permission checks exist server-side
- **P02-REQ-005:** Role changes are audited

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.3 Phase 3: Core Platform Foundation

**Objective:** Build shared platform services used by all modules.

**Key deliverables**
- Audit logs
- Notifications foundation
- File attachments
- Tags
- Custom fields foundation
- Global search foundation
- Import/export jobs
- System settings

**Specific requirements**
- **P03-REQ-001:** Activity-producing actions create logs
- **P03-REQ-002:** Files are permission checked
- **P03-REQ-003:** Tags are company scoped
- **P03-REQ-004:** Custom fields support basic types
- **P03-REQ-005:** Imports produce row errors

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.4 Phase 4: CRM Data Model And Core UX

**Objective:** Deliver CRM master data and sales pipeline foundation.

**Key deliverables**
- Accounts
- Contacts
- Leads
- Opportunities
- Pipelines
- Activity timeline
- CRM table and detail views

**Specific requirements**
- **P04-REQ-001:** Users can create and update CRM records
- **P04-REQ-002:** Duplicate indicators exist
- **P04-REQ-003:** Opportunity stage changes are tracked
- **P04-REQ-004:** Timeline shows activity
- **P04-REQ-005:** Filters support owner/status/date

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.5 Phase 5: Outbound Sales Workflows

**Objective:** Deliver outbound activity management and sales execution workflows.

**Key deliverables**
- Prospect lists
- Campaigns
- Sequences/cadences
- Call tasks
- Email logs
- SMS logs
- LinkedIn activity logs
- Follow-up queues

**Specific requirements**
- **P05-REQ-001:** Reps can log all channel activity
- **P05-REQ-002:** Managers can see activity metrics
- **P05-REQ-003:** Follow-ups can be generated
- **P05-REQ-004:** Sequences support manual steps
- **P05-REQ-005:** Conversion to opportunity works

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.6 Phase 6: Calendar And Task System

**Objective:** Build calendar, tasks, reminders, recurring work, and assignment foundations.

**Key deliverables**
- Task model
- Calendar event model
- Team calendar
- Recurring tasks
- Reminder engine
- SLA due dates

**Specific requirements**
- **P06-REQ-001:** Tasks can link to records
- **P06-REQ-002:** Assignees receive notifications
- **P06-REQ-003:** Overdue state is calculated
- **P06-REQ-004:** Recurring tasks generate future instances
- **P06-REQ-005:** Calendar supports visits and appointments

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.7 Phase 7: Field Sales And Site Work

**Objective:** Deliver field sales, site visits, location-aware check-ins, and job request capture.

**Key deliverables**
- Site records
- Visit scheduling
- Mobile visit list
- Check-in/check-out
- Field notes
- Photo capture
- Job request workflow

**Specific requirements**
- **P07-REQ-001:** Field users can work assigned visits
- **P07-REQ-002:** Check-ins capture GPS when available
- **P07-REQ-003:** Offline notes are queued
- **P07-REQ-004:** Photos attach to visits/sites
- **P07-REQ-005:** Job requests link to accounts and sites

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.8 Phase 8: Products, Warehouses, Depots, And Inventory

**Objective:** Deliver product catalog, warehouses, depots, stock balances, and movement history.

**Key deliverables**
- Products
- Inventory locations
- Bin basics
- Stock balances
- Stock movements
- Receiving
- Transfers
- Adjustments
- Low-stock alerts

**Specific requirements**
- **P08-REQ-001:** Stock movement is append-only
- **P08-REQ-002:** Balances update from movements
- **P08-REQ-003:** Adjustments require reason
- **P08-REQ-004:** Transfers support source/destination
- **P08-REQ-005:** Inventory views filter by warehouse/depot/product

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.9 Phase 9: Orders, Dispatch, Routes, And Logistics

**Objective:** Deliver operational dispatch workflows connecting orders, shipments, routes, stops, vehicles, drivers, and sites.

**Key deliverables**
- Orders
- Shipments
- Dispatch board
- Route plans
- Stops
- Driver assignments
- Proof of delivery
- Exception handling

**Specific requirements**
- **P09-REQ-001:** Dispatcher can assign work
- **P09-REQ-002:** Drivers see assigned stops
- **P09-REQ-003:** Stops capture arrival/completion
- **P09-REQ-004:** Exceptions are logged
- **P09-REQ-005:** Routes can be filtered by date/status/driver

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.10 Phase 10: Fleet, GPS Tracking, And Geofencing

**Objective:** Deliver vehicles, devices, GPS ingestion, live map, route replay, geofences, and alerts.

**Key deliverables**
- Vehicles
- Drivers
- Tracking devices
- Location ping ingestion
- Live map
- Location history
- Geofences
- Geofence events
- Tracking alerts

**Specific requirements**
- **P10-REQ-001:** Devices can be assigned
- **P10-REQ-002:** Map shows stale state
- **P10-REQ-003:** Geofence enter/exit is captured
- **P10-REQ-004:** Route replay supports time filters
- **P10-REQ-005:** Alerts are configurable

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.11 Phase 11: Service Requests And Work Orders

**Objective:** Deliver service requests, work orders, maintenance schedules, parts, labor, and service history.

**Key deliverables**
- Service requests
- Work orders
- Technician assignment
- Parts used
- Labor entries
- Maintenance schedules
- Service history

**Specific requirements**
- **P11-REQ-001:** Requests can become work orders
- **P11-REQ-002:** Technicians can complete assigned work
- **P11-REQ-003:** Parts can link to inventory
- **P11-REQ-004:** Labor is reportable
- **P11-REQ-005:** Service history appears on accounts/sites/assets

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.12 Phase 12: Reporting And Dashboards

**Objective:** Deliver first production dashboards and report foundations.

**Key deliverables**
- Sales dashboard
- Outbound dashboard
- Field dashboard
- Dispatch dashboard
- Inventory dashboard
- Fleet dashboard
- Integration dashboard
- Report definitions

**Specific requirements**
- **P12-REQ-001:** Reports are permission-aware
- **P12-REQ-002:** Filters are saved
- **P12-REQ-003:** Exports are audited
- **P12-REQ-004:** Dashboards load acceptably
- **P12-REQ-005:** Metrics have definitions

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.13 Phase 13: QuickBooks And Integration Framework

**Objective:** Deliver QuickBooks foundation and reusable integration framework.

**Key deliverables**
- Integration connection model
- QuickBooks OAuth/connect flow
- External ID mappings
- Sync jobs
- Sync logs
- Retry tools
- Webhook framework
- API key management

**Specific requirements**
- **P13-REQ-001:** Admins can connect QuickBooks
- **P13-REQ-002:** Sync failures are visible
- **P13-REQ-003:** Retries are safe
- **P13-REQ-004:** External IDs are stored
- **P13-REQ-005:** API keys are scoped and audited

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.14 Phase 14: Offline Mobile And Sync Reliability

**Objective:** Harden offline mobile workflows and sync reliability for field execution.

**Key deliverables**
- Offline cache
- Offline action queue
- Conflict handling
- Photo retry logic
- Sync status UI
- Mobile UX hardening

**Specific requirements**
- **P14-REQ-001:** Users can capture critical work offline
- **P14-REQ-002:** Actions sync idempotently
- **P14-REQ-003:** Conflicts are visible
- **P14-REQ-004:** Failed photos retry
- **P14-REQ-005:** No data loss during connectivity drops

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.15 Phase 15: Admin, Security, Monitoring, And Rollout

**Objective:** Prepare for secure production rollout with monitoring, backup, audit, permission hardening, and release controls.

**Key deliverables**
- Security review
- Monitoring dashboards
- Backup and restore runbook
- Release checklist
- Role QA matrix
- Operational runbooks
- Admin training

**Specific requirements**
- **P15-REQ-001:** Production deployment is observable
- **P15-REQ-002:** Backups are tested
- **P15-REQ-003:** Permission tests pass
- **P15-REQ-004:** Admins can manage rollout
- **P15-REQ-005:** Critical alerts are configured

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.16 Phase 16: Advanced Filters, Saved Views, And Custom Fields Hardening

**Objective:** Deepen cross-module saved views, filters, custom fields, and table UX.

**Key deliverables**
- Advanced saved views
- Role defaults
- Shared filters
- Field visibility rules
- Column presets
- Bulk update hardening

**Specific requirements**
- **P16-REQ-001:** Users can create reusable views
- **P16-REQ-002:** Admins can set defaults
- **P16-REQ-003:** Custom fields are searchable where appropriate
- **P16-REQ-004:** Bulk updates respect permissions

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.17 Phase 17: Automation And Workflow Rules

**Objective:** Add configurable workflow automation across CRM, field, dispatch, inventory, and service modules.

**Key deliverables**
- Rule builder
- Trigger definitions
- Action definitions
- Notification rules
- Assignment rules
- Escalation rules

**Specific requirements**
- **P17-REQ-001:** Rules are auditable
- **P17-REQ-002:** Rules can be tested before activation
- **P17-REQ-003:** Loops are prevented
- **P17-REQ-004:** Admins can disable broken rules

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.18 Phase 18: Advanced Inventory And Barcode Expansion

**Objective:** Expand inventory depth for barcode scanning, lot/serial tracking, advanced transfers, and reconciliation.

**Key deliverables**
- Barcode scanning
- Lot tracking
- Serial tracking
- Cycle counts
- Advanced receiving
- Inventory reconciliation

**Specific requirements**
- **P18-REQ-001:** Barcode actions are fast
- **P18-REQ-002:** Lot/serial fields are reportable
- **P18-REQ-003:** Cycle counts create adjustments
- **P18-REQ-004:** Reconciliation is auditable

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.19 Phase 19: Advanced Dispatch Optimization

**Objective:** Improve dispatch planning with optimization, capacity, constraints, route scoring, and suggested assignments.

**Key deliverables**
- Optimization inputs
- Route scoring
- Capacity constraints
- Suggested assignments
- Manual override workflow
- What-if planning

**Specific requirements**
- **P19-REQ-001:** Dispatchers remain in control
- **P19-REQ-002:** Suggestions explain reasoning
- **P19-REQ-003:** Manual overrides are tracked
- **P19-REQ-004:** Optimization respects constraints

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 30.20 Phase 20: Enterprise Readiness And Scale Hardening

**Objective:** Harden platform for enterprise scale, compliance, integrations, observability, and large customer onboarding.

**Key deliverables**
- Advanced tenancy options
- SSO/SAML later
- Data retention policies
- Advanced audit export
- Load testing
- Large import tooling
- Enterprise admin controls

**Specific requirements**
- **P20-REQ-001:** System handles larger datasets
- **P20-REQ-002:** Retention policies are configurable
- **P20-REQ-003:** Enterprise admin flows are documented
- **P20-REQ-004:** Performance budgets are met

**Design details to drill down next**
- Primary user journeys and wireframes.
- Module-specific data model fields and validation rules.
- API request/response contracts.
- Permissions and edge cases.
- Filter definitions and saved view behavior.
- Reporting metrics and event instrumentation.
- Acceptance criteria and QA scenarios.

**Implementation dependencies**
- Tenant and company scope must be available before company records are created.
- Audit logging must exist before high-impact operational changes launch.
- Permission middleware must be used by every backend endpoint.
- Shared UI patterns should be available before module screens scale.

**Risks**
- Scope creep can delay usable release.
- Overly complex permissions can slow implementation if introduced too early.
- Insufficient reporting events can require painful retrofits.
- Offline and integration failures can damage trust if not visible and recoverable.

**Exit criteria**
- The phase can be demoed end-to-end using realistic data.
- Role-based access is tested.
- Audit history exists for important changes.
- Error states and empty states are handled.
- Documentation is updated for product, design, engineering, and QA.

## 31. Open Questions To Resolve

1. Should companies use shared database tenant separation, isolated databases, or a hybrid model for enterprise customers?
2. Should branches, territories, depots, warehouses, and service areas be separate hierarchy levels or configurable location types?
3. Should LinkedIn remain logging-only, or should the product include reminders, templates, and compliance checks around LinkedIn workflows?
4. Should quotes and pricing be part of MVP or a later dedicated phase?
5. Should invoices be created inside the platform, synced to QuickBooks, or created only in QuickBooks?
6. Should inventory MVP be quantity-only, or does launch require serial/lot tracking?
7. Is barcode scanning required in MVP for warehouses and depots?
8. Should tracking devices be manually assigned, automatically assigned, or both?
9. Should dispatch selection be primarily manual, proximity-based, capacity-based, route-optimized, or a hybrid?
10. Should reports include scheduled email delivery in MVP?
11. Should field mobile be delivered as responsive web first or native app first?
12. What GPS providers or tracker devices must be supported first?
13. What exact QuickBooks objects must sync in the first release?
14. How long should raw GPS pings be retained?
15. Which operational events require customer notifications?
16. Does the first customer require multilingual UI or only English?
17. What countries, tax models, and units of measure must be supported at launch?
18. What customer data import sources exist today?
19. What current spreadsheets or legacy systems must be migrated?
20. Who approves inventory adjustments and dispatch exceptions?

## 32. Future Detailed Documents To Create

- Phase 1 Product Scope Document
- Personas And Workflow Map
- Domain Model And MongoDB Schema Document
- Tenancy And Permissions Architecture Document
- CRM And Outbound Sales Requirements Document
- Field Operations And Drilling Workflow Document
- Inventory, Warehouse, And Depot Requirements Document
- Dispatch, Logistics, Fleet, And GPS Requirements Document
- Service And Work Orders Requirements Document
- Reporting And Analytics Metrics Dictionary
- QuickBooks Integration Architecture Document
- Offline Mobile Sync Design Document
- API Standards And Endpoint Contract Document
- UI Component And Page Pattern Document
- QA Test Plan And Acceptance Criteria Document
- Release, Monitoring, Backup, And Rollout Runbook

## 33. Glossary

- **Tenant:** Top-level isolation boundary for SaaS operation.
- **Company:** Customer organization inside the platform.
- **Branch:** Operational subdivision of a company.
- **Depot:** Vehicle, truck, or inventory staging location.
- **Warehouse:** Inventory storage and fulfillment location.
- **Site:** Physical customer or job location where field work happens.
- **Geofence:** Virtual boundary used for location-aware events.
- **Check-in:** User action proving arrival or presence at a location.
- **Activity:** Timeline event connected to CRM or operational records.
- **Opportunity:** Potential revenue deal in CRM pipeline.
- **Job:** Operational work item to be scheduled, dispatched, and completed.
- **Work Order:** Service execution record assigned to technician or team.
- **Stock Movement:** Append-only inventory event that changes stock state.
- **Sync Job:** Background integration task that creates or updates external system data.
- **Saved View:** Reusable table/report configuration containing filters, columns, sorting, and grouping.

## 34. Master Acceptance Criteria

- **MAC-001:** The system supports multiple companies without data leakage.
- **MAC-002:** Users see only permitted modules and records.
- **MAC-003:** Core CRM records can be created, updated, filtered, searched, and audited.
- **MAC-004:** Outbound activity can be logged across call, email, SMS, and LinkedIn manual activity.
- **MAC-005:** Tasks and calendar events can be assigned, completed, and reported.
- **MAC-006:** Field visits support check-in, notes, photos, and follow-up actions.
- **MAC-007:** Inventory movements update stock balances and preserve history.
- **MAC-008:** Dispatch workflows connect orders/jobs, vehicles, drivers, routes, stops, and exceptions.
- **MAC-009:** GPS tracking supports current location, stale state, history, and geofence events.
- **MAC-010:** Service work orders support assignment, parts, labor, notes, and completion.
- **MAC-011:** QuickBooks sync foundation stores external IDs, logs sync attempts, and exposes errors.
- **MAC-012:** Dashboards provide useful operational visibility with filters.
- **MAC-013:** Offline mobile workflows prevent data loss for critical field actions.
- **MAC-014:** Audit logs preserve meaningful business and security events.
- **MAC-015:** The system can be rolled out safely with monitoring, backups, and admin controls.

## 35. Recommended Immediate Next Step

- Use this master document as the baseline for a focused Phase 1 Product Scope Document.
- For Phase 1, define personas, non-goals, MVP boundaries, success metrics, first customer workflows, module enablement, and exact rollout assumptions.
- After Phase 1 is approved, create the Domain Model and Tenancy/Permissions documents before designing individual screens in detail.

## 36. Requirement Catalogue For Detailed Phase Planning

### 36.1 Data Safety Requirements

- **CAT-01-001:** Tenant scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-002:** Company scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-003:** Soft delete is preferred for business records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-004:** Audit high-impact changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-005:** Validate foreign keys logically; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-006:** Use immutable event records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-007:** Protect exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-008:** Prevent cross-company search leaks; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-009:** Tenant scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-010:** Company scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-011:** Soft delete is preferred for business records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-012:** Audit high-impact changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-013:** Validate foreign keys logically; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-014:** Use immutable event records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-015:** Protect exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-016:** Prevent cross-company search leaks; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-017:** Tenant scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-018:** Company scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-019:** Soft delete is preferred for business records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-020:** Audit high-impact changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-021:** Validate foreign keys logically; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-022:** Use immutable event records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-023:** Protect exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-024:** Prevent cross-company search leaks; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-025:** Tenant scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-026:** Company scope is mandatory; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-027:** Soft delete is preferred for business records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-028:** Audit high-impact changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-029:** Validate foreign keys logically; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-01-030:** Use immutable event records; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.2 User Experience Requirements

- **CAT-02-001:** Provide empty states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-002:** Provide loading states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-003:** Provide error recovery; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-004:** Support saved views; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-005:** Support bulk actions carefully; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-006:** Support responsive layouts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-007:** Use consistent status badges; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-008:** Use timeline patterns; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-009:** Provide empty states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-010:** Provide loading states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-011:** Provide error recovery; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-012:** Support saved views; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-013:** Support bulk actions carefully; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-014:** Support responsive layouts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-015:** Use consistent status badges; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-016:** Use timeline patterns; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-017:** Provide empty states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-018:** Provide loading states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-019:** Provide error recovery; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-020:** Support saved views; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-021:** Support bulk actions carefully; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-022:** Support responsive layouts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-023:** Use consistent status badges; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-024:** Use timeline patterns; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-025:** Provide empty states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-026:** Provide loading states; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-027:** Provide error recovery; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-028:** Support saved views; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-029:** Support bulk actions carefully; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-02-030:** Support responsive layouts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.3 Operations Requirements

- **CAT-03-001:** Support assignments; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-002:** Support reassignment; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-003:** Track planned vs actual times; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-004:** Track exceptions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-005:** Capture proof; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-006:** Capture notes and photos; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-007:** Support manager review; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-008:** Expose overdue work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-009:** Support assignments; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-010:** Support reassignment; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-011:** Track planned vs actual times; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-012:** Track exceptions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-013:** Capture proof; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-014:** Capture notes and photos; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-015:** Support manager review; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-016:** Expose overdue work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-017:** Support assignments; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-018:** Support reassignment; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-019:** Track planned vs actual times; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-020:** Track exceptions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-021:** Capture proof; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-022:** Capture notes and photos; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-023:** Support manager review; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-024:** Expose overdue work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-025:** Support assignments; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-026:** Support reassignment; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-027:** Track planned vs actual times; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-028:** Track exceptions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-029:** Capture proof; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-03-030:** Capture notes and photos; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.4 Inventory Requirements

- **CAT-04-001:** Track source and destination; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-002:** Require reason codes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-003:** Preserve movement history; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-004:** Support low stock thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-005:** Support transfers; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-006:** Support receiving; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-007:** Support picking; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-008:** Support adjustment approvals later; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-009:** Track source and destination; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-010:** Require reason codes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-011:** Preserve movement history; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-012:** Support low stock thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-013:** Support transfers; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-014:** Support receiving; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-015:** Support picking; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-016:** Support adjustment approvals later; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-017:** Track source and destination; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-018:** Require reason codes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-019:** Preserve movement history; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-020:** Support low stock thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-021:** Support transfers; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-022:** Support receiving; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-023:** Support picking; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-024:** Support adjustment approvals later; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-025:** Track source and destination; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-026:** Require reason codes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-027:** Preserve movement history; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-028:** Support low stock thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-029:** Support transfers; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-04-030:** Support receiving; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.5 GPS Requirements

- **CAT-05-001:** Capture accuracy; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-002:** Display stale state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-003:** Track source; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-004:** Support geofence events; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-005:** Support route replay; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-006:** Support manual override; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-007:** Support device health; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-008:** Support alert thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-009:** Capture accuracy; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-010:** Display stale state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-011:** Track source; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-012:** Support geofence events; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-013:** Support route replay; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-014:** Support manual override; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-015:** Support device health; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-016:** Support alert thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-017:** Capture accuracy; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-018:** Display stale state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-019:** Track source; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-020:** Support geofence events; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-021:** Support route replay; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-022:** Support manual override; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-023:** Support device health; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-024:** Support alert thresholds; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-025:** Capture accuracy; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-026:** Display stale state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-027:** Track source; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-028:** Support geofence events; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-029:** Support route replay; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-05-030:** Support manual override; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.6 Integrations Requirements

- **CAT-06-001:** Store external IDs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-002:** Use sync jobs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-003:** Expose errors; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-004:** Support retries; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-005:** Map fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-006:** Audit payload references; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-007:** Rate limit webhooks; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-008:** Support reconnect; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-009:** Store external IDs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-010:** Use sync jobs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-011:** Expose errors; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-012:** Support retries; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-013:** Map fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-014:** Audit payload references; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-015:** Rate limit webhooks; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-016:** Support reconnect; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-017:** Store external IDs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-018:** Use sync jobs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-019:** Expose errors; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-020:** Support retries; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-021:** Map fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-022:** Audit payload references; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-023:** Rate limit webhooks; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-024:** Support reconnect; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-025:** Store external IDs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-026:** Use sync jobs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-027:** Expose errors; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-028:** Support retries; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-029:** Map fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-06-030:** Audit payload references; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.7 Reporting Requirements

- **CAT-07-001:** Define metrics; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-002:** Store timestamps; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-003:** Support filters; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-004:** Support exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-005:** Support rollups; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-006:** Respect permissions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-007:** Track freshness; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-008:** Document definitions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-009:** Define metrics; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-010:** Store timestamps; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-011:** Support filters; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-012:** Support exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-013:** Support rollups; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-014:** Respect permissions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-015:** Track freshness; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-016:** Document definitions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-017:** Define metrics; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-018:** Store timestamps; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-019:** Support filters; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-020:** Support exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-021:** Support rollups; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-022:** Respect permissions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-023:** Track freshness; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-024:** Document definitions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-025:** Define metrics; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-026:** Store timestamps; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-027:** Support filters; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-028:** Support exports; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-029:** Support rollups; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-07-030:** Respect permissions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.8 Security Requirements

- **CAT-08-001:** Authenticate APIs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-002:** Authorize actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-003:** Protect files; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-004:** Log admin changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-005:** Scope API keys; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-006:** Rotate secrets; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-007:** Use least privilege; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-008:** Monitor suspicious activity; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-009:** Authenticate APIs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-010:** Authorize actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-011:** Protect files; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-012:** Log admin changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-013:** Scope API keys; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-014:** Rotate secrets; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-015:** Use least privilege; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-016:** Monitor suspicious activity; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-017:** Authenticate APIs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-018:** Authorize actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-019:** Protect files; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-020:** Log admin changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-021:** Scope API keys; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-022:** Rotate secrets; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-023:** Use least privilege; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-024:** Monitor suspicious activity; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-025:** Authenticate APIs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-026:** Authorize actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-027:** Protect files; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-028:** Log admin changes; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-029:** Scope API keys; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-08-030:** Rotate secrets; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.9 Mobile Requirements

- **CAT-09-001:** Cache assigned work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-002:** Queue offline actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-003:** Retry uploads; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-004:** Show sync state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-005:** Avoid data loss; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-006:** Handle conflicts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-007:** Optimize forms; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-008:** Minimize typing; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-009:** Cache assigned work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-010:** Queue offline actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-011:** Retry uploads; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-012:** Show sync state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-013:** Avoid data loss; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-014:** Handle conflicts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-015:** Optimize forms; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-016:** Minimize typing; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-017:** Cache assigned work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-018:** Queue offline actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-019:** Retry uploads; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-020:** Show sync state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-021:** Avoid data loss; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-022:** Handle conflicts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-023:** Optimize forms; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-024:** Minimize typing; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-025:** Cache assigned work; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-026:** Queue offline actions; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-027:** Retry uploads; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-028:** Show sync state; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-029:** Avoid data loss; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-09-030:** Handle conflicts; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

### 36.10 Admin Requirements

- **CAT-10-001:** Configure modules; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-002:** Manage users; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-003:** Manage roles; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-004:** Manage tags; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-005:** Manage custom fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-006:** View audit logs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-007:** Manage integrations; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-008:** Configure notifications; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-009:** Configure modules; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-010:** Manage users; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-011:** Manage roles; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-012:** Manage tags; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-013:** Manage custom fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-014:** View audit logs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-015:** Manage integrations; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-016:** Configure notifications; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-017:** Configure modules; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-018:** Manage users; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-019:** Manage roles; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-020:** Manage tags; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-021:** Manage custom fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-022:** View audit logs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-023:** Manage integrations; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-024:** Configure notifications; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-025:** Configure modules; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-026:** Manage users; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-027:** Manage roles; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-028:** Manage tags; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-029:** Manage custom fields; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.
- **CAT-10-030:** View audit logs; define exact behavior, permissions, validation, edge cases, API contract, UI state, reporting impact, and QA scenario in the relevant phase document.

## 37. Appendix: Page Inventory Draft

### 37.1 Core/Admin Pages

- **Page:** Tenant list
  - Purpose: Provide a focused workspace for tenant list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Company list
  - Purpose: Provide a focused workspace for company list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Company detail
  - Purpose: Provide a focused workspace for company detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** User list
  - Purpose: Provide a focused workspace for user list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** User invite
  - Purpose: Provide a focused workspace for user invite.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Role editor
  - Purpose: Provide a focused workspace for role editor.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Team editor
  - Purpose: Provide a focused workspace for team editor.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Module settings
  - Purpose: Provide a focused workspace for module settings.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Audit log
  - Purpose: Provide a focused workspace for audit log.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Notification settings
  - Purpose: Provide a focused workspace for notification settings.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** File manager
  - Purpose: Provide a focused workspace for file manager.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Import jobs
  - Purpose: Provide a focused workspace for import jobs.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Export jobs
  - Purpose: Provide a focused workspace for export jobs.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** API keys
  - Purpose: Provide a focused workspace for api keys.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Webhook settings
  - Purpose: Provide a focused workspace for webhook settings.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.2 CRM Pages

- **Page:** Account list
  - Purpose: Provide a focused workspace for account list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Account detail
  - Purpose: Provide a focused workspace for account detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Contact list
  - Purpose: Provide a focused workspace for contact list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Contact detail
  - Purpose: Provide a focused workspace for contact detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Lead list
  - Purpose: Provide a focused workspace for lead list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Lead detail
  - Purpose: Provide a focused workspace for lead detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Opportunity board
  - Purpose: Provide a focused workspace for opportunity board.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Opportunity detail
  - Purpose: Provide a focused workspace for opportunity detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Pipeline settings
  - Purpose: Provide a focused workspace for pipeline settings.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Activity timeline
  - Purpose: Provide a focused workspace for activity timeline.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Duplicate review
  - Purpose: Provide a focused workspace for duplicate review.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.3 Outbound Pages

- **Page:** Prospect list
  - Purpose: Provide a focused workspace for prospect list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Campaign list
  - Purpose: Provide a focused workspace for campaign list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Campaign detail
  - Purpose: Provide a focused workspace for campaign detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Sequence builder
  - Purpose: Provide a focused workspace for sequence builder.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Call queue
  - Purpose: Provide a focused workspace for call queue.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Follow-up queue
  - Purpose: Provide a focused workspace for follow-up queue.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Rep performance
  - Purpose: Provide a focused workspace for rep performance.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Activity log review
  - Purpose: Provide a focused workspace for activity log review.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.4 Calendar/Tasks Pages

- **Page:** My tasks
  - Purpose: Provide a focused workspace for my tasks.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Team tasks
  - Purpose: Provide a focused workspace for team tasks.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Calendar day view
  - Purpose: Provide a focused workspace for calendar day view.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Calendar week view
  - Purpose: Provide a focused workspace for calendar week view.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Calendar month view
  - Purpose: Provide a focused workspace for calendar month view.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Task detail
  - Purpose: Provide a focused workspace for task detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Recurring task settings
  - Purpose: Provide a focused workspace for recurring task settings.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Reminder settings
  - Purpose: Provide a focused workspace for reminder settings.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.5 Field Pages

- **Page:** Site list
  - Purpose: Provide a focused workspace for site list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Site detail
  - Purpose: Provide a focused workspace for site detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Visit list
  - Purpose: Provide a focused workspace for visit list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Visit detail
  - Purpose: Provide a focused workspace for visit detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Mobile assigned visits
  - Purpose: Provide a focused workspace for mobile assigned visits.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Check-in screen
  - Purpose: Provide a focused workspace for check-in screen.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Field note form
  - Purpose: Provide a focused workspace for field note form.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Photo review
  - Purpose: Provide a focused workspace for photo review.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Job request form
  - Purpose: Provide a focused workspace for job request form.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.6 Inventory Pages

- **Page:** Product list
  - Purpose: Provide a focused workspace for product list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Product detail
  - Purpose: Provide a focused workspace for product detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Warehouse list
  - Purpose: Provide a focused workspace for warehouse list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Depot list
  - Purpose: Provide a focused workspace for depot list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Stock balance view
  - Purpose: Provide a focused workspace for stock balance view.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Stock movement history
  - Purpose: Provide a focused workspace for stock movement history.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Receiving screen
  - Purpose: Provide a focused workspace for receiving screen.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Transfer screen
  - Purpose: Provide a focused workspace for transfer screen.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Adjustment screen
  - Purpose: Provide a focused workspace for adjustment screen.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Low-stock view
  - Purpose: Provide a focused workspace for low-stock view.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.7 Dispatch Pages

- **Page:** Dispatch board
  - Purpose: Provide a focused workspace for dispatch board.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Order list
  - Purpose: Provide a focused workspace for order list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Order detail
  - Purpose: Provide a focused workspace for order detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Shipment list
  - Purpose: Provide a focused workspace for shipment list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Shipment detail
  - Purpose: Provide a focused workspace for shipment detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Route planner
  - Purpose: Provide a focused workspace for route planner.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Stop detail
  - Purpose: Provide a focused workspace for stop detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Exception queue
  - Purpose: Provide a focused workspace for exception queue.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Proof review
  - Purpose: Provide a focused workspace for proof review.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.8 Fleet Pages

- **Page:** Vehicle list
  - Purpose: Provide a focused workspace for vehicle list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Vehicle detail
  - Purpose: Provide a focused workspace for vehicle detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Driver list
  - Purpose: Provide a focused workspace for driver list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Driver detail
  - Purpose: Provide a focused workspace for driver detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Device list
  - Purpose: Provide a focused workspace for device list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Device detail
  - Purpose: Provide a focused workspace for device detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Live map
  - Purpose: Provide a focused workspace for live map.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Route replay
  - Purpose: Provide a focused workspace for route replay.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Geofence editor
  - Purpose: Provide a focused workspace for geofence editor.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Tracking alerts
  - Purpose: Provide a focused workspace for tracking alerts.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.9 Service Pages

- **Page:** Service request list
  - Purpose: Provide a focused workspace for service request list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Service request detail
  - Purpose: Provide a focused workspace for service request detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Work order list
  - Purpose: Provide a focused workspace for work order list.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Work order detail
  - Purpose: Provide a focused workspace for work order detail.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Technician mobile work
  - Purpose: Provide a focused workspace for technician mobile work.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Maintenance schedule
  - Purpose: Provide a focused workspace for maintenance schedule.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Parts and labor review
  - Purpose: Provide a focused workspace for parts and labor review.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

### 37.10 Reports Pages

- **Page:** Dashboard home
  - Purpose: Provide a focused workspace for dashboard home.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Sales dashboard
  - Purpose: Provide a focused workspace for sales dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Outbound dashboard
  - Purpose: Provide a focused workspace for outbound dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Field dashboard
  - Purpose: Provide a focused workspace for field dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Dispatch dashboard
  - Purpose: Provide a focused workspace for dispatch dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Inventory dashboard
  - Purpose: Provide a focused workspace for inventory dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Fleet dashboard
  - Purpose: Provide a focused workspace for fleet dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Service dashboard
  - Purpose: Provide a focused workspace for service dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Integration dashboard
  - Purpose: Provide a focused workspace for integration dashboard.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Custom report builder
  - Purpose: Provide a focused workspace for custom report builder.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.
- **Page:** Saved reports
  - Purpose: Provide a focused workspace for saved reports.
  - Required states: loading, empty, filtered empty, permission denied, validation error, success, partial failure where relevant.
  - Required controls: search, filters, sorting, action buttons, record navigation, and contextual help where relevant.
  - Required audit behavior: high-impact actions must write audit entries.

## 38. Appendix: API Object Response Standards

- Every list response should include `items`, `next_cursor`, `total_count` when feasible, and `applied_filters`.
- Every detail response should include the record, related permissions, and useful display metadata.
- Every mutation response should include updated record state and emitted workflow events when useful.
- Every validation error should include field path, code, and message.
- Every async job creation should return job ID, status, and status endpoint.
- Every export job should include audit metadata and expiration date for download link.

## 39. Appendix: Design System Notes

- Use consistent status badge colors and labels across modules.
- Use consistent table action placement.
- Use consistent create/edit patterns per module complexity.
- Use timeline components for activities, audit summaries, job events, dispatch events, and service history.
- Use map marker patterns that distinguish vehicles, users, sites, warehouses, depots, routes, and alerts.
- Use mobile bottom actions for field execution screens.
- Use drawer panels for quick edits and full pages for complex workflows.
- Use confirmation modals for destructive or high-impact actions.

## 40. Final Recommendation

- Build one multi-tenant core platform.
- Keep modules optional and configurable per company.
- Unify CRM, field operations, inventory, dispatch, fleet, and service through shared accounts, tasks, activities, audit logs, and reports.
- Treat QuickBooks, reporting, and offline mobile as first-class architecture concerns.
- Ship a focused MVP that is operationally useful before expanding into advanced automation and optimization.
- Use this document as the master reference, then drill into each phase with dedicated design, requirements, API, data model, filters, and acceptance documents.

## 41. Appendix: Traceability Matrix Starter

| Trace ID | Phase | Area | Planning Note |
| --- | --- | --- | --- |
| P01-Core | Phase 1 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-CRM | Phase 1 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Outbound | Phase 1 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Calendar | Phase 1 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Field | Phase 1 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Inventory | Phase 1 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Dispatch | Phase 1 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Fleet | Phase 1 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Service | Phase 1 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Reports | Phase 1 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Integrations | Phase 1 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Mobile | Phase 1 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P01-Security | Phase 1 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Core | Phase 2 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-CRM | Phase 2 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Outbound | Phase 2 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Calendar | Phase 2 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Field | Phase 2 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Inventory | Phase 2 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Dispatch | Phase 2 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Fleet | Phase 2 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Service | Phase 2 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Reports | Phase 2 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Integrations | Phase 2 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Mobile | Phase 2 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P02-Security | Phase 2 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Core | Phase 3 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-CRM | Phase 3 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Outbound | Phase 3 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Calendar | Phase 3 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Field | Phase 3 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Inventory | Phase 3 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Dispatch | Phase 3 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Fleet | Phase 3 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Service | Phase 3 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Reports | Phase 3 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Integrations | Phase 3 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Mobile | Phase 3 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P03-Security | Phase 3 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Core | Phase 4 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-CRM | Phase 4 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Outbound | Phase 4 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Calendar | Phase 4 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Field | Phase 4 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Inventory | Phase 4 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Dispatch | Phase 4 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Fleet | Phase 4 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Service | Phase 4 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Reports | Phase 4 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Integrations | Phase 4 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Mobile | Phase 4 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P04-Security | Phase 4 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Core | Phase 5 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-CRM | Phase 5 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Outbound | Phase 5 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Calendar | Phase 5 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Field | Phase 5 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Inventory | Phase 5 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Dispatch | Phase 5 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Fleet | Phase 5 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Service | Phase 5 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Reports | Phase 5 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Integrations | Phase 5 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Mobile | Phase 5 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P05-Security | Phase 5 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Core | Phase 6 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-CRM | Phase 6 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Outbound | Phase 6 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Calendar | Phase 6 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Field | Phase 6 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Inventory | Phase 6 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Dispatch | Phase 6 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Fleet | Phase 6 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Service | Phase 6 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Reports | Phase 6 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Integrations | Phase 6 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Mobile | Phase 6 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P06-Security | Phase 6 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Core | Phase 7 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-CRM | Phase 7 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Outbound | Phase 7 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Calendar | Phase 7 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Field | Phase 7 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Inventory | Phase 7 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Dispatch | Phase 7 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Fleet | Phase 7 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Service | Phase 7 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Reports | Phase 7 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Integrations | Phase 7 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Mobile | Phase 7 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P07-Security | Phase 7 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Core | Phase 8 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-CRM | Phase 8 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Outbound | Phase 8 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Calendar | Phase 8 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Field | Phase 8 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Inventory | Phase 8 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Dispatch | Phase 8 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Fleet | Phase 8 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Service | Phase 8 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Reports | Phase 8 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Integrations | Phase 8 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Mobile | Phase 8 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P08-Security | Phase 8 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Core | Phase 9 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-CRM | Phase 9 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Outbound | Phase 9 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Calendar | Phase 9 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Field | Phase 9 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Inventory | Phase 9 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Dispatch | Phase 9 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Fleet | Phase 9 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Service | Phase 9 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Reports | Phase 9 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Integrations | Phase 9 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Mobile | Phase 9 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P09-Security | Phase 9 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Core | Phase 10 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-CRM | Phase 10 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Outbound | Phase 10 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Calendar | Phase 10 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Field | Phase 10 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Inventory | Phase 10 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Dispatch | Phase 10 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Fleet | Phase 10 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Service | Phase 10 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Reports | Phase 10 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Integrations | Phase 10 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Mobile | Phase 10 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P10-Security | Phase 10 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Core | Phase 11 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-CRM | Phase 11 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Outbound | Phase 11 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Calendar | Phase 11 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Field | Phase 11 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Inventory | Phase 11 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Dispatch | Phase 11 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Fleet | Phase 11 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Service | Phase 11 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Reports | Phase 11 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Integrations | Phase 11 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Mobile | Phase 11 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P11-Security | Phase 11 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Core | Phase 12 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-CRM | Phase 12 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Outbound | Phase 12 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Calendar | Phase 12 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Field | Phase 12 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Inventory | Phase 12 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Dispatch | Phase 12 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Fleet | Phase 12 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Service | Phase 12 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Reports | Phase 12 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Integrations | Phase 12 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Mobile | Phase 12 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P12-Security | Phase 12 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Core | Phase 13 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-CRM | Phase 13 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Outbound | Phase 13 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Calendar | Phase 13 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Field | Phase 13 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Inventory | Phase 13 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Dispatch | Phase 13 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Fleet | Phase 13 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Service | Phase 13 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Reports | Phase 13 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Integrations | Phase 13 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Mobile | Phase 13 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P13-Security | Phase 13 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Core | Phase 14 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-CRM | Phase 14 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Outbound | Phase 14 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Calendar | Phase 14 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Field | Phase 14 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Inventory | Phase 14 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Dispatch | Phase 14 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Fleet | Phase 14 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Service | Phase 14 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Reports | Phase 14 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Integrations | Phase 14 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Mobile | Phase 14 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P14-Security | Phase 14 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Core | Phase 15 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-CRM | Phase 15 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Outbound | Phase 15 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Calendar | Phase 15 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Field | Phase 15 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Inventory | Phase 15 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Dispatch | Phase 15 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Fleet | Phase 15 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Service | Phase 15 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Reports | Phase 15 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Integrations | Phase 15 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Mobile | Phase 15 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P15-Security | Phase 15 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Core | Phase 16 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-CRM | Phase 16 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Outbound | Phase 16 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Calendar | Phase 16 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Field | Phase 16 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Inventory | Phase 16 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Dispatch | Phase 16 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Fleet | Phase 16 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Service | Phase 16 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Reports | Phase 16 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Integrations | Phase 16 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Mobile | Phase 16 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P16-Security | Phase 16 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Core | Phase 17 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-CRM | Phase 17 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Outbound | Phase 17 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Calendar | Phase 17 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Field | Phase 17 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Inventory | Phase 17 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Dispatch | Phase 17 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Fleet | Phase 17 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Service | Phase 17 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Reports | Phase 17 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Integrations | Phase 17 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Mobile | Phase 17 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P17-Security | Phase 17 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Core | Phase 18 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-CRM | Phase 18 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Outbound | Phase 18 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Calendar | Phase 18 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Field | Phase 18 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Inventory | Phase 18 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Dispatch | Phase 18 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Fleet | Phase 18 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Service | Phase 18 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Reports | Phase 18 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Integrations | Phase 18 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Mobile | Phase 18 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P18-Security | Phase 18 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Core | Phase 19 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-CRM | Phase 19 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Outbound | Phase 19 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Calendar | Phase 19 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Field | Phase 19 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Inventory | Phase 19 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Dispatch | Phase 19 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Fleet | Phase 19 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Service | Phase 19 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Reports | Phase 19 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Integrations | Phase 19 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Mobile | Phase 19 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P19-Security | Phase 19 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Core | Phase 20 | Core | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-CRM | Phase 20 | CRM | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Outbound | Phase 20 | Outbound | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Calendar | Phase 20 | Calendar | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Field | Phase 20 | Field | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Inventory | Phase 20 | Inventory | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Dispatch | Phase 20 | Dispatch | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Fleet | Phase 20 | Fleet | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Service | Phase 20 | Service | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Reports | Phase 20 | Reports | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Integrations | Phase 20 | Integrations | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Mobile | Phase 20 | Mobile | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
| P20-Security | Phase 20 | Security | Define detailed requirement, owner, status, design link, API link, test case, and release flag during phase planning. |
