# 06 — Implementation Project Workflows

**Scope:** SaaS implementation projects, onboarding task tracking, configurable task statuses, and reusable onboarding templates.
**Architecture:** Backend-first control-plane workflow layer for client implementation management.
**Last updated:** 2026-05-27

---

## 1. Purpose

Phase 06 adds the internal workflow layer used by the SaaS team to manage client onboarding and implementation delivery.

The SaaS platform now tracks:

- Implementation projects tied to organizations and tenants.
- Project tasks assigned to team members.
- Configurable task statuses for workflow tracking.
- Reusable onboarding templates for repeatable client setup patterns.

This phase stays inside the SaaS control plane. It does **not** integrate directly with ERPNext/Frappe runtime data.

---

## 2. Data model

### 2.1 ImplementationProject

Represents a client implementation workstream.

Key fields:

- `organization_id` — owning organization.
- `tenant_id` — tenant being onboarded.
- `template_id` — optional onboarding template.
- `status` — project phase such as discovery, planning, setup, or go-live.
- `owner_user_id` — internal owner.
- `target_go_live_date` — planning target.

The API also exposes derived progress fields:

- `task_count`
- `completed_task_count`
- `progress_percent`

### 2.2 ImplementationTask

Represents a single actionable item inside an implementation project.

Key fields:

- `implementation_project_id`
- `title`
- `description`
- `status`
- `sort_order`
- `assigned_to_user_id`
- `due_date`

### 2.3 ImplementationTaskStatus

Represents configurable workflow statuses used by tasks.

Key fields:

- `code`
- `name`
- `description`
- `sort_order`
- `is_active`
- `is_terminal`

The seeded defaults are lightweight and can be edited later.

### 2.4 ImplementationTemplate

Represents reusable onboarding patterns for similar client implementations.

Key fields:

- `code`
- `name`
- `industry`
- `description`
- `default_modules_json`
- `default_roles_json`
- `default_checklists_json`
- `default_settings_json`

---

## 3. Service behavior

### 3.1 ImplementationService responsibilities

The implementation service owns:

- Project CRUD.
- Task CRUD.
- Task status CRUD.
- Template CRUD.
- Organization membership checks.
- Tenant-to-organization validation.
- Progress calculation for project reads.

### 3.2 Access rules

- Project and task writes require organization write access.
- Platform admins can manage global task statuses and onboarding templates.
- Task status codes must exist and be active before tasks can use them.
- Templates cannot be deleted while referenced by projects.
- Task statuses cannot be deleted while referenced by tasks.

### 3.3 Progress calculation

Project progress is computed from task statuses:

- Total tasks are counted per project.
- Completed tasks are counted using terminal statuses.
- Progress percent is `completed / total * 100`.

---

## 4. API endpoints

### 4.1 Task statuses

- `GET /implementation/task-statuses`
- `POST /implementation/task-statuses`
- `GET /implementation/task-statuses/{status_id}`
- `PATCH /implementation/task-statuses/{status_id}`
- `DELETE /implementation/task-statuses/{status_id}`

### 4.2 Templates

- `GET /implementation/templates`
- `POST /implementation/templates`
- `GET /implementation/templates/{template_id}`
- `PATCH /implementation/templates/{template_id}`
- `DELETE /implementation/templates/{template_id}`

### 4.3 Projects

- `GET /organizations/{organization_id}/implementation-projects`
- `POST /organizations/{organization_id}/implementation-projects`
- `GET /implementation-projects/{project_id}`
- `PATCH /implementation-projects/{project_id}`
- `DELETE /implementation-projects/{project_id}`

### 4.4 Project tasks

- `GET /implementation-projects/{project_id}/tasks`
- `POST /implementation-projects/{project_id}/tasks`
- `GET /implementation-tasks/{task_id}`
- `PATCH /implementation-tasks/{task_id}`
- `DELETE /implementation-tasks/{task_id}`

---

## 5. Migration and seed data

Phase 06 adds a dedicated migration for `implementation_task_statuses`.

Seed data now includes default workflow statuses:

- `todo`
- `in_progress`
- `blocked`
- `review`
- `done`
- `cancelled`

The existing onboarding template seed data remains in place.

---

## 6. Notes for future phases

This phase intentionally keeps the workflow model lightweight.

Likely future expansions:

- Task comments and activity history.
- Task dependencies.
- Template-to-task materialization.
- Assignment notifications.
- SLA tracking.
- Implementation dashboards and reporting.
