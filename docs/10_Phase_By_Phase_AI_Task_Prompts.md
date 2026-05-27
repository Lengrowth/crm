# 10 — Phase-By-Phase AI Task Prompts

This document gives individual prompts for each build phase. Use these after the master prompt.

---

# Phase 00 Prompt — Project Control and Decisions

Read all available project docs. Do not code yet unless asked.

Create the project control documentation:

- `docs/00_Master_Index.md`
- `docs/00_Project_Decisions.md`
- `docs/00_Glossary.md`

Document:

- Product purpose.
- Target first vertical: drilling/manual field operations.
- SaaS-first strategy.
- Why ERPNext/Frappe comes later.
- Frontend/backend separation.
- Initial data model concepts.
- Environments.
- Naming conventions.
- What is in scope and out of scope.
- Phase order.

Stop after creating the docs and ask for review.

---

# Phase 01 Prompt — Monorepo Foundation

Implement the initial repository structure.

Create:

- `/frontend`
- `/backend`
- `/docs`
- `/docker`
- `/scripts`

Frontend:

- Next.js App Router.
- TypeScript.
- Tailwind.
- Basic public pages:
  - Home.
  - Login.
  - Demo.
  - Pricing.
  - Industries.
  - Drilling.
- Basic app shell pages:
  - Dashboard.
  - Organizations.
  - Tenants.
  - Implementation.
  - Settings.

Backend:

- Python API structure.
- Health endpoint.
- Config module.
- ERPNext integration placeholder.
- README.
- `.env.example`.

Docs:

- Root README.
- Frontend README.
- Backend README.
- Phase summary.

Do not build auth or database yet unless explicitly requested.

---

# Phase 02 Prompt — SaaS Backend Domain Model

Implement the SaaS database foundation.

Create models, migrations, schemas, services, and basic CRUD endpoints for:

- Organization.
- SaaSUser.
- OrganizationMembership.
- Tenant.
- Plan.
- Subscription.
- Module.
- OrganizationModule.
- ImplementationTemplate.
- ImplementationProject.
- ImplementationTask.
- Domain.
- ProvisioningJob.
- AuditLog.
- IntegrationCredential.

Add seed data for:

- Starter, Professional, Enterprise plans.
- CRM, Field Ops, Drilling, Fleet, Inventory, Reporting, White Label, Custom Domain, QuickBooks modules.
- Drilling Company MVP template.

Create documentation:

- `docs/data_model/SaaS_Data_Model.md`
- `docs/phase_summaries/Phase_02_Summary_For_Future_Phases.md`

Stop after Phase 02 and provide commands to run migrations and seed data.

---

# Phase 03 Prompt — SaaS Authentication and Authorization

Implement SaaS-level authentication.

Required:

- Register.
- Login.
- Logout/refresh if chosen.
- Current user endpoint.
- Password hashing.
- Token/session management.
- Organization membership checks.
- Platform roles and organization roles.
- Protected API routes.
- Protected frontend app routes.

Roles:

- platform_owner.
- platform_admin.
- implementation_manager.
- support.
- organization_owner.
- organization_admin.
- organization_viewer.

Important:

SaaS auth is separate from ERPNext auth.

Create docs:

- `docs/auth/SaaS_Authentication_And_Authorization.md`
- `docs/phase_summaries/Phase_03_Summary_For_Future_Phases.md`

---

# Phase 04 Prompt — Main Website and Product Shell

Build the public SaaS website and app shell.

Public pages:

- Home.
- Pricing.
- Industries.
- Drilling.
- Field Service.
- Modules.
- Demo request.
- Contact.
- Login.

App shell:

- Sidebar.
- Top nav.
- Dashboard.
- Organizations.
- Tenants.
- Modules.
- Implementation.
- Settings.

Product language:

- Do not position this as only ERPNext hosting.
- Position it as a field operations SaaS using ERP-powered workflows.
- First vertical is drilling.

Create docs:

- `docs/product/Public_Website_Copy_And_Routes.md`
- `docs/phase_summaries/Phase_04_Summary_For_Future_Phases.md`

---

# Phase 05 Prompt — Tenant and Module Management

Implement tenant/module management in the SaaS layer.

Required:

- Create organization.
- Create tenant placeholder.
- Assign plan.
- Select implementation template.
- Enable/disable modules.
- View tenant details.
- View tenant module settings.
- Update tenant status.
- Track provisioning status.

No live ERPNext connection yet.

Create docs:

- `docs/tenants/Tenant_And_Module_Management.md`
- `docs/phase_summaries/Phase_05_Summary_For_Future_Phases.md`

---

# Phase 06 Prompt — Implementation Project Workflow

Implement onboarding/implementation management.

Required:

- Generate implementation project from template.
- Generate implementation tasks.
- Assign tasks.
- Track statuses.
- Track blockers.
- Add notes.
- Set target go-live date.

Drilling MVP default tasks:

- Company info.
- Logo.
- Users.
- Roles.
- Customers import.
- Suppliers import.
- Items/materials import.
- Warehouses.
- Equipment/assets.
- Crews.
- Job workflow.
- Invoice template.
- Test quote-to-invoice.
- Training.
- Go-live approval.

Create docs:

- `docs/implementation/Implementation_Workflow.md`
- `docs/phase_summaries/Phase_06_Summary_For_Future_Phases.md`

---

# Phase 07 Prompt — ERPNext Integration Abstraction

Build the ERPNext integration abstraction.

Required structure:

```txt
backend/src/app/integrations/erpnext/
  base.py
  mock_client.py
  rest_client.py
  provisioning.py
  schemas.py
```

Required interface methods:

- create_site.
- install_erpnext.
- install_custom_app.
- configure_branding.
- create_admin_user.
- enable_modules.
- get_site_health.
- suspend_site.
- backup_site.

Implement mock client only.

Create frontend UI showing mock ERP status.

Create docs:

- `docs/integrations/ERPNext_Integration_Abstraction.md`
- `docs/phase_summaries/Phase_07_Summary_For_Future_Phases.md`

---

# Phase 08 Prompt — Provisioning Jobs and Background Worker

Implement durable provisioning jobs.

Required:

- Queue or background job design.
- Create provisioning jobs.
- Execute mock provisioning steps.
- Store logs.
- Store status.
- Retry failed jobs.
- Show logs in frontend.

Job sequence example:

1. Create site.
2. Install ERPNext.
3. Install custom app.
4. Apply template.
5. Configure branding.
6. Configure domain.
7. Issue SSL.
8. Create admin user.

Create docs:

- `docs/provisioning/Provisioning_Jobs.md`
- `docs/phase_summaries/Phase_08_Summary_For_Future_Phases.md`

---

# Phase 09 Prompt — Billing and Subscription Foundation

Add billing structure.

Required:

- Plans.
- Subscriptions.
- Billing status.
- Manual billing status update.
- Stripe fields.
- Stripe webhook skeleton.
- UI billing panel.

Do not require full Stripe integration before product validation.

Create docs:

- `docs/billing/Billing_And_Subscriptions.md`
- `docs/phase_summaries/Phase_09_Summary_For_Future_Phases.md`

---

# Phase 10 Prompt — White Label and Domain Management

Implement white-label/domain management.

Required:

- Logo URL.
- Brand colors.
- System subdomain.
- Custom domain.
- DNS target.
- DNS verification status.
- SSL status.
- Domain setup instructions.
- Manual activation status.

Do not automate DNS/SSL fully yet unless infrastructure exists.

Create docs:

- `docs/white_label/White_Label_And_Domain_Management.md`
- `docs/phase_summaries/Phase_10_Summary_For_Future_Phases.md`

---

# Phase 11 Prompt — ERPNext Live Connection

Only start this phase after ERPNext/Frappe infrastructure exists.

Replace mock ERPNext client with real connection.

Required:

- Frappe token auth.
- Site health checks.
- API credential storage by secret reference.
- Link tenant to ERPNext site URL.
- Basic DocType read test.
- Provisioning script integration if available.

Create docs:

- `docs/integrations/ERPNext_Live_Connection.md`
- `docs/phase_summaries/Phase_11_Summary_For_Future_Phases.md`

---

# Phase 12 Prompt — Drilling Template Connection

Connect SaaS drilling template to ERPNext/Frappe configuration.

Required:

- Default drilling modules.
- Default roles.
- Default workflows.
- Default DocType/custom field mapping.
- Default checklists.
- Default reports.
- ERPNext setup checklist.
- Automation/manual split.

Create docs:

- `docs/drilling/Drilling_Template_ERPNext_Connection.md`
- `docs/phase_summaries/Phase_12_Summary_For_Future_Phases.md`

---

# Phase 13 Prompt — Production Hardening

Prepare for real users.

Required:

- Audit logging.
- Error handling.
- Access control review.
- Rate limiting plan.
- Secrets management plan.
- Backup status.
- Monitoring hooks.
- Admin-only dangerous actions.
- Security checklist.
- Data export checklist.

Create docs:

- `docs/security/Production_Hardening.md`
- `docs/phase_summaries/Phase_13_Summary_For_Future_Phases.md`

---

# Phase 14 Prompt — Pilot Client Onboarding

Use the SaaS platform to onboard the first drilling client.

Required:

- Organization.
- Tenant.
- Plan.
- Modules.
- Implementation project.
- ERPNext site link.
- Branding.
- Domain.
- Users.
- Data import.
- Training checklist.
- Go-live checklist.
- Support plan.

Create docs:

- `docs/pilot/Pilot_Client_Onboarding.md`
- `docs/phase_summaries/Phase_14_Summary_For_Future_Phases.md`

---

# Phase 15 Prompt — Production Website and Launch Readiness

Finish the public website so it is ready for a real launch or pilot demo.

Required:

- Final homepage copy.
- Pricing page.
- Contact/demo flow.
- Legal pages.
- SEO metadata.
- Launch-ready CTA paths.
- Clear SaaS vs ERPNext positioning.

Create docs:

- `docs/phase_summaries/Phase_15_Summary_For_Future_Phases.md`

---

# Phase 16 Prompt — SaaS Control-Plane Deployment on GCP

Deploy the frontend and backend SaaS control plane on Google Cloud.

Required:

- VM layout.
- Frontend deployment steps.
- Backend deployment steps.
- Reverse proxy.
- HTTPS.
- Health checks.
- Smoke tests.
- Restart strategy.

Create docs:

- `docs/phase_summaries/Phase_16_Summary_For_Future_Phases.md`

---

# Phase 17 Prompt — ERPNext Deployment on GCP

Deploy ERPNext/Frappe as the external tenant runtime.

Required:

- GCP VM setup.
- Docker / Frappe stack setup.
- Demo site creation.
- Tenant site creation.
- SSL / DNS.
- Backup setup.
- Restore validation.
- Custom app install path.

Create docs:

- `docs/phase_summaries/Phase_17_Summary_For_Future_Phases.md`

---

# Phase 18 Prompt — Live SaaS ↔ ERPNext Integration Cutover

Switch from mock behavior to the live ERPNext connection path.

Required:

- Confirm live client wiring.
- Tenant-to-site mapping.
- Health checks.
- Provisioning smoke tests.
- Backup / restore calls.
- Safe production toggle.

Create docs:

- `docs/phase_summaries/Phase_18_Summary_For_Future_Phases.md`

---

# Phase 19 Prompt — Production Hardening

Make the system safe for real users and support operations.

Required:

- Audit logs.
- Error handling.
- Rate limiting.
- Secrets management.
- Monitoring.
- Tenant suspension policy.
- Data export policy.
- Rollback guidance.

Create docs:

- `docs/phase_summaries/Phase_19_Summary_For_Future_Phases.md`

---

# Phase 20 Prompt — Pilot Client Onboarding and Go-Live

Take the first client through the complete SaaS and ERPNext onboarding flow.

Required:

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

Create docs:

- `docs/phase_summaries/Phase_20_Summary_For_Future_Phases.md`
