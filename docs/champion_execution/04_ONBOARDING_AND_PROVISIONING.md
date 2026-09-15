# Phase 4 — Onboarding and Provisioning

## Goal

Connect future-company onboarding, module selection, implementation state, tenant records, domains, and provisioning into a controlled workflow that cannot accidentally damage a live site.

## Build scope

1. Audit the existing organization, tenant, subscription/invoice, implementation, domain, onboarding service, job worker, and ERP integration paths; remove duplicate competing pathways only after compatibility coverage exists.
2. Define onboarding states: draft, submitted, under review, approved, provisioning, validation, ready, rejected, and cancelled.
3. Capture approved company, administrator, module bundle, branding, users, data-import needs, domain/infrastructure, and billing-contact fields.
4. Require explicit operator approval before any infrastructure/provisioning action.
5. Convert approved onboarding into one organization, implementation, tenant, module entitlement set, and provisioning job transactionally.
6. Replace synchronous/in-memory assumptions with durable queued execution and leases/locking appropriate to the existing worker model.
7. Make provisioning steps explicit and idempotent: reserve site name, create/register site, install pinned upstream apps, install LenERP app, apply modules/roles/workspaces/branding, bind domain/SSL, create admin, run health checks, mark ready.
8. Persist step status, attempts, sanitized logs, errors, timestamps, operator actions, and rollback state.
9. Add retry for safe steps and require operator confirmation for actions that may be irreversible.
10. Build operator pages for onboarding review, provisioning progress, failures, retry, rollback, domain/SSL, health, and first-login handoff.
11. Test a synthetic second company through the full path without Champion data.
12. Make public module selection create a versioned onboarding request. It must not directly grant entitlements, create a tenant, change DNS, or modify an ERP site.
13. Keep the contractually included reseller outcome—module showcase plus streamlined onboarding—separate from future per-client customization and any automation classified as Advisory or Needs Review.

## Acceptance tests

- Duplicate submission/idempotency key does not create duplicate organizations, tenants, invoices, or sites.
- Unapproved onboarding cannot provision.
- Invalid module bundle blocks before site mutation.
- Worker restart resumes or safely retries a durable job.
- Failure at each step leaves an actionable state and no false “ready.”
- Tenant/domain uniqueness and authorization are enforced.
- Synthetic tenant reaches first login with correct module bundle and no Champion data.
- Rollback/cleanup behavior is proven for a failed synthetic provisioning.
- A public applicant can revise or resubmit a module request without producing duplicate entitlements or infrastructure.
- No public request can bypass operator review or report an unverified module/site as ready.

## Deployment

Deploy the state model and read-only operator view first within the phase release candidate. Keep execution disabled until the production metadata checks pass. Enable execution only for the synthetic tenant; then retain manual approval for every real provisioning request.

## Gate

Phase 4 passes when a synthetic onboarding request reaches a healthy isolated tenant through durable, auditable, retry-safe steps and production remains unchanged for existing sites.
