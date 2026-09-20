# CHAMP-P03-R1 — Unified Identity and Cross-Navigation

## Release identity

- Release type: Champion package / platform identity implementation
- State: `implemented_locally_staging_gate_open`
- Control-plane branch: `codex/phase3-unified-identity`
- Control-plane implementation commit: `6220253ec0750455a5e6e9c76ef0690406c3809d`
- Canonical LenERP commit: `2eb71db1c633e0d97382ef8e8b92002909d6cbb0`
- Immutable LenERP bundle SHA-256: `265440B0D548C69D29A48C87896A2C8989BFE9485718E52413E19AE3C73F5290`
- Migration: `20260920_0013_phase3_unified_identity`
- Feature flag: `phase3_unified_identity=off` by default; production remains off
- Champion acceptance: not claimed

## Gate status

- [x] Acceptance and rollback boundaries written.
- [x] Work isolated on `codex/phase3-unified-identity` branches.
- [x] Additive migration and downgrade/re-upgrade rehearsal implemented.
- [x] Control-plane, ERP, and cookie boundaries are explicit.
- [x] Local backend/frontend/LenERP validation passes.
- [x] Secret-safe logs and rate-limit paths are implemented.
- [ ] Protected staging candidate deployed exactly once.
- [ ] Browser control-plane-to-ERP and ERP-to-control-plane journeys captured.
- [ ] Protected staging denial, replay, membership-removal, role, rollback, and cleanup evidence captured.
- [ ] Independent read-only review completed.

Local validation totals: backend `82 passed`, frontend `12 passed`, canonical
LenERP `11 passed`; frontend typecheck/build and Python compilation passed.

## Safe current state

The code and canonical ERP artifact are local branch changes only. Central SSO
is not authoritative anywhere. Disable the feature flag and tenant rollout flag
to roll back entry points while preserving mappings and audit history.

Full implementation evidence is in
[11_PHASE_03_IMPLEMENTATION_EVIDENCE.md](../../champion_showcase/11_PHASE_03_IMPLEMENTATION_EVIDENCE.md).
