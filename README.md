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

## Champion ERP relationship

The CRM repository is the platform foundation around the ERP site. It owns:

- organizations, tenants, ERP-site records, onboarding, and implementation;
- module catalog, bundles, dependencies, entitlements, and audit history;
- provisioning, installed-app verification, identity, domains, and billing;
- platform APIs, customer-facing SaaS screens, marketing, and administration.

Champion-specific ERP behavior lives in the private [`lenerp_core`](https://github.com/Len-OS/lenerp_core)
repository. That application owns the detailed Champion experience for:

- customers, contacts, wells, sites, and Well Mapping;
- drilling and field-service jobs, dispatch, crews, rigs, trucks, and materials;
- field execution, completion, reopening, invoicing context, and job history;
- inventory, assets, maintenance, office work, HR, payroll, quality, and support;
- Champion roles, workspaces, reports, forms, print formats, and ERP permissions.

Read the [Champion ERP README](https://github.com/Len-OS/lenerp_core) for the
field-job data model, drilling workflow, well/site behavior, Champion roles,
and ERP application details. This README documents the platform foundation;
it does not duplicate the Champion ERP operating manual.

## Platform module catalog

The CRM platform provides the shared catalog and module lifecycle used by
LenERP. It keeps module identity, dependencies, bundles, role/workspace
defaults, application requirements, and requested/entitled/applied/verified
states consistent across onboarding and provisioning.

The catalog includes Accounting, Buying, Selling, Stock, Assets, HR, Payroll,
Manufacturing, CRM, Quality, Projects, Support, Well Mapping, Field
Operations, Drilling, Fleet, Reporting, White Label, Custom Domain, Point of
Sale, and compatibility aliases. The Champion-specific behavior for those
modules is implemented in `lenerp_core`; this repository manages the platform
context around that application.

## Three-repository product structure

LenERP keeps its responsibilities separated across three private codebases:

| Repository | Product responsibility |
|---|---|
| **`Lengrowth/crm`** | SaaS foundation, organizations, tenants, onboarding, modules, provisioning, billing, domains, identity, implementation, and platform administration. |
| **`Len-OS/lenerp_core`** | Champion ERP application, including wells, drilling, field jobs, dispatch, materials, equipment, roles, workspaces, reports, and ERP-specific workflows. |
| **Private LenERP upstream repository** | Controlled Frappe, ERPNext, and HRMS fork/improvement layer for dependency pins, compatibility fixes, shared patches, and build/install integration. |

The upstream repository is the framework and ERP dependency layer. The
`lenerp_core` repository is the Champion business layer. The CRM repository is
the SaaS and delivery layer. This separation prevents Champion workflows from
being mixed into platform code or upstream framework code.

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
