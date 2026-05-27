# Summary for Future Phases

## Final Decisions Made

- Phase 05 defines Outbound Sales as the execution layer for prospect lists, prospects, campaigns, sequences, sequence steps, outreach enrollments, activity logging, follow-up queues, conversion tracking, and outbound analytics.
- Outbound Sales must build on Phase 04 CRM entities: `Account`, `Contact`, `Lead`, `Opportunity`, `Activity`, `Pipeline`, `PipelineStage`, and `AssignmentRule`.
- Outbound Sales must use Phase 03 shared services: `AuditLog`, `Notification`, `FileAttachment`, `Tag`, `TagAssignment`, `CustomFieldDefinition`, `CustomFieldValue`, `SavedView`, `SearchIndexRecord`, `ImportJob`, `ExportJob`, `SettingsDocument`, `BackgroundJob`, `ApiKey`, `WebhookEndpoint`, and `WebhookDelivery`.
- Every Outbound Sales record is tenant/company scoped with `tenant_id` and `company_id` unless explicitly platform-level configuration is approved later.
- `Prospect` is an outbound target record that may link to an existing `Lead`, `Contact`, or `Account`; it must not replace those CRM entities.
- `Campaign` represents an outbound initiative across target audience, channel mix, ownership, dates, goals, and performance metrics.
- `Sequence` is a reusable cadence definition. `SequenceStep` defines manual or integration-supported touchpoints inside a sequence.
- Phase 05 supports manual sequence execution first. Automated sending, dialer automation, LinkedIn automation, and advanced compliance automation are future-phase or integration-phase concerns unless explicitly approved.
- `OutreachEnrollment` is the source of truth for a target's participation in a campaign/sequence and its current step, pause/stop state, opt-out state, completion state, and conversion linkage.
- Calls, emails, SMS, and LinkedIn actions must be logged as specialized outbound activity records and must also produce or link to CRM `Activity` timeline entries where useful.
- `CallLog`, `EmailLog`, `SmsLog`, and `LinkedInActivity` are operational activity records for outbound reporting and channel-specific fields; they do not replace `Activity`.
- LinkedIn starts as manual activity logging only: profile view, connection request, message, comment, note, and follow-up. Native LinkedIn automation remains out of scope until confirmed.
- `FollowUpTask` should be implemented as canonical `Task` with `category = outbound_follow_up` when Phase 06 task foundations are available. In Phase 05 design, the outbound module may define required follow-up behavior and a thin outbound wrapper only if needed for sequence execution.
- Rep queues are saved, permission-aware operational views over enrollments, due steps, follow-up tasks, overdue work, replies, bounced records, opted-out records, and conversion opportunities.
- Conversion tracking must connect outbound activity to Lead qualification, Account/Contact creation or reuse, Opportunity creation, and campaign/sequence attribution.
- Opt-out, do-not-contact, bounce, invalid contact information, duplicate enrollment, and permission failures must be explicit statuses or error states, not silent failures.
- Imports must use `ImportJob`; exports must use `ExportJob`; saved filters must use `SavedView`; tags must use `Tag` and `TagAssignment`.
- Outbound analytics must be designed from the start and include activity volume, step completion, touch outcomes, reply rates, meeting/appointment creation, lead conversion, opportunity creation, revenue attribution, rep performance, list quality, and compliance exceptions.

## Entities Introduced

| Entity | Owner module | Scope | Purpose | Future phase rule |
| --- | --- | --- | --- | --- |
| `ProspectList` | Outbound Sales | Company-scoped | Segment/import container for outbound targets, source metadata, ownership, compliance context, and list quality. | Reuse for segmentation and imports; do not create separate list concepts for outbound. |
| `Prospect` | Outbound Sales | Company-scoped | Outbound target that may link to `Lead`, `Contact`, or `Account` and can be enrolled into campaigns/sequences. | Must not replace Lead, Contact, or Account. Use links when records already exist. |
| `Campaign` | Outbound Sales | Company-scoped | Outbound initiative with audience, channel mix, ownership, schedule, goals, and performance tracking. | Reporting, integrations, and attribution should reference Campaign where available. |
| `Sequence` | Outbound Sales | Company-scoped | Reusable cadence definition for multi-step outbound execution. | Future automation must preserve this entity and add automation metadata rather than replacing it. |
| `SequenceStep` | Outbound Sales | Company-scoped child of Sequence | Ordered step defining channel, delay, task type, instructions, and optional template references. | Future providers may attach templates or automation settings without changing step identity. |
| `OutreachEnrollment` | Outbound Sales | Company-scoped | Enrollment of a Prospect/Lead/Contact into a Campaign/Sequence with current progress and stop reasons. | Source of truth for sequence participation and conversion attribution. |
| `CallLog` | Outbound Sales | Company-scoped append/activity record | Logged outbound or inbound phone call outcome, disposition, notes, and follow-up. | Must link to CRM Activity for timelines when relevant. |
| `EmailLog` | Outbound Sales | Company-scoped append/activity record | Logged email outreach/reply metadata, participants, provider references, and delivery/reply state. | Do not store sensitive full email body by default unless integration policy approves. |
| `SmsLog` | Outbound Sales | Company-scoped append/activity record | Logged SMS outreach/reply metadata, phone number, provider references, status, and compliance state. | Must honor opt-out and phone compliance states. |
| `LinkedInActivity` | Outbound Sales | Company-scoped append/activity record | Manual LinkedIn activity log for profile views, connection requests, messages, comments, notes, and follow-ups. | Native automation remains out of scope until explicitly approved. |
| `FollowUpTask` | Outbound Sales / Calendar & Tasks | Company-scoped | Outbound follow-up action generated manually or by sequence step. | Implement as `Task` with `category = outbound_follow_up` when Phase 06 exists; avoid duplicate task systems. |

## Fields Introduced

### Shared outbound fields

All Phase 05 company-scoped records use `id`, `tenant_id`, `company_id`, optional `branch_id`, `owner_user_id`, `assigned_user_id` where applicable, `status`, `source`, `external_refs`, `metadata`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, and `deleted_by` where soft deletion is supported.

### ProspectList

`id`, `tenant_id`, `company_id`, `name`, `description`, `source`, `source_detail`, `owner_user_id`, `assigned_team_id`, `segment_rules`, `import_job_id`, `file_attachment_id`, `tag_ids`, `prospect_count`, `active_prospect_count`, `invalid_count`, `duplicate_count`, `opted_out_count`, `compliance_basis`, `consent_source`, `default_campaign_id`, `status`, `created_at`, `created_by`, `updated_at`, `updated_by`, `archived_at`, `archived_by`, `metadata`.

### Prospect

`id`, `tenant_id`, `company_id`, `prospect_list_id`, `lead_id`, `contact_id`, `account_id`, `first_name`, `last_name`, `display_name`, `company_name`, `title`, `email`, `email_normalized`, `phone`, `phone_normalized`, `linkedin_url`, `website`, `industry`, `address`, `timezone`, `source`, `source_detail`, `owner_user_id`, `assigned_user_id`, `assigned_team_id`, `status`, `engagement_status`, `qualification_status`, `do_not_contact`, `do_not_contact_reason`, `opted_out_channels`, `last_contacted_at`, `last_engaged_at`, `next_follow_up_at`, `converted_lead_id`, `converted_account_id`, `converted_contact_id`, `converted_opportunity_id`, `external_refs`, `metadata`.

### Campaign

`id`, `tenant_id`, `company_id`, `name`, `description`, `owner_user_id`, `assigned_team_id`, `prospect_list_ids`, `sequence_ids`, `channel_mix`, `target_filters`, `goal_type`, `goal_value`, `start_at`, `end_at`, `status`, `paused_reason`, `completed_at`, `metrics_snapshot`, `metadata`.

### Sequence

`id`, `tenant_id`, `company_id`, `name`, `description`, `owner_user_id`, `channel_mix`, `status`, `step_count`, `default_timezone`, `business_hours_policy`, `exit_rules`, `pause_rules`, `metadata`.

### SequenceStep

`id`, `tenant_id`, `company_id`, `sequence_id`, `step_number`, `name`, `channel`, `step_type`, `delay_days`, `delay_hours`, `due_time_policy`, `instructions`, `template_ref`, `requires_manual_completion`, `skip_if_no_channel`, `success_outcomes`, `failure_outcomes`, `status`, `metadata`.

### OutreachEnrollment

`id`, `tenant_id`, `company_id`, `campaign_id`, `sequence_id`, `prospect_id`, `target_type`, `target_id`, `owner_user_id`, `assigned_user_id`, `current_step_id`, `current_step_number`, `status`, `enrolled_at`, `started_at`, `paused_at`, `pause_reason`, `completed_at`, `stopped_at`, `stop_reason`, `next_step_due_at`, `last_activity_at`, `last_activity_type`, `last_outcome`, `reply_detected_at`, `converted_at`, `converted_entity_refs`, `metadata`.

### CallLog

`id`, `tenant_id`, `company_id`, `prospect_id`, `lead_id`, `contact_id`, `account_id`, `outreach_enrollment_id`, `campaign_id`, `sequence_id`, `sequence_step_id`, `activity_id`, `task_id`, `direction`, `phone_number`, `phone_normalized`, `started_at`, `ended_at`, `duration_seconds`, `occurred_at`, `actor_user_id`, `outcome`, `disposition`, `voicemail_left`, `notes`, `next_step`, `callback_at`, `status`, `external_refs`, `metadata`.

### EmailLog

`id`, `tenant_id`, `company_id`, `prospect_id`, `lead_id`, `contact_id`, `account_id`, `outreach_enrollment_id`, `campaign_id`, `sequence_id`, `sequence_step_id`, `activity_id`, `direction`, `subject`, `participants`, `from_email`, `to_emails`, `cc_emails`, `bcc_emails`, `provider_message_id`, `provider_thread_id`, `occurred_at`, `sent_at`, `delivered_at`, `opened_at`, `replied_at`, `bounced_at`, `failed_at`, `status`, `body_preview`, `external_refs`, `metadata`.

### SmsLog

`id`, `tenant_id`, `company_id`, `prospect_id`, `lead_id`, `contact_id`, `account_id`, `outreach_enrollment_id`, `campaign_id`, `sequence_id`, `sequence_step_id`, `activity_id`, `direction`, `phone_number`, `phone_normalized`, `body_preview`, `provider_message_id`, `occurred_at`, `sent_at`, `delivered_at`, `replied_at`, `failed_at`, `status`, `opt_out_detected`, `compliance_status`, `external_refs`, `metadata`.

### LinkedInActivity

`id`, `tenant_id`, `company_id`, `prospect_id`, `lead_id`, `contact_id`, `account_id`, `outreach_enrollment_id`, `campaign_id`, `sequence_id`, `sequence_step_id`, `activity_id`, `actor_user_id`, `activity_subtype`, `profile_url`, `subject`, `notes`, `outcome`, `occurred_at`, `needs_follow_up`, `follow_up_due_at`, `status`, `metadata`.

### FollowUpTask

`id`, `tenant_id`, `company_id`, `task_id`, `outreach_enrollment_id`, `prospect_id`, `lead_id`, `contact_id`, `account_id`, `campaign_id`, `sequence_id`, `sequence_step_id`, `assigned_user_id`, `assigned_team_id`, `due_at`, `priority`, `channel`, `reason`, `status`, `completed_at`, `skipped_at`, `skip_reason`, `metadata`. Preferred implementation is a `Task` record with outbound references and category `outbound_follow_up`.

## APIs Introduced

- `GET /api/v1/outbound/prospect-lists`
- `POST /api/v1/outbound/prospect-lists`
- `GET /api/v1/outbound/prospect-lists/{prospect_list_id}`
- `PATCH /api/v1/outbound/prospect-lists/{prospect_list_id}`
- `POST /api/v1/outbound/prospect-lists/{prospect_list_id}/archive`
- `POST /api/v1/outbound/prospect-lists/{prospect_list_id}/import`
- `GET /api/v1/outbound/prospects`
- `POST /api/v1/outbound/prospects`
- `GET /api/v1/outbound/prospects/{prospect_id}`
- `PATCH /api/v1/outbound/prospects/{prospect_id}`
- `POST /api/v1/outbound/prospects/{prospect_id}/convert`
- `POST /api/v1/outbound/prospects/{prospect_id}/do-not-contact`
- `GET /api/v1/outbound/campaigns`
- `POST /api/v1/outbound/campaigns`
- `GET /api/v1/outbound/campaigns/{campaign_id}`
- `PATCH /api/v1/outbound/campaigns/{campaign_id}`
- `POST /api/v1/outbound/campaigns/{campaign_id}/start`
- `POST /api/v1/outbound/campaigns/{campaign_id}/pause`
- `POST /api/v1/outbound/campaigns/{campaign_id}/complete`
- `GET /api/v1/outbound/sequences`
- `POST /api/v1/outbound/sequences`
- `GET /api/v1/outbound/sequences/{sequence_id}`
- `PATCH /api/v1/outbound/sequences/{sequence_id}`
- `POST /api/v1/outbound/sequences/{sequence_id}/steps`
- `PATCH /api/v1/outbound/sequences/{sequence_id}/steps/{sequence_step_id}`
- `POST /api/v1/outbound/enrollments`
- `GET /api/v1/outbound/enrollments`
- `PATCH /api/v1/outbound/enrollments/{outreach_enrollment_id}`
- `POST /api/v1/outbound/enrollments/{outreach_enrollment_id}/pause`
- `POST /api/v1/outbound/enrollments/{outreach_enrollment_id}/resume`
- `POST /api/v1/outbound/enrollments/{outreach_enrollment_id}/stop`
- `POST /api/v1/outbound/enrollments/{outreach_enrollment_id}/complete-step`
- `POST /api/v1/outbound/call-logs`
- `POST /api/v1/outbound/email-logs`
- `POST /api/v1/outbound/sms-logs`
- `POST /api/v1/outbound/linkedin-activities`
- `GET /api/v1/outbound/rep-queue`
- `GET /api/v1/outbound/analytics/*` for approved dashboard endpoints.

## Permissions Introduced

- `outbound.prospect_list.view`
- `outbound.prospect_list.create`
- `outbound.prospect_list.update`
- `outbound.prospect_list.archive`
- `outbound.prospect_list.import`
- `outbound.prospect.view`
- `outbound.prospect.create`
- `outbound.prospect.update`
- `outbound.prospect.archive`
- `outbound.prospect.convert`
- `outbound.prospect.do_not_contact`
- `outbound.campaign.view`
- `outbound.campaign.create`
- `outbound.campaign.update`
- `outbound.campaign.start`
- `outbound.campaign.pause`
- `outbound.campaign.complete`
- `outbound.sequence.view`
- `outbound.sequence.create`
- `outbound.sequence.update`
- `outbound.sequence.archive`
- `outbound.enrollment.view`
- `outbound.enrollment.create`
- `outbound.enrollment.update`
- `outbound.enrollment.pause_resume`
- `outbound.enrollment.stop`
- `outbound.activity.log_call`
- `outbound.activity.log_email`
- `outbound.activity.log_sms`
- `outbound.activity.log_linkedin`
- `outbound.follow_up.view`
- `outbound.follow_up.manage`
- `outbound.analytics.view`
- `outbound.export`
- `outbound.admin.manage_settings`

## UX Patterns Introduced

- Outbound workspace with tabs or routes for Rep Queue, Prospect Lists, Prospects, Campaigns, Sequences, Activity Logs, and Analytics.
- Prospect List import flow using `ImportJob`, validation preview, duplicate summary, invalid-row review, and import result page.
- Prospect detail page with CRM links, timeline, enrollments, contact methods, compliance state, next action, and conversion actions.
- Campaign detail page with status header, audience summary, sequences, performance metrics, enrollment table, activity feed, and controls for start/pause/complete.
- Sequence builder with ordered steps, channel selection, delay rules, manual instructions, template references, preview, and validation warnings.
- Rep Queue showing due steps, overdue follow-ups, replies, recently engaged prospects, callback tasks, and priority work.
- Activity logging drawers for call, email, SMS, and LinkedIn activity with outcome, notes, next step, and follow-up creation.
- Conversion flow that reuses or creates Lead, Contact, Account, and Opportunity according to CRM rules and duplicate checks.
- Permission-aware empty states, disabled controls, redacted records, and export restrictions.

## Reports or Dashboards Introduced

- Outbound Overview Dashboard.
- Rep Activity Dashboard.
- Campaign Performance Dashboard.
- Sequence Performance Dashboard.
- Prospect List Quality Report.
- Follow-up Queue Health Report.
- Conversion Attribution Report.
- Channel Performance Report.
- Compliance Exceptions Report.
- Manager Coaching Report.

## Notifications Introduced

- Follow-up due soon.
- Follow-up overdue.
- Enrollment reply detected where provider integration exists.
- Campaign started, paused, completed, or failed validation.
- Prospect assigned or reassigned.
- Sequence step due.
- Import completed, partially failed, or failed.
- Export completed or failed.
- Do-not-contact or opt-out detected.
- Conversion completed or failed.

## Audit Events Introduced

- `outbound.prospect_list.created`, `.updated`, `.archived`, `.import_started`, `.import_completed`.
- `outbound.prospect.created`, `.updated`, `.archived`, `.do_not_contact_set`, `.converted`.
- `outbound.campaign.created`, `.updated`, `.started`, `.paused`, `.completed`, `.archived`.
- `outbound.sequence.created`, `.updated`, `.archived`.
- `outbound.sequence_step.created`, `.updated`, `.reordered`, `.archived`.
- `outbound.enrollment.created`, `.paused`, `.resumed`, `.stopped`, `.step_completed`, `.completed`, `.converted`.
- `outbound.call_log.created`, `.corrected`, `.archived`.
- `outbound.email_log.created`, `.status_updated`, `.archived`.
- `outbound.sms_log.created`, `.status_updated`, `.opt_out_detected`, `.archived`.
- `outbound.linkedin_activity.created`, `.corrected`, `.archived`.
- `outbound.follow_up.created`, `.completed`, `.skipped`, `.reassigned`.
- `outbound.export_requested`, `.settings_updated`.

## Integrations Introduced

- CSV/Excel import for Prospect Lists through `ImportJob` and `FileAttachment`.
- CSV/Excel export through `ExportJob` with permission checks and audit logging.
- Email provider references are supported through `external_refs.email_provider` and provider message/thread IDs, but full automated sending can be deferred.
- SMS provider references are supported through `external_refs.sms_provider` and provider message IDs, but automated sending and compliance handling must be confirmed in the integrations phase.
- LinkedIn is manual logging only; no native automation or scraping is introduced.
- Webhook events may be emitted later for prospect created/updated, campaign status changed, enrollment changed, activity logged, opt-out detected, and conversion completed.

## Dependencies Created

- Depends on Phase 01 product definition and MVP boundaries.
- Depends on Phase 02 tenant, company, user, membership, role, permission, and module access rules.
- Depends on Phase 03 shared services for audit, notifications, files, tags, saved views, imports, exports, settings, search, and background jobs.
- Depends on Phase 04 CRM data model for Lead, Account, Contact, Opportunity, Activity, AssignmentRule, and CRM timeline behavior.
- Creates dependencies for Phase 06 Calendar and Task System because outbound follow-up tasks should use canonical `Task`.
- Creates dependencies for reporting phases because outbound activity, conversion, and attribution events must be reportable.
- Creates dependencies for integrations phases because email/SMS/LinkedIn provider behavior must respect Phase 05 records.

## Constraints Future Phases Must Respect

- Do not create separate outbound-only replacements for Lead, Contact, Account, Opportunity, Activity, Task, Tag, ImportJob, ExportJob, SavedView, Notification, or AuditLog.
- Do not treat Company as a CRM prospect or customer record; use Account/Lead/Contact/Prospect as appropriate.
- Do not implement native LinkedIn automation without a new explicit decision.
- Do not bypass opt-out, do-not-contact, bounce, or invalid-channel states when enrolling or advancing prospects.
- Do not create automated sending behavior that cannot produce activity logs, status updates, audit records, and provider error visibility.
- Do not allow exports, analytics, saved views, or search to bypass tenant/company/module/permission filtering.
- Do not store raw API keys, provider secrets, or sensitive message content outside approved integration/security patterns.
- Preserve conversion attribution from prospect/list/campaign/sequence/enrollment/activity to Lead, Account, Contact, and Opportunity.
- Keep sequence steps stable enough for historical enrollments; changing a sequence must not rewrite completed activity history.

## Open Questions Carried Forward

- Should Phase 05 introduce a persistent `FollowUpTask` wrapper, or should all follow-up behavior wait for canonical `Task` in Phase 06?
- Which email provider, if any, is MVP for sending, reply detection, bounce handling, and thread sync?
- Which SMS provider, if any, is MVP for sending, replies, delivery receipts, and opt-out detection?
- What exact compliance rules are required for outbound email and SMS in target launch markets?
- Should sequence templates be their own canonical entity in a later phase, or remain `template_ref` references for now?
- Should Campaign support budget/cost attribution in MVP, or should cost analytics be deferred?
- Should prospects be allowed in multiple active campaigns at the same time, or should company settings restrict concurrency?
- Should conversion create Opportunity directly or require Lead qualification first by default?
- What retention policy applies to body previews, message metadata, and provider status history?
- What outbound metrics are required for the first launch dashboard versus later analytics expansion?
