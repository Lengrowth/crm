# PLAT-P0 — Phase 0 Release Record

Status: **CONDITIONAL PASS — repository safety foundation implemented; operational gate remains open**  
Release identity: `PLAT-P0`  
Record date: 2026-09-15  
Operator: Codex, working with the delivery owner  
Approver: Not recorded  
Production promotion: **Not performed**

## Scope and safety decision

This release contains operationally neutral control-plane safety tooling only. It does not begin Phase 1 UI work, Champion workflows, module configuration, or Champion data migration.

Credential rotation is explicitly deferred by the owner for this run. No credential was rotated or invalidated. The existing credential-bearing operator reference was sanitized so values are no longer stored in ordinary documentation. Rotation, secret-store migration, history scanning, MFA/access review, and verification of replacement credentials remain mandatory before any Champion confidential data is received, restored, copied, or imported.

## Verified source baseline

| Item | Evidence | Result |
|---|---|---|
| CRM repository | Local `origin` is `https://github.com/BuildGrowthNow/crm.git`; requested GitHub destination is `https://github.com/Lengrowth/crm`; verified handover candidate `265a9047bb7b4d4cc034be3501b61c0f314cf83f` | Recorded; destination alignment remains a repository-ownership action |
| Previous CRM source tip | `bab5568...` in local history | Recorded as source history only; not claimed as a production rollback target |
| Champion forecast repository | `https://github.com/guerra2fernando/champion-forecast.git`; local branch is ahead of its remote and contains unrelated dirty changes | Read-only inventory only; preserved |
| Frappe/ERPNext production revisions | Frappe `edae775dd36b6c4ad7acab10230262bd74040765`, ERPNext `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`; both `version-15` | Recorded; both production trees have preserved tracked/untracked drift |
| Installed apps and versions | Bench `5.31.0`; site `erp.lengrowth.com`; Frappe `15.119.1`, ERPNext `15.120.0` | Recorded |
| Production runtime | EC2 nginx, MariaDB `10.6.23`, Redis, Supervisor, Frappe workers, SaaS backend/frontend, GitHub Actions runner; env files under `/opt/saas-control/shared/env/` | Recorded without values |
| Production routes and services | `lenerp.lengrowth.com` → Next.js `3000`; `api.lenerp.lengrowth.com` → backend `8001`; `erp.lengrowth.com` and `*.erp.lengrowth.com` → Frappe `8000/9000`; site files under `/home/frappe/frappe-bench/sites/erp.lengrowth.com` | Recorded; public API TLS is an open Cloudflare edge issue |
| Agreement/payment/commencement | Not present in the accessible repository evidence | **Open decision item** |
| Delivery owner | Complete delivery plan identifies Fernando Guerra | Recorded from plan |
| Acceptance authority | Complete delivery plan identifies Champion Well Drilling / Matt or written replacement in Project Start | Recorded from plan; approval not evidenced |

## Implemented repository changes

- Added safe runtime release metadata at `GET /runtime/release`, including release identity, environment, non-secret manifest fields, and server-controlled feature flags.
- Added a manifest builder that records commits, dependency lock hashes, build time, database revision fields, app version fields, installed-app identities, and flags without secret values.
- Added immutable candidate build and preflight scripts. A completed candidate is marked only after the frontend production build succeeds.
- Candidate builds can package a clean pinned `lenerp_core` repository and preflight verifies the custom-app artifact when declared.
- Replaced the main deploy path with staging-only immutable release switching. It keeps `current` and `previous` pointers and restores the prior pointer after a failed smoke test.
- Added a separately invoked production promotion script that requires an explicit approval environment variable and an exact per-candidate successful staging-smoke marker.
- Made the protected production workflow require explicit application/site-backup and off-host-copy confirmations before invoking promotion; the script still rejects any non-`yes` value.
- Added upstream Frappe/ERPNext cleanliness and fail-closed pin checks; missing approved SHAs now fail verification.
- Added a high-confidence secret scan that reports only file paths and never matching content.
- Changed CI so `main` builds/deploys staging; production promotion is a separate manual workflow with a protected production environment.
- Removed credential values from `CLAUDE.md` and replaced them with secret-store handling instructions. This is sanitization, not rotation.
- Generated the non-secret release manifest at `PLAT-P0-manifest.json` from the current source baseline.
- Added the isolated staging-lane contract, non-secret environment/nginx templates, and dedicated ERP staging systemd/Redis units under `ops/staging/`.
- Provisioned the EC2 staging lane at `/opt/saas-control-staging` and `/opt/frappe-staging-bench` with separate control-plane/ERP databases, files, ports, services, queues, workers, and the `staging.example.test` / `erp-staging.example.test` host-header policy.

## Production as-built evidence

- Read-only SSH inventory completed against the EC2 after the temporary port-22 allow rule was opened. The ERP and control plane are co-hosted on the same EC2, as the nginx routes, Supervisor groups, listeners, systemd units, and application directories show.
- The Frappe and ERPNext worktrees are not clean: Frappe has tracked UI/template changes plus untracked backup files; ERPNext has tracked UI/template changes plus untracked `.bak` files. No upstream file was changed by this Phase 0 run.
- The production app worktrees have no configured `origin` remote. Clean, detached local clones of the exact production SHAs were created outside the CRM checkout at `C:\Users\smikl\Desktop\Work\phase0-upstreams\frappe` and `C:\Users\smikl\Desktop\Work\phase0-upstreams\erpnext`; both report clean status.
- Cloudflare DNS is active and proxied for the three temporary hostnames. `lenerp` and `erp` return successfully through the edge. `api.lenerp.lengrowth.com` fails TLS at the Cloudflare edge while the EC2 backend is healthy locally; the connected Wrangler identity lacks the zone DNS/SSL permissions required to correct that setting.

## Tests and evidence

The exact commands and results are maintained below:

- Secret scan: **PASS** — `python scripts/release/secret_scan.py` reported no high-confidence credential patterns and printed no matching content.
- Shell syntax: **PASS** — Git Bash `bash -n` passed for every `scripts/**/*.sh` file. WSL was unavailable, so the check used the installed Git Bash runtime.
- Manifest builder: **PASS** — generated a non-secret manifest with commit, environment, build time, dependency hashes, and feature flags.
- Python compilation: **PASS** — `python -m compileall -q backend/app backend/tests scripts/release scripts/deploy`.
- Frontend typecheck: **PASS** — `npm --prefix frontend run typecheck`.
- Frontend production build: **PASS** — `npm --prefix frontend run build`; Next.js generated 32 static pages and the documented routes.
- New runtime release test: **PASS** — `backend/.venv/Scripts/python.exe -m pytest backend/tests/test_release_metadata.py -q` (1 passed).
- Workflow YAML, manifest JSON, Python compilation (CRM and `lenerp_core`), documentation-link validation, and `git diff --check`: **PASS**.
- Upstream pin guard: **PASS** — a clean pinned test tree was accepted and a missing expected SHA was rejected before verification could pass.
- Disposable local runtime smoke: **PASS** — `backend/.venv/Scripts/python.exe scripts/release/local_smoke.py`; temporary SQLite migrations ran, public root/backend health/ERP runtime/release identity/installed-app inventory passed with `Host: staging.example.test`, the reusable shell smoke authenticated-check path passed via a temporary token file, synthetic register/login/authenticated organization access and unauthenticated denial passed, synthetic tenant provisioning/worker route passed, and the temporary database/processes/token/manifest files were cleaned up.
- Disposable immutable-slot rehearsal: **PASS** — `backend/.venv/Scripts/python.exe scripts/release/rehearse_slots.py`; proved idempotency, exact staging-smoke evidence, preflight rejection, failed-health rollback, first-deploy safety with no known-good pointer, manual rollback, and production-pointer isolation. The rehearsal also led to preserving the prior `previous` pointer across failed candidates.
- Disposable control-plane backup/restore rehearsal: **PASS** — `backend/.venv/Scripts/python.exe scripts/release/rehearse_backup_restore.py --self-test`; a restored control-plane database was upgraded from the first migration to head, its synthetic record was preserved, and site configuration, public files, and private files were restored and verified.
- Full backend suite: **PASS** — `backend/.venv/Scripts/python.exe -m pytest backend/tests -q`; 36 passed. The integration test now uses a disposable authenticated tenant/database, and provisioning retry/idempotency paths pass.
- `git diff --check`: **PASS** after removing the reported trailing whitespace.
- Production baseline: **CONDITIONAL** — public control-plane root `200`, login `200`, ERP root `200`, and unauthenticated ERP API denial `403`; local origin backend and Frappe routes returned `200`, and Supervisor workers were active. The public API hostname failed TLS at the Cloudflare edge, so authenticated/API observation is not complete.
- Actual control-plane staging CI: **PASS** — GitHub Actions runs `34968621678` and `34968811226` proved authenticated deployment/idempotency for the earlier candidate; handover candidate `265a9047bb7b4d4cc034be3501b61c0f314cf83f` passed in run `34971552445`. The verified post-run current/previous pointers were `265a9047bb7b4d4cc034be3501b61c0f314cf83f` / `b6e96b628513e7033949d711fd845f5a4fe4125b`.
- Actual ERP staging: **PASS for the disposable lane** — `/opt/frappe-staging-bench`, site `erp-staging.example.test`, Frappe `15.119.1` at `edae775dd36b6c4ad7acab10230262bd74040765`, ERPNext `15.120.0` at `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`, `lenerp_core` installed; web/login/API, dedicated Redis ports `14100/14101`, web port `28000`, workers, scheduler, and install/uninstall/reinstall cycle passed via `scripts/release/erp_staging_smoke.sh`.

## Backup and recovery evidence

Production backups are now evidenced for the pre-Champion system. A fresh `bench --site erp.lengrowth.com backup --with-files` completed on 2026-09-15 and produced the ERP database, site-config backup, public-files archive, and private-files archive. The control-plane SQLite database was also copied without exposing its contents. All five artifacts were streamed to the private Cloudflare R2 bucket `lenerp-phase0-backups` under `erp/2026-09-15/erp.lengrowth.com/` and `control-plane/2026-09-15/`; each R2 stream hash matched the EC2 source hash byte-for-byte.

The R2 copy was restored outside production: gzip integrity and JSON validation passed, public/private archives extracted, and the SQL dump imported into a new disposable MariaDB schema with 707 tables. The temporary schema and recovery directory were removed after verification. R2 retention policy, backup automation credentials, named owner, and a second independent restore operator still need to be assigned; no Champion data is covered by this evidence.

Code rollback and data recovery remain separate: the release scripts switch immutable code pointers; database/files restoration must be completed and evidenced independently before promotion.

## Release identifiers

- Current CRM handover source identifier: `265a9047bb7b4d4cc034be3501b61c0f314cf83f`.
- Previous CRM source identifier in local history: `bab5568...`; exact full SHA must be recorded from the final candidate manifest before use as a rollback target.
- Current production control-plane source identifier: `1c3ea4d570e08443a8100acb1ecdf506c30a4ca5` in `/opt/saas-control/repo`; production Alembic revision is `20260528_0007`; the host has no immutable `current`/`previous` release pointers.
- Current production ERP source identifiers: Frappe `edae775dd36b6c4ad7acab10230262bd74040765`; ERPNext `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`.
- Previous production release identifier: **not recorded**; there is no prior immutable release target to use for rollback.
- `lenerp_core` local scaffold commit: `728de29`; install/migrate/list/uninstall/reinstall proof passed on the disposable staging site. Remote private-repository ownership is still not evidenced.
- Current staging control-plane release: `265a9047bb7b4d4cc034be3501b61c0f314cf83f`; previous staging release: `b6e96b628513e7033949d711fd845f5a4fe4125b`.

## Gate status

The Phase 0 gate is **not fully passed**. The repository-side safety foundation and production backup/off-host-copy evidence are now present, but mandatory operational evidence remains unresolved:

1. Establish an immutable production release pointer and record a previous known-good code release.
2. Assign R2 backup retention, automation credential ownership, and a second restore operator.
3. Resolve the preserved production Frappe/ERPNext worktree drift and publish `lenerp_core` to the approved private repository without deleting that drift.
4. Complete a staging rollback and failed-health simulation on the live EC2 lane; the two exact-candidate deployments and ERP smoke are already evidenced.
5. Correct the Cloudflare edge TLS configuration for `api.lenerp.lengrowth.com` with a user/session that has the required zone DNS/SSL permissions.
6. Credential rotation and plaintext-secret resolution before Champion data; explicitly deferred, therefore a mandatory pre-data blocker.
7. Record agreement/commencement/ownership records and a named approver.

## Phase 0 checklist status

| # | Requirement | Status | Evidence or blocker |
|---:|---|---|---|
| 1 | Read the Phase 0 source documents and repository instructions | PASS | Source pack and `CLAUDE.md` reviewed for this release. |
| 2 | Preserve the existing Git state and unrelated work | PASS | Dirty worktree preserved; no reset, clean, or destructive checkout was used. |
| 3 | Establish release identity `PLAT-P0` | PASS | This release record and non-secret manifest exist. |
| 4 | Record baseline, ownership, repositories, revisions, services, routes, sites, and backups | CONDITIONAL | EC2/Frappe/control-plane runtime is recorded; repository ownership, approver, and Cloudflare edge TLS ownership remain open. |
| 5 | Verify public, login, authenticated, API, ERP runtime, and worker baseline | CONDITIONAL | Disposable local staging-style smoke passed; production baseline and observation remain unverified. |
| 6 | Create complete ERP/control-plane backups | CONDITIONAL PASS | Fresh ERP database/site-config/public/private backups and control-plane SQLite backup exist; long-term retention/automation ownership is open. |
| 7 | Verify authorized off-host backup copy | CONDITIONAL PASS | Five R2 objects in `lenerp-phase0-backups` match EC2 source hashes; bucket retention/owner is not yet recorded. |
| 8 | Restore backups outside production | PASS for evidence scope | ERP SQL imported into disposable MariaDB schema with 707 tables; files/config restored and validated; temporary targets removed. |
| 9 | Confirm clean, pinned Frappe and ERPNext clones | CONDITIONAL | Exact production SHAs are known and clean detached clones exist locally; production worktrees remain dirty and lack remotes. |
| 10 | Establish and independently install/migrate/list/uninstall `lenerp_core` | PASS for disposable staging | Local scaffold commit `728de29`; install, migrate, list, uninstall, reinstall, and final list passed on `erp-staging.example.test`. Remote private repository ownership remains open. |
| 11 | Fail on tracked upstream modifications | PASS | `scripts/release/verify_upstream_clean.sh` and manual CI workflow added. |
| 12 | Create isolated staging lane | PASS for staging | EC2 evidence shows separate control-plane and ERP paths, databases, files, ports, Redis instances, services/workers, and non-production host-header policy. |
| 13 | Implement immutable release directories/slots | PASS | Candidate builder, current/previous pointers, and slot rehearsal are implemented and tested. |
| 14 | Build frontend/backend/custom-app artifacts before switching traffic | PASS | Candidate builder and preflight enforce this ordering; exact host execution remains pending. |
| 15 | Keep current/previous exact release identifiers | CONDITIONAL | Slot rehearsal proves pointer behavior; production has a known source tip but no immutable current/previous pointers. |
| 16 | Add preflight and post-deploy smoke coverage | PASS for staging; CONDITIONAL for production | Control-plane authenticated smoke and ERP staging smoke pass; production API edge TLS still prevents complete public API observation. |
| 17 | Add non-secret release manifest | PASS | Manifest contains commits, versions, build time, hashes, revisions, flags, environment, and operator. |
| 18 | Add server-controlled feature flags | PASS | Settings-backed flag map and runtime metadata are implemented and tested. |
| 19 | Make deployment/provisioning idempotent | PASS | Provisioning retry/idempotency tests and immutable-slot idempotency rehearsal pass. |
| 20 | Prevent failed candidates from receiving traffic and restore after failed health | PASS | Preflight gate, atomic pointers, failed-health rollback, first-deploy pointer removal, and pointer-isolation rehearsal pass. |
| 21 | Configure staging CI and separate explicit production promotion | PASS for staging path | Exact-candidate CI runs `34968621678` and `34968811226` passed; production promotion remains a separate explicit workflow. |
| 22 | Make hostnames/configuration independent and document final-domain cutover | PASS | Environment-driven URLs/cookies/provider endpoint and domain cutover checklist added; external validation remains open. |
| 23 | Test a non-`lengrowth.com` staging hostname | PASS | `staging.example.test` and `erp-staging.example.test` host-header smoke passed without DNS changes. |
| 24 | Deploy only operationally neutral Phase 0 changes | CONDITIONAL | Repository changes are safety/configuration tooling only; production promotion was deliberately not performed. |
| 25 | Run production smoke and observation window | CONDITIONAL | Public/unauthenticated and local-origin checks passed, but API edge TLS and authenticated observation remain unresolved. |
| 26 | Update release, blocker/risk, handover, deployment/rollback, and checklist records | PASS | Release record, registers, handover inventory, rollback tooling, and this checklist are updated; actual production evidence remains open. |

## Rollback instructions

For staging, stop promotion if preflight fails. If post-switch smoke fails, `deploy_saas_control.sh` restores the previous immutable `current` pointer and restarts the configured services. For production, use `promote_saas_control.sh` only with an existing tested staging candidate, verified application/site and off-host backups, and explicit approval; a failed smoke restores the previous pointer. Database/files recovery is a separate approved restore procedure and is not implied by code rollback.

## Recommended review focus

Review the staging host paths and service units against the scripts, verify that the protected production environment is configured, then complete the production as-built/backup/restore evidence. Confirm the credential exception deadline and secret-store owner before any Champion data handling.
