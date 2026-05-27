# Summary for Future Phases

## Final Decisions Made

- Phase 16 establishes Notifications and Automation as the canonical foundation for notification rules, notification templates, notification preferences, automation rules, triggers, conditions, actions, escalations, subscriptions, delivery governance, admin controls, and cross-module automation safety.
- `Notification` remains the canonical recipient-facing alert record introduced by the Core Platform foundation; Phase 16 expands how notifications are configured, generated, rendered, delivered, read, dismissed, retried, and audited.
- `Reminder` remains the canonical reminder record for task, appointment, calendar, SLA, and recurrence-driven reminders. Phase 16 must not replace `Reminder`; it may orchestrate reminder delivery through notification rules and preferences.
- `AssignmentRule` remains the canonical assignment-specific rule configuration from CRM/Core foundations. Phase 16 must not replace it with `AutomationRule`; automation may invoke assignment behavior through approved assignment actions that reference `AssignmentRule` where assignment logic is needed.
- `NotificationRule` is the canonical company-scoped rule configuration that decides when a notification should be generated for supported event types, modules, severities, roles, teams, users, and related records.
- `NotificationTemplate` is the canonical reusable message template for in-app, email, push, SMS, webhook, and future channels. Templates must be permission-safe and must not expose inaccessible record data.
- `NotificationPreference` is the canonical user/company preference record controlling user opt-in, opt-out, digest, quiet hours, channel selection, and priority thresholds for configurable notifications.
- `AutomationRule` is the canonical cross-module automation configuration for event-driven or scheduled rule execution. It is not a workflow engine replacement, not a business process language, and not a substitute for explicit module workflows.
- `AutomationTrigger`, `AutomationCondition`, and `AutomationAction` are modeled as canonical child/config records or embedded subdocuments under `AutomationRule` depending implementation needs. They define what starts an automation, what must be true, and what action may be performed.
- `EscalationRule` is the canonical configuration for raising priority, notifying supervisors, creating tasks, changing ownership, or moving unresolved exceptions through time-based escalation steps.
- `Subscription` is the canonical user/team/role/entity subscription configuration for explicit follows, watched records, saved-view alert subscriptions, report/automation subscriptions, and operational event streams.
- Phase 16 automation must use allowlisted triggers and allowlisted actions. It must not allow arbitrary code execution, raw database updates, unbounded fan-out, unrestricted external calls, or bypass of module permissions.
- Automation execution must always revalidate tenant, company, module enablement, actor/system context, target record access, action permission, workflow status, and idempotency before performing side effects.
- Notification generation must be permission-aware. Notification title, body, preview, metadata, links, templates, and digests must not leak inaccessible entity names, customer data, locations, amounts, GPS details, attachments, or integration errors.
- High-volume event streams such as raw `LocationPing` records must not directly create user notifications. Notifications should be created from derived exceptions, alert records, summary thresholds, or explicitly configured rules.
- Failed notification deliveries, failed automation executions, skipped actions, blocked permission checks, invalid templates, throttled rules, and escalation failures must be visible to authorized admins and reportable.
- Automation and notification configuration changes must create append-only `AuditLog` entries. Execution attempts that change records, send external communications, invoke webhooks, export data, or escalate incidents must also be auditable.
- Notification delivery channels for Phase 16 are in-app as baseline, email as recommended/optional where provider is configured, push as future-capable for mobile, SMS/WhatsApp only where integration and compliance controls exist, and webhook/system-to-system delivery through existing webhook foundations.
- Phase 16 does not create public API/webhook marketplace scope. Future API/webhooks/import/export phases must respect Phase 16 automation event and action allowlists, idempotency, permission checks, audit requirements, retry rules, rate limits, and failure observability.
- Phase 16 does not create customer-facing portal notifications, full marketing automation, arbitrary workflow scripting, payroll/HR automation, advanced AI automation, or LinkedIn automated action execution.

## Entities Introduced

| Entity | Owner Module | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `NotificationRule` | Notifications / Automation | Tenant + Company; optional module/entity scope | Configures when notifications are generated from allowed platform events. | Reuse for module notification configuration; do not create module-specific rule entities. |
| `NotificationTemplate` | Notifications / Automation | Tenant + Company; optional channel/module scope | Defines safe reusable notification content per channel and locale. | Reuse for all notification copy; templates must be permission-safe. |
| `NotificationPreference` | Notifications / Automation | Tenant + Company + UserMembership/User | Stores user/company channel, digest, quiet-hour, and priority preferences. | Reuse for all user notification preferences; do not create per-module preference tables. |
| `AutomationRule` | Notifications / Automation | Tenant + Company; optional module/entity scope | Configures allowed event-driven or scheduled automation. | Reuse for cross-module automation; do not create arbitrary workflow engines. |
| `AutomationTrigger` | Notifications / Automation | Child of AutomationRule or rule-scoped config | Defines the allowed event, schedule, threshold, or subscription trigger that starts a rule. | Must use registered trigger types only. |
| `AutomationCondition` | Notifications / Automation | Child of AutomationRule or rule-scoped config | Defines safe boolean filters against allowed fields, statuses, priorities, ownership, time windows, and related context. | Must not expose unrestricted query language to end users. |
| `AutomationAction` | Notifications / Automation | Child of AutomationRule or rule-scoped config | Defines an allowlisted side effect such as notify, create task, update approved status, assign, escalate, webhook, or create report run. | Must be permission-checked, idempotent, and audited when state-changing. |
| `EscalationRule` | Notifications / Automation | Tenant + Company; optional module/entity scope | Configures time-based escalation for unresolved exceptions, approvals, overdue tasks, sync failures, and incidents. | Reuse for escalation instead of creating per-module escalation concepts. |
| `Subscription` | Notifications / Automation | Tenant + Company + user/team/role/entity/saved view | Stores explicit watch/follow/subscribe relationships for records, saved views, reports, events, and rule outputs. | Reuse for follows, watched records, saved-view alerts, and operational subscriptions. |

## Fields Introduced

- Common fields for all Phase 16 configuration entities: `id`, `tenant_id`, `company_id`, `name`, `description`, `module_key`, `entity_type`, `status`, `priority`, `created_at`, `created_by_user_id`, `updated_at`, `updated_by_user_id`, `archived_at`, `archived_by_user_id`, `version`, `external_refs`, and `metadata` where approved.
- `NotificationRule`: `event_type`, `source_module`, `target_entity_type`, `recipient_strategy`, `recipient_user_ids`, `recipient_team_ids`, `recipient_role_keys`, `template_id`, `channels`, `priority`, `throttle_policy`, `digest_policy`, `quiet_hours_behavior`, `dedupe_key_template`, `condition_group`, `effective_from_at`, `effective_until_at`, `last_evaluated_at`.
- `NotificationTemplate`: `template_key`, `channel`, `locale`, `subject_template`, `title_template`, `body_template`, `action_label_template`, `deep_link_template`, `allowed_variables`, `redaction_policy`, `fallback_template_id`, `status`, `version`, `test_payload_schema`.
- `NotificationPreference`: `user_id`, `user_membership_id`, `company_id`, `module_key`, `event_type`, `channel_preferences`, `priority_threshold`, `digest_frequency`, `quiet_hours_start`, `quiet_hours_end`, `timezone`, `muted_until_at`, `override_source`, `required_notification_exceptions`.
- `AutomationRule`: `trigger`, `conditions`, `actions`, `execution_mode`, `run_as_strategy`, `owner_user_id`, `owner_team_id`, `rate_limit_policy`, `retry_policy`, `idempotency_policy`, `failure_policy`, `last_run_at`, `next_run_at`, `last_run_status`, `enabled_at`, `disabled_reason`.
- `AutomationTrigger`: `trigger_type`, `event_type`, `schedule_rule_id`, `source_entity_type`, `source_statuses`, `threshold_definition`, `subscription_id`, `webhook_event_key`, `timezone`.
- `AutomationCondition`: `field_path`, `operator`, `value`, `value_type`, `condition_group_id`, `related_entity_reference`, `time_window`, `permission_guard`, `null_behavior`.
- `AutomationAction`: `action_type`, `target_entity_type`, `target_entity_id_template`, `payload_template`, `assignment_rule_id`, `notification_rule_id`, `webhook_endpoint_id`, `task_template`, `status_update`, `requires_approval`, `idempotency_key_template`.
- `EscalationRule`: `source_entity_type`, `source_statuses`, `severity`, `time_to_acknowledge_minutes`, `time_to_resolve_minutes`, `levels`, `recipient_strategy`, `create_task`, `notify_supervisor`, `pause_on_statuses`, `stop_on_statuses`.
- `Subscription`: `subscriber_type`, `subscriber_user_id`, `subscriber_team_id`, `subscriber_role_key`, `target_entity_type`, `target_entity_id`, `saved_view_id`, `report_id`, `event_types`, `channels`, `status`, `frequency`, `last_notified_at`.

## APIs Introduced

- Conceptual admin APIs for listing, creating, updating, testing, activating, pausing, archiving, and versioning `NotificationRule` records.
- Conceptual template APIs for listing, creating, previewing, validating, testing, activating, versioning, and archiving `NotificationTemplate` records.
- Conceptual preference APIs for reading and updating current-user and admin-managed `NotificationPreference` records.
- Conceptual automation APIs for listing, creating, validating, testing, activating, pausing, archiving, dry-running, and viewing execution history for `AutomationRule` records.
- Conceptual APIs for rule trigger catalog, condition field catalog, action catalog, and safe variable catalog so UI builders cannot expose unsupported automation capabilities.
- Conceptual APIs for `EscalationRule` configuration and escalation status review.
- Conceptual APIs for `Subscription` follow/unfollow, saved-view subscription, report subscription, and entity subscription behavior.
- Conceptual notification APIs for inbox, unread counts, mark read/unread, dismiss, bulk read, delivery status, and deep-link resolution.
- Future public API, webhook, import/export, rollout, and final blueprint phases must reuse these event/action constraints and must not create bypass paths.

## Permissions Introduced

- `notifications.notification.view`
- `notifications.notification.manage_own`
- `notifications.notification.manage_company`
- `notifications.rule.view`
- `notifications.rule.manage`
- `notifications.template.view`
- `notifications.template.manage`
- `notifications.preference.view_own`
- `notifications.preference.manage_own`
- `notifications.preference.manage_company`
- `automation.rule.view`
- `automation.rule.manage`
- `automation.rule.activate`
- `automation.rule.test`
- `automation.execution.view`
- `automation.execution.retry`
- `automation.execution.cancel`
- `automation.escalation.view`
- `automation.escalation.manage`
- `automation.subscription.manage_own`
- `automation.subscription.manage_company`

## UX Patterns Introduced

- Notification inbox with unread, read, dismissed, failed, priority, module, entity, assignment, escalation, and sync-failure filters.
- Notification preferences screen with per-channel controls, quiet hours, digest frequency, required notification explanation, and permission-aware disabled states.
- Notification rule admin builder with event selection, recipient strategy, conditions, template/channel selection, throttling, preview, test send, activate/pause, and audit history.
- Template builder with safe variables, channel preview, redaction preview, test payloads, version history, fallback content, and validation errors.
- Automation rule builder with trigger, conditions, action steps, dry run, affected-record preview, permission warnings, rate-limit warnings, execution history, and failure state.
- Escalation configuration screen with levels, timers, recipients, actions, pause/stop statuses, and simulation preview.
- Subscription controls on record headers, saved views, reports, dashboard cards, and operational exception pages where enabled.
- Admin monitoring screen for failed, skipped, throttled, retrying, and blocked notification/automation executions.

## Reports or Dashboards Introduced

- Notification volume by module, event type, channel, priority, recipient, status, and time period.
- Notification delivery health including queued, delivered, read, dismissed, failed, bounced, throttled, and retried counts.
- Automation execution health including success, skipped, blocked, failed, retrying, cancelled, and average execution duration.
- Escalation performance by module, severity, time to acknowledge, time to resolve, level reached, and overdue status.
- User preference coverage and mute/digest adoption for notification governance.
- Admin/security reporting for high-risk automation changes, external delivery actions, webhook-triggering automations, and failed critical notifications.

## Notifications Introduced

- Assignment and ownership change notifications.
- Task, appointment, calendar, SLA, maintenance, scheduled report, and recurrence-driven reminder notifications through existing `Reminder` foundations.
- Exception notifications for low stock, delivery exceptions, speed/stop alerts, device health, sync failures, QuickBooks failures, import/export failures, offline sync conflicts, service exceptions, and security incidents.
- Escalation notifications for unresolved exceptions, overdue tasks, unacknowledged alerts, failed integrations, and high-risk admin/security events.
- Digest notifications where high-volume events would otherwise cause fatigue.
- Subscription notifications for followed records, saved views, watched reports, and configured operational event streams.

## Audit Events Introduced

- `notification_rule.created`, `notification_rule.updated`, `notification_rule.activated`, `notification_rule.paused`, `notification_rule.archived`, `notification_rule.tested`.
- `notification_template.created`, `notification_template.updated`, `notification_template.versioned`, `notification_template.activated`, `notification_template.archived`, `notification_template.tested`.
- `notification_preference.updated_by_user`, `notification_preference.updated_by_admin`, `notification_preference.required_override_applied`.
- `automation_rule.created`, `automation_rule.updated`, `automation_rule.activated`, `automation_rule.paused`, `automation_rule.archived`, `automation_rule.tested`, `automation_rule.execution_started`, `automation_rule.execution_succeeded`, `automation_rule.execution_failed`, `automation_rule.execution_skipped`, `automation_rule.execution_blocked`, `automation_rule.execution_retried`, `automation_rule.execution_cancelled`.
- `escalation_rule.created`, `escalation_rule.updated`, `escalation_rule.activated`, `escalation_rule.paused`, `escalation_rule.archived`, `escalation_level.reached`.
- `subscription.created`, `subscription.updated`, `subscription.paused`, `subscription.cancelled`.
- `notification.delivery_failed`, `notification.delivery_retried`, `notification.delivery_blocked`, `notification.required_sent` for security-critical or operationally critical notifications.

## Integrations Introduced

- Email provider integration readiness for external email delivery of approved notification templates.
- Mobile push provider readiness for future push notifications.
- SMS/WhatsApp provider readiness only where compliance controls, user consent, provider configuration, and notification preferences exist.
- Webhook delivery integration through existing `WebhookEndpoint` and `WebhookDelivery` foundations for allowed automation actions.
- QuickBooks, import/export, offline sync, scheduled report, fleet/device, and security/admin failure events may emit notifications and automation events but must not bypass Phase 16 constraints.

## Dependencies Created

- Depends on Phase 02 tenant, company, user, membership, role, permission, module enablement, and backend permission checks.
- Depends on Phase 03 `Notification`, `AuditLog`, `SettingsDocument`, `BackgroundJob`, `SavedView`, `SearchIndexRecord`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery` foundations.
- Depends on Phase 04 `AssignmentRule`, CRM entities, and activity/timeline context where assignment or customer notifications are configured.
- Depends on Phase 06 `Task`, `CalendarEvent`, `Appointment`, `Reminder`, and `RecurrenceRule` for reminders and scheduled work.
- Depends on Phases 07 through 11 operational exception, assignment, status, proof, device, inventory, dispatch, and service events.
- Depends on Phase 12 reporting foundations for notification and automation health reporting.
- Depends on Phase 13 integration foundations for provider failure notifications and webhook delivery.
- Depends on Phase 14 offline sync foundations for conflict/failure notifications and mobile notification behavior.
- Depends on Phase 15 admin/security foundations for high-risk settings, audit review, security incident, retention, and admin monitoring governance.

## Constraints Future Phases Must Respect

- Future API, webhook, import/export, rollout, and final blueprint phases must respect Phase 16 automation trigger/action allowlists, idempotency, audit, retry, throttling, and permission rules.
- Future modules must register notification event types, template variables, automation triggers, allowed conditions, allowed actions, and audit events rather than creating independent automation systems.
- Future modules must not notify users about records they cannot access.
- Future modules must not create module-specific notification preference, escalation, subscription, or automation-rule entities unless a later global decision explicitly approves a specialized extension.
- Future high-volume telemetry must be summarized or converted into derived alerts before notification generation.
- Future external messaging automation must obey provider configuration, consent/compliance rules, quiet hours, opt-outs, audit logging, and failure observability.
- Future automations that mutate records must revalidate current state and permissions at execution time, not only at rule creation time.
- Future automation actions must be idempotent and safe for retries.
- Future public API/webhook event subscriptions must distinguish between user-facing `Notification`, system `WebhookDelivery`, and `Subscription` preferences.
- Future reporting must expose automation and notification failures as operational risks.

## Open Questions Carried Forward

- Which external email, push, SMS, and WhatsApp providers will be selected for production notification delivery?
- Whether notification digests should be generated by user timezone, company timezone, or per-preference timezone for scheduled emailed reports and operational summaries.
- Whether customer-facing notifications will be supported in a later customer portal phase.
- Whether complex multi-step automation should remain limited to allowlisted actions or later evolve into a richer workflow orchestration engine.
- Whether admin approval is required for all external-channel automation actions or only high-risk actions.
- Final retention periods for read, dismissed, failed, and archived notifications.
- Whether automation execution history should be stored as a dedicated execution entity in a future phase or represented through `AuditLog`, `BackgroundJob`, and reporting rollups in MVP.
- Whether AI-assisted automation recommendations are allowed in a later phase, and what approval controls they require.
