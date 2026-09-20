# Phase 03 — Unified Identity and Cross-Navigation Evidence

**Date:** 2026-09-21 (Asia/Tbilisi)
**Status:** LOCAL REMEDIATION COMPLETE — protected staging rerun required; production SSO is disabled.
**Scope:** additive authorization-code broker boundary, canonical LenERP relying-party bridge, and control-plane/ERP navigation.

## Release identity

- Control-plane branch: `codex/phase3-unified-identity`.
- Control-plane candidate commit: `b2b6debbdd2af0fee1e8a974b7988b979145b40b`.
- Canonical `lenerp_core` branch: `codex/phase3-unified-identity`.
- Canonical LenERP remediation commit: `8d77cec7504d22f9c0a235034777e31fa07fc62`.
- Immutable remediation bundle: `ops/staging/lenerp_core-8d77cec7504d22f9c0a235034777e31fa07fc62.tar`.
- Bundle SHA-256: `D136208D613DEECE9A51F25A7A1A5B4C7C916D8E657043FFFC7BEEC03B90AAA7`.
- Control-plane dependency manifest and installed source marker point to that exact commit.
- Migration: `20260920_0013_phase3_unified_identity`, additive and downgrade-tested.

## Implemented boundary

The control plane remains the user, organization-membership, and tenant authority.
ERP/Frappe remains a separate relying application with a host-scoped Frappe
session. The temporary broker issues only a short-lived, single-use code whose
database representation is SHA-256 hashed. The ERP exchanges it server-to-server
with PKCE S256, exact client/audience/redirect/tenant checks, expiry and replay
checks, then creates the normal Frappe session. No password, password hash,
control-plane cookie, Frappe cookie, or reusable bearer token crosses the
boundary. The replacement gate is a maintained OAuth/OIDC provider/client with
the same exact tenant and role-policy contract.

JIT provisioning is explicit: the ERP site must set `lenerp_sso_jit_enabled=1`
for a new Frappe user to be created; otherwise only an existing approved ERP
user may be reconciled.

Persistent identity mappings record control-plane user, organization, tenant,
ERP site, ERP user, role-profile version, status, and timestamps. Audit rows
record authorization, exchange, denial, replay, role reconciliation, and
revocation events without codes, verifiers, cookies, or secrets.

Membership removal denies every subsequent authorization, token exchange, and
mapping reconciliation, and marks the persistent mapping revoked at the next
control-plane boundary. Existing ERP cookies are host-scoped and are not
silently converted or shared; an already-issued Frappe session remains subject
to its normal Frappe expiry/operator logout policy. Immediate cross-host session
revocation is intentionally outside this temporary broker and is a replacement
gate for a maintained OIDC provider with back-channel logout support.

## UX implementation

- Control-plane `/sso/authorize` reuses the central session, preserves the safe ERP path, and returns denial, expiry, outage, and retry states.
- Authorized tenant detail includes destination, organization, environment, and a readiness-gated `Open ERP` action.
- ERP direct visits initiate the same request; the ERP login surface offers `Sign in with LenERP Control Plane`.
- ERP user navigation includes `LenERP Control Plane` with the configured exact organization/tenant destination.
- Break-glass local login remains separately protected by the configured Frappe administrator boundary.

## Local validation

- Backend full suite: PASS — 109 passed, 5 skipped, 25 existing deprecation warnings; focused Phase 03/control release gate passes.
- Phase 03 security/service tests: PASS, including browser-bound state contract, concurrent code replay, mapping-handle isolation/replay, expiry, PKCE, audience, redirect/path variants, membership, role readiness, deterministic mapping, durable rate limiting, and feature-off denial.
- Frontend Vitest: PASS, 12 tests.
- Frontend typecheck: PASS.
- Frontend production build: PASS, including `/sso/authorize`.
- Canonical LenERP tests: PASS, 11 tests; Python compile: PASS.
- Phase 02 release-script scenario tests cover absent HRMS, exact replay, wrong version/source, failed install, and backup restore; POSIX execution is required for the shell scenarios.

## Staging and production boundary

Protected run `35542421306` was executed against the prior remediation candidate
and reached the Phase 03 browser flow, where it exposed an unsupported
`frappe.db.advisory_lock` call. The current candidate replaces that call with an
explicit MariaDB `GET_LOCK`/`RELEASE_LOCK` guard and repins the immutable bundle.
The server-controlled `phase3_unified_identity` flag defaults off. A fresh
protected run must still capture the browser artifact, API contracts, membership
removal, authenticated break-glass checks before enablement/during enablement/after
rollback, and exact cleanup. Production SSO, production, Cloudflare, upstream
Frappe, ERPNext, and HRMS remain unchanged.

## Rollback

Disable `phase3_unified_identity` and the isolated tenant rollout flag. The staging
workflow now verifies a fresh break-glass login and protected route before enablement,
while SSO is enabled, and after rollback. Remove
the ERP SSO entry points from staging configuration or restore the prior
immutable candidate. Independent Frappe login and control-plane login remain
available; retain identity mappings and audit history. Do not delete mappings,
audit rows, backups, or prior releases as part of rollback.

## Independent read-only review prompt

Review the exact control-plane candidate and canonical `lenerp_core` commit for
Phase 03 only. Verify migration `20260920_0013_phase3_unified_identity`, hash-only
single-use codes, PKCE S256, exact tenant/membership/readiness/role checks,
allowlisted redirects and paths, host-scoped cookie separation, deterministic
JIT role reconciliation, break-glass preservation, rate limits, secret-safe
audits, direct and bidirectional navigation, staging flag-off defaults, and the
protected staging browser evidence. Do not infer Champion approval or production
SSO authorization from synthetic records.
