# 09 — AI Build Prompt For SaaS-First ERPNext Project

Use this prompt when starting a new AI coding session.

Paste this prompt into the AI, then attach or paste the documentation pack:

- `01_GCP_ERPNext_Frappe_Infrastructure_Runbook.md`
- `02_ERPNext_SaaS_Product_Build_Runbook.md`
- `03_ERPNext_Tenant_Provisioning_And_SaaS_Connection_Runbook.md`
- `04_Drilling_ERPNext_Implementation_Blueprint.md`
- `05_Custom_Frappe_App_Development_Runbook.md`
- `06_White_Label_Client_Onboarding_Runbook.md`
- `07_Backup_Restore_Update_And_Disaster_Recovery_Runbook.md`
- `08_SaaS_First_Master_Build_Documentation.md`
- `10_Phase_By_Phase_AI_Task_Prompts.md`

---

# MASTER PROMPT

You are helping me build a SaaS-first platform that will later provision and control ERPNext/Frappe tenants.

## Context

I am building a vertical SaaS for field operations companies, starting with a drilling business use case.

The product will eventually use ERPNext/Frappe as the ERP/operations core, but I want to build the SaaS layer first.

The SaaS layer should handle:

- Main website.
- Demo/signup flow.
- Authentication.
- Organizations/accounts.
- Tenants.
- Plans.
- Modules.
- Implementation templates.
- Implementation projects/tasks.
- White-label settings.
- Domains.
- Provisioning jobs.
- ERPNext integration abstraction.
- Billing status.
- Admin dashboard.

ERPNext/Frappe comes later. For now, build interfaces/mocks so the SaaS platform is ready to connect to ERPNext.

## Required architecture

Use a monorepo-style structure:

```txt
project-root/
  frontend/
  backend/
  docs/
  docker/
  scripts/
```

Frontend:

- Next.js.
- TypeScript.
- App Router.
- Tailwind CSS.
- Clean component structure.
- Public marketing pages and logged-in SaaS dashboard.

Backend:

- Python.
- FastAPI preferred.
- SQLAlchemy or SQLModel.
- Alembic migrations.
- Pydantic schemas.
- REST API.
- Clear service layer.
- Role-based authorization.
- ERPNext integration layer with mock client first.

Database:

- Use a normal SQL database.
- PostgreSQL is acceptable for SaaS metadata.
- MariaDB is also acceptable if easier.
- Do not use ERPNext database directly for the SaaS control layer.

ERPNext/Frappe:

- Do not install ERPNext in this phase.
- Do not mix ERPNext code into the SaaS backend.
- Create integration abstractions under `backend/src/app/integrations/erpnext/`.
- Implement a mock ERPNext client first.
- Later replace it with real Frappe REST API/provisioning scripts.

## Very important implementation rules

1. Do not build everything at once.
2. Work phase by phase.
3. Before coding, read the relevant docs and summarize the phase objective.
4. After each phase, update documentation.
5. Keep `/frontend` and `/backend` separated.
6. Do not put backend logic inside the frontend.
7. Do not make the SaaS app depend on a live ERPNext instance yet.
8. Do not create a fake all-in-one demo with hardcoded data only.
9. Use proper models, migrations, schemas, services, and endpoints.
10. Every new model must have a clear purpose.
11. Every route/API must map to the SaaS concepts in the master docs.
12. Avoid overengineering: no Kubernetes, no microservices, no event streaming, no mobile app at the beginning.
13. Keep code production-oriented but MVP-friendly.
14. Document every phase.
15. Create a phase summary after every phase.

## Current goal

Start with the SaaS product foundation.

Do **not** start with GCP infrastructure.

Do **not** start with ERPNext deployment.

Do **not** start with Frappe custom app development.

Start with:

1. Project structure.
2. Frontend foundation.
3. Backend foundation.
4. SaaS domain model.
5. Auth.
6. Main website.
7. SaaS admin shell.
8. Tenant/module/implementation management.
9. ERPNext integration mock.

## Phase order

Follow this order:

```txt
Phase 00 — Project control and decisions
Phase 01 — Monorepo foundation
Phase 02 — SaaS backend domain model
Phase 03 — SaaS authentication and authorization
Phase 04 — Main website and product shell
Phase 05 — Tenant and module management
Phase 06 — Implementation project workflow
Phase 07 — ERPNext integration abstraction
Phase 08 — Provisioning jobs and background worker
Phase 09 — Billing and subscription foundation
Phase 10 — White-label and domain management
Phase 11 — ERPNext live connection
Phase 12 — Drilling template connection
Phase 13 — Production hardening
Phase 14 — Pilot client onboarding
```

If you cannot complete a phase in one response, complete a coherent subset and explain exactly what remains.

## First task

Begin with **Phase 00 and Phase 01 only**.

Do not continue to later phases until Phase 00 and Phase 01 are complete.

For Phase 00:

- Create/update project-level documentation.
- Define decisions and assumptions.
- Define initial environment variables.
- Define local development approach.

For Phase 01:

- Create folder structure.
- Create root README.
- Create frontend skeleton.
- Create backend skeleton.
- Create local Docker/dev planning files if appropriate.
- Create placeholder health endpoints and pages.
- Create docs folder structure.
- Create `docs/phase_summaries/Phase_01_Summary_For_Future_Phases.md`.

## Expected output

When implementing, provide:

1. Summary of what you are about to build.
2. Files created/changed.
3. Exact code changes.
4. Commands to run locally.
5. Environment variables required.
6. Manual QA checklist.
7. Known limitations.
8. Next phase recommendation.

## Required docs created by the AI

Create or update:

```txt
README.md
docs/00_Master_Index.md
docs/00_Project_Decisions.md
docs/phase_summaries/Phase_01_Summary_For_Future_Phases.md
frontend/README.md
backend/README.md
```

## Required initial backend structure

```txt
backend/
  pyproject.toml
  README.md
  .env.example
  src/
    app/
      __init__.py
      main.py
      api/
        __init__.py
        routes/
          __init__.py
          health.py
      core/
        __init__.py
        config.py
      db/
        __init__.py
      models/
        __init__.py
      schemas/
        __init__.py
      services/
        __init__.py
      integrations/
        __init__.py
        erpnext/
          __init__.py
          base.py
          mock_client.py
      workers/
        __init__.py
  tests/
    __init__.py
```

## Required initial frontend structure

```txt
frontend/
  README.md
  .env.example
  src/
    app/
      page.tsx
      layout.tsx
      globals.css
      login/
        page.tsx
      demo/
        page.tsx
      pricing/
        page.tsx
      industries/
        page.tsx
        drilling/
          page.tsx
      app/
        page.tsx
        organizations/
          page.tsx
        tenants/
          page.tsx
        implementation/
          page.tsx
        settings/
          page.tsx
    components/
      layout/
      ui/
    features/
      auth/
      organizations/
      tenants/
      modules/
      implementation/
    lib/
    services/
      api/
    types/
```

## Important product language

The product is a SaaS control platform for field operations companies.

Do not describe it only as “ERPNext hosting.”

Position it as:

- Field operations SaaS.
- ERP-powered operations platform.
- Modular operating system for manual-service companies.
- Starts with drilling, expands to construction, fleet, warehouse, and field service.

## Important domain rules

- One organization can have one or more tenants.
- One tenant eventually maps to one ERPNext/Frappe site.
- SaaS users are not the same as ERPNext users.
- Modules are reusable product capabilities.
- Implementation templates define repeatable onboarding.
- Provisioning jobs should be durable and logged.
- ERPNext integration must be abstracted.
- Billing should support manual status first, Stripe later.
- White-label should support logo, colors, system subdomain, and custom domain.

## Stop condition

After Phase 00 and Phase 01, stop and ask for review before implementing Phase 02.
