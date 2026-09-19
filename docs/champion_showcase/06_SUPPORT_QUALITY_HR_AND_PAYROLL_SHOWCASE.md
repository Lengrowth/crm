# Phase 06 — Support, Quality, HR and Payroll Showcase

## AI goal

Create useful, permission-safe synthetic module journeys for Support, Quality, HR and Payroll so Matt can see the promised capabilities inside one ERP without treating unapproved employment, compensation or quality policy as final.

## Support journey

Provide three clear request types:

1. System Help → standard Support Issue.
2. Create Product → version-controlled Product Change Request.
3. Update Product → Product Change Request linked to an existing Item and proposed changed fields.

Requests use status, requester, owner, approval, comments, attachments and activity history. Approval may demonstrate a controlled update using synthetic Items; it must not mutate real data.

## Quality journey

Model the existing callback/rework use case:

- callback class: Champion warranty, product warranty, hot-shot run, logistics, truck logging or configurable type;
- work order/job reference;
- schedule disruption;
- reason and responsible team/person;
- crew hours, trucks, equipment and products used;
- phone calls/coordination effort;
- estimated rework cost;
- root cause, corrective action, verification and closure.

Use standard Quality records where they fit and LenERP-owned extensions where the callback structure is industry-specific. Do not force callbacks into generic fields that destroy the source meaning.

## HR journey

Demonstrate synthetic Employee, department/role, attendance or timesheet, availability, leave/time-off and shift/on-call context. Link employees to assignments and jobs through stable Employee/User links rather than free text.

## Payroll journey

Demonstrate restricted synthetic Salary Structure/Assignment, timesheet or attendance input, one bonus/on-call earning component and a draft payroll preview if the pinned HRMS baseline supports it safely. Label all values synthetic. Do not encode tax, deduction, overtime or payroll-accounting rules as Champion-approved.

## UX requirements

- Module homes use Champion labels: Support & Requests, Callbacks & Quality, Crew & Hours, Accounting & Payroll.
- Product-update forms preload the selected Item and request only changed fields.
- Callback entry is field-friendly and supports save-as-draft.
- Payroll amounts are masked/absent outside authorized roles, including search, notifications, APIs and reports.
- Employee self-service and manager actions are visually distinct.
- Synthetic payroll screens carry persistent non-production labeling.

## Acceptance tests

- Employee submits a Support Issue and sees only allowed requests.
- Product update goes through approval and records exact proposed/approved differences.
- Callback links to a synthetic Job and calculates traceable labor/material context.
- Quality manager can assign corrective action; unauthorized roles cannot close it.
- HR user manages synthetic employee/time-off records; unrelated roles are denied.
- Payroll manager sees synthetic payroll; Dispatcher, Field and Support roles are denied by UI, route and API.
- No real employee, SSN, banking, tax or payroll data exists.
- All four module homes pass responsive, keyboard and accessibility checks.

## Non-goals

- Final payroll calculations, taxes, deductions or accounting entries.
- Final bonus/performance policy.
- Public anonymous Support writes.
- Offline/native Field App behavior.

## Gate and rollback

All module entry points remain restricted to synthetic staging roles until permissions and data boundaries pass. Rollback hides custom entry points and disables synthetic workflows; standard records are removed only through exact demo-reset tooling.

## Execution prompt

> Build the synthetic Support, Product Change Request, Callback/Quality, HR and restricted Payroll journeys in this document. Prefer standard ERPNext/HRMS records, add LenERP-owned DocTypes only for real domain gaps, enforce negative permissions and confidential-field boundaries, provide polished responsive UX, create exact reset tooling, and never represent synthetic compensation or policy as Champion-approved.
