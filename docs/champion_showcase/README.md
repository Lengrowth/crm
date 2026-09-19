# Champion Pre-Kickoff Module Showcase and Unified Access Program

**Status:** Phase 01 control-plane profile implemented locally; staging/runtime verification remains blocked
**Purpose:** Prepare a coherent, role-aware, synthetic Champion demonstration before the Matt kickoff without representing unanswered business rules as accepted production configuration.
**Governing release rules:** [`../champion_execution/PHASE_DEPLOYMENT_GATE.md`](../champion_execution/PHASE_DEPLOYMENT_GATE.md) and [`../champion_execution/PROGRAM_AND_RELEASE_MODEL.md`](../champion_execution/PROGRAM_AND_RELEASE_MODEL.md).

## Outcome

Champion should experience one product:

```text
LenERP Control Plane
  company, tenant, modules, access, provisioning and health
                 │
                 │ one identity + verified tenant handoff
                 ▼
Champion ERP Site
  ERPNext + HRMS + lenerp_core
  daily operational records and role workspaces
```

The demonstration must show every module promised in the proposal while remaining truthful about its state. A module is not “shown” merely because a marketing card exists. For this program, a shown module has:

1. a stable control-plane catalog identity;
2. an entitled/applied/verified state that reflects reality;
3. an installed backing application when required;
4. a role-authorized ERP workspace or route;
5. at least one representative synthetic record or workflow;
6. a useful empty state when no record exists;
7. responsive, keyboard-accessible, branded navigation;
8. an explicit “synthetic demonstration” boundary until Champion accepts it.

Phase 00 verification, including the current control-plane/ERP inventory, runtime limitations, role and module matrices, identity/security contract, responsive UX rules, prototype classification, decisions, blockers, and the copy-ready Phase 01 prompt, is recorded in [`00_PROGRAM_BASELINE_AND_UX_CONTRACT.md`](00_PROGRAM_BASELINE_AND_UX_CONTRACT.md). This status does not claim Champion approval, production readiness, HRMS installation, or unified login.

Phase 01 implementation, artifact reconciliation, staging readback boundary, exact rollback notes, and remaining blockers are recorded in [`09_PHASE_01_IMPLEMENTATION_EVIDENCE.md`](09_PHASE_01_IMPLEMENTATION_EVIDENCE.md). `champion-drilling@2` is a versioned control-plane catalog profile only; ERP application, HRMS installation, production, real data, SSO, and Champion acceptance remain out of scope.

## Product and identity decisions

- The control plane is the identity and tenant-selection authority.
- ERPNext, HRMS, and `lenerp_core` are code packages inside the same Champion ERP experience, not separate user-facing systems.
- Authentication is joined through a standards-shaped, short-lived authorization-code exchange. Passwords and session cookies are never copied between applications.
- Opening ERP from the control plane preserves the selected tenant and returns the user to an allowed ERP destination.
- Opening the control plane from ERP returns the user to the authorized organization/tenant page.
- Platform administrators receive no implicit Champion ERP access. ERP access requires an explicit organization membership and ERP role profile.
- A separately protected, audited ERP break-glass administrator remains available for recovery.
- Production activation, real payroll, real employee records, and Champion acceptance are outside the pre-kickoff demonstration unless separately authorized.

## Target ERP navigation

Role visibility is authoritative; users do not see every menu simply because the platform contains every module.

| Experience | Backing capability |
|---|---|
| Home | Role-specific overview and next actions |
| Office Board | Projects, Tasks, assignments, comments, Kanban and Gantt |
| Customers & Sales | CRM, Selling, quotations and invoices |
| Wells & Jobs | `LenERP Well Site`, `LenERP Drilling Job`, scheduling and completion |
| Inventory & Purchasing | Stock, Buying, suppliers, warehouses and receiving |
| Trucks & Equipment | Assets, maintenance and vehicle warehouses |
| Crew & Hours | HRMS Employee, attendance, leave, shifts and timesheets |
| Quality & Callbacks | Quality inspection, callback/rework and corrective action |
| Support & Requests | Issue, system help, product-create and product-update requests |
| Accounting & Payroll | Accounting and HRMS Payroll, restricted by role |
| Reports | Operational, financial and exception reporting |

## Phase sequence

| Phase | AI goal | Primary package impact |
|---|---|---|
| 00 | [`00_PROGRAM_BASELINE_AND_UX_CONTRACT.md`](00_PROGRAM_BASELINE_AND_UX_CONTRACT.md) | C02, C03, C08 |
| 01 | [`01_CHAMPION_MODULE_PROFILE_V2.md`](01_CHAMPION_MODULE_PROFILE_V2.md) | C03, C09 |
| 02 | [`02_HRMS_AND_DEPENDENCY_AWARE_PROVISIONING.md`](02_HRMS_AND_DEPENDENCY_AWARE_PROVISIONING.md) | C03, C09 |
| 03 | [`03_UNIFIED_IDENTITY_AND_CROSS_NAVIGATION.md`](03_UNIFIED_IDENTITY_AND_CROSS_NAVIGATION.md) | C02, C03, C09 |
| 04 | [`04_ROLE_BASED_ERP_SHELL_AND_MODULE_HOME.md`](04_ROLE_BASED_ERP_SHELL_AND_MODULE_HOME.md) | C02, C03, C08, C09 |
| 05 | [`05_OFFICE_BOARD_PROJECTS_AND_TASKS.md`](05_OFFICE_BOARD_PROJECTS_AND_TASKS.md) | C05, C09 |
| 06 | [`06_SUPPORT_QUALITY_HR_AND_PAYROLL_SHOWCASE.md`](06_SUPPORT_QUALITY_HR_AND_PAYROLL_SHOWCASE.md) | C08, C09 |
| 07 | [`07_WELLS_JOBS_MATERIALS_AND_REPORTS_POLISH.md`](07_WELLS_JOBS_MATERIALS_AND_REPORTS_POLISH.md) | C04–C08 |
| 08 | [`08_END_TO_END_UX_CERTIFICATION_AND_MATT_DEMO.md`](08_END_TO_END_UX_CERTIFICATION_AND_MATT_DEMO.md) | All affected packages |

Phases run in order. Reversible design work may overlap, but no later phase may claim an installed, applied, verified, or accepted state before its dependency passes.

## Global UX contract

- Use Champion’s language rather than framework terminology.
- Design around tasks and decisions, not DocType inventories.
- Preserve orientation between control plane and ERP: product mark, organization, environment, current role and destination are always clear.
- Provide a single primary action per page and progressive disclosure for advanced fields.
- Keep confidential values out of list cards, global search, guest pages and unauthorized reports.
- Desktop, tablet and mobile-web layouts are required. Native/offline Field App behavior is not implied.
- Every loading state, empty state, validation error, authorization denial and provider failure must explain what happened and the safe next action.
- Do not create dead module cards, fake analytics, decorative actions, or links to unimplemented pages.
- Meet WCAG 2.2 AA intent: keyboard operation, visible focus, semantic labels, zoom support, contrast, reduced motion and no color-only status.
- Preserve an escape route: Control Plane in the ERP user menu and Open ERP in the tenant context.

## AI execution contract

Each phase document is a bounded goal for an implementation AI. The AI must:

1. inspect the current repository and actual installed-app/runtime state before editing;
2. preserve unrelated dirty worktree changes;
3. use additive, versioned changes and keep upstream Frappe/ERPNext/HRMS clean;
4. implement in the control plane and `lenerp_core` repositories where their ownership boundaries require it;
5. add success, denial, validation, retry and recovery tests;
6. validate locally, then on the isolated staging lane;
7. update package/release evidence without claiming Champion acceptance;
8. stop before real data, production activation, identity cutover, or payroll calculation unless explicitly authorized;
9. leave a concise handoff with changed files, commands, evidence, risks and the exact next phase gate.

## Pre-kickoff completion definition

The program is ready for Matt’s kickoff when:

- one control-plane login can open the authorized Champion ERP without a second password;
- ERP can return the same user to the correct control-plane tenant context;
- every promised module has an honest control-plane and ERP state;
- the role-specific ERP menu is usable and visually coherent;
- Office Board, Support, Quality, HR and Payroll have representative synthetic journeys;
- Wells, Jobs, Materials and Reports are clearly demonstrated as LenERP-owned ERP capabilities;
- unauthorized users and direct URLs are denied;
- no Champion confidential or real payroll data is present;
- a recorded staging demo and fallback plan pass Phase 08.
