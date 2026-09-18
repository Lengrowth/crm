# `CHAMP-C01-R1` — C01 development release record

Status: **IN DEVELOPMENT — not staged, accepted, or released**  
Package: C01 — Company, product name, and branding  
Release identity: `CHAMP-C01-R1`  
Record date: 2026-09-19

## Candidate identity

- CRM control-plane baseline: `08224008142bd8a387f908b656b3565dd1754ae5` on
  authoritative `Lengrowth/crm` `main`
- `lenerp_core` branch: `codex/champ-c01-r1`
- `lenerp_core` commit: `617ea2d67be070b9fe1e389635d3e191edb66d3f` on
  `codex/champ-c01-r1`
- `lenerp_core` version: `0.2.0`
- Frappe reference: `15.119.1`,
  `edae775dd36b6c4ad7acab10230262bd74040765`
- ERPNext reference: `15.120.0`,
  `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`
- Schema revision: additive custom DocTypes/workflow/report/print metadata; staging migration pending
- Runtime flag: no branding application or domain cutover enabled
- CRM release path now fetches the exact `lenerp_core` ref in the protected
  staging workflow, installs/migrates it only on the isolated ERP staging
  bench, and runs the explicit synthetic seed/status smoke.

## Scope and exclusions

This development release keeps the value-free `LenERP Branding Settings`
boundary and adds the reversible C01–C08 synthetic demonstration: Champion
role profiles, Well Site and Drilling Job DocTypes, workflow transitions,
standard ERPNext seed coverage, source-backed operations reporting/API, and a
job completion print format. The explicit demo seed creates only fictitious
records and is never called by install/migrate.

Excluded until approved: exact company values, product name, logos/colors,
domain ownership/timing, branding application, generated-link changes, print
branding, domain cutover, production configuration, and real Champion data.

## Gate evidence

| Gate | Result | Evidence |
|---|---|---|
| Upstream source clean | PASS | Approved local Frappe/ERPNext reference trees have no working-tree changes |
| Static schema contract | PASS | `python -m pytest -q tests` — 4 passed |
| Python compilation | PASS | `python -m compileall -q lenerp_core` |
| Wheel build | PASS | `lenerp_core-0.2.0-py3-none-any.whl` |
| Wheel metadata inclusion | PASS | Wheel contains custom DocTypes, report, workspace, and seed modules |
| `git diff --check` | PASS | Clean on custom-app and CRM changes |
| Frappe install/migrate on isolated staging | PENDING WORKFLOW | Protected workflow now installs exact app ref and runs `erp_demo_smoke.sh` |
| Browser/responsive/print evidence | LOCAL PASS / STAGING PENDING | Local customer pages pass responsive overflow checks; ERP browser evidence requires staged app access |
| Champion UAT/acceptance | NOT RUN | Acceptance authority and Project Start decisions unavailable |
| Production promotion | NOT AUTHORIZED | Package is not accepted and no production behavior is enabled |

## Acceptance and recovery

- Acceptance authority: pending `AGR-02`.
- Success: approved settings install and apply through a staging-tested,
  version-controlled release without changing unrelated ERPNext settings.
- Authorization failure: non-System-Manager access is denied directly, by API,
  and through search/export paths.
- Validation failure: missing or invalid approved inputs do not apply branding.
- Code rollback: return to `lenerp_core` `728de29176ddb9c05c78d734318406d57f10f205`.
- Data correction: correct/remove the additive settings document; do not treat
  code rollback as data correction.

Current package verdict: **IN DEVELOPMENT — synthetic demonstration ready for protected staging validation**.
