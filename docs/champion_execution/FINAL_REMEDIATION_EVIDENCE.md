# Champion Pre-Kickoff Remediation Evidence

## Candidate-bound record

This file is shipped inside the CRM candidate source and is copied into the
protected evidence artifact by the workflow. The final Phase 02 artifact
manifest is the authority for the exact candidate-bound release
`fa137051b6675fbd09102c07942748ce68ea98b9`, workflow run `35505538638`,
artifact name, and documentation hash. The pinned LenERP Core app is
`a7e47208baf6583295f5f2632f4787262cd3f475`.

## Protected checks

- Candidate-bound manifest: runtime release, installed custom app, and this documentation snapshot must match the exact candidate hashes.
- CRM browser evidence: all audited customer-facing routes passed the language audit with 0 findings.
- ERP accessibility: login, 9 authenticated routes, desktop, and mobile must record 0 serious axe violations and a non-empty per-result incomplete review record when axe reports incomplete checks.
- ERP accessibility contract: viewport metadata is present, browser zoom is allowed, and login logos have accessible alternatives.
- C08 dashboard evidence: persisted jobs, wells, invoices, inventory exceptions, asset status, maintenance status/tasks, well history, and operational alerts are required in the browser evidence.
- Role and synthetic evidence: protected role boundaries, print, export, responsive captures, and cleanup artifacts are present.
- Cleanup: Phase 2 pre-capture cleanup removed 3 stale synthetic organizations and 3 tenants; the final Phase 2 manifest removed 3 organizations and 3 tenants. No Phase 3 synthetic records were created; role and disposable identities were removed by the workflow.
- Test accounting: local validation passed the complete backend suite (74 tests), frontend suite (12 tests), release package tests (9 tests), and focused contract/manifest checks (5 tests). Candidate-bound run `35505538638` passed the staging validation suite and uploaded the evidence artifact.

## Disposition

`PHASE 02 HRMS AND DEPENDENCY REMEDIATION: READY FOR INDEPENDENT REVIEW`

This is a remediation-readiness verdict only. It does not award independent PASS, Champion acceptance, real-data authorization, production activation, or Phase 6 approval.

## Phase 03 bootstrap and protected staging record

The zero-job run `35544065745` was not valid protected evidence. Its PR workflow
contained invalid YAML (an extra leading space before the
`EXPECTED_CUSTOM_APP_COMMIT` mapping), and the registered default-branch copy
only selected `push` events for `main`; therefore the PR-branch push had no
eligible job. Action-aware validation also rejected the PR workflow before any
job could start. The failure was not solely a default-branch registration issue.

The minimal safe bootstrap was merged normally through [PR #83](https://github.com/Lengrowth/crm/pull/83)
at `854460e8c1a94fcbf844b18878023ab87d665f09`. It preserved the required job
name `Build one immutable candidate and deploy staging`, keeps the Phase 03
lane default-off, validates same-repository immutable candidate refs, and
retains staging-only permissions and cleanup.

The final protected push run for PR #82 was run `35583191594`, job
`106280466398`, against control-plane commit
`47b15d89a2dba0709b226fa2a2b44f758ef0ee95`; it passed the required check and
uploaded artifact ID `10631363593`, named
`staging-browser-evidence-47b15d89a2dba0709b226fa2a2b44f758ef0ee95`, digest
`sha256:c539d39a1d3699d00025ea93329ea82b92519dc5a8c261ceedf77e58593e92a7`.
The candidate-bound manifest records canonical LenERP commit
`8d77cec7504d22f9c0a235034777e31fa07fc62` and bundle SHA-256
`D136208D613DEECE9A51F25A7A1A5B4C7C916D8E657043FFFC7BEEC03B90AAA7`.

The protected lane passed CRM/frontend/release/LenERP validation, browser SSO
and bidirectional navigation, replay/PKCE/state/redirect/tenant/membership/
role denial checks, membership revocation, break-glass before enablement and
after rollback, and deterministic rollback readiness. Cleanup removed identity
records, role principals, browser records, temporary files/configuration and
synthetic ERP records; the ERP read-only reset ended with zero synthetic
`LenERP Well Site` and `LenERP Drilling Job` records. Production SSO,
production infrastructure, Cloudflare, and temporary AWS SSH access were not
changed. PR #82 is merged at
`c7b0b4e40b6e5ac31ab244cde2303fc83a884d36`; the merge did not deploy to
production or start Phase 04. This correction record is the authoritative
merged-state update for independent review.
