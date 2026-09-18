# Champion pre-kickoff synthetic demonstration runbook

Status: `SYNTHETIC DEMO: READY FOR STAGING VALIDATION`  
Boundary: synthetic records only; no Champion confidential data, real migration, or production activation.

This runbook describes the repeatable demonstration that can be shown before
Project Start answers are available. It does not replace Champion acceptance,
UAT, training, or the final configuration decision record.

## Demonstration accounts and roles

The `lenerp_core` app creates reusable role profiles during install/migrate:

| Role | Demonstration responsibility |
|---|---|
| Champion Administrator | Full Champion ERP administration and recovery |
| Champion Dispatcher | Customers, well sites, scheduling, assignments, job status |
| Champion Sales User | Leads, opportunities, customers, quotes, job context |
| Champion Accounting User | Quotes, invoices, payment and accounting visibility |
| Champion Inventory Manager | Items, suppliers, warehouses, assets, stock workflows |
| Champion Field Technician | Assigned well/job records, work notes, completion capture |
| Champion Platform Operator | Reseller/control-plane role; intentionally absent from Champion ERP DocType permissions |

Create or assign users only in the authorized staging site. Never put a
password or token in this runbook, source, screenshots, or evidence.

## Presentation order

1. Open the LenERP public Champion overview and explain that the walkthrough
   uses fictional records and provisional assumptions.
2. Sign into the ERP staging site as the Champion Administrator and open the
   Champion ERP workspace.
3. Show the company/branding settings boundary and explain that legal identity,
   final name, logo, tax settings, fiscal year, and domain remain configurable.
4. Show Customers and Contacts, then open the three Well Site records. Use the
   map coordinates, depth, pump notes, customer link, search, filtering, and
   export/print actions.
5. Open the Drilling Jobs list. Walk through the completed, in-progress,
   scheduled, and planned records; open the completed job and print the job
   completion record.
6. Show the standard ERPNext Buying, Stock, Assets, Selling, and Accounting
   workspaces as available. The protected staging evidence currently populates
   the custom Champion core records only; do not imply optional supplier/item/
   warehouse/equipment records exist until their standard prerequisites pass.
7. Walk the commercial journey only when the optional prerequisites have been
   satisfied: Lead → Opportunity → Customer → Quotation → Job → Sales Invoice
   → Payment Entry. Point out that accounting values are standard demo values,
   not Champion-approved decisions.
8. Open Champion Operations Summary and the dashboard API. Explain that every
   row and count is read from persisted records, not decorative KPI data.
9. Sign in as a Field Technician and show the reduced record set. Attempt a
   direct restricted route/API action as the Platform Operator and capture the
   expected denial.
10. Close by reviewing the four post-kickoff decisions: approved company and
    branding, role/approval matrix, real data authorization, and final
    accounting/report definitions.

## Seed, rerun, and reset

The seed is opt-in and idempotent. It is never called by install or migrate:

```bash
bench --site erp-staging.example.test execute lenerp_core.demo_seed.seed
bench --site erp-staging.example.test execute lenerp_core.demo_seed.status
bench --site erp-staging.example.test execute lenerp_core.demo_seed.reset
```

The seed uses the `DEMO-CHAMPION-` prefix and the `DEMO Champion Well Drilling`
company name. Reset deletes only that exact synthetic boundary. Run status
after reset and record zero counts before releasing the staging site.

## Expected data

- 1 fictitious company, 3 customers, 3 contacts, and 3 well/site records.
- 4 jobs across Planned, Scheduled, In Progress, and Completed states.
- The current protected staging pass confirms zero optional lead/opportunity,
  supplier/item/warehouse/asset, quotation/invoice/payment records because
  standard ERPNext prerequisites were unavailable; this is an explicit follow-
  up boundary, not a fabricated demo result.
- All locations, names, notes, and values are synthetic and replaceable.

## Fallback procedure

If the ERP staging lane is unavailable, show the public Champion overview and
the documented workflow storyboard only; do not fabricate browser evidence or
claim that persisted ERP workflows passed. If a single standard ERPNext
document cannot be created, capture the exact validation error, keep the custom
records intact, correct the seed/configuration, rerun the seed, and rerun the
full sequence. Do not bypass permissions or alter production.

## Evidence checklist

Record the exact CRM commit, `lenerp_core` commit/version, Frappe and ERPNext
versions, staging site, database migration result, seed/status/reset output,
role-by-role browser evidence, direct denial response, print/PDF inspection,
responsive/accessibility checks, and the remaining Project Start decisions.

The evidence may support:

`CHAMPION PRE-KICKOFF SYNTHETIC DEMO: PASS`

only after the complete staging/browser sequence is reproducible. It must still
state:

- `CHAMPION-SPECIFIC ACCEPTANCE: PENDING PROJECT START`
- `REAL-DATA MIGRATION: NOT AUTHORIZED`
- `PRODUCTION ACTIVATION: NOT AUTHORIZED`
