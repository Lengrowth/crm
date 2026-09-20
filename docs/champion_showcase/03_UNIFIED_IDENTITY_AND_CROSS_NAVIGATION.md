# Phase 03 — Unified Identity and Cross-Navigation

## AI goal

Provide one sign-in experience across the LenERP control plane and the authorized Champion ERP site, plus safe bidirectional navigation, without sharing passwords or application session cookies.

## Identity design

The control plane is the authorization server and membership authority. The ERP site is a relying application.

1. ERP initiates or receives an authorization request with tenant, allowlisted return path, state and PKCE challenge.
2. An unauthenticated user signs in through the existing control-plane login.
3. The control plane validates active user, verified email, organization membership, tenant access, tenant health and approved ERP role profile.
4. It issues a short-lived, single-use authorization code containing no password or reusable session token.
5. ERP exchanges the code over a server-to-server TLS call, validates issuer/audience/tenant/state/expiry/PKCE and consumes it once.
6. ERP creates or updates the mapped Frappe user only within the approved just-in-time provisioning policy, applies approved roles and creates a normal Frappe session.
7. The user lands on an allowlisted ERP route.

Use established OAuth 2.1/OIDC libraries or Frappe-supported provider/client mechanisms where they satisfy the contract. Do not invent reusable bearer tokens in URLs. If a standards-compliant control-plane authorization server is not feasible in the phase, implement only a clearly isolated temporary broker with the same single-use, PKCE, audience and replay protections and document its replacement gate.

## Build scope

- Authorization request, approval/session reuse, code exchange and replay protection.
- Persistent mapping between control-plane user, organization, tenant, ERP user and role-profile version.
- Explicit just-in-time user provisioning policy; inactive or removed memberships are denied and reconciled.
- `Open ERP` on the control-plane tenant/organization context.
- `LenERP Control Plane` in the ERP user dropdown, linked to the authorized organization/tenant route.
- Direct ERP visit redirect to the control-plane sign-in and return.
- Central-session revocation and documented ERP-session revocation behavior.
- Break-glass local ERP administrator, excluded from SSO automation and protected/audited separately.
- Strict redirect allowlists, CSRF/state checks, PKCE, short expiry, one-time consumption, rate limiting and secret-safe logs.

## UX requirements

- No second password prompt when a valid central session and membership exist.
- Cross-navigation actions display destination, organization and environment.
- New-tab behavior is deliberate and consistent; preserve the user’s task context.
- Access denial explains whether membership, tenant readiness or role assignment is missing without leaking another tenant’s existence.
- Provider outage offers safe retry and administrator contact; it never falls back to an insecure shared password.
- Mobile redirects return to a usable route without loops.

## Acceptance tests

- Control-plane login opens the correct ERP tenant and landing page.
- Direct ERP visit completes the same flow.
- ERP returns to the matching control-plane tenant.
- Code replay, expired code, modified state, wrong audience, wrong tenant and unapproved redirect are denied.
- A user from another organization cannot access Champion ERP.
- Platform-admin status alone grants no ERP access.
- Membership removal prevents new ERP sessions and follows the documented existing-session revocation policy.
- Role updates are deterministic and never remove the break-glass administrator.
- Cookies remain host-scoped and are not reused across frameworks.

## Non-goals

- Social login providers unless separately approved.
- Sharing database tables or password hashes.
- Allowing one tenant’s ERP session to open another tenant.

## Gate and rollback

Deploy behind server-controlled flags for an isolated synthetic tenant. Preserve the normal ERP login for the break-glass account. Rollback disables the SSO entry points and returns to independent logins without deleting user mappings or audit records.

## Execution prompt

> Implement the unified identity flow in this document using a standards-based authorization-code design, PKCE, single-use codes, exact tenant membership, explicit role mapping and host-scoped sessions. Add bidirectional navigation and complete denial/replay tests. Stage behind flags, preserve break-glass access, expose no secrets, and do not make production SSO authoritative before protected evidence and human approval.
