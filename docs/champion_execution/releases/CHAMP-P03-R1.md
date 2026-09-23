# CHAMP-P03-R1 — Unified Identity and Cross-Navigation

## Release identity

- Release type: Champion package / platform identity implementation
- State: `protected_staging_pass_merged_review_correction_pending`
- Control-plane branch: `codex/phase3-unified-identity`
- Control-plane candidate commit: `47b15d89a2dba0709b226fa2a2b44f758ef0ee95`
- Canonical LenERP commit: `8d77cec7504d22f9c0a235034777e31fa07fc62`
- Immutable LenERP bundle SHA-256: `D136208D613DEECE9A51F25A7A1A5B4C7C916D8E657043FFFC7BEEC03B90AAA7`
- Migration: `20260921_0014_phase3_security_hardening` (after `20260920_0013_phase3_unified_identity`)
- Feature flag: `phase3_unified_identity=off` by default; production remains off
- Bootstrap PR: [#83](https://github.com/Lengrowth/crm/pull/83), merged normally at `854460e8c1a94fcbf844b18878023ab87d665f09`.
- Zero-job diagnosis: run `35544065745` combined invalid PR-workflow YAML with default-branch event filtering that produced no eligible PR-branch job.
- Protected staging run: `35583191594`, job `106280466398`, passed for the exact candidate above.
- Evidence artifact: ID `10631363593`, name `staging-browser-evidence-47b15d89a2dba0709b226fa2a2b44f758ef0ee95`, digest `sha256:c539d39a1d3699d00025ea93329ea82b92519dc5a8c261ceedf77e58593e92a7`.
- PR #82 merge: `c7b0b4e40b6e5ac31ab244cde2303fc83a884d36`; this merge occurred before the corrective review record was prepared.
- Champion acceptance: not claimed; independent read-only review remains open.

## Gate status

- [x] Acceptance and rollback boundaries written.
- [x] Work isolated on `codex/phase3-unified-identity` branches.
- [x] Additive migration and downgrade/re-upgrade rehearsal implemented.
- [x] Control-plane, ERP, and cookie boundaries are explicit.
- [x] Local backend/frontend/LenERP validation passes, including browser-bound state, mapping-handle isolation, durable rate-limit, and rollback-script coverage.
- [x] Secret-safe logs and rate-limit paths are implemented.
- [x] Protected staging candidate deployed and evidence uploaded for the exact remediation candidate.
- [x] Browser control-plane-to-ERP and ERP-to-control-plane journeys captured.
- [x] Protected remediation staging denial, replay, membership-removal, role, authenticated break-glass rollback, and cleanup evidence captured for the current candidate.
- [ ] Independent read-only review completed.

Local validation totals: backend `89 passed, 25 warnings`, focused Phase 03 `10 passed`,
frontend `12 passed`, canonical LenERP `11 passed`; frontend typecheck/build,
workflow YAML validation, and Python compilation passed.

## Safe current state

The code and canonical ERP artifact were verified in staging. Central SSO is not
authoritative anywhere. The protected lane verified flag/configuration restore,
independent login after rollback, synthetic identity/mapping/file cleanup, zero
synthetic ERP counts, and no temporary AWS SSH access. Production and Cloudflare
were unchanged. PR #82 is merged at the merge commit recorded above; Phase 04
has not started and production SSO remains disabled.

Full implementation evidence is in
[11_PHASE_03_IMPLEMENTATION_EVIDENCE.md](../../champion_showcase/11_PHASE_03_IMPLEMENTATION_EVIDENCE.md).
