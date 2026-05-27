# Summary for Future Phases

## Final Decisions Made

- Phase 04 establishes CRM as the canonical customer/prospect/revenue foundation for later platform phases.
- `Account` is the canonical CRM business/customer/prospect/vendor record and must not be replaced by `Customer`, `Client`, `CRMCompany`, or another duplicate concept.
- `Company` remains the SaaS customer organization inside a `Tenant`; `Account` remains a CRM/operational business record.
- `Contact` is the canonical person record and may relate to one or more Accounts.
- `Lead` is the canonical unqualified or early-stage sales record and may convert into Account, Contact, and Opportunity.
- `Opportunity` is the canonical potential revenue/work record and must connect to Account, Pipeline, and PipelineStage.
- `Pipeline` and `PipelineStage` are company-scoped CRM configuration records, not activity records.
- `Activity` is the canonical CRM/timeline activity record for calls, emails, SMS, meetings, LinkedIn logs, notes, site visits, tasks, status changes, and system events, but it must not replace specialized operational event records in later phases.
- `Note` and `Comment` support collaboration and can appear on timelines, but they are not substitutes for audit logs or operational source-of-truth events.
- `RelationshipMap` is a structured graph document, recommended per Account for MVP, using Account and Contact IDs where possible.
- `AssignmentRule` is a reusable company-scoped rule configuration owned by Core Platform / CRM Automation and must be reusable by outbound, field, service, task, and job-request phases.
- All CRM records must respect `tenant_id`, `company_id`, module enablement, UserMembership, Role, Permission, and future policy-based authorization rules.
- CRM uses Core Platform foundations for AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, ApiKey/Webhook foundations, SettingsDocument, and BackgroundJob.
- CRM imports and exports must use ImportJob and ExportJob.
- CRM exports, merges, conversions, assignment changes, status changes, and admin configuration changes must be audited.
- Phase 05 Outbound Sales must build on Lead, Contact, Account, Opportunity, Activity, and AssignmentRule.
- Later field, dispatch, service, reporting, and integration phases must reuse Account/Contact/Opportunity instead of inventing customer entities.

## Entities Introduced

| Entity | Owner | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `Account` | CRM | Company-scoped, optional branch context | Canonical CRM business/customer/prospect/vendor record. Not Tenant or Company. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Contact` | CRM | Company-scoped, optional branch context | Person related to one or more Accounts, Leads, Opportunities, Activities, and later field/service records. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Lead` | CRM | Company-scoped, optional branch context | Unqualified or early-stage sales record requiring qualification and possible conversion. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Opportunity` | CRM | Company-scoped, optional branch context | Potential revenue or work opportunity tied to Account, pipeline, stage, value, probability, and next action. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Pipeline` | CRM | Company-scoped configuration | Company-configurable sales process container. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `PipelineStage` | CRM | Company-scoped child configuration of Pipeline | Ordered stage inside a Pipeline with default probability and stage type. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Activity` | CRM / Timeline | Company-scoped, linked to one or more records | Unified timeline record for calls, emails, SMS, meetings, LinkedIn logs, notes, site visits, tasks, status changes, and system events. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Note` | Core Platform / CRM collaboration | Company-scoped, linked to one target record | Standalone text note associated with a CRM or operational record; can produce an Activity timeline entry. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `Comment` | Core Platform / Collaboration | Company-scoped, linked to one target record | Threaded or contextual collaboration comment on a record, task, attachment, or activity. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `RelationshipMap` | CRM | Company-scoped, usually per Account | Structured account/contact stakeholder map with nodes, edges, influence, hierarchy, and relationship context. | Reuse this canonical entity; do not create synonyms or duplicates. |
| `AssignmentRule` | Core Platform / CRM Automation | Company-scoped configuration | Reusable rule for assigning leads, accounts, tasks, job requests, or work to users/teams. | Reuse this canonical entity; do not create synonyms or duplicates. |

## Fields Introduced

| Entity | Key fields |
| --- | --- |
| `Account` | `id`, `tenant_id`, `company_id`, `branch_id`, `name`, `display_name`, `type`, `lifecycle_stage`, `status`, `owner_user_id`, `assigned_team_id`, `industry`, `address`, `coordinates`, `website`, `main_phone`, `main_email`, `billing_contact_id`, `primary_contact_id`, `source`, `tags`, `external_refs`, `metadata`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Contact` | `id`, `tenant_id`, `company_id`, `account_ids`, `primary_account_id`, `first_name`, `last_name`, `full_name`, `role_title`, `department`, `emails`, `phones`, `influence_level`, `decision_role`, `relationship_status`, `status`, `owner_user_id`, `do_not_contact_reason`, `preferred_channel`, `source`, `external_refs`, `metadata`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Lead` | `id`, `tenant_id`, `company_id`, `account_id`, `contact_id`, `source`, `source_detail`, `status`, `qualification_status`, `owner_user_id`, `assigned_team_id`, `score`, `priority`, `company_name`, `contact_name`, `email`, `phone`, `industry`, `territory`, `estimated_value`, `interest_summary`, `next_action_at`, `converted_account_id`, `converted_contact_id`, `converted_opportunity_id`, `converted_at`, `unqualified_reason`, `source`, `external_refs`, `metadata`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Opportunity` | `id`, `tenant_id`, `company_id`, `account_id`, `contact_ids`, `lead_id`, `pipeline_id`, `stage_id`, `name`, `status`, `value_amount`, `currency`, `probability`, `expected_close_date`, `actual_close_date`, `lost_reason`, `won_reason`, `owner_user_id`, `assigned_team_id`, `next_action_at`, `source`, `products_summary`, `job_request_id later`, `external_refs`, `metadata`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Pipeline` | `id`, `tenant_id`, `company_id`, `name`, `type`, `description`, `status`, `sort_order`, `is_default`, `allowed_entity_types`, `settings`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `PipelineStage` | `id`, `tenant_id`, `company_id`, `pipeline_id`, `name`, `description`, `sort_order`, `stage_type`, `probability_default`, `is_won_stage`, `is_lost_stage`, `requires_reason`, `status`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Activity` | `id`, `tenant_id`, `company_id`, `activity_type`, `activity_subtype`, `subject`, `body_preview`, `occurred_at`, `actor_user_id`, `owner_user_id`, `direction`, `outcome`, `linked_entities`, `primary_entity_type`, `primary_entity_id`, `source`, `source_ref`, `visibility`, `status`, `corrected_activity_id`, `metadata`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Note` | `id`, `tenant_id`, `company_id`, `entity_type`, `entity_id`, `body`, `visibility`, `pinned`, `status`, `activity_id`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `Comment` | `id`, `tenant_id`, `company_id`, `entity_type`, `entity_id`, `parent_comment_id`, `body`, `status`, `edited_at`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `RelationshipMap` | `id`, `tenant_id`, `company_id`, `account_id`, `nodes`, `edges`, `version`, `status`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |
| `AssignmentRule` | `id`, `tenant_id`, `company_id`, `name`, `description`, `entity_type`, `conditions`, `assignment_strategy`, `assignment_target_type`, `assignment_target_id`, `fallback_target_type`, `fallback_target_id`, `priority`, `status`, `effective_from`, `effective_to`, `last_evaluated_at`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `deleted_at`, `deleted_by_user_id` |

## APIs Introduced

| API ID | Conceptual API |
| --- | --- |
| API-04-001 | GET /api/v1/accounts: list Accounts with permission-aware filters, search, saved view input, pagination, sorting, and optional includes. |
| API-04-002 | POST /api/v1/accounts: create Account with tenant/company scope from session, duplicate warning support, and custom fields/tags payloads. |
| API-04-003 | GET /api/v1/accounts/{account_id}: read Account detail with permission-aware related record summaries. |
| API-04-004 | PATCH /api/v1/accounts/{account_id}: update allowed Account fields with optimistic concurrency metadata. |
| API-04-005 | POST /api/v1/accounts/{account_id}/archive and POST /api/v1/accounts/{account_id}/restore: lifecycle actions where permitted. |
| API-04-006 | POST /api/v1/accounts/merge: merge duplicate Accounts with relationship reassignment and audit log. |
| API-04-007 | GET/POST/PATCH /api/v1/contacts and GET/PATCH /api/v1/contacts/{contact_id}: Contact CRUD and account association management. |
| API-04-008 | POST /api/v1/contacts/merge: merge duplicate Contacts with Account relationship preservation. |
| API-04-009 | GET/POST/PATCH /api/v1/leads and GET /api/v1/leads/{lead_id}: Lead CRUD, qualification fields, ownership, scoring, and source filters. |
| API-04-010 | POST /api/v1/leads/{lead_id}/qualify: mark Lead qualified without necessarily converting immediately. |
| API-04-011 | POST /api/v1/leads/{lead_id}/unqualify: set unqualified state with reason. |
| API-04-012 | POST /api/v1/leads/{lead_id}/convert: convert into Account, Contact, and/or Opportunity with duplicate resolution choices. |
| API-04-013 | GET/POST/PATCH /api/v1/opportunities and GET /api/v1/opportunities/{opportunity_id}: Opportunity CRUD and list workflows. |
| API-04-014 | POST /api/v1/opportunities/{opportunity_id}/move-stage: move stage with validation, probability updates, and audit. |
| API-04-015 | POST /api/v1/opportunities/{opportunity_id}/mark-won and /mark-lost: close opportunity with required reason fields where configured. |
| API-04-016 | GET/POST/PATCH /api/v1/pipelines and GET/POST/PATCH /api/v1/pipelines/{pipeline_id}/stages: manage company CRM pipeline configuration. |
| API-04-017 | POST /api/v1/pipelines/{pipeline_id}/stages/reorder: reorder stages with validation against active Opportunities. |
| API-04-018 | GET/POST/PATCH /api/v1/activities and GET /api/v1/activities/{activity_id}: Activity list, log, correction, archive, and timeline APIs. |
| API-04-019 | GET /api/v1/timeline: generic timeline endpoint accepting entity_type and entity_id, returning permission-filtered Activity, Note, Comment, and related system events. |
| API-04-020 | GET/POST/PATCH /api/v1/notes and GET/POST/PATCH /api/v1/comments: collaboration endpoints for supported records. |
| API-04-021 | GET/PUT /api/v1/accounts/{account_id}/relationship-map: retrieve and replace/update structured RelationshipMap with version checking. |
| API-04-022 | GET/POST/PATCH /api/v1/assignment-rules and POST /api/v1/assignment-rules/evaluate: configure and test rule evaluation. |
| API-04-023 | POST /api/v1/crm/bulk-actions: execute permission-aware bulk assignment, tagging, archive, status update, and export actions asynchronously when large. |
| API-04-024 | POST /api/v1/import-jobs with target_entity=account/contact/lead/opportunity/activity: start CRM imports through Core Platform ImportJob. |
| API-04-025 | POST /api/v1/export-jobs with entity_type=crm entity: start CRM exports through Core Platform ExportJob. |

## Permissions Introduced

| Permission ID | Permission |
| --- | --- |
| PERM-04-001 | crm.account.view: view Account lists and details allowed by company/module/record scope. |
| PERM-04-002 | crm.account.create: create Accounts. |
| PERM-04-003 | crm.account.update: update Accounts. |
| PERM-04-004 | crm.account.delete: archive/soft-delete Accounts. |
| PERM-04-005 | crm.account.merge: merge duplicate Accounts. |
| PERM-04-006 | crm.contact.view/create/update/delete/merge: manage Contacts by action-specific keys. |
| PERM-04-007 | crm.lead.view/create/update/delete: manage Leads by action-specific keys. |
| PERM-04-008 | crm.lead.convert: convert Leads to Account/Contact/Opportunity. |
| PERM-04-009 | crm.opportunity.view/create/update/delete: manage Opportunities. |
| PERM-04-010 | crm.opportunity.close: mark won/lost or reopen where allowed. |
| PERM-04-011 | crm.pipeline.manage: create/update/archive Pipelines and PipelineStages. |
| PERM-04-012 | crm.activity.view/log/update/delete: view and manage Activities according to action-specific keys. |
| PERM-04-013 | crm.note.view/create/update/delete and crm.comment.view/create/update/delete: collaboration permissions. |
| PERM-04-014 | crm.relationship_map.view/manage: view and manage Account relationship maps. |
| PERM-04-015 | crm.assignment_rule.manage: configure AssignmentRules. |
| PERM-04-016 | crm.import and crm.export: run CRM imports/exports; exports must be audited. |
| PERM-04-017 | crm.bulk_action: run bulk changes subject to the underlying entity/action permissions. |
| PERM-04-018 | crm.report.view: view CRM dashboards and report outputs. |
| PERM-04-019 | Ownership/team restrictions may limit records to owned, team, branch, or company-wide visibility through policies later. |

## UX Patterns Introduced

- CRM navigation for Accounts, Contacts, Leads, Opportunities, Activities, and CRM Settings/Pipelines.
- List/table views with saved filters, configurable columns, quick filters, bulk actions, export, empty states, and permission-aware action visibility.
- Account detail layout with header, lifecycle/status, owner/team, contacts, opportunities, activities/timeline, notes/comments, files, tags, custom fields, relationship map, related operational placeholders, and audit summary access.
- Lead workspace with prioritization by owner, source, score, status, next action, overdue follow-up, assignment, and duplicate warnings.
- Lead conversion flow with duplicate candidates and create/link choices for Account, Contact, and Opportunity.
- Opportunity kanban board by PipelineStage plus table view and stage drag/drop with permission validation.
- Reusable Activity Timeline component for CRM records and later operational records.
- RelationshipMap graph UI for stakeholders, influence, hierarchy, and decision roles.
- AssignmentRule builder with condition preview, target selection, priority ordering, and test/evaluate mode.
- Mobile CRM UX focused on quick lookup, lead/contact capture, notes, activities, and assigned/recent records rather than desktop parity.

## Reports or Dashboards Introduced

| Report ID | Report / Dashboard |
| --- | --- |
| REPORT-04-001 | Account counts by lifecycle_stage, type, owner, team, source, industry, geography, created period, and activity recency. |
| REPORT-04-002 | Contact coverage by Account, decision role, influence, do-not-contact status, missing email/phone, and activity recency. |
| REPORT-04-003 | Lead funnel by source, owner, status, score band, qualification outcome, conversion rate, age, and unqualified reason. |
| REPORT-04-004 | Opportunity pipeline by pipeline, stage, owner, team, weighted value, expected close date, stage age, won/lost reason, and revenue forecast. |
| REPORT-04-005 | Activity productivity by user, team, type, outcome, linked entity, period, and next action coverage. |
| REPORT-04-006 | Assignment effectiveness by rule, assigned target, workload balance, conversion rate, and override rate. |
| REPORT-04-007 | Data quality dashboards for duplicates, missing owners, stale next actions, invalid contacts, inactive stages, and unmapped relationships. |
| REPORT-04-008 | CRM export/report access must respect permissions and use report-safe denormalized snapshots where appropriate. |

## Notifications Introduced

| Notification ID | Notification |
| --- | --- |
| NOTIF-04-001 | Notify new owner or team when Account, Lead, or Opportunity is assigned if user preferences allow. |
| NOTIF-04-002 | Notify Lead owner when Lead becomes due/overdue for next action. |
| NOTIF-04-003 | Notify Opportunity owner when close date is approaching, stage is stale, or required next action is missing where configured. |
| NOTIF-04-004 | Notify managers when high-value Opportunity changes stage, is marked lost, or has no activity for configured threshold. |
| NOTIF-04-005 | Notify users mentioned in Comments if mention support is enabled in Core Platform. |
| NOTIF-04-006 | Notify admins when CRM imports partially fail or duplicate conflicts require review. |
| NOTIF-04-007 | Notifications must use Core Platform Notification entity and must not reveal inaccessible records. |

## Audit Events Introduced

| Audit ID | Event Family |
| --- | --- |
| AUDIT-04-001 | crm.account.created, updated, archived, restored, merged, owner_changed, lifecycle_changed. |
| AUDIT-04-002 | crm.contact.created, updated, archived, restored, merged, account_linked, account_unlinked, do_not_contact_changed. |
| AUDIT-04-003 | crm.lead.created, updated, assigned, qualified, unqualified, converted, archived, restored. |
| AUDIT-04-004 | crm.opportunity.created, updated, stage_changed, value_changed, owner_changed, won, lost, reopened, archived. |
| AUDIT-04-005 | crm.pipeline.created, updated, archived and crm.pipeline_stage.created, reordered, updated, archived. |
| AUDIT-04-006 | crm.activity.logged, corrected, archived and source-linked events for later integrations. |
| AUDIT-04-007 | crm.note.created, updated, archived and crm.comment.created, edited, deleted where collaboration history matters. |
| AUDIT-04-008 | crm.relationship_map.created, updated, archived, stakeholder_added, stakeholder_removed, relationship_changed. |
| AUDIT-04-009 | crm.assignment_rule.created, updated, activated, deactivated, archived, evaluated_with_assignment. |
| AUDIT-04-010 | crm.import.started, completed, partially_failed, failed and crm.export.requested, completed, failed, downloaded where available. |
| AUDIT-04-011 | crm.permission_denied may be logged for sensitive denied export/admin/bulk actions based on security policy. |

## Integrations Introduced

| Integration ID | Requirement |
| --- | --- |
| INT-04-001 | QuickBooks customer mapping must use external_refs and later QuickBooksCustomerLink; Account remains operational source of truth. |
| INT-04-002 | Email/SMS/WhatsApp/LinkedIn integrations in later phases must create or link Activity records rather than inventing separate timeline models. |
| INT-04-003 | Public API and webhook phases must reuse CRM endpoints, event names, and permission scopes defined here. |
| INT-04-004 | CSV/Excel imports for Account, Contact, Lead, Opportunity, and Activity must use Core Platform ImportJob. |
| INT-04-005 | Exports must use Core Platform ExportJob and must create audit events. |
| INT-04-006 | External IDs must live in external_refs or ExternalReference/provider link entities, never ad hoc top-level fields. |
| INT-04-007 | Outbound Sales Phase 05 must reuse Lead, Contact, Account, Opportunity, Activity, and AssignmentRule. |
| INT-04-008 | Field, dispatch, service, reporting, and integration phases must reuse Account/Contact/Opportunity instead of inventing customer entities. |

## Dependencies Created

- Depends on Phase 01 product foundation for unified CRM plus operations scope, desktop-first operations, mobile field support, reporting from day one, auditability, and QuickBooks as first-class integration.
- Depends on Phase 02 Tenant, Company, User, UserMembership, Role, Permission, module enablement, and backend authorization rules.
- Depends on Phase 03 Core Platform shared services: AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, ApiKey, WebhookEndpoint, WebhookDelivery, SettingsDocument, and BackgroundJob.
- Creates dependency for Phase 05 Outbound Sales to reuse Lead, Contact, Account, Opportunity, Activity, and AssignmentRule.
- Creates dependency for field, dispatch, service, reporting, QuickBooks, import/export, public API, and webhook phases to use Account/Contact/Opportunity as the shared customer/revenue context.

## Constraints Future Phases Must Respect

- Do not rename Account to Customer, Client, CRMCompany, CustomerCompany, or similar in data model or APIs.
- Do not confuse SaaS Company with CRM Account.
- Do not create module-specific customer/person/opportunity/activity models when the Phase 04 entities cover the concept.
- Do not use Activity as a replacement for specialized append-only operational events such as future inventory, GPS, sync, or audit events.
- Do not use Note or Comment as source-of-truth status, assignment, inventory, dispatch, billing, or operational event records.
- Do not store provider-specific external IDs as random top-level fields; use external_refs or approved provider link entities.
- Do not bypass Core Platform import/export, audit, notification, file, tag, custom field, saved view, search, background job, API key, or webhook foundations.
- Do not expose MongoDB `_id` through public APIs.
- Do not allow cross-tenant or unauthorized cross-company record linking.
- Do not permit exports, bulk actions, merges, conversions, or admin settings changes without backend permission checks and audit events.
- Do not make mobile CRM a full desktop-parity requirement in MVP; prioritize critical capture and assigned/recent context.

## Open Questions Carried Forward

- Confirm final generated ID format for CRM records: ULID, UUIDv7, KSUID, or another sortable opaque ID format.
- Confirm whether Contact-to-Account many-to-many relationships remain embedded as `account_ids` for MVP or require a dedicated relationship collection later.
- Confirm final duplicate matching thresholds and whether fuzzy matching is global default or company-configurable.
- Confirm whether RelationshipMap should remain one structured graph document per Account for MVP or be normalized for very large enterprise accounts.
- Confirm whether Opportunity products/services are summary fields in Phase 04 only or require line-item modeling before Quote/Order phases.
- Confirm whether Lead conversion may be offline in a later mobile phase or remains online-only because of duplicate and permission validation.
- Confirm exact stage type enum values and whether custom closed-won/closed-lost stage labels are allowed per Pipeline.
- Confirm default assignment algorithm options: first-match, round-robin, weighted, capacity-based, territory-based, or manual only for MVP.
- Confirm data retention and purge policy for archived CRM records, Activities, Notes, Comments, and AuditLog references.
- Confirm whether CRM record-level visibility beyond owner/team/company is required for MVP or deferred to policy-based authorization later.
