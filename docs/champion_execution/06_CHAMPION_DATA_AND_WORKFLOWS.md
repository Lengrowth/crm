# Continuous Champion Data Migration and Workflow Validation

## Goal

Prepare migration controls before Champion files arrive, then move received data through profiling, deterministic staging imports, reconciliation, workflow validation, cutover, and production verification. Migration is a continuous workstream rather than a single late development phase.

[`DATA_MIGRATION_REGISTER.md`](DATA_MIGRATION_REGISTER.md) defines stages D01–D09 and the source/import record templates.

## Work that begins before files arrive

1. Record every expected source category, source owner, Champion validator, likely format, authoritative-system decision, unique identifier, history cutoff, expected delivery date, and secure-transfer location.
2. Define the target data dictionary for customers, contacts, sites/wells, jobs, quotes, invoices/opening balances, payments, vendors, items, stock, assets, users, notes, and document references.
3. Create import package conventions for batch ID, source checksum, mapping version/commit, target schema/app version, operator, timestamps, dry run, counts, rejections, held records, duplicates, and correction/reversal.
4. Create synthetic source files that exercise missing values, duplicates, invalid dates, relationship failures, retries, and partial rejection.
5. Build reusable importers/templates only for approved or clearly provisional mappings. Label assumptions that require source confirmation.
6. Establish secure receipt, retention, access, and deletion rules. Complete required credential rotation before Champion files enter the environment.
7. Link each target category to the Champion solution packages that consume it.

## Work after files arrive

1. Preserve untouched source copies and record receipt metadata/checksums.
2. Profile each source for row counts, date ranges, identifiers, duplicates, missing/invalid values, encoding, and relationship quality.
3. Finalize mappings and quality rules with the assigned source owner/validator.
4. Import into a clean staging restore and record accepted, imported, updated, rejected, held, duplicate, and variance counts.
5. Validate customer-to-site/well-to-job-to-invoice and other required relationships.
6. Correct repeatable defects in mapping/import logic and rerun from the same clean restore point.
7. Validate affected Champion solution packages with migrated representative records and production-like volume.
8. Repeat until the same inputs and versions produce the same accepted result.
9. Approve the source freeze, delta capture, final backup, production import, reconciliation, communications, and rollback/correction plan.
10. Run the production import as its own recorded release after accepted code/configuration is already deployed.

## Dependencies and scheduling

- D01–D03 may proceed alongside fixed platform phases.
- D04 begins only when a source is securely received.
- D05–D07 may cause a Champion package to be revised; the revision receives a new package release and does not silently alter an accepted artifact.
- D08 can be drafted early but is approved only after reconciliation and UAT.
- D09 occurs during final cutover and is required before Phase 7 acceptance.
- Different data categories may be at different migration stages. Track them separately instead of blocking all migration on the latest source.

## Acceptance tests

- Every included category has a source owner, validator, mapping, and migration result.
- Counts and control totals balance or have documented, accepted variances.
- Required relationships work where the source supports them.
- Duplicate, rejected, and held-record rules are deterministic.
- Repeating an import from a clean restore produces the same outcome.
- Retry cannot duplicate already-accepted rows.
- Role permissions remain correct with real data content and volume.
- No Champion data appears in Git, public/reseller surfaces, synthetic tenants, logs, or another tenant.
- Production import can be reproduced from recorded code, configuration, and source checksums.
- Code rollback and imported-data correction are documented separately.

## Production release

Deploy accepted compatible code and configuration first, with no destructive cleanup. Smoke-test that release. Then run the final recorded import batch and reconciliation.

Before users resume production work, a cutover rollback may restore the full site. After users create new records, prefer a tested batch correction/reversal so a restore does not erase valid post-cutover work.

## Workstream gate

The migration workstream passes when D01–D09 are complete for every included category, Champion validators approve the reconciliations and representative workflows, final production totals and relationships are accepted, every exception has an owner/decision, and the handover contains the mappings, import tools, batch records, exports, and operating instructions.
