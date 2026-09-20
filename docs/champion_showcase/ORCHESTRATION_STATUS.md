# Champion Pre-Kickoff Module Showcase — Orchestration Status

Last updated: 2026-09-20 (Asia/Tbilisi)

## Program state

| Phase | Current state | Gate decision |
| --- | --- | --- |
| 00 | Complete | PASS |
| 01 | Complete; staging gate deferred by prior record | PASS WITH DEFERRED STAGING GATE |
| 02 | Closed; exact protected candidate and browser evidence verified | PASS — Phase 03 permitted; production unchanged |
| 03 | Protected staging PASS on isolated candidate; production SSO remains off | PASS — independent read-only review open |

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
4. Final candidate-bound staging result: protected run
   `35505538638` / job `106064600813` passed for candidate-bound release
   `fa137051b6675fbd09102c07942748ce68ea98b9`; the PR head was
   `cffe8f9e5499f0845fce2dbceec1767c7a3e5ee4`.

The final real-staging backup/control-plane snapshot is
`/opt/saas-control-staging/shared/backups/phase2-fa137051b6675fbd09102c07942748ce68ea98b9-35505538638/`
with SHA-256 manifest. Staging now points to the immutable release
`fa137051b6675fbd09102c07942748ce68ea98b9`; production was not targeted or changed.

The corrected implementation requires exact installed-app/version/commit
readback, migration, roles, workspaces, queues, HTTP, synthetic ERP checks,
replay/idempotency, authorization, rollback evidence, and the immutable
`lenerp_core/SOURCE_COMMIT.txt` marker. Cloudflare was not changed because no
new verified edge defect appeared.

Phase 02 closure readback: protected staging run `35506309957` / job
`106066811682` passed for the reviewed PR head
`796ea2e0cd7aae0bd2b19bc88e6750b93f1a5642` and immutable merge candidate
`9674a6a1b4adf9447af759458763b25721672272`. The exact evidence artifact is
`staging-browser-evidence-9674a6a1b4adf9447af759458763b25721672272`, artifact
ID `10603752341`, digest
`sha256:bd808a20f5f9743e122dc064113160dbf60ad8bd073638b9dd132bf4c191a8ef`.
Production and Cloudflare remain unchanged. Phase 02 is PASS and Phase 03
protected staging is PASS. Independent read-only review remains open; this
record does not claim production SSO.

## Phase 03 — Unified identity and cross-navigation

Protected run `35533376911` / job `106137957752` passed for control-plane
candidate `ce2a339f2e57784ca933e85c78cac6ce60310b14` and canonical LenERP
commit `3a7121974cb55ebcac120af6c07eaab53cfedb2c`. The immutable bundle SHA-256
is `839AF05D5EDB3D05C3D94AE17FF0DB6614901F44D8286045C5621D7AD826A987`.
Browser evidence artifact `10611928332` has digest
`sha256:3e1f685518fd14b05cb656fa1148b8e14d4293f645788f7d9b4fb31850bb6b62`.
The protected run passed the authorization-code/PKCE flow, replay and denial
checks, control-plane-to-ERP and ERP-to-control navigation, direct ERP access,
membership/mapping revocation, feature-off rollback, independent ERP login,
staging restoration, and synthetic cleanup. Phase 04 was not started.

## Worktree preservation

- Preserved unrelated pre-existing modifications: `CLAUDE.md`,
  `frontend/tsconfig.tsbuildinfo`.
