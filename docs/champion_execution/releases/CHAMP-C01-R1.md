# `CHAMP-C01-R1` — C01 development release record

Status: **IN DEVELOPMENT — synthetic staging pass; Champion acceptance pending**
Package: C01 — Company, product name, and branding  
Release identity: `CHAMP-C01-R1`  
Record date: 2026-09-19

## Candidate identity

- CRM candidate: exact protected candidate selected from `codex/plat-p4-readback-docs`
- `lenerp_core` branch: `codex/champ-c01-r1`
- `lenerp_core` commit: `6d1369252e6279eb1d2cfdf6315c0dce884303d6` on
  `codex/champ-c01-r1`
- `lenerp_core` version: `0.2.0`
- Frappe reference: `15.119.1`,
  `edae775dd36b6c4ad7acab10230262bd74040765`
- ERPNext reference: `15.120.0`,
  `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`
- Schema revision: additive custom DocTypes/workflow/report/print metadata; isolated staging migration passed
- Runtime flag: no branding application or domain cutover enabled
- CRM release path now verifies a SHA256-pinned, content-addressed archive of
  the exact `lenerp_core` commit, extracts that archive for install/migrate on
  the isolated ERP staging bench, and runs the complete seed, role, browser,
  print/export, accessibility, and reset sequence.

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
| Static schema contract | PASS | `python -m pytest -q tests` — 6 passed |
| Python compilation | PASS | `python -m compileall -q lenerp_core` |
| Wheel build | PASS | `lenerp_core-0.2.0-py3-none-any.whl` |
| Wheel metadata inclusion | PASS | Wheel contains custom DocTypes, report, workspace, and seed modules |
| `git diff --check` | PASS | Clean on custom-app and CRM changes |
| Frappe install/migrate on isolated staging | PENDING FINAL PROTECTED RUN | The workflow now deploys only the checksum-verified archive for `lenerp_core` `e87d348…` |
| Synthetic ERP seed/status | IMPLEMENTED; PENDING FINAL PROTECTED RUN | Required persisted journey includes Company 1, Customer 3, Contact 3, Well Site 3, Drilling Job 4, Supplier 1, Item 2, Warehouse 1, Purchase Receipt 1, Stock Entry 1, Asset 2, Asset Maintenance 2, Quotation 1, Sales Invoice 1, Payment Entry 1 |
| Role/browser/print/export/responsive/accessibility evidence | IMPLEMENTED; PENDING FINAL PROTECTED RUN | Real Champion role principals, direct ERP API denials, print/PDF, export, desktop/mobile ERP screens, and reset evidence are captured by the protected workflow |
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

Current package verdict: **IN DEVELOPMENT — synthetic core demonstration passed protected staging; Champion acceptance and optional ERPNext prerequisite decisions remain open**.

## Protected staging evidence

- The next protected run is candidate-bound to the exact CRM commit selected by
  `candidate_ref`, and its browser artifact is named with that full commit SHA.
- Configuration remains `operator-validation`, Phase 1 shell `off`, Phase 4
  synthetic state `off`; no Phase 4 evidence or production activation is
  claimed.
- The run is synthetic staging evidence only. Project Start decisions, Champion
  UAT, acceptance authority, real-data migration, final domain, and production
  promotion remain pending.
