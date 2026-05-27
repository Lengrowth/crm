# Summary for Future Phases

## Final Decisions Made

- Phase 06 establishes Calendar and Tasks as the shared scheduling, due-date, assignment, reminder, recurrence, SLA, and work-queue foundation for CRM, Outbound Sales, Field Sales, Dispatch, Service, Reporting, Notifications, and Mobile workflows.
- Future phases must reuse canonical `Task`, `CalendarEvent`, `Appointment`, `Reminder`, and `RecurrenceRule` entities instead of creating module-specific task, appointment, reminder, or scheduling systems.
- `Task` is the canonical actionable work item for follow-ups, callbacks, internal to-dos, customer promises, SLA actions, field preparation, dispatch prep, service follow-ups, and mobile offline task capture.
- `CalendarEvent` is the canonical scheduled time block for meetings, appointments, site visits, dispatch windows, service windows, internal planning events, and future external calendar sync.
- `Appointment` is a business-facing scheduled interaction built on or linked to `CalendarEvent`; it must not become a duplicate independent calendar system.
- `Reminder` is the canonical notification trigger configuration and runtime reminder record for tasks, appointments, calendar events, SLA deadlines, and recurrence-generated work.
- `RecurrenceRule` is the canonical recurrence configuration for repeat tasks and repeat calendar events. It stores the repeat pattern, timezone, start/end boundaries, and exception handling.
- Phase 06 must use Phase 03 foundations for `Notification`, `AuditLog`, `SavedView`, `SearchIndexRecord`, `FileAttachment`, `Tag`, `TagAssignment`, `CustomFieldDefinition`, `CustomFieldValue`, `SettingsDocument`, `BackgroundJob`, `ImportJob`, and `ExportJob`.
- Phase 06 must use Phase 04 CRM records such as `Account`, `Contact`, `Lead`, `Opportunity`, and `Activity` as related records, not as replacements for task/calendar records.
- Phase 06 must support Phase 05 Outbound Sales follow-up work by representing outbound follow-ups as `Task` records with outbound references and categories rather than a separate follow-up task system.
- All company-scoped records must include `tenant_id` and `company_id`; optional `branch_id`, `assigned_user_id`, `assigned_team_id`, and related record references should be used where relevant.
- User assignment and visibility must follow `UserMembership`, role permissions, company module enablement, and future policy-based authorization compatibility.
- Scheduled and due work must be searchable, filterable, reportable, auditable, and permission-aware.
- Reminders must be generated through the shared notification foundation and must never bypass notification preferences, permission checks, or company/module access rules.
- Recurrence should generate or materialize instances through controlled background jobs and must preserve parent recurrence identity, exception history, and auditability.
- Mobile/offline task execution is required for critical field workflows, but full offline calendar parity, external calendar sync, and complex resource optimization are future concerns.
- SLA support in Phase 06 is foundational: tasks and events may carry due dates, priority, SLA policy references, escalation metadata, and breach timestamps, but advanced SLA policy management can be expanded later.
- External Google Calendar / Microsoft 365 sync is integration-ready but not required as automatic two-way sync in this phase unless explicitly approved.

## Entities Introduced

| Entity | Owner module | Scope | Purpose | Future phase rule |
| --- | --- | --- | --- | --- |
| `Task` | Calendar / Tasks | Company-scoped | Canonical actionable work item with assignment, due date, priority, related records, SLA fields, completion state, reminders, and queue behavior. | All future modules must use this entity for actionable work instead of creating duplicate task concepts. |
| `CalendarEvent` | Calendar / Tasks | Company-scoped | Canonical scheduled time block with start/end, timezone, participants, location, related records, reminders, recurrence, and visibility rules. | Field visits, dispatch windows, service windows, and external calendar integrations must reference or extend this entity. |
| `Appointment` | Calendar / Tasks with CRM/field context | Company-scoped | Business/customer-facing scheduled interaction linked to `CalendarEvent`, CRM records, contacts, sites, or opportunities. | Do not create separate appointment systems in CRM, outbound, field, dispatch, or service phases. |
| `Reminder` | Calendar / Tasks + Notifications | Company-scoped or user-scoped child record | Reminder trigger for tasks, events, appointments, SLA deadlines, or recurrence-generated instances. | Must create/drive `Notification` records rather than bypassing notification infrastructure. |
| `RecurrenceRule` | Calendar / Tasks | Company-scoped configuration/child record | Repeat pattern definition for tasks and calendar events, including timezone, frequency, interval, boundaries, and exceptions. | Future recurring jobs, service schedules, and route patterns should reuse this rule or explicitly extend it. |

## Fields Introduced

### Shared scheduling fields

All major Phase 06 records use `id`, `tenant_id`, `company_id`, optional `branch_id`, `status`, `source`, `external_refs`, `metadata`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, and `deleted_by` where soft deletion is supported.

### Task

`id`, `tenant_id`, `company_id`, `branch_id`, `title`, `description`, `category`, `type`, `status`, `priority`, `owner_user_id`, `assigned_user_id`, `assigned_team_id`, `created_from_module`, `source`, `related_record_type`, `related_record_id`, `related_record_refs`, `account_id`, `contact_id`, `lead_id`, `opportunity_id`, `prospect_id`, `campaign_id`, `outreach_enrollment_id`, `calendar_event_id`, `appointment_id`, `parent_task_id`, `recurrence_rule_id`, `due_at`, `start_at`, `completed_at`, `completed_by`, `cancelled_at`, `cancelled_by`, `snoozed_until`, `sla_policy_id`, `sla_due_at`, `sla_status`, `sla_breached_at`, `reminder_ids`, `checklist_items`, `tags`, `custom_fields`, `offline_client_id`, `sync_status`, `external_refs`, `metadata`.

### CalendarEvent

`id`, `tenant_id`, `company_id`, `branch_id`, `title`, `description`, `event_type`, `status`, `visibility`, `owner_user_id`, `organizer_user_id`, `assigned_user_id`, `assigned_team_id`, `start_at`, `end_at`, `timezone`, `all_day`, `location_text`, `location_address`, `coordinates`, `meeting_url`, `participant_user_ids`, `participant_contact_ids`, `participant_emails`, `related_record_type`, `related_record_id`, `related_record_refs`, `account_id`, `contact_id`, `lead_id`, `opportunity_id`, `site_id`, `job_id`, `work_order_id`, `appointment_id`, `recurrence_rule_id`, `reminder_ids`, `conflict_status`, `external_calendar_provider`, `external_calendar_id`, `external_event_id`, `external_refs`, `metadata`.

### Appointment

`id`, `tenant_id`, `company_id`, `branch_id`, `calendar_event_id`, `title`, `appointment_type`, `status`, `owner_user_id`, `assigned_user_id`, `assigned_team_id`, `account_id`, `contact_id`, `lead_id`, `opportunity_id`, `prospect_id`, `site_id`, `job_request_id`, `scheduled_start_at`, `scheduled_end_at`, `timezone`, `location_type`, `location_text`, `location_address`, `coordinates`, `meeting_url`, `customer_contact_ids`, `internal_participant_user_ids`, `confirmation_status`, `confirmed_at`, `cancelled_at`, `cancelled_by`, `cancellation_reason`, `completed_at`, `no_show_at`, `outcome`, `next_task_id`, `reminder_ids`, `external_refs`, `metadata`.

### Reminder

`id`, `tenant_id`, `company_id`, `user_id`, `target_type`, `target_id`, `task_id`, `calendar_event_id`, `appointment_id`, `reminder_type`, `trigger_at`, `relative_offset_minutes`, `channel`, `status`, `recipient_user_ids`, `recipient_membership_ids`, `notification_id`, `sent_at`, `snoozed_until`, `dismissed_at`, `failed_at`, `failure_reason`, `timezone`, `source`, `metadata`.

### RecurrenceRule

`id`, `tenant_id`, `company_id`, `target_type`, `target_template_id`, `frequency`, `interval`, `by_day`, `by_month_day`, `by_month`, `start_at`, `end_at`, `count`, `timezone`, `next_occurrence_at`, `last_generated_at`, `generation_window_days`, `exception_dates`, `modified_occurrence_refs`, `status`, `owner_user_id`, `created_by`, `updated_by`, `metadata`.

## APIs Introduced

- `GET /api/v1/tasks`
- `POST /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `PATCH /api/v1/tasks/{task_id}`
- `POST /api/v1/tasks/{task_id}/complete`
- `POST /api/v1/tasks/{task_id}/reopen`
- `POST /api/v1/tasks/{task_id}/cancel`
- `POST /api/v1/tasks/{task_id}/assign`
- `POST /api/v1/tasks/{task_id}/snooze`
- `GET /api/v1/calendar/events`
- `POST /api/v1/calendar/events`
- `GET /api/v1/calendar/events/{calendar_event_id}`
- `PATCH /api/v1/calendar/events/{calendar_event_id}`
- `POST /api/v1/calendar/events/{calendar_event_id}/cancel`
- `POST /api/v1/calendar/events/{calendar_event_id}/reschedule`
- `GET /api/v1/calendar/availability`
- `GET /api/v1/appointments`
- `POST /api/v1/appointments`
- `GET /api/v1/appointments/{appointment_id}`
- `PATCH /api/v1/appointments/{appointment_id}`
- `POST /api/v1/appointments/{appointment_id}/confirm`
- `POST /api/v1/appointments/{appointment_id}/complete`
- `POST /api/v1/appointments/{appointment_id}/no-show`
- `POST /api/v1/appointments/{appointment_id}/cancel`
- `GET /api/v1/reminders`
- `POST /api/v1/reminders`
- `PATCH /api/v1/reminders/{reminder_id}`
- `POST /api/v1/reminders/{reminder_id}/snooze`
- `POST /api/v1/reminders/{reminder_id}/dismiss`
- `GET /api/v1/recurrence-rules`
- `POST /api/v1/recurrence-rules`
- `PATCH /api/v1/recurrence-rules/{recurrence_rule_id}`
- `POST /api/v1/recurrence-rules/{recurrence_rule_id}/generate`
- `POST /api/v1/calendar/sync-preview` as future integration support when external calendars are enabled.

## Permissions Introduced

- `calendar.task.view`
- `calendar.task.create`
- `calendar.task.update`
- `calendar.task.assign`
- `calendar.task.complete`
- `calendar.task.cancel`
- `calendar.task.reopen`
- `calendar.task.delete`
- `calendar.task.export`
- `calendar.event.view`
- `calendar.event.create`
- `calendar.event.update`
- `calendar.event.cancel`
- `calendar.event.reschedule`
- `calendar.event.view_private`
- `calendar.event.export`
- `calendar.appointment.view`
- `calendar.appointment.create`
- `calendar.appointment.update`
- `calendar.appointment.confirm`
- `calendar.appointment.complete`
- `calendar.appointment.cancel`
- `calendar.appointment.no_show`
- `calendar.reminder.view`
- `calendar.reminder.create`
- `calendar.reminder.update`
- `calendar.reminder.dismiss`
- `calendar.reminder.snooze`
- `calendar.recurrence.view`
- `calendar.recurrence.create`
- `calendar.recurrence.update`
- `calendar.recurrence.cancel`
- `calendar.availability.view`
- `calendar.analytics.view`
- `calendar.admin.manage_settings`

## UX Patterns Introduced

- Unified Calendar / Tasks workspace with tabs for My Tasks, Team Tasks, Calendar, Appointments, Reminders, Recurring Work, and Analytics.
- Permission-aware task board/table/list views with saved filters, bulk assignment, due-date grouping, priority indicators, overdue indicators, related record links, and mobile-friendly quick completion.
- Calendar day/week/month/agenda views with company/team/user filters, event type coloring, conflict warnings, private event redaction, and related record preview cards.
- Appointment scheduling flow that links customer/CRM records, chooses participants, validates time, creates a `CalendarEvent`, creates reminders, and optionally creates follow-up tasks.
- Reminder panel and notification-driven reminder actions for snooze, dismiss, open record, or mark task complete.
- Recurrence editor with frequency, interval, selected weekdays/month days, start/end limits, preview of generated instances, and exception handling.
- Empty states for no tasks, no scheduled events, no appointments, no reminders, and no recurrence rules, with permission-aware create actions.
- Error states for conflicting schedules, missing permissions, disabled module access, invalid recurrence rules, offline sync conflict, deleted related records, and reminder delivery failure.

## Reports or Dashboards Introduced

- My Task Health dashboard.
- Team Task Load dashboard.
- Overdue and SLA Risk report.
- Appointment Outcome report.
- Calendar Utilization report.
- Reminder Delivery report.
- Recurring Work Generation report.
- Cross-Module Follow-Up report.
- Manager Queue Health report.

## Notifications Introduced

- Task assigned.
- Task reassigned.
- Task due soon.
- Task overdue.
- Task completed by another user.
- SLA approaching breach.
- SLA breached.
- Calendar event invited.
- Calendar event updated.
- Calendar event cancelled.
- Appointment confirmation needed.
- Appointment confirmed.
- Appointment cancelled.
- Appointment no-show recorded.
- Reminder due.
- Reminder snoozed.
- Recurring task/event generation failed.

## Audit Events Introduced

- `calendar.task.created`, `.updated`, `.assigned`, `.reassigned`, `.completed`, `.reopened`, `.cancelled`, `.deleted`, `.snoozed`, `.sla_breached`.
- `calendar.event.created`, `.updated`, `.rescheduled`, `.cancelled`, `.participant_added`, `.participant_removed`, `.privacy_changed`.
- `calendar.appointment.created`, `.updated`, `.confirmed`, `.completed`, `.cancelled`, `.no_show`, `.rescheduled`.
- `calendar.reminder.created`, `.updated`, `.sent`, `.snoozed`, `.dismissed`, `.failed`.
- `calendar.recurrence_rule.created`, `.updated`, `.paused`, `.cancelled`, `.instance_generated`, `.generation_failed`, `.exception_added`.

## Integrations Introduced

- Future external calendar provider integration seam for Google Calendar and Microsoft 365/Outlook.
- Future email/SMS notification delivery hooks through the shared notification system.
- Future webhook events for task, event, appointment, reminder, and recurrence lifecycle changes.
- Future import/export support through `ImportJob` and `ExportJob` for tasks and calendar events.
- Future provider references must use `external_refs`, `external_calendar_provider`, `external_calendar_id`, and `external_event_id` rather than ad hoc fields.

## Dependencies Created

- Depends on Phase 01 product foundation for unified CRM plus operations platform direction.
- Depends on Phase 02 identity, tenancy, company, membership, role, permission, module enablement, and auditability rules.
- Depends on Phase 03 shared foundations for audit, notifications, files, tags, custom fields, saved views, search, imports, exports, settings, background jobs, API keys, and webhooks.
- Depends on Phase 04 CRM entities for related records and timeline context.
- Depends on Phase 05 Outbound Sales requirements to support outbound follow-ups as shared tasks.
- Creates dependencies for Phase 07+ field visits, dispatch assignments, service work orders, reminders, recurring work, offline mobile tasks, reporting, and notifications.

## Constraints Future Phases Must Respect

- Do not create module-specific task systems. Use `Task` with `category`, `type`, and related record references.
- Do not create module-specific appointment systems. Use `Appointment` linked to `CalendarEvent`.
- Do not bypass `Reminder` and `Notification` for due-work alerts.
- Do not store external calendar provider IDs in random fields; use `external_refs` and approved external calendar fields.
- Do not treat private calendar details as visible to all users; permission and privacy behavior must be preserved.
- Do not generate recurring instances without preserving the parent `RecurrenceRule` and exception history.
- Do not allow offline task updates to bypass server-side permission revalidation.
- Do not use custom fields to replace stable due-date, assignment, status, SLA, reminder, or recurrence fields.
- Do not expose MongoDB `_id` as a public API identifier.
- Do not allow reminders, exports, searches, reports, or notifications to leak records across tenant, company, module, branch, team, or permission boundaries.

## Open Questions Carried Forward

- Should MVP include native two-way Google Calendar and Microsoft 365 sync, or only integration-ready fields and manual calendar records?
- Should recurrence materialize future instances immediately for a limited window, generate just-in-time, or use a hybrid model?
- What is the final SLA policy entity owner: Calendar / Tasks, Core Platform, Service, or Reporting?
- Should appointment confirmation support customer-facing links in MVP, or remain internal/manual until a later portal phase?
- Should task priority use a fixed global enum or company-configurable priority labels?
- Should private events block availability while hiding details from unauthorized users?
- What conflict policy should apply when a user is assigned overlapping field, dispatch, service, and meeting events?
