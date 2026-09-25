# LenERP — Complete ERP Platform

**LenERP** is a complete ERP-as-a-Service platform built on Frappe and
ERPNext, expanded into a connected operating system for drilling, field
service, office operations, finance, people, payroll, inventory, assets,
quality, support, and customer work.

This repository contains the full LenERP product: the public and customer
platform, the multi-tenant SaaS services, the ERPNext integration layer, and
the LenERP Core application that turns standard ERPNext modules into one
industry-specific business system.

## What LenERP delivers

| Product layer | Responsibility |
|---|---|
| **LenERP product platform** | Customer onboarding, organizations, ERP sites, modules, implementation, billing, domains, authentication, support, and platform administration. |
| **LenERP ERP experience** | Role-based workspaces and connected workflows for customers, wells, field jobs, drilling, inventory, equipment, sales, accounting, HR, payroll, quality, projects, and support. |
| **LenERP Core** | Frappe application layer containing LenERP DocTypes, workflows, permissions, reports, print formats, accessibility, branding, SSO hooks, and industry-specific operations. |
| **ERPNext/Frappe foundation** | Companies, customers, contacts, selling, buying, stock, assets, accounting, projects, and the extensible document framework. |
| **HRMS and business extensions** | People operations, time off, timesheets, payroll, office work, and other connected capabilities. |

LenERP scales ERPNext/Frappe from a general-purpose ERP foundation into a
complete product for companies that need office coordination and field
execution in the same system. Standard ERPNext records remain the system of
record; LenERP adds the business relationships, workflows, user experience,
permissions, reports, and industry context that connect them.

## The LenERP operating model

LenERP connects the complete business journey:

```text
Lead or customer
  → Contact and well/site
  → Request, opportunity, or quotation
  → Drilling or service job
  → Schedule, crew, rig, truck, and materials
  → Field execution and completion
  → Invoice, payment, and accounting
  → Inventory, maintenance, dashboards, alerts, and history
```

The customer, site, job, equipment, materials, completion, invoice, and
payment records remain connected throughout the lifecycle. A completed field
job becomes useful to dispatch, accounting, inventory, maintenance, managers,
and future service teams instead of ending as an isolated task.

## Drilling, wells, and field jobs

Drilling and field service are first-class LenERP operations.

### Well and site management

`LenERP Well Site` is the canonical operational record for a customer-owned
well or service location. It provides:

- unique well/site identity and site name;
- customer and primary contact links;
- active, needs-review, and inactive status;
- address, city, state/region, postal code, latitude, and longitude;
- measured well depth;
- pump and equipment specifications;
- operational notes, documents, activity, and history;
- current and historical jobs;
- assigned crews, rigs, trucks, equipment, and materials;
- list and map views with search, filters, status markers, exports, and print.

Well validation protects coordinate ranges and prevents invalid negative depth.
Stored site coordinates are kept distinct from live GPS or live technician
tracking, so the location record remains a reliable business reference.

### Drilling and service jobs

`LenERP Drilling Job` is the operational work order connecting a customer to a
well/site and field crew. It includes:

- automatic `JOB-####` job references;
- new well drilling, pump installation, service call, water testing, and
  maintenance job types;
- planned, scheduled, in-progress, completed, and reopened states;
- routine, high, and emergency priorities;
- scheduled date, crew/personnel, drilling rig, truck, and other assets;
- work instructions, work notes, exceptions, and completion details;
- allocated materials through `LenERP Job Material`;
- completion date, change history, print output, and commercial context.

The standard job workflow is:

```text
Planned → Scheduled → In Progress → Completed
                                      ↓
                                   Reopened
```

Dispatch schedules work and assigns resources. Field technicians execute the
job and record the work. Completion requires completion details, and the
system validates dates and state transitions before closing the job. A
dispatcher can reopen work when follow-up is required.

### Dispatch and field execution

The field experience is mobile-first and focused on the work that needs to be
done today. It includes:

- assigned jobs, priorities, schedules, customer, well, and location context;
- start/check-in, instructions, checklists, notes, and structured capture;
- photos, forms, signatures, and supporting documents;
- material usage and stock issue context;
- rig, truck, and equipment confirmation;
- safety, quality, customer, and operational exception reporting;
- visible saved/submitted state;
- complete or submit-for-review actions;
- completion review, reopen handling, and invoice-ready handoff.

Dispatch views expose unassigned, overdue, blocked, emergency, conflicting,
and reopened jobs. Each role sees the work it owns without receiving
unrestricted access to payroll, accounting, or unrelated customer records.

### Materials, equipment, and maintenance

`LenERP Job Material` connects field work to ERPNext Items, UOMs, and
Warehouses. This provides a traceable path from purchase and receipt to
warehouse, job issue, usage, and stock reporting.

ERPNext Assets represent drilling rigs, trucks, pumps, and other equipment.
LenERP connects asset identity, assignment, availability, maintenance history,
preventive maintenance tasks, and the job/site where the asset is being used.

### Completion, commercial close, and history

The completion record preserves the customer, well/site, job dates, crew,
equipment, materials, work notes, completion details, photos, forms, and
signatures. Completion feeds office review, job history, invoice preparation,
asset history, inventory visibility, dashboards, alerts, and future service
planning.

The `Champion Operations Summary` report and `Champion Job Completion` print
format provide business-facing operational output for jobs, customers,
wells/sites, types, statuses, schedules, priorities, crews, and completion
details.

## Modules and business capabilities

LenERP improves every module used by the business with shared navigation,
roles, terminology, workflows, links, reports, accessibility, and customer or
job context.

| Module | LenERP capabilities |
|---|---|
| **CRM and customers** | Customers, contacts, leads, opportunities, follow-up, sites, jobs, activity, and customer history. |
| **Selling and quoting** | Requests, quotes, approvals, job context, completion handoff, invoicing, and payment follow-up. |
| **Accounting and finance** | Invoices, payments, receivables, accounting context, reconciliation, permissions, and management summaries. |
| **Buying and purchasing** | Suppliers, requests, purchase receipts, item availability, and purchasing connected to field demand. |
| **Stock and inventory** | Items, units, warehouses, receiving, transfers, job issue/usage, low-stock exceptions, and traceable movements. |
| **Assets and maintenance** | Rigs, trucks, equipment, assignments, availability, maintenance schedules, service history, and resource status. |
| **HR and people** | Employees, office work, time off, timesheets, manager access, confidentiality, and role-aware people operations. |
| **Payroll** | Payroll preparation, payroll previews, controlled visibility, and people/accounting integration. |
| **Drilling and field service** | Well mapping, wells/sites, drilling jobs, service calls, dispatch, field capture, materials, completion, and reopen handling. |
| **Projects and office work** | Task coordination, ownership, due dates, blockers, dependencies, handoffs, and follow-up. |
| **Quality and support** | Quality classifications, callbacks, rework, support issues, product-change requests, routing, and escalation. |
| **Reports and dashboards** | Job and well history, inventory exceptions, asset and maintenance status, alerts, KPIs, forms, exports, and branded print. |

## Roles and product experience

LenERP provides focused workspaces and least-privilege access for:

- Champion Administrator;
- Champion Dispatcher;
- Champion Sales User;
- Champion Accounting User;
- Champion Inventory Manager;
- Champion Field Technician;
- Champion Platform Operator.

The application adds role-aware navigation, direct-route and API permission
checks, confidential HR/payroll access, central sign-in, role-profile mapping,
responsive layouts, keyboard support, accessible status messaging, and
consistent LenERP branding across authenticated and public pages.

## Product architecture

LenERP uses a multi-organization, multi-tenant architecture in which each
customer ERP site runs Frappe/ERPNext plus LenERP Core. The platform services
manage the customer lifecycle and connect it to the ERP site:

1. A customer and its chosen modules are recorded in LenERP.
2. An ERP site is provisioned with the required Frappe, ERPNext, HRMS, and
   LenERP applications.
3. Modules, roles, workspaces, branding, and integrations are applied to that
   site.
4. ERPNext remains the transactional system of record for business documents.
5. LenERP provides the shared product experience, workflow context, reporting,
   support, implementation, billing, and operational visibility.

This separation lets LenERP scale new modules and customer capabilities in its
own application layer while keeping upstream Frappe and ERPNext clean,
pinned, and upgradeable.

## Repository layout

```
crm/
├── backend/          # FastAPI control-plane API (Python 3.11+)
│   ├── app/
│   │   ├── api/          # HTTP routers (auth, tenants, orgs, billing, …)
│   │   ├── core/         # Config, security headers, rate limiting, logging
│   │   ├── db/           # SQLAlchemy session, Alembic migrations, seed data
│   │   ├── integrations/ # ERPNext HTTP client + mock adapter
│   │   ├── models/       # ORM models (billing, domain, ERPNext)
│   │   ├── repositories/ # Data-access helpers
│   │   ├── schemas/      # Pydantic request/response shapes
│   │   └── services/     # Business logic (audit, billing, provisioning)
│   └── alembic/      # Database migration scripts
├── frontend/         # Next.js 15 marketing + app shell (React 19, Tailwind)
│   ├── app/
│   │   ├── (marketing)/  # Public pages: home, pricing, modules, industries
│   │   └── app/          # Authenticated shell: orgs, tenants, implementation
│   ├── components/   # Shared UI components
│   ├── features/     # Feature-scoped types (auth, billing, orgs, tenants)
│   └── lib/          # API client, auth helpers, env
├── scripts/
│   ├── deploy/       # Staging deploy and explicit production promotion
│   └── release/      # Immutable candidates, manifests, preflight, smoke, and guards
└── .github/
    └── workflows/    # GitHub Actions: deploy to self-hosted runner on push to main
```

## Tech stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Alembic, Pydantic v2
- **Database:** SQLite (local/MVP), configurable for PostgreSQL
- **Frontend:** Next.js 15, React 19, Tailwind CSS 3, Framer Motion
- **ERPNext:** Frappe/ERPNext (mocked locally, live via `ERPNEXT_MODE=live`)
- **Billing:** Stripe (mocked locally via `BILLING_PROVIDER=mock`)
- **CI/CD:** GitHub Actions → self-hosted Linux runner

## Local development

### Backend

Requires Python 3.11+.

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -e .
cp .env.example .env      # edit as needed
alembic upgrade head
python -m app.db.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs available at `http://localhost:8000/docs`.

### Frontend

Requires Node.js 18+.

```bash
cd frontend
npm install
npm run dev     # http://localhost:3000
```

## Environment variables

Copy `backend/.env.example` to `backend/.env`. Key variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///saas_control.db` | DB connection string |
| `BILLING_PROVIDER` | `mock` | `mock` or `stripe` |
| `STRIPE_API_KEY` | *(blank)* | Stripe secret key for live billing |
| `ERPNEXT_MODE` | *(unset)* | Set to `live` to enable real ERPNext calls |
| `SECURITY_HEADERS_ENABLED` | `true` | Inject security response headers |
| `RATE_LIMIT_ENABLED` | `false` | Enable per-IP rate limiting |
| `FRONTEND_BASE_URL` | `http://localhost:3000` | Used in auth email links |
| `PRODUCT_NAME` | `LenERP` | Customer-facing product identity |
| `ENVIRONMENT` | `local` | Runtime lane identity |
| `RELEASE_ID` | `local` | Candidate/release identity exposed by runtime metadata |
| `RELEASE_MANIFEST_PATH` | *(blank)* | Optional non-secret release manifest path |
| `FEATURE_FLAGS` | *(blank)* | Server-controlled comma-separated `name=on/off` flags |
| `RESEND_API_URL` | `https://api.resend.com/emails` | Configurable transactional-email service endpoint |

## API surface

| Router | Prefix | Description |
|--------|--------|-------------|
| auth | `/auth` | Login, logout, session, password reset, email verification |
| organizations | `/organizations` | CRUD for customer organizations |
| tenants | `/tenants` | CRUD for ERPNext tenant instances |
| billing | `/billing` | Subscriptions, invoices, webhook handling |
| provisioning | `/provisioning` | Tenant spin-up and ERPNext instance setup |
| implementation | `/implementation` | Onboarding task tracking |
| domain\_management | `/domains` | Custom domain assignment per tenant |
| catalog | `/catalog` | Module/plan catalog |
| integrations | `/integrations` | ERPNext integration status |
| audit | `/audit` | Platform-admin audit log viewer |
| contact / marketing | — | Contact form and marketing lead capture |
| health | `/health` | Liveness check |

## Deployment

CI builds one immutable candidate and deploys it to staging on push to `main` via `.github/workflows/deploy-saas-control.yml` using a self-hosted runner tagged `saas-control`. Production requires the separate protected manual workflow `.github/workflows/promote-saas-control-production.yml` and an existing tested candidate. The deployment scripts keep `current` and `previous` release pointers and restore the previous pointer after a failed post-switch smoke test.

Phase 0 operational evidence is tracked in [`docs/champion_execution/releases/PLAT-P0.md`](docs/champion_execution/releases/PLAT-P0.md), with the domain transition checklist in [`docs/champion_execution/DOMAIN_CUTOVER_CHECKLIST.md`](docs/champion_execution/DOMAIN_CUTOVER_CHECKLIST.md).

## ERPNext mode

By default, all ERPNext calls use a local mock. To point at a real instance:

```env
ERPNEXT_MODE=live
ERPNEXT_BASE_URL=https://your-erpnext.example.com
ERPNEXT_API_KEY=...
ERPNEXT_API_SECRET=...
```
