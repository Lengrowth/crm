# Summary for Future Phases

## Final Decisions Made

- Phase 03 defines the shared Core Platform foundation that every later module must consume.
- Core Platform owns AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, ApiKey, WebhookEndpoint, WebhookDelivery, SettingsDocument, and BackgroundJob foundations.
- Future modules must extend these shared services instead of creating duplicate service-specific audit logs, notifications, files, tags, custom fields, saved views, imports, exports, API credentials, webhooks, settings, or job frameworks.
- All shared services must respect Tenant, Company, UserMembership, Role, Permission, and module enablement rules from Phase 02.
- All company-scoped platform records must carry `tenant_id` and `company_id` unless explicitly platform/tenant/user scoped.
- MongoDB `_id` must not be exposed as a public API identifier.
- External IDs must be stored in `external_refs` or approved provider link entities.
- AuditLog is append-only and compliance/admin oriented; user-facing activity timelines are separate but may be derived from or linked to operational events.
- Notification is the canonical in-app notification model; email is optional/recommended for job completion and admin-critical events; SMS and push are future-capable.
- FileAttachment is the canonical file/photo/document/proof/import/export file model.
- TagAssignment is recommended as a separate collection/entity rather than embedding tags directly on every record.
- Custom fields may extend records but must not replace stable required fields needed for workflow, permissions, reporting, search, sync, or integrations.
- SavedView stores reusable filters, columns, sorting, grouping, search query, view type, and visibility.
- Global search must be tenant/company/module/permission aware and must not reveal disabled-module or soft-deleted records to unauthorized users.
- ImportJob and ExportJob are the required async frameworks for large or long-running bulk data work.
- ApiKey and WebhookEndpoint are foundations for later public API and integration phases; raw keys/secrets must never be stored in plaintext.
- Background jobs must expose status, retry/error state, idempotency expectations, and admin-visible observability.

## Entities Introduced

| Entity | Purpose | Owner | Scope | Future Phase Rule |
| --- | --- | --- | --- | --- |
| AuditLog | Canonical append-only audit event record. | Core Platform | Tenant/company where applicable | Every future phase must register audit events here. |
| Notification | Recipient-facing notification record. | Core Platform | Tenant/company/user/membership | Later phases define module-specific triggers. |
| FileAttachment | Canonical file/photo/document attachment. | Core Platform | Tenant/company/record | Future modules use this instead of separate photo/document entities unless wrapper required. |
| Tag | Controlled reusable label. | Core Platform | Company/module | Used by filtering, reporting, and segmentation. |
| TagAssignment | Assignment of a Tag to a target record. | Core Platform | Company/record | Recommended separate collection for consistency. |
| CustomFieldDefinition | Configuration for a custom field. | Core Platform | Company/module/entity | Future phases must not use custom fields for stable core fields. |
| CustomFieldValue | Value of a field on a record. | Core Platform | Company/record | Supports search, filters, imports, exports, reports. |
| SavedView | Saved filter/view configuration. | Core Platform | Company/user/team/shared | Phase 18 expands behavior. |
| SearchIndexRecord | Search abstraction for records. | Core Platform | Tenant/company/module | May start in MongoDB or move to search service. |
| ImportJob | Async import process. | Core Platform | Tenant/company/module/entity | All module imports use this framework. |
| ExportJob | Async export process. | Core Platform | Tenant/company/module/entity | All module exports use this framework. |
| ApiKey | Scoped credential record. | Core Platform / Integrations | Tenant/company | Expanded by Phase 17. |
| WebhookEndpoint | Subscriber endpoint configuration. | Core Platform / Integrations | Company | Expanded by Phase 17. |
| WebhookDelivery | Attempted webhook event delivery. | Core Platform / Integrations | Company | Supports delivery health reporting. |
| SettingsDocument | Settings at platform, tenant, company, module, or user level. | Core Platform | Platform/tenant/company/module/user | All modules consume settings hierarchy. |
| BackgroundJob | Operational async job status wrapper. | Core Platform | Tenant/company where applicable | Future phases use this pattern for long-running work. |


## Fields Introduced

### Shared Field Standards

| Field | Type | Requirement | Purpose |
| --- | --- | --- | --- |
| id | string | Yes | Stable application identifier exposed through APIs. MongoDB `_id` must never be exposed as the public contract. |
| tenant_id | string | Required for tenant-owned data | Top-level SaaS isolation boundary. |
| company_id | string | Required for company records | Company scope inside the tenant. |
| created_at | datetime | Yes | UTC timestamp for creation. |
| created_by | ActorReference / user id | Recommended/required for mutable records | Actor that created the record; system actors allowed. |
| updated_at | datetime | Required for mutable records | UTC timestamp for last update. |
| updated_by | ActorReference / user id | Required for mutable records | Actor that last updated the record. |
| deleted_at | datetime | Conditional | Soft-delete timestamp for major configurable/business records. |
| deleted_by | ActorReference / user id | Conditional | Actor that soft-deleted the record. |
| status | enum/string | Conditional | Primary lifecycle state. |
| source | enum/string | Recommended | Origin such as `manual`, `import`, `api`, `integration`, `mobile_offline`, or `system`. |
| external_refs | object | Recommended | Provider IDs and external references; provider-specific IDs must not become top-level ad hoc fields. |
| metadata | object | Recommended | Non-critical extension metadata; must not store required workflow, permission, or reporting data. |


### Important Entity Field Groups

- `AuditLog`: `id`, `tenant_id`, `company_id`, `event_key`, `event_category`, `severity`, `actor`, `target`, `action`, `before`, `after`, `metadata`, `ip_address`, `user_agent`, `created_at`.
- `Notification`: `id`, `tenant_id`, `company_id`, `recipient_user_id`, `recipient_membership_id`, `type`, `channel`, `title`, `body`, `target`, `status`, `read_at`, `delivered_at`, `failed_at`, `failure_reason`, `created_at`, `metadata`.
- `FileAttachment`: `id`, `tenant_id`, `company_id`, `record_type`, `record_id`, `uploaded_by`, `filename`, `original_filename`, `mime_type`, `size_bytes`, `storage_provider`, `storage_key`, `checksum`, `status`, `visibility`, `created_at`, `deleted_at`, `metadata`.
- `Tag`: `id`, `tenant_id`, `company_id`, `name`, `slug`, `color`, `description`, `module_scope`, `status`, `created_at`, `created_by`, `updated_at`, `updated_by`, `metadata`.
- `TagAssignment`: `id`, `tenant_id`, `company_id`, `tag_id`, `record_type`, `record_id`, `assigned_by`, `created_at`, `metadata`.
- `CustomFieldDefinition`: `id`, `tenant_id`, `company_id`, `module_key`, `entity_type`, `field_key`, `label`, `description`, `field_type`, `is_required`, `is_filterable`, `is_reportable`, `options`, `validation`, `default_value`, `status`, `created_at`, `created_by`, `updated_at`, `updated_by`, `metadata`.
- `CustomFieldValue`: `id`, `tenant_id`, `company_id`, `field_definition_id`, `record_type`, `record_id`, `value`, `value_type`, `created_at`, `updated_at`, `metadata`.
- `SavedView`: `id`, `tenant_id`, `company_id`, `owner_user_id`, `module_key`, `entity_type`, `name`, `view_type`, `visibility`, `filters`, `sort`, `columns`, `group_by`, `search_query`, `is_default`, `status`, `created_at`, `updated_at`, `metadata`.
- `SearchIndexRecord`: `id`, `tenant_id`, `company_id`, `record_type`, `record_id`, `module_key`, `title`, `subtitle`, `keywords`, `status`, `owner_user_id`, `updated_at`, `metadata`.
- `ImportJob`: `id`, `tenant_id`, `company_id`, `module_key`, `entity_type`, `status`, `source_type`, `file_attachment_id`, `mapping`, `total_rows`, `processed_rows`, `success_rows`, `failed_rows`, `error_summary`, `started_at`, `completed_at`, `created_by`, `created_at`, `metadata`.
- `ExportJob`: `id`, `tenant_id`, `company_id`, `module_key`, `entity_type`, `status`, `format`, `filters`, `columns`, `file_attachment_id`, `total_rows`, `started_at`, `completed_at`, `expires_at`, `created_by`, `created_at`, `metadata`.
- `ApiKey`: `id`, `tenant_id`, `company_id`, `name`, `key_prefix`, `key_hash`, `scopes`, `status`, `created_by`, `created_at`, `expires_at`, `last_used_at`, `revoked_at`, `revoked_by`, `metadata`.
- `WebhookEndpoint`: `id`, `tenant_id`, `company_id`, `name`, `url`, `event_keys`, `secret_hash`, `status`, `created_by`, `created_at`, `updated_at`, `last_success_at`, `last_failure_at`, `metadata`.
- `WebhookDelivery`: `id`, `tenant_id`, `company_id`, `webhook_endpoint_id`, `event_key`, `payload`, `status`, `attempt_count`, `last_attempt_at`, `next_retry_at`, `response_status`, `response_body_excerpt`, `created_at`, `metadata`.
- `SettingsDocument`: `id`, `tenant_id`, `company_id`, `scope`, `module_key`, `owner_user_id`, `settings`, `version`, `created_at`, `updated_at`, `updated_by`, `metadata`.
- `BackgroundJob`: `id`, `tenant_id`, `company_id`, `job_type`, `related_record`, `status`, `priority`, `attempts`, `max_attempts`, `idempotency_key`, `queued_at`, `started_at`, `completed_at`, `failed_at`, `error_summary`, `created_by`, `metadata`.

## APIs Introduced

| ID | Endpoint | Method | Purpose | Permission |
| --- | --- | --- | --- | --- |
| API-03-001 | GET /api/v1/core/audit-logs | GET | List filtered audit logs | core.audit_log.view |
| API-03-002 | POST /api/v1/core/audit-logs/export | POST | Create audit log export job | core.audit_log.export |
| API-03-003 | GET /api/v1/core/notifications | GET | List current user notifications | core.notification.view |
| API-03-004 | POST /api/v1/core/notifications/{notification_id}/read | POST | Mark notification read | core.notification.view |
| API-03-005 | POST /api/v1/core/files | POST | Upload file attachment | core.file.upload |
| API-03-006 | GET /api/v1/core/files/{file_id}/download | GET | Download file | core.file.view |
| API-03-007 | DELETE /api/v1/core/files/{file_id} | DELETE | Soft-delete file attachment | core.file.delete |
| API-03-008 | GET /api/v1/core/tags | GET | List tags | core.search.use or module access |
| API-03-009 | POST /api/v1/core/tags | POST | Create tag | core.tag.manage |
| API-03-010 | POST /api/v1/core/tag-assignments | POST | Assign tag to record | core.tag.assign |
| API-03-011 | DELETE /api/v1/core/tag-assignments/{assignment_id} | DELETE | Remove tag assignment | core.tag.assign |
| API-03-012 | GET /api/v1/core/custom-fields | GET | List field definitions | record/module access |
| API-03-013 | POST /api/v1/core/custom-fields | POST | Create field definition | core.custom_field.manage_definitions |
| API-03-014 | PATCH /api/v1/core/custom-field-values | PATCH | Upsert custom field values for a record | core.custom_field.edit_values |
| API-03-015 | GET /api/v1/core/saved-views | GET | List saved views | record/module access |
| API-03-016 | POST /api/v1/core/saved-views | POST | Create saved view | core.saved_view.manage_own |
| API-03-017 | GET /api/v1/core/search | GET | Global search | core.search.use |
| API-03-018 | POST /api/v1/core/import-jobs | POST | Create import job | core.import.run |
| API-03-019 | POST /api/v1/core/import-jobs/{job_id}/preview | POST | Validate and preview import | core.import.run |
| API-03-020 | POST /api/v1/core/import-jobs/{job_id}/run | POST | Run import job | core.import.run |
| API-03-021 | POST /api/v1/core/export-jobs | POST | Create export job | core.export.run |
| API-03-022 | GET /api/v1/core/export-jobs/{job_id}/download | GET | Download export result | core.export.run |
| API-03-023 | POST /api/v1/core/api-keys | POST | Create API key | core.api_key.manage |
| API-03-024 | POST /api/v1/core/api-keys/{api_key_id}/revoke | POST | Revoke API key | core.api_key.manage |
| API-03-025 | POST /api/v1/core/webhook-endpoints | POST | Create webhook endpoint | core.webhook.manage |
| API-03-026 | PATCH /api/v1/core/webhook-endpoints/{endpoint_id} | PATCH | Update webhook endpoint | core.webhook.manage |
| API-03-027 | GET /api/v1/core/webhook-deliveries | GET | List webhook deliveries | core.webhook.manage |
| API-03-028 | POST /api/v1/core/webhook-deliveries/{delivery_id}/retry | POST | Retry delivery | core.webhook.manage |
| API-03-029 | GET /api/v1/core/settings | GET | Read settings | authenticated user / admin depending level |
| API-03-030 | PATCH /api/v1/core/settings | PATCH | Update settings | core.settings.manage_company or user ownership |
| API-03-031 | GET /api/v1/core/background-jobs/{job_id} | GET | Get background job status | core.background_job.view |


## Permissions Introduced

| ID | Permission Key | Description | Default Roles | Scope | Audit Required? | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| PERM-03-001 | core.audit_log.view | View audit logs | Company Admin, Super Admin | Tenant/company | No | Must enforce company scope. |
| PERM-03-002 | core.audit_log.export | Export audit logs | Company Admin, Super Admin | Tenant/company | Yes | Sensitive fields must remain masked. |
| PERM-03-003 | core.notification.view | View own notifications | All authenticated users | User/company | No | Users only see notifications for permitted memberships. |
| PERM-03-004 | core.notification.manage_settings | Manage notification settings | Company Admin for company settings; user for personal settings | User/company | Yes for company settings | Role/team preferences are future-capable. |
| PERM-03-005 | core.file.upload | Upload files | Company Admin, managers, authorized operators, field roles | Company/record | Yes | Record access is required. |
| PERM-03-006 | core.file.view | View files | Users with record view permission | Company/record | No | Must check target record permission. |
| PERM-03-007 | core.file.delete | Delete files | Company Admin, owner, authorized managers | Company/record | Yes | Soft delete baseline. |
| PERM-03-008 | core.tag.manage | Create, rename, merge, archive tags | Company Admin, module manager | Company/module | Yes | Avoid uncontrolled tag sprawl. |
| PERM-03-009 | core.tag.assign | Assign or remove tags | Authorized module users | Company/record | Yes when material | Requires target record access. |
| PERM-03-010 | core.custom_field.manage_definitions | Manage custom field definitions | Company Admin, configured module admin | Company/module/entity | Yes | Must validate existing values before breaking changes. |
| PERM-03-011 | core.custom_field.edit_values | Edit custom field values | Users with edit access to target record | Company/record | Conditional | Sensitive or reportable values should audit. |
| PERM-03-012 | core.saved_view.manage_own | Create and manage personal saved views | All authenticated users | User/company/module | No | Must not leak data through filters. |
| PERM-03-013 | core.saved_view.share | Share saved views | Company Admin, managers | Company/team/module | Yes | Shared view visibility must be permission-aware. |
| PERM-03-014 | core.import.run | Run imports | Company Admin, authorized data manager | Company/module/entity | Yes | Large imports run as jobs. |
| PERM-03-015 | core.export.run | Run exports | Company Admin, authorized analyst/manager | Company/module/entity | Yes | Exports are sensitive data extraction. |
| PERM-03-016 | core.api_key.manage | Manage API keys | Company Admin, integration admin, Super Admin where applicable | Tenant/company | Yes | Raw key displayed once only. |
| PERM-03-017 | core.webhook.manage | Manage webhook endpoints | Company Admin, integration admin | Company | Yes | Endpoint URL, events, and secret changes audited. |
| PERM-03-018 | core.background_job.view | View background jobs | Company Admin, Super Admin, authorized ops/admin roles | Tenant/company | No | Details must respect data sensitivity. |
| PERM-03-019 | core.settings.manage_company | Manage company settings | Company Admin | Company | Yes | Includes timezone, locale, module settings, limits. |
| PERM-03-020 | core.search.use | Use global search | All authenticated users | User/company/module | No | Results filtered by tenant, company, module, and record permissions. |


## UX Patterns Introduced

- Core admin layout for settings, audit logs, background jobs, imports, exports, files, API keys, and webhooks.
- Notification center with unread/read states and target-record links.
- File attachment component with upload progress, preview/download/delete controls, and permission states.
- Tag picker with controlled company/module tags.
- Custom field renderer for forms, detail pages, filters, imports, exports, and mobile-compatible forms.
- Saved view selector supporting personal and future shared views.
- Import wizard with upload, mapping, validation/preview, run, progress, and error-row review.
- Export action with format/column/filter confirmation and async job status.
- Global search entry point with type/module filters and permission-aware results.
- Shared empty, loading, error, disabled-module, and permission-denied states.

## Reports or Dashboards Introduced

- No final reporting dashboard is implemented in Phase 03.
- Phase 03 must capture data for future reports on audit event counts, file usage, import/export job status, webhook health, API key usage, notification delivery, search usage, saved view adoption, custom field adoption, tag usage, and admin activity.

## Notifications Introduced

| ID | Event Key | Name | Channels | Recipients | Target | Purpose | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NOTIF-03-001 | core.import.completed | Import completed | In-app baseline; email optional | ImportJob creator and optionally admins | ImportJob | Import completed successfully | Permission-aware link to job summary. |
| NOTIF-03-002 | core.import.completed_with_errors | Import completed with errors | In-app baseline; email optional | ImportJob creator and optionally admins | ImportJob | Import completed with failed rows | Includes counts and error file link if permitted. |
| NOTIF-03-003 | core.export.ready | Export ready | In-app baseline; email optional | ExportJob creator | ExportJob/FileAttachment | Export is ready to download | Download requires permission recheck. |
| NOTIF-03-004 | core.export.failed | Export failed | In-app baseline | ExportJob creator | ExportJob | Export failed | Shows safe error summary. |
| NOTIF-03-005 | core.webhook.disabled | Webhook disabled due to failures | In-app baseline; email recommended | Integration admins and Company Admins | WebhookEndpoint | Webhook endpoint was disabled | Includes endpoint name and last failure summary. |
| NOTIF-03-006 | core.api_key.created | API key created | In-app baseline | Integration admins / creator | ApiKey | API key created | Security-sensitive; never includes raw key. |
| NOTIF-03-007 | core.api_key.revoked | API key revoked | In-app baseline | Integration admins / creator | ApiKey | API key revoked | Includes revocation actor and timestamp. |
| NOTIF-03-008 | core.file.upload_failed | File upload failed | In-app baseline | Uploading user | FileAttachment | File upload failed | Includes retry guidance where safe. |
| NOTIF-03-009 | core.mention.created | Mention/comment notification | Future-capable | Mentioned user | Target record | You were mentioned | Detailed comment model defined later. |
| NOTIF-03-010 | core.settings.changed | Sensitive settings changed | Recommended for admin/security settings | Company Admins / Super Admin as appropriate | SettingsDocument | Settings changed | Avoid noisy notifications for routine personal preferences. |


## Audit Events Introduced

| Event Key | Actor | Target | Scope | Required Metadata | Severity | Retention | Company Admin Visible? | Super Admin Visible? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| core.file.uploaded | actor | FileAttachment | Tenant/company/record | file_id, record_type, record_id, mime_type, size_bytes | info | Standard audit retention | Yes | Yes |
| core.file.deleted | actor | FileAttachment | Tenant/company/record | file_id, record_type, record_id, reason | warning | Standard audit retention | Yes | Yes |
| core.tag.created | actor | Tag | Company/module | tag_id, name, module_scope | info | Standard audit retention | Yes | Yes |
| core.tag.updated | actor | Tag | Company/module | tag_id, before, after | info | Standard audit retention | Yes | Yes |
| core.tag.deleted | actor | Tag | Company/module | tag_id, assignment_count | warning | Standard audit retention | Yes | Yes |
| core.tag.assigned | actor | TagAssignment | Company/record | tag_id, record_type, record_id | info | Standard audit retention | Yes | Yes |
| core.tag.removed | actor | TagAssignment | Company/record | tag_id, record_type, record_id | info | Standard audit retention | Yes | Yes |
| core.custom_field_definition.created | actor | CustomFieldDefinition | Company/module/entity | field_definition_id, field_key, field_type | info | Standard audit retention | Yes | Yes |
| core.custom_field_definition.updated | actor | CustomFieldDefinition | Company/module/entity | field_definition_id, before, after | warning | Standard audit retention | Yes | Yes |
| core.custom_field_value.changed | actor | CustomFieldValue | Company/record | field_definition_id, record_type, record_id, masked before/after if sensitive | info/warning | Standard audit retention | Conditional | Yes |
| core.saved_view.created | actor | SavedView | Company/user/module | saved_view_id, view_type, visibility | info | Standard audit retention | Conditional | Yes |
| core.saved_view.shared | actor | SavedView | Company/module | saved_view_id, visibility, shared_with | info | Standard audit retention | Yes | Yes |
| core.saved_view.deleted | actor | SavedView | Company/user/module | saved_view_id | info | Standard audit retention | Conditional | Yes |
| core.import_job.created | actor | ImportJob | Company/module/entity | import_job_id, entity_type, source_type | info | Standard audit retention | Yes | Yes |
| core.import_job.completed | system/background_job | ImportJob | Company/module/entity | import_job_id, success_rows, failed_rows | info/warning | Standard audit retention | Yes | Yes |
| core.export_job.created | actor | ExportJob | Company/module/entity | export_job_id, entity_type, filters summary | warning | Standard audit retention | Yes | Yes |
| core.export_job.downloaded | actor | ExportJob/FileAttachment | Company/module/entity | export_job_id, file_attachment_id | warning | Standard audit retention | Yes | Yes |
| core.api_key.created | actor | ApiKey | Tenant/company | api_key_id, key_prefix, scopes, expires_at | warning | Extended security retention recommended | Yes | Yes |
| core.api_key.revoked | actor | ApiKey | Tenant/company | api_key_id, key_prefix, reason | warning | Extended security retention recommended | Yes | Yes |
| core.webhook_endpoint.created | actor | WebhookEndpoint | Company | endpoint_id, url host, event_keys | warning | Standard audit retention | Yes | Yes |
| core.webhook_endpoint.updated | actor | WebhookEndpoint | Company | endpoint_id, before, after | warning | Standard audit retention | Yes | Yes |
| core.webhook_endpoint.disabled | system/background_job | WebhookEndpoint | Company | endpoint_id, failure_count, last_failure | error | Standard audit retention | Yes | Yes |
| core.settings.changed | actor | SettingsDocument | Platform/tenant/company/user | scope, module_key, changed_keys, before/after masked | warning | Extended retention for security settings | Yes | Yes |
| core.background_job.failed | system/background_job | BackgroundJob | Tenant/company where applicable | job_id, job_type, error_summary | error | Standard audit retention | Yes | Yes |


## Integrations Introduced

- ApiKey foundation for later public API and integration access.
- WebhookEndpoint and WebhookDelivery foundation for later outbound event subscriptions.
- ImportJob and ExportJob foundations for CSV/Excel and future integration-driven data movement.
- Integration actors must use the ActorReference standard.
- Webhook payloads must include tenant/company context where appropriate and must not leak unauthorized or sensitive data.
- QuickBooks and future integrations must reuse background job, audit, notification, external reference, webhook, and error visibility conventions.

## Dependencies Created

- Phase 04 depends on files, tags, custom fields, audit logs, saved views, and search foundation for CRM records.
- Phase 05 depends on notifications, audit logs, saved views, import/export, and activity/timeline conventions.
- Phase 06 depends on notifications and reminders foundation.
- Phase 07 depends on file attachments/photos, audit logs, notifications, and mobile-compatible upload patterns.
- Phase 08 depends on audit logs, import/export, files, tags, custom fields, and background jobs.
- Phase 09 depends on notifications, audit logs, saved views, files, and background jobs.
- Phase 10 depends on audit logs, notifications, background jobs, and search/index patterns.
- Phase 11 depends on file attachments, audit logs, notifications, and saved views.
- Phase 12 depends on audit, job, search, saved view, and metadata foundations.
- Phase 13 depends on API keys, webhooks, background jobs, audit logs, notifications, and external references.
- Phase 14 depends on file upload retry, offline-compatible audit/timeline creation, and background job conventions.
- Phase 15 depends on audit logs, settings, security controls, and admin observability.
- Phase 16 expands notifications and automation.
- Phase 17 expands API keys, webhooks, import, and export.
- Phase 18 expands search, filters, and custom views.
- Phase 19 depends on background jobs, audit, import/export, and operational observability.
- Phase 20 consolidates all platform foundations.

## Constraints Future Phases Must Respect

- Do not create duplicate module-specific replacements for shared Phase 03 services.
- Do not expose MongoDB `_id` through public APIs.
- Do not store raw API keys or webhook secrets in plaintext.
- Do not bypass backend permission checks; frontend hiding is not enough.
- Do not allow global search, saved views, exports, files, notifications, imports, or webhooks to leak cross-company or disabled-module data.
- Do not use custom fields for stable fields required by workflow, permissions, reporting, sync, audit, or integrations.
- Do not treat AuditLog as the user-facing CRM Activity model; keep internal audit and operational timeline concerns distinct.
- Do not make long-running import/export/webhook/search/report/sync work run only inside request/response calls.
- Do not create provider-specific top-level fields for external IDs; use `external_refs` or approved link entities.
- Do not create module APIs without audit, notification, search, saved view, import/export, file, tag, and custom field impact analysis.

## Open Questions Carried Forward

- Should TagAssignment be a separate collection or embedded on records? Recommended: separate collection for consistency and queryability.
- Should SearchIndexRecord be stored in MongoDB initially or delegated to a search service later?
- Which file storage provider should be used first?
- Should file virus scanning be mandatory at MVP?
- Should custom fields support formula fields in the future?
- Should shared company-level saved views require admin approval?
- Should exports have row limits by plan or role?
- Should API keys be available in MVP or only prepared for Phase 17?
- Should webhooks be available in MVP or only prepared for Phase 17?
- Should notification preferences be user-level only or also role/team-level?
- Should audit log retention be configurable by company?
- Should background jobs be managed by Celery from day one or abstracted first?
