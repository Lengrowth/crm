# Summary for Future Phases

## Final Decisions Made

- Phase 10 establishes Fleet / GPS / Geofencing as the canonical foundation for vehicles, drivers, tracking devices, device assignments, location pings, location history, geofences, geofence events, route replay, speed alerts, stop alerts, device health events, live tracking, historical tracking, and fleet reporting.
- `Vehicle` is the canonical fleet asset record. Future phases must not create `Truck`, `Van`, `FleetAsset`, or `DeliveryVehicle` as separate entity concepts when `Vehicle` covers the meaning.
- `Driver` is the canonical operational driver resource. When a driver authenticates, Driver links to canonical `User`; it must not replace `User` or `UserMembership`.
- `TrackingDevice` is the canonical GPS/telematics device record. Provider-specific identifiers belong in `device_identifier` and `external_refs`, not as public IDs.
- `DeviceAssignment` is the canonical time-bounded assignment of a tracking device to a Vehicle, Driver, User, or other approved tracked entity. Assignment history must not be overwritten.
- `LocationPing` is the canonical append-only raw/normalized location point event. It feeds live tracking, history, route replay, geofence evaluation, and derived alerts.
- `LocationHistory` is a generated aggregation/index over LocationPing. It improves query performance but is not the raw event source of truth.
- `Geofence` is the canonical configured geographic boundary for Site, Depot, Warehouse, Branch, ShipmentStop, or custom operational locations. Future phases must not create duplicate geofence/boundary models.
- `GeofenceEvent` is the canonical append-only geofence event stream for enter, exit, dwell, missed arrival, late arrival, and unauthorized departure.
- `RouteReplay` is a derived replay session/query over retained location and event data. It must respect location history permissions and retention.
- `SpeedAlert` and `StopAlert` are derived operational alerts. Notifications should trigger from these derived exceptions, not directly from every GPS ping.
- `DeviceHealthEvent` is the canonical append-only device health event stream.
- Raw GPS pings are high-volume telemetry and must not be treated the same as business audit logs. Access/export, configuration changes, lifecycle changes, assignment changes, alert actions, and corrections must be audited.
- Fleet tracking must reuse Phase 09 `DispatchPlan`, `RoutePlan`, `ShipmentStop`, `DeliveryException`, and `HandoffEvent` where applicable.
- Fleet tracking must reuse Phase 08 `Depot`, `Warehouse`, `InventoryTransfer`, and inventory location concepts where applicable.
- Fleet tracking must reuse Phase 07 `Site`, `Job`, `Crew`, `EquipmentAssignment`, `CheckInEvent`, and field location concepts where applicable.
- Fleet tracking must reuse Phase 06 `Task`, `CalendarEvent`, `Reminder`, and `RecurrenceRule` for follow-ups, maintenance reminders, scheduled work, and later automation.
- Fleet tracking must reuse Phase 04 `Account`, `Contact`, and `Activity` for customer/site context and timeline visibility where appropriate.
- Fleet tracking must reuse Phase 03 `AuditLog`, `Notification`, `FileAttachment`, `SavedView`, `SearchIndexRecord`, `ImportJob`, `ExportJob`, `SettingsDocument`, `BackgroundJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery`.
- Fleet location access must be privacy-aware and permission-controlled. Live location, historical location, raw payloads, route replay, and exports require separate permissions.
- Retention rules for raw pings, location history, route replay caches, and exports must be respected by Reporting, Notifications/Automation, Offline Mobile, Security/Audit, Integrations, and the final blueprint.

## Entities Introduced

| Entity | Owner | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `Vehicle` | Fleet / Tracking | Company-scoped; optional branch/depot | Canonical fleet asset for trucks, vans, and other road vehicles. | Reuse for dispatch, inventory transfer, service, reporting, integrations, and maintenance. |
| `Driver` | Fleet / Tracking | Company-scoped; optional User link | Operational driver resource. | Link to `User` where authentication is required; do not duplicate identity. |
| `TrackingDevice` | Fleet / Tracking | Company-scoped; provider-aware | GPS/telematics hardware or virtual provider identity. | Map provider devices here; do not create provider-specific device entities unless approved as link entities. |
| `DeviceAssignment` | Fleet / Tracking | Company-scoped time-bounded assignment | Historical assignment of device to tracked resource. | Use for attribution; never overwrite assignment history. |
| `LocationPing` | Fleet / Tracking | Company-scoped append-only telemetry | Raw/normalized location point. | Use as source for live map, history, geofences, alerts, and replay; apply retention. |
| `LocationHistory` | Fleet / Tracking | Company-scoped generated rollup | Historical aggregation/index over pings. | Use for reporting/performance; not source of truth. |
| `Geofence` | Fleet / Tracking | Company-scoped configuration | Geographic boundary for sites, depots, warehouses, branches, stops, or custom locations. | Reuse for field, dispatch, warehouse, service, reporting, and mobile validation. |
| `GeofenceEvent` | Fleet / Tracking | Company-scoped append-only event | Enter/exit/dwell/missed/late/unauthorized departure event. | Use for reporting and derived exceptions; do not notify on every normal event. |
| `RouteReplay` | Fleet / Tracking | Company-scoped generated replay | Time-bounded replay over retained pings and events. | Respect retention, privacy, and permission restrictions. |
| `SpeedAlert` | Fleet / Tracking | Company-scoped derived alert | Speed threshold exception. | Use for safety reports and notifications; alert state is auditable. |
| `StopAlert` | Fleet / Tracking | Company-scoped derived alert | Unexpected, missed, late, excessive dwell, or unauthorized stop exception. | May link to `DeliveryException`; do not duplicate in dispatch/service. |
| `DeviceHealthEvent` | Fleet / Tracking | Company-scoped append-only event | Device health status event. | Use for device health alerts, reports, and provider monitoring. |

## Fields Introduced

- Common required fields across company-scoped fleet records: `id`, `tenant_id`, `company_id`, optional `branch_id`, status fields, timestamps, actor fields, `external_refs`, and soft-delete fields where applicable.
- `Vehicle`: `home_depot_id`, `vehicle_type`, `display_name`, `plate`, `vin`, `make`, `model`, `year`, `capacity_weight`, `capacity_volume`, `odometer_value`, `fuel_type`, `assigned_driver_id`, `current_device_assignment_id`, `maintenance_status`.
- `Driver`: `user_id`, `home_depot_id`, `display_name`, `phone`, `license_number`, `license_class`, `license_expires_at`, `default_vehicle_id`, `duty_status`, `tracking_consent_status`, `tracking_consent_at`.
- `TrackingDevice`: `provider`, `device_identifier`, `serial_number`, `imei`, `sim_number`, `device_type`, `firmware_version`, `last_seen_at`, `last_ping_at`, `battery_level`, `signal_strength`, `current_assignment_id`.
- `DeviceAssignment`: `device_id`, `assigned_entity_type`, `assigned_entity_id`, `vehicle_id`, `driver_id`, `user_id`, `start_at`, `end_at`, `assignment_reason`, `end_reason`, `install_location_notes`.
- `LocationPing`: `device_id`, `vehicle_id`, `driver_id`, `source_type`, `provider`, `provider_event_id`, `occurred_at`, `received_at`, `coordinates`, `accuracy_meters`, `speed`, `heading`, `odometer_value`, `ignition_state`, `normalization_status`, `ignored_reason`.
- `LocationHistory`: `entity_type`, `entity_id`, `time_bucket_start_at`, `time_bucket_end_at`, `path_summary`, `distance_estimate`, `duration_seconds`, `max_speed`, `avg_speed`, `stop_count`, `ping_count`, `data_quality_score`.
- `Geofence`: `shape_type`, `center_lat`, `center_lng`, `radius_meters`, `geo_shape`, `entity_link_type`, `entity_link_id`, `event_rules`, `dwell_threshold_seconds`, `arrival_window_tolerance_minutes`.
- `GeofenceEvent`: `geofence_id`, `event_type`, `entity_type`, `entity_id`, `vehicle_id`, `driver_id`, `device_id`, `location_ping_id`, `related_route_plan_id`, `related_shipment_stop_id`, `occurred_at`, `detected_at`, `rule_snapshot`.
- `RouteReplay`: `route_plan_id`, `vehicle_id`, `driver_id`, `start_at`, `end_at`, `generated_by_user_id`, `ping_count`, `path_summary`, `included_event_types`, `expires_at`, `retention_policy_snapshot`.
- `SpeedAlert`: `vehicle_id`, `driver_id`, `device_id`, `location_ping_id`, `route_plan_id`, `threshold`, `speed`, `severity`, `occurred_at`, `detected_at`, `acknowledged_by_user_id`, `resolved_by_user_id`, `dismissed_reason`, `rule_snapshot`.
- `StopAlert`: `alert_type`, `vehicle_id`, `driver_id`, `route_plan_id`, `shipment_stop_id`, `geofence_event_id`, `location_ping_id`, `severity`, `planned_window_start_at`, `planned_window_end_at`, `actual_context`.
- `DeviceHealthEvent`: `device_id`, `vehicle_id`, `event_type`, `severity`, `battery_level`, `signal_strength`, `firmware_version`, `provider`, `provider_event_id`, `health_payload`.

## APIs Introduced

- Vehicle CRUD, assignment-readiness, archive/restore, list/search/filter, and dashboard endpoints.
- Driver CRUD, User-link management, assignment-readiness, archive/restore, list/search/filter, and sensitive-field access endpoints.
- TrackingDevice CRUD, activation/deactivation, diagnostics, assignment history, and provider metadata endpoints.
- DeviceAssignment create, end, cancel, history, and conflict-detection endpoints.
- LocationPing ingestion endpoints for providers/mobile/internal sources with idempotency and normalization.
- Current location endpoints by vehicle, driver, device, route plan, and dispatch plan.
- Bounded location history endpoints requiring start/end time and permission checks.
- RouteReplay generate/read/export endpoints.
- Geofence CRUD, validation, map listing, and linked-entity endpoints.
- GeofenceEvent list/filter endpoints.
- SpeedAlert and StopAlert list/read/acknowledge/resolve/dismiss endpoints.
- DeviceHealthEvent list/filter endpoints.
- Fleet dashboard aggregate endpoints.
- ImportJob and ExportJob-backed import/export endpoints for fleet records and history summaries.

## Permissions Introduced

- `fleet.module.access`
- `fleet.vehicle.view`, `fleet.vehicle.create`, `fleet.vehicle.update`, `fleet.vehicle.archive`, `fleet.vehicle.assign`
- `fleet.driver.view`, `fleet.driver.create`, `fleet.driver.update`, `fleet.driver.archive`, `fleet.driver.assign`, `fleet.driver.sensitive.view`
- `fleet.device.view`, `fleet.device.create`, `fleet.device.update`, `fleet.device.archive`, `fleet.device.assign`, `fleet.device.health.view`
- `fleet.location.live.view`, `fleet.location.history.view`, `fleet.location.raw.view`, `fleet.location.export`
- `fleet.route_replay.view`, `fleet.route_replay.export`
- `fleet.geofence.view`, `fleet.geofence.create`, `fleet.geofence.update`, `fleet.geofence.archive`, `fleet.geofence.event.view`
- `fleet.alert.view`, `fleet.alert.acknowledge`, `fleet.alert.resolve`, `fleet.alert.dismiss`
- `fleet.report.view`
- `fleet.admin.settings.update`
- Dispatch users may receive limited read access to vehicles, drivers, current location, and stop alerts only for assigned/visible dispatch records where allowed.

## UX Patterns Introduced

- Fleet dashboard with active vehicles, stale vehicles, open alerts, device health, and geofence exceptions.
- Live fleet map with active/stale vehicle markers, last-known location, heading, driver/route context, and permission-filtered labels.
- Vehicle list/detail with table/map views, assignments, current device, current driver, route history, alerts, files, timeline, and audit summary.
- Driver list/detail with User link, duty state, assigned vehicle, route history summary, alerts, and tracking consent state.
- TrackingDevice list/detail with provider, assignment, last seen, health events, diagnostics, and assignment history.
- Geofence list/editor with map/table toggle, radius-based MVP editor, linked entity picker, validation messages, and event rule configuration.
- Route replay screen with timeline scrubber, map path, stop markers, geofence events, alert markers, data-quality indicators, and controlled export.
- Fleet alert center for SpeedAlert, StopAlert, and device-health operational issues.
- Explicit empty states for missing vehicles, drivers, devices, assignments, geofences, provider connection, and location history.
- Explicit error states for missing permission, disabled Fleet module, provider unavailable, GPS unavailable, no pings, stale data, invalid geofence, and retention-expired history.
- Non-map fallback lists for accessibility, low bandwidth, and map provider failures.

## Reports or Dashboards Introduced

- Fleet dashboard: active/stale vehicles, assigned/unassigned vehicles, open alerts, device health issues, vehicles by depot.
- Vehicle utilization: route time, idle time, distance estimate, route count, stop count, assignment coverage.
- Driver performance: assigned routes, on-time arrivals, speed alerts, stop alerts, exception rate.
- Route adherence: planned vs actual path, late stops, missed stops, dwell time, route completion.
- Geofence compliance: enter/exit count, dwell duration, unauthorized departure, missed arrival, late arrival.
- Device health: stale devices, low battery, signal loss, power disconnects, last seen age, provider reliability.
- Alert trends: incident counts, severity, acknowledgement time, resolution time.
- Data quality: ignored pings, low-accuracy pings, assignment gaps, devices without vehicles, vehicles without devices, history gaps.

## Notifications Introduced

- High-severity SpeedAlert notifications.
- StopAlert notifications for active route/DispatchPlan/ShipmentStop issues.
- Stale TrackingDevice notifications.
- DeviceHealthEvent notifications for low battery, power disconnect, no signal, and recovery where configured.
- Critical Geofence exception notifications only when configured as exception-worthy.
- No default notification for every raw LocationPing or normal GeofenceEvent.
- Notification deduplication/throttling to prevent alert storms.
- All notifications must use Phase 03 Notification and respect preferences, permissions, module enablement, and quiet-hour rules where configured.

## Audit Events Introduced

- Vehicle lifecycle, assignment, depot, driver, device, and archive/restore changes.
- Driver lifecycle, User link, sensitive license field, duty/tracking consent, and archive/restore changes.
- TrackingDevice lifecycle, provider identifier, lost/retired state, and assignment changes.
- DeviceAssignment create, activate, end, cancel, correction, and overlap rejection.
- Geofence lifecycle, shape, rule, status, archive/restore changes.
- SpeedAlert and StopAlert acknowledgement, resolution, dismissal, reopen, bulk update, and exception linkage.
- Fleet settings changes for thresholds, stale rules, geofence rules, retention, and notifications.
- RouteReplay generation, viewing where sensitive-access audit is enabled, export, expiration, and failure.
- Location export request, completion, failure, download, cancellation.
- Provider integration connection, disconnection, credential rotation, webhook changes, and sync failure acknowledgement.
- Manual corrections to location attribution, geofence events, alert state, and assignment history.
- Unauthorized access attempts to restricted live location, history, export, raw payload, or route replay endpoints.

## Integrations Introduced

- Provider GPS/telematics ingestion through authenticated webhook/API endpoints.
- Provider device/asset mapping to TrackingDevice, Vehicle, and DeviceAssignment using `external_refs` or approved link records.
- CSV/Excel imports for Vehicles, Drivers, TrackingDevices, and Geofences via ImportJob.
- ExportJob-backed exports for fleet lists, alert summaries, and bounded history summaries.
- Map/geocoding provider usage for UI display and geofence editing; canonical coordinates remain in platform records.
- QuickBooks must not receive raw telemetry; later billing/accounting phases may reference derived operational outcomes only where needed.

## Dependencies Created

- Depends on Phase 02 tenant/company/User/UserMembership/module/permission model.
- Depends on Phase 03 AuditLog, Notification, FileAttachment, SavedView, SearchIndexRecord, ImportJob, ExportJob, SettingsDocument, BackgroundJob, ApiKey, WebhookEndpoint, and WebhookDelivery.
- Depends on Phase 04 Account, Contact, Activity, and CRM timeline context where fleet events appear in customer/site context.
- Depends on Phase 06 Task, CalendarEvent, Reminder, and RecurrenceRule for follow-ups, reminders, and later scheduled maintenance/service workflows.
- Depends on Phase 07 Site, Job, Crew, EquipmentAssignment, CheckInEvent, CheckOutEvent, FieldNote, and FieldPhoto for site and field workflows.
- Depends on Phase 08 Depot, Warehouse, InventoryTransfer, and inventory/depot location model.
- Depends on Phase 09 DispatchPlan, RoutePlan, ShipmentStop, DeliveryException, HandoffEvent, Delivery, Pickup, and ProofOfDelivery.
- Creates dependencies for Phase 11 Service/Work Orders, Phase 12 Reporting, Phase 13 Integrations/QuickBooks, Phase 14 Notifications/Automation, Phase 15 Security/Audit, Phase 16 Offline Mobile, Phase 18 Advanced Reporting/Saved Views, and Phase 20 final blueprint.

## Constraints Future Phases Must Respect

- Do not create duplicate vehicle, driver, tracking device, location ping, geofence, geofence event, route replay, speed alert, stop alert, or device health concepts.
- Do not expose MongoDB `_id` as public API identifier.
- Do not treat raw GPS pings as normal audit logs or notification triggers.
- Do not expose live location, historical location, raw payloads, route replay, or exports without explicit fleet permissions.
- Do not let dispatch/service/reporting bypass fleet privacy, retention, and permission rules.
- Do not overwrite DeviceAssignment history when devices move between vehicles or drivers.
- Do not rewrite historical GeofenceEvent records when geofence shapes or rules change later.
- Do not use LocationHistory as source of truth when retained LocationPing is required for audit/replay accuracy.
- Do not create provider-specific core entities for GPS providers unless approved as link entities.
- Do not notify on every LocationPing or normal GeofenceEvent; notify only on derived exceptions or configured critical events.
- Do not allow unbounded route replay, history query, or location export time ranges.
- Do not store sensitive raw provider payloads or exports without controlled access and retention rules.

## Open Questions Carried Forward

- Which GPS/telematics provider should be supported first?
- What raw LocationPing retention period should be the default per company or subscription tier?
- Should route replay viewing always be audited, or only when sensitive-access audit is enabled?
- Should mobile app background GPS tracking be part of MVP, or should MVP rely on hardware/provider devices first?
- What default speed thresholds should apply by company, vehicle type, route type, and geofence?
- Should polygon geofences be included in MVP or deferred after radius-based geofences?
- Should driver tracking consent be mandatory for all companies or configurable by policy and jurisdiction?
- What map provider should be used for live map, geofence editing, and route replay?
- Should customer-facing ETA/live tracking links be deferred to a later customer portal phase?
- What is the exact archival strategy for raw provider payloads when normalized pings are retained?
