# Phase 17 — ERPNext Deployment Readiness

## Date
2026-05-27

## Goal
Refine Phase 17 into a concrete, operator-friendly deployment checklist for ERPNext/Frappe on GCP as the external tenant runtime, without blending it into SaaS deployment work or live integration cutover.

## What changed

### Phase 17 runbook rewrite
- Reworked `docs/17_ERPNext_Deployment_On_GCP.md` from a general planning document into a step-by-step operator checklist.
- Clarified that the document is a **planning/readiness runbook**, not evidence that ERPNext has already been deployed.
- Kept the architecture boundary explicit:
  - ERPNext runs as an external managed system
  - SaaS deployment remains Phase 16 work
  - live SaaS ↔ ERPNext cutover remains Phase 18 work

### Execution order clarification
- Reorganized the document into a clear run sequence:
  1. prerequisites and naming rules
  2. GCP project and ERP VM setup
  3. DNS preparation
  4. host layout
  5. base host bootstrap
  6. ERPNext runtime installation path
  7. demo site creation
  8. tenant site creation path
  9. custom app installation path
  10. DNS and TLS validation
  11. backup validation
  12. restore drill
  13. operational smoke tests
  14. restart procedure
  15. rollback procedure

### Topology clarification
- Made the recommended production-style topology explicit:
  - one VM for the SaaS control plane
  - one separate VM for ERPNext/Frappe
- Reinforced why ERPNext should not share the SaaS VM for the intended deployment path.

### Phase-boundary reinforcement
- Added a dedicated section for what is **still not done after Phase 17**.
- Added a dedicated section for what remains in **Phase 18**.
- Reinforced that Phase 17 stabilizes the ERP runtime but does not activate live SaaS integration.

### Master index sync
- Updated `docs/00_Master_Index.md` to add the new Phase 17 summary entry.
- Updated the phase sequence text to reflect Phase 17 as a separate ERP runtime deployment runbook on a separate GCP VM.

## Validation run
- No code validation was run.
- This was a documentation-only refinement.

## What remains for later phases

### Before live cutover
- actual ERPNext deployment execution on GCP
- demo-site creation on the real ERP host
- tenant-site creation validation on the real ERP host
- backup execution and restore drill on the real ERP runtime

### Phase 18
- explicitly enable and validate the live ERPNext client path from the SaaS backend
- validate tenant-to-site mapping against the deployed ERP runtime
- validate live health/status and provisioning-related flows
- confirm safe live cutover and rollback behavior
