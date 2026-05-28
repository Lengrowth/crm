# 24 — Production Security, Authorization, and Billing Integrity

**Project:** SaaS-first ERPNext control platform  
**Audience:** backend developers, frontend developers, operators, and technical founders  
**Status:** production hardening gate  
**Last updated:** 2026-05-28

---

## 1. Purpose

This phase closes the remaining production-risk gaps before a real client is onboarded.

It does **not** introduce a new product surface or duplicate existing auth, billing, or email logic.
It hardens the current frontend and backend so the live path is safe to operate.

---

## 2. What already exists in the repo

### Frontend

- A real auth route group already exists under `frontend/app/(auth)/login`.
- The current auth screen supports both sign in and create account in one place.
- Frontend auth helpers already exist in `frontend/lib/auth.ts` and `frontend/lib/auth-api.ts`.
- The app shell and route scaffolding already exist; this phase should reuse them instead of creating duplicate screens.

### Backend

- Auth endpoints already exist at `/auth/register`, `/auth/login`, `/auth/logout`, and `/auth/me`.
- Session and membership models already exist.
- Authorization helpers already exist, including `require_platform_admin` and `require_organization_role`.
- Billing service and provider abstractions already exist.
- The communication service already uses the Resend HTTP API for outbound email.

### Configuration

- Resend settings already exist in backend config: `resend_api_key`, `resend_from_email`, and `marketing_contact_recipient`.
- Billing provider selection already exists through the provider abstraction.

### Important note

- There is **not** a separate password-reset or invitation screen visible in the current frontend tree.
- The current auth UI is a combined login/register screen, which is the correct place to reuse rather than duplicate logic.

---

## 3. Why this phase matters

A SaaS platform can appear complete while still being unsafe to operate.

The current repository already has the core building blocks, but production readiness still depends on enforcing the right boundaries:

- only the correct users can mutate tenant, billing, and integration state
- billing state must not silently diverge from provider truth
- outbound email must use the real Resend path
- privileged actions must be auditable
- live flows must fail closed instead of falling back to mock or placeholder behavior

---

## 4. Scope

### In scope

- route-level authorization for all mutable control-plane endpoints
- organization and tenant membership enforcement at the API boundary
- production billing enforcement with no silent mock fallback
- webhook verification and replay resistance
- session revocation and account lifecycle review
- secure recovery and invitation flows if they are required for onboarding
- audit logging for dangerous or billing-related actions
- negative-path tests for permission, billing, and webhook misuse

### Out of scope

- ERPNext site automation
- custom-domain DNS/SSL automation
- frontend redesign work
- duplicate auth screens or duplicate billing logic
- placeholder implementations
- feature expansion beyond security and integrity

---

## 5. Key repository risks this phase addresses

### 5.1 Billing routes must be strictly controlled

Billing mutation paths are sensitive and must be protected at the router boundary, not only inside service methods.

### 5.2 Tenant and integration mutations must stay scoped

Tenant lifecycle, domain activation, and integration mapping should never be reachable by an unscoped authenticated user.

### 5.3 Account recovery must be real if it is required

If onboarding requires password reset or invitations, those flows must be implemented end to end rather than represented with placeholders.

### 5.4 Production billing must not rely on mock behavior

Mock billing remains useful for tests and local work, but live environments must not silently use it.

### 5.5 Resend should be the single outbound email path

The repo already has a Resend-backed communication service, so production should reuse that path instead of adding a second email implementation.

---

## 6. Deliverables

- Every billing mutation endpoint requires explicit authorization.
- Every tenant mutation endpoint requires explicit authorization.
- Every integration mutation endpoint requires explicit authorization.
- Billing webhook verification is implemented and enforced.
- Recovery and invitation flows are real if they are needed for onboarding.
- Session revocation and lifecycle policies are documented and enforced.
- Audit records exist for privileged state transitions.
- Security-focused tests cover both allowed and denied cases.
- Production email flows use Resend, not placeholders or mock transport.

---

## 7. Exit criteria

This phase is complete only when all of the following are true:

- no unauthenticated write route exists on the production control plane
- no mutable route relies only on service-layer trust without scoped auth checks
- billing webhooks cannot be forged without detection
- production billing does not silently fall back to mock behavior
- real user recovery exists wherever onboarding requires it
- privileged actions are auditable and reviewable
- outbound email uses the production Resend path
- security tests pass in CI

---

## 8. Validation / test plan

- route-level authorization tests for billing, tenants, domains, provisioning, and integrations
- webhook verification tests
- recovery-flow tests if reset or invitation flows are implemented
- negative tests for unauthorized access
- production-config tests that prove mock fallback is blocked
- email-path tests that prove Resend is used for outbound mail

---

## 9. Dependencies

- existing auth/session tables
- control-plane membership model
- audit logging
- billing provider abstraction
- Resend environment variables and secret references
- deployment configuration for production secrets

---

## 10. Recommended implementation order

1. Protect mutable routes.
2. Enforce production billing provider selection and webhook verification.
3. Reuse the existing Resend email path for any production email flows.
4. Add recovery and lifecycle flows only where the product requires them.
5. Extend audit logging.
6. Add tests that prove denial as well as success.

---

## 11. Why this phase must precede onboarding

Without this phase, the platform could allow the wrong user to mutate client data, process billing in an unsafe way, or leave a customer unable to recover access.

That is not launch-safe.
