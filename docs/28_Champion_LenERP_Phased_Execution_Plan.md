# 28 — Champion LenERP Phased Execution Plan

**Status:** Active cross-repository execution baseline  
**Start date:** 2026-09-15  
**Planning rule:** Completion is measured by promised deliverables and acceptance evidence, not internal task-hour estimates.

The complete client, platform, infrastructure, reseller, handover, and warranty plan is maintained beside the controlling Champion proposal and agreement:

- [`../../champion-forecast/docs/COMPLETE_LENERP_DELIVERY_PLAN.md`](../../champion-forecast/docs/COMPLETE_LENERP_DELIVERY_PLAN.md)

The deploy-after-each-phase tactical sequence for this repository is:

- [`champion_execution/README.md`](champion_execution/README.md)

This `crm` repository implements the reseller/control-plane portions of that plan. Its responsibilities are:

1. Preserve the current AWS and Cloudflare deployment while security, ownership, backups, and recovery are verified.
2. Provide organizations, tenant sites, users, implementation records, domains, billing records, and audit history.
3. Replace placeholder module behavior with a persisted module catalog, bundles, dependency rules, organization entitlements, and an administrator UI.
4. Complete the approved reseller module showcase and future-company onboarding path.
5. Convert approved onboarding records into durable, idempotent tenant provisioning/configuration jobs.
6. Install and verify the versioned LenERP Frappe app, module bundle, roles, workspaces, branding, domain, and initial administrator for each tenant.
7. Expose provisioning progress, actionable failures, retry/rollback controls, health, domain/SSL status, and audit evidence.
8. Prove tenant isolation and complete a second-company dry run with synthetic data.
9. Deliver the source, tests, deployment materials, operating guides, dependencies/licenses, and known limitations required by the Champion handover.

The linked plan is canonical so commercial promises and implementation evidence cannot drift across repositories.
