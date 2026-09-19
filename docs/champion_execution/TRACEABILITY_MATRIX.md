# Phase 5 Proposal-to-Package Traceability Matrix

Status: **Initial baseline — requirements and acceptance are pending where
Project Start inputs are unavailable**  
Release identities are package identities; no `PLAT-P5` identity is used.

| Proposal promise | Project Start decisions / source | Package or stage | Code/configuration boundary | Test and evidence | Acceptance actor | Status |
|---|---|---|---|---|---|---|
| Complete current LenERP platform and current modules | `BRD-04`; Phase 3 authoritative catalog and entitlement records | `CHAMP-C03-R1` | CRM module catalog plus ERP module/workspace verification in `lenerp_core` | Catalog matrix, applied/verified ERP readback, role visibility and denial tests | Authorized Champion decision maker (`AGR-02`) | Synthetic workspace implemented; Champion module approval pending |
| Champion ERP configured for well drilling and field service | `JOB-01`–`JOB-12`, `CRM-02`–`CRM-04`, `ORG-03`–`ORG-05` | `CHAMP-C04-R1`–`CHAMP-C07-R1` | `lenerp_core` DocTypes, fixtures, roles, workflows, reports and standard ERPNext links | Representative journeys 1–8, clean install/migrate, responsive and permission evidence | Authorized Champion UAT actors (`GLV-04`, `GLV-05`) | Synthetic implementation in development; staging/browser evidence pending |
| Well Mapping: locations, depth, pump specs, completion records | `JOB-06`, `JOB-07`, `DAT-08`–`DAT-10` | `CHAMP-C04-R1` | `lenerp_core` Site/Well model and approved map/list/detail behavior | CRUD, validation, duplicate/search, map/list, report/export and permission tests | Champion Well/Site validator plus acceptance authority | Synthetic schema and validation implemented; approved identifiers/rules pending |
| Approved company settings, product identity and branding | `ORG-01`, `BRD-01`–`BRD-03` | `CHAMP-C01-R1` | `lenerp_core` `0.2.0` value-free settings boundary; standard ERPNext settings applied only after approval | Static contract test and wheel-content check pass; clean install/migrate, light/dark/responsive, links, print/PDF and fallback assets pending | Acceptance authority (`AGR-02`) | Foundation implemented; approved values and staging evidence pending |
| Reseller module showcase and streamlined onboarding refinement | `BRD-04`–`BRD-11`; PLAT-P3/PLAT-P4 controls | Platform PLAT-P3/PLAT-P4 plus final refinement evidence | CRM control-plane catalog/onboarding; no unapproved new provisioning/billing | Existing platform regression, request-only/approval/isolation/cleanup artifacts | Delivery owner and Champion acceptance authority | Platform foundation passed; Champion refinement pending |
| Agreed data migration | `DAT-01`–`DAT-15` | `DATA-D01-R1`–`DATA-D09-R1`, coordinated with C04–C08 | Versioned import tools/mappings and controlled staging batches; no real data under waiver | Counts, checksums, deterministic rerun, reconciliation, workflow validation and cutover readback | Source owners/validators and acceptance authority (`DAT-14`, `GLV-05`) | D01–D03 preparation only |
| Staff training | `GLV-02`, `GLV-03` | `FINAL-P7` after package release | Role-based guides and training records | Attendance, guided journeys, sign-off | Acceptance authority | Not started |
| Documentation and operating handover | `GLV-08`–`GLV-10` | Every package plus `FINAL-P7` | Release records, admin/user/developer/runbooks and handover inventory | Receipt checklist, repository/infra/backup access evidence | Acceptance authority | Not started |
| Infrastructure, source-code and ownership handover | `GLV-08`, `BRD-01`–`BRD-03` | `FINAL-P7` | Protected release path, domain/backup/monitoring ownership transfer | Ownership, backup/restore, rollback, domain and operational smoke evidence | Authorized handover recipient | Not started |

## Commercial boundary register

| Request/feature | Classification | Rule/evidence |
|---|---|---|
| Separate mobile Field App | Advisory | `AGR-09`, `JOB-10`; responsive web may be included, native/separate app requires approval |
| New external accounting integration (QuickBooks or other) | Needs Review / Advisory unless expressly accepted | `ACC-09`; accounting ambiguity blocks C07 implementation guesses |
| Complete reseller-site rewrite | Needs Review | Proposal promises showcase/refinement; `BRD-07`, `BRD-08`, `BRD-11` define the included boundary |
| Unlimited provisioning, billing, or future reseller customization | Deferred/Advisory | Existing PLAT-P4 controls and proposal advisory terms remain authoritative |
| Live GPS tracking | Needs Review | Well Mapping proposal does not itself approve live tracking |

No row is accepted merely because a synthetic screen or fixture exists.
