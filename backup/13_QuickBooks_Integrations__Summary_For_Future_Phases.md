# Summary for Future Phases

## Final Decisions Made

- Phase 13 establishes QuickBooks as the first accounting integration and creates the reusable integration foundation for provider connections, external accounts, sync jobs, sync logs, external references, QuickBooks links, webhook delivery attempts, retries, errors, admin visibility, reporting, and auditability.
- `IntegrationConnection` is the canonical configured provider connection record. Future phases must not create provider-specific connection entities such as `QuickBooksConnection`, `SmsConnection`, or `TelematicsConnection`; use `IntegrationConnection` with `provider` and provider metadata.
- `IntegrationAccount` is the canonical external account/profile/realm context under an `IntegrationConnection`. For QuickBooks, it represents the connected QuickBooks company/realm.
- `SyncJob` is the canonical asynchronous integration sync run record for manual, scheduled, retry, webhook-triggered, reconciliation, backfill, push, pull, and metadata refresh work.
- `SyncLog` is the canonical object-level sync result record emitted by `SyncJob`.
- `ExternalReference` is the canonical queryable mapping from internal source entity to external provider object and must be used with embedded `external_refs` on source records where applicable.
- QuickBooks-specific provider links are approved only for `QuickBooksCustomerLink`, `QuickBooksInvoiceLink`, and `QuickBooksItemLink`. Future phases must not create `QBCustomer`, `QBInvoice`, `QBItem`, or duplicated provider mirror entities unless a new global decision approves it.
- `QuickBooksCustomerLink` maps CRM `Account` and optional `Contact` context to QuickBooks Customer objects. It does not create a new Customer source entity.
- `QuickBooksInvoiceLink` maps `Order` to QuickBooks Invoice objects for Phase 13. Invoice creation ownership remains an Open Question because the platform may later introduce a dedicated billing/invoice source entity.
- `QuickBooksItemLink` maps `Product` to QuickBooks Item/Product/Service objects. It does not replace the Product catalog.
- `WebhookDelivery` is the canonical outbound webhook delivery attempt record. Phase 13 defines delivery observability and retry conventions; Phase 17 may expand public API/webhook endpoint management.
- QuickBooks is a sync integration, not the accounting ledger replacement and not the operational source of truth for CRM, orders, products, dispatch, field, service, inventory, or reporting records.
- Integration failures must never be silent. Failed, partially failed, stale, skipped, and retrying states must be visible to authorized admins and reportable.
- Provider credentials, tokens, refresh tokens, signing secrets, webhook secrets, and raw sensitive payload fields must never be stored or displayed in plaintext. Use `auth_reference`, `secret_ref`, and redacted payload previews.
- Integration actions must respect tenant isolation, company scoping, module enablement, RBAC, record permissions, export permissions, and future policy-based authorization.
- Integration monitoring and reporting must reuse Phase 12 `MetricDefinition`, `ReportRun`, `RollupSnapshot`, dashboards, and report conventions.
- Integration events must reuse Phase 03 `AuditLog`, `Notification`, `BackgroundJob`, `SavedView`, `SearchIndexRecord`, `ImportJob`, `ExportJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery` foundations.

## Entities Introduced

| Entity | Owner | Purpose | Future Phase Rule |
| --- | --- | --- | --- |
| `IntegrationConnection` | Integrations | Configured external provider connection. | Reuse for all provider connections. Do not create provider-specific connection duplicates. |
| `IntegrationAccount` | Integrations | External account/profile/realm under a connection. | Reuse for provider account contexts such as QuickBooks realm/company, telematics account, SMS account, or email workspace. |
| `SyncJob` | Integrations | Async sync execution record. | Reuse for all provider sync, backfill, retry, reconciliation, metadata refresh, and integration job observability. |
| `SyncLog` | Integrations | Object-level sync result. | Reuse for row/object-level provider results, errors, retries, and troubleshooting. |
| `ExternalReference` | Integrations | Queryable internal-to-external mapping. | Reuse for all external object mappings; combine with `external_refs` on source entities. |
| `QuickBooksCustomerLink` | Integrations / QuickBooks | Account/Contact to QuickBooks Customer mapping. | Do not create duplicate customer entities. |
| `QuickBooksInvoiceLink` | Integrations / QuickBooks | Order to QuickBooks Invoice mapping. | Reuse until a future approved billing source entity supersedes Order as invoice source. |
| `QuickBooksItemLink` | Integrations / QuickBooks | Product to QuickBooks Item mapping. | Do not duplicate Product catalog. |
| `WebhookDelivery` | Integrations | Outbound webhook delivery attempt. | Reuse for future API/webhooks phase and provider event delivery observability. |

## Fields Introduced

- Standard integration scope fields: `id`, `tenant_id`, `company_id`, `provider`, `connection_id`, `integration_account_id`, `created_at`, `created_by`, `updated_at`, `updated_by`, `archived_at`.
- `IntegrationConnection`: `provider_environment`, `auth_reference`, `scopes`, `status`, `health_status`, `sync_settings`, `last_sync_at`, `last_successful_sync_at`, `last_error_code`, `last_error_message`, `revoked_at`.
- `IntegrationAccount`: `external_account_id`, `external_realm_id`, `display_name`, `metadata`, `status`.
- `SyncJob`: `sync_type`, `direction`, `trigger_source`, `status`, `requested_by`, `started_at`, `completed_at`, `retry_count`, `idempotency_key`, `object_counts`, `error_summary`, `lock_key`.
- `SyncLog`: `sync_job_id`, `entity_type`, `entity_id`, `external_object_type`, `external_id`, `operation`, `status`, `error_code`, `error_message`, `attempt_count`, `occurred_at`.
- `ExternalReference`: `entity_type`, `entity_id`, `external_object_type`, `external_id`, `external_display_id`, `external_version`, `sync_status`, `status`, `last_synced_at`, `last_seen_external_at`, `deleted_at`.
- `QuickBooksCustomerLink`: `account_id`, `contact_id`, `quickbooks_customer_id`, `quickbooks_display_name`, `sync_status`, `last_synced_at`, `last_error_code`, `last_error_message`, `external_reference_id`.
- `QuickBooksInvoiceLink`: `order_id`, `quickbooks_invoice_id`, `quickbooks_doc_number`, `sync_status`, `invoice_sync_direction`, `amount_total`, `currency`, `last_synced_at`, `last_error_code`, `external_reference_id`.
- `QuickBooksItemLink`: `product_id`, `quickbooks_item_id`, `quickbooks_item_type`, `quickbooks_name`, `sync_status`, `last_synced_at`, `last_error_code`, `external_reference_id`.
- `WebhookDelivery`: `webhook_endpoint_id`, `event_type`, `source_entity_type`, `source_entity_id`, `payload_hash`, `status`, `attempt_count`, `next_retry_at`, `last_attempted_at`, `delivered_at`, `response_status_code`, `error_message`, `discarded_at`.

## APIs Introduced

- Integration connection admin APIs for connect/create, read, update settings, reconnect, revoke, archive, and health check.
- Integration account read APIs scoped under connections.
- Sync job APIs for list, read, start manual sync, retry job, and inspect job counts/errors.
- Sync log APIs for list, read, filter by job/entity/provider/status/error category, and object-level retry.
- External reference lookup APIs by internal entity, provider object, provider ID, object type, and connection.
- QuickBooks link APIs for customer, invoice, and item link visibility, stale marking, retry, and approved mapping override.
- Webhook delivery APIs for list, read, retry/replay where allowed, and redacted payload/error inspection.
- All integration APIs require stable error envelopes with `code`, `message`, `retryable`, `correlation_id`, and `resolution_category`.

## Permissions Introduced

- `integrations.connection.view`
- `integrations.connection.manage`
- `integrations.connection.secret.manage`
- `integrations.sync.view`
- `integrations.sync.run`
- `integrations.sync.retry`
- `integrations.sync.payload.view`
- `integrations.mapping.view`
- `integrations.mapping.manage`
- `integrations.quickbooks.view`
- `integrations.quickbooks.manage`
- `integrations.webhook_delivery.view`
- `integrations.webhook_delivery.retry`
- Exporting integration logs also requires relevant export permissions. Source-record visibility must still be respected.

## UX Patterns Introduced

- Settings > Integrations provider-card landing page.
- QuickBooks connect/reconnect/revoke setup flow with environment and permission explanation.
- Integration connection detail page with health, account, scopes, sync settings, recent jobs, unresolved errors, and audit summary.
- Sync Jobs table and detail views with status chips, filters, object counts, logs, retry controls, and error summaries.
- Mapping views for ExternalReference and QuickBooks customer/invoice/item links.
- QuickBooks readiness panels on Account, Order, and Product detail pages.
- Redacted payload preview drawer.
- Empty, disconnected, failed, stale, archived, and permission-denied states for integration screens.
- Saved views for failed invoices, stale customer links, failed item links, recent sync jobs, and unresolved provider errors.

## Reports or Dashboards Introduced

- Integration health dashboard.
- QuickBooks sync readiness dashboard.
- Sync job success/failure trend.
- Failed object sync report.
- Stale mapping report.
- Retry volume and retry success report.
- Connection uptime/degraded status report.
- QuickBooks customer, invoice, and item link coverage metrics.

## Notifications Introduced

- Connection disconnected or revoked.
- Authentication expired or reconnect required.
- Scheduled sync failed.
- Sync job partially failed above configured threshold.
- Manual action required for mapping conflict, stale link, or validation error.
- Repeated webhook delivery failures.
- Retry succeeded after previous failure.

## Audit Events Introduced

- `integration.connection.created`
- `integration.connection.connected`
- `integration.connection.updated`
- `integration.connection.reconnected`
- `integration.connection.revoked`
- `integration.connection.archived`
- `integration.connection.health_checked`
- `integration.sync_job.created`
- `integration.sync_job.started`
- `integration.sync_job.completed`
- `integration.sync_job.failed`
- `integration.sync_job.retried`
- `integration.sync_log.retried`
- `integration.external_reference.created`
- `integration.external_reference.updated`
- `integration.external_reference.marked_stale`
- `integration.external_reference.archived`
- `integration.quickbooks_customer_link.created`
- `integration.quickbooks_invoice_link.created`
- `integration.quickbooks_item_link.created`
- `integration.mapping.override`
- `integration.webhook_delivery.retried`
- `integration.payload_preview.viewed`

## Integrations Introduced

- QuickBooks Online as first accounting integration.
- Provider-neutral integration foundation for future email, SMS, WhatsApp, LinkedIn logging support, external calendar, telematics, API, webhooks, import/export, and integration marketplace work.
- Outbound webhook delivery observability pattern through `WebhookDelivery`.
- External reference and provider link conventions for all future integrations.

## Dependencies Created

- Depends on Phase 02 Tenant, Company, UserMembership, Role, Permission, module enablement, and backend permission enforcement.
- Depends on Phase 03 AuditLog, Notification, BackgroundJob, SavedView, SearchIndexRecord, ImportJob, ExportJob, ApiKey, WebhookEndpoint, WebhookDelivery, SettingsDocument, and secure shared services.
- Depends on Phase 04 Account, Contact, Activity, and CRM timeline for customer context.
- Depends on Phase 08 Product for QuickBooks item mapping.
- Depends on Phase 09 Order for QuickBooks invoice mapping.
- Depends on Phase 12 Reporting / Dashboards for integration health, rollups, metric definitions, and admin analytics.
- Creates conventions that Phase 14+ API/webhooks/import/export, admin/security, notifications/automation, rollout, and final blueprint must reuse.

## Constraints Future Phases Must Respect

- Do not expose MongoDB `_id` as public API ID.
- Do not store or display provider secrets in plaintext.
- Do not create provider-specific duplicate connection, job, log, or external mapping entities when Phase 13 entities cover the purpose.
- Do not create duplicate customer, invoice, item, product, or order source entities for QuickBooks sync without an approved global decision.
- Always include tenant and company scope in integration records and queries.
- Always use `ExternalReference` plus source-record `external_refs` for external IDs.
- Keep QuickBooks customer, invoice, and item mappings in approved link entities.
- Sync jobs and webhook deliveries must be asynchronous, retry-aware, auditable, and observable.
- All integration failures must be visible, permission-aware, reportable, and recoverable where possible.
- Reporting, API, webhook, notification, automation, admin, security, rollout, and final blueprint phases must reuse Phase 13 integration conventions.

## Open Questions Carried Forward

- Should Order remain the long-term source entity for QuickBooks invoices, or should a future dedicated BillingInvoice entity own invoice creation?
- Which QuickBooks object mappings beyond Customer, Invoice, and Item are required for MVP: payments, estimates, sales receipts, credit memos, tax codes, classes, locations, vendors, bills, or deposits?
- Which QuickBooks fields are mandatory per target customer accounting configuration, especially tax, class, location, income account, payment terms, and currency?
- Should QuickBooks sync be one-way push first, pull-first, or selective bidirectional for customer/item updates?
- What are the exact retention periods for SyncLog and WebhookDelivery payload metadata?
- What provider secret storage service will be used in production?
- What exact ID generation format will be used for integration entities: ULID, UUIDv7, KSUID, or another opaque sortable ID?
