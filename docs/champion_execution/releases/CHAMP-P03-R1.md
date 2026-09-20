# CHAMP-P03-R1 — Unified Identity and Cross-Navigation

## Release identity

- Release type: Champion package / platform identity implementation
- State: `implemented_locally_staging_gate_open`
- Control-plane branch: `codex/phase3-unified-identity`
- Control-plane implementation commit: `6fcca9105c4ab811b0124beba5040b7adbb30aee`
- Canonical LenERP commit: `568b7fe947af344e7f4b67739f4f30b2b1c50d2d`
- Immutable LenERP bundle SHA-256: `D4AB4EA8D683E8F0D9FC29668379FE334D20B76968C0A961E1015BCE3AAB9EC3`
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
