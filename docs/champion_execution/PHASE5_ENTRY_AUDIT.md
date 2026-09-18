# Phase 5 Champion Solution Workstream — Entry Audit

Status: **BLOCKED for Champion acceptance; safe synthetic preparation in progress**  
Audit date: 2026-09-18  
Overall workstream release identity: none — use only the package identities
`CHAMP-C01-R1` through `CHAMP-C08-R1` (and later package revisions).

## Authority and precedence

The implementation follows the documented precedence:

1. Executed agreement and amendments.
2. Accepted proposal.
3. Approved Project Start decisions and acceptance records.
4. Complete LenERP delivery plan.
5. This CRM execution pack.

The local `champion-forecast` checkout references
`docs/COMPLETE_LENERP_DELIVERY_PLAN.md`, but that file is not present in the
checkout audited on 2026-09-18. No replacement or inferred requirement is
being treated as authoritative. The accepted proposal source is
`champion-forecast/src/app/proposal/page.tsx`; the Project Start question
registry is `champion-forecast/src/lib/project-start/questions.ts`.

## Repository and runtime baseline

| Input | Observed state | Evidence |
|---|---|---|
| Authoritative CRM `Lengrowth/crm` `main` | `08224008142bd8a387f908b656b3565dd1754ae5` | `git ls-remote https://github.com/Lengrowth/crm.git refs/heads/main` |
| Local CRM checkout | `bc7e2bec9912a5713fb0c2605bbc21852e9acdb2`, branch `codex/plat-p4`, ahead 16; intentional dirty changes preserved | `git status --short --branch` |
| CRM remote note | `origin` points to `BuildGrowthNow/crm`; `lengrowth` is the authoritative remote used for verification | `git remote -v` |
| `lenerp_core` baseline | clean `main` at `728de29176ddb9c05c78d734318406d57f10f205`, app `0.1.0` scaffold before C01 slice | local repository audit |
| `lenerp_core` work | isolated branch `codex/champ-c01-r1`, value-free C01 settings boundary in progress | local repository audit |
| Frappe | `15.119.1`, `edae775dd36b6c4ad7acab10230262bd74040765` | clean approved reference checkout |
| ERPNext | `15.120.0`, `945e825bee3d0d645f6cb59bcaab90fcbfb98ce3` | clean approved reference checkout |
| Fixed platform baseline | PLAT-P0 through PLAT-P4 recorded as passed/review-passed; PLAT-P4 candidate `27ede631c667c67f45d534108abeb975816ee83e` | `releases/PLAT-P4.md` |

The CRM working-tree changes in `CLAUDE.md`,
`frontend/tsconfig.tsbuildinfo`, `POST_PROGRAM_FEATURES_AND_CONTROLS.md`, and
`UX_SCREEN_BLUEPRINT.md` were present before this audit and remain untouched.

## Revalidation after concurrent branch movement

During continuation, the active CRM checkout moved to
`codex/plat-p4-readback-docs` and the authoritative `Lengrowth/crm` `main`
advanced to `4a63264e1e8cb7c998c767262a6e1022647ff7b0`. The Phase 5 commits
were cherry-picked onto the active branch without conflicts. The `lenerp_core`
implementation remains the independent commit `ed551dc` on
`codex/champ-c01-r1`; no production pointer, upstream tree, or Champion data
was changed. The earlier `0822400…` value remains the point-in-time baseline
used when this audit was first written, not the current remote head.

## Entry findings

### Available

- Synthetic package work is allowed by the governing documents.
- The custom-app boundary is established and the upstream reference trees are
  clean and pinned.
- The proposal promises the complete current platform/modules, Champion
  drilling and field-service configuration, Well Mapping, branding, reseller
  showcase/onboarding refinement, migration, training, documentation, and
  infrastructure/source handover.
- The Project Start registry defines concrete discovery IDs for agreement,
  company/roles, data, sales, jobs, inventory, accounting, reports, branding,
  and go-live acceptance.

### Missing or blocked

- No accessible saved Project Start record or export was found in the local
  `champion-forecast` workspace. The code contains only the unanswered seed
  record; no answer is being inferred.
- No local accepted-agreement record or executed-copy evidence was found in the
  authoritative workspaces. The CRM handover notes refer to an external
  attestation, but it is not treated as independently verified here.
- The acceptance authority, system administrator, user list, role matrix,
  approval limits, and confidential-data boundaries are not recorded in the
  accessible Project Start data.
- Company settings, final product name/assets/domain, Well/Site identifiers and
  fields, job states/transitions, inventory rules, accounting rules, KPI
  definitions, forms, and print outputs remain unanswered.
- Credential rotation is still waived. Champion confidential files cannot be
  received, copied, restored, processed, or imported under the current waiver.
- The read-only SSH inventory of current production/staging installed apps and
  customizations could not be completed because the approved host timed out on
  port 22. No production change was attempted.
- `lenerp_core` had no DocTypes, fixtures, patches, hooks, roles, workspaces,
  reports, print formats, or tests before the C01 foundation slice.
- The proposal question source contains stale literal `$32,000` and `$80/hour`
  strings, while the canonical commercial config/proposal is `$30,000` and
  `$55/hour`; runtime registry normalization currently hides the mismatch. It
  must be corrected or explicitly reconciled before treating the question
  source as a commercial record.

## Current package disposition

| Package release | Classification | State | Immediate blocker |
|---|---|---|---|
| `CHAMP-C01-R1` | Included | In development, synthetic/value-free foundation | `ORG-01`, `BRD-01`–`BRD-03`, approved assets/domain, staging evidence, acceptance actor |
| `CHAMP-C02-R1` | Included | Proposed/blocked | `AGR-02`, `ORG-02`–`ORG-06`, confidential-data boundaries and approval limits |
| `CHAMP-C03-R1` | Included platform profile | Defined, synthetic-only | Approved module/workspace matrix and ERP application/verification evidence |
| `CHAMP-C04-R1` | Included | Proposed/blocked | `JOB-06`–`JOB-07`, `CRM-02`, representative decisions and C02 permissions |
| `CHAMP-C05-R1` | Included | Proposed/blocked | C02/C04 plus `JOB-01`–`JOB-05`, `JOB-08`–`JOB-12` |
| `CHAMP-C06-R1` | Included | Proposed/blocked | C02/C05 plus `INV-01`–`INV-06` |
| `CHAMP-C07-R1` | Included | Proposed/blocked | C02/C05 plus `CRM-03`–`CRM-04`, `ACC-01`–`ACC-08`; accounting ambiguity is a blocker |
| `CHAMP-C08-R1` | Included | Proposed/blocked | C04–C07 plus `JOB-12`, `REP-01`–`REP-04`, forms/print inputs |

Detailed package records are in `docs/champion_execution/packages/`. The
proposal-to-package matrix is in `TRACEABILITY_MATRIX.md`.

## Minimum unblock sequence

1. Make the saved Project Start record/export available through the approved
   location, or record that it does not yet exist.
2. Resolve agreement/commencement/payment and identify the authorized Champion
   acceptance actor (`AGR-01`, `AGR-02`, `AGR-07`).
3. Approve C01 company/branding/domain inputs (`ORG-01`, `BRD-01`–`BRD-03`).
4. Authorize credential rotation and secure transfer before any real files are
   received; until then continue only with synthetic records.
5. Provide C02 role/approval inputs, then approve the C03 module/workspace
   matrix before ERP verification is claimed.

Until these decisions and evidence exist, the correct workstream verdict is:

`PHASE 5 / CHAMPION SOLUTION WORKSTREAM: BLOCKED`
