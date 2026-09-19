# Phase 01 — Implementation Evidence and Boundaries

**Date:** 2026-09-20
**Status:** Implemented locally; staging/runtime verification remains blocked.

## Authorized staging readback boundary

No authorized live staging installed-app/runtime readback was available from this workstation before implementation. Read-only reachability checks found no listener on the documented staging control-plane ports `18001`/`13001` or ERP port `28000`; no credentials, `bench`, login, write API, install, migrate, seed, reset, DNS, or production command was used.

The evidence retained for this phase is therefore the declared, non-live record in `ops/production/release-runtime-baseline.json`, the pinned archive `ops/staging/lenerp_core-a7e47208baf6583295f5f2632f4787262cd3f475.tar`, `ops/staging/lenerp_core/SOURCE_COMMIT.txt`, and the clean sibling checkout at `C:\Users\smikl\Desktop\Work\lenerp_core` (`fd18845527039619538ab9906cb8197c83e053b1`). The archive checksum is `C62038908A835BAF7C5F3FB418DF561D8E5246AA00156F21D88EAC53153571AC`, and the embedded source marker is `a7e47208baf6583295f5f2632f4787262cd3f475`. The declared runtime lists Frappe, ERPNext, and `lenerp_core` only; HRMS is not verified installed. HR and Payroll consequently remain hidden and `needs-attention` until an authorized readback proves the required HRMS application and role/workspace configuration.

## Artifact reconciliation

- The sibling `fd18845` source and the staged/runtime `a7e47208` archive contain the same application content after line-ending normalization; the archive is the declared runtime artifact and is not re-labeled as a live readback.
- The checked-in staging mirror had duplicate tracked package paths under `ops/staging/lenerp_core/lenerp_core/doctype`, `report`, and `workspace`. The canonical Frappe package paths are `ops/staging/lenerp_core/lenerp_core/lenerp_core/doctype`, `report`, and `workspace`, matching the archive layout. The redundant top-level embedded copies were removed; bytecode remains excluded from evidence.
- No sibling repository or staged/runtime installation was mutated.

## Phase 01 result

`champion-drilling@2` is seeded additively from `champion-drilling@1` with HR, Payroll, Quality, and Support. Bundle versions are immutable: an existing `(bundle_key, version)` is never rewritten by routine seeding. Dependency closure remains deterministic and preview-only until an authorized operator applies it.

The Phase 01 profile document classifies every v2 capability as visible when verified, role-only, pending configuration, or hidden/preserved. The catalog UI presents the capabilities in the required Business, Operations, People, and Platform groups.

The control-plane response now exposes, per module:

- `requested`, `entitled`, `applied`, and `verified` as explicit state flags;
- `hidden` for unentitled, operator-only, preserved, or HR/Payroll-not-yet-verified capabilities;
- `needs_attention` plus human-readable reasons for pending/failed application or verification;
- required backing application and dependency codes before apply.

Module entitlement audits now carry first-class affected tenant IDs and previous/current bundle key/version attribution, while preserving actor, organization, idempotency, and before/after entitlement snapshots.
The organization module audit view renders the affected tenant IDs and bundle transition alongside each change reason.

The provisioning provider and worker require per-module required-app readback before setting `applied`, and require required-app, role, and workspace readback before setting `verified`. Missing HRMS leaves HR/Payroll `pending`, `hidden`, and `needs_attention` with an install/readback/retry action; missing roles/workspaces and failed provider readbacks remain unverified.

No ERP application, HRMS installation, production entitlement change, real Champion data, SSO endpoint, or Champion acceptance was performed.

## Rollback

Rollback is additive and reversible: select the prior `champion-drilling@1` bundle or reverse the audited entitlement change with its idempotency key. Do not delete `champion-drilling@2` after it has been used. The duplicate embedded paths can be restored only if a future release explicitly needs the old malformed mirror; the canonical package paths and declared `a7e47208` archive remain the source of truth.

## Local review gates

- `python -m pytest backend/tests -q`: 63 passed.
- `python -m pytest ops/staging/lenerp_core/tests -q`: 6 passed.
- `npm run typecheck` and `npm test -- --run`: passed, 12 frontend tests.
- Alembic head: `20260920_0012`; migration rehearsal passed.
- Python compile, secret scan, relative Markdown links, and `git diff --check`: passed.

These are local gates only. They do not replace authorized staging installed-app, role/workspace, candidate, rollback, or acceptance evidence.

## Remaining blockers

- Authorized staging installed-app/runtime readback is still required.
- HRMS revision/license/build and HR/Payroll role/workspace verification remain pending.
- ERP application, real data, SSO, production, and Champion acceptance remain out of scope for Phase 01.
