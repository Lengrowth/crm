# Summary for Future Phases

## Final Decisions Made

- Phase 08 establishes Inventory / Warehouse / Depots as the canonical product, stock, warehouse, depot, bin, movement, receiving, picking, packing, adjustment, transfer, and low-stock foundation.
- `Product` is the canonical item record for inventory, orders, dispatch, service parts usage, reporting, and QuickBooks item sync readiness.
- `ProductCategory` is the canonical product grouping hierarchy.
- `StockUnit` is the canonical unit/conversion record for inventory quantities.
- `InventoryItem` is the canonical physical or trackable stock instance where lot, serial, condition, or item-level custody tracking is needed.
- `InventoryBalance` is the current-state materialized quantity rollup by product/location/bin/lot/serial/condition.
- `StockMovement` is the append-only source-of-truth event for inventory history and quantity-changing actions.
- `Warehouse` and `Depot` are canonical inventory locations. Depot is also future-compatible with fleet and dispatch, but it must not replace Vehicle.
- `BinLocation` is the canonical storage position under a Warehouse or Depot and must support future barcode scanning.
- `ReceivingRecord`, `PickTicket`, `PackRecord`, `InventoryAdjustment`, `InventoryTransfer`, and `LowStockAlert` are canonical Phase 08 workflow entities.
- Inventory must reuse Phase 03 Core Platform services for AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, SettingsDocument, BackgroundJob, ApiKey, WebhookEndpoint, and WebhookDelivery.
- Inventory must reuse Phase 04 `Account` for suppliers/vendors/customers where appropriate instead of creating a Supplier entity.
- Inventory must reuse Phase 06 `Task`, `Reminder`, and `Notification` foundations for follow-ups and alerts where needed.
- Inventory must reuse Phase 07 `Job` as a possible PickTicket source, but Job must not own inventory master data or inventory balances.
- All inventory records are tenant/company scoped and must never expose MongoDB `_id` as a public API identifier.
- Every stock-changing action must be auditable and must produce or reference StockMovement.
- Orders, dispatch, service, QuickBooks item sync, reporting, mobile scanning, and warehouse/depot permissions must reuse the Phase 08 inventory model.

## Entities Introduced

| Entity | Owner | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `Product` | Inventory / Warehouse | Company-scoped | Canonical sellable/stockable/usable item. | Reuse for orders, shipments, service parts, QuickBooks items, and reports. |
| `ProductCategory` | Inventory / Warehouse | Company-scoped | Product grouping and hierarchy. | Reuse for product filtering, reporting, imports, and catalog organization. |
| `StockUnit` | Inventory / Warehouse | Company-scoped | Unit and conversion definition. | Reuse for receiving, picking, transfer, movement, and reporting quantities. |
| `InventoryItem` | Inventory / Warehouse | Company-scoped/location-scoped | Trackable physical/batch/serial/condition stock instance. | Reuse for lot/serial/mobile scanning/custody tracking. |
| `InventoryBalance` | Inventory / Warehouse | Company-scoped/location-scoped | Current stock rollup. | Reuse for availability queries and dashboards; do not use as history source. |
| `Warehouse` | Inventory / Warehouse | Company-scoped, optional branch | Storage facility for receiving, bins, picking, packing, and transfers. | Reuse for dispatch, reports, integrations, and location permissions. |
| `Depot` | Inventory / Warehouse | Company-scoped, optional branch | Operational depot/base for inventory and future fleet/dispatch. | Reuse for fleet bases and route/depot context; do not replace Vehicle. |
| `BinLocation` | Inventory / Warehouse | Warehouse/depot child | Specific storage position. | Reuse for barcode scanning and directed warehouse workflows. |
| `ReceivingRecord` | Inventory / Warehouse | Company-scoped/location-scoped | Inbound stock receipt workflow. | Posting creates StockMovement; future purchasing may link to it. |
| `PickTicket` | Inventory / Warehouse | Company-scoped/location-scoped | Picking request for Job and future Order/Shipment/WorkOrder contexts. | Reuse for dispatch/order/service picking. |
| `PackRecord` | Inventory / Warehouse | Company-scoped | Packing confirmation after picking. | Reuse for future Shipment and proof/handoff workflows. |
| `StockMovement` | Inventory / Warehouse | Company-scoped/location-scoped append-only event | Inventory movement/correction history. | All future inventory-changing workflows must post StockMovement. |
| `InventoryAdjustment` | Inventory / Warehouse | Company-scoped/location-scoped | Controlled quantity correction. | Reuse for correction workflows, approvals, reporting, and audit. |
| `InventoryTransfer` | Inventory / Warehouse | Company-scoped/location-scoped | Stock transfer between locations with in-transit state. | Reuse for depot replenishment, dispatch loadouts, and future vehicle/job movement. |
| `LowStockAlert` | Inventory / Warehouse | Company-scoped/location-scoped | Threshold alert for replenishment. | Reuse in reporting, notifications, tasks, and replenishment planning. |

## Fields Introduced

- Common fields for Phase 08 entities: `id`, `tenant_id`, `company_id`, optional `branch_id`, `status`, `source`, `metadata`, `external_refs`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` where archiving applies.
- Product fields: `sku`, `name`, `description`, `product_category_id`, `default_stock_unit_id`, `unit_of_measure`, `item_type`, `track_inventory`, `track_lot`, `track_serial`, `reorder_enabled`, `reorder_min_qty`, `reorder_target_qty`, `accounting_code`, `external_refs.quickbooks`.
- ProductCategory fields: `parent_product_category_id`, `name`, `code`, `description`, `sort_order`, `status`.
- StockUnit fields: `product_id`, `unit_code`, `unit_name`, `base_unit_code`, `conversion_factor_to_base`, `decimal_precision`, `is_default_purchase_unit`, `is_default_sales_unit`, `is_default_stock_unit`.
- InventoryItem fields: `product_id`, `inventory_balance_id`, `lot_number`, `serial_number`, `condition`, `location_type`, `location_id`, `bin_location_id`, `received_record_id`, `source_stock_movement_id`.
- InventoryBalance fields: `product_id`, `location_type`, `location_id`, `warehouse_id`, `depot_id`, `bin_location_id`, `lot_number`, `serial_number`, `condition`, `on_hand_qty`, `reserved_qty`, `committed_qty`, `available_qty`, `damaged_qty`, `in_transit_qty`, `last_movement_at`, `version`.
- Warehouse fields: `branch_id`, `name`, `code`, `warehouse_type`, `address`, `timezone`, `manager_user_id`, `receiving_enabled`, `picking_enabled`, `packing_enabled`, `bin_tracking_enabled`.
- Depot fields: `branch_id`, `name`, `code`, `depot_type`, `address`, `timezone`, `manager_user_id`, `supports_inventory`, `supports_fleet`, `bin_tracking_enabled`.
- BinLocation fields: `location_type`, `location_id`, `warehouse_id`, `depot_id`, `zone`, `aisle`, `rack`, `shelf`, `bin_code`, `barcode_value`, `capacity_qty`, `capacity_unit_id`.
- ReceivingRecord fields: `receiving_number`, `source_type`, `source_reference`, `supplier_account_id`, `destination_location_type`, `destination_location_id`, `received_by_user_id`, `received_at`, `expected_at`, `lines[]`, `attachments`, `notes`.
- PickTicket fields: `pick_ticket_number`, `source_entity_type`, `source_entity_id`, `warehouse_id`, `depot_id`, `assigned_user_id`, `priority`, `requested_by_user_id`, `due_at`, `lines[]`, `short_reason`.
- PackRecord fields: `pack_record_number`, `pick_ticket_id`, `packed_by_user_id`, `packed_at`, `package_count`, `package_labels[]`, `weight`, `dimensions`, `staging_location`.
- StockMovement fields: `product_id`, `inventory_item_id`, `movement_type`, `qty`, `stock_unit_id`, `base_qty`, `source_location_type`, `source_location_id`, `source_bin_location_id`, `destination_location_type`, `destination_location_id`, `destination_bin_location_id`, `lot_number`, `serial_number`, `condition`, `related_entity_type`, `related_entity_id`, `occurred_at`, `recorded_by_user_id`, `reversal_of_stock_movement_id`.
- InventoryAdjustment fields: `adjustment_number`, `product_id`, `location_type`, `location_id`, `bin_location_id`, `current_qty_snapshot`, `adjustment_qty`, `reason_code`, `reason_notes`, `requested_by_user_id`, `approved_by_user_id`, `approved_at`, `posted_at`, `stock_movement_ids`.
- InventoryTransfer fields: `transfer_number`, `source_location_type`, `source_location_id`, `destination_location_type`, `destination_location_id`, `requested_by_user_id`, `released_by_user_id`, `shipped_by_user_id`, `received_by_user_id`, `shipped_at`, `received_at`, `lines[]`, `discrepancy_notes`, `stock_movement_ids`.
- LowStockAlert fields: `product_id`, `location_type`, `location_id`, `bin_location_id`, `threshold_qty`, `current_available_qty`, `target_qty`, `severity`, `triggered_at`, `acknowledged_by_user_id`, `acknowledged_at`, `resolved_at`, `source_inventory_balance_id`.

## APIs Introduced

- Product APIs: list, create, read, update, archive.
- ProductCategory APIs: list, create/update/manage hierarchy.
- StockUnit APIs: list and manage unit conversions.
- Warehouse APIs: list, create, read, update, archive/inactivate.
- Depot APIs: list, create, read, update, archive/inactivate.
- BinLocation APIs: list, create, update, archive/inactivate.
- InventoryBalance APIs: query current balances by product/location/bin/lot/serial/condition.
- InventoryItem APIs: query item-level tracked inventory.
- ReceivingRecord APIs: create draft, update draft, post, cancel/archive.
- PickTicket APIs: create, release, complete, cancel/short.
- PackRecord APIs: create, update draft, pack/cancel.
- InventoryTransfer APIs: create, release, ship, receive, cancel, record discrepancy.
- InventoryAdjustment APIs: create, approve/reject, post, cancel.
- StockMovement APIs: list movement history and create controlled reversal.
- LowStockAlert APIs: list, acknowledge, dismiss/resolve.
- Inventory import/export APIs using ImportJob and ExportJob.
- All stock-changing APIs must be permission-checked and idempotent or accept `idempotency_key`.

## Permissions Introduced

- `inventory.product.view`
- `inventory.product.create`
- `inventory.product.update`
- `inventory.product.archive`
- `inventory.product_category.manage`
- `inventory.stock_unit.manage`
- `inventory.location.view`
- `inventory.location.manage`
- `inventory.bin.manage`
- `inventory.balance.view`
- `inventory.item.view`
- `inventory.receiving.create`
- `inventory.receiving.post`
- `inventory.pick.create`
- `inventory.pick.release`
- `inventory.pick.complete`
- `inventory.pack.create`
- `inventory.transfer.create`
- `inventory.transfer.release`
- `inventory.transfer.ship`
- `inventory.transfer.receive`
- `inventory.adjustment.create`
- `inventory.adjustment.approve`
- `inventory.adjustment.post`
- `inventory.stock_movement.view`
- `inventory.stock_movement.reverse`
- `inventory.low_stock.view`
- `inventory.low_stock.manage`
- `inventory.import`
- `inventory.export`

## UX Patterns Introduced

- Inventory workspace with Products, Balances, Warehouses, Depots, Receiving, Picking, Packing, Transfers, Adjustments, Low Stock, and Movement History views.
- Product detail page with balances, movements, units, reorder rules, files, tags, custom fields, and audit summary.
- Warehouse/Depot detail page with bins, balances, open work, recent movements, and operational flags.
- InventoryBalance matrix/drilldown by product, location, bin, lot, serial, and condition.
- Guided receiving, picking, packing, transfer, adjustment, and low-stock workflows.
- Movement history timeline/table that is visually distinct from editable workflow records.
- Setup empty states guiding users through ProductCategory, Product, Warehouse/Depot, BinLocation, and starting stock setup.
- Permission-denied states that do not leak hidden quantities or locations.
- Error states for duplicate SKU, insufficient stock, inactive location, invalid unit conversion, stale balance snapshot, and failed posting.

## Reports or Dashboards Introduced

- Inventory Balance by Product and Location.
- Low Stock and Reorder Watchlist.
- Stock Movement History.
- Receiving Volume and Supplier Receipts.
- Picking Throughput and Shortage Rate.
- Transfer Aging and Discrepancies.
- Adjustment Reasons and Value Impact.
- Damaged Inventory by Location.
- In-Transit Inventory.
- Inventory Activity by User.

## Notifications Introduced

- `low_stock_alert.opened`
- `inventory_transfer.ready_to_receive`
- `inventory_transfer.discrepancy`
- `pick_ticket.assigned`
- `pick_ticket.short`
- `inventory_adjustment.approval_requested`
- `inventory_adjustment.approved_or_rejected`
- `receiving_record.posted`

## Audit Events Introduced

- `inventory.product.created`
- `inventory.product.updated`
- `inventory.product.archived`
- `inventory.location.created`
- `inventory.location.updated`
- `inventory.bin.created`
- `inventory.bin.updated`
- `inventory.receiving.posted`
- `inventory.receiving.cancelled`
- `inventory.pick.released`
- `inventory.pick.completed`
- `inventory.pack.packed`
- `inventory.transfer.released`
- `inventory.transfer.shipped`
- `inventory.transfer.received`
- `inventory.transfer.discrepancy_recorded`
- `inventory.adjustment.created`
- `inventory.adjustment.approved`
- `inventory.adjustment.rejected`
- `inventory.adjustment.posted`
- `inventory.stock_movement.recorded`
- `inventory.stock_movement.reversed`
- `inventory.low_stock.acknowledged`
- `inventory.low_stock.resolved`
- `inventory.import.started`
- `inventory.export.started`

## Integrations Introduced

- QuickBooks item sync readiness through `Product.external_refs.quickbooks` and `accounting_code`; active QuickBooks sync remains Phase 13.
- Import/export support through Core Platform `ImportJob` and `ExportJob`.
- Future webhook eligibility for stock movement, receiving posted, pick completed, transfer shipped/received, adjustment posted, and low-stock events.
- Future Orders/Dispatch link through `PickTicket.source_entity_type/source_entity_id` and InventoryTransfer source/destination patterns.
- Future Service link through Product and StockMovement for PartsUsage.
- Future Fleet link through Depot reuse and future Vehicle location support.

## Dependencies Created

- Depends on Phase 02 Tenant, Company, UserMembership, Role, Permission, and module enablement.
- Depends on Phase 03 Core Platform shared services: AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, SettingsDocument, BackgroundJob.
- Depends on Phase 04 CRM `Account` for supplier/vendor/customer references.
- Depends on Phase 06 Calendar/Tasks where Tasks/Reminders are used for low-stock or approval follow-ups.
- Depends on Phase 07 `Job` as a valid PickTicket source context.
- Creates required dependencies for Phase 09 Orders/Dispatch, Phase 10 Fleet, Phase 11 Service, Phase 12 Reporting, Phase 13 QuickBooks/Integrations, Phase 14 Offline Mobile, and later advanced UX/scanning phases.

## Constraints Future Phases Must Respect

- Do not create duplicate Product, Item, Material, Part, Supplier, InventoryTransaction, WarehouseLocation, DepotLocation, or StockLog entities when Phase 08 entities cover the concept.
- Future orders, dispatch, logistics, service, fleet, reporting, QuickBooks, and mobile workflows must reuse `Product`, `InventoryBalance`, `StockMovement`, `Warehouse`, `Depot`, `BinLocation`, `PickTicket`, `PackRecord`, `InventoryTransfer`, and `InventoryAdjustment` where applicable.
- `StockMovement` remains append-only; correction requires reversal or adjustment, not edit/delete.
- `InventoryBalance` is current state and must be reconciled or rebuilt from StockMovement history where practical.
- Tenant/company scoping is mandatory on all inventory entities.
- Warehouse/depot/bin scoping must never replace tenant/company scoping.
- QuickBooks must not become the operational source of truth for inventory.
- Mobile/offline stock-changing workflows must use idempotency and sync conflict handling.
- Barcode scanning must build on `BinLocation.barcode_value`, product SKU/barcode-capable metadata, and stock movement commands rather than introducing a separate scanning inventory model.
- Advanced serial/lot workflows must extend `InventoryItem`, `InventoryBalance`, and `StockMovement` rather than replacing them.

## Open Questions Carried Forward

- ODR-006: Confirm final hierarchy and permission model for Branch, Warehouse, Depot, Territory, Service Area, and future Vehicle storage locations.
- ODR-013: Confirm whether serial and lot tracking must be fully supported in MVP or only data-model ready.
- ODR-014: Confirm timing and required hardware assumptions for barcode scanning.
- Confirm whether PurchaseOrder belongs in Phase 08, Phase 09, Phase 13, or a later procurement phase.
- Confirm whether trucks/vehicles should hold inventory in Phase 08 MVP or only after Fleet/Dispatch phases introduce Vehicle and RoutePlan.
- Confirm whether formal CycleCount is required in MVP or deferred.
- Confirm whether inventory valuation and costing method are required before QuickBooks integration or reporting phases.
