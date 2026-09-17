# Champion Execution Pack

**Status:** Active — PLAT-P1 verified; Phase 2 baseline available
**Started:** 2026-09-15  
**Purpose:** Deliver the complete Champion purchase through safe production releases while allowing Champion-specific configuration and data work to enter when their inputs become available.

This folder is the tactical implementation sequence for `../../../champion-forecast/docs/COMPLETE_LENERP_DELIVERY_PLAN.md`. The agreement and accepted proposal define the commercial obligation. The complete delivery plan defines the promised outcome. This pack defines how the work is built, released, validated, and handed over.

The completed Phase 1 production baseline is candidate
`12bc548056c59341d3ccc492a5353a696a7c0661`, with the responsive operator
shell enabled by the server-controlled `platform_phase1_shell` flag. The old
shell remains available through the same global flag for the next platform
phase; see
[`releases/PLAT-P1.md`](releases/PLAT-P1.md) for the evidence record.

## Current implementation assumptions

- The signed-agreement and cleared-payment dates must be recorded before contractual delivery is marked started.
- Champion's migration files are expected after platform work begins.
- `erp.lengrowth.com` is the temporary ERPNext implementation hostname; the SaaS control plane currently runs at `lenerp.lengrowth.com`. Phase 1 shell acceptance uses the SaaS hostname plus the non-public staging lane. The final production hostname will use a new domain bought and controlled for Champion.
- The existing AWS/Cloudflare environment may be used during implementation, but final infrastructure, repository, DNS, SSL, backup, and administrative ownership must match the agreement at handover.
- No application behavior, generated link, callback, cookie scope, email template, webhook, or monitoring rule may depend permanently on `lengrowth.com`.
- Known exposed implementation credentials may remain temporarily only while the environment contains no Champion confidential data, by the delivery owner's recorded decision. They remain an open security item, must not be committed, and must be rotated before any Champion data is received or loaded.
- Production is never the first environment to receive a code, schema, configuration, or import change.
- Existing URLs and APIs remain compatible until replacements are deployed and verified.

## Execution model

The program has three coordinated tracks. See [`PROGRAM_AND_RELEASE_MODEL.md`](PROGRAM_AND_RELEASE_MODEL.md) for the complete rules.

### Track A — fixed platform phases

| Phase | Document | Production outcome |
|---|---|---|
| 0 | [`00_RELEASE_SAFETY_FOUNDATION.md`](00_RELEASE_SAFETY_FOUNDATION.md) | Reproducible staging-first delivery, backups, restore, rollback, custom-app boundary, and temporary-domain controls |
| 1 | [`01_UX_SHELL_AND_MENU.md`](01_UX_SHELL_AND_MENU.md) | Responsive CRM/reseller application shell with compatible routes |
| 2 | [`02_CORE_PAGES_AND_DESIGN_SYSTEM.md`](02_CORE_PAGES_AND_DESIGN_SYSTEM.md) | Reusable design system and operational CRM pages |
| 3 | [`03_MODULE_CONTROL.md`](03_MODULE_CONTROL.md) | Shared module catalog, bundles, entitlements, application status, and audit |
| 4 | [`04_ONBOARDING_AND_PROVISIONING.md`](04_ONBOARDING_AND_PROVISIONING.md) | Reseller module selection, reviewed onboarding, and controlled tenant provisioning |
| 7 | [`07_GO_LIVE_TRAINING_AND_HANDOVER.md`](07_GO_LIVE_TRAINING_AND_HANDOVER.md) | Final-domain production cutover, accepted Champion operation, training, and complete ownership handover |

Platform production promotions remain ordered `0 -> 1 -> 2 -> 3 -> 4 -> 7`. Phase 7 cannot start until the required Champion solution packages and migration stages have converged.

### Track B — Champion solution packages

Champion pages, modules, roles, workflows, reports, and configuration are delivery packages, not one immovable calendar phase. They may enter after their dependencies and requirements are ready, between platform releases or near the end. They are governed by [`05_ERP_UX_AND_DRILLING_PAGES.md`](05_ERP_UX_AND_DRILLING_PAGES.md) and tracked in [`CHAMPION_SOLUTION_REGISTER.md`](CHAMPION_SOLUTION_REGISTER.md).

### Track C — continuous data migration

Migration begins with source inventory and mapping before the files arrive, continues through repeatable staging imports and reconciliation, and ends with the production cutover. It is governed by [`06_CHAMPION_DATA_AND_WORKFLOWS.md`](06_CHAMPION_DATA_AND_WORKFLOWS.md) and tracked in [`DATA_MIGRATION_REGISTER.md`](DATA_MIGRATION_REGISTER.md).

## What can be ready before Champion data

- Release safety, staging, rollback, and the `lenerp_core` application boundary.
- CRM/reseller design, navigation, organizations, implementations, tenant records, and operator views.
- The shared public/internal module catalog, dependency rules, bundles, entitlement workflow, and audit.
- A draft Champion module profile and role/navigation structure, pending approval.
- Reseller module selection and onboarding that creates a reviewed request rather than mutating a live tenant.
- Controlled provisioning proven with a synthetic second company.
- Champion Well/Job schema and workflow scaffolding where discovery decisions are approved, using synthetic records.
- Import templates, batch controls, source-register structure, mapping rules, rejection reports, and reconciliation formats.
- Domain-independent application configuration and a documented transition from the temporary hostname.

This is a reusable platform and a synthetic Champion foundation. It is not final Champion acceptance. Real data and approved operational decisions are still required for final permissions, field mappings, workflows, reports, reconciliation, UAT, training, and cutover.

## Mandatory release gate

Every platform phase, Champion solution package, and data/import release uses [`PHASE_DEPLOYMENT_GATE.md`](PHASE_DEPLOYMENT_GATE.md). A release is complete only when its exact artifact, configuration, schema revision, affected package IDs, test evidence, backup/recovery plan, approver, and production result are recorded.

## Compatibility and package rules

- Use additive, backward-compatible migrations. Destructive cleanup belongs in a later release.
- Add new APIs before moving the UI; retire old APIs only after consumers are verified absent.
- Keep old URLs as compatible routes or redirects through the domain transition.
- Put incomplete pages, module actions, and provisioning commands behind server-controlled flags.
- New module settings default to disabled until approved.
- Provisioning and imports must be idempotent and safe to retry.
- A public module choice creates an onboarding request. It never directly grants an entitlement or provisions infrastructure.
- Keep `marketed`, `requested`, `entitled`, `applied`, and `verified` module states distinct.
- Do not combine a broad UI redesign, destructive schema change, and production data migration in one release.
- If a production smoke test fails, roll back the code/configuration release instead of debugging on the live release.
- A Champion package may be inserted between platform phases, but it receives its own release identity and cannot bypass the deployment gate.

## Start here

Start with Phase 0. Record contract commencement, baseline the existing environment, protect the current data, create staging, establish the custom-app boundary, and prove recovery before changing the production experience.

The active Phase 0 release record is [`releases/PLAT-P0.md`](releases/PLAT-P0.md), with the non-secret Phase 0 record manifest in [`releases/PLAT-P0-manifest.json`](releases/PLAT-P0-manifest.json). The deployed candidate carries its own runtime manifest generated from `ops/production/release-runtime-baseline.json`; the protected production readback and backup evidence are complete.

Design and discovery can proceed locally while Phase 0 is being completed, but no later phase or package is promoted to production before the Phase 0 gate passes.
