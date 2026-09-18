# Phase 0 and Phase 1 Handover Inventory

Status: `PLAT-P0` complete; `PLAT-P1` verified; `PLAT-P2` PASS; `PLAT-P3` PASS; no secret values belong here.

## Repositories and source

| Component | Repository/remotes | Current evidence |
|---|---|---|
| CRM control plane | Local `https://github.com/BuildGrowthNow/crm.git`; authoritative destination `https://github.com/Lengrowth/crm` | production current `86fcde5b822b06e40980f904d81b87854903dfc6`, previous `68926c22aab01079f17c2cebe21edeeff8ca2c75`; protected Phase 3 remediation promotion, rollout, synthetic verification/reversal, observation, and complete cleanup passed; Phase 1 shell is restored on |
| Champion forecast / commercial plan | `https://github.com/guerra2fernando/champion-forecast.git` | local checkout has unrelated dirty changes; preserve them |
| Frappe upstream | `https://github.com/frappe/frappe.git` | production `edae775dd36b6c4ad7acab10230262bd74040765`; clean detached clone at `C:\Users\smikl\Desktop\Work\phase0-upstreams\frappe` |
| ERPNext upstream | `https://github.com/frappe/erpnext.git` | production `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`; clean detached clone at `C:\Users\smikl\Desktop\Work\phase0-upstreams\erpnext` |
| `lenerp_core` | Private `https://github.com/Len-OS/lenerp_core.git`; synthetic demo branch `codex/champ-c01-r1` at `01c8199` (`0.2.0`) | C01–C08 synthetic DocTypes, roles, workflow, reports, print path, seed/status/reset; isolated ERP staging installation remains candidate-bound |

## Runtime and ownership

- Temporary ERPNext implementation hostname: `erp.lengrowth.com`; the SaaS control plane currently uses `lenerp.lengrowth.com`; the final Champion domain is not selected.
- Hostname acceptance interpretation: Phase 1 shell validation targets `lenerp.lengrowth.com` plus the non-public `staging.example.test` lane. `erp.lengrowth.com` remains the separate Frappe/ERPNext application hostname and is not a SaaS-shell target.
- Control-plane product and service URLs must come from environment/site configuration.
- AWS EC2 and Cloudflare zone are verified; the temporary application hostnames are proxied through Cloudflare to the EC2 origin. Canonical public API `lenerp-api.lengrowth.com` resolves through Cloudflare and `/health` returned HTTP `200` on 2026-09-15 and again after retirement verification on 2026-09-16. The old deep hostname `api.lenerp.lengrowth.com` is retired, must not be used, and its old DNS record was deleted from Cloudflare on 2026-09-16.
- Final non-secret production readback artifact from workflow `35108238557` reports Frappe and ERPNext source trees clean at the recorded production heads; no upstream source was changed by this run.
- Reproducible staging-lane contract: `ops/staging/`; control-plane and ERP staging host/service/database/file evidence is established on the EC2 with private host-header checks.
- The preceding `PLAT-P2` release served exact candidate `41ac76500a6a502ac78f22d6dbefbf90996ee46a`; its shell flag was on, the previous candidate was `f1d54e9af4fe620d4c565038f64f989c37e36d6f`, and older rollback pointers `851302ef…` / `12bc548…` remain available through protected release pointers.
- Final remediated candidate browser/WCAG evidence is PR run [35257247863](https://github.com/Lengrowth/crm/actions/runs/35257247863), artifact [10512978308](https://github.com/Lengrowth/crm/actions/runs/35257247863/artifacts/10512978308), and post-merge main run [35257785806](https://github.com/Lengrowth/crm/actions/runs/35257785806), artifact [10513394070](https://github.com/Lengrowth/crm/actions/runs/35257785806/artifacts/10513394070). The artifacts record UI CRUD/validation, cross-company mutation denial, responsive/theme/accessibility evidence, and exact cleanup for candidate `41ac765…`. The prior `12bc548…` candidate remains available through protected release pointers.
- Live hostname reconciliation on 2026-09-17 confirmed `erp.lengrowth.com` serves the Frappe login surface and redirects `/app` to Frappe `/login`, while `lenerp.lengrowth.com` serves the SaaS surface and redirects unauthenticated `/app` to the SaaS `/login`; `lenerp-api.lengrowth.com/health` returned HTTP 200. This explicitly resolves the Phase 1 wording ambiguity without rerouting the ERP hostname.
- Exact-current-candidate flag-only fallback is proven by off run [35238093438](https://github.com/Lengrowth/crm/actions/runs/35238093438) / artifact [10503643197](https://github.com/Lengrowth/crm/actions/runs/35238093438/artifacts/10503643197), followed by restore-on run [35238216926](https://github.com/Lengrowth/crm/actions/runs/35238216926) / artifact [10504491369](https://github.com/Lengrowth/crm/actions/runs/35238216926/artifacts/10504491369); both preserved the current and previous release pointers.
- The final Phase 2 production readback artifact is [10513034032](https://github.com/Lengrowth/crm/actions/runs/35258252240/artifacts/10513034032) from run [35258252240](https://github.com/Lengrowth/crm/actions/runs/35258252240). It reports current `41ac765…`, previous `f1d54e9…`, local health `200`, active backend/frontend/nginx/R2 timer services, enabled R2 lifecycle rules, 17 R2 objects, shell flag `true`, clean Frappe/ERPNext heads, and zero temporary smoke users, organizations, or sessions. The authorized Phase 2 smoke passed create/read/update, tenant-isolation read/mutation denial, and exact dependent-record cleanup; the Phase 2 manifest reports zero remaining records for every created class. Runtime release observations returned `200` with release and commit identity `41ac765…`.
- Phase 3 candidate-bound staging run [35278665942](https://github.com/Lengrowth/crm/actions/runs/35278665942) produced browser artifact [10521149490](https://github.com/Lengrowth/crm/actions/runs/35278665942/artifacts/10521149490) for exact candidate `86fcde5b…`. The actual final remote-main staging run is [35281045275](https://github.com/Lengrowth/crm/actions/runs/35281045275), artifact [10522837696](https://github.com/Lengrowth/crm/actions/runs/35281045275/artifacts/10522837696), testing head `6bb59b2…`. That staging artifact reports `platform_phase1_shell=false` by environment; protected production promotion/readback [35279102175](https://github.com/Lengrowth/crm/actions/runs/35279102175) with artifact [10522240159](https://github.com/Lengrowth/crm/actions/runs/35279102175/artifacts/10522240159) reports the production candidate `86fcde5b…`, `platform_phase1_shell=true`, active services, local health `200`, and clean upstream trees.
- Phase 3 remediation rollout evidence is complete: read-only run [35279338775](https://github.com/Lengrowth/crm/actions/runs/35279338775), operator-only synthetic verification run [35279271616](https://github.com/Lengrowth/crm/actions/runs/35279271616) / artifact [10522300063](https://github.com/Lengrowth/crm/actions/runs/35279271616/artifacts/10522300063), and general rollout run [35279384713](https://github.com/Lengrowth/crm/actions/runs/35279384713). Operator evidence reports zero synthetic cleanup counts for every created record class and token files, successful reversal, and no ERP verification without trusted evidence. Final live observation returned health `200`, Phase 1 shell `true`, and stable `writes=true`, `operator_only=false`, `general=true`.

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

- Phase 2 is the preceding release baseline: it served exact candidate `41ac76500a6a502ac78f22d6dbefbf90996ee46a` with previous candidate `f1d54e9af4fe620d4c565038f64f989c37e36d6f`; the current PLAT-P3 candidate and previous pointer are recorded above. The runtime manifest may continue to report `environment: staging` because immutable artifacts are staging-built and promoted unchanged.
- The next release must continue to use staging-first immutable candidates and the protected production workflow; no Phase 2 page redesign or Champion data import is implied by this handover.

## Phase 4 baseline

- `PLAT-P3` is PASS on exact production candidate `86fcde5b…`; the persisted
  module catalog, versioned bundle control, deterministic entitlement resolver,
  organization audit/reversal path, and server-controlled general authorized-role
  rollout are available to Phase 4 onboarding work.
- Public module selections remain onboarding requests only. Phase 4 must keep
  operator approval, durable idempotent provisioning, ERP application/verification
  evidence, and tenant/domain isolation separate from entitlement selection.
- C03 remains `defined` and synthetic-only; no Champion data, final domain, or
  unresolved role/module decision is carried forward as accepted.

## Phase 4 implementation status

- The local PLAT-P4 implementation is on `codex/plat-p4` from authoritative
  `lengrowth/main` `2a697a831d04a41aaabb3e6f2413f53ce4e749c6`; the candidate is
  not yet committed or materialized as an immutable release.
- Migration `20260918_0010` adds versioned onboarding requests, management
  credential hashes, operator decisions, durable provisioning steps/events/
  outbox, first-login handoff state, and job lease/retry metadata.
- Public intake, operator review/approval/conversion, synthetic-only execution,
  exact cleanup, and the retired direct-provisioning guard pass the local
  validation suite. `frontend/tsconfig.tsbuildinfo` remains an expected local
  change and must be preserved.
- Staging has a guarded workflow input and
  `scripts/release/phase4_synthetic_smoke.py`; no immutable-candidate staging
  artifact or protected production Phase 4 evidence exists yet. Do not claim
  PLAT-P4 PASS or enable Phase 4 flags in production until those artifacts are
  reconciled.

## Phase 2 baseline

- Phase 2 implementation is isolated on branch `codex/plat-p2` from verified
  remote `main` `edb3f463ed50e1009a13e8e96b95b563ddc6f6b9`.
- The release adds reusable operator primitives and bounded protected read
  models at `/dashboard/summary` and `/implementation/portfolio`; no database
  revision or production Frappe/ERPNext change is required.
- Local validation is recorded in `releases/PLAT-P2.md`; exact candidate
  `41ac765…` passed protected staging, main, production promotion, observation,
  UI/API CRUD, mutation isolation, Phase 2 cleanup, and readback. The release
  record contains the full evidence and accepted limitations.
