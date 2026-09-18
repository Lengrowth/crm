# `CHAMP-C01-R1` — C01 development release record

Status: **IN DEVELOPMENT — not staged, accepted, or released**  
Package: C01 — Company, product name, and branding  
Release identity: `CHAMP-C01-R1`  
Record date: 2026-09-18

## Candidate identity

- CRM control-plane baseline: `08224008142bd8a387f908b656b3565dd1754ae5` on
  authoritative `Lengrowth/crm` `main`
- `lenerp_core` branch: `codex/champ-c01-r1`
- `lenerp_core` commit: `ed551dc`
- `lenerp_core` version: `0.2.0`
- Frappe reference: `15.119.1`,
  `edae775dd36b6c4ad7acab10230262bd74040765`
- ERPNext reference: `15.120.0`,
  `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`
- Schema revision: not installed; no database migration
- Runtime flag: no branding application or domain cutover enabled
- CRM release-path commit: `4eaa7ad` parameterizes
  `EXPECTED_CUSTOM_APP_VERSION`; the existing `0.1.0` default is preserved,
  and C01 staging must invoke the smoke with `EXPECTED_CUSTOM_APP_VERSION=0.2.0`.

## Scope and exclusions

This development slice adds a value-free `LenERP Branding Settings` Single
DocType to the approved custom-app boundary. It contains fields for the
required company, product, asset, branding-mode, and final-domain inputs, but
stores no defaults, Champion data, or assets. It is restricted to `System
Manager` and does not replace standard ERPNext settings.

Excluded until approved: exact company values, product name, logos/colors,
domain ownership/timing, branding application, generated-link changes, print
branding, domain cutover, production configuration, and real Champion data.

## Gate evidence

| Gate | Result | Evidence |
|---|---|---|
| Upstream source clean | PASS | Approved local Frappe/ERPNext reference trees have no working-tree changes |
| Static schema contract | PASS | `python -m pytest -q tests` — 1 passed |
| Python compilation | PASS | `python -m compileall -q lenerp_core` |
| Wheel build | PASS | `lenerp_core-0.2.0-py3-none-any.whl` |
| Wheel metadata inclusion | PASS | Wheel contains `lenerp_branding_settings.json` |
| `git diff --check` | PASS | Clean on custom-app and CRM changes |
| Frappe install/migrate on disposable staging | NOT RUN | No local `bench`; approved host SSH inventory timed out |
| Browser/responsive/print evidence | NOT RUN | Requires approved values and staging candidate |
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

Current package verdict: **BLOCKED pending approved inputs and staging access**.
