# Phase 16 — SaaS Control-Plane Deployment Readiness

## Date
2026-05-27

## Goal
Refine Phase 16 into a concrete, operator-friendly deployment preparation package for the SaaS control plane only, without executing deployment and without starting ERPNext cutover work.

## What changed

### Phase 16 runbook rewrite
- Reworked `docs/16_SaaS_Control_Plane_Deployment_On_GCP.md` from a general planning document into a step-by-step operator checklist.
- Expanded it further into a beginner-friendly GCP execution runbook with:
  - exact GCP Console menu paths
  - copy-paste host setup commands
  - exact Nginx hostnames for `crm.lenquant.com` and `crm-api.lenquant.com`
  - browser SSH, static IP, DNS, Certbot, restart, and smoke-test steps
  - updated Python instructions to use `python3` when the VM already provides `3.11+` (for example Ubuntu 26.04 with Python 3.14)
- Clarified that Phase 16 is **planning/readiness work**, not proof of executed deployment.
- Kept the phase boundary explicit:
  - SaaS control plane only
  - no ERPNext deployment yet
  - no live SaaS ↔ ERPNext cutover yet
  - no production secrets committed

### Execution order clarification
- Reorganized the document into a clear run sequence:
  1. prerequisites and entry gate
  2. GCP project and VM setup
  3. DNS preparation
  4. host layout
  5. base host bootstrap
  6. frontend runtime preparation
  7. backend runtime preparation
  8. `systemd` service preparation
  9. Nginx and TLS preparation
  10. health checks
  11. smoke tests
  12. restart procedure
  13. rollback procedure

### Repo-grounded runtime details
- Anchored the checklist to the repository’s current runtime shape:
  - frontend build/start flow from `frontend/package.json`
  - backend `uvicorn app.main:app` runtime from `backend`
  - backend health endpoint at `GET /health`
  - ERPNext runtime visibility endpoint at `GET /integrations/erpnext/runtime`
- Used the current frontend route structure for smoke-test coverage:
  - `/`
  - `/pricing`
  - `/contact`
  - `/demo`
  - `/login`
  - `/app`
  - `/app/organizations`
  - `/app/tenants`
  - `/app/settings`

### Safety and phase-boundary reinforcement
- Made the ERPNext safety expectations explicit for production-like environments:
  - local/test may still use mock where appropriate
  - production-like environments should not silently fall back to mock
  - live ERPNext enablement remains Phase 18 work
- Added a dedicated section for what is **still not done after Phase 16**.
- Added a dedicated section for what remains in Phase 17 and Phase 18.

### Documentation and automation sync
- Updated `docs/21_GCP_SaaS_And_ERPNext_Deployment_Guide.md` to:
  - use the correct document number in the title
  - reflect the fixed SaaS hostnames `crm.lenquant.com` and `crm-api.lenquant.com`
  - point operators to Phase 16 and Phase 17 as the primary execution runbooks
- Added `docs/22_GitHub_Actions_SaaS_Auto_Deploy.md` for post-setup SaaS deployment automation using a self-hosted GitHub Actions runner on the SaaS VM.
- Added repository automation assets:
  - `.github/workflows/deploy-saas-control.yml`
  - `scripts/deploy/deploy_saas_control.sh`
- Updated `docs/00_Master_Index.md` earlier in this phase series to:
  - include the missing phase summary entries for Phases 08–15
  - add the Phase 16 summary entry
  - refresh the phase sequence text through Phase 18 and the new deployment automation doc

## Validation run
- No code validation was run.
- This was a documentation-only refinement.

## What remains for later phases

### Still not done before real deployment
- actual GCP deployment execution
- actual DNS cutover
- final server-side secret placement
- final server bootstrapping and service activation on a real host
- production smoke testing on a live domain

### Phase 17
- deploy ERPNext/Frappe as the external runtime on GCP
- validate ERPNext site creation, routing, HTTPS, and backup/restore

### Phase 18
- explicitly enable and validate the live ERPNext client path
- validate tenant-to-site mapping against a real ERPNext environment
- validate live health/provisioning-related flows
- confirm safe live cutover and rollback behavior
