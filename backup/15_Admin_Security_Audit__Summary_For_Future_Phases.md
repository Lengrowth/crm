# Summary for Future Phases

## Final Decisions Made

- Phase 15 establishes Admin, Security, and Audit as the canonical foundation for administrative controls, security hardening, audit review, tenant/company isolation testing, permission hardening, admin settings, compliance expectations, monitoring, backup/restore governance, data retention, security incident handling, super admin operations, and rollout security gates.
- Phase 15 does not replace Phase 02 identity and access foundations. `Tenant`, `Company`, `User`, `UserMembership`, `Role`, `Permission`, `Policy`, `Session`, `Invitation`, and module enablement remain the canonical access model.
- Phase 15 does not replace Phase 03 Core Platform services. It extends and governs canonical `AuditLog`, `Notification`, `FileAttachment`, `SavedView`, `SearchIndexRecord`, `ImportJob`, `ExportJob`, `SettingsDocument`, `BackgroundJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery`.
- `SecuritySetting` is the canonical company/tenant/platform-scoped security configuration record for MFA requirements, session controls, password policy, export restrictions, API-key policy, IP allowlists where enabled, retention enforcement toggles, incident notification rules, and security gate requirements.
- `AuditReview` is the canonical formal review record for audit-log review, access review, permission review, export review, integration review, offline sync review, backup/restore review, and security gate evidence.
- `RetentionPolicy` is the canonical data retention and purge/anonymization policy record. Future phases must not create separate retention entities per module.
- `AdminAction` is the canonical high-impact administrative action wrapper used to capture intent, target, approval state, execution state, risk level, reason, and audit evidence for sensitive admin operations. It complements, but does not replace, append-only `AuditLog`.
- `SecurityIncident` is the canonical security incident record for suspected or confirmed tenant isolation issues, unauthorized access, credential compromise, suspicious export/import/API activity, integration credential concerns, data exposure, and security gate failures.
- `BackupJob` is the canonical backup execution record for scheduled, manual, pre-deploy, pre-migration, and emergency backups.
- `RestoreJob` is the canonical restore execution record for test restores, staging restores, emergency restores, point-in-time restore requests, and restore validation evidence.
- Audit logs remain append-only and immutable from normal application flows. Admin correction must create new audit events rather than editing prior audit history.
- High-volume telemetry such as raw `LocationPing` records is not treated as business audit logs, but configuration changes, access/export, derived alerts, assignment changes, retention changes, security reviews, and administrative actions must be audited.
- Permission changes, role changes, membership changes, module enablement changes, integration credential changes, API key changes, webhook configuration changes, export access, backup restore requests, retention policy changes, security setting changes, and super admin access must always be audited.
- Tenant and company boundaries must be verified server-side in API handlers, background jobs, workers, reporting datasets, exports, search indexes, notifications, integrations, offline sync, and restore workflows.
- Reports, exports, saved views, scheduled reports, API/webhook outputs, integrations, and offline sync must re-check permissions and company scope at execution time, not only when configured.
- Super admin operations must be minimized, reason-coded, audit logged, scoped, and visible through AdminAction and AuditReview where they affect tenant/company data or security posture.
- Backup and restore operations must never bypass tenant isolation, permissions, encryption expectations, audit requirements, retention constraints, or environment separation.
- Restore workflows must default to staging/test restore validation before production restoration unless an emergency restore path is explicitly authorized.
- Retention policies must be explicit, searchable, reportable, auditable, and future-compatible with legal hold, export, anonymization, and purge workflows.
- Security rollout gates are required before production enablement of sensitive modules and capabilities, including integrations, exports, public APIs, webhooks, mobile offline sync, admin settings, permissions, and backup/restore operations.
- Future notifications/automation, API/webhooks/import/export, rollout/operations, and final blueprint phases must respect Phase 15 security hardening rules.

## Entities Introduced

| Entity | Owner Module | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `SecuritySetting` | Admin / Security | Platform, tenant, or company depending setting | Stores security configuration and enforcement controls. | Future modules must reference this for security behavior instead of introducing module-specific security config records. |
| `AuditReview` | Admin / Security | Tenant/company, optional platform scope | Formal review record over audit logs, permissions, integrations, exports, retention, offline sync, incidents, and rollout gates. | Future phases must create review requirements here when security/compliance review is needed. |
| `RetentionPolicy` | Admin / Security | Tenant/company/module/entity scope | Defines retention, purge, anonymization, archive, legal hold compatibility, and enforcement behavior. | Future phases must register retention needs here instead of creating separate retention entities. |
| `AdminAction` | Admin / Security | Tenant/company/platform scoped by target | Captures high-impact admin intent, approval, execution, reason, and evidence. | Future high-risk admin operations should create AdminAction records and linked AuditLog entries. |
| `SecurityIncident` | Admin / Security | Tenant/company/platform, depending blast radius | Tracks suspected or confirmed security incidents, triage, severity, containment, remediation, notification, and closure. | Future monitoring/automation phases may create incidents automatically, but must reuse this entity. |
| `BackupJob` | Admin / Security / Operations | Tenant/company/platform/environment | Tracks backup execution, status, scope, trigger, retention, validation, and evidence. | Future rollout/operations must use this for backup observability and release gates. |
| `RestoreJob` | Admin / Security / Operations | Tenant/company/platform/environment | Tracks restore request, approval, execution, validation, and rollback evidence. | Future operations must use this for test and emergency restore workflows. |

## Fields Introduced

- Shared fields for all Phase 15 entities: `id`, `tenant_id`, `company_id` where applicable, `scope_type`, `scope_id`, `status`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `archived_at`, `archived_by_user_id`, `external_refs`, `metadata`, `audit_correlation_id`, and stable public application identifiers. MongoDB `_id` must not be exposed.
- `SecuritySetting`: `setting_key`, `setting_group`, `setting_value`, `effective_value`, `enforcement_mode`, `applies_to_module`, `applies_to_entity_type`, `is_inherited`, `inherited_from_scope_type`, `inherited_from_scope_id`, `requires_admin_action`, `requires_reauth`, `effective_from_at`, `effective_until_at`, `last_evaluated_at`, `risk_level`, `change_reason`, `version`, `locked_by_platform`, `allowed_override_scope`, `validation_schema`, `last_reviewed_at`, `next_review_due_at`.
- `AuditReview`: `review_type`, `review_period_start_at`, `review_period_end_at`, `review_scope`, `reviewer_user_id`, `reviewer_team_id`, `review_status`, `risk_rating`, `sample_strategy`, `source_query`, `source_saved_view_id`, `audit_log_ids`, `related_admin_action_ids`, `related_incident_ids`, `findings`, `exceptions`, `remediation_tasks`, `completed_at`, `approved_by_user_id`, `approval_notes`, `evidence_file_attachment_ids`, `next_review_due_at`.
- `RetentionPolicy`: `policy_name`, `policy_code`, `target_module`, `target_entity_type`, `target_event_type`, `retention_period_days`, `retention_action`, `archive_before_purge`, `anonymize_fields`, `preserve_fields`, `legal_hold_supported`, `default_legal_hold_behavior`, `enforcement_status`, `last_run_at`, `next_run_at`, `last_run_result`, `exemption_rules`, `approval_required`, `approved_by_user_id`, `effective_from_at`, `superseded_by_policy_id`.
- `AdminAction`: `action_type`, `target_entity_type`, `target_entity_id`, `target_user_id`, `target_membership_id`, `target_module`, `risk_level`, `reason_code`, `reason_text`, `requested_by_user_id`, `approved_by_user_id`, `approval_status`, `execution_status`, `executed_at`, `expires_at`, `requires_reauth`, `requires_mfa`, `requires_dual_control`, `before_snapshot_ref`, `after_snapshot_ref`, `related_audit_log_ids`, `related_incident_id`, `rollback_available`, `rollback_action_id`.
- `SecurityIncident`: `incident_number`, `incident_type`, `severity`, `status`, `detection_source`, `detected_at`, `reported_by_user_id`, `assigned_owner_user_id`, `affected_tenant_ids`, `affected_company_ids`, `affected_user_ids`, `affected_entity_refs`, `suspected_blast_radius`, `confirmed_blast_radius`, `containment_actions`, `remediation_actions`, `root_cause`, `customer_notification_required`, `customer_notified_at`, `regulatory_review_required`, `closed_at`, `postmortem_file_attachment_ids`, `linked_audit_review_id`.
- `BackupJob`: `job_type`, `environment`, `backup_scope_type`, `backup_scope_id`, `trigger_type`, `triggered_by_user_id`, `status`, `started_at`, `completed_at`, `storage_reference`, `encrypted`, `encryption_key_ref`, `retention_until_at`, `size_bytes`, `record_counts`, `validation_status`, `validation_details`, `failure_reason`, `related_release_id`, `related_admin_action_id`.
- `RestoreJob`: `restore_type`, `environment`, `source_backup_job_id`, `restore_scope_type`, `restore_scope_id`, `requested_by_user_id`, `approved_by_user_id`, `approval_status`, `status`, `started_at`, `completed_at`, `target_environment`, `target_tenant_id`, `target_company_id`, `restore_point_at`, `validation_status`, `validation_details`, `rollback_plan_ref`, `customer_impact_notes`, `failure_reason`, `related_incident_id`, `related_admin_action_id`.

## APIs Introduced

- `GET /api/v1/admin/security-settings`
- `POST /api/v1/admin/security-settings`
- `GET /api/v1/admin/security-settings/{security_setting_id}`
- `PATCH /api/v1/admin/security-settings/{security_setting_id}`
- `POST /api/v1/admin/security-settings/{security_setting_id}/review`
- `GET /api/v1/admin/audit-reviews`
- `POST /api/v1/admin/audit-reviews`
- `GET /api/v1/admin/audit-reviews/{audit_review_id}`
- `PATCH /api/v1/admin/audit-reviews/{audit_review_id}`
- `POST /api/v1/admin/audit-reviews/{audit_review_id}/complete`
- `GET /api/v1/admin/retention-policies`
- `POST /api/v1/admin/retention-policies`
- `PATCH /api/v1/admin/retention-policies/{retention_policy_id}`
- `POST /api/v1/admin/retention-policies/{retention_policy_id}/run-preview`
- `POST /api/v1/admin/retention-policies/{retention_policy_id}/request-enforcement`
- `GET /api/v1/admin/admin-actions`
- `POST /api/v1/admin/admin-actions`
- `POST /api/v1/admin/admin-actions/{admin_action_id}/approve`
- `POST /api/v1/admin/admin-actions/{admin_action_id}/execute`
- `POST /api/v1/admin/admin-actions/{admin_action_id}/cancel`
- `GET /api/v1/admin/security-incidents`
- `POST /api/v1/admin/security-incidents`
- `PATCH /api/v1/admin/security-incidents/{security_incident_id}`
- `POST /api/v1/admin/security-incidents/{security_incident_id}/contain`
- `POST /api/v1/admin/security-incidents/{security_incident_id}/close`
- `GET /api/v1/admin/backup-jobs`
- `POST /api/v1/admin/backup-jobs`
- `GET /api/v1/admin/backup-jobs/{backup_job_id}`
- `GET /api/v1/admin/restore-jobs`
- `POST /api/v1/admin/restore-jobs`
- `POST /api/v1/admin/restore-jobs/{restore_job_id}/approve`
- `POST /api/v1/admin/restore-jobs/{restore_job_id}/execute`
- `POST /api/v1/admin/restore-jobs/{restore_job_id}/validate`
- All APIs must enforce tenant/company scope, module access, permission checks, rate limits where relevant, audit logging, and idempotency for mutation operations.

## Permissions Introduced

- `admin.security_setting.view`
- `admin.security_setting.manage`
- `admin.security_setting.review`
- `admin.audit_review.view`
- `admin.audit_review.create`
- `admin.audit_review.complete`
- `admin.retention_policy.view`
- `admin.retention_policy.manage`
- `admin.retention_policy.enforce`
- `admin.admin_action.view`
- `admin.admin_action.request`
- `admin.admin_action.approve`
- `admin.admin_action.execute`
- `admin.security_incident.view`
- `admin.security_incident.manage`
- `admin.security_incident.close`
- `admin.backup_job.view`
- `admin.backup_job.run`
- `admin.restore_job.view`
- `admin.restore_job.request`
- `admin.restore_job.approve`
- `admin.restore_job.execute`
- `admin.tenant_isolation_test.view`
- `admin.tenant_isolation_test.run`
- `admin.permission_hardening.view`
- `admin.permission_hardening.manage`
- `admin.audit_log.export`
- Super admin permissions must be separated from company admin permissions. Company admins must not receive platform-wide powers by default.

## UX Patterns Introduced

- Admin Security Dashboard with security posture cards, unresolved incidents, failed backup/restore jobs, upcoming audit reviews, risky settings, permission changes, export activity, integration health, and offline sync security indicators.
- Security Settings screens with grouped settings, inherited values, override indicators, validation warnings, change previews, reauthentication prompts, and audit history panels.
- Audit Review list and detail screens with period, review type, reviewer, findings, exceptions, evidence, completion workflow, and linked remediation tasks.
- Retention Policy screen with target entity selectors, retention period controls, dry-run preview, affected-record estimates, approval state, legal hold warnings, and enforcement history.
- Admin Action center with request, approval, execution, rollback, and evidence timelines.
- Security Incident workspace with severity, timeline, affected scopes, containment checklist, remediation checklist, linked audit logs, customer notification status, and closure notes.
- Backup and Restore center with backup status, restore requests, validation status, environment warnings, scope summaries, approval behavior, and emergency restore warnings.
- Permission behavior pattern: users without permission must not see sensitive detail values; screens should show safe empty/blocked states instead of leaking counts, names, or configuration secrets.

## Reports or Dashboards Introduced

- Security Posture Dashboard.
- Audit Review Completion Report.
- Permission Change Report.
- Admin Action Report.
- Retention Enforcement Report.
- Security Incident Report.
- Backup and Restore Health Report.
- Export and API Access Risk Report.
- Tenant/Company Isolation Test Results Report.
- Integration Security Review Report.
- Offline Sync Security Review Report.

## Notifications Introduced

- Security setting changed.
- High-risk admin action requested.
- High-risk admin action approved, executed, failed, or canceled.
- Audit review assigned, due soon, overdue, completed, or reopened.
- Retention policy enforcement preview completed or enforcement failed.
- Security incident created, severity escalated, containment required, customer notification required, or closed.
- Backup job failed, backup validation failed, or backup missing for required gate.
- Restore job requested, awaiting approval, started, completed, failed, or validation failed.
- Permission hardening issue detected.
- Tenant isolation test failed.
- Suspicious export/API/integration/offline sync activity detected.

## Audit Events Introduced

- `security_setting.created`
- `security_setting.updated`
- `security_setting.review_requested`
- `security_setting.review_completed`
- `audit_review.created`
- `audit_review.updated`
- `audit_review.completed`
- `audit_review.reopened`
- `retention_policy.created`
- `retention_policy.updated`
- `retention_policy.preview_run`
- `retention_policy.enforcement_requested`
- `retention_policy.enforced`
- `retention_policy.enforcement_failed`
- `admin_action.requested`
- `admin_action.approved`
- `admin_action.rejected`
- `admin_action.executed`
- `admin_action.failed`
- `admin_action.canceled`
- `security_incident.created`
- `security_incident.updated`
- `security_incident.severity_changed`
- `security_incident.containment_action_added`
- `security_incident.closed`
- `backup_job.created`
- `backup_job.started`
- `backup_job.completed`
- `backup_job.failed`
- `backup_job.validation_completed`
- `restore_job.requested`
- `restore_job.approved`
- `restore_job.started`
- `restore_job.completed`
- `restore_job.failed`
- `restore_job.validation_completed`
- `tenant_isolation_test.started`
- `tenant_isolation_test.failed`
- `tenant_isolation_test.passed`
- `permission_hardening.issue_detected`
- `permission_hardening.issue_resolved`

## Integrations Introduced

- No new external provider integration is introduced by Phase 15.
- Phase 15 introduces security governance requirements for all integrations, including credential handling, secret redaction, connection changes, webhook endpoint security, failed sync visibility, API key scoping, provider access review, and audit review.
- QuickBooks integration monitoring must surface in security review where credential, sync, mapping, export, or webhook risk exists.
- Future public API, webhook, import/export, and automation phases must use Phase 15 permission, audit, retention, incident, and rollout gate requirements.

## Dependencies Created

- Depends on Phase 01 product foundation for unified SaaS scope, MVP boundaries, desktop/mobile behavior, auditability, and offline-friendly capture.
- Depends on Phase 02 identity and access for Tenant, Company, User, UserMembership, Role, Permission, Policy, Session, Invitation, module access, backend authorization, and offline revalidation.
- Depends on Phase 03 core platform for AuditLog, Notification, FileAttachment, SavedView, SearchIndexRecord, ImportJob, ExportJob, SettingsDocument, BackgroundJob, ApiKey, WebhookEndpoint, and WebhookDelivery.
- Depends on Phases 04 through 14 for module-specific entities and workflows that must be governed by security settings, audit review, retention, incident handling, backup/restore, tenant isolation testing, reporting, integrations, and offline sync hardening.
- Creates dependencies for future notifications/automation, API/webhooks/import/export, rollout/operations, and final blueprint phases.

## Constraints Future Phases Must Respect

- Do not create duplicate admin/security/audit entities when `SecuritySetting`, `AuditReview`, `RetentionPolicy`, `AdminAction`, `SecurityIncident`, `BackupJob`, or `RestoreJob` covers the concept.
- Do not bypass backend tenant/company checks, even for internal admin screens, background jobs, integrations, exports, reports, offline sync, or support tooling.
- Do not expose secrets, tokens, API keys, webhook signing secrets, refresh tokens, connection credentials, password hashes, or sensitive backup references in plaintext UI, API responses, exports, audit details, logs, or notifications.
- Do not treat frontend hiding as authorization.
- Do not allow scheduled reports, automations, exports, imports, webhooks, integration sync, or offline queued actions to run without permission revalidation.
- Do not allow retention purge/anonymization to destroy audit evidence needed for security investigations unless explicitly approved by a future legal/compliance decision.
- Do not allow production restores without audit logging, approval rules, scope validation, environment validation, and post-restore verification.
- Do not let company admins access platform-wide tenant data unless an explicit super admin support workflow grants narrowly scoped, audited access.
- Do not use `AuditReview` as a substitute for append-only `AuditLog`; AuditReview is a review/evidence workflow.
- Do not use `AdminAction` as a substitute for permission checks; AdminAction is an approval/evidence wrapper for high-impact operations.
- Future notifications and automation must include escalation and suppression rules that do not leak sensitive data to unauthorized users.
- Future API/webhook/import/export phases must include rate limits, scopes, audit events, security settings, retention handling, and incident triggers defined by Phase 15.

## Open Questions Carried Forward

1. Should platform-wide super admin access require mandatory dual control for all production tenant data access, or only for high-risk actions such as restore, impersonation, credential rotation, and destructive retention enforcement?
2. Which MFA provider and policy engine will be used in implementation, and will MFA be mandatory for all users or only admins in MVP?
3. What are the default retention periods for audit logs, security incidents, raw telemetry, exports, integration logs, offline sync logs, and file attachments?
4. What legal hold workflow is required for MVP, if any?
5. Should production restore operations be available from the application UI, or should the UI only request and track restore operations executed through infrastructure tooling?
6. What exact backup storage provider, encryption key management approach, and restore-point objectives will be used in production?
7. Should tenant isolation tests be executable by company admins, or only visible as pass/fail evidence from platform security operations?
8. What compliance frameworks are launch-critical: SOC 2 readiness, GDPR-style data rights, industry-specific requirements, customer contract requirements, or internal operational controls only?
9. Should admin support impersonation be allowed, or should the product use screen-sharing/support tokens without true impersonation?
10. What security incident notification timeline and customer communication workflow will be adopted for launch customers?
