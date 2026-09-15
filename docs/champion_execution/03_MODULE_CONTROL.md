# Phase 3 — Module Control

## Goal

Replace the static Modules page and placeholder entitlement service with persisted, authorized module administration for Champion and future companies.

## Current gap

- The `Module` and `OrganizationModule` tables already exist.
- `/modules` currently supports catalog reads only.
- `ModuleEntitlementService` raises `NotImplementedError`.
- The frontend Modules page uses a hardcoded six-item array rather than the backend catalog.
- Dependencies, bundles, compatibility, effective entitlements, audit history, and ERP-application status are not complete.

## Build scope

1. Define stable catalog entries for Accounting, Buying, Selling, Stock, Assets, HR, Payroll, Manufacturing, CRM, Quality, Projects, Support, Well Mapping, and approved supporting modules.
2. Add backward-compatible metadata for category, description, active state, dependency rules, incompatibilities, required app/version, default roles/workspaces, configuration schema, and display order.
3. Implement the entitlement service to resolve plan defaults, implementation-template defaults, organization overrides, dependencies, and disabled/unavailable states.
4. Add authorized APIs to read the catalog, preview a change, enable/disable organization modules, read effective entitlements, and inspect audit history.
5. Make every change transactional and idempotent; reject invalid dependency/incompatibility states before persistence.
6. Record actor, organization, old state, new state, reason, and timestamp in the audit log.
7. Build the Modules UI with catalog/list views, search/filter, module detail, status/dependency explanation, organization assignment, bundle preview, confirmation, and result feedback.
8. Add a company-level Modules tab showing effective modules, source of entitlement, configuration state, and pending ERP application work.
9. Separate “entitled in control plane” from “applied and verified on ERP site.” Never report ready until ERP verification succeeds.
10. Create default bundles such as Champion Drilling and Generic Field Service without making future-company customization automatic.
11. Use one authoritative catalog and stable keys for the public reseller showcase, onboarding selection, internal entitlement administrator, provisioning worker, and ERP verification.
12. Represent module state explicitly as `marketed`, `requested`, `entitled`, `applied`, and `verified`; do not collapse these into one enabled flag.
13. Create the initial Champion module profile as package C03. Classify each included module as Champion-enabled, administrator-only, hidden/preserved, or pending configuration without removing it from the delivered platform.

## Acceptance tests

- Catalog matches every promised current module.
- Authorized operator can preview and apply a valid bundle.
- Dependency enable/disable behavior is deterministic.
- Invalid/incompatible selection is rejected without partial writes.
- Unauthorized user cannot change entitlements.
- Audit history shows exact before/after state.
- Retry of the same request does not duplicate assignments.
- Existing organizations with no explicit assignments receive the documented safe default.
- UI reports control-plane and ERP-site state separately.
- Public/reseller module descriptions and internal entitlements resolve to the same stable catalog entries.
- Champion's module profile preserves every included current platform module while exposing only approved modules to each role.

## Deployment

Release additively:

1. Deploy schema/catalog/read APIs with writes disabled.
2. Validate catalog and existing-organization defaults in production.
3. Enable writes for the operator account only.
4. Apply a non-production/synthetic organization bundle and verify audit/rollback.
5. Enable generally only after the synthetic test passes.

## Gate

Phase 3 passes when module decisions are persisted, dependency-safe, authorized, auditable, reversible, and visible in production without claiming unverified ERP activation.
