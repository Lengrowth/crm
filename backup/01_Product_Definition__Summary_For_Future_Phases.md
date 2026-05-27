# Summary for Future Phases

## Source Document

This summary is derived from `01_Product_Definition.md`.

## Phase Purpose

Phase 01 established the official product foundation for the platform before technical architecture, detailed feature specifications, UI designs, APIs, permissions, integrations, or implementation plans are created. It defines what the platform is, who it serves, which problems it solves, what belongs in the MVP, what is intentionally excluded, and which product-level constraints all later phase documents must respect.

Phase 01 is a product-definition document, not a low-level implementation specification. Later phases must expand details, but must not contradict the product positioning, MVP boundaries, personas, modules, workflows, and constraints defined here.

## Final Decisions Made

- The platform is one unified multi-company SaaS platform.
- CRM, outbound sales, field operations, drilling, logistics, inventory, warehouse/depot operations, fleet/device tracking, service/work orders, reporting, notifications, search, integrations, admin/security, and offline mobile belong in one modular platform.
- The product is a CRM plus operations platform, not a generic CRM only.
- The product is not a fleet tracker only.
- The product is not a field-service app only.
- The product is not a warehouse management system only.
- The product is not a full ERP, accounting, payroll, HR, or marketing automation replacement in the first version.
- QuickBooks is the first accounting integration.
- QuickBooks must be treated as a sync integration, not the operational source of truth.
- Desktop-first UX is required for managers, dispatchers, admins, analysts, warehouse managers, and operators doing complex planning or reporting.
- Mobile workflows are required for field execution roles such as field sales reps, drivers, service technicians, and field managers.
- Offline-friendly capture is required for critical field workflows.
- Reporting must be designed from the beginning.
- Auditability is required for important administrative, operational, inventory, dispatch, sync, export, and permission-related actions.
- The MVP should focus on visibility, execution, CRM, field activity, inventory basics, tracking basics, QuickBooks foundation, and basic dashboards.
- Advanced optimization, full offline app parity, advanced AI, full accounting replacement, payroll, HR, complex ERP, advanced route optimization, and complex WMS features are excluded from MVP unless later confirmed.

## Product Vision

The product vision is to become the unified operating system for companies that sell, dispatch, track, deliver, service, and report on field work. The platform connects CRM and operations so management can see the full lifecycle from first contact to completed work without forcing teams to jump between disconnected spreadsheets, CRMs, dispatch boards, fleet trackers, warehouse systems, service systems, and accounting sync logs.

The platform must support both sales-first companies, where outbound and pipeline activity create operational demand, and operations-first companies, where dispatch, field execution, inventory, vehicles, and service history are the daily center of work. It must remain modular while preserving shared records, activity history, permissions, reporting, search, auditability, and integration foundations.

## Product Mission

The mission is to help operational companies manage customer relationships and field execution in one practical system. The platform should help companies manage accounts, leads, opportunities, outbound activity, tasks, appointments, site visits, crews, jobs, vehicles, drivers, depots, warehouses, inventory, service work, proof capture, QuickBooks sync, and performance reporting without losing the context between sales promises and operational delivery.

## Product Positioning

| Area | Summary |
| --- | --- |
| Category | Modular multi-company SaaS CRM plus operations platform for field, dispatch, inventory, fleet, service, reporting, and accounting-connected workflows. |
| Primary value proposition | One operational source of truth from sales activity and customer commitments through dispatch, field execution, inventory usage, proof capture, service work, reporting, and QuickBooks sync visibility. |
| Differentiation from generic CRM | Generic CRMs usually stop at leads, accounts, opportunities, and activities. This platform continues into site work, dispatch, fleet, inventory, service execution, proof capture, and accounting sync visibility. |
| Differentiation from field-service software | Pure field-service tools usually start when work is requested. This platform includes outbound sales, CRM history, opportunity context, customer relationship management, and pipeline-to-work handoff. |
| Differentiation from fleet tracking tools | Fleet trackers show vehicles and locations. This platform connects vehicles and drivers to jobs, dispatch, stops, field proof, inventory movement, customer records, and reporting. |
| Why CRM plus operations matters | Sales promises become operational commitments. If CRM and operations are disconnected, teams lose context, managers lose visibility, and customers experience delays or inconsistent follow-through. |

## Target Customer Segments

| Segment | Main pain points | Most relevant modules | MVP relevance |
| --- | --- | --- | --- |
| Drilling and field-service companies | Informal sales handoffs, lost site details, unclear crew readiness, scattered field proof. | CRM; Field Sales / Site Work; Drilling Operations; Dispatch; Fleet; Inventory; Reporting; QuickBooks. | High; likely first vertical focus and strong MVP validation fit. |
| Logistics and delivery operations | Manual dispatch, low visibility into vehicles/stops, phone-based exception handling, inconsistent proof. | Orders / Dispatch / Logistics; Fleet; Inventory; Mobile; Reporting. | Medium; support basic dispatch visibility, but not advanced optimization. |
| B2B sales teams with field activity | CRM does not capture field proof, operations cannot see promises, weak follow-up discipline. | CRM; Outbound Sales; Calendar and Tasks; Field Sales / Site Work; Reporting. | High; core CRM/outbound/visit loop belongs in MVP. |
| Warehouse-backed operations | Stock uncertainty, unaudited transfers, dispatch promises without inventory readiness, spreadsheet reliance. | Inventory / Warehouse / Depots; Dispatch; Service; Reporting; QuickBooks. | High for inventory basics; complex WMS features excluded. |
| Multi-location service businesses | Inconsistent branch visibility, work orders separated from customer history, parts usage not connected. | Service / Work Orders; Inventory; Fleet; Calendar; Reporting. | Medium; service may be MVP-light unless first customer requires it. |
| Companies needing CRM plus dispatch visibility | Sales and operations operate from different truths; managers cannot see lead-to-completion status. | CRM; Opportunities; Jobs; Dispatch; Field; Reporting. | Very high; central product promise. |
| Companies needing QuickBooks-connected operational workflows | Invoices/items/customers disconnected from operations; sync failures hidden; finance lacks operational context. | Integrations; QuickBooks; CRM; Orders; Inventory; Reporting. | High; QuickBooks foundation belongs in MVP, but not full accounting replacement. |

## Primary Personas

| Persona | Main goals | Main modules used | Mobile relevance | Reporting relevance | MVP relevance |
| --- | --- | --- | --- | --- | --- |
| Super Admin | Protect platform health, configure tenants, support escalation without violating tenant isolation. | Core Platform; Admin/Security; Reporting; Integrations. | Low; responsive admin access may help. | Tenant adoption, incidents, sync failures, support workload. | Later for full platform operations; referenced in MVP for tenant setup. |
| Company Admin | Configure company, manage users, enable modules, monitor data quality and sync health. | Core Platform; Admin/Security; Integrations; Reporting; all enabled modules. | Medium for urgent approvals/settings. | User adoption, permission changes, imports, integration health. | MVP. |
| Sales Manager | Drive follow-up, pipeline quality, territory coverage, rep performance, and conversion. | CRM; Outbound Sales; Calendar and Tasks; Field Sales / Site Work; Reporting. | Medium. | Pipeline velocity, activities, conversion, meetings, opportunities. | MVP. |
| Sales Rep | Prioritize outreach, log activities, create opportunities, maintain next steps. | CRM; Outbound Sales; Calendar and Tasks. | High for calls, notes, meetings, and visits. | Personal activity, overdue tasks, pipeline, win/loss. | MVP. |
| Field Manager | Ensure site work is assigned, visible, safe, and completed with proof. | Field Sales / Site Work; Drilling Operations; Dispatch; Fleet; Reporting; Offline Mobile. | High. | Visit completion, missed check-ins, job readiness, crew utilization. | MVP. |
| Field Sales Rep | Turn field conversations into documented opportunities and job requests. | CRM; Field Sales / Site Work; Calendar and Tasks; Offline Mobile. | Very high; mobile-first execution role. | Visits completed, check-ins, follow-ups, influenced opportunities. | MVP. |
| Dispatcher | Convert job demand into executable schedules and monitor progress/exceptions. | Orders / Dispatch / Logistics; Fleet; Field; Calendar; Reporting. | Medium; desktop-first with urgent mobile updates. | On-time dispatch, exceptions, route progress, completion proof. | MVP for basic dispatch visibility; later for advanced logistics. |
| Driver | Know assigned work, report arrival/departure, capture proof, work offline. | Dispatch; Fleet; Offline Mobile; Field capture. | Very high; mobile-first and offline-critical. | Stops completed, exceptions, location freshness, proof captured. | MVP for check-ins and basic tracking; later for full route workflows. |
| Warehouse Manager | Maintain stock accuracy and ensure field/dispatch readiness. | Inventory / Warehouse / Depots; Dispatch; Reporting; Integrations. | Medium for approvals/exceptions. | Stock accuracy, low-stock risk, transfer completion, adjustments. | MVP for basics; later for barcode/serial/lot. |
| Warehouse Operator | Receive, pick, transfer, load, and adjust stock with an audit trail. | Inventory / Warehouse / Depots; Dispatch support. | High on warehouse floor/depot. | Picks completed, errors, discrepancies, transfers. | MVP for simple stock movements. |
| Service Manager | Prioritize service work, assign technicians, track parts/labor, validate closure. | Service / Work Orders; Inventory; Calendar; Reporting. | Medium for urgent exceptions. | Open work orders, SLA compliance, first-time fix, parts usage. | Later/MVP-light if early customer requires it. |
| Service Technician | Complete assigned work, document parts/labor/notes/proof even offline. | Service / Work Orders; Inventory; Calendar; Offline Mobile. | Very high; mobile-first and offline-critical. | Completion rate, rework, parts used, notes/photos. | Later unless service is part of first MVP customer. |
| Analyst / Reporting User | Convert platform activity into trustworthy operational insight. | Reporting / Dashboards; all modules view/report access. | Low; mostly desktop. | Primary reporting persona. | MVP for basic dashboards; later for custom builder. |
| Read-Only Viewer | Monitor status and results without changing operational data. | Reporting; CRM; Jobs; Work Orders; Dispatch; Dashboards. | Low to medium. | Filtered dashboards and shared visibility. | MVP for management visibility. |

## Persona-to-Module Expectations

| Persona | Core | CRM | Outbound | Calendar | Field/Site | Drilling | Inventory | Dispatch | Fleet | Service | Reporting | Integrations | Offline |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Super Admin | Primary | View | View | View | View | View | View | View | View | View | Primary | Primary | View |
| Company Admin | Primary | Secondary | Secondary | Secondary | Secondary | Secondary | Secondary | Secondary | Secondary | Secondary | Primary | Primary | Secondary |
| Sales Manager | Secondary | Primary | Primary | Primary | Secondary | View | View | View | View | View | Primary | Secondary | Secondary |
| Sales Rep | Secondary | Primary | Primary | Primary | Secondary | No | No | No | No | No | Secondary | Secondary | Secondary |
| Field Manager | Secondary | Secondary | View | Primary | Primary | Primary | Secondary | Primary | Primary | Secondary | Primary | View | Primary |
| Field Sales Rep | Secondary | Primary | Secondary | Primary | Primary | Secondary | No | Secondary | Secondary | No | Secondary | View | Primary |
| Dispatcher | Secondary | View | No | Secondary | Secondary | Secondary | Secondary | Primary | Primary | Secondary | Primary | View | Secondary |
| Driver | View | No | No | Secondary | Secondary | Secondary | Secondary | Primary | Primary | No | View | No | Primary |
| Warehouse Manager | Secondary | View | No | Secondary | View | Secondary | Primary | Secondary | Secondary | Secondary | Primary | Secondary | Secondary |
| Warehouse Operator | Secondary | No | No | View | No | No | Primary | Secondary | No | View | View | No | Secondary |
| Service Manager | Secondary | Secondary | No | Primary | Secondary | Secondary | Secondary | Secondary | Secondary | Primary | Primary | Secondary | Primary |
| Service Technician | Secondary | View | No | Secondary | Secondary | Secondary | Secondary | Secondary | Secondary | Primary | View | No | Primary |
| Analyst / Reporting User | Secondary | View | View | View | View | View | View | View | View | View | Primary | View | View |
| Read-Only Viewer | View | View | View | View | View | View | View | View | View | View | View | View | View |

Legend: `Primary` = primary module owner/user; `Secondary` = regular supporting use; `View` = view-only or limited visibility; `No` = not typical.

## Core Product Problems

- CRM disconnected from field execution.
- Sales promises not visible to operations.
- Poor truck, crew, driver, and job visibility.
- Manual dispatch and follow-up coordination.
- Inventory uncertainty across warehouses and depots.
- Weak accountability for check-ins, status updates, and completion.
- Reporting scattered across tools.
- QuickBooks disconnected from operational records.
- Poor offline support for field users.

## Product Principles Future Phases Must Respect

- Multi-tenant by design.
- Company-scoped access by default.
- Modular but unified platform.
- CRM and operations share activity history.
- Desktop-first for managers and operators.
- Mobile-first for field execution moments.
- Offline-friendly for critical workflows.
- Real-time where operationally valuable.
- Eventually consistent where safer and cheaper.
- Reporting designed from day one.
- Auditability for important actions.
- Integration failures must be visible.
- No silent data loss.
- No duplicate entity concepts.

## Modules Introduced

| Module | Purpose | MVP relevance | Later-phase relevance |
| --- | --- | --- | --- |
| Core Platform | Shared tenant, company, user, role, module, audit, files, import/export, custom fields, search, and settings foundation. | Authentication, company roles, module enablement, audit baseline, files, imports, basic settings. | Advanced admin, enterprise controls, data retention, deeper custom fields, support tooling. |
| CRM | Manage relationships, leads, accounts, contacts, opportunities, ownership, activity history, and pipeline. | Core records, pipeline basics, timelines, ownership, tasks, basic imports. | Duplicate merging, territory automation, enrichment, scoring. |
| Outbound Sales | Support outreach, campaign/cadence discipline, channel logging, and sales productivity. | Activity logging, manual sequences/tasks, basic campaign lists and performance. | Automated sending, advanced cadence branching, compliance controls, AI suggestions. |
| Calendar and Tasks | Coordinate appointments, tasks, reminders, visits, follow-ups, SLA dates, and assignments. | Basic tasks, appointments, reminders, assignments, calendar views. | Advanced recurrence, SLA automation, shared calendars, resource scheduling. |
| Field Sales / Site Work | Capture site interactions, visits, check-ins, photos, notes, job requests, and proof. | Basic visits, check-ins, notes, photos, job requests. | Advanced forms, safety/hazard checklists, territory optimization. |
| Drilling Operations | Represent drilling-specific job execution as a field operations specialization. | Keep extension points; basic drilling context if needed. | Detailed drilling workflows, equipment planning, production metrics, specialized forms. |
| Inventory / Warehouse / Depots | Manage products, balances, stock movements, warehouses, depots, receiving, transfers, picking, and adjustments. | Product catalog, warehouse/depot basics, balances, stock movement history, receiving/transfer/adjustment basics. | Barcode, bin optimization, serial/lot, replenishment, cost layers. |
| Orders / Dispatch / Logistics | Coordinate jobs, orders, routes, stops, vehicles, drivers, proof, and exceptions. | Basic job/dispatch assignment, status visibility, vehicle/driver assignment, simple stops. | Route optimization, advanced route plans, proof workflows, customer notifications. |
| Fleet / Device Tracking | Track vehicles, drivers, devices, location pings, geofences, freshness, and route history. | Vehicles, drivers, tracking foundation, pings, geofences, current location visibility. | Route replay, advanced alerts, device health, maintenance integrations. |
| Service / Work Orders | Manage service requests, work orders, technicians, checklists, parts, labor, and service history. | Optional MVP-light work order basics if required. | Maintenance schedules, SLA automation, recurring work, customer sign-off. |
| Reporting and Dashboards | Provide role-aware sales, operational, inventory, fleet, dispatch, service, integration, and offline insight. | Basic dashboards for sales, field, dispatch, inventory, integration health, offline sync. | Custom report builder, scheduled reports, deeper analytics. |
| Integrations | Connect QuickBooks, email/SMS/WhatsApp logs, REST API, webhooks, CSV/Excel import/export. | QuickBooks foundation, import/export basics, sync logs, admin-visible errors. | Marketplace, advanced mapping, two-way sync extensions. |
| Notifications and Automation | Notify users about important events and automate safe reminders. | Basic reminders and critical exception notifications. | Advanced workflow rules, scheduled automations, escalation chains. |
| Search, Filters, and Custom Views | Provide permission-aware discovery and reusable operational views. | Global search foundation, list search, core filters and saved views. | Advanced view builder, personal/team/shared views, custom field filters. |
| Offline Mobile and Sync | Capture critical field execution actions in weak connectivity and sync safely later. | Offline capture for tasks, visits, check-ins, notes, photos, task updates. | Broader offline parity, complex conflict resolution, background sync optimization. |
| Admin, Security, and Audit | Control access, settings, audit history, and secure operations. | Company roles, permission foundation, audit of important changes. | Cerbos/policy engine, record-level rules, access review, retention policies. |

## MVP Scope

| MVP item | Why it belongs in MVP | Related modules | Future-phase dependency |
| --- | --- | --- | --- |
| Multi-company authentication foundation | Required before any company-scoped workflow can safely exist. | Core Platform; Admin/Security. | Phase 02 and Phase 03 must define identity, tenant, company, membership, and context behavior. |
| Company-level roles and permissions | Prevents uncontrolled data exposure and supports modular rollout. | Core Platform; Admin/Security. | Phase 02/15 must define permission structure; all modules must respect it. |
| Core CRM records | CRM is the front door for sales and customer context. | CRM; Core Platform. | Phase 04 must detail CRM entities, views, workflows, and requirements. |
| Outbound activity logging | Outbound discipline creates measurable pipeline and history. | Outbound Sales; CRM; Calendar. | Phase 05 must detail channels, activity types, and cadence boundaries. |
| Calendar and tasks | The platform needs a shared next-action system. | Calendar and Tasks; CRM; Field; Dispatch; Service. | Phase 06 must define task/appointment/reminder behavior. |
| Basic site visits | Connects field sales to operational readiness. | Field Sales / Site Work; CRM; Calendar; Mobile. | Phase 07 must define visit execution, proof, notes, and handoff. |
| Check-ins and check-outs | Creates operational accountability and proof of presence. | Field; Fleet; Mobile; Reporting. | Phases 07, 10, and 14 must define location, geofence, and offline behavior. |
| Basic vehicle and worker tracking | Dispatch and field managers need basic operational awareness. | Fleet; Dispatch; Mobile. | Phase 10 must define vehicles, drivers, devices, pings, and freshness. |
| Basic geofences | Supports check-in validation and exception visibility. | Fleet; Field; Dispatch. | Phase 10 must define geofence model and events. |
| Inventory and warehouse basics | Inventory uncertainty is a core operational pain. | Inventory / Warehouse / Depots; Dispatch; Service; Reporting. | Phase 08 must define products, locations, balances, movements, and adjustments. |
| QuickBooks sync foundation | Finance alignment is a major product promise and must not be bolted on later. | Integrations; CRM; Inventory; Orders; Reporting. | Phase 13 must define connections, external refs, sync jobs, logs, retries, and errors. |
| Basic dashboards | Adoption depends on management visibility. | Reporting / Dashboards; all MVP modules. | Phase 12 must define metrics, dashboards, permissions, and freshness expectations. |
| Mobile offline capture for check-ins, notes, photos, and tasks | Field reliability is a core trust requirement. | Offline Mobile; Field; Dispatch; Service; Mobile. | Phase 14 must define offline queue, sync status, conflicts, and failure handling. |

## MVP Exclusions

- Advanced route optimization.
- Full offline app parity.
- Barcode scanning unless confirmed.
- Serial/lot inventory unless confirmed.
- Complex branch/depot hierarchy permissions unless confirmed.
- Advanced quote/pricing engine unless confirmed.
- Full marketing automation.
- Native LinkedIn automation.
- Advanced AI recommendations.
- Custom report builder if too large for MVP.
- Full accounting system replacement.
- Payroll.
- HR management.
- Complex ERP functionality.
- Advanced WMS-grade wave planning, robotics, or conveyor integration.
- Native ELD compliance unless explicitly required.
- Enterprise SSO unless required by an early customer.
- Customer-facing portal unless added by later phase decision.

## Product Boundary Rules

- It is a CRM plus operations platform.
- It is not a full ERP replacement in the first version.
- It is not an accounting system replacement.
- It is not a payroll system.
- It is not only a fleet tracker.
- It is not only a field-service app.
- It is not only a warehouse management system.
- It must connect workflows without overbuilding every category from day one.
- It should prioritize operational visibility, execution accountability, auditability, and reliable capture over advanced automation in the first release.

## High-Level User Journeys

| Journey | Trigger | Main personas | Key records | Success outcome | Later phases affected |
| --- | --- | --- | --- | --- | --- |
| Outbound sales to opportunity | Imported lead, prospecting list, referral, inbound interest, or assignment. | Sales Rep; Sales Manager. | Lead, Account, Contact, Activity, Opportunity, Task. | Qualified opportunity has owner, stage, next action, and activity history. | CRM; Outbound; Calendar; Reporting. |
| Opportunity to site visit | Opportunity requires field validation, visit, or site assessment. | Sales Rep; Field Sales Rep; Sales Manager; Field Manager. | Opportunity, Account, Contact, Site, SiteVisit, Task, FieldNote. | Opportunity has verified site context and next operational step. | CRM; Calendar; Field/Site; Mobile. |
| Site visit to job request | Visit identifies operational work to be scheduled. | Field Sales Rep; Field Manager; Dispatcher; Sales Manager. | SiteVisit, FieldNote, FileAttachment, JobRequest, Job, Account, Site. | Job request has enough scope, site, timing, and proof to plan work. | Field/Site; Dispatch; Reporting; Drilling. |
| Job request to dispatch | Approved job request or order is ready for scheduling. | Dispatcher; Field Manager; Warehouse Manager; Driver. | Job, Order, Vehicle, Driver, RoutePlan, Stop, InventoryBalance. | Assigned work is visible to execution users with schedule and required context. | Dispatch; Inventory; Fleet; Mobile. |
| Dispatch to field execution | Scheduled job/route/stop starts. | Driver; Dispatcher; Field Manager. | Job, Stop, RoutePlan, CheckIn, FieldNote, ProofOfDelivery, LocationPing. | Work status and proof are captured and visible to dispatch/management. | Dispatch; Fleet; Mobile; Reporting. |
| Warehouse stock to truck/depot usage | Job/order/service work requires stock movement. | Warehouse Operator; Warehouse Manager; Dispatcher; Driver. | Product, InventoryBalance, StockMovement, PickTicket, InventoryTransfer, Vehicle, Depot. | Stock movement is auditable and readiness is visible. | Inventory; Dispatch; Fleet; Reporting. |
| Field completion to reporting | Field work, visit, stop, or service task is completed. | Field user; Manager; Analyst. | Job, SiteVisit, WorkOrder, Activity, FileAttachment, MetricSnapshot. | Managers see completed work and proof in reports and timelines. | Field; Dispatch; Service; Reporting. |
| Operational record to QuickBooks sync | Customer/item/invoice-relevant operational record becomes sync-eligible. | Company Admin/Finance Admin; Manager; Analyst. | Account, Product, Order, Invoice reference, IntegrationConnection, SyncJob, SyncLog, ExternalReference. | Accounting references remain aligned and sync failures are transparent. | Integrations; CRM; Inventory; Orders; Reporting. |
| Service request to work order completion | Customer issue or maintenance need is submitted. | Service Manager; Service Technician; Warehouse Manager. | ServiceRequest, WorkOrder, WorkOrderTask, Product, StockMovement, FieldNote. | Service work is completed with history, parts usage, and proof. | Service; Calendar; Inventory; Mobile; Reporting. |
| Offline field action to synced record | Field user performs critical action without reliable connectivity. | Driver; Field Sales Rep; Technician; Dispatcher; Field Manager; Company Admin. | OfflineAction, CheckIn, FieldNote, FileAttachment, Task, SyncJob, SyncLog. | No field work is silently lost and synced records preserve actor/time context. | Offline Mobile; Field; Dispatch; Service; Integrations. |

## Business Requirements Introduced

| Requirement ID | Short summary | Future-phase impact |
| --- | --- | --- |
| BR-01-001 | Support multiple customer companies within a secure multi-tenant SaaS model. | Phase 02/03 and all modules must preserve tenant/company isolation. |
| BR-01-002 | Support CRM and operations workflows in one shared system. | All business modules must connect to shared records, timelines, reporting, and permissions. |
| BR-01-003 | Provide management visibility from lead through completed job/service outcome. | Reporting, CRM, field, dispatch, service, and integration phases must preserve lifecycle visibility. |
| BR-01-004 | Support modular enablement by company. | Core platform and admin phases must support company-level module activation. |
| BR-01-005 | Support QuickBooks as the first accounting integration. | Integration phase must prioritize QuickBooks foundation. |
| BR-01-006 | Support offline-friendly field capture for critical workflows. | Mobile/offline phase must define capture, queue, sync status, and errors. |
| BR-01-007 | Preserve shared activity history across CRM, field, dispatch, service, and relevant operational modules. | Record detail pages and timelines across modules must reuse activity concepts. |
| BR-01-008 | Support company-scoped access as the primary permission boundary. | Identity and permissions must be company-aware by default. |
| BR-01-009 | Support role-based access for common company roles. | Permissions phase must define roles/actions without bypassing module needs. |
| BR-01-010 | Support auditability for important operational and administrative actions. | Audit logging must be included across core, inventory, dispatch, sync, and security actions. |
| BR-01-011 | Support sales-first workflows that generate operational demand. | CRM/outbound/field-to-dispatch handoff must remain intact. |
| BR-01-012 | Support operations-first workflows that manage execution and visibility. | Dispatch, fleet, inventory, service, and reporting phases must support execution workflows. |
| BR-01-013 | Support warehouses, depots, and inventory as first-class operational domains. | Inventory phase must model stock locations and movements as core, not metadata-only. |
| BR-01-014 | Support vehicles, drivers, devices, and location visibility where enabled. | Fleet phase must define tracking foundation and permission controls. |
| BR-01-015 | Support field check-ins, proof capture, notes, photos, and status updates. | Field/mobile phases must make these core field actions. |
| BR-01-016 | Support basic dispatch assignment and status visibility before advanced optimization. | Dispatch phase must prioritize assignment and visibility, not optimization first. |
| BR-01-017 | Support reporting and dashboard expectations from the beginning. | Reporting data must be considered in every module. |
| BR-01-018 | Expose integration failures and sync status to administrators. | Integration and admin UX must show errors, retries, and status. |
| BR-01-019 | Prevent silent data loss in offline, import, export, and integration workflows. | Offline, import/export, and integrations need recoverable failures and visible states. |
| BR-01-020 | Use canonical entity names from the global domain model. | All phases must avoid duplicate concepts and synonyms. |
| BR-01-021 | Support CSV and Excel import/export foundations. | Phase 17/import-export and core platform phases must define jobs, status, and row-level errors. |
| BR-01-022 | Support search, filters, and saved views as shared platform capabilities. | Search/view phase must define permission-aware discovery and reusable views. |
| BR-01-023 | Support light and dark mode as a product-level UX expectation. | UI phases must account for theme support. |
| BR-01-024 | Allow future expansion into advanced permissions, record-level rules, automation, barcode, route optimization, and enterprise readiness. | Later phases can extend through controlled decisions without disrupting MVP. |
| BR-01-025 | Avoid replacing accounting, payroll, HR, or full ERP systems in the first version. | Product scope must remain bounded in later phases. |
| BR-01-026 | Support role-aware management dashboards and exception visibility. | Reporting phase must include role-aware dashboards and exceptions. |

## Functional Requirements Introduced

| Requirement ID | Short summary | Future-phase impact |
| --- | --- | --- |
| FR-01-001 | Authorized users access only permitted tenant/company contexts. | Identity, API, UI, search, reporting, import/export, sync must be scoped. |
| FR-01-002 | Company admins manage users, roles, and enabled modules at baseline. | Admin/security phases must define role/module management. |
| FR-01-003 | Core CRM records support create, update, list, search, filter, and detail views. | CRM phase must detail CRUD, views, and validation. |
| FR-01-004 | Leads, accounts, contacts, and opportunities support ownership. | CRM permissions/reporting must respect ownership. |
| FR-01-005 | Activity logging works against CRM and operational records. | Timelines and activity APIs must be cross-module. |
| FR-01-006 | Outbound call, email, SMS, WhatsApp, and LinkedIn activity logging are supported channels. | Outbound phase must separate logging from native automation. |
| FR-01-007 | Tasks, appointments, due dates, assignments, and reminders are supported. | Calendar/task phase must define next-action system. |
| FR-01-008 | Site visits can be scheduled and completed. | Field/site phase must define visit lifecycle. |
| FR-01-009 | Field check-in and check-out capture is supported. | Field/mobile/fleet phases must handle location, time, and proof. |
| FR-01-010 | Notes, photos, and file attachments are supported on field/operational records. | File and mobile phases must support proof capture and sync. |
| FR-01-011 | Basic job request creation from site or opportunity context. | Field-to-dispatch handoff must be detailed later. |
| FR-01-012 | Basic dispatch assignment of jobs to users, vehicles, or crews. | Dispatch phase must define assignment and status visibility. |
| FR-01-013 | Vehicles and drivers/workers exist as operational resources. | Fleet and dispatch phases must define resources. |
| FR-01-014 | Tracking devices and location pings are supported where tracking is enabled. | Fleet phase must define pings, freshness, and privacy. |
| FR-01-015 | Basic geofence definitions and events are supported. | Fleet/field phase must define geofence model and events. |
| FR-01-016 | Products, warehouses, depots, balances, and stock movement history are supported. | Inventory phase must detail stock model. |
| FR-01-017 | Receiving, transfers, picking/loading, and adjustments are supported at product-definition level. | Inventory phase must define stock movement types and controls. |
| FR-01-018 | Service request and work order concepts exist for future service workflows. | Service phase must expand when prioritized. |
| FR-01-019 | Role-aware dashboards and module-aware reporting are supported. | Reporting phase must define permission-aware metrics. |
| FR-01-020 | Import and export jobs have visible status. | Import/export phase must define jobs and errors. |
| FR-01-021 | QuickBooks connection status and sync logs are supported. | Integration phase must define sync lifecycle. |
| FR-01-022 | External references are stored for synced provider records. | Integration and entity phases must preserve provider links. |
| FR-01-023 | Integration errors and retryable failures are visible to authorized admins. | Admin and integration UX must expose failures. |
| FR-01-024 | Permission-aware global search is supported. | Search phase must respect tenant/company/role scope. |
| FR-01-025 | Module list search, filters, sorting, and saved views are shared platform capabilities. | Search/filter/view phase must define reusable patterns. |
| FR-01-026 | Table, kanban, calendar, map, and timeline patterns are supported where relevant. | UX phases must reuse consistent view patterns. |
| FR-01-027 | Mobile field workflows for assigned work and critical capture actions are supported. | Mobile phase must focus on execution moments. |
| FR-01-028 | Offline queueing for check-ins, notes, photos, and task updates is supported. | Offline phase must define queue and sync behavior. |
| FR-01-029 | Sync status for offline-created actions is displayed. | Mobile/offline UI must show pending/synced/failed/conflict states. |
| FR-01-030 | Audit logs cover important create, update, delete/archive, restore, status transition, assignment, permission, import/export, and sync actions. | Audit must be cross-module. |
| FR-01-031 | Soft delete/archive behavior is supported for major business records. | Later phases must define deletion/archive patterns. |
| FR-01-032 | Company-scoped custom fields and metadata are supported without replacing canonical fields. | Custom fields cannot hide required workflow/reporting fields. |

## Non-Functional Requirements Introduced

| Requirement ID | Category | Short summary | Future-phase impact |
| --- | --- | --- | --- |
| NFR-01-001 | Multi-tenancy | All business records must be isolated by tenant and scoped by company where applicable. | All app, API, search, report, import/export, sync paths must prevent cross-tenant exposure. |
| NFR-01-002 | Security | Access must be role-based and permission-aware. | Every module must validate view/edit/export/sync permissions. |
| NFR-01-003 | Reliability | Critical workflows fail visibly and recoverably. | Offline, sync, import/export, and file upload must not silently fail. |
| NFR-01-004 | Auditability | Important actions are traceable with actor, action, entity, timestamp, scope, and relevant metadata. | Audit design must be cross-module. |
| NFR-01-005 | Performance | Core list, detail, and dashboard experiences remain usable with realistic SMB volumes. | Later phases must define screen-level targets and rollups. |
| NFR-01-006 | Offline resilience | Defined critical field actions work in poor connectivity. | Offline actions must preserve actor/time and show sync states. |
| NFR-01-007 | Data integrity | Core workflow fields are explicit and validated. | Important status/owner/assignment/timestamps cannot live only in notes or metadata. |
| NFR-01-008 | Observability | Operational jobs and integrations are diagnosable. | Structured logs, correlation IDs, sync logs, job status, and admin errors are required. |
| NFR-01-009 | Scalability | Modules support growth by company, record volume, and enabled modules. | Do not assume one company, one warehouse, one depot, or one operating location. |
| NFR-01-010 | Usability | Common workflows must be practical for non-technical users. | UX must use clear statuses, empty states, errors, guided actions, and role-focused views. |
| NFR-01-011 | Accessibility basics | Core UI supports readable contrast, keyboard-friendly interactions, labels, and responsive layouts. | UI phases must define detailed accessibility targets. |
| NFR-01-012 | Integration reliability | External integrations are stateful, retry-aware, and visible. | Sync jobs need queued/running/succeeded/failed/partially failed/skipped/retry states. |
| NFR-01-013 | Privacy | GPS, driver, user activity, and customer data visibility are permission-controlled. | Location and user performance data cannot be broadly exposed by default. |
| NFR-01-014 | Maintainability | Module boundaries are clear and canonical entity names are reused. | No duplicate concepts or synonyms in future phases. |
| NFR-01-015 | Extensibility | Custom fields, integrations, APIs, webhooks, and automation use controlled extension seams. | Extensions cannot bypass permissions, audit, reporting, or data integrity. |

## Entities Introduced

Phase 01 does not define detailed schemas. It references canonical product-level entities that future phase documents must reuse and detail in the proper phase.

| Entity | Related module | Phase expected to detail it | Notes |
| --- | --- | --- | --- |
| Tenant | Core Platform | Phase 02/03 | Highest SaaS isolation boundary. |
| Company | Core Platform | Phase 02/03 | Primary customer/company scope for records and permissions. |
| User | Core Platform | Phase 02/03 | Authenticated person using the system. |
| UserMembership | Core Platform | Phase 02/03 | Connects user to tenant/company/role context. |
| Role | Admin/Security | Phase 02/15 | Role grouping for access control. |
| Permission | Admin/Security | Phase 02/15 | Action/module capability control. |
| Account | CRM | Phase 04 | Company/customer relationship record. |
| Contact | CRM | Phase 04 | Person associated with account, lead, opportunity, or operational context. |
| Lead | CRM / Outbound | Phase 04/05 | Prospect or early sales record. |
| Opportunity | CRM | Phase 04 | Sales opportunity that can generate field/operational demand. |
| Activity | CRM / Outbound / Shared Timeline | Phase 04/05/03 | Shared event/history item across CRM and operations. |
| Task | Calendar and Tasks | Phase 06 | Assigned next action or work item. |
| CalendarEvent | Calendar and Tasks | Phase 06 | Calendar appointment/event concept; may align with Appointment. |
| Site | Field Sales / Site Work | Phase 07 | Customer/location context for visits, jobs, or service. |
| SiteVisit | Field Sales / Site Work | Phase 07 | Scheduled/executed visit tied to CRM/site. |
| CheckInEvent | Field / Mobile / Fleet | Phase 07/10/14 | Arrival/departure/status capture; may align with CheckIn. |
| JobRequest | Field / Dispatch | Phase 07/09 | Request created from site/opportunity context. |
| Job | Dispatch / Field / Drilling | Phase 09/07 | Operational work unit. |
| Product | Inventory | Phase 08 | Item/SKU/service item foundation; may link to QuickBooks item. |
| Warehouse | Inventory | Phase 08 | Stock storage location. |
| Depot | Inventory / Fleet / Dispatch | Phase 08/10 | Operational stock/vehicle base. |
| InventoryBalance | Inventory | Phase 08 | Stock balance by product/location. |
| StockMovement | Inventory | Phase 08 | Auditable movement/adjustment/usage event. |
| Order | Dispatch / Logistics | Phase 09 | Operational/customer order concept. |
| Shipment | Dispatch / Logistics | Phase 09 | Delivery/shipment execution record. |
| DispatchPlan | Dispatch / Logistics | Phase 09 | Assignment/scheduling plan; may align with RoutePlan. |
| RoutePlan | Dispatch / Logistics | Phase 09 | Planned route/stops for driver/vehicle. |
| Vehicle | Fleet | Phase 10 | Operational vehicle resource. |
| Driver | Fleet / Dispatch | Phase 10 | Driver/worker resource, often linked to User. |
| TrackingDevice | Fleet | Phase 10 | Device/source for location pings. |
| Geofence | Fleet / Field | Phase 10 | Operational boundary around site/depot/etc. |
| LocationPing | Fleet | Phase 10 | Current/historical location signal. |
| ServiceRequest | Service | Phase 11 | Intake for service need. |
| WorkOrder | Service | Phase 11 | Service execution record. |
| Report | Reporting | Phase 12 | Report output or definition concept. |
| Dashboard | Reporting | Phase 12 | Role-aware dashboard. |
| IntegrationConnection | Integrations | Phase 13 | External integration connection/config. |
| SyncJob | Integrations / Offline | Phase 13/14 | Sync/import/export/offline job unit. |
| AuditLog | Admin/Security/Audit | Phase 15 | Trace of important business/admin actions. |
| Notification | Notifications | Phase 16 | In-app/email/SMS alert or reminder. |
| FileAttachment | Core / Field / Service | Phase 03/07/11/14 | Photos, proof, documents, files. |
| SavedView | Search / Filters / Views | Phase 18 | Saved filters/views for tables, kanban, maps, etc. |

## Fields Introduced

Phase 01 does not define implementation-level field schemas. Detailed fields must be defined in later phase documents. Shared product-level fields and concepts implied by Phase 01 include:

| Field | Product-level meaning |
| --- | --- |
| `id` | Stable unique identifier for major records. |
| `tenant_id` | Tenant isolation scope. |
| `company_id` | Company-level scope and primary access boundary. |
| `created_at` | Record creation timestamp. |
| `created_by` | Actor who created the record. |
| `updated_at` | Last update timestamp. |
| `updated_by` | Actor who last updated the record. |
| `deleted_at` | Soft delete/archive timestamp where applicable. |
| `deleted_by` | Actor who deleted/archived the record where applicable. |
| `status` | Explicit workflow/status field for reportable lifecycle state. |
| `source` | Origin of record/action, such as manual, import, mobile, integration, or automation. |
| `external_refs` | References to external provider records such as QuickBooks IDs. |
| `metadata` | Controlled extension data that must not replace canonical required fields. |

Additional product-level field concepts referenced by Phase 01 include owner/assignee fields, audit fields, soft delete/archive fields, custom fields, sync status, and reporting rollup fields. Later phases must define exact names and schemas.

## APIs Introduced

Phase 01 introduces API expectations, not final contracts. Future API work must be tenant/company scoped, permission-aware, auditable, and consistent with canonical entity names.

- Authentication APIs.
- User/company context APIs.
- CRM record APIs.
- Activity logging APIs.
- Task/calendar APIs.
- Site visit/check-in APIs.
- Inventory APIs.
- Dispatch/logistics APIs.
- Fleet/tracking APIs.
- Service APIs.
- Reporting APIs.
- Integration/QuickBooks sync APIs.
- Import/export APIs.
- Webhook/API access future APIs.
- Open REST API as a future/extension surface.
- API behavior must not bypass permissions, auditability, tenant/company scope, or integration error visibility.

## Permissions Introduced

- Company-level access is primary.
- Module-level access is required.
- Role-based actions are required.
- Record-level permissions are future-capable.
- Super Admin and Company Admin must remain separate.
- Permission changes must be auditable.
- Mobile actions must respect assigned work and permitted record visibility.
- Reports, exports, search, APIs, integrations, sync logs, and dashboards must respect permissions.
- Sensitive GPS, driver, user performance, financial, customer, and export data must not be broadly visible by default.

## UX Patterns Introduced

- Desktop-first admin/operator/reporting experience.
- Mobile-optimized field capture.
- Responsive layouts.
- Tables.
- Kanban.
- Calendar.
- Map views.
- Record detail pages.
- Activity timelines.
- Clear status labels.
- Sync state indicators.
- Empty states.
- Error states.
- Light and dark mode.
- Role-focused views.
- Permission-aware visibility.
- Pending/synced/failed/conflict states for offline actions.

## Reports or Dashboards Introduced

- Sales dashboards.
- Pipeline reports.
- Outreach reports.
- Field activity reports.
- Dispatch performance reports.
- Fleet utilization reports.
- Inventory movement and balance reports.
- Service performance reports.
- QuickBooks sync health reports.
- Operational exception reports.
- Team productivity reports.
- Admin/security reports.
- Offline sync health reports.
- Custom reports later.
- Scheduled reports later unless specifically added to MVP.
- Reports must be role-aware, permission-aware, and designed from day one.

## Notifications Introduced

- Task reminders.
- Dispatch alerts.
- Geofence alerts.
- Sync failure alerts.
- Inventory alerts.
- Service/work order alerts.
- Assignment alerts.
- Exception alerts.
- Offline issue alerts.
- In-app notifications.
- Email notifications.
- SMS notifications where needed later.
- Notification preferences/configuration where appropriate.
- Notifications must be useful, permission-aware, and focused on operationally important changes.

## Audit Events Introduced

- Login and permission changes.
- Record creation and edits.
- Delete/archive and restore actions.
- Status transitions.
- Assignment changes.
- Inventory movement.
- Dispatch actions.
- Tracking/geofence events that matter operationally.
- Import and export actions.
- Integration sync operations.
- Admin/security actions.
- Sensitive exports.
- High-impact operational actions.
- Audit logs should include actor, action, entity, timestamp, scope, and relevant before/after metadata where appropriate.

## Integrations Introduced

- QuickBooks as the first accounting integration.
- Email provider integrations.
- SMS integrations.
- WhatsApp integrations.
- LinkedIn activity logging.
- Open REST API.
- Webhooks.
- CSV import/export.
- Excel import/export.
- External references.
- Sync logs.
- Retry behavior.
- Admin-visible sync errors.
- Connection status.
- Skipped/partial failure visibility.
- Provider-specific mapping is not finalized in Phase 01.
- QuickBooks is a sync/accounting reference layer, not the operational source of truth.

## Dependencies Created

- Phase 02 depends on product boundaries and personas.
- Phase 03 depends on core platform expectations.
- Phase 04 depends on CRM definitions.
- Phase 05 depends on outbound scope.
- Phase 06 depends on calendar/task expectations.
- Phase 07 depends on field/site work expectations.
- Phase 08 depends on inventory and warehouse MVP scope.
- Phase 09 depends on dispatch/logistics workflows.
- Phase 10 depends on fleet/tracking expectations.
- Phase 11 depends on service/work order boundaries.
- Phase 12 depends on reporting expectations.
- Phase 13 depends on QuickBooks/integration expectations.
- Phase 14 depends on offline/mobile expectations.
- Phase 15 depends on admin/security/audit expectations.
- Phase 16 depends on notification/automation expectations.
- Phase 17 depends on API/webhook/import/export expectations.
- Phase 18 depends on search/filter/view expectations.
- Phase 19 depends on rollout/operations expectations.
- Phase 20 must consolidate and must not introduce major new features.

## Constraints Future Phases Must Respect

- Do not contradict the unified platform direction.
- Do not split CRM and operations into separate products.
- Do not treat QuickBooks as the operational source of truth.
- Do not design features without tenant/company scoping.
- Do not bypass identity/access rules.
- Do not create duplicate entity concepts.
- Do not rename canonical entities, modules, personas, phases, or workflows casually.
- Do not overbuild MVP features unless explicitly confirmed.
- Do not make mobile full desktop parity by default.
- Do not make offline support universal unless required.
- Do not add detailed module behavior outside the proper phase.
- Do not introduce new major modules without marking them as future or open.
- Do not turn Phase 01 into a technical architecture document.
- Do not expand MVP without documenting tradeoffs and obtaining a decision.
- Do not treat drilling as a separate product unless a later accepted decision changes that.
- Do not hide required workflow/reporting/permission fields inside metadata or custom fields.
- Do not allow search, reports, exports, integrations, or mobile sync to bypass company and permission scoping.
- Do not silently drop offline actions, integration failures, import errors, export failures, or upload failures.
- Do not introduce detailed permission matrices, final API contracts, database schemas, or screen-by-screen designs in documents assigned to other phases.

## Product Risks Carried Forward

- Scope creep.
- Overbuilding MVP.
- Weak tenant isolation.
- Conflicting entity names.
- Offline sync complexity.
- QuickBooks sync complexity.
- Reporting performance.
- GPS privacy and reliability.
- Inventory accuracy.
- Dispatch workflow complexity.
- Permission complexity.
- Mobile adoption issues.
- Data quality and duplicate CRM records.
- Integration error handling and support burden.
- Too much module breadth before validating the first customer segment.
- Under-designed audit/reporting fields that become hard to retrofit later.

## Recommended Decisions Carried Forward

- Treat drilling operations as a field operations specialization unless later separated explicitly.
- Treat QuickBooks as a sync integration, not the operational source of truth.
- Keep MVP focused on visibility and execution before advanced optimization.
- Treat mobile as field-execution-first, not full admin parity.
- Keep CRM, field operations, inventory, dispatch, fleet, service, reporting, and integrations modular but unified.
- Use canonical entity names from the global domain model.
- Design reporting, auditability, sync status, and permissions from the start.
- Keep custom fields and metadata as extensions, not replacements for required workflow/reporting fields.
- Prefer visible, recoverable failure states for offline, imports, exports, integrations, and uploads.

## Open Questions Carried Forward

- Should the MVP include quote/pricing?
- Should invoices be created in-app or only synced to QuickBooks?
- Should barcode scanning be MVP?
- Should serial/lot inventory be MVP?
- Should route optimization be MVP?
- Should scheduled emailed reports be MVP?
- Should Cerbos be adopted from day one?
- How deep should branch/depot-level permissions be in the first version?
- Should LinkedIn remain logging-only?
- What is the first exact customer segment to optimize for?
- How deep should drilling-specific workflows be in the first release?
- Should service/work orders be MVP-light or pushed later?
- Which reports are mandatory for the first customer launch?
- Which mobile actions must work offline on day one?
- Which QuickBooks objects should be included in the first sync foundation?
