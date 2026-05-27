# 00_Global_Decisions_Register.md

**Document type:** Global decision register control document  
**Applies to:** All future phase documents for the multi-company SaaS CRM, outbound sales, field operations, drilling workflows, logistics, warehouse, fleet, dispatch, service, reporting, integrations, QuickBooks sync, and offline-capable mobile platform  
**Audience:** Product architects, systems architects, technical decision owners, AI documentation writers, engineering leads, design leads, QA leads, implementation leads, and delivery managers  
**Status:** Control standard  
**Source documents:** Master Platform Documentation; `00_Global_Documentation_Rules.md`; `00_Global_Domain_Model.md`  
**Last reviewed:** 2026-05-09

---

# 1. Purpose of This Document

This document defines the official global decision register for the platform. It exists so future phase documents do not make conflicting architecture, product, data, UX, permission, integration, security, operations, or implementation decisions.

This document does not create Phase 1, does not rewrite the master documentation, and does not create detailed feature specifications. It records global decisions that future phase documents must respect.

# 2. How This Document Should Be Used

Every future phase writer must read this document before defining scope, entities, APIs, permissions, UX, reports, integrations, audit events, offline behavior, or implementation notes.

Required usage process:

1. Read the master documentation, global documentation rules, global domain model, and this register.
2. Identify all decisions that affect the target phase.
3. Reuse accepted decisions exactly.
4. Treat recommended decisions as the default unless the phase proposes a documented change.
5. Treat open decisions as open questions unless the phase has enough evidence to recommend a decision.
6. Add new cross-phase decisions to this register rather than burying them in prose.
7. Keep decision IDs stable. Do not renumber existing decisions.
8. Mark any proposed change as a new decision or a superseding decision.

# 3. Decision Register Principles

- Decisions must be explicit, traceable, and reusable across phases.
- Accepted decisions are binding until superseded.
- Recommended decisions are strong defaults, not casual suggestions.
- Open decisions must remain visible until resolved.
- Decisions must not contradict the master documentation or global domain model.
- Entity names, module names, and phase names must not be casually renamed.
- Avoid unnecessary complexity; record only decisions with cross-phase impact.
- Security, tenant isolation, auditability, offline reliability, and integration failure visibility take priority over visual polish.
- A future phase may propose a change, but it must not silently override this register.

# 4. Decision Status Definitions

| Status | Meaning | Future Phase Behavior |
|---|---|---|
| Accepted | Official platform decision. | Must be followed unless superseded through this register. |
| Recommended | Preferred direction based on current information. | Must not be contradicted silently; changes require rationale. |
| Open | Unresolved decision requiring owner review. | Treat as an open question unless the phase has enough evidence to recommend or accept a decision. |
| Deferred | Intentionally postponed. | Do not implement as current scope unless reprioritized. |
| Rejected | Explicitly disallowed. | Do not implement or reintroduce without a new decision. |
| Superseded | Replaced by a newer decision. | Follow the superseding decision ID. |

# 5. Decision Categories

| Category | ID Prefix | Scope |
|---|---|---|
| Architecture | ADR | Backend, frontend, API, infrastructure, module architecture, technical patterns. |
| Product | PDR | Product scope, MVP boundaries, workflow intent, module packaging, user-facing behavior. |
| Data | DDR | Domain model, entity ownership, identifiers, MongoDB modeling, events, rollups. |
| UX | UXDR | Navigation, views, mobile UX, tables, maps, timelines, saved views. |
| Integration | IDR | QuickBooks, external providers, webhooks, API keys, imports/exports, sync. |
| Security | SDR | Authorization, audit, isolation, compliance, data exposure, admin controls. |
| Operations | ODR | Deployment, monitoring, jobs, retention, unresolved platform operations choices. |

# 6. Decision ID Format

Use these ID prefixes exactly:

| Prefix | Meaning | Example |
|---|---|---|
| ADR | Architecture decision record | ADR-001 |
| PDR | Product decision record | PDR-001 |
| DDR | Data/domain decision record | DDR-001 |
| UXDR | UX decision record | UXDR-001 |
| IDR | Integration decision record | IDR-001 |
| SDR | Security decision record | SDR-001 |
| ODR | Operations decision record | ODR-001 |

Rules:

- IDs must be unique.
- IDs must be stable after publication.
- Do not renumber existing IDs.
- If a decision changes, create a new decision and mark the old one `Superseded`.
- Use the category prefix that best matches the main impact.

# 7. Decision Record Template

```markdown
## ADR-001: Decision Title

| Field | Value |
|---|---|
| Status | Accepted / Recommended / Open / Deferred / Rejected / Superseded |
| Category | Architecture / Product / Data / UX / Integration / Security / Operations |
| Owner | Product Architect / Engineering Lead / Product Owner / Security Lead |
| Affected Modules | Module names |
| Affected Phases | Phase numbers |
| Source | Master Documentation / Global Domain Model / Recommended |
| Last Reviewed | YYYY-MM-DD |

### Context

Explain the situation and why this decision matters.

### Decision

State the decision clearly.

### Rationale

Explain why this decision is preferred.

### Consequences

Explain what this decision enables, restricts, or requires.

### Implementation Guidance

Explain how future phase documents should apply this decision.

### Risks

List risks created by this decision.

### Review Triggers

List events that should cause this decision to be reviewed.

### Related Decisions

List related decision IDs.
```

# 8. Global Decision Index

| ID | Title | Status | Category | Affected Modules | Affected Phases |
|---|---|---|---|---|---|
| PDR-001 | One Core Platform With Optional Modules | Accepted | Product | All modules | All phases |
| PDR-002 | CRM and Operations Share a Unified Platform | Accepted | Product | CRM, Outbound Sales, Field Operations, Dispatch, Inventory, Fleet, Service, Reporting | Phases 04-12 |
| PDR-003 | Desktop-First Operations With Strong Mobile Support | Accepted | Product | Core Platform, CRM, Dispatch, Inventory, Fleet, Service, Mobile | All phases |
| PDR-004 | Reporting Designed From the Beginning | Accepted | Product | Reporting / Analytics, All operational modules | All phases |
| PDR-005 | QuickBooks Is a First-Class Integration | Accepted | Product | Integrations, QuickBooks, CRM, Orders, Inventory, Reporting | Phases 08-13 |
| PDR-006 | MVP Must Not Attempt the Full Platform at Once | Accepted | Product | All modules | All phases |
| PDR-007 | Use the Planned 20-Document Phase Structure | Accepted | Product | Documentation, All modules | All phases |
| PDR-008 | LinkedIn Starts as Activity Logging | Recommended | Product | Outbound Sales, CRM, Integrations | Phase 05, Phase 13 |
| DDR-001 | Tenant Is the Top-Level SaaS Isolation Boundary | Accepted | Data | Core Platform, Identity and Access, Security, All modules | All phases |
| DDR-002 | Company Is the Customer Organization Inside a Tenant | Accepted | Data | Core Platform, Identity and Access, All modules | All phases |
| DDR-003 | Company-Level Access Is the Primary Permission Boundary | Accepted | Data | Identity and Access, Permissions, All modules | All phases |
| DDR-004 | Users Belong to Companies Through UserMembership | Accepted | Data | Identity and Access, Core Platform | Phase 02, All phases |
| SDR-001 | Super Admin Access Is Separate From Company Admin Access | Accepted | Security | Core Platform, Identity and Access, Admin, Security | Phase 02, Phase 15, All phases |
| SDR-002 | Role-Based Permissions Are the Baseline | Accepted | Security | Identity and Access, Permissions, All modules | Phase 02, All phases |
| SDR-003 | Policy-Based Authorization May Be Introduced Through Cerbos | Recommended | Security | Identity and Access, Permissions, Security | Phase 02, Phase 15, Phase 20 |
| SDR-004 | Record-Level Permissions Are Future-Capable but Not Universal in MVP | Accepted | Security | Permissions, CRM, Field Operations, Service, Reporting | All phases |
| SDR-005 | Permissions Must Be Auditable | Accepted | Security | Identity and Access, Audit, Admin | Phase 02, Phase 03, Phase 15, All phases |
| ADR-001 | Backend Uses Python and FastAPI | Accepted | Architecture | Backend API, All modules | All phases |
| ADR-002 | MongoDB Is the Primary Operational Database | Accepted | Architecture | Data Platform, All modules | All phases |
| ADR-003 | Redis and Workers Support Async Operational Work | Accepted | Architecture | Backend API, Integrations, Reporting, Notifications, Imports/Exports, GPS | Phases 03, 12, 13, 15, All relevant phases |
| DDR-005 | Use Stable Application IDs | Accepted | Data | Data Platform, API, Offline Mobile, Integrations | All phases |
| DDR-006 | Do Not Expose MongoDB _id as Public API ID | Accepted | Data | API, Data Platform, All modules | All phases |
| DDR-007 | Use References Instead of Deep Nesting for Searchable or Controlled Records | Accepted | Data | Data Platform, All modules | All phases |
| DDR-008 | Use Denormalized Snapshots and Rollups for Dashboards | Accepted | Data | Reporting / Analytics, All modules | Phases 03, 12, All phases |
| DDR-009 | Use Append-Only Event Records for Operational History | Accepted | Data | Audit, Inventory, Fleet, Field Operations, Integrations, Reporting | All phases |
| DDR-010 | Use Soft Delete for Major Business Records | Accepted | Data | All business modules | All phases |
| DDR-011 | Location Pings, Stock Movements, Audit Logs, and Sync Logs Are Append-Only | Accepted | Data | Fleet, Inventory, Audit, Integrations | Phases 08, 10, 13, 15, All relevant phases |
| DDR-012 | AuditLog Is Required for Important Administrative and Operational Actions | Accepted | Data | Audit, All modules | All phases |
| ADR-004 | REST API Is the Primary API Style | Accepted | Architecture | API, All modules | All phases |
| ADR-005 | API Endpoints Must Be Tenant and Company Scoped | Accepted | Architecture | API, Security, All modules | All phases |
| ADR-006 | Import and Export Run as Jobs | Accepted | Architecture | Imports/Exports, All modules | Phase 03, Phase 13, All relevant phases |
| ADR-007 | Frontend Uses Next.js | Accepted | Architecture | Frontend, All modules | All phases |
| ADR-008 | Styling Uses Tailwind CSS and shadcn/ui | Accepted | Architecture | Frontend, UX, All modules | All phases |
| UXDR-001 | Support Light and Dark Mode | Accepted | UX | Frontend, All modules | All phases |
| UXDR-002 | Desktop Operators Need Table, Kanban, Calendar, and Map Views | Accepted | UX | CRM, Outbound Sales, Calendar, Dispatch, Fleet, Inventory, Service | Phases 04-12, 16 |
| UXDR-003 | Major List Pages Define Filters Before Implementation | Accepted | UX | All modules, Search / Saved Views | All phases |
| UXDR-004 | Mobile UX Focuses on Field Workflows, Not Desktop Parity | Accepted | UX | Mobile, Field Operations, Dispatch, Service, Fleet, Inventory | Phases 07-11, 14 |
| UXDR-005 | Activity Timeline Appears on Key Records | Accepted | UX | CRM, Field Operations, Dispatch, Inventory, Fleet, Service, Integrations | Phases 04-13 |
| UXDR-006 | Global Search Is a Core Platform Feature | Accepted | UX | Core Platform, Search, All modules | Phase 03, All phases |
| UXDR-007 | Saved Filters and Saved Views Are Supported | Accepted | UX | Search / Saved Views, All modules | Phase 03, Phase 16, All phases |
| DDR-013 | Reporting Uses Rollups Rather Than Expensive Runtime Joins | Accepted | Data | Reporting / Analytics, All modules | Phase 12, All phases |
| PDR-009 | Custom Report Builder Is Planned, Not Necessarily MVP | Recommended | Product | Reporting / Analytics | Phase 12, Phase 20 |
| ADR-009 | Basic Offline Support Is Required | Accepted | Architecture | Mobile, Field Operations, Dispatch, Service, Fleet, Inventory | Phase 14, Relevant earlier phases |
| ADR-010 | Offline Actions Use a Local Queue With Explicit Conflict Handling | Accepted | Architecture | Mobile, Sync, Field Operations, Dispatch, Service | Phase 14, Relevant earlier phases |
| ADR-011 | Live Tracking Required Where Operationally Important | Accepted | Architecture | Fleet, Dispatch, Field Operations | Phases 09, 10, 14 |
| DDR-014 | Historical Route Replay Is Required | Accepted | Data | Fleet, Dispatch, Reporting | Phase 10, Phase 12 |
| DDR-015 | Geofence Entry and Exit Events Are Required | Accepted | Data | Fleet, Field Operations, Dispatch, Service | Phases 07, 09, 10, 14 |
| DDR-016 | Multiple Warehouses and Depots Are Required | Accepted | Data | Inventory / Warehouse, Dispatch, Fleet | Phase 08, Phase 09, Phase 10 |
| DDR-017 | Stock Movements Are Event-Based and Balances Are Derived or Maintained From Events | Accepted | Data | Inventory / Warehouse, Reporting, Service, Dispatch | Phase 08, Phase 11, Phase 12 |
| DDR-018 | Transfers, Receiving, Picking, Packing, and Adjustments Are Separate Models | Accepted | Data | Inventory / Warehouse, Dispatch, Service | Phase 08, Phase 09, Phase 11 |
| DDR-019 | Use Vehicle as Canonical Entity, Not Truck | Accepted | Data | Fleet, Dispatch, Service | Phase 10, All relevant phases |
| DDR-020 | Drivers Are Users With Role and Membership Context | Recommended | Data | Fleet, Identity and Access, Dispatch | Phase 10, Phase 02 |
| DDR-021 | Tracking Devices Are Assignable to Vehicles or Users | Accepted | Data | Fleet, Mobile, Dispatch | Phase 10, Phase 14 |
| PDR-010 | Orders, Dispatch, and Logistics Use Manual Control First | Recommended | Product | Orders / Dispatch / Logistics, Fleet, Inventory | Phase 09, Phase 19 |
| PDR-011 | Service Uses WorkOrder as Canonical Execution Record | Accepted | Product | Service / Work Orders, Inventory, Field Operations | Phase 11 |
| IDR-001 | External IDs Stored in External References | Accepted | Integration | Integrations, QuickBooks, All synced modules | Phase 13, All integration phases |
| IDR-002 | Integration Sync Has Explicit Logs and Retry Behavior | Accepted | Integration | Integrations, QuickBooks, Notifications, Admin | Phase 13, All integration phases |
| IDR-003 | Webhooks Are Part of the Integration Layer | Accepted | Integration | Integrations, API, Webhooks | Phase 13, All relevant phases |
| IDR-004 | Email, SMS, WhatsApp, API, and Webhooks Are Planned Integration Surfaces | Accepted | Integration | Integrations, Outbound Sales, Notifications, API | Phases 05, 13, 16, 17 |
| IDR-005 | QuickBooks Customer, Invoice, and Item Links Are Approved Link Entities | Accepted | Integration | QuickBooks, Integrations, CRM, Orders, Inventory | Phase 13 |
| PDR-012 | Notifications Are Useful, Permission-Aware, and Configurable | Accepted | Product | Notifications, All modules | Phase 16, All relevant phases |
| SDR-006 | Tenant and Company Isolation Must Be Tested | Accepted | Security | Security, QA, All modules | All phases |
| SDR-007 | API Keys, Webhooks, and Exports Are Scoped, Revocable, Auditable, and Rate-Limited | Accepted | Security | Integrations, API, Webhooks, Imports/Exports | Phase 13, Phase 15, Phase 20 |
| SDR-008 | GPS and Device Tracking Require Permission and Visibility Controls | Accepted | Security | Fleet, Mobile, Dispatch, Security | Phase 10, Phase 14, Phase 15 |
| ODR-001 | Use Structured Logging and Correlation IDs | Accepted | Operations | Backend API, Workers, Integrations, Monitoring | Phase 15, All phases |
| ODR-002 | Deployment Must Support API, Worker, Realtime, and Scheduled Jobs | Accepted | Operations | Operations, Backend API, Workers, Realtime, Reporting | Phase 15, Phase 20 |
| ODR-003 | Admin-Visible Failure States Are Required | Accepted | Operations | Admin, Integrations, Imports/Exports, Offline, Notifications, GPS | Phase 03, 13, 14, 15 |
| ODR-004 | Phase Documents Rely on Summaries Instead of Full Prior Documents | Accepted | Operations | Documentation, All modules | All phases |
| IDR-007 | CSV and Excel Imports Validate Rows and Report Errors | Accepted | Integration | Imports/Exports, All modules | Phase 03, Phase 13, All relevant phases |
| ODR-005 | Tenant Database Isolation Model | Open | Operations | Data Platform, Security, Operations | Phase 02, Phase 15, Phase 20 |
| ODR-006 | Location Hierarchy for Branches, Departments, Depots, Warehouses, Territories, and Service Areas | Open | Operations | Core Platform, Inventory, Fleet, Dispatch, Reporting | Phase 03, Phase 08, Phase 09, Phase 10 |
| ODR-007 | Raw GPS Ping Retention Policy | Open | Operations | Fleet, Reporting, Security, Operations | Phase 10, Phase 15, Phase 20 |
| ODR-008 | Route Optimization Requirement | Open | Operations | Dispatch, Fleet, Orders / Logistics | Phase 09, Phase 19 |
| ODR-009 | Scheduled Emailed Reports Timing | Open | Operations | Reporting, Notifications, Integrations | Phase 12, Phase 16, Phase 20 |
| ODR-010 | Cerbos Adoption Timing | Open | Operations | Identity and Access, Permissions, Security | Phase 02, Phase 15, Phase 20 |
| ODR-011 | Application ID Format | Open | Operations | Data Platform, API, Offline, Integrations | Phase 02, Phase 03, Phase 14 |
| ODR-012 | Quote and Pricing MVP Scope | Open | Operations | CRM, Field Sales / Drilling, Orders, QuickBooks | Phase 04, Phase 07, Phase 09, Phase 13 |
| IDR-006 | Invoice Creation Ownership | Open | Integration | QuickBooks, Orders, Reporting | Phase 09, Phase 13 |
| ODR-013 | Serial and Lot Tracking Timing | Open | Operations | Inventory / Warehouse, Service, Reporting | Phase 08, Phase 18 |
| ODR-014 | Barcode Scanning Timing | Open | Operations | Inventory / Warehouse, Mobile, Dispatch | Phase 08, Phase 14, Phase 18 |
| PDR-013 | Reject Separate Products for CRM, Dispatch, Inventory, and Tracking | Rejected | Product | All modules | All phases |
| DDR-022 | Reject Public Exposure of MongoDB _id | Rejected | Data | API, Data Platform | All phases |
| ADR-012 | Full Offline App Parity Is Deferred | Deferred | Architecture | Mobile, Offline, All modules | Phase 14, Phase 20 |

# 9. Product and Scope Decisions

## PDR-001: One Core Platform With Optional Modules

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The platform combines CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet, dispatch, service, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

### Decision

Build one unified platform with optional modules enabled per company, not separate products stitched together.

### Rationale

Shared identity, activity, task, audit, files, search, reporting, and integration foundations reduce duplication and prevent inconsistent user experiences.

### Consequences

Module enablement must be configurable by company; shared foundations become cross-phase dependencies; modules must not create duplicate identity, customer, audit, search, or task systems.

### Implementation Guidance

Every phase must identify which optional modules it affects and must reuse shared platform foundations even when the phase focuses on one module.

### Risks

Module coupling may increase if shared services are poorly bounded; feature flags and clear owner modules are required.

### Review Triggers

Review if a module requires independent deployment, data residency, or a separate product contract.

### Related Decisions

ADR-001, DDR-001, PDR-002

## PDR-002: CRM and Operations Share a Unified Platform

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | CRM, Outbound Sales, Field Operations, Dispatch, Inventory, Fleet, Service, Reporting |
| Affected Phases | Phases 04-12 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Sales promises, field execution, logistics, inventory, fleet status, service work, and billing readiness must be visible together.

### Decision

CRM and operational modules must share Account, Contact, Activity, Task, AuditLog, reporting, and permission foundations.

### Rationale

The product promise depends on connecting what was sold to what is scheduled, delivered, serviced, and invoiced.

### Consequences

Future phases cannot design CRM, dispatch, inventory, fleet, or service as isolated systems with separate histories or identities.

### Implementation Guidance

Record detail pages must expose related records and activity timelines where permissions allow.

### Risks

Poor relationship modeling can create noisy timelines; phase documents must define which events appear on shared timelines.

### Review Triggers

Review if a customer requires CRM-only deployment with strict operational data separation.

### Related Decisions

PDR-001, DDR-007, UXDR-005

## PDR-003: Desktop-First Operations With Strong Mobile Support

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | Core Platform, CRM, Dispatch, Inventory, Fleet, Service, Mobile |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Office operators need dense planning, review, and reporting screens. Field users need fast capture workflows on mobile, including weak connectivity handling.

### Decision

Optimize desktop for operators and managers while designing mobile for field execution, capture, route work, check-ins, notes, photos, and completion.

### Rationale

The platform has different user modes; forcing full desktop parity onto mobile would slow field workflows and increase complexity.

### Consequences

Desktop phases must define table and workspace views; mobile phases must define focused task flows and offline behavior.

### Implementation Guidance

Do not shrink desktop tables into mobile workflows; design mobile screens around assigned work and capture.

### Risks

Some admin functions may be unavailable on mobile initially; this must be explicit in phase scope.

### Review Triggers

Review if native mobile becomes a launch requirement or if field users require offline access to more record types.

### Related Decisions

UXDR-001, ADR-009, ADR-010

## PDR-004: Reporting Designed From the Beginning

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | Reporting / Analytics, All operational modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Management visibility is a core success condition, and retrofitting analytics after workflow launch would be costly.

### Decision

Every phase must define reporting and analytics impact, including source data, statuses, timestamps, owners, filters, rollups, and audit/event dependencies.

### Rationale

Reporting-aware data design prevents missing fields, ambiguous status histories, and expensive runtime-only calculations.

### Consequences

Phase documents must not defer all metrics; even when a dashboard is later, data capture must be designed now.

### Implementation Guidance

Add reporting impact tables to every phase and identify required event records, rollups, snapshots, and filters.

### Risks

Over-instrumentation can slow delivery; metrics should focus on operational decisions and audit needs.

### Review Triggers

Review when custom report builder scope is confirmed or when performance tests show reporting bottlenecks.

### Related Decisions

DDR-008, DDR-009, PDR-007

## PDR-005: QuickBooks Is a First-Class Integration

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | Integrations, QuickBooks, CRM, Orders, Inventory, Reporting |
| Affected Phases | Phases 08-13 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Finance and administration require reliable accounting sync visibility, especially for QuickBooks.

### Decision

Design QuickBooks sync as a first-class integration with explicit mappings, sync jobs, sync logs, retry behavior, admin visibility, and external references.

### Rationale

Accounting sync affects customers, products/items, invoices, billing readiness, errors, retries, and support workflows.

### Consequences

QuickBooks-related fields and external IDs must be planned in source records and integration records; sync failures must not be silent.

### Implementation Guidance

Future phases touching Account, Product, Order, invoice readiness, or payments must document QuickBooks impact.

### Risks

QuickBooks object scope is not fully confirmed; premature deep mapping may create rework.

### Review Triggers

Review when exact QuickBooks objects, invoice ownership, tax requirements, and country scope are confirmed.

### Related Decisions

IDR-001, IDR-006, IDR-007

## PDR-008: LinkedIn Starts as Activity Logging

| Field | Value |
|---|---|
| Status | Recommended |
| Category | Product |
| Owner | Product Owner |
| Affected Modules | Outbound Sales, CRM, Integrations |
| Affected Phases | Phase 05, Phase 13 |
| Source | Master Documentation / Recommended |
| Last Reviewed | 2026-05-09 |

### Context

Outbound sales includes LinkedIn activity, but automatic LinkedIn workflow depth is unresolved.

### Decision

Treat LinkedIn as manual activity logging at first: connection request, message sent, profile viewed, comment, note, and follow-up.

### Rationale

Logging supports relationship context without prematurely building risky or provider-dependent automation.

### Consequences

Automated LinkedIn actions, templates, compliance checks, and workflow automation remain open until confirmed.

### Implementation Guidance

Outbound phase documents should model LinkedInActivity and follow-up tasks without assuming external LinkedIn automation.

### Risks

Manual logging may frustrate reps who expect automation; product messaging must be clear.

### Review Triggers

Review if customer requirements or integration feasibility confirm deeper LinkedIn automation.

### Related Decisions

IDR-005, ODR-008

## PDR-013: Reject Separate Products for CRM, Dispatch, Inventory, and Tracking

| Field | Value |
|---|---|
| Status | Rejected |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

A disconnected product approach conflicts with the platform promise and shared foundations.

### Decision

Rejected: do not build CRM, dispatch, inventory, and tracking as separate products with separate identity, customer, task, audit, or reporting systems.

### Rationale

Separate systems would recreate spreadsheets and manual reconciliation across modules.

### Consequences

All modules must integrate through shared platform foundations and canonical domain model.

### Implementation Guidance

Future phases must reject designs that create disconnected mini-products.

### Risks

Too much unification can create tight coupling; owner modules and APIs must remain clear.

### Review Triggers

Review only if a strategic product split is formally approved.

### Related Decisions

PDR-001, PDR-002

# 10. Tenant and Company Model Decisions

## DDR-001: Tenant Is the Top-Level SaaS Isolation Boundary

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Core Platform, Identity and Access, Security, All modules |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Tenant isolation is a product, security, and architecture requirement across the platform.

### Decision

Tenant is the highest SaaS isolation boundary. All tenant data must be scoped by tenant_id unless explicitly platform-global.

### Rationale

Tenant scoping prevents cross-customer data leakage and supports future deployment and data residency options.

### Consequences

Every business query, API request, worker job, sync job, audit log, and search index must enforce tenant scope.

### Implementation Guidance

Phase data models must include tenant_id on tenant-scoped and company-scoped records and explain any exception.

### Risks

Missing tenant scope creates critical security risk and migration difficulty.

### Review Triggers

Review if database isolation strategy changes or enterprise tenants require dedicated infrastructure.

### Related Decisions

SDR-001, ADR-002, ODR-005

## DDR-002: Company Is the Customer Organization Inside a Tenant

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Core Platform, Identity and Access, All modules |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

The platform supports multiple companies and optional modules per company. Company must not be confused with CRM Account.

### Decision

Company is the SaaS customer organization inside a Tenant. Account is the CRM business/customer/prospect/vendor record.

### Rationale

This separation prevents customer-organization records from being mixed with CRM records.

### Consequences

Company-scoped records must include company_id; CRM customer/prospect records must use Account.

### Implementation Guidance

Future phases must not create CustomerCompany, ClientCompany, CRMCompany, or other Company/Account duplicates.

### Risks

Users may use casual labels such as customer or client; documentation must map those labels to canonical entities.

### Review Triggers

Review if tenant structure needs reseller, franchise, or holding-company models.

### Related Decisions

DDR-001, DDR-003, DDR-018

## DDR-003: Company-Level Access Is the Primary Permission Boundary

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Security Lead |
| Affected Modules | Identity and Access, Permissions, All modules |
| Affected Phases | All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Permissions are company-scoped first, with deeper segmentation supported later.

### Decision

Company-level access through UserMembership is the primary permission boundary for normal users.

### Rationale

Company scoping keeps MVP access understandable while preserving branch, team, depot, warehouse, and policy extensions.

### Consequences

Most company records must be hidden unless the user has an active membership or tenant-level authorization for that company.

### Implementation Guidance

Phase documents must define default role access by company and document branch/team/depot/warehouse filters only when needed.

### Risks

Company-level scoping may be too broad for enterprise customers; policy-based restrictions must remain future-capable.

### Review Triggers

Review when branch, department, territory, depot, or warehouse-level permissions are required by launch customers.

### Related Decisions

DDR-004, SDR-002, SDR-003

## ODR-005: Tenant Database Isolation Model

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Engineering Lead |
| Affected Modules | Data Platform, Security, Operations |
| Affected Phases | Phase 02, Phase 15, Phase 20 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

The source documents do not confirm whether tenants use shared database separation, isolated databases, or hybrid isolation for enterprise customers.

### Decision

Open decision: choose shared database, isolated database, or hybrid tenant database model.

### Rationale

The choice affects security posture, cost, operations, migrations, backups, and enterprise sales.

### Consequences

Until resolved, design records with tenant_id and avoid assumptions that prevent future database isolation.

### Implementation Guidance

Phase documents must not hardcode architecture that makes hybrid isolation impossible.

### Risks

Late decision can force migration or refactoring.

### Review Triggers

Review before production architecture finalization and enterprise customer onboarding.

### Related Decisions

DDR-001, ADR-002, SDR-006

## ODR-006: Location Hierarchy for Branches, Departments, Depots, Warehouses, Territories, and Service Areas

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Product Architect |
| Affected Modules | Core Platform, Inventory, Fleet, Dispatch, Reporting |
| Affected Phases | Phase 03, Phase 08, Phase 09, Phase 10 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

The source documents support Branch, Department, Depot, Warehouse, and territories/service areas, but their hierarchy is not fully confirmed.

### Decision

Open decision: determine whether branches, departments, depots, warehouses, territories, and service areas are hierarchy levels, configurable location types, or related but separate scopes.

### Rationale

Hierarchy affects permissions, reporting filters, dispatch, inventory balances, and fleet assignment.

### Consequences

Use canonical entities already defined; do not invent a new universal hierarchy entity unless approved.

### Implementation Guidance

Phases should model clear required relationships and carry unresolved hierarchy questions forward.

### Risks

Wrong hierarchy can create reporting and permission rework.

### Review Triggers

Review during Phase 03 and Phase 08 scope finalization.

### Related Decisions

DDR-016, DDR-003

# 11. Identity and Access Decisions

## DDR-004: Users Belong to Companies Through UserMembership

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Identity and Access, Core Platform |
| Affected Phases | Phase 02, All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Users may belong to one or more companies, and memberships store roles, teams, status, and effective permissions.

### Decision

Use UserMembership as the canonical link between User, Company, roles, teams, branch scope, and access status.

### Rationale

A separate user record per company would break cross-company administration and create identity duplication.

### Consequences

Roles and permissions are assigned through membership context; membership status controls company access.

### Implementation Guidance

Do not create CompanyUser, UserCompanyRole, DriverUser, TechnicianUser, or module-specific identity duplicates.

### Risks

Membership complexity can grow; phase documents must keep the baseline clear and add policy only when justified.

### Review Triggers

Review if external workforce, subcontractor, or guest access introduces different membership needs.

### Related Decisions

DDR-003, SDR-002, DDR-017

## SDR-001: Super Admin Access Is Separate From Company Admin Access

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Core Platform, Identity and Access, Admin, Security |
| Affected Phases | Phase 02, Phase 15, All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Super admins configure global platform behavior; company admins configure company modules and users.

### Decision

Separate tenant/platform super admin capability from company admin capability and audit both.

### Rationale

Platform support access must not bypass company permissions casually, and company admins must not gain tenant-wide power by default.

### Consequences

Admin screens, permissions, audit events, and support workflows must distinguish global/tenant admin from company admin.

### Implementation Guidance

Every phase with admin behavior must state whether the action is platform-global, tenant-scoped, or company-scoped.

### Risks

Support workflows can become slow if super-admin access is too restricted; break-glass controls may be needed later.

### Review Triggers

Review when enterprise support tooling, impersonation, or delegated administration is designed.

### Related Decisions

DDR-001, DDR-003, SDR-005

# 12. Permissions and Authorization Decisions

## SDR-002: Role-Based Permissions Are the Baseline

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Identity and Access, Permissions, All modules |
| Affected Phases | Phase 02, All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The platform needs practical baseline permissions without overengineering enterprise policy rules too early.

### Decision

Use role-based permissions as the baseline authorization model, with permission keys assigned to roles through UserMembership.

### Rationale

RBAC is understandable for admins, testable by QA, and sufficient for many MVP workflows.

### Consequences

Every API and UI route must check role-derived permissions plus tenant/company scope.

### Implementation Guidance

Phase documents must define permission keys using lowercase dot notation and default roles.

### Risks

Role explosion can occur if roles are used for every conditional rule; policy support remains available.

### Review Triggers

Review when customers require branch, territory, field-value, export, or record-level conditional permissions.

### Related Decisions

SDR-003, SDR-004, DDR-004

## SDR-003: Policy-Based Authorization May Be Introduced Through Cerbos

| Field | Value |
|---|---|
| Status | Recommended |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Identity and Access, Permissions, Security |
| Affected Phases | Phase 02, Phase 15, Phase 20 |
| Source | Recommended |
| Last Reviewed | 2026-05-09 |

### Context

The domain model includes Policy for conditional access beyond static roles, and Cerbos is under consideration.

### Decision

Keep policy-based authorization future-capable and consider Cerbos when conditions exceed simple RBAC. Do not require Cerbos from day one unless complexity justifies it.

### Rationale

This avoids premature infrastructure complexity while preserving a path to branch, team, export, and record-level policies.

### Consequences

Permission data structures should not block a later Cerbos adoption; policy syntax must stay simple until required.

### Implementation Guidance

Future phases should document conditional rules as policies, not hardcoded role variants, when they have cross-phase impact.

### Risks

Adopting Cerbos later may require migration from internal checks; adopting too early may slow MVP.

### Review Triggers

Review before Phase 02 implementation finalization or when enterprise customer policy requirements become firm.

### Related Decisions

SDR-002, ODR-010

## SDR-004: Record-Level Permissions Are Future-Capable but Not Universal in MVP

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Permissions, CRM, Field Operations, Service, Reporting |
| Affected Phases | All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

The platform may require own/team/branch/record restrictions, but not every MVP feature needs full record-level ACLs.

### Decision

Design record-level permissions as future-capable, but require them in MVP only where specifically needed by a workflow or security boundary.

### Rationale

This balances implementation speed with future enterprise needs.

### Consequences

Records must include owner, assigned user/team, company, and branch/depot/warehouse fields where needed so future policies can use them.

### Implementation Guidance

Phase documents must identify whether visibility is own, team, company, branch, or custom policy based.

### Risks

Insufficient early fields can make later record-level permissions hard; shared fields must be preserved.

### Review Triggers

Review when sensitive records, cross-company admin, branch restrictions, or customer-specific privacy requirements arise.

### Related Decisions

SDR-002, SDR-003, DDR-009

## SDR-005: Permissions Must Be Auditable

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Identity and Access, Audit, Admin |
| Affected Phases | Phase 02, Phase 03, Phase 15, All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Permission changes are high-impact administrative actions.

### Decision

Role changes, membership changes, policy changes, API key changes, module enablement changes, and admin access changes must produce AuditLog entries.

### Rationale

Auditability supports security reviews, troubleshooting, and compliance expectations.

### Consequences

Permission mutation APIs must capture actor, before/after values, entity, tenant/company scope, timestamp, and reason where required.

### Implementation Guidance

Future phase documents must include audit events for every permission-impacting workflow.

### Risks

Audit logs may contain sensitive data; access to audit logs must itself be permission-controlled.

### Review Triggers

Review when audit retention, export, or external compliance requirements are defined.

### Related Decisions

SDR-001, SDR-002, DDR-012

## ODR-010: Cerbos Adoption Timing

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Security Lead |
| Affected Modules | Identity and Access, Permissions, Security |
| Affected Phases | Phase 02, Phase 15, Phase 20 |
| Source | Recommended / Open |
| Last Reviewed | 2026-05-09 |

### Context

Policy-based authorization may be needed, but adoption from day one is not confirmed.

### Decision

Open decision: determine whether Cerbos is adopted from day one or later.

### Rationale

This affects authorization architecture, testing, deployment, developer workflow, and policy migration.

### Consequences

Keep policy concepts compatible with future Cerbos adoption while implementing RBAC baseline.

### Implementation Guidance

Do not make phase documents depend on Cerbos unless this decision becomes accepted.

### Risks

Late adoption may require refactoring; early adoption may slow MVP.

### Review Triggers

Review before Phase 02 engineering implementation begins.

### Related Decisions

SDR-002, SDR-003

# 13. Module Architecture Decisions

## ADR-003: Redis and Workers Support Async Operational Work

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Backend API, Integrations, Reporting, Notifications, Imports/Exports, GPS |
| Affected Phases | Phases 03, 12, 13, 15, All relevant phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Imports, exports, sync, notifications, geofence evaluation, rollups, and long-running work must not block API requests.

### Decision

Use Redis where appropriate for caching, rate limiting, locks, ephemeral queues, and fanout; use workers for asynchronous jobs.

### Rationale

Separating request handling from long-running work improves reliability and user-visible error handling.

### Consequences

Every asynchronous workflow must define job status, retry behavior, logs, idempotency, and admin visibility where needed.

### Implementation Guidance

Phase documents must identify which actions enqueue jobs and how users see progress or failure.

### Risks

Queue misuse can hide failures; job observability and retry limits are required.

### Review Triggers

Review if queue volume, geofence processing, sync load, or report rollups outgrow the initial worker model.

### Related Decisions

ADR-001, IDR-003, ODR-002

# 14. Data Architecture Decisions

## DDR-005: Use Stable Application IDs

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Data Platform, API, Offline Mobile, Integrations |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Offline-capable workflows and public APIs need stable IDs independent of MongoDB internals.

### Decision

Every record must use immutable application-level id as the canonical identifier. IDs are opaque strings and may be generated client-side or server-side where offline requires it.

### Rationale

Stable IDs support public APIs, imports, sync, offline queues, logs, and support workflows.

### Consequences

Natural keys such as email, SKU, VIN, order number, or QuickBooks ID must not replace id.

### Implementation Guidance

All phase data models must include id and treat it as immutable after creation.

### Risks

ID generation format remains open; inconsistent generation can cause collisions or ordering issues.

### Review Triggers

Review when ULID, UUIDv7, KSUID, or another ID format is selected.

### Related Decisions

DDR-006, ODR-011

## DDR-006: Do Not Expose MongoDB _id as Public API ID

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | API, Data Platform, All modules |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

MongoDB _id is an internal storage detail and must not become the public contract.

### Decision

Public APIs, URLs, import/export, webhooks, external references, and UI routes must use application id, not MongoDB _id.

### Rationale

This preserves storage flexibility and prevents leaking internal implementation details.

### Consequences

Backend may store _id internally, but it must not appear as canonical public identifier.

### Implementation Guidance

API examples must use entity-specific parameters such as {account_id}, {job_id}, or {work_order_id}.

### Risks

Some libraries expose _id by default; serializers must explicitly prevent leakage.

### Review Triggers

Review only if storage technology or internal API boundaries change.

### Related Decisions

DDR-005, ADR-005

## DDR-007: Use References Instead of Deep Nesting for Searchable or Controlled Records

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Data Platform, All modules |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Many records require independent permissions, reporting, search, updates, audit, and integration mapping.

### Decision

Use references or link entities instead of deep nesting for records that need independent permissions, reporting, search, status, lifecycle, or frequent updates.

### Rationale

This keeps data queryable, auditable, and extensible across modules.

### Consequences

Small immutable snapshots may be embedded for historical readability, but mutable operational children should be referenced.

### Implementation Guidance

Phase documents must state whether each entity is embedded, referenced, append-only, snapshot, or current state.

### Risks

Over-referencing can increase query complexity; denormalized summaries may be needed for display.

### Review Triggers

Review when access patterns show performance or consistency problems.

### Related Decisions

ADR-002, DDR-008, DDR-009

## DDR-008: Use Denormalized Snapshots and Rollups for Dashboards

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Reporting / Analytics, All modules |
| Affected Phases | Phases 03, 12, All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Dashboards and operational reports cannot rely only on expensive runtime joins.

### Decision

Use denormalized snapshots, materialized rollups, and summary collections for expensive or frequently viewed metrics.

### Rationale

This supports responsive dashboards while preserving source event history.

### Consequences

Rollups must identify source data, calculation rules, refresh triggers, and staleness behavior.

### Implementation Guidance

Future phases must define reporting impact and indicate whether a rollup or snapshot is required.

### Risks

Rollups can become stale or inconsistent; reconciliation and rebuild jobs must be planned.

### Review Triggers

Review when dashboard performance budgets, custom reporting, or analytics storage are finalized.

### Related Decisions

PDR-004, DDR-009, ADR-003

## DDR-009: Use Append-Only Event Records for Operational History

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Audit, Inventory, Fleet, Field Operations, Integrations, Reporting |
| Affected Phases | All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Operational history must explain what happened over time and support audit, reporting, sync, and route replay.

### Decision

Use append-only event records where possible for operational history, including StockMovement, LocationPing, GeofenceEvent, AuditLog, SyncLog, HandoffEvent, and key check-in/progress events.

### Rationale

Append-only history improves traceability, replay, reconciliation, and investigations.

### Consequences

Current state records may be updated, but event history must not be overwritten except approved correction/redaction models.

### Implementation Guidance

Phase documents must distinguish current state from event history and define correction behavior.

### Risks

Append-only collections can grow quickly; retention and archiving policies are required for high-volume events.

### Review Triggers

Review when retention, compliance redaction, or high-volume storage costs are defined.

### Related Decisions

DDR-008, DDR-012, ODR-007

## DDR-010: Use Soft Delete for Major Business Records

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | All business modules |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Business records may be needed for audit, reporting, integration reconciliation, and restore workflows after removal from active use.

### Decision

Use soft delete or archive fields for major business records. Hard delete requires explicit global approval and retention policy.

### Rationale

Soft delete preserves history while keeping default lists clean.

### Consequences

Archived records are hidden by default but may be accessible through archived filters with permissions.

### Implementation Guidance

Phase documents must include deleted_at and deleted_by_user_id where soft delete applies and define restore rules where needed.

### Risks

Soft-deleted records may still affect uniqueness, reporting, and sync; phases must define behavior.

### Review Triggers

Review when legal retention, privacy deletion, or compliance redaction requirements are defined.

### Related Decisions

DDR-009, SDR-006

## ODR-011: Application ID Format

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Engineering Lead |
| Affected Modules | Data Platform, API, Offline, Integrations |
| Affected Phases | Phase 02, Phase 03, Phase 14 |
| Source | Global Domain Model Open Question |
| Last Reviewed | 2026-05-09 |

### Context

Stable application IDs are required, but the exact format is unresolved.

### Decision

Open decision: choose ULID, UUIDv7, KSUID, or another sortable opaque ID format.

### Rationale

ID format affects offline creation, sorting, logs, support, index locality, and readability.

### Consequences

Until resolved, all IDs are opaque strings and examples should not imply a final format beyond optional prefixes.

### Implementation Guidance

Do not parse IDs for business meaning.

### Risks

A poor choice can affect indexing and offline conflict handling.

### Review Triggers

Review before first production schema migration or API publication.

### Related Decisions

DDR-005, DDR-006

# 15. MongoDB Modeling Decisions

## ADR-002: MongoDB Is the Primary Operational Database

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Data Platform, All modules |
| Affected Phases | All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

The platform needs flexible operational records, event streams, snapshots, and module-specific schemas.

### Decision

Use MongoDB as the primary operational database for platform business records.

### Rationale

MongoDB supports document modeling, event collections, denormalized rollups, and extensible module data when governed by strict modeling rules.

### Consequences

Future phases must model collections carefully, avoid uncontrolled nesting, and preserve tenant/company scope and indexability.

### Implementation Guidance

Use MongoDB for operational state and event records; evaluate specialized stores only when a workload requires it.

### Risks

Poor schema discipline can create inconsistent data; global domain model rules are mandatory.

### Review Triggers

Review if analytics, search, time-series, or enterprise tenant isolation requires additional storage systems.

### Related Decisions

DDR-005, DDR-006, ADR-003

## DDR-011: Location Pings, Stock Movements, Audit Logs, and Sync Logs Are Append-Only

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Fleet, Inventory, Audit, Integrations |
| Affected Phases | Phases 08, 10, 13, 15, All relevant phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Certain records are evidence trails and should not be edited as normal mutable records.

### Decision

LocationPing, StockMovement, AuditLog, SyncLog, GeofenceEvent, DeviceHealthEvent, and high-impact operational event logs must be append-only by default.

### Rationale

These records support route replay, inventory reconciliation, compliance, and integration support.

### Consequences

Corrections must be modeled as reversal, adjustment, ignored, or replacement events, not in-place edits.

### Implementation Guidance

Future phases must not add edit/delete workflows for these event collections without approved correction semantics.

### Risks

High event volume creates storage and indexing pressure; retention is an open operations decision.

### Review Triggers

Review when retention rules, correction policies, or legal deletion requirements are finalized.

### Related Decisions

DDR-009, DDR-012, ODR-007

## DDR-022: Reject Public Exposure of MongoDB _id

| Field | Value |
|---|---|
| Status | Rejected |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | API, Data Platform |
| Affected Phases | All phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Public exposure of storage identifiers would leak implementation details and constrain future storage changes.

### Decision

Rejected: do not expose MongoDB _id in public API responses, URLs, webhooks, exports, or integration payloads as the canonical ID.

### Rationale

Application IDs are the public contract.

### Consequences

Serializers and schemas must suppress or map _id internally.

### Implementation Guidance

Future phase examples must not use _id as public ID.

### Risks

Developer mistakes are likely if default Mongo documents are returned directly.

### Review Triggers

Review only if this register is superseded by a storage strategy decision.

### Related Decisions

DDR-005, DDR-006

# 16. Event and Audit Decisions

## DDR-012: AuditLog Is Required for Important Administrative and Operational Actions

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Security Lead |
| Affected Modules | Audit, All modules |
| Affected Phases | All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

The platform must trace operational and administrative changes, especially permissions, inventory, dispatch, and sync.

### Decision

AuditLog is the canonical append-only compliance-grade audit record for important actions.

### Rationale

Audit logs support accountability, troubleshooting, permission reviews, and operational trust.

### Consequences

Create AuditLog entries for create, update, archive, restore, status transition, assignment, permission-impacting, export, import, sync, and high-impact operational changes.

### Implementation Guidance

Each phase must define audit events, actor, entity, captured before/after fields, and reason.

### Risks

Audit log volume and sensitive content must be managed; access to logs requires strict permissions.

### Review Triggers

Review when audit retention, export, or external compliance controls are defined.

### Related Decisions

SDR-005, DDR-011, SDR-006

# 17. API Architecture Decisions

## ADR-001: Backend Uses Python and FastAPI

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Backend API, All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The master architecture identifies Python and FastAPI as the preferred backend stack.

### Decision

Use Python and FastAPI for API services unless a formal architecture decision supersedes this.

### Rationale

FastAPI supports typed contracts, async request handling, and productive service development for the platform.

### Consequences

API standards, middleware, auth, validation, error handling, and background job handoff must be consistent across phases.

### Implementation Guidance

Phase API requirements should assume FastAPI-style REST endpoints and pydantic-style request/response schemas.

### Risks

Python ecosystem choices for workers, ODM, and migrations must be standardized to avoid fragmentation.

### Review Triggers

Review if scale, team skills, or provider constraints justify a different service stack.

### Related Decisions

ADR-004, ADR-005, ODR-001

## ADR-004: REST API Is the Primary API Style

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | API, All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The platform needs clear resource contracts for web, mobile, integrations, and documentation.

### Decision

Use REST as the primary API style for platform resources.

### Rationale

REST is straightforward for CRUD, list filters, saved views, jobs, imports/exports, and integrations.

### Consequences

GraphQL or specialized APIs may be considered later only with a specific need and decision record.

### Implementation Guidance

Phase API sections must define method, endpoint, purpose, permission, request, response, and errors.

### Risks

Poor REST design can create inconsistent resource names; global API naming rules must be followed.

### Review Triggers

Review when realtime subscriptions, complex reporting queries, or external developer needs justify another API pattern.

### Related Decisions

ADR-001, ADR-005, IDR-004

## ADR-005: API Endpoints Must Be Tenant and Company Scoped

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | API, Security, All modules |
| Affected Phases | All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

APIs are the primary path for web, mobile, integrations, and external access to business records.

### Decision

Every API endpoint must enforce tenant scope and, where applicable, company scope and module permissions.

### Rationale

Backend enforcement prevents UI bypass and cross-company data leakage.

### Consequences

Tenant/company context must come from authenticated session, membership, API key, route context, or explicit authorized admin scope.

### Implementation Guidance

Do not rely on frontend filtering for security; workers and background jobs must also enforce scope.

### Risks

Multi-company admin views can become complex; APIs must make scope explicit and testable.

### Review Triggers

Review if shared database vs isolated database strategy changes.

### Related Decisions

DDR-001, DDR-003, SDR-006

## ADR-006: Import and Export Run as Jobs

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Imports/Exports, All modules |
| Affected Phases | Phase 03, Phase 13, All relevant phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Large CSV, Excel, and report exports require validation, row-level errors, and long-running processing.

### Decision

Imports and exports must run asynchronously as jobs, with status, row-level validation, permissions, audit logging, and download or retry behavior.

### Rationale

Job-based processing avoids API timeouts and makes failures visible and recoverable.

### Consequences

Import/export jobs must be tenant/company scoped and permission checked.

### Implementation Guidance

Phase documents must define importable/exportable fields, validation errors, and audit events where imports/exports apply.

### Risks

Job queues can be overloaded; throttling and limits are required later.

### Review Triggers

Review when large customer migrations or scheduled report exports are scoped.

### Related Decisions

ADR-003, IDR-004, ODR-003

# 18. Frontend Architecture Decisions

## ADR-007: Frontend Uses Next.js

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Frontend, All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The master architecture identifies Next.js for the web application.

### Decision

Use Next.js for the web frontend architecture.

### Rationale

Next.js supports server-side data fetching for secure initial pages and client-side fetching for interactive workspaces.

### Consequences

Routing, layouts, auth guards, module guards, and page composition must be standardized.

### Implementation Guidance

Phase documents should assume Next.js route/page patterns and avoid incompatible frontend assumptions.

### Risks

Poor route organization can make module scaling difficult; global UI architecture rules are needed.

### Review Triggers

Review if native-only or micro-frontend architecture becomes required.

### Related Decisions

ADR-008, UXDR-001

## ADR-008: Styling Uses Tailwind CSS and shadcn/ui

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Design Lead |
| Affected Modules | Frontend, UX, All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The master architecture specifies Tailwind CSS and shadcn/ui for consistent layouts and components.

### Decision

Use Tailwind CSS and shadcn/ui as the baseline UI styling and component approach.

### Rationale

A shared component system reduces UI drift across 20 phases and supports fast implementation.

### Consequences

Phase documents must specify screen behavior and states rather than inventing new visual systems.

### Implementation Guidance

Introduce new components only when existing shared patterns cannot satisfy the workflow.

### Risks

Component inconsistency can still occur without governance; a UI component and page pattern document remains needed.

### Review Triggers

Review if design system requirements expand beyond shadcn/ui capabilities.

### Related Decisions

ADR-007, UXDR-001, UXDR-003

## UXDR-001: Support Light and Dark Mode

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Design Lead |
| Affected Modules | Frontend, All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The requested UX includes support for light and dark mode.

### Decision

All core screens and components must support light and dark mode.

### Rationale

Theme support affects design tokens, maps, tables, forms, and mobile readability.

### Consequences

UI implementation must avoid hardcoded colors that break either mode.

### Implementation Guidance

Phase UX requirements must include empty, loading, error, success, permission-denied, and theme-safe states.

### Risks

Dark mode map layers and third-party widgets may require provider-specific configuration.

### Review Triggers

Review if branding or tenant-level theming requirements expand.

### Related Decisions

ADR-008, UXDR-003

# 19. UX and Navigation Decisions

## UXDR-002: Desktop Operators Need Table, Kanban, Calendar, and Map Views

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Design Lead |
| Affected Modules | CRM, Outbound Sales, Calendar, Dispatch, Fleet, Inventory, Service |
| Affected Phases | Phases 04-12, 16 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Operators and managers need dense workspaces for lists, pipelines, schedules, dispatch boards, and location-aware workflows.

### Decision

Major desktop modules must support appropriate table, kanban, calendar, and map views where the workflow requires them.

### Rationale

Different operational workflows are best served by different view modes.

### Consequences

Not every entity needs every view, but each major list page must define its required views before implementation.

### Implementation Guidance

Phase documents must specify view modes, columns, filters, states, and bulk actions.

### Risks

Too many view modes can increase scope; view modes must match workflow value.

### Review Triggers

Review if users require additional views such as Gantt, route timeline, or board variants.

### Related Decisions

UXDR-003, UXDR-006, ADR-007

## UXDR-004: Mobile UX Focuses on Field Workflows, Not Desktop Parity

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Design Lead |
| Affected Modules | Mobile, Field Operations, Dispatch, Service, Fleet, Inventory |
| Affected Phases | Phases 07-11, 14 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Field users need assigned work, check-ins, notes, photos, proof, and sync reliability more than full admin and reporting screens.

### Decision

Mobile UX must prioritize assigned tasks, routes, check-ins, notes, photos, proof of delivery, service completion, and exception capture.

### Rationale

This keeps mobile fast, usable in field conditions, and compatible with offline support.

### Consequences

Full desktop parity is not required initially. Admin, reporting, and complex planning may remain desktop-first.

### Implementation Guidance

Phase documents must define mobile workflows only where the target users require field execution or capture.

### Risks

Field users may expect more mobile functionality; limitations must be explicit.

### Review Triggers

Review if native app scope or full offline parity becomes required.

### Related Decisions

PDR-003, ADR-009, UXDR-005

## UXDR-005: Activity Timeline Appears on Key Records

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Design Lead |
| Affected Modules | CRM, Field Operations, Dispatch, Inventory, Fleet, Service, Integrations |
| Affected Phases | Phases 04-13 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Every important operational event should produce searchable, reportable, permission-aware history.

### Decision

Key records must expose an activity timeline that combines relevant user actions, system events, notes, files, status changes, and related operational events where permissions allow.

### Rationale

Timelines connect CRM and operations and help users understand current state.

### Consequences

Timeline entries must respect permissions and avoid leaking restricted linked records.

### Implementation Guidance

Phase documents must define which events appear on timeline and which remain audit-only.

### Risks

Timelines can become noisy; filters and event relevance rules are needed.

### Review Triggers

Review when timeline volume, privacy, or cross-module display rules become problematic.

### Related Decisions

PDR-002, DDR-012, UXDR-004

# 20. Search, Filters, and Views Decisions

## UXDR-003: Major List Pages Define Filters Before Implementation

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Design Lead |
| Affected Modules | All modules, Search / Saved Views |
| Affected Phases | All phases |
| Source | Master Documentation / Global Documentation Rules |
| Last Reviewed | 2026-05-09 |

### Context

Search, filters, sorting, pagination, saved views, and column configuration are baseline list expectations.

### Decision

Each major list page must define searchable fields, filters, sorting, pagination, saved views, default columns, and permission-aware behavior before implementation.

### Rationale

Filters and saved views drive productivity and must be consistent across modules.

### Consequences

Implementation must not ship generic lists without explicit filter definitions.

### Implementation Guidance

Phase documents must include Search, Filters, and Saved Views sections even when not applicable.

### Risks

Overly broad filters can hurt performance; indexes and search strategy must align.

### Review Triggers

Review when advanced filters and saved views hardening is implemented.

### Related Decisions

UXDR-002, UXDR-006, DDR-008

## UXDR-006: Global Search Is a Core Platform Feature

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Product Architect |
| Affected Modules | Core Platform, Search, All modules |
| Affected Phases | Phase 03, All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Users need a single way to find accounts, jobs, orders, vehicles, inventory, service records, and operational history.

### Decision

Global search is a core platform feature and must respect tenant, company, module, role, and record permissions.

### Rationale

Search reinforces the one-platform model and reduces spreadsheet/manual lookup dependence.

### Consequences

Search indexing must include major entities and exclude records the user cannot access.

### Implementation Guidance

Phase documents must define searchable fields and permission constraints for new entities.

### Risks

Search can leak data through result titles or snippets; security tests must cover this.

### Review Triggers

Review when external search infrastructure, search relevance, or advanced indexing is selected.

### Related Decisions

DDR-001, DDR-003, UXDR-003

## UXDR-007: Saved Filters and Saved Views Are Supported

| Field | Value |
|---|---|
| Status | Accepted |
| Category | UX |
| Owner | Design Lead |
| Affected Modules | Search / Saved Views, All modules |
| Affected Phases | Phase 03, Phase 16, All phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Desktop operators need repeatable list configurations, filters, columns, sorting, grouping, and report-style views.

### Decision

Support saved filters and saved views for major list and reporting pages, with permission-aware sharing where applicable.

### Rationale

Saved views reduce repeated configuration and support team workflows.

### Consequences

Views must store filters, columns, sorting, grouping, owner, scope, and sharing permissions where supported.

### Implementation Guidance

Future phases must reuse SavedView rather than creating module-specific saved filter entities.

### Risks

Sharing saved views can leak assumptions or data; view execution must enforce current permissions.

### Review Triggers

Review during advanced filters, saved views, and custom fields hardening.

### Related Decisions

UXDR-003, UXDR-006, SDR-004

# 21. Reporting and Analytics Decisions

## DDR-013: Reporting Uses Rollups Rather Than Expensive Runtime Joins

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Reporting / Analytics, All modules |
| Affected Phases | Phase 12, All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Operational dashboards need performant metrics across statuses, timestamps, owners, events, inventory, dispatch, fleet, and service.

### Decision

Reporting should use materialized rollups and snapshots where runtime joins are expensive or unreliable.

### Rationale

This supports scalable dashboards and avoids fragile cross-collection aggregation at request time.

### Consequences

Reports must define source entities, metric definitions, rollup refresh rules, and staleness indicators.

### Implementation Guidance

Phase documents must not assume ad hoc runtime joins for high-volume metrics.

### Risks

Rollup bugs can create misleading metrics; reconciliation and test fixtures are required.

### Review Triggers

Review when analytics warehouse or custom report builder architecture is decided.

### Related Decisions

PDR-004, DDR-008

## PDR-009: Custom Report Builder Is Planned, Not Necessarily MVP

| Field | Value |
|---|---|
| Status | Recommended |
| Category | Product |
| Owner | Product Owner |
| Affected Modules | Reporting / Analytics |
| Affected Phases | Phase 12, Phase 20 |
| Source | Master Documentation / Recommended |
| Last Reviewed | 2026-05-09 |

### Context

The platform needs custom report foundations, but MVP should not attempt every advanced reporting capability.

### Decision

Plan for a custom report builder, but do not require full builder capability in MVP unless a customer need confirms it.

### Rationale

Early dashboards and saved reports can capture core metrics while preserving extensibility.

### Consequences

MetricDefinition, ReportDefinition, ReportRun, RollupSnapshot, and ScheduledReport should be modeled for future use as applicable.

### Implementation Guidance

Phase 12 must define MVP reports and future builder boundaries.

### Risks

If reporting is too limited, managers may continue using spreadsheets; core dashboards must still be useful.

### Review Triggers

Review when report users validate required metrics and scheduled report needs.

### Related Decisions

DDR-013, ODR-009

## ODR-009: Scheduled Emailed Reports Timing

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Product Owner |
| Affected Modules | Reporting, Notifications, Integrations |
| Affected Phases | Phase 12, Phase 16, Phase 20 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

Saved reports may support schedules later, but MVP timing is unresolved.

### Decision

Open decision: determine whether scheduled emailed reports are MVP or later.

### Rationale

This affects report definitions, notification/email providers, permissions, and export controls.

### Consequences

ReportDefinition should allow future schedule metadata, but scheduled delivery need not be built until accepted.

### Implementation Guidance

Do not assume scheduled emailing exists in MVP dashboards.

### Risks

Delayed scheduled reports may disappoint managers; early implementation may increase compliance risk.

### Review Triggers

Review during Phase 12 reporting scope and email provider selection.

### Related Decisions

PDR-009, PDR-012, SDR-007

# 22. Mobile and Offline Decisions

## ADR-009: Basic Offline Support Is Required

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Mobile, Field Operations, Dispatch, Service, Fleet, Inventory |
| Affected Phases | Phase 14, Relevant earlier phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Field users must not lose work when connectivity drops.

### Decision

Basic offline support is required for selected field workflows.

### Rationale

Offline capability is core to field trust but should be focused to avoid full app complexity.

### Consequences

Offline-supported records must carry stable IDs, tenant/company scope, actor, timestamps, sync metadata, and conflict strategy.

### Implementation Guidance

Every mobile/offline phase must define offline behavior, sync rules, and conflict handling.

### Risks

Offline bugs can corrupt data or create duplicate events; idempotency and tests are mandatory.

### Review Triggers

Review if field mobile delivery changes to native-first or if broader offline parity is required.

### Related Decisions

DDR-005, ADR-010, UXDR-004

## ADR-010: Offline Actions Use a Local Queue With Explicit Conflict Handling

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Engineering Lead |
| Affected Modules | Mobile, Sync, Field Operations, Dispatch, Service |
| Affected Phases | Phase 14, Relevant earlier phases |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Offline workflows include assigned tasks, routes, check-ins, notes, photos, and completion events.

### Decision

Offline actions must be stored in a local queue and synced with explicit conflict handling, idempotency, status, and user-visible failure states.

### Rationale

Queued actions preserve work and make sync recoverable after weak connectivity.

### Consequences

Conflict handling must be defined per workflow: append-only events usually sync safely; mutable state changes may require server merge, user resolution, or rejection.

### Implementation Guidance

Phase documents must state conflict behavior for every offline-capable workflow.

### Risks

Poor conflict UX can create user confusion; field users need clear resolution prompts.

### Review Triggers

Review when native app architecture or offline storage technology is selected.

### Related Decisions

ADR-009, DDR-009, DDR-005

## ADR-012: Full Offline App Parity Is Deferred

| Field | Value |
|---|---|
| Status | Deferred |
| Category | Architecture |
| Owner | Product Architect |
| Affected Modules | Mobile, Offline, All modules |
| Affected Phases | Phase 14, Phase 20 |
| Source | Master Documentation / Recommended |
| Last Reviewed | 2026-05-09 |

### Context

Mobile/offline support is required, but full desktop parity offline would be expensive and unnecessary for first operational release.

### Decision

Defer full offline app parity. Focus initial offline support on assigned tasks, routes, check-ins, notes, photos, proof, and selected event capture.

### Rationale

This preserves field reliability without overbuilding admin, reporting, and planning workflows offline.

### Consequences

Offline framework should not block future expansion to additional entities.

### Implementation Guidance

Phase 14 must explicitly list supported and unsupported offline workflows.

### Risks

Some users may expect offline access to all records; product documentation must set expectations.

### Review Triggers

Review after core field workflows are validated or if launch customer requires more offline breadth.

### Related Decisions

ADR-009, ADR-010, UXDR-004

# 23. Maps, GPS, and Geofencing Decisions

## ADR-011: Live Tracking Required Where Operationally Important

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Architecture |
| Owner | Product Architect |
| Affected Modules | Fleet, Dispatch, Field Operations |
| Affected Phases | Phases 09, 10, 14 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Dispatch and operations require live visibility into vehicles, drivers, crews, stops, delays, site work, and completion proof.

### Decision

Live tracking is required where operationally important, especially dispatch boards, live maps, active routes, and field check-ins.

### Rationale

Operational control depends on timely status and location, but not every module needs real-time behavior.

### Consequences

Real-time updates should be used for live maps, dispatch status, notifications, and selected operational changes; polling may be used where sufficient.

### Implementation Guidance

Phase documents must define stale states, update frequency expectations, and fallback behavior.

### Risks

Tracking raises privacy, battery, and data volume risks; permissions and settings must control it.

### Review Triggers

Review when GPS providers, mobile app platform, retention, or device strategy is confirmed.

### Related Decisions

DDR-014, ADR-012, SDR-008

## DDR-014: Historical Route Replay Is Required

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Fleet, Dispatch, Reporting |
| Affected Phases | Phase 10, Phase 12 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Managers need route history, proof, exceptions, geofence events, and check-in context after work completes.

### Decision

Historical route replay is required using LocationPing history overlaid with stops, geofence events, check-ins, and route context.

### Rationale

Route replay supports accountability, customer support, operational review, and safety investigations.

### Consequences

LocationPing must be append-only and queryable by vehicle/user, time range, source, and company scope.

### Implementation Guidance

Phase 10 must define route replay data and UX requirements.

### Risks

Raw ping retention may be expensive and is unresolved.

### Review Triggers

Review when GPS ping retention and storage strategy are decided.

### Related Decisions

ADR-011, DDR-011, ODR-007

## DDR-015: Geofence Entry and Exit Events Are Required

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Fleet, Field Operations, Dispatch, Service |
| Affected Phases | Phases 07, 09, 10, 14 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Geofencing and check-ins are required for site arrival, departure, route monitoring, and exceptions.

### Decision

Geofence events must capture enter, exit, dwell, missed arrival, late arrival, and unauthorized departure where configured.

### Rationale

Geofence events provide operational proof and trigger useful alerts and reports.

### Consequences

MVP may start with radius-based geofences; polygon support can come later.

### Implementation Guidance

Phase documents must distinguish user check-ins from system-generated geofence events.

### Risks

GPS accuracy can create false events; confidence, accuracy, and stale-location rules are needed.

### Review Triggers

Review when supported GPS sources and geofence shapes are confirmed.

### Related Decisions

ADR-011, DDR-014, UXDR-004

## DDR-021: Tracking Devices Are Assignable to Vehicles or Users

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Fleet, Mobile, Dispatch |
| Affected Phases | Phase 10, Phase 14 |
| Source | Master Documentation / Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Tracking sources include phones, tablets, and dedicated devices where permitted.

### Decision

TrackingDevice and DeviceAssignment must support assignment to Vehicle or User, with source, status, battery where available, and last-seen state.

### Rationale

This supports vehicle trackers, mobile devices, and mixed tracking strategies.

### Consequences

Assignments must be auditable and time-bounded where needed.

### Implementation Guidance

Phase 10 must define assignment workflow and stale device behavior.

### Risks

Privacy and consent rules may vary; security and compliance review is required.

### Review Triggers

Review when GPS providers, BYOD policy, and device assignment automation are selected.

### Related Decisions

ADR-011, DDR-019, SDR-008

## SDR-008: GPS and Device Tracking Require Permission and Visibility Controls

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Fleet, Mobile, Dispatch, Security |
| Affected Phases | Phase 10, Phase 14, Phase 15 |
| Source | Master Documentation / Recommended |
| Last Reviewed | 2026-05-09 |

### Context

Phone, tablet, and device tracking may expose sensitive worker location data.

### Decision

Location tracking must be permission-controlled, operationally justified, and visible through stale/last-seen/device health states.

### Rationale

Tracking is operationally necessary but must not become uncontrolled surveillance.

### Consequences

Users with tracking visibility must have explicit permissions; collection sources and device assignment must be auditable.

### Implementation Guidance

Phase 10 and Phase 14 must define consent/notice assumptions, visibility permissions, and stale tracking behavior.

### Risks

Legal requirements vary by jurisdiction; compliance review may be required.

### Review Triggers

Review when launch countries, BYOD policy, and GPS providers are known.

### Related Decisions

ADR-011, DDR-021, ODR-007

## ODR-007: Raw GPS Ping Retention Policy

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Security Lead |
| Affected Modules | Fleet, Reporting, Security, Operations |
| Affected Phases | Phase 10, Phase 15, Phase 20 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

LocationPing volume can grow quickly and contains sensitive movement data.

### Decision

Open decision: define how long raw GPS pings are retained and whether summarized history is retained longer.

### Rationale

Retention affects storage cost, route replay, privacy, analytics, and compliance.

### Consequences

Until resolved, phase docs must design LocationPing as append-only and include retention metadata hooks where appropriate.

### Implementation Guidance

Do not promise indefinite raw ping retention.

### Risks

Short retention may weaken investigations; long retention increases cost and privacy risk.

### Review Triggers

Review when tracking provider, legal region, and customer policy are known.

### Related Decisions

DDR-014, SDR-008

# 24. Inventory and Warehouse Decisions

## DDR-016: Multiple Warehouses and Depots Are Required

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Inventory / Warehouse, Dispatch, Fleet |
| Affected Phases | Phase 08, Phase 09, Phase 10 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The platform must support multiple warehouses, multiple truck depots, and multiple field operating locations.

### Decision

Model Warehouse and Depot as canonical inventory/operations locations with type, hierarchy, and company/branch scope as applicable.

### Rationale

Accurate inventory, dispatch, fleet assignment, and reporting require explicit location models.

### Consequences

InventoryBalance, StockMovement, Vehicle, RoutePlan, and transfer workflows must reference warehouses/depots where applicable.

### Implementation Guidance

Do not collapse all locations into one generic text field.

### Risks

Whether branches, depots, warehouses, and service areas form one hierarchy is open.

### Review Triggers

Review when location hierarchy and branch/department/depot/warehouse relationship is finalized.

### Related Decisions

ODR-002, DDR-017

## DDR-017: Stock Movements Are Event-Based and Balances Are Derived or Maintained From Events

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Engineering Lead |
| Affected Modules | Inventory / Warehouse, Reporting, Service, Dispatch |
| Affected Phases | Phase 08, Phase 11, Phase 12 |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Inventory history, auditability, transfer reconciliation, and service parts usage require event history.

### Decision

StockMovement is the append-only inventory event; InventoryBalance is current-state derived or maintained from StockMovement events.

### Rationale

This supports audit history, reconciliation, and reporting.

### Consequences

Receiving, picking, packing, transfers, adjustments, parts usage, and truck/depot movements must create StockMovement records.

### Implementation Guidance

Phase 08 must define movement types, balance update logic, and correction behavior.

### Risks

Incorrect event handling can produce wrong balances; reconciliation jobs are required.

### Review Triggers

Review when serial/lot tracking and barcode scanning decisions are made.

### Related Decisions

DDR-011, ODR-006, ODR-007

## DDR-018: Transfers, Receiving, Picking, Packing, and Adjustments Are Separate Models

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Inventory / Warehouse, Dispatch, Service |
| Affected Phases | Phase 08, Phase 09, Phase 11 |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Inventory workflows have distinct states, permissions, audit requirements, and operational meanings.

### Decision

Model receiving, picking, packing, transfers, and adjustments separately while connecting them to StockMovement events.

### Rationale

Separate models prevent workflow ambiguity and support targeted permissions and reporting.

### Consequences

Each workflow must define status, actor, timestamp, source/destination, discrepancy handling, and audit events.

### Implementation Guidance

Do not represent all inventory changes as generic notes or a single adjustment form.

### Risks

More entities increase implementation effort; MVP can start with essential fields but must preserve distinctions.

### Review Triggers

Review when warehouse process detail and barcode scope are validated.

### Related Decisions

DDR-017, ODR-006

## ODR-013: Serial and Lot Tracking Timing

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Product Owner |
| Affected Modules | Inventory / Warehouse, Service, Reporting |
| Affected Phases | Phase 08, Phase 18 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

Inventory MVP may be quantity-only or may require serial/lot tracking at launch.

### Decision

Open decision: determine whether inventory needs serial/lot tracking in early versions.

### Rationale

This affects InventoryItem, StockUnit, InventoryBalance, StockMovement, picking, receiving, service parts, and barcode workflows.

### Consequences

Keep data model future-capable for lot/serial fields but do not require full workflows until accepted.

### Implementation Guidance

Do not hide serial/lot requirements in custom_fields if they become core operational fields.

### Risks

Adding serial/lot later may require inventory migration.

### Review Triggers

Review before Phase 08 schema finalization.

### Related Decisions

DDR-017, DDR-018

## ODR-014: Barcode Scanning Timing

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Product Owner |
| Affected Modules | Inventory / Warehouse, Mobile, Dispatch |
| Affected Phases | Phase 08, Phase 14, Phase 18 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

Barcode scanning is a future expansion candidate but may be required by warehouse workflows.

### Decision

Open decision: determine whether barcode scanning is MVP or future.

### Rationale

This affects mobile hardware/browser support, BinLocation, Product, StockUnit, receiving, picking, packing, and transfer UX.

### Consequences

Treat barcode scanning as future-capable unless confirmed for MVP.

### Implementation Guidance

Use barcode-ready fields only where they do not overcomplicate MVP.

### Risks

Late barcode support may require UX and process redesign.

### Review Triggers

Review before Phase 08 and Phase 18 planning.

### Related Decisions

DDR-018, ODR-013

# 25. Orders, Dispatch, and Logistics Decisions

## PDR-010: Orders, Dispatch, and Logistics Use Manual Control First

| Field | Value |
|---|---|
| Status | Recommended |
| Category | Product |
| Owner | Product Owner |
| Affected Modules | Orders / Dispatch / Logistics, Fleet, Inventory |
| Affected Phases | Phase 09, Phase 19 |
| Source | Master Documentation / Recommended |
| Last Reviewed | 2026-05-09 |

### Context

Full route optimization is out of MVP unless reprioritized, but dispatchers need assignment, resequencing, exceptions, and live monitoring.

### Decision

Start with manual dispatch control, route sequencing, assignments, exception handling, and visibility; keep route optimization future-capable.

### Rationale

Manual control matches operational simplicity and avoids over-automation before rules are validated.

### Consequences

RoutePlan and DispatchPlan must support later optimization inputs such as capacity, distance, time windows, and constraints.

### Implementation Guidance

Phase 09 should not require an advanced optimization engine.

### Risks

Manual dispatch may not scale for larger fleets; optimization is likely later.

### Review Triggers

Review when dispatch volume, route complexity, or customer requirements justify optimization.

### Related Decisions

ODR-008, ADR-011

## ODR-008: Route Optimization Requirement

| Field | Value |
|---|---|
| Status | Open |
| Category | Operations |
| Owner | Product Owner |
| Affected Modules | Dispatch, Fleet, Orders / Logistics |
| Affected Phases | Phase 09, Phase 19 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

Manual dispatch is recommended initially, but dispatch selection strategy is unresolved.

### Decision

Open decision: determine whether dispatch selection is manual, proximity-based, capacity-based, route-optimized, or hybrid.

### Rationale

This affects routing data, UI complexity, algorithms, integrations, and dispatcher workflows.

### Consequences

Until resolved, Phase 09 should preserve route constraints and manual sequencing without requiring an optimizer.

### Implementation Guidance

Do not build advanced route optimization unless explicitly accepted.

### Risks

Insufficient data capture in early phases can limit later optimization.

### Review Triggers

Review before Phase 19 or if launch customer requires optimization earlier.

### Related Decisions

PDR-010, ADR-011

# 26. Fleet and Device Tracking Decisions

## DDR-019: Use Vehicle as Canonical Entity, Not Truck

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Fleet, Dispatch, Service |
| Affected Phases | Phase 10, All relevant phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

The platform tracks trucks and other road vehicles.

### Decision

Use Vehicle as the canonical entity for trucks, vans, and other fleet road assets. Do not create Truck as a separate core entity.

### Rationale

Vehicle is more extensible and prevents synonym drift.

### Consequences

UI may display truck where context requires, but data models, APIs, permissions, and reports must use Vehicle.

### Implementation Guidance

Future phases must not introduce FleetAsset or Truck unless approved as a specialized extension.

### Risks

Users may expect truck language; UI labels must be documented if different from entity names.

### Review Triggers

Review if non-road assets require separate Asset modeling.

### Related Decisions

DDR-020, DDR-021

## DDR-020: Drivers Are Users With Role and Membership Context

| Field | Value |
|---|---|
| Status | Recommended |
| Category | Data |
| Owner | Product Architect |
| Affected Modules | Fleet, Identity and Access, Dispatch |
| Affected Phases | Phase 10, Phase 02 |
| Source | Global Domain Model / Recommended |
| Last Reviewed | 2026-05-09 |

### Context

Drivers usually need to log in, see assigned routes, check in, and capture proof.

### Decision

Drivers should be Users with UserMembership and role context when they authenticate. Driver may exist as an operational profile/resource only when needed before full user account creation.

### Rationale

This avoids a separate identity system while allowing operational assignment.

### Consequences

Dispatch and fleet workflows must link driver assignments to User where possible.

### Implementation Guidance

Do not create separate driver login identities.

### Risks

Some drivers may be contractors or temporary resources; lightweight operational Driver records may still be needed.

### Review Triggers

Review when contractor and non-login driver workflows are confirmed.

### Related Decisions

DDR-004, DDR-019

# 27. Service and Work Order Decisions

## PDR-011: Service Uses WorkOrder as Canonical Execution Record

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | Service / Work Orders, Inventory, Field Operations |
| Affected Phases | Phase 11 |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Service workflows differ from generic Tasks and operational Jobs because they include technician work, parts, labor, checklist, and completion history.

### Decision

Use WorkOrder as the canonical service execution record. Use Job for generic operational field work and link only when workflow requires it.

### Rationale

This keeps service lifecycle and reporting distinct while still integrating with accounts, sites, inventory, and history.

### Consequences

Service tasks may exist as WorkOrderTask, but general follow-ups should use Task.

### Implementation Guidance

Phase 11 must not replace Job with WorkOrder globally or vice versa.

### Risks

Overlap between field jobs and service work may confuse users; phase docs must define when each applies.

### Review Triggers

Review when service and drilling operations share workflows that require tighter unification.

### Related Decisions

DDR-007, DDR-017

# 28. Integration Architecture Decisions

## IDR-001: External IDs Stored in External References

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Integration |
| Owner | Engineering Lead |
| Affected Modules | Integrations, QuickBooks, All synced modules |
| Affected Phases | Phase 13, All integration phases |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

Records synced to external providers need stable mapping without provider-specific fields scattered across modules.

### Decision

Store external IDs in external_refs and ExternalReference records. QuickBooks IDs must appear under external_refs.quickbooks and/or approved QuickBooks link entities.

### Rationale

Centralized external references simplify sync, reconciliation, retries, and future integration marketplace support.

### Consequences

Provider-specific mappings belong to integration-owned records unless an approved link entity exists.

### Implementation Guidance

Future phases must not add ad hoc qbo_id, provider_id, or external_customer_id fields directly without approval.

### Risks

Mapping complexity may require provider-specific link entities; those must be explicitly documented.

### Review Triggers

Review when new integration providers require additional mapping semantics.

### Related Decisions

PDR-005, IDR-006

## IDR-002: Integration Sync Has Explicit Logs and Retry Behavior

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Integration |
| Owner | Engineering Lead |
| Affected Modules | Integrations, QuickBooks, Notifications, Admin |
| Affected Phases | Phase 13, All integration phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

No silent failure is a guiding principle, and integrations can fail for provider, credential, validation, or mapping reasons.

### Decision

Every integration sync must have SyncJob/SyncLog records, status, attempts, retry policy, error details, and admin-visible resolution actions.

### Rationale

Visible sync behavior improves support and prevents data loss or user confusion.

### Consequences

Sync jobs must support queued, running, succeeded, failed, partially_failed, skipped, and retrying states.

### Implementation Guidance

Phase documents must define sync triggers, idempotency keys, validation, retries, and admin error views.

### Risks

Verbose errors can expose sensitive data; sanitize logs while preserving troubleshooting value.

### Review Triggers

Review when provider rate limits, retry policy, or admin sync tooling is finalized.

### Related Decisions

ADR-003, IDR-001, PDR-005

## IDR-003: Webhooks Are Part of the Integration Layer

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Integration |
| Owner | Engineering Lead |
| Affected Modules | Integrations, API, Webhooks |
| Affected Phases | Phase 13, All relevant phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

External systems need event notifications from platform workflows.

### Decision

Webhooks are integration-layer resources with company/module configuration, delivery logs, retries, signing, and permission-controlled management.

### Rationale

Treating webhooks as integrations avoids one-off outbound HTTP calls from feature modules.

### Consequences

Webhook delivery must use async jobs and WebhookDelivery logs.

### Implementation Guidance

Phase documents must identify events eligible for webhooks, payload shape ownership, and failure behavior.

### Risks

Webhook payloads can leak data; scopes and signatures are mandatory.

### Review Triggers

Review when external developer platform requirements are finalized.

### Related Decisions

ADR-006, IDR-004, SDR-007

## IDR-004: Email, SMS, WhatsApp, API, and Webhooks Are Planned Integration Surfaces

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Integration |
| Owner | Product Architect |
| Affected Modules | Integrations, Outbound Sales, Notifications, API |
| Affected Phases | Phases 05, 13, 16, 17 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Outbound channels and platform integrations include email, SMS, WhatsApp, REST API, webhooks, and imports/exports.

### Decision

Plan integration surfaces for email, SMS, WhatsApp, REST API, webhooks, CSV, and Excel, with provider abstraction where applicable.

### Rationale

This enables communication workflows without tightly coupling feature modules to providers.

### Consequences

Provider-specific sending automation may be phased; logs and activities can exist before full automation.

### Implementation Guidance

Future phases must distinguish activity logging from provider-executed send/sync actions.

### Risks

Compliance requirements for messaging vary by region and provider; messaging automation may need policy controls.

### Review Triggers

Review when providers, countries, consent requirements, and messaging compliance rules are confirmed.

### Related Decisions

IDR-003, PDR-008, SDR-007

# 29. QuickBooks Decisions

## IDR-005: QuickBooks Customer, Invoice, and Item Links Are Approved Link Entities

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Integration |
| Owner | Engineering Lead |
| Affected Modules | QuickBooks, Integrations, CRM, Orders, Inventory |
| Affected Phases | Phase 13 |
| Source | Global Domain Model |
| Last Reviewed | 2026-05-09 |

### Context

QuickBooks mappings need explicit records for customer, invoice, and item sync.

### Decision

Use QuickBooksCustomerLink, QuickBooksInvoiceLink, and QuickBooksItemLink as approved QuickBooks link entities, alongside external_refs.quickbooks where applicable.

### Rationale

These links support sync state, mapping details, timestamps, errors, and provider object IDs without polluting source modules.

### Consequences

Additional QuickBooks link entities require a new decision.

### Implementation Guidance

Phase 13 must define the exact mapping fields and source entity relationships.

### Risks

Invoice ownership is unresolved; link entity use must not imply invoices are created in-app.

### Review Triggers

Review when exact first-release QuickBooks objects are confirmed.

### Related Decisions

PDR-005, IDR-001, ODR-005

## IDR-006: Invoice Creation Ownership

| Field | Value |
|---|---|
| Status | Open |
| Category | Integration |
| Owner | Product Owner |
| Affected Modules | QuickBooks, Orders, Reporting |
| Affected Phases | Phase 09, Phase 13 |
| Source | Master Documentation Open Question |
| Last Reviewed | 2026-05-09 |

### Context

The source documents do not confirm whether invoices are created in-app, synced to QuickBooks, or created only in QuickBooks.

### Decision

Open decision: determine invoice creation ownership and sync direction.

### Rationale

Invoice ownership affects data model, UI, permissions, accounting controls, QuickBooks mappings, and billing state.

### Consequences

Until resolved, model billing_status and QuickBooksInvoiceLink carefully without assuming full in-app invoicing.

### Implementation Guidance

Do not design the platform as a full accounting ledger replacement.

### Risks

Wrong invoice ownership can create accounting reconciliation issues.

### Review Triggers

Review during QuickBooks integration scope definition.

### Related Decisions

PDR-005, IDR-005

# 30. Notification Decisions

## PDR-012: Notifications Are Useful, Permission-Aware, and Configurable

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | Notifications, All modules |
| Affected Phases | Phase 16, All relevant phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Notifications should alert users to assignments, exceptions, sync failures, and important state changes without creating noise.

### Decision

Notifications must be permission-aware, user/company configurable where appropriate, and generated only for useful state changes.

### Rationale

This prevents information leakage and notification fatigue.

### Consequences

Notification records must not expose inaccessible entities in title, body, links, or metadata.

### Implementation Guidance

Phase documents must define trigger, recipient, channel, timing, preference behavior, and access checks.

### Risks

Under-notification can hide operational failures; over-notification reduces trust.

### Review Triggers

Review when customer-facing notifications and scheduled reports are scoped.

### Related Decisions

SDR-007, UXDR-005

# 31. Security and Compliance Decisions

## SDR-006: Tenant and Company Isolation Must Be Tested

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Security, QA, All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Tenant/company isolation is a core security and product requirement.

### Decision

Every phase must include tests for tenant and company isolation, permission checks, and blocked cross-company access.

### Rationale

Authorization defects are critical and must be caught before rollout.

### Consequences

QA and automated tests must cover API, UI, search, reports, workers, webhooks, imports/exports, and sync jobs.

### Implementation Guidance

Do not mark a phase complete unless isolation tests pass for affected modules.

### Risks

Tests may miss background jobs and search indexes; coverage must include non-API paths.

### Review Triggers

Review during security audit, enterprise readiness, or after any authorization incident.

### Related Decisions

DDR-001, DDR-003, ADR-005

## SDR-007: API Keys, Webhooks, and Exports Are Scoped, Revocable, Auditable, and Rate-Limited

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Security |
| Owner | Security Lead |
| Affected Modules | Integrations, API, Webhooks, Imports/Exports |
| Affected Phases | Phase 13, Phase 15, Phase 20 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

External access and data extraction create high security and compliance risk.

### Decision

API keys, webhook endpoints, and export actions must be scoped, revocable, auditable, and rate-limited.

### Rationale

This protects tenant data and supports operational control.

### Consequences

Admin UI must show key status, scope, last used, creator, and revoke action where applicable.

### Implementation Guidance

Phase documents must define permission keys and audit events for creating, using, and revoking external access.

### Risks

Overly broad keys can leak data; least privilege should be default.

### Review Triggers

Review when external developer portal or enterprise API governance is planned.

### Related Decisions

IDR-003, ADR-006, SDR-006

# 32. Import, Export, and Webhook Decisions

## IDR-007: CSV and Excel Imports Validate Rows and Report Errors

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Integration |
| Owner | Engineering Lead |
| Affected Modules | Imports/Exports, All modules |
| Affected Phases | Phase 03, Phase 13, All relevant phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

CSV and Excel imports are planned integration surfaces and can create large volumes of operational data.

### Decision

CSV and Excel imports must validate data before committing records and must produce row-level errors for failed rows.

### Rationale

Row-level validation prevents partial confusion and supports user correction without support intervention.

### Consequences

Import jobs must be asynchronous, tenant/company scoped, permission checked, and auditable.

### Implementation Guidance

Future phases must define importable fields, required columns, validation rules, duplicate handling, and failure output for each import workflow.

### Risks

Large imports can overload workers or create duplicates; limits and idempotency should be defined.

### Review Triggers

Review when migration tooling and launch customer import sources are confirmed.

### Related Decisions

ADR-006, SDR-007

# 33. Deployment, Monitoring, and Operations Decisions

## ODR-001: Use Structured Logging and Correlation IDs

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Operations |
| Owner | Engineering Lead |
| Affected Modules | Backend API, Workers, Integrations, Monitoring |
| Affected Phases | Phase 15, All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

Operational support requires tracing API, worker, sync, import/export, notification, and geofence flows.

### Decision

Use structured logs with correlation IDs across API and worker flows.

### Rationale

This enables debugging, observability, and incident response across asynchronous workflows.

### Consequences

Every high-impact job or API call should carry tenant, company, actor, request/job ID, and correlation ID where safe.

### Implementation Guidance

Phase implementation notes must identify key logs and monitoring signals for new workflows.

### Risks

Logs may contain sensitive data; redaction rules are required.

### Review Triggers

Review when monitoring platform and log retention are selected.

### Related Decisions

ADR-001, ADR-003, ODR-002

## ODR-002: Deployment Must Support API, Worker, Realtime, and Scheduled Jobs

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Operations |
| Owner | Engineering Lead |
| Affected Modules | Operations, Backend API, Workers, Realtime, Reporting |
| Affected Phases | Phase 15, Phase 20 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The architecture separates API handling from async jobs and uses real-time updates where valuable.

### Decision

Deployment architecture must support API services, worker services, scheduled jobs, realtime fanout, and operational monitoring.

### Rationale

The platform cannot run reliably as a single monolithic request-only process.

### Consequences

Deployment docs must define service roles, scaling, health checks, environment variables, and failure modes.

### Implementation Guidance

Future phases must not assume long-running jobs execute inside request handlers.

### Risks

More service roles increase operational complexity; MVP deployment should be as simple as possible while preserving separation.

### Review Triggers

Review when cloud provider, container platform, and scale requirements are selected.

### Related Decisions

ADR-003, ADR-011, ODR-001

## ODR-003: Admin-Visible Failure States Are Required

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Operations |
| Owner | Product Architect |
| Affected Modules | Admin, Integrations, Imports/Exports, Offline, Notifications, GPS |
| Affected Phases | Phase 03, 13, 14, 15 |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

No silent failure is a guiding principle. Sync failures, offline conflicts, GPS permission issues, and data validation errors must be visible and recoverable.

### Decision

Admin and user workflows must expose actionable failure states for sync, import/export, offline sync, notifications, and GPS/device issues.

### Rationale

Visibility reduces support burden and operational risk.

### Consequences

Failures must include status, affected record, retry/resolve actions, timestamp, owner, and safe error details where applicable.

### Implementation Guidance

Phase documents must include error states and recovery paths for all async or external workflows.

### Risks

Too many failure surfaces can overwhelm admins; dashboards should prioritize actionable issues.

### Review Triggers

Review when admin monitoring and alerting are designed.

### Related Decisions

IDR-002, ADR-010, ODR-001

# 34. MVP and Phase Sequencing Decisions

## PDR-006: MVP Must Not Attempt the Full Platform at Once

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Owner |
| Affected Modules | All modules |
| Affected Phases | All phases |
| Source | Master Documentation |
| Last Reviewed | 2026-05-09 |

### Context

The target platform is broad and includes advanced permissions, route optimization, barcode scanning, custom reporting, integrations, and enterprise hardening.

### Decision

MVP must deliver a usable operational slice and foundation without attempting every advanced capability at launch.

### Rationale

A phased approach reduces scope risk while preserving extensibility for later modules.

### Consequences

Phase documents must distinguish MVP, Later, and Future scope and avoid introducing advanced features unless required by the phase objective.

### Implementation Guidance

When in doubt, document future capability seams rather than implementing full capability immediately.

### Risks

Deferring too much may create unusable workflows; MVP cuts must preserve tenant safety, auditability, core workflows, and sync reliability.

### Review Triggers

Review during phase planning, customer validation, or when launch customer requirements change.

### Related Decisions

PDR-007, ADR-003, PDR-009

## PDR-007: Use the Planned 20-Document Phase Structure

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Product |
| Owner | Product Architect |
| Affected Modules | Documentation, All modules |
| Affected Phases | All phases |
| Source | Master Documentation / Global Documentation Rules |
| Last Reviewed | 2026-05-09 |

### Context

The master documentation defines 20 future phase documents and global rules require summaries for continuity.

### Decision

Future work must use the planned 20-phase structure unless a formal decision changes it. Phase 20 consolidates enterprise readiness and scale hardening, not major net-new product scope.

### Rationale

Stable phase structure prevents duplicate design work and helps future AI writers consume summaries instead of all prior documents.

### Consequences

Every phase document must include a Summary for Future Phases and must respect prior phase summaries and this register.

### Implementation Guidance

Do not create unrelated phase documents or merge phases without a proposed change to this decision.

### Risks

Rigid phasing can slow urgent customer needs; exceptions require explicit decision records.

### Review Triggers

Review if delivery planning changes the phase sequence, splits a phase, or adds a phase beyond 20.

### Related Decisions

PDR-006, ODR-004

## ODR-004: Phase Documents Rely on Summaries Instead of Full Prior Documents

| Field | Value |
|---|---|
| Status | Accepted |
| Category | Operations |
| Owner | Product Architect |
| Affected Modules | Documentation, All modules |
| Affected Phases | All phases |
| Source | Global Documentation Rules |
| Last Reviewed | 2026-05-09 |

### Context

Future writers need continuity across 20 documents without re-reading every full prior document each time.

### Decision

Every phase must end with Summary for Future Phases and future phases should rely on these summaries plus global control documents and relevant prior phase details.

### Rationale

This keeps phase generation scalable and reduces contradiction risk.

### Consequences

Summaries must capture final decisions, entities, fields, APIs, permissions, UX patterns, reports, notifications, audit events, integrations, dependencies, constraints, and open questions.

### Implementation Guidance

Do not omit the summary or leave it generic.

### Risks

Poor summaries will cause future drift; architect review must validate them.

### Review Triggers

Review if a documentation management system or decision database replaces Markdown summaries.

### Related Decisions

PDR-007, ODR-001

# 35. Open Decision Backlog

The following open or partly unresolved decisions must be carried forward until resolved. Future phase writers must not invent answers without documenting a recommended or accepted decision.

| ID | Open Decision | Owner | Affected Phases | Impact If Unresolved |
|---|---|---|---|---|
| ODR-005 | Tenant Database Isolation Model | Engineering Lead | Phase 02, Phase 15, Phase 20 | Late decision can force migration or refactoring. |
| ODR-006 | Location Hierarchy for Branches, Departments, Depots, Warehouses, Territories, and Service Areas | Product Architect | Phase 03, Phase 08, Phase 09, Phase 10 | Wrong hierarchy can create reporting and permission rework. |
| ODR-007 | Raw GPS Ping Retention Policy | Security Lead | Phase 10, Phase 15, Phase 20 | Short retention may weaken investigations; long retention increases cost and privacy risk. |
| ODR-008 | Route Optimization Requirement | Product Owner | Phase 09, Phase 19 | Insufficient data capture in early phases can limit later optimization. |
| ODR-009 | Scheduled Emailed Reports Timing | Product Owner | Phase 12, Phase 16, Phase 20 | Delayed scheduled reports may disappoint managers; early implementation may increase compliance risk. |
| ODR-010 | Cerbos Adoption Timing | Security Lead | Phase 02, Phase 15, Phase 20 | Late adoption may require refactoring; early adoption may slow MVP. |
| ODR-011 | Application ID Format | Engineering Lead | Phase 02, Phase 03, Phase 14 | A poor choice can affect indexing and offline conflict handling. |
| ODR-012 | Quote and Pricing MVP Scope | Product Owner | Phase 04, Phase 07, Phase 09, Phase 13 | Deferring pricing may limit sales-to-operations handoff; including it may expand scope significantly. |
| IDR-006 | Invoice Creation Ownership | Product Owner | Phase 09, Phase 13 | Wrong invoice ownership can create accounting reconciliation issues. |
| ODR-013 | Serial and Lot Tracking Timing | Product Owner | Phase 08, Phase 18 | Adding serial/lot later may require inventory migration. |
| ODR-014 | Barcode Scanning Timing | Product Owner | Phase 08, Phase 14, Phase 18 | Late barcode support may require UX and process redesign. |

# 36. Decision Review Process

Decision reviews must occur when a phase proposes a new cross-phase rule, changes an accepted decision, resolves an open decision, or discovers a contradiction between source documents.

Review process:

1. Identify the affected decision IDs.
2. Confirm whether the proposed change is local to one phase or global across phases.
3. If global, create a new decision record or update the status of an existing one.
4. If replacing a prior accepted decision, mark the prior decision `Superseded` and reference the new decision ID.
5. Update the Global Decision Index.
6. Carry the decision into the phase document's `Recommended Decisions` or `Summary for Future Phases` section.
7. Do not delete old decision IDs. Historical traceability matters.

Minimum review owners:

| Decision Type | Required Owner | Secondary Reviewer |
|---|---|---|
| Product scope | Product Owner | Product Architect |
| Architecture | Engineering Lead | Product Architect |
| Data/domain | Product Architect | Engineering Lead |
| UX/navigation | Design Lead | Product Architect |
| Integration | Engineering Lead | Product Owner |
| Security/permissions | Security Lead | Engineering Lead |
| Operations/deployment | Engineering Lead | Security Lead where applicable |

# 37. Rules for Future Phase Writers

- Do not override accepted decisions.
- Do not silently contradict recommended decisions.
- If a phase requires changing a decision, mark it as a proposed change.
- Use open decisions as open questions unless the phase has enough information to recommend a decision.
- Add new decisions to this register when a phase creates cross-phase impact.
- Do not duplicate decisions already recorded.
- Keep decision IDs stable.
- Do not renumber existing decision IDs.
- Do not casually rename existing entities, modules, or phases.
- Do not create duplicate identity, customer, task, audit, search, inventory, fleet, or integration models.
- Do not hide decisions in prose; add them to this register or to the phase's recommended decisions section.
- Do not use `TBD` without also adding an open question.
- Do not design APIs without tenant/company scope and permission checks.
- Do not design mobile field workflows without offline and sync behavior.
- Do not design integrations without retry, logs, error visibility, and admin recovery.
- Do not design reports without source data, filters, and rollup/snapshot impact.

# 38. Summary for Future Phases

This register establishes binding and recommended cross-phase decisions for the platform. Future phases must use it as a control document alongside the master documentation, global documentation rules, and global domain model.

The most important cross-phase constraints are:

- Build one modular but unified platform.
- Preserve tenant and company isolation everywhere.
- Use the canonical global domain model.
- Use stable application IDs and never expose MongoDB `_id`.
- Use MongoDB as the operational database with disciplined references, events, snapshots, and rollups.
- Use Python/FastAPI, REST APIs, Next.js, Tailwind CSS, and shadcn/ui unless superseded.
- Use RBAC baseline and keep policy-based authorization future-capable.
- Audit important actions.
- Make sync, offline, GPS, import/export, and integration failures visible and recoverable.
- Keep MVP scoped and defer advanced capabilities unless accepted.

# Summary for Future Phases

## Final Decisions Made

Accepted decisions: PDR-001, PDR-002, PDR-003, PDR-004, PDR-005, PDR-006, PDR-007, DDR-001, DDR-002, DDR-003, DDR-004, SDR-001, SDR-002, SDR-004, SDR-005, ADR-001, ADR-002, ADR-003, DDR-005, DDR-006, DDR-007, DDR-008, DDR-009, DDR-010, DDR-011, DDR-012, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008, UXDR-001, UXDR-002, UXDR-003, UXDR-004, UXDR-005, UXDR-006, UXDR-007, DDR-013, ADR-009, ADR-010, ADR-011, DDR-014, DDR-015, DDR-016, DDR-017, DDR-018, DDR-019, DDR-021, PDR-011, IDR-001, IDR-002, IDR-003, IDR-004, IDR-005, PDR-012, SDR-006, SDR-007, SDR-008, ODR-001, ODR-002, ODR-003, ODR-004, IDR-007.

Key accepted outcomes:

- The platform is one core modular SaaS platform with optional modules.
- CRM and operations share common identity, activity, task, audit, search, reporting, and integration foundations.
- Tenant is the top-level isolation boundary and Company is the customer organization inside the SaaS platform.
- Company-level access through UserMembership is the primary permission boundary.
- Super admin and company admin access are separate.
- RBAC is the baseline authorization model.
- Permissions and high-impact changes must be auditable.
- MongoDB is the primary operational database.
- Stable application IDs are required and MongoDB `_id` must not be exposed as the public API ID.
- Append-only event records are required for operational history where appropriate.
- Soft delete is the default for major business records.
- Backend uses Python/FastAPI and REST APIs.
- Frontend uses Next.js, Tailwind CSS, and shadcn/ui.
- Global search, saved views, activity timelines, reporting impact, and permission-aware filters are core platform expectations.
- Basic offline support is required for field workflows.
- Live tracking, route replay, geofence events, and device last-seen/health tracking are required where operationally important.
- Multiple warehouses and depots are required.
- Stock movements are event-based and inventory balances are derived or maintained from movement events.
- Vehicle is the canonical entity, not Truck.
- QuickBooks is a first-class integration.
- Webhooks are part of the integration layer.
- Tenant/company isolation must be tested.
- Phase documents must follow the planned 20-phase structure and include summaries for future phases.

## Recommended Decisions

Recommended decisions: PDR-008, SDR-003, PDR-009, DDR-020, PDR-010.

Recommended defaults:

- LinkedIn should begin as manual activity logging unless deeper automation is confirmed.
- Cerbos should remain future-capable but not required from day one unless policy complexity justifies it.
- Custom report builder is planned but not necessarily MVP.
- Drivers should be Users with membership and role context when they authenticate.
- Orders, dispatch, and logistics should use manual dispatcher control first while preserving future optimization seams.

## Open Decisions

Open decisions: ODR-005, ODR-006, ODR-007, ODR-008, ODR-009, ODR-010, ODR-011, ODR-012, IDR-006, ODR-013, ODR-014.

Open questions carried forward include:

- Shared database vs isolated database vs hybrid tenant database model.
- Whether branches, departments, depots, warehouses, territories, and service areas should all be hierarchy levels.
- Whether LinkedIn remains logging-only or grows into workflow automation.
- Whether quote/pricing belongs in MVP.
- Whether invoices are created in-app or only synced to QuickBooks.
- Whether inventory needs serial/lot tracking in early versions.
- Whether barcode scanning is MVP or future.
- Whether route optimization is required or manual dispatch is enough.
- Whether scheduled emailed reports are MVP or later.
- Whether Cerbos should be adopted from day one or later.
- Application ID format.
- GPS ping retention policy.

## Rejected Decisions

Rejected decisions: PDR-013, DDR-022.

Rejected outcomes:

- Do not build CRM, dispatch, inventory, and tracking as disconnected products with separate foundations.
- Do not expose MongoDB `_id` as the public API identifier.

Deferred decisions: ADR-012.

Deferred outcomes:

- Full offline app parity is deferred; initial offline support focuses on field execution and capture workflows.

## Decision ID Rules

- Use ADR-### for architecture decisions.
- Use PDR-### for product decisions.
- Use DDR-### for data/domain decisions.
- Use UXDR-### for UX decisions.
- Use IDR-### for integration decisions.
- Use SDR-### for security decisions.
- Use ODR-### for operations decisions.
- Keep IDs stable.
- Do not renumber IDs.
- Supersede old decisions rather than deleting or renumbering them.

## Decision Status Rules

- `Accepted` decisions are binding.
- `Recommended` decisions are the default direction and must not be contradicted silently.
- `Open` decisions must be carried as open questions until resolved.
- `Deferred` decisions must not be implemented unless reprioritized.
- `Rejected` decisions must not be reintroduced without a new decision.
- `Superseded` decisions are historical and must point to a newer decision.

## Cross-Phase Constraints

- Tenant/company scope is mandatory for business data.
- Permission checks are mandatory for APIs, UI routes, search, reports, workers, webhooks, imports/exports, and sync jobs.
- Reporting impact must be defined in every phase.
- Mobile/offline impact must be defined for field workflows.
- Integration impact must include logs, retries, errors, and admin recovery.
- Audit events must be defined for important actions.
- Canonical entity names from the global domain model must be reused exactly.
- Phase 20 consolidates enterprise readiness and scale hardening rather than introducing major new product domains.

## Decisions Future Phases Must Respect

Future phases must respect all `Accepted` decisions in this register, especially PDR-001, PDR-002, DDR-001, DDR-002, DDR-003, DDR-004, SDR-001, SDR-002, SDR-005, ADR-001, ADR-002, DDR-005, DDR-006, DDR-009, DDR-012, ADR-004, ADR-005, ADR-007, ADR-008, UXDR-003, UXDR-006, ADR-009, ADR-010, ADR-011, DDR-016, DDR-017, DDR-019, PDR-005, IDR-001, IDR-002, SDR-006, and PDR-007.

## Decisions That Require Review

The following decisions require review before or during affected phases:

- ODR-005 before production tenant database architecture is finalized.
- ODR-006 before branch, warehouse, depot, territory, or service-area permissions/reporting are implemented.
- ODR-007 before high-volume GPS tracking launch.
- ODR-008 before advanced dispatch or Phase 19.
- ODR-009 before scheduled reporting is promised.
- ODR-010 before policy engine implementation.
- ODR-011 before public API IDs and offline IDs are finalized.
- ODR-012 before CRM-to-order pricing workflows are implemented.
- IDR-006 before QuickBooks invoice sync scope is finalized.
- ODR-013 and ODR-014 before advanced inventory or barcode workflows.

## Open Questions Carried Forward

- What tenant database isolation model will be used at launch and for enterprise customers?
- What is the final organization/location hierarchy across branch, department, depot, warehouse, territory, and service area?
- What is the exact LinkedIn integration scope?
- Is quote/pricing part of MVP?
- Where are invoices created and which system owns invoice truth?
- Does inventory launch require serial/lot tracking?
- Is barcode scanning required for MVP?
- What dispatch optimization level is required?
- Are scheduled emailed reports MVP or later?
- Is Cerbos adopted immediately or later?
- Which ID format will be used for stable application IDs?
- How long are raw GPS pings retained?
