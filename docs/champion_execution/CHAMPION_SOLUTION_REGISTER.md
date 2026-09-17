# Champion Solution Package Register

## Purpose

Champion-specific modules, pages, workflows, configuration, reports, and forms are tracked as packages so they can enter the release stream when their requirements become available. They are not postponed into one large late release and are not silently added to an unrelated platform phase.

## Package register

| ID | Package | Minimum inputs | Typical dependencies | Initial pre-data work | Final acceptance evidence |
|---|---|---|---|---|---|
| C01 | Company, product name, and branding | Legal/company settings, timezone, currency, fiscal year, approved product/brand assets | Phase 0 | Settings templates and replaceable assets | Approved company settings and branded production surfaces |
| C02 | Users, roles, and permissions | User list, role matrix, confidential-data rules, approval limits | Phase 0; Phase 1 for polished navigation | Role fixtures, synthetic users, negative authorization tests | Each approved role completes allowed actions and is denied restricted actions |
| C03 | Champion module profile and navigation | Enabled/admin-only/hidden module decisions and dependency approval | Phase 3 for entitlement truth | Draft Champion bundle and role workspaces | PLAT-P3 catalog and synthetic entitlement-control evidence complete; effective Champion bundle application/ERP verification remains unresolved until approved decisions and data exist |
| C04 | Customer, Site/Well, and Well Mapping | Identifiers, required fields, GPS/location rules, completion-record requirements | Phase 0 custom app | DocType/schema scaffold and synthetic wells | Required well data saves, links, searches, reports, and exports correctly |
| C05 | Drilling and service job workflow | Job types, states, transitions, assignments, completion/reopen rules, office/field responsibilities | C02, C04 | Synthetic end-to-end workflow | Approved customer-to-well-to-job-to-completion scenario passes |
| C06 | Inventory, purchasing, trucks, rigs, and assets | Warehouses/vehicles, items/UOM, stock-use rules, purchasing, maintenance requirements | C02, C05 and ERP Stock/Buying/Assets | Synthetic locations/items/assets | Approved stock, purchasing, assignment, and maintenance scenarios pass |
| C07 | CRM, quoting, invoicing, payments, and accounting | Lead/customer flow, quote approval, chart of accounts, taxes, payment terms, opening balances | C02, C05 and Selling/Accounting | Document links and synthetic commercial flow | Approved quote-to-job-to-invoice/payment controls and totals pass |
| C08 | Dashboards, reports, alerts, forms, and print formats | KPIs, report samples, alerts, signatures/photos/forms, audience and delivery format | Relevant C04–C07 packages | Reusable layouts and synthetic examples | Approved outputs match source rules and role visibility |

The register is the initial decomposition. Add a new package only when a requirement cannot be safely accepted within an existing package. New modules or materially new features must also receive the required commercial classification and written approval.

## Package record template

Copy this section for each implementation/release of a package.

### Identity

- Package ID:
- Package name:
- Commercial classification: Included / Advisory / Needs Review / Deferred
- Requirement owner:
- Acceptance authority:
- Target release:
- Current state:
- Feature flag:

### Inputs and dependencies

- Approved decisions:
- Required data/source samples:
- Platform phase dependencies:
- Module/app/version dependencies:
- Related package IDs:
- Domain/environment dependencies:

### Scope

- Included behavior:
- Pages/routes/DocTypes affected:
- Roles and permissions affected:
- APIs/jobs/integrations affected:
- Data/schema impact:
- Explicit exclusions:

### Acceptance and recovery

- Representative success scenario:
- Authorization failure scenario:
- Validation failure scenario:
- Retry/idempotency scenario, when relevant:
- Existing behavior regression tests:
- Code rollback:
- Data correction/recovery:
- Evidence location:
- Champion acceptance date/actor:

## Rules

- A package may be split into multiple releases while keeping one acceptance outcome.
- A synthetic implementation does not close requirements that depend on Champion data or approval.
- Hiding a workspace is not authorization; permissions are tested by direct UI route and API access.
- Selected modules remain distinct from installed modules. `marketed`, `requested`, `entitled`, `applied`, and `verified` states must be visible where relevant.
- Unselected included platform modules remain installed/preserved or administrator-accessible according to the approved module matrix; they are not deleted from the delivered platform.
- Every package is reproducible through the custom app, fixtures, patches, import scripts, or documented configuration automation. Undocumented production-only edits do not satisfy delivery.
