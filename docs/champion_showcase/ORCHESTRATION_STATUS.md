# Champion Pre-Kickoff Module Showcase — Orchestration Status

Last updated: 2026-09-20 (Asia/Tbilisi)

## Program state

| Phase | Current state | Gate decision |
| --- | --- | --- |
| 00 | Complete | PASS |
| 01 | Complete; staging gate deferred by prior record | PASS WITH DEFERRED STAGING GATE |
| 02 | Corrected locally; clean disposable compatibility proof passed; protected candidate verification pending | In progress — Phase 02 only |
| 03–08 | Not started | Pending Phase 02 PASS |

## Phase 02 — HRMS and dependency-aware provisioning

The prior conclusion that no compatible official HRMS v15 baseline existed was
unsupported. Issue #1639 records a failed site resolving the fixture through
`frappe.core`; it does not prove that HRMS lacks the DocType. The exact pins
remain unchanged:

- Frappe `15.119.1` / `edae775dd36b6c4ad7acab10230262bd74040765`.
- ERPNext `15.120.0` / `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`.
- HRMS `15.64.1` / `e68a3deaa95ae5b2c3d743297d0a4ab505733fc1`.
- `lenerp_core` `0.2.0` / artifact source marker `a7e47208baf6583295f5f2632f4787262cd3f475`.

Evidence is deliberately separated into four states:

1. Historical dirty/partial-site failure: `35484379236` exposed a Git
   ownership/readback defect and the earlier replay exposed stale metadata;
   neither is compatibility evidence.
2. Successful protected run: `35484693593` / job `106008810882` completed the
   pinned staging path for candidate `27f4907578f09e1f540c90e7e6d8fd30fd9aaeb5`.
3. New clean disposable proof: `ops/staging/evidence/phase2-clean-disposable-install.json`
   records one-time installation and migration in the order Frappe, ERPNext,
   HRMS, `lenerp_core`; before HRMS the DocType and HR Module Def were absent,
   and afterward `Expense Claim Type` was `module=HR` with
   `Module Def.app_name=hrms`.
4. Final candidate-bound staging result: pending the protected workflow for
   the corrected PR head, including exact LenERP artifact reconciliation.

The real staging backup/control-plane snapshot for this correction is
`/opt/saas-control-staging/shared/backups/phase2-cleanproof-20260920T101500Z/`
with SHA-256 manifest. The staging pointer remained
`47d1d6dd3b8ecbd0b490485d38160df7001b5169`; production was not changed.

The corrected implementation requires exact installed-app/version/commit
readback, migration, roles, workspaces, queues, HTTP, synthetic ERP checks,
replay/idempotency, authorization, rollback evidence, and the immutable
`lenerp_core/SOURCE_COMMIT.txt` marker. Cloudflare was not changed because no
new verified edge defect appeared.

Scoped Phase 02 production-path scripts remain locally validated but have not
been executed against production. No Phase 03 work is included or authorized.

## Worktree preservation

- Preserved unrelated pre-existing modifications: `CLAUDE.md`,
  `frontend/tsconfig.tsbuildinfo`.
