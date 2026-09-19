# Phase 07 — Wells, Jobs, Materials and Reports Polish

## AI goal

Make the existing LenERP-owned operational foundation understandable and credible in the module showcase, while preserving the distinction between implemented scaffolding and the later Champion discovery required for final fields and workflows.

## Current foundation

- `LenERP Well Site` links a unique site/well identity to Customer, Contact, address, coordinates, depth, pump notes and operational notes.
- `LenERP Drilling Job` links Customer, Well Site, job type, schedule, status/workflow, personnel text, rig/truck Assets, priority, materials, work notes and completion.
- `LenERP Job Material` links Item, quantity, UOM and issuing Warehouse as a child record.
- Champion roles, a Champion ERP workspace, Operations Summary, dashboard API, alerts and a completion print format exist for synthetic records.

## Build scope

1. Improve workspace/module-home presentation for Wells & Jobs and Reports.
2. Replace ambiguous field labels with unit-aware, translatable labels; do not silently convert the existing depth field without a migration/compatibility decision.
3. Present Customer → Well → Job → Materials → Completion → Invoice context through links and timelines.
4. Replace free-text assigned personnel in the demonstration path with approved Employee/User links or a backward-compatible structured assignment layer while preserving existing data.
5. Clearly label material rows as planned/recorded usage until a submitted Stock Entry exists. Do not imply stock deduction from child-table presence alone.
6. Link rigs/trucks to Assets and show maintenance/availability context without exposing unauthorized data.
7. Remove demo-ID-only assumptions from production-intended reports while retaining explicit synthetic filters for demo reset/evidence.
8. Make report source, filters, as-of time, permission scope and synthetic state visible.
9. Add useful empty states and guided next actions for missing Well, Job or material data.
10. Preserve later extension points for casing, static water level, yield, formations, permits, state reports, completion records, photos and service history; do not invent their final schema.

## UX requirements

- A Well detail page answers location, customer, current status and related work first.
- A Job detail page answers schedule, crew/assets, work state, materials and completion first.
- Related records open without losing the operational context.
- Forms group planning, execution and completion fields progressively.
- Reports distinguish alerts from facts and link every exception to its source record.
- Print output is branded, legible and clearly synthetic in the demonstration.

## Acceptance tests

- Dispatcher completes the synthetic Customer → Well → Job → Completion path.
- Field Technician sees and edits only authorized operational fields.
- Accounting and Inventory roles see appropriate linked context without unrestricted Well/Job mutation.
- A material row does not change stock until an explicit stock transaction is introduced.
- Operations Summary works with its documented scope and no longer depends accidentally on demo naming for production behavior.
- Dashboard counts reconcile to persisted synthetic records.
- Direct route, print, export, mobile, keyboard and accessibility checks pass.

## Non-goals

- Final Champion Well schema.
- QR scan sessions, automatic stock issue or invoice generation.
- Government permit automation.
- Real Champion records.

## Gate and rollback

Use additive fields/routes and compatibility migrations. Preserve old fields until read/write migration and rollback are proven. Demo records must have exact seed/reset manifests.

## Execution prompt

> Polish the existing `lenerp_core` Well Site, Drilling Job, Job Material, workspace, reports and print experience for an honest synthetic Matt demonstration. Improve structured links, role UX, report provenance and responsive accessibility without inventing unanswered Champion fields, silently changing units, claiming stock movement, or loading real data.
