# Phase 0 and Phase 1 Handover Inventory

Status: `PLAT-P0` complete; `PLAT-P1` verified; `PLAT-P2` PASS; no secret values belong here.

## Repositories and source

| Component | Repository/remotes | Current evidence |
|---|---|---|
| CRM control plane | Local `https://github.com/BuildGrowthNow/crm.git`; authoritative destination `https://github.com/Lengrowth/crm` | production current `f1d54e9af4fe620d4c565038f64f989c37e36d6f`, previous `851302efc617f8a6587b30694a5c65a3e06de20a`; protected Phase 2 promotion/readback and synthetic CRUD/isolation cleanup passed |
| Champion forecast / commercial plan | `https://github.com/guerra2fernando/champion-forecast.git` | local checkout has unrelated dirty changes; preserve them |
| Frappe upstream | `https://github.com/frappe/frappe.git` | production `edae775dd36b6c4ad7acab10230262bd74040765`; clean detached clone at `C:\Users\smikl\Desktop\Work\phase0-upstreams\frappe` |
| ERPNext upstream | `https://github.com/frappe/erpnext.git` | production `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`; clean detached clone at `C:\Users\smikl\Desktop\Work\phase0-upstreams\erpnext` |
| `lenerp_core` | Private `https://github.com/Len-OS/lenerp_core.git`; `main` at `728de29176ddb9c05c78d734318406d57f10f205` | Installed/migrated/listed/uninstalled/reinstalled on disposable EC2 ERP staging; remote now recorded |

## Runtime and ownership

- Temporary ERPNext implementation hostname: `erp.lengrowth.com`; the SaaS control plane currently uses `lenerp.lengrowth.com`; the final Champion domain is not selected.
- Hostname acceptance interpretation: Phase 1 shell validation targets `lenerp.lengrowth.com` plus the non-public `staging.example.test` lane. `erp.lengrowth.com` remains the separate Frappe/ERPNext application hostname and is not a SaaS-shell target.
- Control-plane product and service URLs must come from environment/site configuration.
- AWS EC2 and Cloudflare zone are verified; the temporary application hostnames are proxied through Cloudflare to the EC2 origin. Canonical public API `lenerp-api.lengrowth.com` resolves through Cloudflare and `/health` returned HTTP `200` on 2026-09-15 and again after retirement verification on 2026-09-16. The old deep hostname `api.lenerp.lengrowth.com` is retired, must not be used, and its old DNS record was deleted from Cloudflare on 2026-09-16.
- Final non-secret production readback artifact from workflow `35108238557` reports Frappe and ERPNext source trees clean at the recorded production heads; no upstream source was changed by this run.
- Reproducible staging-lane contract: `ops/staging/`; control-plane and ERP staging host/service/database/file evidence is established on the EC2 with private host-header checks.
- `PLAT-P2` production serves exact candidate `f1d54e9af4fe620d4c565038f64f989c37e36d6f`; its shell flag is on, the previous Phase 1 candidate is `851302efc617f8a6587b30694a5c65a3e06de20a`, and the older `12bc548…` rollback remains available through protected release pointers.
- Exact-candidate enabled-shell browser/WCAG evidence is run [35237762341](https://github.com/Lengrowth/crm/actions/runs/35237762341) with artifact [10503792511](https://github.com/Lengrowth/crm/actions/runs/35237762341/artifacts/10503792511); its operator-validation identity is synthetic and uses a disposable authenticated platform-admin fixture. Protected production promotion/readback is run [35234505403](https://github.com/Lengrowth/crm/actions/runs/35234505403) with artifact [10502656299](https://github.com/Lengrowth/crm/actions/runs/35234505403/artifacts/10502656299). The prior `12bc548…` candidate remains the previous pointer.
- Live hostname reconciliation on 2026-09-17 confirmed `erp.lengrowth.com` serves the Frappe login surface and redirects `/app` to Frappe `/login`, while `lenerp.lengrowth.com` serves the SaaS surface and redirects unauthenticated `/app` to the SaaS `/login`; `lenerp-api.lengrowth.com/health` returned HTTP 200. This explicitly resolves the Phase 1 wording ambiguity without rerouting the ERP hostname.
- Exact-current-candidate flag-only fallback is proven by off run [35238093438](https://github.com/Lengrowth/crm/actions/runs/35238093438) / artifact [10503643197](https://github.com/Lengrowth/crm/actions/runs/35238093438/artifacts/10503643197), followed by restore-on run [35238216926](https://github.com/Lengrowth/crm/actions/runs/35238216926) / artifact [10504491369](https://github.com/Lengrowth/crm/actions/runs/35238216926/artifacts/10504491369); both preserved the current and previous release pointers.
- The final Phase 2 production readback artifact is [10509816751](https://github.com/Lengrowth/crm/actions/runs/35252397846/artifacts/10509816751) from run [35252397846](https://github.com/Lengrowth/crm/actions/runs/35252397846). It reports current `f1d54e9…`, previous `851302ef…`, local health `200`, active backend/frontend/nginx/R2 timer services, enabled R2 lifecycle rules, 17 R2 objects, shell flag `true`, clean Frappe/ERPNext heads, and zero temporary smoke users, organizations, or sessions. The authorized Phase 2 smoke passed create/read/update and tenant-isolation denial; exact dependent records were cleaned. Public SaaS root, canonical API health, and runtime release observations each returned `200` with release and commit identity `f1d54e9…`.

## Release artifacts

- Immutable candidate builder: `scripts/release/build_candidate.sh`.
- Non-secret release manifest builder: `scripts/release/build_manifest.py`.
- Staging deployment: `scripts/deploy/deploy_saas_control.sh`.
- Explicit production promotion: `scripts/deploy/promote_saas_control.sh`.
- Preflight and smoke checks: `scripts/release/preflight.sh`, `scripts/release/smoke.sh`.
- Upstream source guard: `scripts/release/verify_upstream_clean.sh`.
- Secret scan: `scripts/release/secret_scan.py`.
- Phase 1 shell smoke: `scripts/release/shell_smoke.sh`.

## Data and recovery

- Site database, site configuration, public files, private files, and control-plane database must never be committed.
- Backup destination is Cloudflare R2 bucket `lenerp-phase0-backups`; ERP/control-plane artifacts were uploaded and byte-hash verified. Final production readback from workflow `35108238557` independently queried 11 objects and confirmed the enabled seven-day incomplete-multipart abort rule plus enabled 90-day lifecycle rules for `erp/` and `control-plane/`. Scheduled automation is enabled on production, and the first automated run on 2026-09-16 uploaded and verified six objects under `automated/production/20260916T083532Z/`. Pedro (`pedrocdiegues@gmail.com`) is recorded as the second independent restore operator.
- The ERP SQL dump restored into disposable MariaDB schema `plat_p0_restore_20260915` with 707 tables; the temporary schema was removed after verification.
- The disposable ERP staging site is `erp-staging.example.test` under `/opt/frappe-staging-bench`; control-plane staging is under `/opt/saas-control-staging`. Their databases, files, Redis ports, services, and workers are separate from production.
- No Champion confidential data may be received, restored, copied, or imported before credential rotation and plaintext-secret resolution are complete.

## Next-phase baseline

- Phase 2 production now serves exact candidate `f1d54e9af4fe620d4c565038f64f989c37e36d6f` with previous candidate `851302efc617f8a6587b30694a5c65a3e06de20a`, the operator shell enabled, and the older rollback pointer `12bc548…` retained. The runtime manifest may continue to report `environment: staging` because the immutable artifact is staging-built and promoted unchanged.
- The next release must continue to use staging-first immutable candidates and the protected production workflow; no Phase 2 page redesign or Champion data import is implied by this handover.

## Phase 2 baseline

- Phase 2 implementation is isolated on branch `codex/plat-p2` from verified
  remote `main` `edb3f463ed50e1009a13e8e96b95b563ddc6f6b9`.
- The release adds reusable operator primitives and bounded protected read
  models at `/dashboard/summary` and `/implementation/portfolio`; no database
  revision or production Frappe/ERPNext change is required.
- Local validation is recorded in `releases/PLAT-P2.md`; exact candidate
  `f1d54e9…` passed protected staging, main, production promotion, observation,
  CRUD/isolation cleanup, and readback. The release record contains the full
  evidence and accepted limitations.
