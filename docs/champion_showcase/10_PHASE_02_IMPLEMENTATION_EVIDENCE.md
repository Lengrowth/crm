# Phase 02 — Implementation Evidence

**Date:** 2026-09-20
**Status:** Corrected implementation committed locally; exact staging candidate is pending the protected staging run. Production remains unchanged until that run passes.
**Release scope:** dependency-aware HRMS provisioning for synthetic Champion tenants only.

## Evidence boundary

This record does not claim Champion acceptance, real employee/payroll data,
production HRMS installation, or Phase 03 work. Production HR/Payroll
navigation remains disabled until exact application, role, workspace, and site
readback succeeds.

## HRMS pin and compatibility

| Field | Recorded value |
|---|---|
| Repository | `https://github.com/frappe/hrms.git` |
| Tag | `v15.64.1` |
| Exact commit | `e68a3deaa95ae5b2c3d743297d0a4ab505733fc1` |
| Version | `15.64.1` |
| License | GNU General Public License (v3) |
| Frappe compatibility | `>=15.0.0,<16.0.0` |
| ERPNext compatibility | `>=15.0.0,<16.0.0` |
| Reviewed baseline | Frappe `15.119.1`, ERPNext `15.120.0` |
| Source authority | Official upstream `pyproject.toml`, `__init__.py`, `hooks.py`, `setup.py`, tag readback, and [HRMS issue #1639](https://github.com/frappe/hrms/issues/1639) |
| Artifact checksum | Not packaged in this repository; immutable commit/tag is the release identity |

The exact dependency record is [application-dependencies.json](../../ops/staging/application-dependencies.json). The broad
`>=15,<16` metadata is not treated as an installation guarantee: the pinned
ERPNext baseline removed the legacy Frappe HR module path, while official
HRMS v15.64.1 still calls its own `Expense Claim Type` fixture from
`after_install`. Issue #1639 records the same traceback and the supported
operator recovery is a bounded uninstall/clear-cache/reinstall replay on the
isolated synthetic site. No upstream source or fixture is patched.

## Implementation

- `calculate_required_applications` deduplicates effective module requirements,
  keeps platform applications separate, rejects unpinned applications and
  conflicting pins, and returns stable install order: Frappe, ERPNext, HRMS,
  `lenerp_core`.
- Effective modules without HR or Payroll do not include HRMS. HR or Payroll
  metadata requires HRMS; Payroll also retains its HR, Accounting, and other
  dependency closure.
- The durable onboarding workflow adds an `install_pinned_hrms` step only when
  the effective application plan requires HRMS. The step is idempotent and
  rechecks exact installed-app readback after installation.
- The provisioning sequence now performs provider-confirmed migration before
  module configuration, then roles/workspaces, health, and installed-app/module
  verification. A provider/network failure cannot become success.
- HR/Payroll status rows are created only after metadata validation and remain
  pending/hidden/needs-attention when HRMS is missing or incompatible. Verified
  requires installed-app, module, role, and workspace readback.
- The operator UI presents `Installing People & Payroll capability` with
  expandable technical detail; exact step names remain operator-only detail.
- The staging install workflow and provider adapter perform at most one
  HRMS-specific recovery replay after this known upstream fixture failure;
  success still requires exact installed-app, commit, migration, role and
  workspace readback.

## Local validation

| Check | Result |
|---|---|
| Focused Phase 02 tests | PASS — 5 tests |
| Existing Phase 01/Phase 4/provider tests | PASS — 13 tests |
| Complete backend suite | PASS — 68 tests |
| Python compile/import | PASS — `python -m compileall -q backend/app` |
| Frontend tests | PASS — 12 tests |
| Frontend typecheck/build | PASS — `npm --prefix frontend run typecheck` and `npm --prefix frontend run build` |
| Staging/release package tests | PASS — 9 tests |
| Migration rehearsal | Existing Phase 01 rehearsal retained; Phase 02 additive migration has no new schema revision |
| Secret scan | PASS — no high-confidence credential patterns |
| Markdown links | No dedicated repository validator present; relative links in changed docs reviewed |
| `git diff --check` | PASS on the reviewed candidate |

## Infrastructure diagnosis and recovery

| Port | Intended purpose | Root cause of direct reachability failure | Final boundary | Health |
|---|---|---|---|---|
| `18001` | Staging control-plane backend | Intentional loopback bind and no public staging listener | `127.0.0.1`; host-header/private staging lane only | Healthy locally on EC2; `/health` returned `200` |
| `13001` | Staging control-plane frontend | Intentional loopback bind and no public staging listener | `127.0.0.1`; host-header/private staging lane only | Healthy locally on EC2; root returned `200` |
| `28000` | Staging Frappe web | Intentional loopback bind and no public staging listener | `127.0.0.1`; host-header/private staging lane only | Service/listener healthy; unauthenticated method returned expected `404` for the checked endpoint |

AWS account/region readback: account `288947333598`, region `us-east-1`, EC2
`i-0f54fba441caa7154`, security group `sg-0387e9287e4817700`. Ingress is
limited to Cloudflare IP ranges on 80/443 and the approved SSH `/32`; no raw
staging-port ingress was added. The temporary inspection SSH rule for
`212.58.102.127/32` was revoked after readback.

EC2 readback showed all staging and production control-plane/Frappe services
active, loopback listeners present, Nginx serving production HTTPS routes, and
staging pointers `current -> 802f1bdb0f7642ea627b08235dfa3aa16e7b9eda` and
`previous -> a930f2d2e0aea900b130ca970f7ed785704b26d3` before Phase 02 deploy.
Cloudflare edge checks returned `200` for `https://lenerp.lengrowth.com/` and
`https://lenerp-api.lengrowth.com/health`. No DNS, tunnel, Worker, or public
route change was needed.

## Corrected staging path and safe rollback

The prior evidence's `c032a37f78240bba1b8b8593bd3bd439e66a3fb6` is stale and
is not this correction candidate. The corrected candidate is the new immutable
commit recorded in the release record and orchestration status after commit.
Before the corrected staging mutation, a fresh verified backup was captured
under `/opt/saas-control-staging/shared/backups/phase2-20260920T020224Z/`,
including the control-plane SQLite snapshot and the four Frappe
database/config/public/private backup artifacts. The backup inventory and
SHA-256 manifest are retained on the staging host.

The first staging attempt failed during `bench --site erp-staging.example.test
install-app hrms` because HRMS `15.64.1` attempted to create the legacy
`Expense Claim Type` fixture while the pinned Frappe `15.119.1` / ERPNext
`15.120.0` runtime has no `frappe.core.doctype.expense_claim_type` module.
This is an upstream fixture-order compatibility defect, not a worker
success/readback failure. The corrected workflow retains the exact official
HRMS revision, removes only a partial HRMS site registration when present,
clears the isolated site cache, retries once, then migrates and fails closed
unless the exact app, commit, roles and workspaces are read back.

The control-plane candidate was never switched: `current` remained
`802f1bdb0f7642ea627b08235dfa3aa16e7b9eda`, and no `.staging-smoke-passed`
marker was created for Phase 02. The ERP site/database/files were restored from
the pre-attempt backup; HRMS was removed from the bench, Python package, and
bench app registries. Final readback shows only Frappe `15.119.1`, ERPNext
`15.120.0`, and `lenerp_core 0.2.0` installed, with all staging services healthy
and local health responses `18001=200`, `13001=200`, and ERP unauthenticated API
`28000=403`.

## Staging candidate

At the time this record was authored, the corrected candidate had not yet
completed the protected staging workflow. The required candidate-bound gates
remain direct HRMS install/replay, migration, installed-app/version/commit
readback, HR/Payroll role/workspace readback, provisioning retry/replay,
authorization and tenant-isolation smoke, and rollback evidence. Promotion
must use the exact corrected candidate and cannot substitute another HRMS
version or weaken exact verification.

## Production promotion

Production is blocked until every required staging gate above passes. Any
promotion must use the exact staging-tested candidate, the documented backup
path, additive migration, direct site readback, synthetic-only verification,
and the protected production promotion workflow. No employees, salary
structures, payroll entries, tax rules, or accounting postings are authorized.

## Remaining risks and decisions

- HRMS exact source commit is pinned, but the selected HRMS/platform pins are
  incompatible at install time. Resolve that compatibility at the reviewed
  dependency baseline, then repeat the complete staging gate before any
  production work.
- Champion role names, payroll rules, tax/deduction rules, final visibility,
  and acceptance authority remain business decisions; technical verification
  must not be represented as Champion acceptance.
- Cloudflare Wrangler was not deployed because this repository contains no
  Worker/Pages configuration; the installed/authenticated Wrangler check did
  not produce a usable local CLI response. No Cloudflare mutation was made.

## Correction operator readback (2026-09-20)

The isolated staging host was revalidated before the corrected candidate run:

- AWS account `288947333598`, region `us-east-1`, EC2
  `i-0f54fba441caa7154`, security group `sg-0387e9287e4817700`.
- Staging services remained active and ERP web remained bound to loopback
  `127.0.0.1:28000`; no internal port ingress was added.
- A fresh full staging backup was created before HRMS mutation at
  `/opt/saas-control-staging/shared/backups/phase2-20260920T020224Z/` with
  database, site config, public files, private files, and control-plane SQLite
  artifacts plus a SHA-256 manifest.
- The exact official HRMS tag/commit installed and `bench --site
  erp-staging.example.test migrate` completed successfully after the bounded
  replay path. Readback reported Frappe `15.119.1`, ERPNext `15.120.0`, HRMS
  `15.64.1`, HRMS commit `e68a3deaa95ae5b2c3d743297d0a4ab505733fc1`, and
  installed apps `frappe`, `erpnext`, `lenerp_core`, `hrms`.
- Direct provider readback found HRMS `Expense Claim Type`, `Employee`, and
  `Salary Structure` DocTypes, HR roles `HR User` and `HR Manager`, and the
  HRMS-owned `HR` and `Payroll` workspaces. ERP root returned HTTP `200` after
  the required service restart.

These are operator readbacks of the isolated ERP lane. They do not yet claim
that the corrected control-plane commit has passed its protected staging
workflow; the candidate hash, staging run, production backup/promotion, and
final Phase 02 verdict remain pending until that exact workflow completes.
