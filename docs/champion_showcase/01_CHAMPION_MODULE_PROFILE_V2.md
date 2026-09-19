# Phase 01 — Champion Module Profile Version 2

## AI goal

Create a versioned Champion module proposal that preserves `champion-drilling@1` and adds HR, Payroll, Quality and Support with deterministic dependencies, truthful application states and clear role visibility.

## Required profile

`champion-drilling@2` must include the approved existing profile plus:

- `hr` — requires `hrms`;
- `payroll` — requires `hrms`, `hr` and `accounting`;
- `quality` — requires `stock`;
- `support` — requires `crm`.

Projects remains the backing capability for the Office Board. Manufacturing remains preserved and available because it is listed in the proposal, but it is hidden from Champion’s primary navigation until a use case is approved. Point of Sale remains unselected unless approved separately.

## Profile visibility classification

The catalog and daily-menu promise are separate. The following classification applies after entitlement, runtime verification, and the user’s ERP role are evaluated:

| Capability | Group | Champion classification | Gate or explanation |
|---|---|---|---|
| Accounting | Business | Role-only | ERPNext installed; accounting role required. |
| Buying | Business | Visible when verified | ERPNext installed; purchasing role required. |
| Selling | Business | Visible when verified | ERPNext installed; sales role required. |
| Stock | Operations | Visible when verified | ERPNext installed; stock role required. |
| Assets | Operations | Visible when verified | ERPNext installed; asset role required. |
| CRM | Business | Visible when verified | ERPNext installed; sales role required. |
| Projects | Business | Visible when verified | Backing capability for Office Board. |
| Field Operations | Operations | Visible when verified | ERPNext installed; dispatcher or field role required. |
| Well Mapping | Operations | Visible when verified | `lenerp_core` installed; field role required. |
| Drilling | Operations | Visible when verified | ERPNext/`lenerp_core` configuration and field role required. |
| Fleet | Operations | Visible when verified | ERPNext installed; fleet role required. |
| Reporting | Business | Role-only | ERPNext installed; reporting role required. |
| HR | People | Pending configuration and role-only | HRMS installed plus HR role/workspace/readback verification. |
| Payroll | People | Pending configuration and role-only | HRMS installed plus HR, accounting, payroll role/workspace/readback verification. |
| Quality | Operations | Visible when verified | ERPNext installed; quality role required. |
| Support | Business | Visible when verified | ERPNext installed; support role required. |

Manufacturing is preserved but hidden/preserved outside Champion navigation until a use case is approved. Point of Sale is intentionally excluded from both Champion bundles and remains unselected unless separately approved.

## Build scope

1. Add `champion-drilling@2` without mutating or deleting version 1.
2. Ensure catalog seeding is idempotent and does not rewrite historical bundle membership.
3. Add or update profile documentation to classify every proposal module as visible, role-only, hidden/preserved or pending configuration.
4. Update bundle preview so dependencies and backing applications are visible before apply.
5. Display why a module is not verified: missing app, pending provisioning, missing role configuration, failed readback or intentionally hidden.
6. Keep entitlement changes operator-authorized, auditable, idempotent and reversible.
7. Do not report HR or Payroll as applied merely because the bundle was selected.
8. Add a bundle comparison view or clear summary showing changes from version 1 to version 2.

## UX requirements

- Use human labels and short operational descriptions.
- Group modules into Business, Operations, People and Platform rather than one long technical list.
- Show dependency expansion before confirmation.
- Provide a visible distinction between “included in the purchased platform” and “configured for Champion’s daily menu.”
- Confirmation must name the organization, tenant, bundle version and applications that may need installation.
- A failed apply leaves the previous effective state understandable and recoverable.

## Acceptance tests

- Version 1 remains byte-for-byte semantically stable.
- Version 2 resolves all dependencies deterministically.
- Preview includes HRMS as required for HR/Payroll.
- Disabling HR while Payroll is selected is rejected without partial writes.
- Unauthorized and cross-organization mutations are denied.
- Reapplying the same request is idempotent.
- Audit records identify actor, organization, old/new bundle and effective modules.
- UI never equates entitlement with ERP verification.

## Non-goals

- Installing HRMS.
- Creating payroll rules or employee records.
- Making all modules visible to all users.

## Gate and rollback

Ship catalog/read behavior first, validate on a synthetic organization, then enable operator-only writes. Rollback selects the previous versioned bundle; do not delete version 2 records after use.

## Execution prompt

> Implement the immutable `champion-drilling@2` profile and its preview/apply UX. Preserve version 1, enforce dependencies, expose required applications, keep requested/entitled/applied/verified states separate, add authorization and idempotency tests, and stop before any ERP application installation or production entitlement change.
