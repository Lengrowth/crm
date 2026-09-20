# CHAMP-P03-R1 — Unified Identity and Cross-Navigation

## Release identity

- Release type: Champion package / platform identity implementation
- State: `local_remediation_ready_staging_rerun_required`
- Control-plane branch: `codex/phase3-unified-identity`
- Control-plane candidate commit: `ce2a339f2e57784ca933e85c78cac6ce60310b14`
- Canonical LenERP commit: `3a7121974cb55ebcac120af6c07eaab53cfedb2c`
- Immutable LenERP bundle SHA-256: `839AF05D5EDB3D05C3D94AE17FF0DB6614901F44D8286045C5621D7AD826A987`
- Migration: `20260921_0014_phase3_security_hardening` (after `20260920_0013_phase3_unified_identity`)
- Feature flag: `phase3_unified_identity=off` by default; production remains off
- Protected staging run: `35533376911`; job `106137957752`.
- Browser evidence artifact: `10611928332`, digest `sha256:3e1f685518fd14b05cb656fa1148b8e14d4293f645788f7d9b4fb31850bb6b62`.
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
- [ ] Protected remediation staging denial, replay, membership-removal, role, authenticated break-glass rollback, and cleanup evidence captured.
- [ ] Independent read-only review completed.

Local validation totals: backend `105 passed, 5 skipped`, frontend `12 passed`, canonical
LenERP `11 passed`; frontend typecheck/build, workflow YAML validation, and Python compilation passed.

## Safe current state

The code and canonical ERP artifact are local branch changes only. Central SSO
is not authoritative anywhere. Disable the feature flag and tenant rollout flag
to roll back entry points while preserving mappings and audit history.

Full implementation evidence is in
[11_PHASE_03_IMPLEMENTATION_EVIDENCE.md](../../champion_showcase/11_PHASE_03_IMPLEMENTATION_EVIDENCE.md).
