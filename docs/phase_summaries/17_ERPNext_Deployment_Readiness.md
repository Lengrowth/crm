# Phase 17 — ERPNext Deployment Readiness

## Date
2026-05-27

## Goal
Refine Phase 17 into a concrete, beginner-friendly deployment checklist for ERPNext/Frappe on GCP as the external tenant runtime, with the same operator guidance style as Phase 16.

## What changed

### Phase 17 runbook rewrite
- Reworked `docs/17_ERPNext_Deployment_On_GCP.md` into a detailed step-by-step GCP runbook.
- Expanded it from a high-level checklist into a beginner-friendly operator guide with:
  - exact GCP Console menu paths
  - static IP reservation steps
  - explicit firewall creation steps for ports `80` and `443`
  - browser SSH guidance
  - copy-paste Docker / Compose / Frappe commands
  - staged DNS and HTTPS validation
- Kept the architecture boundary explicit:
  - ERPNext runs as an external managed system
  - SaaS deployment remains Phase 16 work
  - live SaaS ↔ ERPNext cutover remains Phase 18 work

### Concrete ERP hostname walkthrough
- Made the ERP hostnames concrete for the first deployment walkthrough:
  - `demo-erp.lenquant.com`
  - `champion.lenquant.com`
- Reinforced that these are intentionally separate from:
  - `crm.lenquant.com`
  - `crm-api.lenquant.com`

### Execution order clarification
- Reorganized the document into a very explicit run sequence:
  1. GCP project, billing, and API setup
  2. static IP reservation
  3. Cloud Storage backup bucket creation
  4. ERP VM creation
  5. explicit firewall rule creation
  6. DNS setup and verification
  7. Docker and Compose installation
  8. Frappe Docker clone and env setup
  9. ERP runtime startup
  10. demo site creation and validation
  11. first tenant site creation and validation
  12. custom app installation shape
  13. backup validation
  14. restore drill guidance
  15. restart and rollback basics

### Operator-friendly details added
- Added explicit guidance to avoid the issues already seen in Phase 16:
  - do not rely only on VM HTTP/HTTPS checkboxes
  - create firewall rules explicitly
  - verify DNS before expecting TLS to work
  - test the demo site first, then expand `SITES_RULE` for the first tenant site
- Added a concrete `.env` template shape for the ERP runtime with:
  - pinned ERPNext version
  - Let’s Encrypt email
  - initial `SITES_RULE`

### Documentation sync
- Updated `docs/21_GCP_SaaS_And_ERPNext_Deployment_Guide.md` to reflect the concrete ERP hostname examples used in the new Phase 17 runbook.

## Validation run
- No code validation was run.
- This was a documentation-only refinement.

## What remains for later phases

### Before live cutover
- actual ERPNext deployment execution on GCP
- demo-site creation on the real ERP host
- first tenant-site creation validation on the real ERP host
- backup execution and restore drill on the real ERP runtime

### Phase 18
- explicitly enable and validate the live ERPNext client path from the SaaS backend
- validate tenant-to-site mapping against the deployed ERP runtime
- validate live health/status and provisioning-related flows
- confirm safe live cutover and rollback behavior
