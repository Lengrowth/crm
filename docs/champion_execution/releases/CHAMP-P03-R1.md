# CHAMP-P03-R1 — Unified Identity and Cross-Navigation

## Release identity

- Release type: Champion package / platform identity implementation
- State: `protected_staging_pass_final_sha_rerun_required`
- Control-plane branch: `codex/phase3-unified-identity`
- Control-plane candidate commit: `f9589276076e6514c9054447a026f9758ef64a71`
- Canonical LenERP commit: `8d77cec7504d22f9c0a235034777e31fa07fc62`
- Immutable LenERP bundle SHA-256: `D136208D613DEECE9A51F25A7A1A5B4C7C916D8E657043FFFC7BEEC03B90AAA7`
- Migration: `20260921_0014_phase3_security_hardening` (after `20260920_0013_phase3_unified_identity`)
- Feature flag: `phase3_unified_identity=off` by default; production remains off
- Bootstrap PR: [#83](https://github.com/Lengrowth/crm/pull/83), merged normally at `854460e8c1a94fcbf844b18878023ab87d665f09`.
- Zero-job diagnosis: run `35544065745` combined invalid PR-workflow YAML with default-branch event filtering that produced no eligible PR-branch job.
- Protected staging run: `35580080046`, job `106270676103`, passed for the exact candidate above.
- Evidence artifact: ID `10630670710`, name `staging-browser-evidence-f9589276076e6514c9054447a026f9758ef64a71`, digest `sha256:8dadcefb707df1fb481e7a1980d3aa533c28a099837e814a3f4de1197be4f412`.
- Final protected rerun: required once after this documentation-only commit so the required PASS is attached to the final PR head.
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

The code and canonical ERP artifact are staged only. Central SSO is not
authoritative anywhere. The protected lane verified flag/configuration restore,
independent login after rollback, synthetic identity/mapping/file cleanup, zero
synthetic ERP counts, and no temporary AWS SSH access. Production and Cloudflare
were unchanged. PR #82 is intentionally open and unmerged; Phase 04 has not
started.

Full implementation evidence is in
[11_PHASE_03_IMPLEMENTATION_EVIDENCE.md](../../champion_showcase/11_PHASE_03_IMPLEMENTATION_EVIDENCE.md).
