# Summary for Future Phases

## Final Decisions Made

- Phase 11 establishes Service / Work Orders as the canonical foundation for service intake, service execution, work order tasks, recurring maintenance schedules, service history, labor entries, and service parts usage.
- `ServiceRequest` is the canonical intake record for customer, internal, asset, dispatch, or integration-originated service needs. Future phases must not introduce `ServiceTicket` as a duplicate intake entity.
- `WorkOrder` is the canonical service execution record. It must not replace generic `Job`, and `Job` must not replace service execution workflows. Link `WorkOrder` and `Job` only when operational context requires it.
- `WorkOrderTask` is the canonical checklist/action item inside a WorkOrder. General follow-ups, callbacks, and unrelated reminders must use canonical `Task`.
- `MaintenanceSchedule` is the canonical recurring service plan for vehicles, drilling equipment, and approved future assets. It must reuse canonical `RecurrenceRule` for time-based recurrence.
- `ServiceHistory` is the read-optimized historical record created from completed WorkOrders for Account, Site, Vehicle, DrillingEquipment, and future approved serviceable entities.
- `LaborEntry` is the canonical labor/time record on a WorkOrder. Payroll is out of scope; approved labor may later support billing and reporting.
- `PartsUsage` is the canonical parts consumption/reservation/return record on a WorkOrder and must reference canonical `Product`; stock-changing actions must create or reference `StockMovement`.
- Service must reuse Phase 03 shared services: `AuditLog`, `Notification`, `FileAttachment`, `SavedView`, `SearchIndexRecord`, `ImportJob`, `ExportJob`, `Tag`, `TagAssignment`, `CustomFieldDefinition`, `CustomFieldValue`, `SettingsDocument`, `BackgroundJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery`.
- Service must reuse Phase 04 CRM entities: `Account`, `Contact`, `Opportunity`, and `Activity` for customer context and timelines.
- Service must reuse Phase 06 `Task`, `CalendarEvent`, `Appointment`, `Reminder`, and `RecurrenceRule` for scheduling, reminders, follow-ups, and maintenance recurrence.
- Service must reuse Phase 07 `Site`, `Job`, `Crew`, `EquipmentAssignment`, `FieldNote`, and `FieldPhoto` where service overlaps field work, but WorkOrder remains service execution.
- Service must reuse Phase 08 `Product`, `InventoryItem`, `InventoryBalance`, `StockMovement`, `Warehouse`, `Depot`, `BinLocation`, `PickTicket`, and `InventoryTransfer` for service parts.
- Service must reuse Phase 09 `Order`, `DispatchPlan`, `RoutePlan`, `ShipmentStop`, `DeliveryException`, and `HandoffEvent` when service is triggered by logistics context.
- Service must reuse Phase 10 `Vehicle`, `Driver`, `TrackingDevice`, geofence/location context, and device health events for asset maintenance context where applicable.
- All Phase 11 records are tenant/company scoped and must never expose MongoDB `_id` as a public API identifier.
- Mobile/offline technician execution is required for assigned work order viewing, task completion, note/photo capture, labor capture, staged parts usage, and completion attempts, with server revalidation on sync.
- Reporting, QuickBooks, offline sync, notifications/automation, and final blueprint phases must respect WorkOrder status, PartsUsage + StockMovement rules, LaborEntry approval rules, and ServiceHistory creation rules.

## Entities Introduced

| Entity | Owner | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `ServiceRequest` | Service / Work Orders | Company-scoped | Canonical intake record for a customer, internal, asset, dispatch, or integration-reported service need before execution is approved or converted into a WorkOrder. | Reporting, automation, customer portals, SLA dashboards, and integration intake must use ServiceRequest instead of creating service ticket intake duplicates. |
| `WorkOrder` | Service / Work Orders | Company-scoped | Canonical service execution record assigned to technicians and used to manage service tasks, labor, parts, completion proof, service history, and billing readiness. | QuickBooks, reporting, offline mobile, customer notifications, and automation must treat WorkOrder as service execution, not as generic Task or Job replacement. |
| `WorkOrderTask` | Service / Work Orders | Company-scoped | Checklist, inspection step, required action, safety step, or technician task inside a WorkOrder. | Future inspection templates and automation may generate WorkOrderTask rows, but general follow-up work must use canonical Task. |
| `MaintenanceSchedule` | Service / Work Orders | Company-scoped | Recurring preventive maintenance or scheduled service plan for Vehicle, DrillingEquipment, or approved asset types. | Automation, fleet health, drilling equipment maintenance, reporting, and offline technician queues must reuse this schedule model. |
| `ServiceHistory` | Service / Work Orders | Company-scoped | Immutable or append-only service completion history derived from completed WorkOrders and used to show historical service by account, site, vehicle, equipment, or other serviceable entity. | Reporting and customer/asset history must use ServiceHistory as the read-optimized history record while WorkOrder remains the execution source. |
| `LaborEntry` | Service / Work Orders | Company-scoped | Technician or worker time entry against a WorkOrder for operational cost, productivity, billing readiness, and reporting. | Payroll is out of scope; QuickBooks and reporting may consume approved LaborEntry summaries where billing integration is later approved. |
| `PartsUsage` | Service / Work Orders with Inventory / Warehouse stock ownership | Company-scoped | Planned, reserved, consumed, returned, or cancelled part usage on a WorkOrder, linked to canonical Product and inventory StockMovement. | QuickBooks item mapping, service margin reports, inventory availability, and offline mobile parts capture must reuse PartsUsage and StockMovement rules. |

## Fields Introduced

- `ServiceRequest`: `id`, `tenant_id`, `company_id`, `account_id`, `site_id`, `requester_contact_id`, `requester_user_id`, `source`, `source_record_type`, `source_record_id`, `issue_title`, `issue_description`, `priority`, `severity`, `status`, `requested_at`, `needed_by_at`, `triaged_at`, `approved_at`, `rejected_at`, `converted_work_order_id`, `assigned_team_id`, `assigned_user_id`, `sla_due_at`, `external_refs`, metadata fields.
- `WorkOrder`: `id`, `tenant_id`, `company_id`, `work_order_number`, `service_request_id`, `maintenance_schedule_id`, `account_id`, `contact_ids`, `site_id`, `job_id`, `order_id`, `dispatch_plan_id`, `route_plan_id`, `shipment_stop_id`, `asset_type`, `asset_id`, `assigned_user_id`, `assigned_team_id`, `crew_id`, `vehicle_id`, `depot_id`, `status`, `priority`, `service_type`, `problem_summary`, `instructions`, schedule timestamps, execution timestamps, proof attachment IDs, `billable_status`, totals, metadata fields.
- `WorkOrderTask`: `id`, `tenant_id`, `company_id`, `work_order_id`, `title`, `description`, `task_type`, `sort_order`, `required`, `assigned_user_id`, `status`, completion/skipped metadata, input/proof requirement fields.
- `MaintenanceSchedule`: `id`, `tenant_id`, `company_id`, `asset_type`, `asset_id`, `name`, `service_type`, `recurrence_rule_id`, meter and due fields, defaults, `status`, pause/archive metadata.
- `ServiceHistory`: `id`, `tenant_id`, `company_id`, `work_order_id`, `service_entity_type`, `service_entity_id`, `account_id`, `site_id`, `asset_type`, `asset_id`, `service_type`, `completed_at`, `completed_by_user_id`, `summary`, `resolution_summary`, labor/parts rollups, `billable_status`.
- `LaborEntry`: `id`, `tenant_id`, `company_id`, `work_order_id`, `user_id`, `team_id`, `labor_type`, `started_at`, `ended_at`, `hours_qty`, `break_minutes_qty`, rate/billable fields, `status`, submit/approve/reject metadata, notes.
- `PartsUsage`: `id`, `tenant_id`, `company_id`, `work_order_id`, `product_id`, `inventory_item_id`, `stock_unit_id`, requested/reserved/used/returned/scrapped quantities, source location fields, `stock_movement_ids`, `status`, cost/bill fields, usage/return metadata.

## APIs Introduced

- `/api/v1/service-requests` for intake list, create, detail, update, triage, approve, reject, archive, and conversion actions.
- `/api/v1/service-requests/{service_request_id}/convert-to-work-order`.
- `/api/v1/work-orders` for list, create, detail, update, schedule, assign, lifecycle transitions, complete, cancel, archive, and export preparation.
- `/api/v1/work-orders/{work_order_id}/status-transitions`.
- `/api/v1/work-orders/{work_order_id}/complete`.
- `/api/v1/work-order-tasks` and WorkOrder-scoped task batch endpoints for checklist creation, reorder, completion, and skipped handling.
- `/api/v1/labor-entries` for create, timer capture, submit, approve, reject, and void.
- `/api/v1/parts-usage` for plan, reserve, use, return, cancel, and StockMovement linkage.
- `/api/v1/maintenance-schedules` for schedule management, next-due preview, pause/resume, archive, and work order generation.
- `/api/v1/service-history` for permission-filtered service history read models.
- Mobile sync endpoints for batched offline WorkOrder, task, labor, parts, notes, files, and completion actions with conflict reporting.

## Permissions Introduced

- `service.service_request.view`, `service.service_request.create`, `service.service_request.update`, `service.service_request.triage`, `service.service_request.approve`, `service.service_request.reject`, `service.service_request.convert`, `service.service_request.archive`, `service.service_request.export`.
- `service.work_order.view`, `service.work_order.create`, `service.work_order.update`, `service.work_order.schedule`, `service.work_order.assign`, `service.work_order.start`, `service.work_order.block`, `service.work_order.complete`, `service.work_order.cancel`, `service.work_order.archive`, `service.work_order.export`.
- `service.work_order_task.manage`, `service.work_order_task.complete`.
- `service.labor_entry.view`, `service.labor_entry.create`, `service.labor_entry.update_own`, `service.labor_entry.submit`, `service.labor_entry.approve`, `service.labor_entry.reject`, `service.labor_entry.void`, `service.labor_entry.view_cost`, `service.labor_entry.export`.
- `service.parts_usage.view`, `service.parts_usage.plan`, `service.parts_usage.reserve`, `service.parts_usage.use`, `service.parts_usage.return`, `service.parts_usage.cancel`, `service.parts_usage.view_cost`, `service.parts_usage.edit_billable_amount`.
- `service.maintenance_schedule.view`, `service.maintenance_schedule.create`, `service.maintenance_schedule.update`, `service.maintenance_schedule.pause`, `service.maintenance_schedule.resume`, `service.maintenance_schedule.generate_work_order`, `service.maintenance_schedule.archive`.
- `service.service_history.view`, `service.service_history.export`.
- Service inventory actions also require corresponding inventory permissions; service cost/billing fields require cost/billing permissions.

## UX Patterns Introduced

- Service Requests list and detail with triage, source context, conversion action, files, notes, and timeline.
- Work Orders board and table views with status grouping, saved views, bulk assignment, and operational filters.
- WorkOrder detail page with header, status actions, assignment/schedule panels, checklist, labor, parts, files/proof, timeline, and audit summary.
- Technician mobile queue and mobile execution screen with offline banner, task completion, notes/photos, labor capture, parts capture, signature capture, and completion validation.
- Maintenance Schedule list/detail with asset context, recurrence, next due, last service, pause/resume, and generated work orders.
- Service History tabs on Account, Site, Vehicle, and approved asset detail pages.
- Empty/error states for no records, no permission, module disabled, filters too narrow, inventory unavailable, required task incomplete, stale sync version, missing proof, and invalid status transitions.

## Reports or Dashboards Introduced

- Service backlog, overdue work, blocked work, unassigned work, scheduled work, and in-progress work.
- WorkOrder completion volume, cycle time, scheduled-versus-actual variance, SLA performance, and service type trends.
- Technician productivity, labor hours, labor approval status, and team workload.
- Parts usage by product, location, account, site, WorkOrder, technician, and billable status.
- Maintenance compliance by asset, schedule, due date, overdue count, and completed preventive work.
- Billing readiness report for completed WorkOrders with labor approved, parts finalized, proof collected, and billing hold status.
- Service history reports by Account, Site, Vehicle, DrillingEquipment, and future serviceable entities.

## Notifications Introduced

- High-priority ServiceRequest created.
- WorkOrder assigned or schedule changed.
- WorkOrder blocked or blocked beyond threshold.
- Reminder before scheduled service start.
- Parts cannot be reserved or inventory shortage.
- LaborEntry submitted for approval.
- WorkOrder completed.
- MaintenanceSchedule due soon or overdue.
- WorkOrder ready for billing when billing workflow is enabled.

## Audit Events Introduced

- ServiceRequest created, updated, triaged, approved, rejected, converted, archived.
- WorkOrder created, scheduled, assigned, started, status changed, blocked, unblocked, completed, cancelled, archived, reopened where allowed.
- WorkOrderTask created, updated, reordered, completed, skipped, override approved.
- LaborEntry created, timer started/stopped, submitted, approved, rejected, voided, cost/bill rate changed.
- PartsUsage planned, reserved, used, returned, cancelled, cost/bill amount changed, StockMovement linked.
- MaintenanceSchedule created, updated, paused, resumed, expired, archived, generated WorkOrder, recurrence changed.
- ServiceHistory created.
- Service file/proof uploaded, deleted, replaced, or signature captured.
- Service export, bulk update, bulk assignment, and override actions.

## Integrations Introduced

- QuickBooks readiness foundation for WorkOrder, approved LaborEntry, and finalized PartsUsage; actual QuickBooks sync remains a later integration phase.
- Inventory integration through Product, InventoryItem, InventoryBalance, StockMovement, Warehouse, Depot, BinLocation, PickTicket, and InventoryTransfer.
- Fleet integration through Vehicle, Driver, location context, device health, and maintenance schedules.
- Dispatch integration through DispatchPlan, RoutePlan, ShipmentStop, DeliveryException, and HandoffEvent when service work originates from logistics.
- Calendar integration through CalendarEvent, Appointment, Reminder, and RecurrenceRule.
- Webhook-ready events for service request, work order, parts, labor, and maintenance state changes.

## Dependencies Created

- Depends on Phase 02 tenant/company/user/membership/role/permission/module access rules.
- Depends on Phase 03 shared AuditLog, Notification, FileAttachment, SavedView, SearchIndexRecord, ImportJob, ExportJob, BackgroundJob, settings, tags, custom fields, APIs, and webhooks.
- Depends on Phase 04 Account, Contact, Opportunity, Activity, and customer timeline foundations.
- Depends on Phase 06 Task, CalendarEvent, Appointment, Reminder, and RecurrenceRule.
- Depends on Phase 07 Site, Job, Crew, EquipmentAssignment, FieldNote, and FieldPhoto.
- Depends on Phase 08 Product, InventoryItem, StockUnit, StockMovement, Warehouse, Depot, BinLocation, PickTicket, and InventoryTransfer.
- Depends on Phase 09 Order, DispatchPlan, RoutePlan, ShipmentStop, DeliveryException, and HandoffEvent where service is logistics-triggered.
- Depends on Phase 10 Vehicle, Driver, device/location context, and maintenance-related fleet concepts.

## Constraints Future Phases Must Respect

- Do not create `ServiceTicket`, `RepairTicket`, `ServiceTask`, `PartLine`, `TechnicianTime`, or `AssetServiceLog` as duplicate entities when Phase 11 entities cover the meaning.
- WorkOrder is service execution only; Job remains generic operational field work; Task remains general actionable follow-up work.
- PartsUsage must reference Product and create/reference StockMovement for quantity-changing actions.
- LaborEntry approval status must be respected by reporting, billing readiness, QuickBooks, and analytics.
- ServiceHistory is created from completed WorkOrders and is the service history read model for account/site/asset timelines.
- Offline service actions must be revalidated on sync, especially completion, labor, inventory, billing, and permission-sensitive operations.
- QuickBooks must not invoice draft, cancelled, blocked, or incomplete WorkOrders, unapproved LaborEntry rows, or unfinalized PartsUsage rows.
- Notifications and automation must use canonical Notification and Reminder foundations and must respect permission and preference rules.
- Reports must not derive inventory usage from WorkOrder notes; they must use PartsUsage and StockMovement.
- Cost, margin, billing, export, and audit data must remain permission-controlled.

## Open Questions Carried Forward

- Confirm whether WorkOrder should support customer-visible status labels separate from internal statuses.
- Confirm whether WorkOrder completion requires customer signature by default or only by service type/company setting.
- Confirm whether maintenance recurrence should support meter/odometer/hour-based automation in MVP or remain field-ready only.
- Confirm how service billable status maps to QuickBooks invoice candidates in the integration phase.
- Confirm whether WorkOrderTask templates and inspection templates are Phase 11 scope or should be deferred to automation/configuration phases.
- Confirm whether external customer portal service requests are in a later phase or remain API-ready only.
- Confirm whether ServiceHistory corrections should use a correction event model or restricted admin edit workflow.
