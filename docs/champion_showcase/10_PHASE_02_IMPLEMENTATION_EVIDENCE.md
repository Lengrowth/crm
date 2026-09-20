# Phase 02 — Implementation Evidence

**Date:** 2026-09-20
**Status:** PASS — clean disposable HRMS compatibility verified and corrected protected staging candidate passed. Ready for independent read-only review; production remains unchanged.
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
| Artifact checksum | `C62038908A835BAF7C5F3FB418DF561D8E5246AA00156F21D88EAC53153571AC` for the pinned LenERP bundle |

The exact dependency record is [application-dependencies.json](../../ops/staging/application-dependencies.json). The broad
`>=15,<16` metadata is backed by the one-time disposable proof in
[phase2-clean-disposable-install.json](../../ops/staging/evidence/phase2-clean-disposable-install.json).
That proof installed the exact pins once and recorded no `Expense Claim Type`
DocType or `HR` Module Def before HRMS. After HRMS installation and migration,
the DocType was `module=HR` and the Module Def was `app_name=hrms`. Issue #1639
therefore documents a stale/incorrect site metadata resolution, not proof that
the official v15 pin is incompatible. No upstream source or fixture is patched,
skipped, uninstalled, or replayed as acceptance evidence.

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
- The staging install workflow now installs the exact HRMS tag once when the
  app is absent, migrates idempotently, and requires exact installed-app,
  version, commit, role, workspace, and source-marker readback. The provider
  adapter reports `lenerp_core`'s immutable artifact marker instead of
  assuming every app is a Git checkout.

## Local validation

| Check | Result |
|---|---|
| Focused Phase 02/provider/release tests | PASS — 17 tests, 4 warnings |
| Complete backend suite | PASS — 74 tests, 25 warnings |
| Python compile/import | PASS — `python -m compileall -q backend/app` |
| Frontend tests | PASS — 12 tests |
| Frontend typecheck/build | PASS — `npm --prefix frontend run typecheck` and `npm --prefix frontend run build` |
| Staging/release package tests | PASS — 9 tests; additional contract/manifest check 5 tests |
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
The final staging ERP site reports Frappe `15.119.1`, ERPNext `15.120.0`,
HRMS `15.64.1`, and `lenerp_core 0.2.0`, with source readbacks
`edae775dd36b6c4ad7acab10230262bd74040765`,
`945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`,
`e68a3deaa95ae5b2c3d743297d0a4ab505733fc1`, and
`a7e47208baf6583295f5f2632f4787262cd3f475`, respectively. The prior `d8cb884…`
checkout is historical/replayed state and is superseded by the final artifact.
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
The clean disposable gate passed before the real staging correction. A real
staging backup and control-plane copy were then captured at
`/opt/saas-control-staging/shared/backups/phase2-cleanproof-20260920T101500Z/`;
the staging pointer was unchanged at
`/opt/saas-control-staging/releases/47d1d6dd3b8ecbd0b490485d38160df7001b5169`.
The corrected protected candidate retained a new backup at
`/opt/saas-control-staging/shared/backups/phase2-fa137051b6675fbd09102c07942748ce68ea98b9-35505538638/`
and reconciled the LenERP artifact marker to
`a7e47208baf6583295f5f2632f4787262cd3f475`.

The first historical staging attempt failed while the dirty/partial site
resolved the fixture through `frappe.core.doctype.expense_claim_type`. The
failure was a site metadata/install-state defect. The clean disposable proof
resolved the same DocType through `HR/hrms` on the same immutable versions;
the corrected workflow therefore proceeds through the exact pin and keeps all
readbacks fail-closed without uninstall, fixture skipping, or local patching.

For the historical failed attempt, the control-plane candidate was never
switched: `current` remained
`802f1bdb0f7642ea627b08235dfa3aa16e7b9eda`, and no `.staging-smoke-passed`
marker was created for Phase 02. The historical ERP site/database/files were
restored from the pre-attempt backup; HRMS was removed from the bench, Python
package, and bench app registries. The last recorded staging readback showed
only Frappe `15.119.1`, ERPNext `15.120.0`, and `lenerp_core 0.2.0` installed,
with staging services healthy. Those are historical host readbacks, not a
current candidate-bound staging pass.

## Final staging candidate

The disposable clean-install candidate passed. Protected run `35484693593`
(`106008810882`) completed the earlier pinned staging path for candidate
`27f4907578f09e1f540c90e7e6d8fd30fd9aaeb5`. The corrected final run
`35505538638` (`106064600813`) passed for candidate-bound release
`fa137051b6675fbd09102c07942748ce68ea98b9` and PR head
`cffe8f9e5499f0845fce2dbceec1767c7a3e5ee4`.

Final staging readback: Frappe `15.119.1` /
`edae775dd36b6c4ad7acab10230262bd74040765`, ERPNext `15.120.0` /
`945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`, HRMS `15.64.1` /
`e68a3deaa95ae5b2c3d743297d0a4ab505733fc1`, and `lenerp_core 0.2.0` /
`a7e47208baf6583295f5f2632f4787262cd3f475`. Migration, HR/Payroll roles and
workspaces, queues, HTTP, synthetic ERP, replay/idempotency, authorization,
browser/accessibility, print/export, and cleanup gates passed. The artifact is
[staging-browser-evidence-fa137051b6675fbd09102c07942748ce68ea98b9](https://github.com/Lengrowth/crm/actions/runs/35505538638/artifacts/10603289709).

The final backup and rollback boundary is
`/opt/saas-control-staging/shared/backups/phase2-fa137051b6675fbd09102c07942748ce68ea98b9-35505538638/`.
The workflow was staging-only; production and Cloudflare were unchanged.
Phase 03 synthetic browser creation was disabled for this Phase 02 run, and
the final readback reports zero Phase 2 and Phase 3 synthetic records.

## Production promotion

Production is blocked until every required staging gate above passes. Any
promotion must use the exact staging-tested candidate, the documented backup
path, additive migration, direct site readback, synthetic-only verification,
and the protected production promotion workflow. No employees, salary
structures, payroll entries, tax rules, or accounting postings are authorized.

## Remaining risks and decisions

- HRMS exact source commit and clean-install compatibility are now verified;
  the remaining gate is candidate-bound staging reconciliation and independent
  read-only review.
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
