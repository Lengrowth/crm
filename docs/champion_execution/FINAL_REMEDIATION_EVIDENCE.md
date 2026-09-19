# Champion Pre-Kickoff Remediation Evidence

## Candidate-bound record

This file is shipped inside the CRM candidate source and is copied into the
protected evidence artifact by the workflow. The artifact manifest is the
authority for the exact CRM candidate SHA, workflow run, artifact name, and
documentation hash. The pinned LenERP Core app for the protected candidate is
`a7e47208baf6583295f5f2632f4787262cd3f475`.

## Protected checks

- Candidate-bound manifest: runtime release, installed custom app, and this documentation snapshot must match the exact candidate hashes.
- CRM browser evidence: all audited customer-facing routes passed the language audit with 0 findings.
- ERP accessibility: login, 9 authenticated routes, desktop, and mobile must record 0 serious axe violations and a non-empty per-result incomplete review record when axe reports incomplete checks.
- ERP accessibility contract: viewport metadata is present, browser zoom is allowed, and login logos have accessible alternatives.
- C08 dashboard evidence: persisted jobs, wells, invoices, inventory exceptions, asset status, maintenance status/tasks, well history, and operational alerts are required in the browser evidence.
- Role and synthetic evidence: protected role boundaries, print, export, responsive captures, and cleanup artifacts are present.
- Cleanup: Phase 2 exact-record manifest contains 3 organizations and 3 tenants; Phase 3 exact-record manifest contains 1 organization and 1 tenant; role and disposable identities were removed by the workflow.
- Test accounting: the complete Core checkout runs `python -m pytest -q` → 8 passed; CRM’s targeted release-contract subset runs `python -m pytest -q scripts/release/test_erp_demo_contract.py scripts/release/test_verify_phase4_evidence.py` → 7 passed. Candidate-bound CI supplies the CRM 56 backend and 12 frontend results.

## Disposition

`CHAMPION PRE-KICKOFF SYNTHETIC DEMO REMEDIATION: READY FOR INDEPENDENT REVIEW`

This is a remediation-readiness verdict only. It does not award independent PASS, Champion acceptance, real-data authorization, production activation, or Phase 6 approval.
