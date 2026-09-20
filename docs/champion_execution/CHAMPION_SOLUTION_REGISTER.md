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
| C09 | Office work, people, payroll, quality, and support | Office task states, user/manager matrix, HR/payroll confidentiality and rules, callback/quality classifications, support routing | C02, C03, C05, C07, C08; pinned HRMS v15.64.1 | Synthetic Office Board, employees/time-off/timesheets/payroll preview, callbacks and support/product-change requests | One-login role journeys pass; confidential data is denied; installed apps and module states reconcile |

The register is the initial decomposition. Add a new package only when a requirement cannot be safely accepted within an existing package. New modules or materially new features must also receive the required commercial classification and written approval.

## Phase 5 package release mapping

| Package | Release identity | Current state | Evidence/next gate |
|---|---|---|---|
| C01 | `CHAMP-C01-R1` | `in_development` | Configurable branding boundary implemented; approved Champion values and staging evidence remain pending |
| C02 | `CHAMP-C02-R1` | `in_development` | Synthetic role profiles and negative-permission boundary implemented; approved user/approval matrix remains pending |
| C03 | `CHAMP-C03-R1` | `in_development` | Champion ERP workspace and standard module profile implemented for synthetic staging; approved module matrix remains pending |
| C04 | `CHAMP-C04-R1` | `in_development` | Persisted Well Site schema, links, coordinates, validation, and permissions implemented; approved identifiers/rules remain pending |
| C05 | `CHAMP-C05-R1` | `in_development` | Persisted job workflow, assignment, lifecycle states, completion validation, and print format implemented; approved process remains pending |
| C06 | `CHAMP-C06-R1` | `in_development` | Standard ERPNext inventory/buying/assets seed path implemented; approved stock and maintenance rules remain pending |
| C07 | `CHAMP-C07-R1` | `in_development` | Synthetic lead-to-payment seed path implemented; chart, tax, payment, and approval decisions remain pending |
| C08 | `CHAMP-C08-R1` | `in_development` | Persisted operations dashboard/API now includes inventory exceptions, asset/maintenance status, well history, and alerts; approved KPI/audience/alert definitions remain pending |
| C09 | `CHAMP-C09-R1` | `phase02_pass_phase03_permitted` | Phase 02 HRMS pin, resolver, durable install/migrate/readback, truthful states, and tests passed in protected staging run `35506309957`; Champion acceptance and production promotion remain unclaimed |

Each identity is independently reviewable. A later revision such as
`CHAMP-C04-R2` is required when approved requirements or accepted behavior
change; no `PLAT-P5` identity exists.

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

## Final Champion pre-kickoff remediation evidence

The next protected staging candidate binds the CRM source, the immutable LenERP Core app `a7e47208baf6583295f5f2632f4787262cd3f475`, and the remediation documentation snapshot. The protected artifact must execute the candidate-bound build, expanded C08 dashboard evidence, ERP accessibility review, full customer-facing language audit, synthetic role/readback checks, and cleanup. Champion acceptance, real-data migration, and production activation remain pending.

Detailed hashes, artifact digest, and review disposition are recorded in [FINAL_REMEDIATION_EVIDENCE.md](FINAL_REMEDIATION_EVIDENCE.md).
