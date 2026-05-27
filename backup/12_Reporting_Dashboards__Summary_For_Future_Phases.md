# Summary for Future Phases

## Final Decisions Made

- Phase 12 establishes Reporting / Dashboards as the canonical foundation for dashboards, reports, report definitions, report runs, metric definitions, rollup snapshots, scheduled reports, analytics permissions, dashboard UX, report filters, data freshness, and materialized metrics.
- `Dashboard` is the canonical configurable visual workspace for KPIs, charts, tables, operational summaries, and drilldowns. Future phases must not create module-specific dashboard entities such as `ServiceDashboard`, `FleetDashboard`, or `SalesDashboard`; use `Dashboard` with module context and cards instead.
- `Report` is the canonical user-facing saved or generated report record. It must not replace `ReportDefinition`; it references or materializes from a definition and stores selected filters, columns, grouping, visibility, and ownership.
- `ReportDefinition` is the canonical reusable report template/source schema record. It defines datasets, allowed joins, filter schemas, columns, metrics, grouping rules, visualization defaults, and execution constraints.
- `ReportRun` is the canonical immutable execution record for generated reports, exports, scheduled report deliveries, and expensive dashboard refreshes. Future export/API phases must reuse it for report execution observability.
- `MetricDefinition` is the canonical reusable metric catalog entry. Metrics used by dashboards, reports, automation, QuickBooks sync monitoring, final blueprint, and rollout analytics must use these definitions instead of ad hoc formulas.
- `RollupSnapshot` is the canonical materialized metric/report aggregate record. Expensive operational metrics must use snapshots where needed and must expose freshness metadata.
- `ScheduledReport` is the canonical schedule and recipient configuration for recurring report delivery. It must reuse notification/export foundations and must revalidate permissions at run time.
- Reporting is read-oriented and cross-module, but it does not own operational source-of-truth records from CRM, outbound, calendar/tasks, field, inventory, dispatch, fleet, or service.
- Reporting must reuse Phase 03 shared services: `AuditLog`, `Notification`, `FileAttachment`, `SavedView`, `SearchIndexRecord`, `ImportJob`, `ExportJob`, `SettingsDocument`, `BackgroundJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery`.
- Reporting must reuse Phase 04 CRM entities and activity history for sales, account, pipeline, contact, lead, opportunity, and activity analytics.
- Reporting must reuse Phase 05 outbound records for campaign, sequence, enrollment, outreach, channel activity, conversion, and rep performance analytics.
- Reporting must reuse Phase 06 `Task`, `CalendarEvent`, `Appointment`, `Reminder`, and `RecurrenceRule` for task, schedule, SLA, reminder, and scheduled report cadence context.
- Reporting must reuse Phase 07 field entities for site, visit, check-in/out, job, crew, equipment, photo, and field note analytics.
- Reporting must reuse Phase 08 inventory entities for product, stock movement, inventory balance, warehouse, depot, bin, receiving, picking, packing, adjustment, transfer, and low-stock analytics.
- Reporting must reuse Phase 09 orders/dispatch/logistics entities for orders, shipments, stops, dispatch plans, route plans, proof, exceptions, pickups, deliveries, and handoff analytics.
- Reporting must reuse Phase 10 fleet entities for vehicle, driver, device, assignment, location, geofence, route replay, alert, and device health analytics. Raw GPS pings must not be exposed through broad reports unless permission and retention rules allow it.
- Reporting must reuse Phase 11 service entities for service requests, work orders, work order tasks, maintenance schedules, service history, labor entries, and parts usage analytics.
- All Phase 12 reporting records are tenant/company scoped unless explicitly platform-provided templates are read-only and copied into company scope.
- MongoDB `_id` must never be exposed as a public report/dashboard/API identifier.
- Reporting permissions must enforce tenant, company, module enablement, record permission, analytics permission, export permission, schedule permission, and sensitive-field restrictions.
- Dashboard and report results must not leak record counts, labels, names, GPS/location data, service history, revenue, inventory value, or personally sensitive user performance information to unauthorized users.
- Report exports must preserve filters, columns, grouping, run timestamp, actor, freshness metadata, and permission context.
- Dashboard cards and reports must display data freshness, source module, filter scope, and permission-truncated states where relevant.
- Real-time consistency is not required for rollup-backed dashboards. Staleness must be visible and bounded by metric freshness targets.
- Scheduled reports and report exports must use background jobs and must not execute long-running report work inside the main API request path.
- Report schedules must revalidate recipient permissions at delivery time and suppress unauthorized rows/columns rather than sending stale entitlements.
- Custom reports are supported at the definition/configuration level, but unrestricted arbitrary database querying is not allowed in MVP.

## Entities Introduced

| Entity | Owner module | Scope | Purpose | Future phase rule |
| --- | --- | --- | --- | --- |
| `Dashboard` | Reporting / Analytics | Company-scoped; optional user/team/shared visibility | Configurable visual workspace for KPIs, charts, tables, and drilldowns. | Reuse for all module dashboards; do not create module-specific dashboard entities. |
| `Report` | Reporting / Analytics | Company-scoped; optional user/team/shared visibility | User-facing saved/generated report using filters, columns, grouping, and definition references. | Reuse for report lists, exports, schedules, API report execution, and analytics UX. |
| `ReportDefinition` | Reporting / Analytics | Company-scoped configuration; optional platform template source | Canonical report schema/template with dataset, filters, columns, joins, metrics, and visualization defaults. | Future modules must register reportable datasets through definitions, not ad hoc report code only. |
| `ReportRun` | Reporting / Analytics | Company-scoped immutable execution history | Execution record for report generation, export, schedule, or dashboard refresh. | Export/API/integration phases must reuse for observability and auditability. |
| `MetricDefinition` | Reporting / Analytics | Company-scoped configuration; optional platform defaults | Reusable metric formula and dimension definition. | Future phases must use metric catalog standards for KPIs and automation triggers. |
| `RollupSnapshot` | Reporting / Analytics | Company-scoped materialized aggregate | Materialized aggregate at a defined metric, grain, scope, and time period. | Expensive reports and dashboards must use snapshots where needed and show freshness metadata. |
| `ScheduledReport` | Reporting / Analytics | Company-scoped schedule configuration | Recurring report refresh/delivery settings with recipients, formats, cadence, and permissions. | Notification/export/API phases must reuse it for report delivery. |

## Fields Introduced

### Dashboard

`id`, `tenant_id`, `company_id`, `name`, `description`, `dashboard_type`, `module_scope`, `layout`, `cards`, `default_filters`, `visibility`, `owner_user_id`, `owner_team_id`, `shared_role_ids`, `source_report_ids`, `source_metric_ids`, `refresh_policy`, `freshness_status`, `last_refreshed_at`, `status`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id`, `external_refs`.

### Report

`id`, `tenant_id`, `company_id`, `report_definition_id`, `name`, `description`, `report_type`, `module_scope`, `filters`, `columns`, `group_by`, `sort`, `visualization`, `visibility`, `owner_user_id`, `owner_team_id`, `shared_role_ids`, `last_run_id`, `last_run_at`, `last_successful_run_at`, `freshness_status`, `export_allowed`, `schedule_allowed`, `status`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id`, `external_refs`.

### ReportDefinition

`id`, `tenant_id`, `company_id`, `template_origin`, `name`, `description`, `source_module`, `dataset_key`, `base_entity`, `allowed_joins`, `filter_schema`, `column_schema`, `metric_definition_ids`, `default_columns`, `default_filters`, `default_group_by`, `default_sort`, `supported_visualizations`, `row_level_permission_model`, `sensitive_fields`, `execution_mode`, `max_date_range_days`, `max_row_limit`, `snapshot_policy`, `status`, `version`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deprecated_at`, `external_refs`.

### ReportRun

`id`, `tenant_id`, `company_id`, `report_id`, `report_definition_id`, `scheduled_report_id`, `dashboard_id`, `run_type`, `requested_by_user_id`, `requested_for_user_id`, `filters_snapshot`, `columns_snapshot`, `permission_context_snapshot`, `freshness_snapshot`, `status`, `started_at`, `completed_at`, `failed_at`, `duration_ms`, `row_count`, `truncated`, `result_file_attachment_id`, `error_code`, `error_message`, `correlation_id`, `idempotency_key`, `created_at`.

### MetricDefinition

`id`, `tenant_id`, `company_id`, `metric_key`, `name`, `description`, `source_module`, `source_entities`, `formula`, `aggregation`, `dimensions`, `grain`, `time_field`, `filters`, `permission_model`, `freshness_target_minutes`, `snapshot_required`, `display_format`, `higher_is_better`, `owner_user_id`, `status`, `version`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deprecated_at`.

### RollupSnapshot

`id`, `tenant_id`, `company_id`, `metric_definition_id`, `report_definition_id`, `source_module`, `snapshot_key`, `grain`, `period_start_at`, `period_end_at`, `dimensions`, `scope`, `values`, `source_watermark_at`, `computed_at`, `computation_status`, `source_record_count`, `error_code`, `error_message`, `version`, `created_at`.

### ScheduledReport

`id`, `tenant_id`, `company_id`, `report_id`, `report_definition_id`, `name`, `description`, `schedule_rule_id`, `timezone`, `recipient_user_ids`, `recipient_team_ids`, `recipient_email_overrides`, `delivery_channels`, `export_format`, `filters_snapshot`, `columns_snapshot`, `visibility`, `owner_user_id`, `next_run_at`, `last_run_id`, `last_run_at`, `last_successful_run_at`, `failure_count`, `status`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `paused_at`, `deleted_at`.

## APIs Introduced

- `GET /api/v1/dashboards`
- `POST /api/v1/dashboards`
- `GET /api/v1/dashboards/{dashboard_id}`
- `PATCH /api/v1/dashboards/{dashboard_id}`
- `DELETE /api/v1/dashboards/{dashboard_id}`
- `POST /api/v1/dashboards/{dashboard_id}/refresh`
- `GET /api/v1/reports`
- `POST /api/v1/reports`
- `GET /api/v1/reports/{report_id}`
- `PATCH /api/v1/reports/{report_id}`
- `DELETE /api/v1/reports/{report_id}`
- `POST /api/v1/reports/{report_id}/run`
- `POST /api/v1/reports/{report_id}/export`
- `GET /api/v1/report-definitions`
- `GET /api/v1/report-definitions/{report_definition_id}`
- `POST /api/v1/report-definitions`
- `PATCH /api/v1/report-definitions/{report_definition_id}`
- `GET /api/v1/report-runs`
- `GET /api/v1/report-runs/{report_run_id}`
- `GET /api/v1/metric-definitions`
- `POST /api/v1/metric-definitions`
- `PATCH /api/v1/metric-definitions/{metric_definition_id}`
- `GET /api/v1/rollup-snapshots`
- `GET /api/v1/scheduled-reports`
- `POST /api/v1/scheduled-reports`
- `PATCH /api/v1/scheduled-reports/{scheduled_report_id}`
- `DELETE /api/v1/scheduled-reports/{scheduled_report_id}`
- `POST /api/v1/scheduled-reports/{scheduled_report_id}/run-now`

## Permissions Introduced

- `reporting.dashboard.view`
- `reporting.dashboard.create`
- `reporting.dashboard.update`
- `reporting.dashboard.delete`
- `reporting.dashboard.share`
- `reporting.dashboard.refresh`
- `reporting.report.view`
- `reporting.report.create`
- `reporting.report.update`
- `reporting.report.delete`
- `reporting.report.run`
- `reporting.report.export`
- `reporting.report.schedule`
- `reporting.report.share`
- `reporting.report_definition.view`
- `reporting.report_definition.manage`
- `reporting.metric_definition.view`
- `reporting.metric_definition.manage`
- `reporting.rollup_snapshot.view`
- `reporting.sensitive_metrics.view`
- `reporting.cross_company.view` as a future/admin-only permission when cross-company reporting is explicitly enabled.

## UX Patterns Introduced

- Reporting home with role-aware default dashboards, recently viewed reports, scheduled reports, and data freshness notices.
- Dashboard builder with drag-and-drop layout, cards, metric tiles, charts, tables, drilldowns, saved filters, and permission-aware preview.
- Report catalog with module, owner, visibility, schedule, freshness, and favorite filters.
- Report builder with dataset selection, field picker, filters, grouping, sorting, visualization configuration, preview, and validation.
- Report run history screen with status, row counts, execution duration, result files, errors, and permission context.
- Metric catalog screen for admin/analyst users.
- Scheduled report management screen with cadence, timezone, recipients, delivery channel, export format, and permission warning preview.
- Empty, stale, permission-truncated, unsupported-module, no-data, over-limit, and background-job-running states are required.

## Reports or Dashboards Introduced

- Executive Overview Dashboard.
- Sales Pipeline Dashboard.
- Outbound Performance Dashboard.
- Calendar / Task SLA Dashboard.
- Field Operations Dashboard.
- Inventory / Warehouse Dashboard.
- Orders / Dispatch Dashboard.
- Fleet / GPS Dashboard.
- Service / Work Orders Dashboard.
- Team Productivity Dashboard.
- Exception and Risk Dashboard.
- QuickBooks / Integration Readiness Dashboard foundation for later phases.

## Notifications Introduced

- Scheduled report delivered.
- Scheduled report failed.
- Report export completed.
- Report export failed.
- Dashboard refresh failed.
- Rollup computation delayed or failed.
- Sensitive report shared.
- Scheduled report recipient permission removed.
- Report definition deprecated.

## Audit Events Introduced

- `reporting.dashboard.created`
- `reporting.dashboard.updated`
- `reporting.dashboard.deleted`
- `reporting.dashboard.shared`
- `reporting.dashboard.refreshed`
- `reporting.report.created`
- `reporting.report.updated`
- `reporting.report.deleted`
- `reporting.report.shared`
- `reporting.report.run_requested`
- `reporting.report.export_requested`
- `reporting.report.export_completed`
- `reporting.report.export_failed`
- `reporting.report_definition.created`
- `reporting.report_definition.updated`
- `reporting.report_definition.deprecated`
- `reporting.metric_definition.created`
- `reporting.metric_definition.updated`
- `reporting.metric_definition.deprecated`
- `reporting.rollup_snapshot.computed`
- `reporting.rollup_snapshot.failed`
- `reporting.scheduled_report.created`
- `reporting.scheduled_report.updated`
- `reporting.scheduled_report.paused`
- `reporting.scheduled_report.deleted`
- `reporting.scheduled_report.delivered`
- `reporting.scheduled_report.failed`
- `reporting.sensitive_data_accessed`

## Integrations Introduced

- Reporting exports must reuse `ExportJob` and `FileAttachment`.
- Scheduled report delivery must reuse `Notification` and future email/provider delivery foundations.
- Public API/export phases must expose report execution through `ReportRun` instead of bypassing report permissions.
- QuickBooks/integration phases must reuse `MetricDefinition` and `RollupSnapshot` standards for sync health, invoice readiness, inventory valuation, service billing readiness, and reconciliation dashboards.
- Webhooks may later be emitted for report export completed, scheduled report failed, and rollup failed events through `WebhookEndpoint` and `WebhookDelivery`.

## Dependencies Created

- Depends on Phase 02 tenant/company/user/membership/role/permission rules.
- Depends on Phase 03 shared services for audit, notification, files, saved views, search, import/export, settings, background jobs, API keys, and webhooks.
- Depends on Phase 04 CRM data for account, contact, lead, opportunity, pipeline, activity, and ownership metrics.
- Depends on Phase 05 outbound data for campaign, sequence, outreach, channel, conversion, and rep metrics.
- Depends on Phase 06 calendar/tasks for task, event, appointment, reminder, recurrence, SLA, and scheduled report cadence semantics.
- Depends on Phase 07 field/site/job data for site, visit, check-in/out, job, crew, field note, field photo, and equipment metrics.
- Depends on Phase 08 inventory/warehouse data for product, stock, movement, balance, warehouse, depot, bin, receiving, pick/pack, adjustment, transfer, and low-stock metrics.
- Depends on Phase 09 order/dispatch/logistics data for order, shipment, stop, route, delivery, pickup, proof, exception, and handoff metrics.
- Depends on Phase 10 fleet/device tracking data for vehicle, driver, device, location history, geofence, route replay, alert, and device health metrics.
- Depends on Phase 11 service/work order data for service request, work order, task, maintenance, service history, labor, and parts metrics.

## Constraints Future Phases Must Respect

- Future QuickBooks/integration, admin/security, notifications/automation, API/export, final blueprint, and rollout phases must use Phase 12 reporting definitions, metric standards, run history, freshness metadata, and permission model.
- Future phases must register new reportable datasets and metrics through `ReportDefinition` and `MetricDefinition` rather than creating isolated reporting logic.
- Future phases must not expose exports, dashboards, API reports, or scheduled reports without enforcing reporting permissions and source-record permissions.
- Future phases must not send scheduled reports without permission revalidation at delivery time.
- Future phases must include data freshness and rollup computation status wherever materialized metrics are displayed.
- Future phases must preserve report run history for audit, troubleshooting, and customer support.
- Future phases must not treat rollup snapshots as source-of-truth operational records; they are derived, materialized reporting artifacts.
- Future phases must avoid arbitrary unrestricted database query builders in customer-facing reporting unless a later security/admin decision explicitly approves it.
- Future phases must not create provider-specific metric fields when `MetricDefinition`, `RollupSnapshot`, or `external_refs` can represent the relationship.

## Open Questions Carried Forward

- Confirm the exact MVP list of default dashboards by role and module package.
- Confirm whether company admins may create custom `ReportDefinition` records in MVP or only create `Report` records from platform-provided definitions.
- Confirm whether cross-company reporting is required for tenant administrators in MVP or deferred to admin/security phases.
- Confirm export row limits, retention periods for report result files, and whether large exports require approval workflows.
- Confirm whether scheduled reports may deliver to external email addresses in MVP or only to authenticated users.
- Confirm whether sensitive metrics such as individual performance, revenue, GPS history, inventory valuation, and service labor cost require separate permission gates by default.
- Confirm rollup computation SLAs per dashboard category.
- Confirm whether report definitions are versioned with immutable historical versions or mutable versions with run snapshots only.
