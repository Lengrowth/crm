# LenERP — SaaS Control Plane

**LenERP** is a managed ERP-as-a-Service platform built on top of ERPNext/Frappe. This repo is the **SaaS control plane** — the layer that sits above ERPNext and handles multi-tenancy, billing, onboarding, and the public marketing site.

## What it does

| Layer | Responsibility |
|-------|---------------|
| **Marketing site** | Public-facing Next.js website for LenERP (landing, pricing, modules, industries) |
| **Control API** | FastAPI backend managing organizations, tenants, billing, provisioning, and auth |
| **ERPNext integration** | Adapter layer that provisions and configures ERPNext instances per tenant |

The platform supports multi-organization, multi-tenant architecture where each tenant maps to an ERPNext instance. The control plane handles everything that is *outside* ERPNext: sign-up flow, subscription billing, domain management, implementation tracking, and platform-admin audit tooling.

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
