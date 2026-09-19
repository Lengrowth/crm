# Phase 00 — Program Baseline and UX Contract

## AI goal

Establish the exact current module, application, identity, workspace and route baseline; convert the intended one-product experience into testable UX and security contracts before feature implementation begins.

## Starting facts to verify

- The control plane has local email/password sessions and organization memberships.
- Frappe maintains a separate ERP session.
- The inspected release/runtime contract declares Frappe, ERPNext and `lenerp_core`; live production/staging installed-app state was inaccessible, and HRMS is not a verified installed dependency.
- The catalog contains HR, Payroll, Quality and Support, while `champion-drilling@1` excludes them.
- The current Champion ERP workspace exposes Wells, Jobs, Operations Summary and selected standard ERP links.
- Existing public Champion/Vercel pages are prototypes and sources for workflow discovery, not automatically trusted identity or data boundaries.

If runtime evidence contradicts these facts, record the discrepancy and update the plan before implementation.

## Build scope

1. Inventory control-plane routes, authentication/session behavior, organization memberships, tenant records, catalog entries, bundles and module-application states.
2. Inventory staging ERP installed apps, workspaces, roles, custom DocTypes, standard module routes and custom-app revision.
3. Record the current cross-origin/domain, cookie, CSRF, CORS and redirect boundaries without printing secrets.
4. Define the canonical user journeys:
   - sign in to the control plane and open Champion ERP;
   - open ERP directly and authenticate through the control plane;
   - return from ERP to the matching control-plane tenant;
   - deny an authenticated user who lacks tenant/ERP membership;
   - use a break-glass local ERP administrator during identity-provider failure.
5. Produce the role/navigation matrix for Administrator, Office/Dispatcher, Sales, Accounting, Inventory, Field, HR, Payroll, Quality, Support and Read-only users.
6. Define the module-showcase record and action for every proposal module.
7. Define responsive breakpoints and the core shell states: loading, empty, partial, error, access denied, provider unavailable and synthetic-data notice.
8. Create a decision register for unresolved domain, product-name, final role and module-visibility decisions. Do not invent Matt’s answers.

## UX deliverables

- Navigation map for the control plane and ERP.
- Role-to-workspace matrix.
- Module-to-representative-workflow matrix.
- Annotated control-plane tenant header containing `Open ERP`, ERP status and environment.
- Annotated ERP user menu containing `LenERP Control Plane` and the active organization.
- Shared status vocabulary: Available, Selected, Entitled, Applying, Applied, Verified, Needs attention.
- Copy rules that distinguish synthetic demonstration, configured capability and accepted production workflow.

## Acceptance tests

- Every promised module has one owner, backing app, route/workspace, role audience and representative workflow.
- No planned route depends on a shared password, cross-application cookie reuse or an open redirect.
- The identity sequence documents success, expired code, replay, wrong tenant, inactive user, provider outage and recovery behavior.
- Mobile and keyboard flows can reach both cross-navigation actions.
- The baseline records exact installed apps and commits without exposing secrets.
- Existing public prototype pages are classified as Keep temporarily, Replace, Merge or Retire; unknown decisions remain explicitly pending.

## Non-goals

- Installing HRMS.
- Creating SSO endpoints.
- Changing production navigation.
- Loading real Champion data.

## Gate and rollback

This documentation-only phase passes when the matrices and contracts are reviewed against the repositories and staging inventory. Rollback is removal of unapproved documentation changes; no runtime state changes are allowed.

## Execution prompt

> Audit the current LenERP control plane, ERP staging site and `lenerp_core` application. Produce the Phase 00 module, role, route, identity and UX baseline described in this document. Treat all existing records as evidence, preserve unrelated changes, expose no secrets, make no production mutation, and do not proceed to implementation while an identity or module ownership boundary is ambiguous.

---

## Verified Phase 00 baseline — 2026-09-19

### Result and evidence boundary

**Phase 00 result: PASS as a documentation baseline.** The repository and static staging contract were inspected, the required matrices and UX/security contracts are recorded below, and no runtime or production mutation was performed. **Phase 01 entry is BLOCKED** by the unresolved items in [Blockers and Phase 01 prerequisites](#blockers-and-phase-01-prerequisites).

This is not Champion approval, production readiness, an identity cutover, or proof that the staging site is currently reachable. Runtime facts are marked `verified`, `declared`, `not observed`, or `inaccessible` rather than inferred.

Evidence inspected:

- Control plane: `backend/app`, `frontend/app`, `frontend/components`, `frontend/lib`, `backend/alembic`, `ops/staging`, `ops/production/release-runtime-baseline.json`, and the control-plane release history at `30194dd`.
- Governing documents: [`champion_execution/README.md`](../champion_execution/README.md), [`PROGRAM_AND_RELEASE_MODEL.md`](../champion_execution/PROGRAM_AND_RELEASE_MODEL.md), [`PHASE_DEPLOYMENT_GATE.md`](../champion_execution/PHASE_DEPLOYMENT_GATE.md), [`03_MODULE_CONTROL.md`](../champion_execution/03_MODULE_CONTROL.md), [`04_ONBOARDING_AND_PROVISIONING.md`](../champion_execution/04_ONBOARDING_AND_PROVISIONING.md), [`05_ERP_UX_AND_DRILLING_PAGES.md`](../champion_execution/05_ERP_UX_AND_DRILLING_PAGES.md), and [`CHAMPION_SOLUTION_REGISTER.md`](../champion_execution/CHAMPION_SOLUTION_REGISTER.md).
- Sibling Frappe app: `C:\Users\smikl\Desktop\Work\lenerp_core`, clean working tree, local `HEAD` `fd18845527039619538ab9906cb8197c83e053b1`; the staging-embedded source and runtime baseline are pinned to `a7e47208baf6583295f5f2632f4787262cd3f475`.
- Existing Vercel/proposal workspace: `C:\Users\smikl\Desktop\Work\champion-forecast`, clean working tree, including [`docs/PRE_KICKOFF_DEMO_BOUNDARY.md`](../../../champion-forecast/docs/PRE_KICKOFF_DEMO_BOUNDARY.md) and its App Router pages.

Runtime checks from this workstation were read-only. TCP checks found no listener on local control-plane ports `8000`/`3000`, staging control-plane ports `18001`/`13001`, or the documented staging ERP port `28000`. The staging host, its `/opt` filesystem, systemd services, bench, site database, and installed-app list were therefore inaccessible. No `bench`, `curl`, login, write API, install, migrate, seed, reset, DNS, or production command was run.

### Control-plane inventory

#### Authentication and authorization

| Area | Verified repository behavior | Phase 00 implication |
|---|---|---|
| Sign-in | `POST /auth/login` validates the local user and returns an opaque session token. Password hashes use PBKDF2; sessions are persisted as hashed tokens with expiry/revocation fields. | This is a control-plane-local session, not an ERP/Frappe session. |
| Browser storage | The Next.js frontend stores the token in the configurable `crm-auth-token` cookie. It is readable by browser JavaScript; default path is `/`, default `SameSite=Lax`, production default `Secure`, default max age 30 days. | Do not reuse this cookie on the ERP host. A future handoff must use a short-lived one-time code. |
| API authentication | Frontend API calls copy the token into an `Authorization: Bearer` header. Backend dependencies resolve the session, active user, and current organization/tenant access. | Middleware presence checks are not authorization; `/auth/me` remains the validity check. |
| Membership | `OrganizationMembership` links user, organization, and role. Organization/tenant services enforce membership; platform admin can access control-plane administration but is not intended to imply ERP access. | ERP access requires an explicit organization membership and ERP role profile. |
| Organization writes | Organization and tenant mutation routes use control-plane write-access checks. Module writes additionally require feature flags and owner/admin/implementation-manager or platform-admin rules. | Entitlement administration is separate from ERP application state. |
| Session expiry/logout | Backend sessions carry expiry and revocation; logout revokes the current session. Frontend clears the cookie after failed `/auth/me` or sign-out. | Expired central sessions must not silently create or retain an ERP session. |
| Password/email recovery | Password reset and email-verification token flows exist as local control-plane features. | They are not an SSO protocol and must not be used as an ERP credential bridge. |

#### Organizations, tenants, catalog, bundles, entitlements, and application state

The control plane has persisted models for `Organization`, `OrganizationMembership`, `Tenant`, `Module`, `OrganizationModule`, `ModuleBundle`, `ModuleBundleItem`, `ModuleEntitlementRequest`, `ModuleEntitlementAudit`, and `ModuleApplicationStatus`. Tenant records carry environment, lifecycle, ERP site name/base URL, credential references, and provisioning status. Secrets themselves are not part of this evidence.

The seeded catalog currently contains 21 rows: Accounting, Buying, Selling, Stock, Assets, HR, Payroll, Manufacturing, CRM, Quality, Projects, Support, Well Mapping, Field Operations, Drilling, Fleet, Reporting, White Label, Custom Domain, Point of Sale, and the non-marketed legacy Inventory alias. Dependencies and required applications are encoded in `backend/app/db/seed.py`; HR and Payroll require `hrms`, Payroll also requires Accounting, Quality requires Stock, Support requires CRM, and Well Mapping requires Field Operations plus `lenerp_core`.

The only seeded bundles are:

- `champion-drilling@1`: Accounting, Buying, Selling, Stock, Assets, CRM, Projects, Field Operations, Well Mapping, Drilling, Fleet, and Reporting.
- `generic-field-service@1`: CRM, Selling, Stock, Assets, Projects, Field Operations, Fleet, and Reporting.

`champion-drilling@2` is required by the showcase plan but is not present in the inspected seed. Phase 01 must add it immutably; it must not rewrite `@1`.

The current entitlement resolver distinguishes inherited plan/template defaults, bundle selection, explicit organization overrides, dependencies, audit history, and idempotent replay. It separates `requested`/`entitled` from ERP `application_state` and `verification_state`. ERP application status is written by the durable provisioning worker after provider readback; a catalog selection alone is not proof of application. The code does not yet expose a complete showcase vocabulary for `hidden` and `needs-attention`; those are defined as UI/status-contract terms below and must be mapped without collapsing the persisted distinctions.

#### Control-plane routes and feature flags

| Surface | Current routes or behavior | Current status |
|---|---|---|
| Auth | `/auth/register`, `/auth/login`, `/auth/me`, `/auth/logout`, password reset, email verification | Implemented local auth; no authorization-code/PKCE exchange route. |
| Health/release | `/health`, `/runtime/release` | Implemented; runtime endpoint returns safe manifest metadata and server feature flags only. Live readback was inaccessible. |
| Organizations/tenants | `/organizations`, `/organizations/{id}`, organization tenants, `/tenants`, tenant detail/update/suspend/reactivate | Implemented control-plane records and access checks. No ERP handoff action is present in the inspected frontend. |
| Catalog | `/modules`, `/catalog/modules`, `/public/modules`, `/module-bundles`, `/plans`, `/implementation-templates` | Catalog and bundle reads exist; public catalog is not an entitlement. |
| Entitlements | organization modules read, preview, apply, reverse, audit | Implemented with dependency validation, preview hash, idempotency, and feature-gated writes. It does not itself install or verify ERP apps. |
| Onboarding | public request create/read/revise/submit; operator review/approve/reject/cancel/convert; execution authorization; job detail/events/retry | Durable workflow exists. Staging example flags keep public intake, operator view, conversion, execution, and real execution off by default. |
| Provisioning | durable steps include validation, isolated site creation, pinned ERPNext, `lenerp_core`, modules, roles/workspaces, branding, domain/SSL, admin handoff, health, verification, first login, ready | Synthetic-only execution is policy-gated. The worker installs `erpnext` and `lenerp_core`; it has no HRMS installation step yet. |
| ERP integration | runtime summary plus legacy mapping/site-status/backup/restore/domain APIs | Runtime modes are `mock`, `bench`, `live`, and `disabled`; local defaults to mock, staging bench requires explicit staging configuration, and production-like defaults to disabled unless intentionally configured. Legacy mutations are separately feature-gated. |
| Frontend navigation | `/app`, organizations, tenants, modules, onboarding, implementation, settings | Current operator shell is control-plane oriented. There is no tenant-context `Open ERP` action. |

The checked-in staging example has `platform_phase1_shell`, `onboarding_public_intake`, `onboarding_operator_view`, `onboarding_conversion`, `onboarding_execution`, `onboarding_synthetic_allowlist`, and `onboarding_real_execution` flags. Their example values leave them off. Module-write flags and live runtime values were not observed from a running environment; do not infer their deployment state from source defaults.

### ERP and `lenerp_core` inventory

#### Application and release assumptions

The sibling app is a private Frappe custom application boundary, version `0.2.0`, intended to be installed beside pinned Frappe and ERPNext. Its hooks install reusable Champion roles, workflow metadata, a completion print format, and standard ERPNext permission rows; demo data is opt-in through `lenerp_core.demo_seed.seed`. It contains no HRMS dependency in `pyproject.toml`, `hooks.py`, `install.py`, or the staged archive.

The local sibling repository is clean at `fd18845`. The staged embedded copy and release runtime baseline identify `a7e47208` and Frappe/ERPNext revisions `edae775...` and `945e825...`; the exact runtime baseline file lists only `frappe`, `erpnext`, and `lenerp_core`. This is a declared artifact record, not a live installed-app readback. The tracked `ops/staging/lenerp_core` snapshot also contains duplicate top-level/nested package paths and differs from the current sibling source; Phase 01 must reconcile packaging before using it as evidence.

#### Custom DocTypes, workflow, routes, fixtures, and menus

| Capability | Current evidence | Current readiness |
|---|---|---|
| Well/site | `LenERP Well Site`: Customer and Contact links, status, address/location, latitude/longitude, depth, pump specification, notes; validation rejects invalid coordinates and negative depth. | Persisted code and permissions exist in the sibling app; final Champion fields and rules remain open. |
| Drilling job | `LenERP Drilling Job`: Customer, Well Site, job type/status/workflow, date, personnel text, rig/truck Assets, priority, child materials, notes, completion. Validation requires completion details for completed jobs and sane dates. | Persisted code and synthetic workflow foundation exist; assignment and final process remain open. |
| Job material | `LenERP Job Material` child table links item, description, quantity, UOM, and issuing warehouse. | Schema exists; a child row must not be represented as posted stock movement. |
| Branding boundary | `LenERP Branding Settings`, System Manager only, value-free configuration boundary. | No approved Champion values or final branding. |
| Workspace | `Champion ERP` workspace is restricted to six Champion roles and links Well sites, Drilling jobs, Operations Summary, Customers, Quotes, Invoices, and Equipment. | Useful current foundation; not yet the complete role-based module shell. |
| Report | `Champion Operations Summary` script report, limited to four roles, reads synthetic `DEMO-*` drilling jobs. | Current synthetic report exists; production-intended provenance and broader module reporting need Phase 07. |
| Workflow | `Champion Drilling Job`: Planned → Scheduled → In Progress → Completed, with Reopened; Dispatcher and Field Technician transitions are defined by install hooks. | Current synthetic workflow metadata; not Champion-approved. |
| Print | `Champion Job Completion` print format includes customer, well/site, crew, notes, completion, and an explicit synthetic notice. | Current synthetic evidence; branding and final fields pending. |
| Demo API | `lenerp_core.api.demo_status` and `dashboard_summary` are role-gated and label output synthetic. Current sibling `HEAD` includes persisted jobs, wells, invoices, inventory exceptions, assets, maintenance, well history, and alerts. | Code exists locally; staging artifact must be reconciled before it can be treated as current evidence. |
| Demo seed/reset | `demo_seed.seed`, `status`, and `reset` use `DEMO-`-scoped records and are explicitly invoked. | Safe boundary is documented; no seed/reset was run in this phase. |
| Fixtures/menus | No Champion fixture directory or custom route map was found. Frappe workspace JSON, hooks, install hooks, report JSON, and standard Frappe routes are the current menu mechanism. | Custom menu expansion is a Phase 04 concern. |

#### Installed-app verification matrix

| Environment | Evidence inspected | HRMS state |
|---|---|---|
| Local control plane | Python/Next source only; no local runtime listener on ports 8000/3000 | Not applicable to the ERP, and no local ERP bench was available. |
| Local `lenerp_core` sibling | Standalone source repository; no Frappe site or `bench` executable available on this workstation | **Unknown/inaccessible**, not verified installed. |
| Isolated staging lane | Static contract defines `/opt/frappe-staging-bench`, site `erp-staging.example.test`, port 28000, and `bench list-apps`; all local staging ports were closed and the remote host/filesystem was inaccessible | **Unknown at runtime**. Static provisioning installs only Frappe/ERPNext plus `lenerp_core`; HRMS is not present in the staged source or worker install sequence. |
| Declared production baseline | `ops/production/release-runtime-baseline.json` lists Frappe, ERPNext, and `lenerp_core` only | **Not declared installed**; this is not a live readback and production was not contacted. |

No claim that HRMS is installed may be made until an authorized, read-only staging `bench --site <site> list-apps --format json` readback records the exact app/version. No HRMS installation is part of Phase 00.

### Module ownership and representative-workflow matrix

Readiness uses the state vocabulary in this document. `Catalog only` means a control-plane row exists but no ERP application/readback proves the workflow. `Synthetic foundation` means current local `lenerp_core` code or demo seed can represent a limited scenario; it is not acceptance.

| Module / Champion language | Owner/package | Backing application | Intended route/workspace | Permitted showcase roles | Representative synthetic workflow | Honest readiness |
|---|---|---|---|---|---|---|
| Accounting | LenERP platform / C07 | ERPNext Accounting | Accounting; invoices and payments | Administrator, Accounting | Quote → invoice → payment review | Catalog + seeded synthetic records; ERP runtime not read back. |
| Buying | C06/C07 | ERPNext Buying | Inventory & Purchasing | Administrator, Inventory, Accounting | Supplier → purchase receipt → stock availability | Catalog/bundle only; runtime not verified. |
| Selling | C07 | ERPNext Selling | Customers & Sales | Administrator, Sales, Accounting | Opportunity → quotation → invoice | Catalog/bundle only; runtime not verified. |
| Stock | C06 | ERPNext Stock | Inventory & Purchasing | Administrator, Inventory, Dispatcher | Receive item → issue material to a job | Catalog/bundle only; no claim that a child material row posts stock. |
| Assets / equipment | C06 | ERPNext Assets plus `lenerp_core` links | Trucks & Equipment | Administrator, Inventory, Field | Assign rig/truck → review maintenance attention | Catalog/bundle; local synthetic API evidence, staging artifact mismatch. |
| CRM | C07 | ERPNext CRM | Customers & Sales | Administrator, Sales | Lead → opportunity → customer context | Catalog/bundle only; runtime not verified. |
| Projects / Office Board | C05/C09 | ERPNext Projects, Tasks, ToDo, Timesheets | Office Board | Administrator, Office/Dispatcher, Read-only | Create task → assign → comment → complete | Catalog/bundle; no Office Board workspace currently exists. |
| Field Operations | C05/C09 | ERPNext Projects plus `lenerp_core` job foundation | Wells & Jobs / Field Operations | Administrator, Office/Dispatcher, Field | Schedule crew → start field work → hand back completion | Catalog/bundle + partial custom foundation; role UX pending. |
| Well Mapping | C04 | `lenerp_core` | Wells & Jobs / Well Mapping | Administrator, Office/Dispatcher, Field | Customer → well/site with coordinates and pump notes | Local custom DocType verified; staging/app installation and final schema not verified. |
| Drilling | C04/C05 | `lenerp_core` | Wells & Jobs / Drilling | Administrator, Office/Dispatcher, Field | Well → drilling job → completion print/report | Local custom DocType/workflow verified; deployment and approval pending. |
| Fleet | C06 | ERPNext Assets plus job asset links | Trucks & Equipment / Fleet | Administrator, Inventory, Field | Truck/rig assignment → availability/maintenance review | Catalog/bundle only; named Fleet role/workspace not present. |
| Reporting | C08 | ERPNext reports plus `lenerp_core` report/API | Reports / Operations Summary | Administrator, Office/Dispatcher, Sales, Field | Review job, well, inventory, asset and exception facts | Local synthetic API/report foundation; current staged artifact and runtime need reconciliation. |
| HR / Crew & Hours | C09 | HRMS | Crew & Hours / Human Resources | Administrator, HR, Read-only as approved | Employee → attendance/leave/timesheet | Catalog only; HRMS runtime unknown and no HR role/workspace exists. |
| Payroll / Accounting & Payroll | C09 | HRMS + ERPNext Accounting | Accounting & Payroll / Payroll | Administrator, Payroll | Synthetic hours → draft payroll preview with masked values | **Blocked** on HRMS, payroll rules, confidentiality and approval. |
| Quality / Callbacks & Quality | C09 | ERPNext Quality plus LenERP callback extension if approved | Callbacks & Quality / Quality | Administrator, Quality, Office/Dispatcher | Callback → corrective action → verification/close | Catalog only; excluded from current bundle and no Champion role/workspace. |
| Support / Support & Requests | C09 | ERPNext Support plus LenERP product-change request if approved | Support & Requests / Support | Administrator, Support, Office/Dispatcher | System help or product request → triage → resolution/approval | Catalog only; excluded from current bundle and no Champion role/workspace. |
| Manufacturing | Platform / preserved proposal capability | ERPNext Manufacturing | Manufacturing, hidden from primary menu | Administrator/operator only unless approved | Review preserved capability without enabling Champion navigation | Marketed catalog row, not in `champion-drilling@1`; hidden/preserved. |
| Point of Sale | Platform / separately approved | ERPNext POS | Point of Sale, hidden | Administrator/operator only unless approved | No Champion workflow in Phase 00 | Marketed catalog row, not in current bundle; pending approval. |
| White Label | C01/platform | Control plane + `LenERP Branding Settings` | Settings / branding | Platform operator/System Manager | Review empty branding boundary without applying values | Non-marketed operator capability; no approved values. |
| Custom Domain | C01/C02/platform | Control-plane domain management + Frappe host configuration | Domains / tenant context | Platform operator only | Review domain mapping readiness, no DNS mutation | Feature-gated and unverified; no production change. |

### Champion role-to-menu/workspace matrix

The first column is the operational role name for the showcase. The second column is the currently evidenced Frappe role where one exists. “Planned” is not an authorization grant.

| Champion role | Current Frappe role evidence | Current workspace/menu | Intended Champion menu/workspaces | Allowed representative scope | Readiness / gap |
|---|---|---|---|---|---|
| Administrator | `Champion Administrator` | `Champion ERP` plus permitted standard records | All approved modules, Settings, Reports | Full synthetic showcase; no implicit platform-admin meaning | Current custom role/workspace exists; final role matrix pending. |
| Office / Dispatcher | `Champion Dispatcher` | `Champion ERP`, Well sites, Drilling jobs, Customers | Home, Office Board, Customers & Sales, Wells & Jobs, Inventory read/context, Reports | Assign and progress work; no payroll totals | Custom role exists; Office Board and final direct-route tests pending. |
| Sales | `Champion Sales User` | `Champion ERP` role membership; standard CRM/Selling permissions are installed by hook | Home, Customers & Sales, CRM, quotes/invoice context | Lead → opportunity → quote; no unrestricted operations | Role exists; workspace links and route/readback not fully verified. |
| Accounting | `Champion Accounting User` | Role created and standard permission hook includes accounting records; workspace role is present | Home, Customers & Sales context, Accounting & Payroll, Reports | Invoice/payment review; payroll only if separately authorized | Role exists; HRMS/payroll is blocked. |
| Inventory | `Champion Inventory Manager` | Role created and standard Item/Supplier/Warehouse/Receipt/Stock/Asset permissions are defined | Inventory & Purchasing, Trucks & Equipment, Reports | Receive/issue/asset maintenance | Role exists; staged permission/readback not verified. |
| Field | `Champion Field Technician` | `Champion ERP`, Well sites and Drilling jobs; limited custom permissions | Home, Wells & Jobs, Trucks & Equipment, Crew & Hours as approved | Start/complete assigned work; no payroll or financial totals | Role and custom records exist; structured employee assignment pending. |
| HR | No Champion HR role found | No HR workspace | Crew & Hours | Employee, leave, attendance, timesheet | Planned only; HRMS and role policy required. |
| Payroll | No Champion Payroll role found | No Payroll workspace | Accounting & Payroll | Synthetic draft payroll preview only | Blocked on HRMS, payroll policy, confidentiality and approval. |
| Quality | No Champion Quality role found | No Quality workspace | Callbacks & Quality | Callback/inspection/corrective action | Planned only; current catalog row is excluded from bundle. |
| Support | No Champion Support role found | No Support workspace | Support & Requests | Help/product request triage | Planned only; current catalog row is excluded from bundle. |
| Read-only | No dedicated Champion read-only role found | No read-only workspace | Home, approved read-only module homes and Reports | Read-only synthetic facts, no writes or sensitive totals | Planned only; must be created and negative-tested in a later phase. |
| Platform operator | `Champion Platform Operator` is created by install hook but is not in the workspace role list and is excluded from the demo API allowlist | No ERP workspace by design | Control Plane only | Tenant/module/provisioning administration, not Champion ERP | Must remain denied in ERP; platform-admin status alone is not an ERP grant. |

### Control Plane ↔ ERP navigation map

| Direction | Current behavior | Contract for implementation |
|---|---|---|
| Control Plane → organization | `/app/organizations/{organizationId}` shows company details and links to ERP sites/modules | Preserve organization context and make the selected tenant/environment explicit. |
| Control Plane → tenant | `/app/tenants/{tenantId}` shows site, domain, lifecycle and provisioning status | Add one obvious primary **Open ERP** action only when the tenant is authorized and healthy. Build the target from a server-validated tenant record; reject open redirects and do not trust arbitrary query URLs. |
| Control Plane → ERP handoff | No handoff endpoint, code exchange, or frontend action currently exists | Phase 03 adds state + PKCE authorization request, one-time code exchange, exact user/org/tenant/role binding, and host-scoped Frappe session creation. |
| ERP → home | Frappe standard `/app` shell plus `Champion ERP` workspace for current Champion roles | Keep standard routes compatible; the shell must show product, organization, environment and current role without exposing raw technical names as primary labels. |
| ERP → Control Plane | No `LenERP Control Plane` action was found in `lenerp_core` or the staged shell | Add a user-dropdown action labeled **LenERP Control Plane** that returns to the exact authorized `/app/organizations/{organizationId}/tenants/{tenantId}` context through an allowlisted, signed return state. |
| Direct ERP visit | Frappe has its own login/session; no central redirect is implemented | Unauthenticated direct visits may redirect to central sign-in with state/PKCE. Break-glass local ERP admin remains independent. |
| Tenant switch | No cross-application tenant switch is implemented | Never switch only from a client-provided tenant id. Reauthorize the target organization/tenant and require a fresh Frappe session or mapped tenant context. |

### Authentication, cookie, CSRF, CORS, tenant, and authorization boundaries

Current boundaries are intentionally separate:

1. **Control plane.** Local email/password login creates an opaque control-plane session. The browser sends its bearer token to the control-plane API. CORS is explicit from configured origins; the control plane does not expose an ERP session cookie.
2. **Frappe/ERP.** Frappe owns the ERP session cookie, CSRF token, user mapping, role checks, document permissions, and site database. The Frappe app shell includes `frappe.csrf_token` for its own same-origin actions. No control-plane token is accepted by current Frappe code.
3. **Tenant boundary.** The control plane maps organization → tenant → ERP site/base URL. Frappe site isolation and Frappe permissions protect ERP data, but there is currently no signed assertion binding a control-plane membership to a Frappe user/session.
4. **Authorization boundary.** Control-plane organization membership and role checks protect control-plane records. Frappe role and DocType permissions protect ERP routes/API calls. Hiding a workspace is never sufficient; direct URL and API denial are required.
5. **Cross-origin boundary.** No current SSO callback or ERP CORS policy was observed. The future code exchange must be server-to-server over TLS; it must not require shared cookies, copied passwords, or a reusable bearer token in a URL.

### Unified-login sequences

The following are required behavior, not current implementation evidence.

| Scenario | Required sequence and safe outcome |
|---|---|
| Success | ERP or Control Plane starts an authorization request with organization, tenant, allowlisted destination, state, and PKCE. The user signs in or reuses a valid control-plane session. Control Plane validates active user, verified email, membership, tenant health, and ERP role profile. It returns a short-lived, single-use code. ERP exchanges it server-to-server, validates issuer/audience/tenant/state/PKCE, maps the user, creates its normal Frappe session, and lands on the allowlisted route. |
| Denial | Missing membership, inactive user, suspended tenant, missing ERP role, or failed entitlement verification returns a clear denial without revealing another tenant. No ERP session is created; the event is audited. |
| Expiry | An expired code is rejected and consumed state is not recreated. The user sees “This sign-in link expired” with one primary action to restart sign-in. |
| Replay | A second redemption of the same code is rejected, logged as replay, and cannot create or refresh a Frappe session. |
| Wrong tenant | Code tenant, requested tenant, site host, and mapped Frappe target must match. Any mismatch fails closed, does not reveal whether the other tenant exists, and returns the user to a safe organization context. |
| Outage | If the control plane or code exchange is unavailable, ERP shows a provider-unavailable state with retry and support guidance. It never falls back to a shared password or copied token. Existing independent Frappe sessions follow the documented revocation policy. |
| Break-glass | A separately protected local ERP administrator can recover the site during identity-provider outage. It is excluded from SSO automation, time-bound/audited, stored through the approved secret process, and never used as evidence that ordinary users have ERP access. |
| Return to Control Plane | The ERP user dropdown sends the current mapped organization/tenant and a server-validated return state to Control Plane. The destination is the matching tenant page, not a generic home or arbitrary URL. |

### Unified module-state vocabulary

The display vocabulary is a projection of catalog, entitlement, provisioning, role-visibility, and provider-readback evidence. It must never turn a selection into a claim of readiness.

| State | Meaning | Entry evidence | User-facing copy |
|---|---|---|---|
| Marketed | Capability is listed in the public/catalog offer. | Active marketed catalog row. | “Available in the LenERP platform.” |
| Requested | Someone has requested it for an organization/bundle/profile. | Versioned request or bundle selection. | “Requested for this company.” |
| Entitled | Control Plane resolved the capability for the organization after dependency checks. | Effective entitlement and audit record. | “Included for this company; ERP setup is separate.” |
| Applying | The approved provisioning/configuration work is in progress. | Durable job and current step show work in progress. | “Setting up [capability].” |
| Applied | Provider readback confirms application/configuration is present. | `ModuleApplicationStatus.application_state=applied` plus sanitized evidence. | “Set up on the ERP site.” |
| Verified | Provider and role/workspace/readback checks pass for the exact tenant and version. | `verification_state=verified`, exact evidence reference, negative checks where relevant. | “Ready for this synthetic showcase.” |
| Hidden | Capability is installed/preserved or cataloged but intentionally absent from this role’s primary menu. | Role/entitlement/administrative visibility policy; direct authorization still enforced. | “Available to approved administrators” or omit from menu with an accessible explanation. |
| Needs attention | A dependency, application, verification, role mapping, provider, or runtime readback is missing/failed/unknown. | Failed state or unresolved runtime evidence. | “Needs attention — [safe next action].” Never “ready.” |

Precedence for user-facing aggregate status is `Needs attention` over `Applying`, then `Entitled`, then `Requested`/`Marketed`; `Hidden` is a visibility qualifier and never overrides a denial. A module may be `Entitled` and `Hidden`, or `Applied` but still not `Verified`.

### Responsive UX and accessibility contract

Use Champion language such as **Office Board**, **Wells & Jobs**, **Crew & Hours**, **Callbacks & Quality**, **Support & Requests**, **Customers & Sales**, and **Accounting & Payroll**. Raw Frappe DocType names belong in secondary technical detail, support diagnostics, or links where needed.

Every major screen has one primary action:

| Screen | One primary action |
|---|---|
| Control Plane tenant context | **Open ERP** |
| Module profile | **Review setup** / **Apply approved profile** according to authorization |
| ERP home | **Open my next task** |
| Office Board | **Add task** |
| Wells & Jobs | **Create or open job** |
| Module home | **Start [role-appropriate workflow]** |
| Error/denial/provider outage | **Retry** or **Return to the correct workspace**, never a dead card |

Responsive contract:

- **Desktop (≥1024 CSS px):** persistent role-aware navigation, tenant/environment context in the header, two-column list/detail where it improves scanning, and no horizontal scrolling for primary actions.
- **Tablet (768–1023 CSS px):** collapsible navigation, preserved breadcrumbs/context, one-column forms with grouped sections, and list/detail transitions that retain filters.
- **Mobile web (320–767 CSS px):** drawer navigation, one-column cards/forms, sticky or clearly placed primary action, list view instead of forced wide Kanban, column switcher for Office Board, and no requirement for native/offline behavior.
- At 200% zoom and 320 CSS px, the primary action, context, status, error, and escape route remain reachable without clipping or color-only meaning.

Accessibility and state contract:

- Logical keyboard order; skip link; keyboard-reachable nav, application switcher, primary action, profile menu, dialogs, tables, and Kanban alternatives.
- Visible focus with sufficient contrast; semantic headings, labels, descriptions, live regions for async result/error, and text plus icon for status (never color alone).
- Loading state says what is loading; empty state explains what the user can do next; validation state identifies the field and correction; denial explains missing access without cross-tenant leakage; provider failure offers retry/support; partial state identifies which records are unavailable.
- Persistent banner/badge: **Synthetic demonstration data — not Champion production data.** Payroll screens additionally state that compensation, tax, deduction, and accounting rules are provisional.
- Confidential values are excluded from unauthorized lists, global search, notifications, exports, and reports. No credentials, tokens, or private configuration are shown in UI evidence.

### Existing Champion/Vercel prototype inventory

The `champion-forecast` repository is a proposal, Project Start, acceptance, and handover workspace, not the production ERP host. The following classification is for the showcase boundary; it does not delete or modify that repository.

| Prototype route | Classification | Reason / handoff |
|---|---|---|
| `/` | Keep temporarily | Delivery dashboard, phases, blockers, scope, and handover context; keep separate from daily ERP navigation until an approved replacement exists. |
| `/overview` | Keep temporarily | Commercial and project overview; useful kickoff context, not an ERP workspace. |
| `/proposal` | Keep temporarily | Contract/proposal source; do not merge commercial claims into runtime module state. |
| `/project-start` and `/project-start/[projectId]` | Keep temporarily | Authoritative Champion-specific decision intake per the existing boundary document; no real data or credentials. |
| `/docs` | Keep temporarily | Generated delivery/handover evidence; link to the verified baseline rather than pretending it is an operational ERP report. |
| `/technologies` | Keep temporarily | Ownership and infrastructure explanation; update only through approved handover work. |
| `/usergrowth` | Keep temporarily | Timeline and delivery explanation; not a tenant/work module. |
| `/advisoryhours` | Keep temporarily | Commercial advisory boundary; not a product capability. |
| `/team` | Merge into `/overview` if still needed | Current route redirects to overview; no independent showcase value. |
| `/details` | Retire | Current route redirects to `/`; no distinct behavior. |
| `/settings` | Replace or merge after ownership decision | Contains Project Start/delivery controls and infrastructure notes; it must not become a shared runtime settings surface without a clear audience and authorization boundary. |
| `/demo` | Replace | It is a narrative/live-demo page with a hard-coded credential-like value and direct legacy ERP URL in source. It was not copied or changed; remove/rotate that exposure before any public use and replace with the authorized Control Plane → ERP handoff. |
| `/sensitivity` | Retire | Current route redirects to `/usergrowth`; no distinct showcase behavior. |
| `/investmentprojection` | Retire from the operational showcase | Purchase/payment view is commercial control, not a Champion ERP module; keep only if the proposal workspace requires it. |
| `/fernando` | Keep temporarily | Delivery-owner profile; unrelated to ERP navigation. |

The prototype’s `docs/PRE_KICKOFF_DEMO_BOUNDARY.md` correctly says its synthetic ERP demonstration is provisional and that Project Start remains authoritative. The existing hard-coded credential-like content is a security blocker for future exposure; this Phase 00 change does not print, copy, or rotate it.

### Decision register — Matt or Pedro required

No answer is inferred. Each item remains open until Matt or Pedro records the decision in the authoritative project-start/decision register and the affected package is updated.

| Decision | Why it blocks a truthful showcase | Decision owner |
|---|---|---|
| Final company display/legal name, product name, logo, colors, domain, timezone, currency, fiscal year | Controls branding, tenant context, documents, and handoff ownership | Matt/Pedro — unassigned |
| `champion-drilling@2` membership and visibility for every proposal capability, including preserved Manufacturing and POS | Current bundle is `@1` and excludes HR, Payroll, Quality, and Support | Matt/Pedro — unassigned |
| Exact Champion role names, managers, approval limits, and role-to-menu assignments | Current Frappe roles cover only six operational roles; HR/Payroll/Quality/Support/Read-only are absent | Matt/Pedro — unassigned |
| HRMS version and whether HR/Payroll must be shown at kickoff | Runtime installation is not verified and payroll rules are not approved | Matt/Pedro — unassigned |
| Employee, attendance, leave, shift, timesheet, payroll, tax, deduction, and confidentiality rules | Prevents synthetic screens from being mistaken for approved payroll configuration | Matt/Pedro — unassigned |
| Office Board labels/transitions and who may assign, reprioritize, close, or reopen work | Current labels are a proposed pattern, not an accepted process | Matt/Pedro — unassigned |
| Well, job, material, callback, quality, support, product-change, and completion fields/statuses | Current custom fields are scaffolding and include unresolved free-text personnel | Matt/Pedro — unassigned |
| Accounting chart, taxes, payment terms, invoice/payment approvals, and job costing | Determines whether commercial journeys are illustrative or usable | Matt/Pedro — unassigned |
| Central identity authority, accepted email/tenant mapping, break-glass ownership, and revocation policy | Required to implement one-login behavior without unsafe assumptions | Matt/Pedro — unassigned |
| Synthetic scenario names, seed/reset approval, demo users, and acceptable screenshots | Ensures the Matt walkthrough is reproducible and contains no real data | Matt/Pedro — unassigned |
| Acceptance authority, UAT evidence, exceptions, and kickoff definition of “shown” | Prevents technical readiness from being represented as Champion acceptance | Matt/Pedro — unassigned |

### Blockers and Phase 01 prerequisites

Phase 01 may begin only after the following are either resolved or explicitly accepted as a documented exception:

1. **Runtime evidence:** obtain an authorized read-only staging inventory: exact Frappe/ERPNext/HRMS/`lenerp_core` versions, site health, installed apps, workspaces, roles, and synthetic seed status. Local and staging runtime were inaccessible in this phase.
2. **HRMS decision and pin:** choose a Frappe v15-compatible HRMS revision, record ownership/license/build evidence, and keep HR/Payroll hidden until installation and verification pass.
3. **Immutable bundle profile:** add `champion-drilling@2` without changing `@1`; show dependency expansion and separate requested/entitled/applied/verified states.
4. **Artifact reconciliation:** reconcile sibling `lenerp_core` `fd18845` with staged/runtime `a7e47208`, including the duplicate embedded package paths, before relying on dashboard or accessibility evidence.
5. **Identity contract:** implement and test the standards-shaped one-time authorization-code/PKCE flow, user/org/tenant mapping, direct ERP entry, replay/expiry/wrong-tenant denial, and both cross-navigation actions. No current endpoint exists.
6. **Role/workspace boundary:** define and negative-test HR, Payroll, Quality, Support, Read-only, Office Board, and module-home roles; platform operator must remain denied from ERP unless explicitly mapped.
7. **Showcase workflows:** implement synthetic Office Board, Support, Quality, HR, and restricted Payroll journeys; current `lenerp_core` only proves the Wells/Jobs foundation and a limited dashboard/report path.
8. **Prototype security:** remove/rotate the pre-existing credential-like demo value in `champion-forecast` before the page is exposed or linked; do not reuse its direct ERP URL as an access mechanism.
9. **Decision closure:** record the Matt/Pedro decisions above; unresolved requirements remain `Pending` or `Needs attention`, never `Verified`.
10. **Staging-only gate:** use the generic deployment gate, synthetic-only data, exact candidate artifacts, clean upstream trees, secret scan, role/tenant negative tests, responsive/keyboard checks, and rollback evidence. Do not install apps, load data, or change production as part of Phase 00.

### Validation record

- **Relative Markdown links:** all links introduced by this verified section point to existing repository documents or the documented sibling prototype path; they must be checked again with the link script before commit.
- **`git diff --check`:** required after documentation edits; no runtime command is needed for this phase.
- **Secrets:** no secret, credential, token, password, private key, or runtime value was added to this document. Existing credential-like prototype content was not copied and remains an external blocker.
- **Runtime/production mutation:** none. Only read-only source inspection, git metadata inspection, TCP reachability checks, and DNS resolution attempts were performed. No service was contacted with credentials; no Frappe or production operation was invoked.
- **Working-tree safety:** unrelated pre-existing changes in `CLAUDE.md`, `docs/00_Master_Index.md`, `docs/champion_execution`, and `frontend/tsconfig.tsbuildinfo` are outside this Phase 00 edit and must remain untouched.

### Copy-ready prompt for Phase 01

> Continue from the verified Phase 00 baseline in `docs/champion_showcase/00_PROGRAM_BASELINE_AND_UX_CONTRACT.md`. Implement only Phase 01: create immutable `champion-drilling@2` from `@1`, adding HR, Payroll, Quality, and Support with deterministic dependencies; preserve `@1`; expose requested/entitled/applied/verified/hidden/needs-attention states; and keep ERP application, HRMS installation, production, real Champion data, SSO endpoints, and Champion acceptance out of scope. Before editing, obtain or record the authorized staging installed-app/runtime readback, reconcile sibling `lenerp_core` `fd18845` with the staged/runtime `a7e47208` artifact, and resolve the duplicate embedded package paths. Use the existing control-plane catalog/entitlement/audit/idempotency boundaries, add authorization/dependency/replay tests, preserve unrelated dirty worktree changes, run the documentation and test gates, and stop after Phase 01 with exact files, evidence, blockers, and rollback notes.
