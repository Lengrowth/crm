# Phase 0 — Release Safety Foundation

## Goal

Create a deployment path in which candidate code is built and tested before it receives production traffic, and the previous release can be restored quickly. The delivered outcome remains a real Champion production ERP; staging is the verification path to that live system, not a substitute for it. This phase comes before production UX work because the current script updates the live checkout, migrates the live database, restarts services, and only then performs health checks.

## Repository and application model established in this phase

```text
frappe          pinned upstream clone; no LenERP edits
erpnext         pinned upstream clone; no LenERP edits
lenerp_core     LenERP custom Frappe app and private Git repository
crm             reseller website and SaaS/module-control repository
site database   Champion business records; never stored in Git
site files      Champion public/private attachments; never stored in Git
```

The development and staging benches clone the same Frappe and ERPNext remotes and exact commits currently approved for production. LenERP does not use a modified ERPNext fork unless a specific upstream limitation is documented and Matt accepts the long-term maintenance consequence. All normal LenERP records, pages, menus, roles, workspaces, CSS/JS, reports, print formats, fixtures, hooks, and patches live in `lenerp_core`.

## Build scope

0. Record the executed-agreement date, cleared-payment date, Service Commencement Date, delivery owner, Champion acceptance authority, and the current ownership of repositories, AWS, Cloudflare, DNS, backups, and service accounts.
1. Record the current production commits for `frappe`, `erpnext`, and every installed app, plus site database revisions, service definitions, environment-file locations, nginx routes, domains, and health endpoints without recording secret values.
2. Confirm the upstream remotes and create a version manifest containing exact commit SHAs—not only broad branch names such as `version-15`.
3. Create development/staging clones of the approved Frappe and ERPNext versions. Confirm their worktrees are clean and keep their upstream remotes unchanged.
4. Scaffold `lenerp_core` as a separate custom Frappe app, initialize its private repository, install it on a development site, and prove that an empty initial version can be installed and removed without modifying upstream source.
5. Add an automated check that fails when tracked changes appear inside the upstream `frappe` or `erpnext` repositories.
6. Verify current database, site configuration, public-file, and private-file backups and an off-host copy; perform a restoration rehearsal outside production.
7. Create a staging lane with separate frontend/backend processes, ERP site/database/files, environment values, and hostname/access policy. It may share the EC2 temporarily only if resource and data isolation are proven.
8. Change control-plane deployment from a mutable live checkout to immutable release directories or equivalent blue/green slots.
9. Build frontend, backend, and custom-app candidate artifacts before switching the active service pointer or production app version.
10. Keep the current and previous known-good releases locally, plus the off-host source repositories and matching database/file recovery points.
11. Add pre-deploy tests and post-deploy smoke scripts for public site, login, authenticated app, backend health, ERP runtime, Frappe app list/version, and affected routes/workflows.
12. Add a deployment manifest containing control-plane commit, upstream commits, custom-app commit/version, build time, dependency lock hashes, database revisions, enabled flags, and operator.
13. Change CI so a merge to `main` builds an immutable release and deploys that exact release to staging. Production promotion of the same tested release requires a separate explicit action/approval.
14. Adopt expand/migrate/contract database changes: additive schema first, compatible code second, cleanup only in a later proven release.
15. Add feature-flag support so unfinished menu/pages/module actions can deploy disabled.
16. Add automatic failure handling: do not switch traffic on failed preflight; switch back to the previous code release on failed post-switch health.
17. Define data-operation controls: every import has a batch ID, source checksum, mapping version, counts, operator, timestamp, and reversal/correction plan.
18. Protect the origin and verify Cloudflare-to-origin TLS/access without changing DNS during the first rehearsal unless required.
19. Record `erp.lengrowth.com` as a temporary implementation hostname and inventory every hostname dependency: ERP `host_name`, nginx, TLS, cookies, CSRF/CORS, callbacks, generated links, email templates, webhooks, monitoring, backups, and external integrations.
20. Move hostname/product-name values into environment or site configuration so the final Champion domain can be tested and switched without changing application logic.
21. Create the final-domain cutover checklist, including Champion account ownership, DNS/TLS validation, old-host redirect/compatibility period, smoke tests, and rollback.
22. Record the temporary credential-rotation exception as a risk while no Champion confidential data is present. Remove plaintext secrets and rotate affected credentials before receiving or loading Champion data and before Phase 0 is marked complete.
23. Create the initial handover inventory for repositories, source history, schemas, migrations, tests, deployment/configuration templates, dependencies/licenses, infrastructure, data, documentation, and known limitations.

## Code rollback and data rollback are different

- A code rollback switches the control plane and `lenerp_core` to the previous compatible release. It does not undo database patches or imported business records.
- A full site restore returns the database and files to the backup point. It is appropriate before users resume production work or during an approved cutover rollback.
- Once users create records after an import, restoring the old backup would delete that new work. Correct the identified import batch with a tested correction/reversal script instead.
- Destructive schema cleanup is never shipped in the same release that stops using the old schema. This keeps the previous code version compatible during rollback.
- Every production release therefore records two plans: **code rollback** and **data recovery/correction**.

## Required tests

- Existing backend suite.
- Frontend typecheck and production build.
- Confirm development/staging upstream worktrees are clean and pinned to the approved SHAs.
- Install, migrate, list, and remove the initial `lenerp_core` app on a disposable site.
- Deploy candidate to staging twice to prove idempotency.
- Roll staging back to the previous release.
- Create a complete ERP site backup including database, site configuration, public files, and private files; restore it to a disposable site.
- Upgrade a restored control-plane database copy and recover it from backup.
- Simulate a failed frontend health check and confirm production pointer is not changed or is restored.
- Merge a harmless release to `main`; confirm staging deploys automatically and production does not change until explicit promotion.
- Run the candidate under a non-`lengrowth.com` test hostname and confirm authentication, routing, generated URLs, API calls, files, and background jobs do not depend on the temporary hostname.
- Confirm a secret scan contains no live credential values and the replacement credentials work before any Champion data is admitted.

## Production release

Deploy only the safety tooling and operationally neutral changes. Do not combine this release with menu redesign or schema-heavy module control.

Run the generic deployment gate. Confirm existing public and authenticated behavior is unchanged after promotion.

## Gate

Phase 0 passes when commencement and ownership are recorded; the pinned upstream clones are clean; `lenerp_core` installs independently; staging exists; `main` deploys staging rather than blindly changing production; candidate artifacts are checked before traffic; code and data recovery are proven; temporary-domain dependencies and final cutover are documented; exposed credentials are removed/rotated before Champion data; and the existing application remains healthy after the new deployment mechanism is used in production.

## Execute Phase 0 in this order

1. Record commencement, acceptance authority, ownership boundaries, temporary-domain status, and the credential exception/deadline.
2. Baseline and back up the current production systems.
3. Restore the ERP backup to a disposable/staging site and verify its files.
4. Record and clone the approved upstream commits into development/staging.
5. Create the empty `lenerp_core` custom app repository and prove clean installation.
6. Create the isolated staging lane for the control plane and ERP site.
7. Implement immutable releases, health checks, flags, rollback, and hostname-independent configuration.
8. Change `main` to automatic staging deployment plus explicit production promotion.
9. Remove/rotate exposed credentials before Champion data is admitted and close the recorded exception.
10. Promote one operationally neutral release through the complete gate.
11. Only then promote Phase 1 or Champion solution packages to production.
