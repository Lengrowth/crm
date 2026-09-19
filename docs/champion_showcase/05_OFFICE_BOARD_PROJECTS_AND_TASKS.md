# Phase 05 — Office Board, Projects and Tasks

## AI goal

Provide the office team with a Jira-like workflow inside Champion ERP using standard Project, Task, assignment, comment and timesheet foundations, avoiding another external task system.

## Target workflow

The initial synthetic board uses configurable states based on the current Champion pattern:

```text
Urgent → High Priority → Medium Priority → Low Priority
                      ↘ Waiting for Counting → Done
```

The final labels and transitions remain subject to Matt’s approval.

## Build scope

1. Create an `Office Board` workspace and saved views over standard Projects and Tasks.
2. Provide list, Kanban, calendar and Gantt access where standard capabilities are useful.
3. Support title, description, department/project, due date, priority, status, assignees, checklist/dependencies, linked business record, comments and attachments.
4. Use Frappe assignment/ToDo behavior for multiple assignees; do not require users to copy names between properties.
5. Add deterministic due-date attention indicators. Automatic status movement must be separately configurable and must not overwrite a user-controlled business status without an approved rule.
6. Link tasks to Wells, Jobs, Customers, Items, Suppliers, Purchase Orders, Quality records and Support requests.
7. Separate permit records from generic tasks when permit structure is introduced; tasks may link to a Permit but must not be the only permit database.
8. Add `My work`, `Team board`, `Overdue`, `Waiting`, and `Recently completed` views.
9. Preserve standard comments/activity history for auditability.

## UX requirements

- Fast task creation with advanced fields collapsed.
- Drag/drop has an equivalent keyboard/menu action.
- Cards show only actionable summary: title, due state, assignees, linked record and blocker.
- Opening a task preserves board filters when returning.
- Mobile uses a usable column switcher/list rather than forcing a wide horizontal board.
- Empty boards explain how work enters the system.

## Acceptance tests

- Office user can create, assign, comment, reprioritize and complete a task.
- Multiple assignees receive independent assignments without manual name duplication.
- Unauthorized Field or Accounting roles cannot modify unrelated office tasks.
- Due indicators are deterministic across timezone boundaries.
- Linked Job/Well/Item opens correctly and back-navigation preserves context.
- List, Kanban and direct URL permissions agree.
- Responsive, keyboard and accessibility checks pass.

## Non-goals

- Recreating every Jira feature.
- Chat replacement.
- Final permit workflow.
- Real employee performance scoring.

## Gate and rollback

Use additive workspace/saved-view/configuration changes and synthetic tasks. Rollback hides the Office Board workspace; standard Task records remain accessible through Projects.

## Execution prompt

> Build a Champion Office Board using standard ERPNext/Frappe Projects, Tasks, assignments, comments and timesheets. Deliver a polished list/Kanban/mobile experience, multiple-assignee behavior, linked business records, due attention, authorization tests and synthetic demo data. Do not introduce a separate task database or claim final status rules without Matt’s approval.
