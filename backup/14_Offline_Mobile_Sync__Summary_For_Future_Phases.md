# Summary for Future Phases

## Final Decisions Made

- Phase 14 establishes Offline Mobile and Sync as the canonical foundation for mobile offline behavior, local caching, offline action queueing, sync orchestration, conflict handling, retry behavior, permissions revalidation, attachment/photo sync, company cache isolation, sync status UX, and mobile reliability.
- Offline capability is intentionally focused. Full offline desktop/app parity remains deferred. Initial offline support must prioritize assigned field, dispatch, service, inventory, proof, task, and event-capture workflows where connectivity loss would otherwise cause lost work.
- `OfflineCacheRecord` is the canonical local-cache manifest/state record for offline-capable records and payload bundles. Future phases must not create module-specific local cache entities such as `TaskOfflineCache`, `RouteCache`, or `ServiceCache`.
- `OfflineActionQueueItem` is the canonical client-side queued action record for offline-created, offline-updated, or deferred mobile actions. Future phases must not create separate queue entities per module.
- `SyncOperation` is the canonical server-visible sync transaction/run record for mobile sync attempts, batches, uploads, downloads, retries, permission revalidations, and conflict outcomes. It complements but does not replace Phase 13 `SyncJob` for integration/provider sync work.
- `SyncConflict` is the canonical conflict record for offline sync conflicts that need system resolution, user resolution, supervisor resolution, or audit/reporting visibility.
- `SyncStatus` is the canonical reusable sync-state object/summary exposed on offline-capable records, list rows, detail headers, sync center screens, and admin monitoring.
- Offline-created records and events must carry stable application IDs, `tenant_id`, `company_id`, actor identity, original client timestamp, device/session metadata, idempotency key, and `sync_metadata`.
- Server-side validation, module enablement checks, company access checks, record-level permission checks, and workflow status checks must be revalidated when queued offline actions sync. Frontend pre-checks are not enough.
- Offline actions must never silently disappear. Users must see pending, syncing, synced, failed, blocked, and conflict states where relevant, with safe retry behavior.
- Append-only event records such as `CheckInEvent`, `CheckOutEvent`, `FieldNote` events, `LocationPing`, `GeofenceEvent`, `HandoffEvent`, `StockMovement`, `JobProgressEvent`, and proof/completion events should prefer additive/idempotent sync rather than destructive merge.
- Mutable record updates must use version/ETag or equivalent optimistic concurrency. Conflicts must be handled by explicit strategy: server wins, client wins by permissioned override, field-level merge, duplicate-safe append, or user/supervisor resolution.
- Attachment and photo sync must use `FileAttachment` as the canonical file model. Module-specific wrappers such as `FieldPhoto` and `ProofOfDelivery` may reference `FileAttachment`; they must not store binary content directly.
- Company cache isolation is mandatory. A mobile device must never expose one company’s cached data while operating in another company context. Switching company context must lock, clear, or partition local caches according to approved security settings.
- Sync UX must be consistent across mobile modules: offline banner, per-record sync badges, queue/sync center, retry controls, conflict resolution screen, attachment upload progress, stale-data warnings, and safe sign-out behavior.
- Admin/security, notifications/automation, reporting, rollout, and final blueprint phases must respect offline validation, conflict, local cache, company isolation, queue, and sync-status rules from Phase 14.

## Entities Introduced

| Entity | Owner Module | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `OfflineCacheRecord` | Offline Mobile and Sync | Client-local with tenant/company/user/session scope; server may store manifest summaries | Tracks which records, bundles, attachments, metadata, and permissions are cached for offline use. | Reuse for all offline cache tracking; do not create module-specific cache state records. |
| `OfflineActionQueueItem` | Offline Mobile and Sync | Client-local first; server may receive mirrored queue metadata during sync | Captures offline or deferred actions with payload, target, idempotency key, status, retry state, dependencies, and validation result. | Reuse for offline action queueing across field, dispatch, inventory, fleet, service, and tasks. |
| `SyncOperation` | Offline Mobile and Sync | Tenant/company/user/device scoped; server-visible | Represents a mobile sync run, batch, upload, download, retry, permission revalidation, or conflict-handling operation. | Reuse for mobile sync observability; do not confuse with provider integration `SyncJob`. |
| `SyncConflict` | Offline Mobile and Sync | Tenant/company/record/user scoped | Records conflicts created by stale local data, server-side changes, permission revocation, duplicate events, deleted/archived records, or workflow invalidation. | Reuse for all offline conflict tracking and resolution workflows. |
| `SyncStatus` | Offline Mobile and Sync | Embedded object or derived summary on records, queue items, sync operations, and views | Standardizes sync state shown to users, admins, reports, and APIs. | Reuse status vocabulary and badges across future mobile, reporting, admin, and rollout phases. |

## Fields Introduced

- Shared sync fields: `sync_status`, `sync_metadata`, `local_record_id`, `server_record_id`, `client_generated_id`, `idempotency_key`, `client_version`, `server_version`, `base_version`, `last_synced_at`, `last_sync_attempt_at`, `last_sync_error_code`, `last_sync_error_message`, `conflict_id`, `device_id`, `session_id`, `offline_created_at`, `offline_updated_at`, `client_occurred_at`, `synced_at`, `sync_batch_id`, `requires_user_resolution`, `requires_admin_review`.
- `OfflineCacheRecord` fields: `id`, `tenant_id`, `company_id`, `user_id`, `membership_id`, `device_id`, `session_id`, `record_type`, `record_id`, `record_scope`, `cache_key`, `cache_version`, `record_version`, `payload_hash`, `cached_payload_ref`, `cached_at`, `expires_at`, `last_accessed_at`, `stale_at`, `cache_status`, `offline_available`, `pinned_by_user`, `preloaded_by_rule`, `permission_snapshot`, `module_snapshot`, `attachment_manifest`, `size_bytes`, `encryption_state`, `purge_reason`, `sync_metadata`.
- `OfflineActionQueueItem` fields: `id`, `tenant_id`, `company_id`, `user_id`, `membership_id`, `device_id`, `session_id`, `target_entity_type`, `target_entity_id`, `local_target_id`, `action_type`, `operation_type`, `payload`, `payload_hash`, `payload_schema_version`, `depends_on_queue_item_ids`, `idempotency_key`, `base_version`, `client_version`, `created_offline_at`, `queued_at`, `first_attempted_at`, `last_attempted_at`, `attempt_count`, `next_retry_at`, `queue_status`, `priority`, `validation_status`, `server_response_ref`, `conflict_id`, `error_code`, `error_message`, `sync_operation_id`.
- `SyncOperation` fields: `id`, `tenant_id`, `company_id`, `user_id`, `membership_id`, `device_id`, `session_id`, `operation_type`, `trigger`, `direction`, `status`, `started_at`, `completed_at`, `items_total`, `items_succeeded`, `items_failed`, `items_conflicted`, `bytes_uploaded`, `bytes_downloaded`, `network_type`, `app_version`, `schema_version`, `retry_of_operation_id`, `correlation_id`, `error_code`, `error_message`, `summary`, `sync_metadata`.
- `SyncConflict` fields: `id`, `tenant_id`, `company_id`, `user_id`, `membership_id`, `device_id`, `target_entity_type`, `target_entity_id`, `local_target_id`, `queue_item_id`, `sync_operation_id`, `conflict_type`, `conflict_status`, `resolution_strategy`, `server_snapshot_ref`, `client_snapshot_ref`, `field_diffs`, `detected_at`, `resolved_at`, `resolved_by_user_id`, `resolution_notes`, `audit_log_id`, `requires_supervisor`, `blocking_reason`.
- `SyncStatus` fields: `state`, `detail`, `last_synced_at`, `last_attempted_at`, `pending_count`, `failed_count`, `conflict_count`, `blocked_count`, `stale`, `stale_reason`, `retry_available`, `manual_resolution_required`, `last_error_code`, `last_error_message`, `sync_operation_id`.

## APIs Introduced

- `GET /api/v1/mobile/bootstrap` returns company-scoped offline bootstrap configuration, module availability, sync schema versions, user permissions summary, and cache rules.
- `GET /api/v1/mobile/sync/pull` returns authorized changes, deletions/tombstones, version updates, cache invalidation hints, and attachment manifests since a cursor.
- `POST /api/v1/mobile/sync/push` submits queued offline actions with idempotency keys, dependency ordering, client timestamps, device metadata, and base versions.
- `POST /api/v1/mobile/sync/operations` creates or starts a `SyncOperation` for observability and correlation.
- `GET /api/v1/mobile/sync/operations/{sync_operation_id}` returns sync operation status, counts, errors, conflicts, and retry guidance.
- `GET /api/v1/mobile/sync/status` returns queue, cache, conflict, failed upload, stale data, and permission-blocked summaries for the current user/company/device.
- `POST /api/v1/mobile/sync/queue/{queue_item_id}/retry` retries a failed queue item when safe.
- `POST /api/v1/mobile/sync/conflicts/{sync_conflict_id}/resolve` resolves conflicts using approved strategies and required permissions.
- `POST /api/v1/mobile/attachments/initiate-upload` creates a resumable upload session for offline photos/files using `FileAttachment`.
- `POST /api/v1/mobile/attachments/complete-upload` completes attachment upload and binds the file to the target record or wrapper after permission revalidation.
- `POST /api/v1/mobile/cache/purge` clears company/user/device cache state for logout, company switch, admin revocation, or security event.
- `GET /api/v1/mobile/sync/cursors` returns current server cursors by entity/workflow for incremental sync.

## Permissions Introduced

- `offline.sync.use` allows a user to use offline sync in an enabled company.
- `offline.cache.read` allows authorized mobile caching of assigned records and permitted reference data.
- `offline.queue.create` allows creating local queued actions for approved workflows.
- `offline.queue.retry` allows retrying the user’s own failed queue items.
- `offline.queue.admin_review` allows admins/supervisors to view and manage failed queue items for users in their company scope.
- `offline.conflict.view` allows viewing sync conflicts for records the user can access.
- `offline.conflict.resolve_own` allows resolving conflicts caused by the user’s own queued actions when the target workflow permits it.
- `offline.conflict.resolve_team` allows supervisors/admins to resolve conflicts for assigned teams or company scope.
- `offline.cache.purge` allows admin-triggered remote cache purge or device session invalidation.
- `offline.sync.monitor` allows admin/reporting users to view sync health dashboards and operation history.
- Existing record permissions still apply. Offline permission keys never bypass `task.*`, `field.*`, `dispatch.*`, `inventory.*`, `fleet.*`, `service.*`, `file.*`, `report.*`, or admin permissions.

## UX Patterns Introduced

- Global mobile offline banner with states: online, weak connection, offline, syncing, sync failed, conflict needs review, cache stale.
- Per-record sync badge displayed on lists, detail headers, forms, attachments, timeline entries, and completion screens.
- Mobile Sync Center screen showing pending actions, failed actions, conflicts, attachment uploads, stale cached data, last successful sync, and retry options.
- Conflict Resolution screen showing user-entered values, server values, reason for conflict, safe merge choices, permission errors, and escalation path.
- Attachment upload progress and retry UI for photos, signatures, proof files, and documents.
- Company switch protection pattern requiring cache partitioning, purge, or reauthentication before another company’s cache is available.
- Offline-safe form pattern: show cached-data age, local validation, server-validation pending notice, and final sync outcome.
- Empty states for no offline records, no pending sync items, no conflicts, no failed uploads, and no cache available.
- Error states for permission revoked, record deleted/archived, module disabled, stale version, dependency failed, attachment upload failed, and storage quota exceeded.

## Reports or Dashboards Introduced

- Mobile Sync Health dashboard: active devices, last sync times, pending queue counts, failed items, conflicts, blocked permissions, upload failures, and stale cache counts.
- Offline Adoption report: users using offline mode, workflows captured offline, offline completion rates, average sync delay, and sync success rate.
- Conflict Resolution report: conflicts by module, entity, type, age, resolver, outcome, and repeat conflict patterns.
- Attachment Sync report: pending uploads, failed uploads, retry counts, file sizes, and time to completion.
- Permission Revalidation Failure report: queued actions blocked because company/module/record permissions changed before sync.

## Notifications Introduced

- Notify mobile user when queued actions fail permanently or require conflict resolution.
- Notify mobile user when large attachment uploads fail after retries.
- Notify supervisor/admin when high-priority field, service, proof, dispatch, or inventory actions are blocked beyond configured thresholds.
- Notify admin/security when a cache purge, device revocation, or suspicious repeated sync failure occurs.
- Notify assigned record owners when offline completion, proof, or exception events sync successfully if the workflow already supports such notifications.
- Notifications must not reveal inaccessible record data and must respect notification preferences unless security-critical.

## Audit Events Introduced

- `offline.cache.created`, `offline.cache.refreshed`, `offline.cache.stale`, `offline.cache.purged`
- `offline.queue.item_created`, `offline.queue.item_synced`, `offline.queue.item_failed`, `offline.queue.item_retried`, `offline.queue.item_blocked`
- `offline.sync.started`, `offline.sync.completed`, `offline.sync.failed`, `offline.sync.partial_success`
- `offline.conflict.detected`, `offline.conflict.resolved`, `offline.conflict_escalated`, `offline.conflict_rejected`
- `offline.permission_revalidated`, `offline.permission_revalidation_failed`
- `offline.attachment.upload_started`, `offline.attachment.upload_completed`, `offline.attachment.upload_failed`
- `offline.device.cache_purge_requested`, `offline.device.cache_purge_completed`, `offline.device_revoked`

## Integrations Introduced

- Phase 14 does not introduce third-party provider integrations.
- Offline sync must not duplicate Phase 13 integration entities. Mobile `SyncOperation` is for mobile/offline sync; provider accounting sync continues to use `SyncJob`, `SyncLog`, `ExternalReference`, and provider link entities.
- Offline-created records that later sync to QuickBooks or other providers must preserve stable IDs, timestamps, audit history, and external reference readiness.
- Attachment sync must use the Core Platform file service and `FileAttachment` so later API/webhook/export phases can reuse file metadata and permissions.
- Future public API and webhook phases must respect idempotency keys, server versions, conflict semantics, and tombstone/change cursor behavior defined by Phase 14.

## Dependencies Created

- Depends on Tenant, Company, User, UserMembership, Role, Permission, Session, and module access rules from Phase 02.
- Depends on AuditLog, Notification, FileAttachment, SavedView, SearchIndexRecord, SettingsDocument, BackgroundJob, ImportJob, ExportJob, ApiKey, WebhookEndpoint, and WebhookDelivery foundations from Phase 03.
- Depends on CRM records such as Account, Contact, Lead, Opportunity, Activity, and AssignmentRule where offline mobile workflows reference customer context.
- Depends on Task, CalendarEvent, Appointment, Reminder, and RecurrenceRule for mobile work queues and scheduled field/service workflows.
- Depends on Site, SiteVisit, CheckInEvent, CheckOutEvent, FieldNote, FieldPhoto, JobRequest, Job, JobStage, Crew, EquipmentAssignment, and JobProgressEvent for field offline capture.
- Depends on Product, InventoryItem, InventoryBalance, Warehouse, Depot, BinLocation, PickTicket, PackRecord, StockMovement, InventoryAdjustment, and InventoryTransfer for warehouse/depot offline operations.
- Depends on Order, Shipment, ShipmentStop, DispatchPlan, RoutePlan, Delivery, Pickup, ProofOfDelivery, DeliveryException, and HandoffEvent for dispatch/logistics offline workflows.
- Depends on Vehicle, Driver, TrackingDevice, LocationPing, GeofenceEvent, and DeviceHealthEvent for fleet/mobile location-aware workflows.
- Depends on ServiceRequest, WorkOrder, WorkOrderTask, MaintenanceSchedule, LaborEntry, PartsUsage, and ServiceHistory for service offline workflows.
- Depends on Dashboard, Report, ReportDefinition, ReportRun, MetricDefinition, and RollupSnapshot for sync health reporting.
- Depends on IntegrationConnection, IntegrationAccount, SyncJob, SyncLog, ExternalReference, and QuickBooks link entities for downstream provider sync readiness.

## Constraints Future Phases Must Respect

- Admin/security must include device session management, cache purge, offline permission revalidation, offline audit review, sync monitoring permissions, and company cache isolation.
- Notifications/automation must not trigger prematurely from unsynced offline actions unless explicitly marked as local-only reminders. Server-side notifications must occur only after successful sync or approved conflict resolution.
- Reporting must distinguish client occurrence time, server sync time, and resolution time for offline actions.
- Public API/webhooks/import/export must preserve idempotency, versioning, tombstones, sync cursors, conflict semantics, and stable IDs.
- Rollout/migration must test weak connectivity, app upgrades with queued actions, local schema migrations, remote wipe/cache purge, device loss, and storage quota behavior.
- Final blueprint must verify that every mobile/offline-capable workflow defines cached data, queued actions, sync trigger, conflict handling, failed sync visibility, permissions revalidation, attachment handling, and audit behavior.
- Future phases must not introduce module-specific offline queues, conflict tables, cache records, or sync status vocabulary unless a new global decision supersedes Phase 14.
- Future phases must not make offline actions bypass workflow rules, inventory integrity, dispatch status rules, service completion rules, QuickBooks sync constraints, audit logging, or record-level permissions.

## Open Questions Carried Forward

- OQ-14-001: Confirm final application ID generator for offline-capable records: ULID, UUIDv7, KSUID, or another opaque sortable ID.
- OQ-14-002: Confirm mobile storage technology per client platform, including encryption, schema migration, and quota behavior.
- OQ-14-003: Confirm whether Phase 14 implementation is PWA-first, native-first, or hybrid for MVP.
- OQ-14-004: Confirm remote wipe requirements for lost devices and terminated users.
- OQ-14-005: Confirm how long offline cached data may remain on a device before forced refresh or purge.
- OQ-14-006: Confirm exact attachment upload limits, compression rules, and background upload behavior.
- OQ-14-007: Confirm whether supervisors can resolve field user conflicts on behalf of users for all workflows or only selected high-risk workflows.
- OQ-14-008: Confirm whether offline map tiles/geocoding are in MVP scope or deferred.
- OQ-14-009: Confirm whether inventory quantity-changing actions are offline-enabled in MVP or restricted to online-only except drafts.
- OQ-14-010: Confirm whether QuickBooks-triggering actions created offline are held until successful operational sync and admin review or allowed to enter provider sync automatically when validation passes.
