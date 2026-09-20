# CHAMP-P03-R1 — Unified Identity and Cross-Navigation

## Release identity

- Release type: Champion package / platform identity implementation
- State: `local_remediation_complete_staging_rerun_required`
- Control-plane branch: `codex/phase3-unified-identity`
- Control-plane candidate commit: `d4517eeb842e121cd133ca630f9e8b15c4b22f8c`
- Canonical LenERP commit: `8d77cec7504d22f9c0a235034777e31fa07fc62`
- Immutable LenERP bundle SHA-256: `D136208D613DEECE9A51F25A7A1A5B4C7C916D8E657043FFFC7BEEC03B90AAA7`
- Migration: `20260921_0014_phase3_security_hardening` (after `20260920_0013_phase3_unified_identity`)
- Feature flag: `phase3_unified_identity=off` by default; production remains off
- Previous protected staging run: `35542421306` (failed in the Phase 03 browser step on an unavailable Frappe advisory-lock API; cleanup completed).
- Protected rerun: required for this exact candidate; no passing artifact is claimed.
- Champion acceptance: not claimed; independent read-only review remains open.

## Gate status

- [x] Acceptance and rollback boundaries written.
- [x] Work isolated on `codex/phase3-unified-identity` branches.
- [x] Additive migration and downgrade/re-upgrade rehearsal implemented.
- [x] Control-plane, ERP, and cookie boundaries are explicit.
- [x] Local backend/frontend/LenERP validation passes, including browser-bound state, mapping-handle isolation, durable rate-limit, and rollback-script coverage.
- [x] Secret-safe logs and rate-limit paths are implemented.
- [x] Protected staging candidate deployed exactly once for the prior gate run; a new protected remediation run is required.
- [x] Browser control-plane-to-ERP and ERP-to-control-plane journeys captured.
- [ ] Protected remediation staging denial, replay, membership-removal, role, authenticated break-glass rollback, and cleanup evidence captured for the current candidate.
- [ ] Independent read-only review completed.

Local validation totals: backend `109 passed, 5 skipped`, frontend `12 passed`, canonical
LenERP `11 passed`; frontend typecheck/build, workflow YAML validation, and Python compilation passed.

## Safe current state

The code and canonical ERP artifact are local branch changes only. Central SSO
is not authoritative anywhere. Disable the feature flag and tenant rollout flag
to roll back entry points while preserving mappings and audit history.

Full implementation evidence is in
[11_PHASE_03_IMPLEMENTATION_EVIDENCE.md](../../champion_showcase/11_PHASE_03_IMPLEMENTATION_EVIDENCE.md).
