# Phase 02 — Implementation Evidence

**Date:** 2026-09-20
**Status:** Corrected locally; staging is blocked by the unresolved official HRMS/Frappe compatibility defect. Production remains unchanged.
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
| Source authority | Official upstream `pyproject.toml`, `__init__.py`, `hooks.py`, `setup.py`, tag/branch readback, and [HRMS issue #1639](https://github.com/frappe/hrms/issues/1639) |
| Artifact checksum | Not packaged in this repository; immutable commit/tag is the release identity |

The exact dependency record is [application-dependencies.json](../../ops/staging/application-dependencies.json). The broad
`>=15,<16` metadata is not treated as an installation guarantee: official
Frappe v15.119.1 has no `frappe.core.doctype.expense_claim_type` controller,
while official HRMS v15.64.1 still calls its `Expense Claim Type` fixture from
`after_install`. Issue #1639 records the same traceback. A retry, uninstall,
cache clear, or skipped fixture does not alter that source incompatibility, so
the candidate now fails closed before provider mutation. No upstream source or
fixture is patched.

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
- The staging install workflow and provider adapter refuse the blocked HRMS
  pin; no recovery replay is presented as compatibility evidence. Exact
  installed-app, commit, migration, role and workspace readback remain
  mandatory once an official compatible set is selected.

## Local validation

| Check | Result |
|---|---|
| Focused Phase 02/provider/release tests | PASS — 18 tests |
| Complete backend suite | PASS — 89 tests |
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

Current external readback on 2026-09-20 confirms the production control-plane
pointers remain `current -> 4a63264e1e8cb7c998c767262a6e1022647ff7b0` and
`previous -> 27ede631c667c67f45d534108abeb975816ee83e`. The production ERP site
reports only Frappe `15.119.1` and ERPNext `15.120.0`; HRMS is not installed.
The staging ERP site currently reports Frappe `15.119.1`, ERPNext `15.120.0`,
HRMS `15.64.1`, and `lenerp_core 0.2.0`, but its LenERP source readback is
`d8cb884405d844c50ca8c568ac80572b149f67f3`, not the pinned candidate commit
`a7e47208baf6583295f5f2632f4787262cd3f475`. This is historical/replayed
staging state and is not accepted as clean-install or candidate-bound evidence.
Cloudflare DNS and public HTTPS readbacks for `lenerp.lengrowth.com` and
`lenerp-api.lengrowth.com/health` returned HTTP 200; no edge mutation was made.

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
The corrected candidate has not entered staging mutation: its candidate
preflight stops on the blocked HRMS compatibility record before the control
plane pointer switch or ERP application mutation. No new staging backup was
created for this intentionally blocked path.

The first staging attempt failed during `bench --site erp-staging.example.test
install-app hrms` because HRMS `15.64.1` attempted to create the legacy
`Expense Claim Type` fixture while the pinned Frappe `15.119.1` / ERPNext
`15.120.0` runtime has no `frappe.core.doctype.expense_claim_type` module.
This is an upstream fixture-order compatibility defect, not a worker
success/readback failure. The corrected workflow refuses the blocked official
HRMS pin before staging mutation; it does not uninstall, clear cache, retry,
patch, or skip the incompatible fixture. A future compatible set must still
pass exact app, commit, roles, and workspace readback.

The control-plane candidate was never switched: `current` remained
`802f1bdb0f7642ea627b08235dfa3aa16e7b9eda`, and no `.staging-smoke-passed`
marker was created for Phase 02. The historical ERP site/database/files were
restored from the pre-attempt backup; HRMS was removed from the bench, Python
package, and bench app registries. The last recorded staging readback showed
only Frappe `15.119.1`, ERPNext `15.120.0`, and `lenerp_core 0.2.0` installed,
with staging services healthy. Those are historical host readbacks, not a
current candidate-bound staging pass.

## Staging candidate

No staging candidate has passed. The candidate build preflight now stops before
the control-plane pointer switch because the declared HRMS set is marked
`blocked` in the dependency manifest. The required future gates remain clean
HRMS installation, migration, installed-app/version/commit readback,
HR/Payroll and LenERP role/workspace readback, provisioning retry/replay,
authorization and tenant-isolation smoke, and rollback evidence. Promotion
must use one exact candidate and cannot substitute another HRMS version or
weaken exact verification.

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

## Historical failed operator attempt (superseded)

The isolated staging host was revalidated before the corrected candidate run:

- AWS account `288947333598`, region `us-east-1`, EC2
  `i-0f54fba441caa7154`, security group `sg-0387e9287e4817700`.
- Staging services remained active and ERP web remained bound to loopback
  `127.0.0.1:28000`; no internal port ingress was added.
- A fresh full staging backup was created before HRMS mutation at
  `/opt/saas-control-staging/shared/backups/phase2-20260920T020224Z/` with
  database, site config, public files, private files, and control-plane SQLite
  artifacts plus a SHA-256 manifest.
- The official HRMS tag/commit was attempted against Frappe `15.119.1` and
  ERPNext `15.120.0`; installation failed in `hrms.after_install` while
  creating the removed `Expense Claim Type` fixture. The site was restored
  from the fresh backup and the control-plane pointer was not accepted.
- Any readback recorded after a bounded retry is historical diagnostic evidence
  only; it is superseded and cannot establish clean-install compatibility.

These are historical operator readbacks of the isolated ERP lane. They do not
claim a clean installation, candidate-bound staging pass, production backup or
promotion, independent review, or Phase 02 acceptance.

## Protected candidate attempt and runner recovery

The first protected correction workflow for commit `cdae0535cb3af425b423f6858aaa779d4edf3b98`
was run as GitHub Actions `35483735652` (job `106006113638`). It failed during
the candidate-bound validation suite before candidate deployment because npm
reported `ENOSPC`; staging readback showed the runner root filesystem at
39 GB, 100% used, with approximately 370 MB free. The workflow therefore did
not switch the control-plane staging pointer, create a staging-pass marker, or
mutate production. This candidate is not staging-approved.

Read-only host inspection found 18 GB of old, unreferenced immutable control
plane release directories under `/opt/saas-control/releases`. The active and
previous rollback targets were verified and retained. Twelve explicitly named
older directories were removed after path and pointer validation, leaving
approximately 8.9 GB free. The next correction commit is a new immutable
candidate and must repeat the complete protected staging gate.

The next protected workflow (`35484379236`) used candidate
`3793b9870461828a8421272ac7ace6fd17297561`. It captured and verified the
candidate-bound backup at
`/opt/saas-control-staging/shared/backups/phase2-67eb84e2dc304fa6dbab538fc9ad2d3bb932a84b-35484379236/`, deployed the exact candidate, installed/migrated HRMS and
`lenerp_core`, and passed service, port, HTTP 200/403, and migration steps.
The run failed at the final HRMS commit readback because the smoke script
invoked Git as the runner account against the `frappe`-owned checkout and Git
correctly rejected the repository as dubious ownership. This is a readback
implementation defect; production was unchanged and a new candidate is
required after the script runs the readback as `frappe`.
