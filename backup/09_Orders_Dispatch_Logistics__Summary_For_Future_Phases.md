# Summary for Future Phases

## Final Decisions Made

- Phase 09 establishes Orders / Dispatch / Logistics as the canonical foundation for orders, order lines, shipments, shipment stops, dispatch plans, route plans, deliveries, pickups, proof of delivery, delivery exceptions, and custody handoff events.
- `Order` is the canonical customer or operational order record. Future phases must not create separate `CustomerOrder`, `DeliveryOrder`, `SalesOrder`, or `JobOrder` entities unless formally approved as provider-specific link entities.
- `OrderLine` is the canonical order line record and must reference `Product` from Phase 08 when a line represents a stockable, sellable, or service item already managed in inventory.
- `Shipment` is the canonical movement record for goods, materials, equipment, work output, or operational commitments across one or more stops.
- `ShipmentStop` is the canonical ordered stop record and must be reused by route, delivery, pickup, proof, exception, fleet, geofence, reporting, and mobile workflows.
- `DispatchPlan` is the canonical dispatcher-controlled planning record for connecting Jobs, Shipments, RoutePlans, drivers, vehicles, crews, depots, and stops.
- `RoutePlan` is the canonical ordered route record. Phase 09 supports manual planning and resequencing; full route optimization is deferred.
- `Delivery` and `Pickup` are completion/attempt records for stops. They must not replace `ShipmentStop` or `Order`.
- `ProofOfDelivery` is the canonical proof artifact wrapper and must reuse `FileAttachment` for photos, files, and signatures where binary content is required.
- `DeliveryException` is the canonical exception record for dispatch, shipment, stop, delivery, pickup, customer unavailable, missing inventory, vehicle issue, weather, blocked site, safety issue, or related logistics disruption.
- `HandoffEvent` is append-only and records custody transfer between warehouse, depot, driver, crew, customer, or another actor/resource.
- Phase 09 must reuse Phase 04 CRM entities for customer context: `Account`, `Contact`, and where useful `Opportunity`.
- Phase 09 must reuse Phase 07 field entities for physical work/location context: `Site`, `Job`, `JobRequest`, `Crew`, `EquipmentAssignment`, `FieldNote`, and `FieldPhoto` where relevant.
- Phase 09 must reuse Phase 08 inventory entities for product, stock, warehouse, depot, picking, packing, transfers, balances, and stock movements.
- Phase 09 must reuse Phase 06 `Task`, `CalendarEvent`, `Appointment`, `Reminder`, and `RecurrenceRule` for scheduled work, dispatch windows, follow-ups, and reminders.
- Phase 09 must reuse Phase 03 shared services for `AuditLog`, `Notification`, `FileAttachment`, `SavedView`, `SearchIndexRecord`, `Tag`, `TagAssignment`, `CustomFieldDefinition`, `CustomFieldValue`, `ImportJob`, `ExportJob`, `SettingsDocument`, `BackgroundJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery`.
- All Phase 09 records are tenant/company scoped and must never expose MongoDB `_id` as the public API identifier.
- Dispatch and logistics status/event models created in Phase 09 must be reused by Fleet Tracking, Service, Reporting, QuickBooks, Offline Mobile, Notifications/Automation, and the final system blueprint.

## Entities Introduced

| Entity | Owner | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `Order` | Orders / Dispatch / Logistics | Company-scoped, optional branch/depot/site | Canonical customer or operational order containing products, services, commitments, fulfillment state, and billing readiness. | Reuse for dispatch, shipments, service billing context, reports, and QuickBooks invoice readiness. |
| `OrderLine` | Orders / Dispatch / Logistics | Child of `Order`, company-scoped | Canonical line item for product, service, fee, or operational deliverable. | Reference `Product` where applicable; do not create module-specific line records. |
| `Shipment` | Orders / Dispatch / Logistics | Company-scoped, optional depot/warehouse/job/order | Movement of goods, equipment, materials, or work output across stops. | Reuse for fleet, delivery dashboards, route replay, exceptions, and reporting. |
| `ShipmentStop` | Orders / Dispatch / Logistics | Child of `Shipment`, company-scoped | Ordered pickup/delivery/service/handoff/depot/warehouse stop. | Reuse for fleet geofences, mobile stop list, proof, exceptions, and reports. |
| `DispatchPlan` | Orders / Dispatch / Logistics | Company-scoped, optional depot/branch | Dispatcher-controlled daily/shift plan connecting work, shipments, routes, drivers, vehicles, and crews. | Fleet and service phases must reference this instead of creating dispatch board-specific plans. |
| `RoutePlan` | Orders / Dispatch / Logistics | Company-scoped, optional vehicle/driver/depot | Ordered route with planned and actual stop sequence. | Fleet phase must connect GPS and route replay to this entity. |
| `Delivery` | Orders / Dispatch / Logistics | Child of `ShipmentStop` and optional `Order` | Delivery attempt or completion record. | Reporting, QuickBooks readiness, and customer proof workflows must reuse it. |
| `Pickup` | Orders / Dispatch / Logistics | Child of `ShipmentStop`; optional `InventoryTransfer` | Pickup attempt or completion record. | Inventory transfer, return, and service pickup workflows must reuse it. |
| `ProofOfDelivery` | Orders / Dispatch / Logistics | Child of `Delivery` or `ShipmentStop` | Captured proof artifact metadata linked to files/signatures/GPS/time. | Mobile, customer proof, disputes, and reporting must reuse it. |
| `DeliveryException` | Orders / Dispatch / Logistics | Company-scoped operational exception | Exception affecting route, stop, shipment, delivery, pickup, inventory, customer, vehicle, weather, blocked site, or safety. | Notifications, reporting, service, and fleet must reuse exception taxonomy. |
| `HandoffEvent` | Orders / Dispatch / Logistics | Company-scoped append-only event | Custody transfer between warehouse, depot, driver, crew, customer, or actor/resource. | Inventory, fleet, service, audit, and dispute workflows must treat it as custody evidence. |

## Fields Introduced

- `Order`: `id`, `tenant_id`, `company_id`, `branch_id`, `account_id`, `contact_id`, `site_id`, `opportunity_id`, `job_id`, `order_number`, `source_type`, `requested_delivery_window_start_at`, `requested_delivery_window_end_at`, `priority`, `status`, `billing_status`, `fulfillment_status`, `currency`, `subtotal_amount`, `tax_amount`, `discount_amount`, `total_amount`, `notes`, `external_refs`, `created_at`, `created_by`, `updated_at`, `updated_by`, `archived_at`, `archived_by`.
- `OrderLine`: `id`, `tenant_id`, `company_id`, `order_id`, `product_id`, `line_type`, `description`, `qty`, `stock_unit_id`, `unit_price`, `discount_amount`, `tax_code`, `line_total`, `status`, `allocated_qty`, `fulfilled_qty`, `warehouse_id`, `depot_id`, `metadata`, audit timestamps.
- `Shipment`: `id`, `tenant_id`, `company_id`, `order_id`, `job_id`, `dispatch_plan_id`, `route_plan_id`, `shipment_number`, `origin_site_id`, `destination_site_id`, `warehouse_id`, `depot_id`, `status`, `planned_start_at`, `planned_end_at`, `actual_start_at`, `actual_end_at`, `assigned_driver_id`, `assigned_user_id`, `vehicle_id`, `crew_id`, `priority`, `exception_count`, `proof_required`, `notes`, audit timestamps.
- `ShipmentStop`: `id`, `tenant_id`, `company_id`, `shipment_id`, `route_plan_id`, `site_id`, `warehouse_id`, `depot_id`, `account_id`, `contact_id`, `stop_sequence`, `stop_type`, `status`, `planned_arrival_at`, `planned_departure_at`, `actual_arrival_at`, `actual_departure_at`, `service_window_start_at`, `service_window_end_at`, `arrival_latitude`, `arrival_longitude`, `completion_latitude`, `completion_longitude`, `instructions`, `proof_required`, `exception_id`, audit timestamps.
- `DispatchPlan`: `id`, `tenant_id`, `company_id`, `branch_id`, `depot_id`, `plan_date`, `plan_name`, `status`, `dispatcher_user_id`, `assigned_team_id`, `shipment_ids`, `route_plan_ids`, `job_ids`, `notes`, `published_at`, `started_at`, `completed_at`, `cancelled_at`, audit timestamps.
- `RoutePlan`: `id`, `tenant_id`, `company_id`, `dispatch_plan_id`, `vehicle_id`, `driver_id`, `assigned_user_id`, `depot_id`, `planned_start_at`, `planned_end_at`, `actual_start_at`, `actual_end_at`, `planned_distance`, `planned_duration_minutes`, `actual_distance`, `actual_duration_minutes`, `status`, `route_sequence_snapshot`, `manual_sequence_reason`, audit timestamps.
- `Delivery`: `id`, `tenant_id`, `company_id`, `shipment_stop_id`, `order_id`, `shipment_id`, `status`, `delivered_at`, `delivered_by_user_id`, `received_by_name`, `received_by_contact_id`, `delivery_notes`, `proof_of_delivery_ids`, `failed_reason`, `exception_id`, audit timestamps.
- `Pickup`: `id`, `tenant_id`, `company_id`, `shipment_stop_id`, `shipment_id`, `inventory_transfer_id`, `status`, `picked_up_at`, `picked_up_by_user_id`, `released_by_name`, `pickup_notes`, `proof_required`, `exception_id`, audit timestamps.
- `ProofOfDelivery`: `id`, `tenant_id`, `company_id`, `delivery_id`, `shipment_stop_id`, `proof_type`, `file_attachment_id`, `signed_by`, `signature_file_attachment_id`, `photo_file_attachment_ids`, `captured_at`, `captured_by_user_id`, `capture_latitude`, `capture_longitude`, `device_id`, `status`, `rejection_reason`, audit timestamps.
- `DeliveryException`: `id`, `tenant_id`, `company_id`, `shipment_id`, `shipment_stop_id`, `delivery_id`, `pickup_id`, `route_plan_id`, `dispatch_plan_id`, `exception_type`, `severity`, `status`, `description`, `occurred_at`, `reported_by_user_id`, `acknowledged_at`, `acknowledged_by_user_id`, `resolved_at`, `resolved_by_user_id`, `resolution_notes`, `notification_ids`, audit timestamps.
- `HandoffEvent`: `id`, `tenant_id`, `company_id`, `shipment_id`, `shipment_stop_id`, `inventory_transfer_id`, `stock_movement_id`, `vehicle_id`, `from_actor_type`, `from_actor_id`, `to_actor_type`, `to_actor_id`, `handoff_type`, `entity_type`, `entity_id`, `occurred_at`, `recorded_by_user_id`, `latitude`, `longitude`, `file_attachment_ids`, `notes`, `status`.

## APIs Introduced

- `/api/v1/orders` for order list, create, detail, update, confirm, cancel, archive, restore, and export actions.
- `/api/v1/orders/{order_id}/lines` for order line create, update, allocation status, fulfillment status, cancellation, and validation.
- `/api/v1/shipments` for shipment planning, assignment, dispatch linkage, status transitions, and detail views.
- `/api/v1/shipments/{shipment_id}/stops` for ordered stop management, resequencing, arrival, departure, completion, skip, and exception actions.
- `/api/v1/dispatch-plans` for daily/shift dispatch plan creation, publication, assignment, monitoring, completion, exception, and cancellation.
- `/api/v1/route-plans` for route creation, manual resequencing, assignment, start, progress, completion, and cancellation.
- `/api/v1/deliveries` for delivery attempt/completion records and proof linkage.
- `/api/v1/pickups` for pickup attempt/completion records and inventory transfer linkage.
- `/api/v1/proofs-of-delivery` for proof capture, file/signature/photo linkage, acceptance, rejection, and archive.
- `/api/v1/delivery-exceptions` for exception creation, acknowledgement, resolution, cancellation, and notification linkage.
- `/api/v1/handoff-events` for append-only custody handoff recording and retrieval.
- `/api/v1/dispatch-board` for permission-aware operational board data grouped by unassigned, assigned, in progress, delayed, completed, exception, and cancelled.
- `/api/v1/mobile/assigned-stops` for mobile driver/field user stop lists with offline-safe sync metadata.
- All APIs must enforce tenant/company/module/permission checks and must use stable application IDs, never MongoDB `_id`.

## Permissions Introduced

- `orders.order.view`, `orders.order.create`, `orders.order.update`, `orders.order.confirm`, `orders.order.cancel`, `orders.order.archive`, `orders.order.export`.
- `orders.order_line.manage`, `orders.order_line.allocate`, `orders.order_line.fulfill`, `orders.order_line.cancel`.
- `orders.shipment.view`, `orders.shipment.create`, `orders.shipment.update`, `orders.shipment.assign`, `orders.shipment.start`, `orders.shipment.complete`, `orders.shipment.cancel`, `orders.shipment.export`.
- `orders.shipment_stop.view`, `orders.shipment_stop.manage`, `orders.shipment_stop.resequence`, `orders.shipment_stop.arrive`, `orders.shipment_stop.complete`, `orders.shipment_stop.skip`.
- `orders.dispatch_plan.view`, `orders.dispatch_plan.create`, `orders.dispatch_plan.update`, `orders.dispatch_plan.publish`, `orders.dispatch_plan.assign`, `orders.dispatch_plan.cancel`.
- `orders.route_plan.view`, `orders.route_plan.create`, `orders.route_plan.update`, `orders.route_plan.resequence`, `orders.route_plan.start`, `orders.route_plan.complete`.
- `orders.delivery.view`, `orders.delivery.complete`, `orders.delivery.fail`, `orders.delivery.override`.
- `orders.pickup.view`, `orders.pickup.complete`, `orders.pickup.fail`, `orders.pickup.override`.
- `orders.proof.view`, `orders.proof.capture`, `orders.proof.accept`, `orders.proof.reject`, `orders.proof.archive`.
- `orders.exception.view`, `orders.exception.create`, `orders.exception.acknowledge`, `orders.exception.resolve`, `orders.exception.cancel`.
- `orders.handoff.view`, `orders.handoff.record`.
- `orders.dispatch_board.view`, `orders.dispatch_board.manage`, `orders.mobile.execute_assigned`.

## UX Patterns Introduced

- Dispatch Board with grouped operational lanes: unassigned, assigned, in progress, delayed, completed, exception, cancelled.
- Dispatch Calendar/Day View for plan date, route load, driver/vehicle assignment, and stop windows.
- Route Builder with ordered stop list, drag/drop manual resequencing where permission allows, sequence validation, and warning states.
- Driver Mobile Stop List showing assigned stops, planned windows, customer/site instructions, status, offline state, and next action.
- Stop Execution Screen with arrive, depart, complete delivery, complete pickup, capture proof, report exception, and notes actions.
- Proof Capture flow for signature, photo, received-by name, GPS/time capture, and offline queue state.
- Exception Drawer for delay, customer unavailable, inventory missing, vehicle issue, weather, site blocked, safety issue, and other documented exception types.
- Handoff Capture flow for warehouse/depot/driver/crew/customer custody transfer with actor/resource references and optional photo/signature.
- Order Detail view with lines, fulfillment state, shipments, related job/site/account, billing state, timeline, files, exceptions, and audit summary.
- Shipment Detail view with stops, route, assigned resources, proof, exceptions, handoffs, timeline, and related inventory movement context.

## Reports or Dashboards Introduced

- Dispatch Board Metrics: unassigned, assigned, in progress, delayed, completed, exception, and cancelled work counts.
- Delivery Performance Dashboard: on-time delivery rate, attempted deliveries, successful deliveries, failed deliveries, average stop duration, and proof completion rate.
- Exception Dashboard: exception volume by type, severity, route, driver, dispatcher, depot, account, and resolution time.
- Route Plan Report: planned vs actual duration, planned vs actual stop count, manual resequences, cancelled routes, and completion status.
- Order Fulfillment Report: order status, line allocation, fulfilled quantity, partial fulfillment, and billing readiness.
- Handoff Chain Report: custody events by shipment/order/inventory transfer and missing handoff warnings.
- Mobile Execution Report: offline actions queued, failed syncs, proof capture success, and stop completion timestamps.

## Notifications Introduced

- Dispatch plan published or changed.
- Shipment assigned to driver/user/crew.
- Route plan assigned, started, delayed, completed, or cancelled.
- Stop assigned, upcoming, late, arrived, completed, skipped, or exception.
- Proof of delivery captured, rejected, or missing.
- Delivery exception created, acknowledged, escalated, resolved, or cancelled.
- Warehouse/depot/driver handoff recorded or missing.
- Order confirmed, partially fulfilled, fulfilled, cancelled, or billing-ready.

## Audit Events Introduced

- `order.created`, `order.updated`, `order.confirmed`, `order.cancelled`, `order.archived`, `order.restored`.
- `order_line.created`, `order_line.updated`, `order_line.allocated`, `order_line.fulfilled`, `order_line.cancelled`.
- `shipment.created`, `shipment.updated`, `shipment.assigned`, `shipment.started`, `shipment.completed`, `shipment.exception`, `shipment.cancelled`.
- `shipment_stop.created`, `shipment_stop.updated`, `shipment_stop.resequenced`, `shipment_stop.arrived`, `shipment_stop.departed`, `shipment_stop.completed`, `shipment_stop.skipped`, `shipment_stop.exception`.
- `dispatch_plan.created`, `dispatch_plan.updated`, `dispatch_plan.published`, `dispatch_plan.assigned`, `dispatch_plan.started`, `dispatch_plan.completed`, `dispatch_plan.cancelled`.
- `route_plan.created`, `route_plan.updated`, `route_plan.resequenced`, `route_plan.assigned`, `route_plan.started`, `route_plan.completed`, `route_plan.cancelled`.
- `delivery.completed`, `delivery.failed`, `pickup.completed`, `pickup.failed`.
- `proof_of_delivery.captured`, `proof_of_delivery.accepted`, `proof_of_delivery.rejected`, `proof_of_delivery.archived`.
- `delivery_exception.created`, `delivery_exception.acknowledged`, `delivery_exception.resolved`, `delivery_exception.cancelled`.
- `handoff_event.recorded`.

## Integrations Introduced

- QuickBooks invoice readiness must be supported through `Order.billing_status`, `Order.fulfillment_status`, `Delivery.status`, and proof/completion timestamps, but Phase 09 does not implement full QuickBooks sync.
- Inventory integration must connect order lines, shipments, pickups, handoffs, PickTickets, PackRecords, InventoryTransfers, StockMovements, InventoryBalances, Warehouses, and Depots.
- Fleet integration must later connect RoutePlans and ShipmentStops to Vehicles, Drivers, LocationPings, GeofenceEvents, RouteReplay, and live map state.
- Notification integrations must reuse the canonical Notification service and user preferences.
- Webhook integrations should emit order, shipment, stop, proof, exception, and handoff events through existing webhook foundations.
- Import/export must use `ImportJob` and `ExportJob` for orders, shipments, routes, and exception reports.

## Dependencies Created

- Depends on Phase 02 tenant/company/user/membership/role/permission foundations.
- Depends on Phase 03 shared audit, notification, files, saved views, search, imports, exports, settings, background jobs, API key, and webhook foundations.
- Depends on Phase 04 CRM Account, Contact, Opportunity, Activity, Note, Comment, and AssignmentRule where customer context or timeline context is needed.
- Depends on Phase 06 Task, CalendarEvent, Appointment, Reminder, and RecurrenceRule for scheduling and follow-up behavior.
- Depends on Phase 07 Site, Job, JobRequest, Crew, EquipmentAssignment, FieldNote, FieldPhoto, CheckInEvent, and CheckOutEvent for site and operational work context.
- Depends on Phase 08 Product, StockUnit, InventoryItem, InventoryBalance, StockMovement, Warehouse, Depot, BinLocation, ReceivingRecord, PickTicket, PackRecord, InventoryTransfer, and LowStockAlert.
- Creates required inputs for Phase 10 Fleet / GPS / Geofencing, Phase 11 Service / Work Orders, Phase 12 Reporting / Analytics, Phase 13 QuickBooks / Integrations, Phase 14 Mobile / Offline, Phase 16 Notifications / Automation, and Phase 20 final blueprint.

## Constraints Future Phases Must Respect

- Future phases must reuse Phase 09 statuses for dispatch, shipment, route, stop, delivery, pickup, proof, exception, and handoff workflows unless an explicit superseding decision is approved.
- Fleet tracking must attach GPS, geofence, route replay, and live map behavior to `RoutePlan` and `ShipmentStop`; it must not create a duplicate route/stop model.
- Service workflows must reference `Order`, `Shipment`, `ShipmentStop`, `Delivery`, `Pickup`, `ProofOfDelivery`, and `DeliveryException` where service work includes delivery, pickup, proof, or customer-site logistics.
- Reporting must derive logistics KPIs from explicit status fields, timestamps, exception records, proof records, and handoff events rather than free-text notes.
- QuickBooks sync must treat Phase 09 records as operational source context but must not make QuickBooks the source of truth for dispatch/order state.
- Offline mobile must support queued arrival, departure, completion, proof, exception, and handoff actions with revalidation on sync.
- Notifications and automation must use Phase 09 event triggers without creating duplicate event names.
- HandoffEvent must remain append-only; corrections must be recorded as additional events, not destructive edits.
- DeliveryException must remain the canonical exception model for logistics; future modules may add fields or taxonomy values through controlled decisions but must not duplicate it.
- Advanced route optimization, AI dispatch planning, native ELD compliance, customer portal delivery tracking, and advanced telemetry remain future scope unless explicitly reprioritized.

## Open Questions Carried Forward

- Confirm whether `Driver` is introduced in Phase 10 only or may be referenced in Phase 09 as a future entity while using `assigned_user_id` for MVP execution.
- Confirm the final location hierarchy for branch, depot, warehouse, territory, and service area scoping.
- Confirm whether order numbering is company-wide, branch-specific, depot-specific, or configurable by company settings.
- Confirm the exact billing readiness rules that QuickBooks will consume in the integration phase.
- Confirm whether partial delivery of individual order lines should be represented only through `OrderLine.fulfilled_qty` or through a separate fulfillment allocation record in a later phase.
- Confirm whether customer-facing proof links or customer notification tracking belong in Phase 09 or a later customer portal/notification phase.
- Confirm the retention policy for proof files, signatures, photos, GPS coordinates, and handoff evidence.
- Confirm whether route distance/duration estimates come from manual entry, internal calculation, or a map provider in MVP.
- Confirm whether dispatch board real-time updates require WebSocket/SSE in MVP or can begin with polling.
- Confirm whether exceptions require SLA/escalation policies in Phase 09 or should only emit notifications and tasks until automation is expanded.
