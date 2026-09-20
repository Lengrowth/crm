# Champion Pre-Kickoff Module Showcase — Orchestration Status

Last updated: 2026-09-20 (Asia/Tbilisi)

## Program state

| Phase | Current state | Gate decision |
| --- | --- | --- |
| 00 | Complete | PASS |
| 01 | Complete; staging gate deferred by prior record | PASS WITH DEFERRED STAGING GATE |
| 02 | Corrected locally; staging blocked by official HRMS compatibility | FAIL — EXTERNAL REQUIREMENT |
| 03–08 | Not started; blocked on Phase 02 PASS | Pending |

## Phase 02 — HRMS and dependency-aware provisioning

Current correction disposition: the historical staging-success claims below
are superseded. Candidate `87a812531569374232ed80f1cd98ac7bd0ff6099` is not
resolvable in this checkout or from the configured remotes, and the official
HRMS/Frappe compatibility set is now explicitly blocked pending an upstream
fix or an approved aligned baseline. No production mutation is authorized by
this record.

- Implementation candidate reported by the prior implementation: `97d5f63`.
- Reported staging candidate in implementation evidence: `c032a37f78240bba1b8b8593bd3bd439e66a3fb6`; reconciliation is an explicit review gate.
- Initial reviewer: fresh `gpt-5.6-luna` (high reasoning), read-only; verdict: **FAIL — CORRECTIONS REQUIRED**.
- Review findings: staging HRMS install/migration failed; reported staging candidate `c032a37f78240bba1b8b8593bd3bd439e66a3fb6` differs materially from reported implementation commit `97d5f63`; broad v15 metadata constraints did not establish compatibility; successful candidate-bound runtime readbacks and production gate evidence are absent; runtime HRMS identity must be bound explicitly.
- Exact pins independently observed by review: Frappe 15.119.1 (`edae775dd36b6c4ad7acab10230262bd74040765`), ERPNext 15.120.0 (`945e825bee3d0d645f6cb59bcaab90fcbfb98ce3`), HRMS v15.64.1 (`e68a3deaa95ae5b2c3d743297d0a4ab505733fc1`).
- Correction agent: `gpt-5.6-luna` (high reasoning), write/deployment capable; scope strictly Phase 02; correction cycle 1 completed locally and blocked before staging mutation.
- First protected correction workflow: GitHub Actions run `35483735652` / job `106006113638` reached candidate-bound validation but failed before candidate deployment because the staging runner filesystem was full (`/dev/root` 39 GB, 100% used; npm reported `ENOSPC`). No candidate switch, ERP mutation, or production mutation occurred in that run.
- Capacity remediation: read-only inspection identified 18 GB of unreferenced historical directories under `/opt/saas-control/releases`; the active and previous rollback targets (`4a63264e1e8cb7c998c767262a6e1022647ff7b0` and `27ede631c667c67f45d534108abeb975816ee83e`) were preserved, and twelve older unreferenced directories were removed with explicit target validation. The host now has 8.9 GB free (78% used). This is recorded as deployment-infrastructure remediation, not a phase implementation result.
- Reported prior staging result: HRMS v15.64.1 installation failed due to missing Expense Claim Type on the pinned Frappe 15.119.1 / ERPNext 15.120.0 baseline; staging was reportedly restored from backup; production reportedly unchanged.
- Compatibility decision: the historical selection of official HRMS `v15.64.1` commit `e68a3deaa95ae5b2c3d743297d0a4ab505733fc1` is retained only as a rejected/blocked pin. Frappe v15.119.1 has no `frappe.core.doctype.expense_claim_type` controller while HRMS v15.64.1 still creates that fixture. No retry, fixture skip, local patch, or floating pin is accepted as compatibility evidence.
- Staging access validation: AWS account `288947333598`, region `us-east-1`, EC2 `i-0f54fba441caa7154`, SG `sg-0387e9287e4817700`; temporary SSH `/32` `212.58.102.127/32` was added only for this correction and will be revoked after evidence capture. Internal ERP/control-plane ports remain loopback-only.
- Fresh staging backup: `/opt/saas-control-staging/shared/backups/phase2-20260920T020224Z/`; database/config/public/private/control-plane artifacts created and SHA-256 manifest retained before HRMS mutation.
- Staging compatibility replay: historical diagnostic attempt only; the clean install failed at the HRMS `Expense Claim Type` fixture and the site was restored. It is not a staging pass.
- Deployment/rollback state: the corrected candidate's release preflight stops before pointer switch because the official HRMS pin is blocked; historical staging services/readbacks remain audit evidence only; production was not changed.
- Correction commits: `cdae0535cb3af425b423f6858aaa779d4edf3b98` (HRMS recovery/readbacks), `e8757881735bd4a2d7ba2ebec3fdd22a94a66981` (recorded protected-run ENOSPC and capacity remediation), `3793b9870461828a8421272ac7ace6fd17297561` (candidate-bound backup, lenerp_core bench registration, backup-bound ERP readback).
- Candidate `3793b9870461828a8421272ac7ace6fd17297561` captured a candidate-bound backup, deployed, installed/migrated pinned HRMS and lenerp_core, then workflow `35484379236` failed only at HRMS commit readback because Git was invoked as the runner against a `frappe`-owned checkout (dubious ownership). No staging restore was needed for that readback-only failure; production stayed unchanged.
- Corrective commit/candidate: `27f4907578f09e1f540c90e7e6d8fd30fd9aaeb5`, which performs Git commit readback as `frappe` rather than weakening Git ownership checking.
- Protected workflow `35484693593`, job `106008810882`, and candidate `87a812531569374232ed80f1cd98ac7bd0ff6099` are historical claims retained for audit only; the candidate is not resolvable locally or from configured remotes and is not accepted.
- Historical candidate-bound staging evidence claim for backup `/opt/saas-control-staging/shared/backups/phase2-87a812531569374232ed80f1cd98ac7bd0ff6099-35484693593/` is superseded and cannot be used as current evidence because the candidate is not resolvable and the HRMS clean-install failure remains established.
- Production has not been changed. The existing promotion workflow is incorrectly coupled to `phase3_migration_approved=yes` and would apply a Phase 03 migration. It cannot be used for Phase 02 promotion as-is; this is an active scoped release-flow correction, not a Phase 03 approval.
- Scoped Phase 02-only production-path scripts are implemented and locally validated: `scripts/release/materialize_phase2_production_candidate.sh`, `scripts/release/run_verified_production_backup.sh`, `scripts/release/phase2_production_preflight.sh`, and `scripts/release/install_phase2_production_hrms.sh`. They have not been executed against production.
- Read-only production baseline: current `4a63264e1e8cb7c998c767262a6e1022647ff7b0`, previous `27ede631c667c67f45d534108abeb975816ee83e`; services and R2 backup timer active; ERP `apps.txt` currently contains only Frappe/ERPNext. No pointer/app/migration/backup mutation/restart occurred during this remediation design.
- Current AWS/ERP readback: production site has only Frappe `15.119.1` and ERPNext `15.120.0`; staging site has HRMS `15.64.1` and exact Frappe/ERPNext/HRMS commits but `lenerp_core` reads `d8cb884405d844c50ca8c568ac80572b149f67f3` instead of the pinned `a7e47208baf6583295f5f2632f4787262cd3f475`. Staging is historical/replayed state, not a clean candidate pass. Cloudflare public endpoints returned HTTP 200 and were not changed.
- Unresolved decisions: upstream-compatible HRMS release or approved aligned baseline; fresh independent read-only review; final Phase 02 gate. No staging or production mutation is authorized while the compatibility gate is blocked.
- Workflow `35484379236` captured and verified backup `/opt/saas-control-staging/shared/backups/phase2-67eb84e2dc304fa6dbab538fc9ad2d3bb932a84b-35484379236`, deployed the exact candidate, installed/migrated HRMS and `lenerp_core`, and passed HTTP/service checks. It failed at HRMS commit readback because the smoke script ran Git as the runner user against the `frappe`-owned checkout (`dubious ownership`). No production mutation occurred; the readback is corrected in the next immutable candidate.

## Worktree preservation

- Preserved unrelated pre-existing modifications: `CLAUDE.md`, `frontend/tsconfig.tsbuildinfo`.
