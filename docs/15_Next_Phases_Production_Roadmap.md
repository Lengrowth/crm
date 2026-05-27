# Next Phases Production Roadmap

**Project:** SaaS-first ERPNext control platform
**Scope:** production readiness, public website completion, Google Cloud deployment, ERPNext deployment, and go-live hardening
**Last updated:** 2026-05-27

---

## 1. Why this roadmap exists

The repository already contains a solid SaaS control-plane foundation, but it is still not a finished production launch package.

This roadmap turns the remaining work into **clear, execution-ready phases** so you can finish the website, deploy the SaaS app, deploy ERPNext, connect both systems, and then launch the first client with a controlled rollout.

This document is intentionally forward-looking. It is not a build log. It is the plan for the remaining work.

---

## 2. What I found in the repository

### 2.1 What is already in place

- **Frontend shell exists.**
  - Public marketing routes exist.
  - Protected `/app` shell exists.
  - The UI is intentionally placeholder-style and SaaS-first.

- **Backend control plane exists.**
  - Organizations, tenants, plans, modules, billing state, provisioning jobs, and implementation models are present.
  - Auth scaffolding and SaaS CRUD are already established.

- **ERPNext integration abstraction exists.**
  - A real HTTP client exists.
  - A mock client exists.
  - A service layer exists to coordinate provisioning.
  - Provisioning metadata and records are already modeled.

- **Deployment documentation already exists in pieces.**
  - The GCP infrastructure runbook exists.
  - The tenant provisioning runbook exists.
  - The backup/restore / disaster recovery runbook exists.
  - The phase prompt document already reaches Phase 14.

### 2.2 What is still placeholder or incomplete

- **The website is not production-complete.**
  - Public pages still need final launch copy, metadata, legal pages, and conversion paths.

- **Live ERPNext is not fully cut over.**
  - The repo still defaults to mock behavior in multiple places.
  - There are still integration and wiring decisions to finalize before production use.

- **Provisioning is not yet a durable background workflow.**
  - The current worker path is still synchronous/in-process.
  - That is acceptable for development, but not ideal for live tenant onboarding.

- **Deployment manifests are not yet repo-native.**
  - There is good runbook material, but no complete production deployment package in the codebase snapshot.

### 2.3 Important constraint for this roadmap

- **Environment variables are out of scope for this document.**
  - You said you will place the production env vars on the server yourself.
  - This roadmap therefore focuses on everything else: code, routes, deployment flow, infrastructure steps, validation, and operational readiness.

---

## 3. Guiding principles for the remaining phases

- **Keep the SaaS control layer separate from ERPNext.**
  - The SaaS app owns tenants, billing state, module entitlements, and operational metadata.
  - ERPNext remains the external tenant runtime.

- **Do not launch production with mock integration behavior active.**
  - Mock mode is useful for development and testing only.
  - Production must use a real integration path once verified.

- **Prefer simple, repeatable operations.**
  - Use one clear deployment pattern.
  - Avoid premature complexity.

- **Backups and restore must exist before paid clients.**
  - Do not treat backup/restore as optional.

- **Roll out in waves.**
  - Internal demo first.
  - Then staging.
  - Then the first friendly client.
  - Then the broader client set.

---

## 4. Proposed remaining phases

The repository’s current phase documentation reaches Phase 14. The following phases extend that work into production launch.

---

### Phase 15 — Production website and launch readiness

**Goal:** turn the public website and shell into something you can actually show a lead, trial user, or pilot client.

**What must be completed**

- Replace placeholder marketing copy with launch-ready copy.
- Finalize the homepage positioning.
- Add or confirm key public routes:
  - home
  - pricing
  - contact/demo request
  - login
  - privacy policy
  - terms of service
  - security/contact page if needed
- Make the public site explain the product boundary clearly:
  - SaaS control plane first
  - ERPNext as the tenant runtime
  - implementation and onboarding as part of the service
- Add production-grade metadata:
  - page titles
  - descriptions
  - Open Graph metadata
  - favicon / brand assets
  - indexing rules
- Verify that the marketing routes and dashboard routes are cleanly separated.
- Ensure CTA flow is simple:
  - request demo
  - sign in
  - contact sales
  - see pricing

**Suggested deliverables**

- Final marketing homepage copy.
- Pricing page content or pricing placeholder with clear CTA.
- Contact/demo flow.
- Legal pages.
- SEO metadata.
- Public launch checklist.

**Exit criteria**

- A visitor can understand what the product does in under 30 seconds.
- A visitor can tell the difference between the SaaS control app and an ERPNext tenant.
- The site is presentable for an actual public launch or pilot demo.

---

### Phase 16 — SaaS control-plane deployment on Google Cloud

**Goal:** deploy the SaaS control app itself on GCP in a repeatable way.

**What must be completed**

- Decide the SaaS deployment topology.
  - Recommended: a dedicated SaaS app VM or service boundary.
  - Keep it separate from ERPNext if production reliability matters.
- Define the runtime approach for the frontend and backend.
  - Frontend build and serve process.
  - Backend API process.
  - Reverse proxy and TLS termination.
- Define the production host layout:
  - app domain
  - API domain or subdomain
  - logs location
  - deployment directory
  - restart strategy
- Document operational startup and restart commands.
- Verify that the SaaS app can be launched with production settings on GCP.
- Add final deployment validation for:
  - health check endpoint
  - login/register flow
  - organization and tenant CRUD
  - dashboard shell
  - public website routes

**Suggested deliverables**

- GCP project setup checklist.
- VM provisioning checklist.
- Firewall and DNS checklist.
- Frontend/backend startup instructions.
- Reverse proxy configuration instructions.
- Smoke-test checklist.

**Exit criteria**

- The SaaS app is reachable through a production domain.
- The app can serve public pages and the protected shell.
- Core SaaS APIs are reachable and working in production mode.

---

### Phase 17 — ERPNext deployment on Google Cloud

**Goal:** deploy ERPNext/Frappe as the external tenant runtime on GCP.

**What must be completed**

- Provision the ERPNext host or bench environment.
- Set up the Frappe/ERPNext runtime with the documented architecture.
- Create a demo site.
- Create the first tenant site.
- Install ERPNext.
- Install the custom app when ready.
- Configure DNS and SSL for each site.
- Verify site routing and tenant isolation.
- Test site backup and restore.

**Suggested deliverables**

- GCP VM / host setup instructions.
- Frappe / ERPNext runtime installation steps.
- Site creation steps.
- Custom app installation steps.
- Domain and SSL setup steps.
- Backup and restore validation steps.

**Exit criteria**

- A new ERPNext site can be created on the GCP host.
- ERPNext loads over HTTPS.
- The site can be backed up and restored in a test flow.
- A tenant can be identified by domain and site name consistently.

---

### Phase 18 — Live SaaS ↔ ERPNext integration cutover

**Goal:** switch from mock behavior to a real SaaS-to-ERPNext integration path under controlled conditions.

**What must be completed**

- Confirm the real HTTP client path is wired correctly.
- Remove ambiguity between mock and live integration code paths.
- Document how tenant records map to ERPNext site metadata.
- Store integration references in the SaaS layer.
- Validate provisioning calls against a real ERPNext environment.
- Validate status/health queries against a real ERPNext site.
- Validate backup and restore operations against the real environment.
- Confirm the production toggle path is explicit and safe.

**Suggested deliverables**

- Live integration checklist.
- Mock vs live mode decision matrix.
- Tenant-to-site mapping documentation.
- Health/status call documentation.
- Provisioning smoke test documentation.

**Exit criteria**

- A SaaS tenant can be linked to a real ERPNext site.
- Provisioning works against the real runtime.
- Site status can be checked from the SaaS layer.
- The system is no longer relying on mock behavior in production.

---

### Phase 19 — Operational hardening and recovery readiness

**Goal:** make the system safe enough for real customers.

**What must be completed**

- Add or finalize audit logging.
- Add meaningful error handling and operator-visible failures.
- Add rate limiting where needed.
- Add admin-only protection for dangerous actions.
- Document backup, restore, and retention policy.
- Add monitoring and alerting.
- Document incident response and rollback steps.
- Confirm tenant suspension and reactivation rules.
- Confirm the support process for a failed provisioning or failed update.

**Suggested deliverables**

- Security hardening checklist.
- Monitoring checklist.
- Backup / restore drill results.
- Rollback guide.
- Tenant suspension policy.
- Incident response notes.

**Exit criteria**

- You can recover from a failed deployment.
- You can recover from a failed tenant provisioning.
- You can tell whether the platform is healthy without guessing.
- You can suspend or restore a tenant without data loss.

---

### Phase 20 — Pilot client onboarding and first go-live

**Goal:** take the first real client through the system end to end.

**What must be completed**

- Create the organization.
- Create the tenant.
- Assign the plan.
- Enable the purchased modules.
- Generate the implementation project.
- Provision the ERPNext site.
- Configure branding and domain.
- Create users.
- Import initial data.
- Complete the training and go-live checklist.
- Define support escalation and ownership.

**Suggested deliverables**

- Pilot onboarding checklist.
- Internal training checklist.
- Client go-live checklist.
- Support escalation checklist.
- Initial success criteria for the pilot.

**Exit criteria**

- The first client can work in the system.
- The client can log in and complete core workflows.
- The client has a support path.
- The team has a repeatable onboarding process.

---

## 5. Recommended order of execution

If you want the shortest practical path to production, do these in order:

1. **Finish the production website.**
2. **Deploy the SaaS control app on GCP.**
3. **Deploy ERPNext/Frappe on GCP.**
4. **Cut over from mock to live ERPNext integration.**
5. **Harden operations and verify backup/restore.**
6. **Onboard the first pilot client.**

---

## 6. Documents that should exist alongside these phases

These are the docs that should be maintained as this roadmap progresses:

- Production deployment guide for the SaaS app.
- GCP infrastructure runbook.
- ERPNext deployment runbook.
- Live integration guide.
- Production hardening / security checklist.
- Backup / restore / rollback runbook.
- Pilot client onboarding checklist.

---

## 7. Final note

This roadmap deliberately keeps the SaaS control plane and ERPNext deployment as separate concerns.

That separation is the safest way to reach production without accidentally mixing the product boundary with the tenant runtime.
