# 08 — SaaS-First Master Build Documentation

**Project:** ERPNext/Frappe-powered vertical SaaS platform  
**Architecture direction:** SaaS control platform first, ERPNext/Frappe tenant integration second  
**Frontend:** Next.js in `/frontend`  
**Backend:** Python API in `/backend`  
**ERP core:** ERPNext/Frappe, connected later as tenant infrastructure  
**Date:** 2026-05-22

---

## 1. Purpose

This document defines the phased build plan for the SaaS product that will eventually control ERPNext/Frappe tenants.

The goal is to avoid starting with production infrastructure too early. First, build the SaaS foundation:

1. Main website.
2. SaaS backend.
3. Authentication.
4. Tenant/account model.
5. Module catalog.
6. Admin dashboard.
7. Client onboarding workflow.
8. ERPNext integration adapter.
9. Tenant provisioning workflow.
10. Billing, white-labeling, backups, and operations.

ERPNext/Frappe will come later as the operational ERP engine. The SaaS layer should be designed from the beginning to control ERPNext, but it should not depend on ERPNext being live on day one.

---

## 2. Key decision: SaaS first, ERPNext second

### Why SaaS first?

You want to build a product, not only host ERPNext.

If you start directly with ERPNext, you may end up doing manual client-by-client implementation work. That becomes an agency model.

The SaaS-first layer gives you:

- Product identity.
- Main website.
- Central authentication for your own team and future customers.
- A place to store clients, tenants, plans, modules, domains, billing status, implementation status, and provisioning logs.
- A clean way to add ERPNext later.
- A repeatable onboarding and provisioning process.

### What the SaaS layer owns

The SaaS layer is the control center.

It does **not** replace ERPNext. It manages clients and eventually controls ERPNext tenant creation/configuration.

The SaaS layer owns:

- Public website.
- Demo/signup flow.
- SaaS user accounts.
- Organizations/accounts.
- Tenants.
- Plans.
- Modules.
- Billing status.
- White-label settings.
- Domain settings.
- Provisioning jobs.
- ERPNext connection settings.
- Internal admin dashboard.
- Implementation checklist.
- Client onboarding status.
- Audit logs.

ERPNext owns:

- CRM.
- Customers.
- Quotes.
- Sales orders.
- Invoices.
- Accounting.
- Inventory.
- Projects.
- Employees.
- Assets.
- Workflows.
- Field operations data after your custom Frappe app exists.

---

## 3. Repository structure

Use one repository with two main applications:

```txt
project-root/
  README.md
  docs/
    00_Master_Index.md
    00_Project_Decisions.md
    00_Glossary.md
    phase_summaries/
    data_model/
    auth/
    tenants/
    implementation/
    integrations/
    provisioning/
    billing/
    white_label/
    drilling/
    security/

  frontend/
    package.json
    next.config.ts
    tsconfig.json
    src/
      app/
      components/
      features/
      lib/
      services/
      types/
      styles/

  backend/
    pyproject.toml
    alembic.ini
    src/
      app/
        main.py
        api/
        core/
        db/
        models/
        schemas/
        services/
        workers/
        integrations/
        modules/
    tests/

  docker/
    local/
      docker-compose.yml
      .env.example

  scripts/
    dev/
    provisioning/
    backups/
```

### Why separate `/frontend` and `/backend`

- Next.js handles the web UI.
- Python backend handles auth, database, billing, ERPNext integration, and provisioning logic.
- ERPNext/Frappe remains a separate system that the SaaS backend connects to later.

### Do not put ERPNext inside this app yet

Create interfaces first:

```txt
backend/src/app/integrations/erpnext/
  base.py
  mock_client.py
  rest_client.py
  provisioning.py
  schemas.py
```

At first, the ERPNext integration can be mocked. Later, when ERPNext is online, replace the mock with real API calls and provisioning scripts.

---

## 4. Technology decisions

### Frontend

Use:

- Next.js App Router.
- TypeScript.
- Tailwind CSS.
- A clean component system.
- Public website pages.
- Logged-in SaaS dashboard pages.
- API client layer inside `frontend/src/services`.

### Backend

Use:

- FastAPI or similar Python API framework.
- SQLAlchemy or SQLModel.
- Alembic migrations.
- Pydantic schemas.
- JWT/session auth.
- Role-based access.
- Background jobs later.
- REST API first.

### SaaS database

Recommended default:

- PostgreSQL for the SaaS backend, because it is good for SaaS metadata, JSON fields, and long-term product work.
- For the local-only MVP phase, a SQLite file database is acceptable and keeps setup simple. Keep `DATABASE_URL` configurable so the project can move back to PostgreSQL later without changing the code path.
- ERPNext/Frappe keeps MariaDB.

Acceptable simpler option:

- MariaDB for both SaaS and ERPNext if you want fewer database technologies.

The SaaS database is **not** the ERPNext database. It stores SaaS control data.

### ERPNext/Frappe connection

Later connection methods:

- Frappe REST API.
- Token authentication.
- Provisioning scripts that run `bench` commands.
- Custom internal automation service.
- Direct API calls to configure tenants after site creation.

---

## 5. Core SaaS concepts

### Organization

Represents the customer company.

Example:

```txt
Organization:
  name: ABC Drilling
  legal_name: ABC Drilling LLC
  industry: drilling
  billing_email: finance@abc.com
  status: trial | active | suspended | cancelled
```

### Tenant

Represents one ERP/client environment.

In the future, one organization could have more than one tenant.

Example:

```txt
Tenant:
  organization_id
  tenant_slug: abc-drilling
  primary_domain: abc.yourdomain.com
  custom_domain: ops.abcdrilling.com
  erpnext_site_name: abc.yourdomain.com
  erpnext_base_url: https://abc.yourdomain.com
  provisioning_status: not_started | queued | running | ready | failed
```

### SaaS user

A SaaS user may be:

- Your internal admin.
- Implementation manager.
- Support user.
- Future customer admin in the SaaS portal.

Do not confuse SaaS users with ERPNext tenant users. ERPNext has its own users per site.

### Plan

Commercial package.

Example:

```txt
Plan:
  name: Starter
  monthly_price_cents: 9900
  included_users: 5
  included_modules: crm, field_ops
```

### Module

Reusable product capability.

Examples:

- CRM.
- Field operations.
- Drilling.
- Fleet.
- Inventory.
- Reporting.
- QuickBooks integration.
- White label.
- Advanced permissions.

### Implementation template

A repeatable setup blueprint for a type of client.

Example:

```txt
Template: Drilling Company MVP
Modules:
  - CRM
  - Projects
  - Field Operations
  - Drilling
  - Fleet
  - Inventory
Default roles:
  - Owner
  - Dispatcher
  - Field Supervisor
  - Technician
  - Accountant
Default checklists:
  - Daily Field Report
  - Safety Checklist
  - Equipment Inspection
```

### Provisioning job

A durable job that records every step required to create/configure a tenant.

Example:

```txt
ProvisioningJob:
  tenant_id
  type: create_erpnext_site
  status: queued | running | succeeded | failed
  started_at
  finished_at
  logs
  error_message
```

---

## 6. Core SaaS backend data model

Implement these before connecting ERPNext.

### Organization

Fields:

```txt
id
name
legal_name
industry
country
timezone
billing_email
status
created_at
updated_at
```

Statuses:

```txt
lead
trial
active
suspended
cancelled
archived
```

### SaaSUser

Fields:

```txt
id
email
full_name
password_hash
status
last_login_at
created_at
updated_at
```

Statuses:

```txt
invited
active
disabled
deleted
```

### OrganizationMembership

Fields:

```txt
id
organization_id
user_id
role
created_at
updated_at
```

Roles:

```txt
owner
admin
implementation_manager
support
viewer
```

### Tenant

Fields:

```txt
id
organization_id
tenant_slug
environment
status
primary_domain
custom_domain
erpnext_site_name
erpnext_base_url
erpnext_api_key_ref
erpnext_api_secret_ref
provisioning_status
created_at
updated_at
```

Environments:

```txt
demo
staging
production
```

Tenant statuses:

```txt
planned
provisioning
ready
suspended
failed
archived
```

### Plan

Fields:

```txt
id
code
name
description
monthly_price_cents
annual_price_cents
is_active
created_at
updated_at
```

### Subscription

Fields:

```txt
id
organization_id
plan_id
status
stripe_customer_id
stripe_subscription_id
current_period_start
current_period_end
created_at
updated_at
```

Statuses:

```txt
trialing
active
past_due
cancelled
unpaid
manual
```

### Module

Fields:

```txt
id
code
name
description
category
is_active
created_at
updated_at
```

Module examples:

```txt
crm
field_ops
drilling
fleet
inventory
reporting
quickbooks
white_label
custom_domain
```

### OrganizationModule

Fields:

```txt
id
organization_id
module_id
status
enabled_by
enabled_at
disabled_at
settings_json
created_at
updated_at
```

### ImplementationTemplate

Fields:

```txt
id
code
name
industry
description
default_modules_json
default_roles_json
default_checklists_json
default_settings_json
created_at
updated_at
```

### ImplementationProject

Fields:

```txt
id
organization_id
tenant_id
template_id
status
owner_user_id
target_go_live_date
created_at
updated_at
```

Statuses:

```txt
discovery
configuration
testing
training
go_live
complete
on_hold
```

### ImplementationTask

Fields:

```txt
id
implementation_project_id
title
description
status
sort_order
assigned_to_user_id
due_date
created_at
updated_at
```

Statuses:

```txt
todo
doing
blocked
done
skipped
```

### Domain

Fields:

```txt
id
tenant_id
domain
type
status
dns_target
ssl_status
verified_at
created_at
updated_at
```

Types:

```txt
system_subdomain
custom_domain
```

Statuses:

```txt
pending_dns
verified
active
failed
removed
```

### ProvisioningJob

Fields:

```txt
id
tenant_id
job_type
status
requested_by_user_id
started_at
finished_at
attempt_count
logs_json
error_message
created_at
updated_at
```

Job types:

```txt
create_site
install_erpnext
install_custom_app
apply_template
configure_branding
configure_domain
issue_ssl
create_admin_user
suspend_site
backup_site
restore_site
```

### AuditLog

Fields:

```txt
id
actor_user_id
organization_id
tenant_id
action
entity_type
entity_id
metadata_json
ip_address
created_at
```

### IntegrationCredential

Fields:

```txt
id
organization_id
tenant_id
provider
label
secret_ref
status
created_at
updated_at
```

Providers:

```txt
erpnext
stripe
quickbooks
google_cloud
smtp
```

Never store raw secrets in plain database fields. Store references to a secret manager or encrypted vault.

---

## 7. Frontend routes

### Public website

```txt
/
/pricing
/industries
/industries/drilling
/industries/field-service
/modules
/demo
/contact
/login
```

### SaaS app routes

```txt
/app
/app/organizations
/app/organizations/[organizationId]
/app/organizations/[organizationId]/tenants
/app/tenants/[tenantId]
/app/tenants/[tenantId]/modules
/app/tenants/[tenantId]/domains
/app/tenants/[tenantId]/provisioning
/app/implementation
/app/implementation/[projectId]
/app/settings
/app/admin
```

### Later ERP links

Do not build full ERP inside Next.js at first.

Later, add links such as:

```txt
Open ERP: https://client-a.yourdomain.com
Open ERP Admin: https://client-a.yourdomain.com/app
Open ERP Customer Portal: https://client-a.yourdomain.com/portal
```

---

## 8. Backend API endpoints

### Auth

```txt
POST /auth/register
POST /auth/login
POST /auth/logout
POST /auth/refresh
POST /auth/forgot-password
POST /auth/reset-password
GET  /auth/me
```

### Organizations

```txt
GET    /organizations
POST   /organizations
GET    /organizations/{id}
PATCH  /organizations/{id}
DELETE /organizations/{id}
```

### Tenants

```txt
GET    /tenants
POST   /tenants
GET    /tenants/{id}
PATCH  /tenants/{id}
POST   /tenants/{id}/suspend
POST   /tenants/{id}/reactivate
```

### Modules

```txt
GET  /modules
GET  /organizations/{id}/modules
POST /organizations/{id}/modules/{module_code}/enable
POST /organizations/{id}/modules/{module_code}/disable
```

### Implementation templates and projects

```txt
GET   /implementation-templates
POST  /implementation-templates
GET   /implementation-templates/{id}
PATCH /implementation-templates/{id}

GET   /implementation-projects
POST  /implementation-projects
GET   /implementation-projects/{id}
PATCH /implementation-projects/{id}
POST  /implementation-projects/{id}/tasks
PATCH /implementation-tasks/{task_id}
```

### Domains

```txt
GET  /tenants/{tenant_id}/domains
POST /tenants/{tenant_id}/domains
POST /domains/{domain_id}/verify
POST /domains/{domain_id}/activate
```

### Provisioning

```txt
GET  /tenants/{tenant_id}/provisioning-jobs
POST /tenants/{tenant_id}/provisioning-jobs
GET  /provisioning-jobs/{job_id}
POST /provisioning-jobs/{job_id}/retry
```

### ERPNext integration

Start as mock endpoints:

```txt
GET  /erpnext/status
POST /erpnext/mock/create-site
POST /erpnext/mock/apply-template
```

Later real endpoints:

```txt
POST /erpnext/sites
POST /erpnext/sites/{site_name}/install-app
POST /erpnext/sites/{site_name}/configure-branding
POST /erpnext/sites/{site_name}/create-admin-user
POST /erpnext/sites/{site_name}/enable-modules
GET  /erpnext/sites/{site_name}/health
```

---

## 9. Phased implementation plan

### Phase 00 — Project control and decisions

Goal: create the source of truth for product, architecture, and implementation.

Deliverables:

- Repository initialized.
- `/docs` folder created.
- Master index document.
- Environment decisions.
- Naming conventions.
- Local development setup defined.
- SaaS-first architecture accepted.

Done when a new AI/developer can read the docs and understand the project.

---

### Phase 01 — Monorepo foundation

Goal: create the folder structure, local dev workflow, and basic documentation.

Deliverables:

- `/frontend` created.
- `/backend` created.
- `/docs` created.
- `/docker/local/docker-compose.yml` planned.
- `.env.example` files planned.
- Root README written.
- Backend health endpoint.
- Frontend public/app skeleton pages.

Done when frontend starts locally, backend starts locally, health check works, and README explains how to run both.

---

### Phase 02 — SaaS backend domain model

Goal: build the SaaS control database before any ERPNext integration.

Deliverables:

- Database models.
- Migrations.
- Pydantic schemas.
- CRUD service layer.
- Seed data for plans, modules, and templates.
- Local list endpoints for organizations, tenants, modules, plans, and templates.

Models to implement first:

- Organization.
- SaaSUser.
- OrganizationMembership.
- Tenant.
- Plan.
- Module.
- OrganizationModule.
- ImplementationTemplate.
- ImplementationProject.
- ImplementationTask.
- Domain.
- ProvisioningJob.
- AuditLog.

Done when database can be migrated and API can list organizations, tenants, modules, and templates.

---

### Phase 03 — SaaS authentication and authorization

Goal: create SaaS-level auth.

Deliverables:

- Register/login.
- Password hashing.
- Token/session management.
- Current user endpoint.
- Organization memberships.
- Internal admin role.
- Basic route protection.

Important: SaaS auth is for the SaaS control app. ERPNext tenant auth remains inside each ERPNext site.

Implementation note for the local-first build:

- Use opaque bearer tokens backed by a local `auth_sessions` table.
- Store the token in a frontend cookie for route-scaffold protection.
- Keep membership and role checks inside the SaaS control layer.

---

### Phase 04 — Main website and product shell

Goal: build the public-facing SaaS website and logged-in app shell.

Deliverables:

- Home.
- Pricing.
- Industries.
- Drilling page.
- Modules page.
- Demo request.
- Login.
- App dashboard.
- Organizations.
- Tenants.
- Modules.
- Implementation.
- Settings.

Implementation note for the local-first build:

- Treat `/app` as the canonical logged-in shell.
- Keep public marketing routes separate from the protected app routes.

Done when website communicates the product and logged-in app shell exists.

---

### Phase 05 — Tenant and module management

Goal: let the SaaS admin create organizations, tenants, and choose modules before ERPNext exists.

Deliverables:

- Create organization.
- Create tenant placeholder.
- Select implementation template.
- Enable/disable modules.
- Assign plan.
- Set tenant status.
- View tenant detail.
- View tenant modules.

Done when you can model a real drilling customer inside the SaaS database.

Phase 05 is now implemented in this repository and summarized in `docs/phase_summaries/05_Organizations_And_Tenants_Management_Summary.md`.

---

### Phase 06 — Implementation project workflow

Goal: turn each new client into a managed implementation project.

Deliverables:

- Generate implementation project from template.
- Generate tasks from template.
- Assign tasks.
- Track status.
- Track blockers.
- Store go-live date.
- Store notes.

Example drilling implementation tasks:

- Collect company legal info.
- Collect logo.
- Collect users.
- Define roles.
- Import customers.
- Import suppliers.
- Import items/materials.
- Configure warehouses.
- Configure equipment/assets.
- Configure crews.
- Configure job workflow.
- Configure invoice template.
- Test quote-to-invoice flow.
- Train admin.
- Train field supervisor.
- Go-live approval.

---

### Phase 07 — ERPNext integration abstraction

Goal: prepare for ERPNext without requiring live ERPNext infrastructure.

Deliverables:

- ERPNext integration interface.
- Mock ERPNext client.
- Real client skeleton.
- Provisioning service abstraction.
- Tenant ERP status page.
- Simulated site creation job.

Interface methods:

```txt
create_site(tenant)
install_erpnext(site_name)
install_custom_app(site_name, app_name)
configure_branding(site_name, branding)
create_admin_user(site_name, user)
enable_modules(site_name, modules)
get_site_health(site_name)
suspend_site(site_name)
backup_site(site_name)
```

---

### Phase 08 — Provisioning jobs and background worker

Goal: create durable long-running job handling.

Deliverables:

- ProvisioningJob model wired to service.
- Job status updates.
- Retry support.
- Logs per job.
- Background worker design.
- Admin UI for job logs.

---

### Phase 09 — Billing and subscription foundation

Goal: add billing structure, but do not block MVP on perfect automation.

Deliverables:

- Plan model connected to organizations.
- Subscription model.
- Manual subscription status management.
- Stripe customer/subscription fields.
- Webhook endpoint skeleton.
- Billing status shown in admin.

MVP rule: start with manual billing status if needed.

---

### Phase 10 — White-label and domain management

Goal: prepare the SaaS layer to manage branding and custom domains.

Deliverables:

- Branding settings.
- Logo URL.
- Primary color.
- Custom domain records.
- DNS verification status.
- SSL status.
- Domain activation workflow.

---

### Phase 11 — ERPNext live connection

Goal: connect the SaaS layer to real ERPNext/Frappe.

Prerequisite: ERPNext infrastructure exists.

Deliverables:

- Real ERPNext client.
- Token-based API auth.
- Site status check.
- Create/configure tenant through scripts or internal API.
- Link SaaS tenant to ERPNext site.
- Store ERPNext URL and API credential references.
- Health checks.

---

### Phase 12 — Drilling template connection

Goal: connect the SaaS implementation template to ERPNext/Frappe configuration.

Deliverables:

- Drilling template in SaaS.
- Matching ERPNext/Frappe setup script.
- Default roles.
- Default modules.
- Default workflows.
- Default custom fields.
- Default reports.
- Default checklists.

---

### Phase 13 — Production hardening

Goal: prepare for real customers.

Deliverables:

- Audit logs.
- Error handling.
- Security headers.
- Backup status.
- Basic monitoring.
- Admin-only controls.
- Rate limiting.
- Secrets management.
- Data export policy.
- Tenant suspension policy.

---

### Phase 14 — Pilot client onboarding

Goal: run the first real drilling client through the system.

Deliverables:

- Organization created.
- Tenant created.
- Modules selected.
- Implementation project generated.
- ERPNext site created.
- Branding/domain configured.
- Users created.
- Initial data imported.
- Go-live checklist completed.
- Support process defined.

---

### Phase 15 — Production website and launch readiness

Goal: finish the public website and launch-facing content.

Deliverables:

- Final homepage copy.
- Pricing page.
- Contact/demo flow.
- Legal pages.
- SEO metadata.
- Clear SaaS vs ERPNext positioning.

---

### Phase 16 — SaaS control-plane deployment on GCP

Goal: deploy the frontend and backend SaaS control plane on Google Cloud.

Deliverables:

- VM layout.
- Frontend deployment process.
- Backend deployment process.
- Reverse proxy and HTTPS.
- Health checks and smoke tests.

---

### Phase 17 — ERPNext deployment on GCP

Goal: deploy the ERPNext/Frappe tenant runtime on Google Cloud.

Deliverables:

- GCP VM setup.
- Docker/Frappe stack setup.
- Demo site creation.
- Tenant site creation.
- DNS and SSL.
- Backup and restore validation.

---

### Phase 18 — Live SaaS ↔ ERPNext integration cutover

Goal: move from mock integration to a live ERPNext connection path.

Deliverables:

- Live client wiring.
- Tenant-to-site mapping.
- Health checks.
- Provisioning smoke tests.
- Safe production toggle.

---

### Phase 19 — Production hardening

Goal: make the platform safe for real users and support operations.

Deliverables:

- Audit logs.
- Error handling.
- Rate limiting.
- Secrets management.
- Monitoring.
- Tenant suspension policy.
- Rollback guidance.

---

### Phase 20 — Pilot client go-live

Goal: take the first real client through the full SaaS and ERPNext onboarding flow.

Deliverables:

- Organization.
- Tenant.
- Plan.
- Modules.
- Implementation project.
- ERPNext site link.
- Branding.
- Domain.
- Users.
- Initial data.
- Training.
- Go-live checklist.
- Support plan.

---

## 10. How to use previous docs

- **Document 01 — Infrastructure:** use later when ready to deploy ERPNext/Frappe and production services.
- **Document 02 — SaaS Product Build:** use now for product scope, website, auth, plans, modules, and SaaS admin.
- **Document 03 — Tenant Provisioning:** use from Phase 07 onward.
- **Document 04 — Drilling Implementation Blueprint:** use early to define the real product value.
- **Document 05 — Custom Frappe App Development:** use later when building the Frappe app.
- **Document 06 — White Label Onboarding:** use from Phase 06 and Phase 10.
- **Document 07 — Backup/Restore/DR:** use when production and ERPNext infrastructure exist.

---

## 11. What not to build first

Do not start with:

- Full Stripe automation.
- Full ERPNext automatic tenant provisioning.
- Full custom-domain automation.
- Complex analytics.
- Mobile app.
- Replacing ERPNext UI.
- Kubernetes.
- Multi-cloud deployments.
- Heavy microservices.
- Enterprise SSO.
- Advanced permission engines.

Build the SaaS skeleton first. Then build enough workflow to onboard one drilling client. Then automate the repetitive parts.

---

## 12. Required phase summary format

At the end of every implementation phase, create:

```txt
docs/phase_summaries/Phase_XX_Summary_For_Future_Phases.md
```

Each summary must contain:

```txt
# Phase XX Summary For Future Phases

## What was built

## Files created/changed

## Database models/migrations added

## API endpoints added

## Frontend routes/screens added

## Environment variables added

## Important decisions

## Known limitations

## Manual testing checklist

## Next recommended phase
```

This keeps future AI sessions grounded and prevents context loss.
