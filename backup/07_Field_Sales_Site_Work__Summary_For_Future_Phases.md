# Summary for Future Phases

## Final Decisions Made

- Phase 07 establishes Field Sales / Site Work as the canonical foundation for Sites, SiteVisits, check-ins/check-outs, FieldNotes, FieldPhotos, JobRequests, Jobs, JobStages, Crews, EquipmentAssignments, territory coverage, site outcomes, and mobile field capture.
- `Site` is the canonical physical customer or operational location. Future phases must not create duplicate concepts such as CustomerSite, FieldLocation, JobLocation, or ServiceLocation when `Site` covers the meaning.
- `SiteVisit` is the canonical scheduled or completed visit to a Site. It may link to CalendarEvent and Appointment but must not replace them.
- `CheckInEvent` and `CheckOutEvent` are append-only operational event records and are offline-capable.
- `FieldNote` is the canonical structured field-captured note for Site, SiteVisit, Job, and JobRequest contexts.
- `FieldPhoto` is a metadata wrapper around canonical `FileAttachment`; it must not store binary file content directly.
- `JobRequest` is the canonical sales/field-to-operations handoff request before work becomes a scheduled Job.
- `Job` is the generic operational work record for scheduled field work. Drilling, dispatch, service, fleet, inventory, reporting, and QuickBooks phases must extend or reference it rather than replacing it.
- `JobStage` is the canonical ordered checkpoint/stage inside a Job.
- `Crew` is the canonical field resource group made of Users.
- `EquipmentAssignment` is the canonical assignment of equipment, vehicle, drilling equipment, or resource to a Job, Crew, SiteVisit, or time window.
- All Phase 07 records must use tenant/company scoping and stable application IDs; MongoDB `_id` must not be exposed as the public API ID.
- Phase 07 must reuse Core Platform services for AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, SettingsDocument, BackgroundJob, ApiKey, WebhookEndpoint, and WebhookDelivery.
- Phase 07 must reuse CRM records for Account, Contact, Lead, Opportunity, Activity, Pipeline context, and AssignmentRule where applicable.
- Phase 07 must reuse Calendar / Tasks records for Task, CalendarEvent, Appointment, Reminder, and RecurrenceRule instead of creating duplicate task or scheduling systems.

## Entities Introduced

| Entity | Owner | Scope | Purpose | Future Phase Rule |
| --- | --- | --- | --- | --- |
| `Site` | Field Sales / Site Work | Company-scoped, optional branch/territory | Physical customer or operational location. | Reuse for dispatch stops, service locations, drilling sites, job locations, delivery locations, and geofences. |
| `SiteVisit` | Field Sales / Site Work | Company-scoped | Scheduled or completed visit to a Site. | Link to CalendarEvent/Appointment; do not create duplicate visit systems. |
| `CheckInEvent` | Field Sales / Site Work | Company-scoped append-only event | User/location check-in event with offline metadata. | Reuse for field proof, geofence, mobile, reporting, fleet, and job attendance context. |
| `CheckOutEvent` | Field Sales / Site Work | Company-scoped append-only event | User/location check-out event with offline metadata. | Reuse for duration, completion proof, and visit/job attendance context. |
| `FieldNote` | Field Sales / Site Work | Company-scoped | Structured field note linked to Site, SiteVisit, Job, or JobRequest. | Reuse for field, drilling, dispatch, and service notes where field capture is needed. |
| `FieldPhoto` | Field Sales / Site Work | Company-scoped | Photo metadata wrapper linked to FileAttachment. | Reuse for field evidence; do not create separate photo binaries per module. |
| `JobRequest` | Field Sales / Site Work | Company-scoped | Request for operational work before scheduling. | Reuse for sales-to-ops and field-to-ops handoffs. |
| `Job` | Field Sales / Site Work | Company-scoped | Generic operational work record. | DrillingJob and later operational extensions must reference Job. |
| `JobStage` | Field Sales / Site Work | Company-scoped child of Job | Ordered checkpoint/stage inside a Job. | Reuse for job progress and required evidence checks. |
| `Crew` | Field Sales / Site Work | Company-scoped | Group of Users assigned to field work. | Reuse for dispatch, drilling, fleet, service, and reporting resource context. |
| `EquipmentAssignment` | Field Sales / Site Work | Company-scoped | Assignment of resources/equipment/vehicles to work. | Reuse for future drilling equipment, fleet assets, inventory tools, and job planning. |

## Fields Introduced

- Shared fields: `id`, `tenant_id`, `company_id`, optional `branch_id`, optional `territory_id`, `status`, `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`, `deleted_by`, `metadata`, `external_refs` where relevant.
- `Site`: `account_id`, `primary_contact_id`, `name`, `site_code`, `address`, `coordinates`, `access_notes`, `hazard_notes`, `timezone`, `owner_user_id`.
- `SiteVisit`: `site_id`, `account_id`, `contact_ids`, `assigned_user_id`, `assigned_team_id`, `calendar_event_id`, `appointment_id`, `purpose`, `scheduled_start_at`, `scheduled_end_at`, `actual_start_at`, `actual_end_at`, `outcome`, `next_action`, `follow_up_task_id`, `offline_sync_state`.
- `CheckInEvent` / `CheckOutEvent`: `user_id`, `membership_id`, `entity_type`, `entity_id`, `site_id`, `site_visit_id`, `job_id`, `occurred_at`, `coordinates`, `geofence_status`, `distance_from_site_meters`, `device_id`, `captured_offline`, `offline_created_at`, `offline_sync_state`, `sync_error_code`.
- `FieldNote`: `entity_type`, `entity_id`, `site_id`, `site_visit_id`, `job_id`, `job_request_id`, `author_user_id`, `category`, `body`, `visibility`, `follow_up_required`, `follow_up_task_id`, `activity_id`, `captured_offline`, `offline_sync_state`.
- `FieldPhoto`: `file_attachment_id`, `entity_type`, `entity_id`, `site_id`, `site_visit_id`, `job_id`, `captured_by_user_id`, `captured_at`, `coordinates`, `caption`, `category`, `review_status`, `captured_offline`, `offline_sync_state`.
- `JobRequest`: `account_id`, `site_id`, `opportunity_id`, `source`, `requested_by_user_id`, `requester_contact_id`, `priority`, `scope`, `requested_date`, `due_date`, `constraints`, `required_equipment`, `estimated_value`, `converted_job_id`, `rejection_reason`.
- `Job`: `account_id`, `site_id`, `job_request_id`, `opportunity_id`, `job_number`, `job_type`, `priority`, `scheduled_start_at`, `scheduled_end_at`, `actual_start_at`, `actual_end_at`, `owner_user_id`, `crew_id`, `primary_contact_id`, `readiness_status`, `completion_summary`, `blocked_reason`.
- `JobStage`: `job_id`, `name`, `code`, `sort_order`, `required`, `requires_photo`, `requires_note`, `assigned_user_id`, `started_at`, `completed_at`, `skipped_reason`.
- `Crew`: `name`, `lead_user_id`, `member_user_ids`, `branch_id`, `territory_id`, `availability_status`, `default_vehicle_id`, `notes`.
- `EquipmentAssignment`: `equipment_type`, `equipment_id`, `assigned_to_type`, `assigned_to_id`, `job_id`, `crew_id`, `site_visit_id`, `start_at`, `end_at`, `planned_by_user_id`, `checked_out_by_user_id`, `checked_in_by_user_id`, `condition_out`, `condition_in`.

## APIs Introduced

- `/api/v1/sites`
- `/api/v1/site-visits`
- `/api/v1/check-in-events`
- `/api/v1/check-out-events`
- `/api/v1/field-notes`
- `/api/v1/field-photos`
- `/api/v1/job-requests`
- `/api/v1/jobs`
- `/api/v1/jobs/{job_id}/stages`
- `/api/v1/crews`
- `/api/v1/equipment-assignments`
- Required action endpoints: schedule, reschedule, check-in, check-out, complete, cancel, mark-missed, triage, approve, reject, convert-to-job, assign-crew, assign-equipment, start, block, unblock, complete-job, cancel-job.

## Permissions Introduced

- `field.site.view`, `field.site.create`, `field.site.update`, `field.site.archive`, `field.site.export`
- `field.site_visit.view`, `field.site_visit.create`, `field.site_visit.update`, `field.site_visit.cancel`, `field.site_visit.check_in`, `field.site_visit.check_out`, `field.site_visit.export`
- `field.field_note.view`, `field.field_note.create`, `field.field_note.update_own`, `field.field_note.archive`, `field.field_note.view_private`
- `field.field_photo.view`, `field.field_photo.create`, `field.field_photo.archive`, `field.field_photo.review`, `field.field_photo.export`
- `field.job_request.view`, `field.job_request.create`, `field.job_request.triage`, `field.job_request.approve`, `field.job_request.reject`, `field.job_request.convert`, `field.job_request.export`
- `field.job.view`, `field.job.create`, `field.job.schedule`, `field.job.update`, `field.job.start`, `field.job.block`, `field.job.complete`, `field.job.cancel`, `field.job.archive`, `field.job.export`
- `field.crew.view`, `field.crew.manage`, `field.crew.assign`, `field.crew.archive`
- `field.equipment_assignment.view`, `field.equipment_assignment.manage`, `field.equipment_assignment.override_conflict`, `field.equipment_assignment.export`

## UX Patterns Introduced

- Site list/table/map views with saved filters.
- Site detail page with site header, account/contact links, map card, access/hazard cards, visits, jobs, notes, photos, files, tasks, timeline, and audit summary.
- SiteVisit queue for due, overdue, upcoming, in-progress, missed, completed, and needs-follow-up visits.
- Mobile-first SiteVisit execution screen with directions, hazards, contact info, check-in, note/photo capture, check-out, and sync state.
- JobRequest triage board/list.
- Job detail workspace with stages, schedule, crew, equipment, blockers, notes/photos, and completion summary.
- Crew roster and assignment view.
- Equipment assignment conflict warning pattern.
- Permission-aware empty, disabled, error, and offline states.

## Reports or Dashboards Introduced

- Site coverage by account, owner, territory, last visit, next visit, and status.
- Visit completion and missed-visit dashboard.
- Check-in/check-out compliance and geofence variance report.
- Field notes/photos evidence report.
- JobRequest funnel report.
- Job status and blocked jobs report.
- Crew utilization and equipment conflict report.

## Notifications Introduced

- SiteVisit assigned/rescheduled.
- SiteVisit overdue/missed.
- SiteVisit outcome requires follow-up.
- New JobRequest created.
- JobRequest approved/rejected/converted.
- Job scheduled/rescheduled/blocked/unblocked/cancelled.
- Equipment assignment conflict or overdue return.

## Audit Events Introduced

- Site create/update/archive/restore and high-impact address/coordinate/access/hazard changes.
- SiteVisit schedule/assignment/status/cancel/missed/complete events.
- CheckInEvent and CheckOutEvent creation/rejection/correction metadata.
- FieldNote create/edit/visibility/archive/follow-up task creation.
- FieldPhoto upload/review rejection/archive/attachment-related actions.
- JobRequest create/triage/approve/reject/convert/priority/archive.
- Job create/schedule/assign/start/block/unblock/complete/cancel/archive.
- JobStage complete/skip/override/evidence changes.
- Crew membership and lead changes.
- EquipmentAssignment create/activate/complete/cancel/conflict override/condition changes.

## Integrations Introduced

- CRM integration through Account, Contact, Lead, Opportunity, Activity, Task, CalendarEvent, Appointment, and AssignmentRule.
- Core Platform integration through AuditLog, Notification, FileAttachment, Tag, TagAssignment, CustomFieldDefinition, CustomFieldValue, SavedView, SearchIndexRecord, ImportJob, ExportJob, SettingsDocument, BackgroundJob, ApiKey, WebhookEndpoint, and WebhookDelivery.
- Future geofencing/fleet linkage through Site, CheckInEvent, CheckOutEvent, SiteVisit, Job, Geofence, and GeofenceEvent.
- Future drilling linkage through Job, Site, JobStage, Crew, EquipmentAssignment, FieldNote, and FieldPhoto.
- Future dispatch/logistics linkage through Site, Job, Crew, EquipmentAssignment, scheduled windows, and status transitions.
- Future service linkage through Site, Job, FieldNote, FieldPhoto, ServiceRequest, and WorkOrder.
- Future QuickBooks context through Account, Job, Site, completion state, and billing readiness metadata, without making QuickBooks the operational source of truth.

## Dependencies Created

- Depends on Phase 01 product foundation and MVP scope.
- Depends on Phase 02 tenant/company/UserMembership/Role/Permission/module enablement rules.
- Depends on Phase 03 Core Platform shared services.
- Depends on Phase 04 CRM canonical Account, Contact, Lead, Opportunity, Activity, and AssignmentRule.
- Depends on Phase 05 Outbound Sales for outbound-generated site visit and opportunity handoff context.
- Depends on Phase 06 Calendar / Tasks for Task, CalendarEvent, Appointment, Reminder, and RecurrenceRule.

## Constraints Future Phases Must Respect

- Do not create duplicate Site, JobRequest, Job, Crew, EquipmentAssignment, check-in, check-out, field note, or field photo concepts.
- Drilling-specific entities must extend or reference Job; they must not replace the generic Job.
- Service WorkOrder may connect to Job and Site but must not replace Job for generic field operations.
- Dispatch and logistics must use Site and Job references where field work location and operational work already exist.
- Fleet/geofencing must link geofence evidence to Site, SiteVisit, Job, CheckInEvent, and CheckOutEvent where applicable.
- Reporting must remain permission-aware and tenant/company scoped.
- Offline sync must revalidate permissions and module access before accepting queued field actions.
- FieldPhoto must continue to use FileAttachment for file storage and access control.
- Field activity that matters to customer history should create or link to CRM Activity where useful.

## Open Questions Carried Forward

- Confirm whether territory is represented as a standalone `Territory` entity, a configuration value, or a field controlled by AssignmentRule in a later phase.
- Confirm whether geofence validation is enforced in Phase 07 MVP or only captured for future Fleet / GPS / Geofencing behavior.
- Confirm whether Job numbers are system-generated, company-configurable, or manually allowed with uniqueness validation.
- Confirm whether Crew availability is manually maintained in Phase 07 or derived from CalendarEvent and Job assignments later.
- Confirm whether EquipmentAssignment can reference generic assets before Fleet, Inventory, and DrillingEquipment phases are fully defined.
- Confirm retention and privacy rules for location history, device metadata, and field photos.
- Confirm whether customer-facing visit/job summaries are needed before a future customer portal phase.
