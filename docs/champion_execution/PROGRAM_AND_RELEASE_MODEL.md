# Program and Release Model

## Purpose

This document separates contractual delivery milestones from technical release sequencing. Champion-specific requirements and migration inputs will become available at different times; they must be allowed to enter the program without turning production deployment into an untracked sequence of exceptions.

## Sources and precedence

1. Executed Software Purchase and Implementation Agreement and signed amendments.
2. Accepted proposal where it does not conflict with the agreement.
3. Approved Project Start decisions and acceptance records.
4. Complete LenERP delivery plan.
5. This tactical execution pack.

This pack controls implementation mechanics. It does not expand or reduce the commercial scope.

## Three-track delivery system

| Track | Contents | Scheduling rule | Completion rule |
|---|---|---|---|
| Platform | Safety, CRM/reseller UX, module administration, onboarding, provisioning | Fixed dependency order | Each phase is independently deployable and passes the release gate |
| Champion solution | Company setup, roles, selected modules, Well/Job pages, workflows, reports, forms | Package enters when its requirements and dependencies are ready | Package acceptance tests and Champion approval pass |
| Data migration | Inventory, mapping, import, reconciliation, cutover | Continuous from discovery through go-live | Counts, relationships, totals, exceptions, and validators are accepted |

Development may overlap across tracks. Production changes remain explicit releases.

## Release identities

Use one of these identifiers in the release record:

- `PLAT-P0` through `PLAT-P4` for fixed platform phases.
- `CHAMP-C01-R1`, `CHAMP-C02-R1`, and so on for Champion solution packages.
- `DATA-D01-R1`, `DATA-D02-R1`, and so on for migration work.
- `FINAL-P7` for final qualification, domain cutover, training, acceptance, and handover.

A release may contain more than one package only when their dependencies, rollback behavior, and acceptance tests are compatible. The release record lists every included package and explicitly states why combining them is safe.

## Package lifecycle

Every Champion and data package uses these states:

1. `proposed` — requested but not classified or approved.
2. `defined` — owner, scope, dependencies, and acceptance scenarios recorded.
3. `ready` — required decisions/data are available and implementation may begin.
4. `in_development` — isolated implementation is in progress.
5. `in_staging` — exact candidate is deployed for validation.
6. `accepted` — package evidence and approval are recorded.
7. `released` — accepted package is promoted and production smoke tests pass.
8. `deferred` — intentionally postponed with owner and reason.
9. `blocked` — cannot proceed until a recorded dependency is resolved.

`released` does not mean the complete Champion program is accepted. Final program acceptance occurs only at Phase 7.

## Entry rules for flexible work

A Champion-specific page, module configuration, workflow, report, or import may enter between fixed phases when:

- its package ID exists in the appropriate register;
- commercial classification is Included, Advisory, Needs Review, or Deferred;
- requirements and acceptance scenarios are approved;
- prerequisite platform APIs/components and module dependencies exist;
- the database change is additive or has a rehearsed recovery plan;
- unfinished behavior is disabled by a server-controlled flag;
- the release uses the generic deployment gate.

Work may be designed or scaffolded with synthetic data before requirements are final, but it remains `proposed` or `defined`; it cannot be represented as Champion-accepted functionality.

## Platform dependency spine

1. Phase 0 establishes the safe release path.
2. Phase 1 supplies stable navigation and route behavior.
3. Phase 2 supplies shared page/component patterns.
4. Phase 3 supplies module catalog and entitlement truth.
5. Phase 4 supplies reseller onboarding and controlled provisioning.
6. Phase 7 converges all required Champion packages and data stages on the final domain.

Champion packages can be released as soon as their actual dependencies are present. For example, a Well DocType package can follow Phase 0, while its polished CRM/operator status page may depend on Phase 2.

## Temporary and final domain model

`erp.lengrowth.com` is the temporary ERPNext implementation hostname, not the
SaaS control-plane hostname or the permanent Champion ownership boundary. The
current SaaS control plane is served at `lenerp.lengrowth.com`; Phase 1 shell
acceptance must test that hostname and the non-public staging lane separately
from the ERPNext hostname.

Domain transition stages:

1. Inventory current DNS, TLS, nginx, ERP host settings, callbacks, cookies, email links, webhooks, monitoring, and backups.
2. Replace hardcoded hostnames with environment/configuration values.
3. Record the final product name and Champion-controlled domain/account when approved.
4. Add the final hostname to staging and test DNS, TLS, authentication, API, files, email links, background jobs, and external monitoring.
5. Freeze changes, back up code/database/files, bind the final production hostname, and run the production smoke suite.
6. Keep the old hostname as a documented redirect or compatibility route for the approved transition period.
7. Remove temporary-domain dependencies only after traffic, integrations, and bookmarks are verified migrated.

The final handover records ownership and administrative control of the production server, GitHub repositories, DNS/registrar, SSL, backup destination, service accounts, and monitoring.

## Security timing decision

The delivery owner may begin Phase 0 baseline, local development, staging construction, and synthetic-data work before rotating known exposed credentials, provided no Champion confidential data enters the affected environment. The exception is recorded in the risk/blocker register.

Before receiving, restoring, or importing Champion data:

- rotate every exposed administrator, API, database, and service credential;
- remove plaintext values from ordinary documentation and repository candidates;
- verify secret scans and repository history;
- issue least-privilege project credentials and enable MFA where available.

This exception permits work to begin; it does not permit Phase 0 security completion to be claimed early.

## Convergence gate before Phase 7

Phase 7 may begin only when:

- fixed platform Phases 0–4 have passed;
- every required Champion package is accepted in staging;
- migration has reached an accepted reconciliation and cutover plan;
- final name, domain, ownership accounts, users, trainers, validators, and acceptance authority are recorded;
- blocking defects and scope decisions are closed or explicitly accepted;
- the final candidate and recovery points are identified.
