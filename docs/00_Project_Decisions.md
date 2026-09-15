# Project Decisions

## Decision 1: SaaS First, ERPNext Second

The repository is designed as a SaaS control platform first. ERPNext/Frappe is not the first deliverable and should not be required for local development of the foundation.

## Decision 2: Separate Frontend And Backend

- `/frontend` will hold the Next.js App Router application.
- `/backend` will hold the Python API and integration adapters.
- The two applications communicate over HTTP.

## Decision 3: SaaS Control Layer Owns Metadata Only

The SaaS database stores organizations, users, tenants, plans, modules, subscriptions, domains, provisioning jobs, audit logs, and integration metadata. ERPNext stores operational ERP data in its own tenant site databases later.

## Decision 4: ERPNext Must Remain Abstract At First

ERPNext/Frappe connections are modeled as interfaces and mocks until the live tenant infrastructure exists. No live ERPNext server is required for the first phases.

## Decision 5: FastAPI Style Backend

The backend will use a FastAPI-style layout with separate `api`, `core`, `db`, `models`, `schemas`, `services`, `integrations`, and `workers` packages.

## Decision 6: Next.js App Router Frontend

The frontend will use Next.js App Router with TypeScript and a clean route-group structure for marketing, auth, and dashboard shells.

## Decision 7: PostgreSQL As The SaaS Target Database

The docs recommend PostgreSQL for SaaS metadata. The backend will be structured to support that target, while still keeping the first phases lightweight.

## Decision 8: No Secrets In Git

Only `.env.example` files are committed. Real environment variables stay local or in deployment systems.

## Decision 9: Phase Summaries Are Required

Every phase must end with a short summary under `/docs/phase_summaries` so the build history stays easy to audit.

## Decision 10: Minimal Dependencies

Only add dependencies when they are needed by the current phase. Prefer a small, production-oriented stack over premature tooling.

## Decision 11: AWS And Cloudflare Are The Current Runtime Baseline

The existing AWS EC2, nginx, and Cloudflare deployment is the current as-built runtime. Earlier GCP documents remain historical references and must not be treated as an instruction to migrate the active pilot.

## Decision 12: LenERP Extends Upstream Through A Custom App

Permanent LenERP business behavior, drilling records, roles, workspaces, reports, fixtures, styling, and migrations belong in a version-controlled custom Frappe app. Upstream framework and ERP source trees remain pinned and unmodified so community updates can be evaluated and applied through development and staging first.

## Decision 13: LenERP Is The Customer-Facing Brand

Client-facing UI, domains, print formats, messages, and ordinary product documentation use LenERP branding. Private technical handover material retains accurate dependency versions and required third-party license/copyright notices. Upstream code is not represented as authored by LenERP.

## Decision 14: Champion Execution Is Deliverable-Driven

Internal execution planning is organized by promised outcomes and acceptance gates rather than hour allocations. The executed agreement remains the commercial authority, while the complete cross-repository plan and promise traceability matrix live in `../champion-forecast/docs/COMPLETE_LENERP_DELIVERY_PLAN.md`. Reusable module administration, provisioning, reseller onboarding, UX, security, handover, and warranty work are included in that single traceable program wherever required by the active promises.
