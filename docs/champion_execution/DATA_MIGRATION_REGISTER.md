# Data Migration Workstream Register

## Purpose

Data migration is a continuous workstream. It starts before source files arrive and produces independently reviewable evidence at each stage. Actual production import remains late, after accepted staging reconciliation and UAT.

## Stages

| ID | Stage | Can begin before files? | Output | Exit condition |
|---|---|---:|---|---|
| D01 | Source inventory and responsibility | Yes | Source/owner/validator/category/format register and secure-transfer plan | Every expected source has an owner and authoritative-system decision |
| D02 | Data dictionary and import contract | Yes, with headers/samples | Target fields, identifiers, relationships, required values, formats, and history cutoffs | Mapping assumptions are approved or explicitly marked pending |
| D03 | Import framework and controls | Yes | Batch IDs, checksum capture, mapping versions, dry-run mode, rejection output, counts, and correction hooks | Synthetic import is repeatable and idempotent |
| D04 | Source profiling | No | Counts, date ranges, nulls, duplicates, invalid values, and quality risks | Every received source has a signed-off profile |
| D05 | Clean staging import | No | Imported/rejected/held/duplicate counts and relationship results | Clean restore and deterministic rerun succeed |
| D06 | Reconciliation and correction | No | Control totals, variance report, mapping corrections, accepted exceptions | Assigned validators approve counts/totals/relationships or exceptions |
| D07 | Workflow UAT with migrated data | No | Representative workflow, permission, report, and output evidence | Required Champion packages pass with representative records |
| D08 | Cutover preparation | Partly | Freeze time, delta-capture plan, final source list, backup, rollback/correction plan, communications | Go-live authority approves final runbook |
| D09 | Production import and verification | No | Final batch records, reconciliation, exceptions, smoke tests, and sign-off | Production totals and relationships are accepted |

## Source register template

| Source ID | Category | System/file | Owner | Validator | Format | Expected date | Authoritative? | Unique key | History cutoff | Secure location | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |

## Import batch record

- Batch ID:
- Stage/release ID:
- Environment:
- Source IDs:
- Source checksums:
- Mapping version/commit:
- Target schema/app version:
- Started/completed:
- Operator:
- Source rows:
- Accepted rows:
- Imported rows:
- Rejected rows:
- Held rows:
- Duplicate rows:
- Updated rows:
- Variance summary:
- Rejection/exception evidence:
- Code rollback plan:
- Data correction/reversal plan:
- Backup/restore point:
- Validator and decision:

## Rules

## Phase 02 closure note

Phase 02 used synthetic staging records only. The protected PASS run
`35506309957` created no Champion data migration batch and production was not
targeted or changed. Phase 03 identity validation must continue to use
disposable synthetic identities and mappings; it is not Champion acceptance or
production data migration.

- Preserve untouched source copies and work only from controlled copies.
- Never place Champion source records in Git, public links, reseller demos, AI prompts, ordinary logs, or synthetic tenants.
- No Champion file is received until the secure-transfer location, access list, retention, and credential rotation are complete.
- Never clean the only source copy or manually repair production as the primary migration method.
- A rerun against the same clean state must produce the same result.
- Every transformation is versioned and testable.
- Code rollback and imported-data correction are separate plans.
- After users begin production work, an old full-site restore may destroy new records; use a tested batch correction/reversal unless an approved cutover rollback still applies.
- Accepted exceptions remain visible in the migration and handover records.
