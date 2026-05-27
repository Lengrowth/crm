# Phase 04–20 Documentation Prompts

This Markdown file contains ready-to-paste prompts for generating Phase 04 through Phase 20 of the documentation set.

## General Workflow Reminder

For every phase from Phase 04 onward, provide the next AI with:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. All prior `__Summary_For_Future_Phases.md` files
6. The relevant phase prompt from this file

Do not keep sending all full previous phase documents forever. Send the global control documents plus prior summary files.

Every phase prompt below requires two downloadable Markdown outputs:

1. The full phase document.
2. The phase summary for future phases.

---

## Phase 04 Prompt — CRM Data Model

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 03

Your task is to create the Phase 04 document:

# 04_CRM_Data_Model.md

You must also create a separate future-phase summary file:

# 04_CRM_Data_Model__Summary_For_Future_Phases.md

Important:
- Do not create Phase 05.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `04_CRM_Data_Model.md`
- Name the summary file exactly: `04_CRM_Data_Model__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 04 design level.


Your goal:
Create a complete Phase 04 CRM Data Model document that defines CRM foundation: Accounts, Contacts, Leads, Opportunities, Pipelines, Pipeline Stages, Activities, Notes, Comments, Relationship Maps, Assignment Rules, CRM ownership, lifecycle, filters, permissions, audit, and reporting.

This phase must define or expand these entities where relevant:

- Account
- Contact
- Lead
- Opportunity
- Pipeline
- PipelineStage
- Activity
- Note
- Comment
- RelationshipMap
- AssignmentRule

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-04-001`.
- Functional requirements must use IDs like `FR-04-001`.
- Non-functional requirements must use IDs like `NFR-04-001`.
- API requirements must use IDs like `API-04-001`.
- UX requirements must use IDs like `UX-04-001`.
- Permission requirements must use IDs like `PERM-04-001`.
- Audit requirements must use IDs like `AUDIT-04-001`.
- Reporting requirements must use IDs like `REPORT-04-001`.
- Notification requirements must use IDs like `NOTIF-04-001`.
- Integration requirements must use IDs like `INT-04-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-04-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Phase 05 Outbound Sales must build on Lead, Contact, Account, Opportunity, Activity, and AssignmentRule. Later field, dispatch, service, reporting, and integration phases must reuse Account/Contact/Opportunity instead of inventing customer entities.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 04 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`04_CRM_Data_Model__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `04_CRM_Data_Model.md`.
- Create and provide a second downloadable Markdown file named exactly `04_CRM_Data_Model__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 05 Prompt — Outbound Sales

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 04

Your task is to create the Phase 05 document:

# 05_Outbound_Sales.md

You must also create a separate future-phase summary file:

# 05_Outbound_Sales__Summary_For_Future_Phases.md

Important:
- Do not create Phase 06.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `05_Outbound_Sales.md`
- Name the summary file exactly: `05_Outbound_Sales__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 05 design level.


Your goal:
Create a complete Phase 05 Outbound Sales document that defines outbound sales operations: Prospect Lists, Prospects, Campaigns, Sequences, Sequence Steps, Outreach Enrollments, Call Logs, Email Logs, SMS Logs, LinkedIn Activity logging, Follow-up Tasks, rep queues, conversion tracking, and outbound analytics.

This phase must define or expand these entities where relevant:

- ProspectList
- Prospect
- Campaign
- Sequence
- SequenceStep
- OutreachEnrollment
- CallLog
- EmailLog
- SmsLog
- LinkedInActivity
- FollowUpTask

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-05-001`.
- Functional requirements must use IDs like `FR-05-001`.
- Non-functional requirements must use IDs like `NFR-05-001`.
- API requirements must use IDs like `API-05-001`.
- UX requirements must use IDs like `UX-05-001`.
- Permission requirements must use IDs like `PERM-05-001`.
- Audit requirements must use IDs like `AUDIT-05-001`.
- Reporting requirements must use IDs like `REPORT-05-001`.
- Notification requirements must use IDs like `NOTIF-05-001`.
- Integration requirements must use IDs like `INT-05-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-05-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Future phases must reuse outbound activity records for reporting, task scheduling, notifications, integrations, and CRM timelines. Native LinkedIn automation must remain out of scope unless explicitly confirmed.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 05 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`05_Outbound_Sales__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `05_Outbound_Sales.md`.
- Create and provide a second downloadable Markdown file named exactly `05_Outbound_Sales__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 06 Prompt — Calendar and Task System

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 05

Your task is to create the Phase 06 document:

# 06_Calendar_Tasks.md

You must also create a separate future-phase summary file:

# 06_Calendar_Tasks__Summary_For_Future_Phases.md

Important:
- Do not create Phase 07.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `06_Calendar_Tasks.md`
- Name the summary file exactly: `06_Calendar_Tasks__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 06 design level.


Your goal:
Create a complete Phase 06 Calendar and Task System document that defines the shared task, calendar, appointment, reminder, recurrence, assignment, due-date, SLA, and scheduling foundation used by CRM, outbound, field sales, dispatch, service, and mobile workflows.

This phase must define or expand these entities where relevant:

- Task
- CalendarEvent
- Appointment
- Reminder
- RecurrenceRule

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-06-001`.
- Functional requirements must use IDs like `FR-06-001`.
- Non-functional requirements must use IDs like `NFR-06-001`.
- API requirements must use IDs like `API-06-001`.
- UX requirements must use IDs like `UX-06-001`.
- Permission requirements must use IDs like `PERM-06-001`.
- Audit requirements must use IDs like `AUDIT-06-001`.
- Reporting requirements must use IDs like `REPORT-06-001`.
- Notification requirements must use IDs like `NOTIF-06-001`.
- Integration requirements must use IDs like `INT-06-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-06-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Field visits, dispatch assignments, service work orders, reminders, offline mobile tasks, reporting, and notifications must reuse the shared task/calendar foundation.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 06 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`06_Calendar_Tasks__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `06_Calendar_Tasks.md`.
- Create and provide a second downloadable Markdown file named exactly `06_Calendar_Tasks__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 07 Prompt — Field Sales and Site Work

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 06

Your task is to create the Phase 07 document:

# 07_Field_Sales_Site_Work.md

You must also create a separate future-phase summary file:

# 07_Field_Sales_Site_Work__Summary_For_Future_Phases.md

Important:
- Do not create Phase 08.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `07_Field_Sales_Site_Work.md`
- Name the summary file exactly: `07_Field_Sales_Site_Work__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 07 design level.


Your goal:
Create a complete Phase 07 Field Sales and Site Work document that defines field sales and site-work workflows: Sites, Site Visits, Check-ins, Check-outs, Field Notes, Field Photos, Job Requests, Jobs, Job Stages, Crews, Equipment Assignments, territory coverage, site outcomes, and mobile capture.

This phase must define or expand these entities where relevant:

- Site
- SiteVisit
- CheckInEvent
- CheckOutEvent
- FieldNote
- FieldPhoto
- JobRequest
- Job
- JobStage
- Crew
- EquipmentAssignment

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-07-001`.
- Functional requirements must use IDs like `FR-07-001`.
- Non-functional requirements must use IDs like `NFR-07-001`.
- API requirements must use IDs like `API-07-001`.
- UX requirements must use IDs like `UX-07-001`.
- Permission requirements must use IDs like `PERM-07-001`.
- Audit requirements must use IDs like `AUDIT-07-001`.
- Reporting requirements must use IDs like `REPORT-07-001`.
- Notification requirements must use IDs like `NOTIF-07-001`.
- Integration requirements must use IDs like `INT-07-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-07-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Drilling operations, dispatch, fleet, service, reporting, offline sync, and QuickBooks-related workflows must reuse Site, JobRequest, Job, CheckInEvent, and FieldNote concepts where appropriate.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 07 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`07_Field_Sales_Site_Work__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `07_Field_Sales_Site_Work.md`.
- Create and provide a second downloadable Markdown file named exactly `07_Field_Sales_Site_Work__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 08 Prompt — Inventory, Warehouse, and Depots

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 07

Your task is to create the Phase 08 document:

# 08_Inventory_Warehouse_Depots.md

You must also create a separate future-phase summary file:

# 08_Inventory_Warehouse_Depots__Summary_For_Future_Phases.md

Important:
- Do not create Phase 09.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `08_Inventory_Warehouse_Depots.md`
- Name the summary file exactly: `08_Inventory_Warehouse_Depots__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 08 design level.


Your goal:
Create a complete Phase 08 Inventory, Warehouse, and Depots document that defines products, product categories, stock units, inventory items, inventory balances, warehouses, depots, bin locations, receiving, picking, packing, stock movements, adjustments, transfers, low-stock alerts, and warehouse/depot workflows.

This phase must define or expand these entities where relevant:

- Product
- ProductCategory
- StockUnit
- InventoryItem
- InventoryBalance
- Warehouse
- Depot
- BinLocation
- ReceivingRecord
- PickTicket
- PackRecord
- StockMovement
- InventoryAdjustment
- InventoryTransfer
- LowStockAlert

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-08-001`.
- Functional requirements must use IDs like `FR-08-001`.
- Non-functional requirements must use IDs like `NFR-08-001`.
- API requirements must use IDs like `API-08-001`.
- UX requirements must use IDs like `UX-08-001`.
- Permission requirements must use IDs like `PERM-08-001`.
- Audit requirements must use IDs like `AUDIT-08-001`.
- Reporting requirements must use IDs like `REPORT-08-001`.
- Notification requirements must use IDs like `NOTIF-08-001`.
- Integration requirements must use IDs like `INT-08-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-08-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Orders, dispatch, service, QuickBooks item sync, reporting, mobile scanning, and warehouse/depot permissions must reuse the inventory model.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 08 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`08_Inventory_Warehouse_Depots__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `08_Inventory_Warehouse_Depots.md`.
- Create and provide a second downloadable Markdown file named exactly `08_Inventory_Warehouse_Depots__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 09 Prompt — Orders, Dispatch, and Logistics

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 08

Your task is to create the Phase 09 document:

# 09_Orders_Dispatch_Logistics.md

You must also create a separate future-phase summary file:

# 09_Orders_Dispatch_Logistics__Summary_For_Future_Phases.md

Important:
- Do not create Phase 10.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `09_Orders_Dispatch_Logistics.md`
- Name the summary file exactly: `09_Orders_Dispatch_Logistics__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 09 design level.


Your goal:
Create a complete Phase 09 Orders, Dispatch, and Logistics document that defines orders, order lines, shipments, shipment stops, dispatch plans, route plans, deliveries, pickups, proof of delivery, delivery exceptions, handoff events, dispatcher workflows, and logistics tracking.

This phase must define or expand these entities where relevant:

- Order
- OrderLine
- Shipment
- ShipmentStop
- DispatchPlan
- RoutePlan
- Delivery
- Pickup
- ProofOfDelivery
- DeliveryException
- HandoffEvent

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-09-001`.
- Functional requirements must use IDs like `FR-09-001`.
- Non-functional requirements must use IDs like `NFR-09-001`.
- API requirements must use IDs like `API-09-001`.
- UX requirements must use IDs like `UX-09-001`.
- Permission requirements must use IDs like `PERM-09-001`.
- Audit requirements must use IDs like `AUDIT-09-001`.
- Reporting requirements must use IDs like `REPORT-09-001`.
- Notification requirements must use IDs like `NOTIF-09-001`.
- Integration requirements must use IDs like `INT-09-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-09-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Fleet tracking, service, reporting, QuickBooks, offline mobile, notifications/automation, and final system blueprint must reuse dispatch/logistics status and event models.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 09 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`09_Orders_Dispatch_Logistics__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `09_Orders_Dispatch_Logistics.md`.
- Create and provide a second downloadable Markdown file named exactly `09_Orders_Dispatch_Logistics__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 10 Prompt — Fleet and Device Tracking

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 09

Your task is to create the Phase 10 document:

# 10_Fleet_Device_Tracking.md

You must also create a separate future-phase summary file:

# 10_Fleet_Device_Tracking__Summary_For_Future_Phases.md

Important:
- Do not create Phase 11.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `10_Fleet_Device_Tracking.md`
- Name the summary file exactly: `10_Fleet_Device_Tracking__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 10 design level.


Your goal:
Create a complete Phase 10 Fleet and Device Tracking document that defines vehicles, drivers, tracking devices, device assignments, location pings, location history, geofences, geofence events, route replay, speed alerts, stop alerts, device health, live tracking, historical tracking, privacy/security, and fleet reporting.

This phase must define or expand these entities where relevant:

- Vehicle
- Driver
- TrackingDevice
- DeviceAssignment
- LocationPing
- LocationHistory
- Geofence
- GeofenceEvent
- RouteReplay
- SpeedAlert
- StopAlert
- DeviceHealthEvent

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-10-001`.
- Functional requirements must use IDs like `FR-10-001`.
- Non-functional requirements must use IDs like `NFR-10-001`.
- API requirements must use IDs like `API-10-001`.
- UX requirements must use IDs like `UX-10-001`.
- Permission requirements must use IDs like `PERM-10-001`.
- Audit requirements must use IDs like `AUDIT-10-001`.
- Reporting requirements must use IDs like `REPORT-10-001`.
- Notification requirements must use IDs like `NOTIF-10-001`.
- Integration requirements must use IDs like `INT-10-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-10-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Reporting, notifications/automation, offline mobile, security/audit, and final blueprint must respect fleet tracking privacy, event, and retention rules.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 10 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`10_Fleet_Device_Tracking__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `10_Fleet_Device_Tracking.md`.
- Create and provide a second downloadable Markdown file named exactly `10_Fleet_Device_Tracking__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 11 Prompt — Service and Work Orders

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 10

Your task is to create the Phase 11 document:

# 11_Service_Work_Orders.md

You must also create a separate future-phase summary file:

# 11_Service_Work_Orders__Summary_For_Future_Phases.md

Important:
- Do not create Phase 12.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `11_Service_Work_Orders.md`
- Name the summary file exactly: `11_Service_Work_Orders__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 11 design level.


Your goal:
Create a complete Phase 11 Service and Work Orders document that defines service requests, work orders, work order tasks, maintenance schedules, service history, labor entries, parts usage, service technician workflows, follow-up actions, service statuses, audit events, and service reporting.

This phase must define or expand these entities where relevant:

- ServiceRequest
- WorkOrder
- WorkOrderTask
- MaintenanceSchedule
- ServiceHistory
- LaborEntry
- PartsUsage

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-11-001`.
- Functional requirements must use IDs like `FR-11-001`.
- Non-functional requirements must use IDs like `NFR-11-001`.
- API requirements must use IDs like `API-11-001`.
- UX requirements must use IDs like `UX-11-001`.
- Permission requirements must use IDs like `PERM-11-001`.
- Audit requirements must use IDs like `AUDIT-11-001`.
- Reporting requirements must use IDs like `REPORT-11-001`.
- Notification requirements must use IDs like `NOTIF-11-001`.
- Integration requirements must use IDs like `INT-11-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-11-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Reporting, QuickBooks, offline sync, notifications/automation, and final blueprint must respect service work order and parts/labor rules.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 11 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`11_Service_Work_Orders__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `11_Service_Work_Orders.md`.
- Create and provide a second downloadable Markdown file named exactly `11_Service_Work_Orders__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 12 Prompt — Reporting and Dashboards

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 11

Your task is to create the Phase 12 document:

# 12_Reporting_Dashboards.md

You must also create a separate future-phase summary file:

# 12_Reporting_Dashboards__Summary_For_Future_Phases.md

Important:
- Do not create Phase 13.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `12_Reporting_Dashboards.md`
- Name the summary file exactly: `12_Reporting_Dashboards__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 12 design level.


Your goal:
Create a complete Phase 12 Reporting and Dashboards document that defines dashboards, reports, report definitions, report runs, metric definitions, rollup snapshots, scheduled reports, analytics permissions, dashboard UX, report filters, data freshness, and materialized metrics.

This phase must define or expand these entities where relevant:

- Dashboard
- Report
- ReportDefinition
- ReportRun
- MetricDefinition
- RollupSnapshot
- ScheduledReport

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-12-001`.
- Functional requirements must use IDs like `FR-12-001`.
- Non-functional requirements must use IDs like `NFR-12-001`.
- API requirements must use IDs like `API-12-001`.
- UX requirements must use IDs like `UX-12-001`.
- Permission requirements must use IDs like `PERM-12-001`.
- Audit requirements must use IDs like `AUDIT-12-001`.
- Reporting requirements must use IDs like `REPORT-12-001`.
- Notification requirements must use IDs like `NOTIF-12-001`.
- Integration requirements must use IDs like `INT-12-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-12-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
QuickBooks/integrations, admin/security, notifications/automation, API/export, final blueprint, and rollout must use reporting definitions and metric standards.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 12 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`12_Reporting_Dashboards__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `12_Reporting_Dashboards.md`.
- Create and provide a second downloadable Markdown file named exactly `12_Reporting_Dashboards__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 13 Prompt — QuickBooks and Integrations

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 12

Your task is to create the Phase 13 document:

# 13_QuickBooks_Integrations.md

You must also create a separate future-phase summary file:

# 13_QuickBooks_Integrations__Summary_For_Future_Phases.md

Important:
- Do not create Phase 14.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `13_QuickBooks_Integrations.md`
- Name the summary file exactly: `13_QuickBooks_Integrations__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 13 design level.


Your goal:
Create a complete Phase 13 QuickBooks and Integrations document that defines QuickBooks as first accounting integration plus general integration foundations: connections, accounts, sync jobs, sync logs, external references, QuickBooks links, provider integrations, retries, errors, and admin visibility.

This phase must define or expand these entities where relevant:

- IntegrationConnection
- IntegrationAccount
- SyncJob
- SyncLog
- ExternalReference
- QuickBooksCustomerLink
- QuickBooksInvoiceLink
- QuickBooksItemLink
- WebhookDelivery

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-13-001`.
- Functional requirements must use IDs like `FR-13-001`.
- Non-functional requirements must use IDs like `NFR-13-001`.
- API requirements must use IDs like `API-13-001`.
- UX requirements must use IDs like `UX-13-001`.
- Permission requirements must use IDs like `PERM-13-001`.
- Audit requirements must use IDs like `AUDIT-13-001`.
- Reporting requirements must use IDs like `REPORT-13-001`.
- Notification requirements must use IDs like `NOTIF-13-001`.
- Integration requirements must use IDs like `INT-13-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-13-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
API/webhooks/import/export, admin/security, notifications/automation, reporting, rollout, and final blueprint must reuse integration conventions.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 13 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`13_QuickBooks_Integrations__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `13_QuickBooks_Integrations.md`.
- Create and provide a second downloadable Markdown file named exactly `13_QuickBooks_Integrations__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 14 Prompt — Offline Mobile and Sync

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 13

Your task is to create the Phase 14 document:

# 14_Offline_Mobile_Sync.md

You must also create a separate future-phase summary file:

# 14_Offline_Mobile_Sync__Summary_For_Future_Phases.md

Important:
- Do not create Phase 15.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `14_Offline_Mobile_Sync.md`
- Name the summary file exactly: `14_Offline_Mobile_Sync__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 14 design level.


Your goal:
Create a complete Phase 14 Offline Mobile and Sync document that defines offline mobile behavior, local cache, offline action queue, sync operations, conflict handling, retry behavior, permissions revalidation, attachment/photo sync, company cache isolation, sync status UX, and mobile reliability.

This phase must define or expand these entities where relevant:

- OfflineCacheRecord
- OfflineActionQueueItem
- SyncOperation
- SyncConflict
- SyncStatus

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-14-001`.
- Functional requirements must use IDs like `FR-14-001`.
- Non-functional requirements must use IDs like `NFR-14-001`.
- API requirements must use IDs like `API-14-001`.
- UX requirements must use IDs like `UX-14-001`.
- Permission requirements must use IDs like `PERM-14-001`.
- Audit requirements must use IDs like `AUDIT-14-001`.
- Reporting requirements must use IDs like `REPORT-14-001`.
- Notification requirements must use IDs like `NOTIF-14-001`.
- Integration requirements must use IDs like `INT-14-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-14-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Admin/security, notifications/automation, reporting, rollout, and final blueprint must respect offline validation, conflict, and mobile cache rules.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 14 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`14_Offline_Mobile_Sync__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `14_Offline_Mobile_Sync.md`.
- Create and provide a second downloadable Markdown file named exactly `14_Offline_Mobile_Sync__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 15 Prompt — Admin, Security, and Audit

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 14

Your task is to create the Phase 15 document:

# 15_Admin_Security_Audit.md

You must also create a separate future-phase summary file:

# 15_Admin_Security_Audit__Summary_For_Future_Phases.md

Important:
- Do not create Phase 16.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `15_Admin_Security_Audit.md`
- Name the summary file exactly: `15_Admin_Security_Audit__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 15 design level.


Your goal:
Create a complete Phase 15 Admin, Security, and Audit document that defines administrative controls, security hardening, audit review, tenant/company isolation testing, permission hardening, admin settings, compliance expectations, monitoring, backups, data retention, super admin operations, and rollout security gates.

This phase must define or expand these entities where relevant:

- SecuritySetting
- AuditReview
- RetentionPolicy
- AdminAction
- SecurityIncident
- BackupJob
- RestoreJob

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-15-001`.
- Functional requirements must use IDs like `FR-15-001`.
- Non-functional requirements must use IDs like `NFR-15-001`.
- API requirements must use IDs like `API-15-001`.
- UX requirements must use IDs like `UX-15-001`.
- Permission requirements must use IDs like `PERM-15-001`.
- Audit requirements must use IDs like `AUDIT-15-001`.
- Reporting requirements must use IDs like `REPORT-15-001`.
- Notification requirements must use IDs like `NOTIF-15-001`.
- Integration requirements must use IDs like `INT-15-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-15-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Notifications/automation, API/webhooks/import/export, rollout/operations, and final blueprint must respect admin/security/audit hardening rules.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 15 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`15_Admin_Security_Audit__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `15_Admin_Security_Audit.md`.
- Create and provide a second downloadable Markdown file named exactly `15_Admin_Security_Audit__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 16 Prompt — Notifications and Automation

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 15

Your task is to create the Phase 16 document:

# 16_Notifications_Automation.md

You must also create a separate future-phase summary file:

# 16_Notifications_Automation__Summary_For_Future_Phases.md

Important:
- Do not create Phase 17.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `16_Notifications_Automation.md`
- Name the summary file exactly: `16_Notifications_Automation__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 16 design level.


Your goal:
Create a complete Phase 16 Notifications and Automation document that defines notification rules, templates, channels, triggers, automation rules, conditions, actions, escalation, reminders, subscriptions, user preferences, admin controls, and cross-module automation governance.

This phase must define or expand these entities where relevant:

- NotificationRule
- NotificationTemplate
- NotificationPreference
- AutomationRule
- AutomationTrigger
- AutomationCondition
- AutomationAction
- EscalationRule
- Subscription

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-16-001`.
- Functional requirements must use IDs like `FR-16-001`.
- Non-functional requirements must use IDs like `NFR-16-001`.
- API requirements must use IDs like `API-16-001`.
- UX requirements must use IDs like `UX-16-001`.
- Permission requirements must use IDs like `PERM-16-001`.
- Audit requirements must use IDs like `AUDIT-16-001`.
- Reporting requirements must use IDs like `REPORT-16-001`.
- Notification requirements must use IDs like `NOTIF-16-001`.
- Integration requirements must use IDs like `INT-16-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-16-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
API/webhooks/import/export, search/views, rollout, and final blueprint must respect automation event and action constraints.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 16 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`16_Notifications_Automation__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `16_Notifications_Automation.md`.
- Create and provide a second downloadable Markdown file named exactly `16_Notifications_Automation__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 17 Prompt — API, Webhooks, Import, and Export

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 16

Your task is to create the Phase 17 document:

# 17_API_Webhooks_Import_Export.md

You must also create a separate future-phase summary file:

# 17_API_Webhooks_Import_Export__Summary_For_Future_Phases.md

Important:
- Do not create Phase 18.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `17_API_Webhooks_Import_Export.md`
- Name the summary file exactly: `17_API_Webhooks_Import_Export__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 17 design level.


Your goal:
Create a complete Phase 17 API, Webhooks, Import, and Export document that defines external/public API standards, API keys, scopes, rate limits, webhooks, webhook events, webhook delivery/retry, import framework, export framework, bulk operations, API documentation standards, and developer experience.

This phase must define or expand these entities where relevant:

- ApiKey
- ApiScope
- ApiRequestLog
- WebhookEndpoint
- WebhookEvent
- WebhookDelivery
- ImportJob
- ImportMapping
- ImportErrorRow
- ExportJob
- BulkOperation

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-17-001`.
- Functional requirements must use IDs like `FR-17-001`.
- Non-functional requirements must use IDs like `NFR-17-001`.
- API requirements must use IDs like `API-17-001`.
- UX requirements must use IDs like `UX-17-001`.
- Permission requirements must use IDs like `PERM-17-001`.
- Audit requirements must use IDs like `AUDIT-17-001`.
- Reporting requirements must use IDs like `REPORT-17-001`.
- Notification requirements must use IDs like `NOTIF-17-001`.
- Integration requirements must use IDs like `INT-17-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-17-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Search/filter/custom views, rollout/operations, and final blueprint must apply API and import/export standards.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 17 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`17_API_Webhooks_Import_Export__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `17_API_Webhooks_Import_Export.md`.
- Create and provide a second downloadable Markdown file named exactly `17_API_Webhooks_Import_Export__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 18 Prompt — Search, Filters, and Custom Views

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 17

Your task is to create the Phase 18 document:

# 18_Search_Filters_Custom_Views.md

You must also create a separate future-phase summary file:

# 18_Search_Filters_Custom_Views__Summary_For_Future_Phases.md

Important:
- Do not create Phase 19.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `18_Search_Filters_Custom_Views.md`
- Name the summary file exactly: `18_Search_Filters_Custom_Views__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 18 design level.


Your goal:
Create a complete Phase 18 Search, Filters, and Custom Views document that defines global search, module search, filters, saved views, table views, kanban views, calendar views, map views, activity timelines, custom view sharing, filter persistence, search indexing, and permission-aware results.

This phase must define or expand these entities where relevant:

- SearchIndexRecord
- SavedView
- FilterDefinition
- ViewConfiguration
- SearchQueryLog
- RecentRecord
- PinnedView

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-18-001`.
- Functional requirements must use IDs like `FR-18-001`.
- Non-functional requirements must use IDs like `NFR-18-001`.
- API requirements must use IDs like `API-18-001`.
- UX requirements must use IDs like `UX-18-001`.
- Permission requirements must use IDs like `PERM-18-001`.
- Audit requirements must use IDs like `AUDIT-18-001`.
- Reporting requirements must use IDs like `REPORT-18-001`.
- Notification requirements must use IDs like `NOTIF-18-001`.
- Integration requirements must use IDs like `INT-18-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-18-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Rollout/operations and final blueprint must respect unified search/filter/view UX and permission rules.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 18 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`18_Search_Filters_Custom_Views__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `18_Search_Filters_Custom_Views.md`.
- Create and provide a second downloadable Markdown file named exactly `18_Search_Filters_Custom_Views__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 19 Prompt — Rollout, Migration, and Operations

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 18

Your task is to create the Phase 19 document:

# 19_Rollout_Migration_Operations.md

You must also create a separate future-phase summary file:

# 19_Rollout_Migration_Operations__Summary_For_Future_Phases.md

Important:
- Do not create Phase 20.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `19_Rollout_Migration_Operations.md`
- Name the summary file exactly: `19_Rollout_Migration_Operations__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 19 design level.


Your goal:
Create a complete Phase 19 Rollout, Migration, and Operations document that defines rollout strategy, migration planning, onboarding operations, environment strategy, release process, monitoring, support, backups, operational runbooks, data migration, customer enablement, phased launch, QA gates, and production readiness.

This phase must define or expand these entities where relevant:

- MigrationJob
- MigrationRun
- MigrationError
- Release
- FeatureFlag
- OperationalRunbook
- Incident
- SupportTicket
- BackupJob
- RestoreJob

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-19-001`.
- Functional requirements must use IDs like `FR-19-001`.
- Non-functional requirements must use IDs like `NFR-19-001`.
- API requirements must use IDs like `API-19-001`.
- UX requirements must use IDs like `UX-19-001`.
- Permission requirements must use IDs like `PERM-19-001`.
- Audit requirements must use IDs like `AUDIT-19-001`.
- Reporting requirements must use IDs like `REPORT-19-001`.
- Notification requirements must use IDs like `NOTIF-19-001`.
- Integration requirements must use IDs like `INT-19-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-19-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Phase 20 must consolidate the entire system blueprint and reference rollout constraints without introducing major new features.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 19 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`19_Rollout_Migration_Operations__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `19_Rollout_Migration_Operations.md`.
- Create and provide a second downloadable Markdown file named exactly `19_Rollout_Migration_Operations__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
## Phase 20 Prompt — Final System Blueprint

```text
You are a senior product architect, SaaS systems analyst, domain specialist, and technical documentation lead.

I am building a large multi-company SaaS platform for CRM, outbound sales, field operations, drilling workflows, logistics, warehouses, fleet tracking, dispatch, service work, reporting, integrations, QuickBooks sync, and offline-capable mobile workflows.

I will provide you with these control documents:

1. `00_Master_Platform_Documentation.md`
2. `00_Global_Documentation_Rules.md`
3. `00_Global_Domain_Model.md`
4. `00_Global_Decisions_Register.md`
5. all available prior phase summary files from Phase 01 through Phase 19

Your task is to create the Phase 20 document:

# 20_Final_System_Blueprint.md

You must also create a separate future-phase summary file:

# 20_Final_System_Blueprint__Summary_For_Future_Phases.md

Important:
- Do not create Phase 21.
- Do not rewrite the master documentation.
- Do not rewrite the global control documents.
- Do not rewrite prior phase documents.
- Use prior phase summaries for continuity instead of requiring full previous phase documents.
- Do not introduce decisions that contradict the master documentation, global documentation rules, global domain model, global decisions register, or prior phase summaries.
- Use the provided documents as the source of truth.
- The output must be delivered as downloadable Markdown files, not only pasted in chat.
- Name the full document exactly: `20_Final_System_Blueprint.md`
- Name the summary file exactly: `20_Final_System_Blueprint__Summary_For_Future_Phases.md`
- In the chat response, provide only a short note and the two download links.
- The document must be detailed, practical, strict, and reusable by future phase writers.
- If a decision is unclear, mark it as an Open Question or Recommended Decision.
- Do not casually rename entities, modules, personas, phases, or workflows.
- Do not invent unnecessary complexity.
- Do not create duplicate entity concepts where the global domain model already defines a canonical entity.
- The document should be production-grade and implementation-ready at the Phase 20 design level.
- Phase 20 must consolidate existing documentation and must not introduce major new features.

Your goal:
Create a complete Phase 20 Final System Blueprint document that defines the full consolidated platform blueprint: product architecture, module map, entity map, workflow map, API/integration map, UX patterns, security model, reporting model, rollout plan, and cross-phase constraints, without introducing major new features.

This phase must define or expand these entities where relevant:

- No new core entities unless consolidating previously introduced entities

For each entity, include:
- Purpose
- Owner module
- Scope
- Tenant/company scoping
- Key fields
- Relationships
- Lifecycle
- Statuses
- Index considerations
- Permissions impact
- Audit requirements
- Reporting impact
- Future-phase impact

Follow the structure and documentation standards from `00_Global_Documentation_Rules.md`.

The full document must include at least these sections:

1. Document Metadata
2. Phase Purpose
3. Phase Goals
4. Scope
5. Non-Goals
6. Source-of-Truth Definitions
7. Canonical Entity Definitions
8. Entity Lifecycle and Status Rules
9. Entity Relationship Rules
10. Workflow Requirements
11. Data Model Requirements
12. API Requirements
13. UI / UX Requirements
14. Search, Filters, and Saved Views
15. Permissions and Access Control
16. Notifications
17. Audit Logging
18. Reporting and Analytics Impact
19. Mobile and Offline Impact
20. Integration Impact
21. Security Considerations
22. Edge Cases
23. Business Requirements
24. Functional Requirements
25. Non-Functional Requirements
26. User Stories
27. Recommended Decisions
28. Open Questions
29. Dependencies
30. Future Phase Considerations
31. Acceptance Criteria
32. Implementation Notes
33. Summary for Future Phases

Requirements:
- Business requirements must use IDs like `BR-20-001`.
- Functional requirements must use IDs like `FR-20-001`.
- Non-functional requirements must use IDs like `NFR-20-001`.
- API requirements must use IDs like `API-20-001`.
- UX requirements must use IDs like `UX-20-001`.
- Permission requirements must use IDs like `PERM-20-001`.
- Audit requirements must use IDs like `AUDIT-20-001`.
- Reporting requirements must use IDs like `REPORT-20-001`.
- Notification requirements must use IDs like `NOTIF-20-001`.
- Integration requirements must use IDs like `INT-20-001`.
- Offline/mobile requirements, where relevant, must use IDs like `OFFLINE-20-001`.

Minimum detail requirements:
- Include at least 15 business requirements.
- Include at least 30 functional requirements.
- Include at least 15 non-functional requirements.
- Include detailed conceptual API requirements.
- Include detailed UX requirements for screens, components, views, forms, empty states, error states, and permission behavior.
- Include detailed permission requirements.
- Include detailed audit event requirements.
- Include reporting and analytics implications.
- Include notification implications.
- Include integration implications.
- Include mobile/offline implications where relevant.
- Include at least 20 phase-specific edge cases.
- Include user stories grouped by relevant personas.
- Include Mermaid diagrams where useful, including at least one entity relationship diagram and one workflow diagram.
- Include dependencies on prior phases and impacts on later phases.

Future-phase constraint:
Phase 20 is the final consolidation artifact. It should not create Phase 21 or introduce major new modules.

At the end of the full document, include this exact structure:

# Summary for Future Phases

## Final Decisions Made

## Entities Introduced

## Fields Introduced

## APIs Introduced

## Permissions Introduced

## UX Patterns Introduced

## Reports or Dashboards Introduced

## Notifications Introduced

## Audit Events Introduced

## Integrations Introduced

## Dependencies Created

## Constraints Future Phases Must Respect

## Open Questions Carried Forward

This summary must be written so future AI writers can use it instead of reading the entire Phase 20 document. It must be concise but complete and preserve all cross-phase decisions, reusable context, entity definitions, permission rules, API expectations, audit events, notification rules, integration foundations, and unresolved questions.

Also create a second downloadable file named exactly:

`20_Final_System_Blueprint__Summary_For_Future_Phases.md`

This second file must contain only the Summary for Future Phases section from the full document.

Output requirements:
- Create and provide a downloadable Markdown file named exactly `20_Final_System_Blueprint.md`.
- Create and provide a second downloadable Markdown file named exactly `20_Final_System_Blueprint__Summary_For_Future_Phases.md`.
- Do not only paste the document into the chat.
- In the chat response, provide only a short note and the two download links.

Here is the master documentation:

[PASTE 00_MASTER_PLATFORM_DOCUMENTATION HERE]

Here is the first global control document, `00_Global_Documentation_Rules.md`:

[PASTE 00_GLOBAL_DOCUMENTATION_RULES HERE]

Here is the second global control document, `00_Global_Domain_Model.md`:

[PASTE 00_GLOBAL_DOMAIN_MODEL HERE]

Here is the third global control document, `00_Global_Decisions_Register.md`:

[PASTE 00_GLOBAL_DECISIONS_REGISTER HERE]

Paste all prior phase summary files here:

[PASTE ALL PRIOR PHASE SUMMARY FILES HERE]
```

---
