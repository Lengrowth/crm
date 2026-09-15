# Phase 7 — Go-Live, Training, and Handover

## Goal

Converge the fixed platform phases, required Champion solution packages, accepted migration stages, and final-domain infrastructure; certify production, train Champion, transfer the complete purchased system, and start the contractual defect-warranty process.

## Entry requirements

- Fixed platform Phases 0–4 have passed their release gates.
- Every Included Champion package in `CHAMPION_SOLUTION_REGISTER.md` is accepted in staging or has an explicit written exception.
- Migration stages D01–D08 are complete for every included category and the D09 production runbook is approved.
- Final product name, Champion-controlled domain, DNS/registrar ownership, production infrastructure, GitHub destination, backup destination, service accounts, acceptance authority, validators, and trainers are recorded.
- The final release manifest, production backup, code rollback, data cutover rollback/correction, communication plan, and old-domain compatibility period are approved.

## Build scope

1. Close or explicitly accept all blocking UAT defects.
2. Run final production smoke, authorization, tenant-isolation, backup, restore-instruction, monitoring, and rollback checks.
3. Train office/dispatch, sales, accounting, inventory, field, management, and administrators on their actual workflows.
4. Deliver administrator and role-based user guides.
5. Deliver architecture, developer, code, build, deployment, migration, test, release, update, rollback, monitoring, and operating documentation.
6. Deliver data import, user/permission, module administration, onboarding/provisioning, backup, restoration, incident, and common-operations guides.
7. Deliver repository history, release tags, schemas, migrations, tests, deployment/config templates, dependency/license inventory, data exports, test records, issue register, and known limitations.
8. Transfer hosting, SSL, backup, service-account, and available administrative access through a secure channel.
9. Demonstrate community update rehearsal, recovery, module assignment, provisioning operator flow, and the Champion production workflow to the receiving administrator/developers.
10. Record final acceptance, warranty start, advisory/deferred items, and operational-copy deletion schedule.
11. Bind and verify the Champion-controlled production domain, update hostname-dependent configuration, and retain `erp.lengrowth.com` only as an approved temporary redirect/compatibility route.
12. Verify Champion has owner/equivalent administrative control of the transferred repositories, production infrastructure, DNS/registrar, SSL, backups, monitoring, and service accounts.
13. Deliver the completed Champion solution package register, data migration register, release records, acceptance evidence, and unresolved/accepted exception records.

## Acceptance tests

- Champion's acceptance owner completes the agreed production workflow.
- Every promised handover item has a recipient and receipt date.
- Repository/infrastructure ownership matches the executed agreement.
- Backup and restoration instructions are usable by the receiving administrator.
- All remaining issues are accepted, warranty, advisory, or deferred—never silently omitted.
- Warranty intake and release process is active for 30 days after go-live.
- Every Included Champion package maps to the exact production release and acceptance evidence.
- Final production migration D09 reconciles and Champion validators approve the result.
- Authentication, generated links, email templates, APIs, files, jobs, webhooks, backups, and monitoring operate on the Champion-controlled domain.
- The old implementation hostname exposes no independent Champion application or data after the approved transition.

## Deployment

The final release uses the same deployment gate as every earlier phase. There is no special direct-production shortcut for go-live. Freeze exact release tags and manifests after acceptance.

## Gate

Phase 7 passes when Champion can operate independently on its controlled domain/infrastructure, confirms receipt of code/data/documentation/access/training, accepts all required package and migration outcomes, signs final acceptance, and the warranty register is active.
