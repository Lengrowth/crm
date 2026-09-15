# Scripts

Helper scripts for local development and future automation will live here.

Keep scripts small, explicit, and phase-specific.

Release safety scripts are intentionally split by responsibility:

- `release/build_candidate.sh` creates an immutable candidate from an exact Git ref.
- Set `CUSTOM_APP_REPO`/`CUSTOM_APP_REF` when building to package the clean pinned `lenerp_core` artifact alongside the control-plane candidate.
- `release/build_manifest.py` writes non-secret release identity, dependency hashes, and installed-app commit/version identities.
- `release/preflight.sh` validates a built candidate before traffic.
- `release/smoke.sh` validates public, backend, ERP runtime, release identity, and manifest-installed-app identity endpoints.
- `release/erp_staging_smoke.sh` validates the isolated EC2 ERP staging bench,
  pinned Frappe/ERPNext/custom-app inventory, private ports, workers, and
  unauthenticated ERP API behavior.
- Set `REQUIRE_AUTH_SMOKE=true` and provide an operator token through `AUTH_TOKEN_FILE` for authenticated `/auth/me` and API checks; the token contents are never printed.
- `release/local_smoke.py` runs that smoke contract against disposable local frontend/backend services and a temporary SQLite database.
- `release/rehearse_slots.py` proves candidate idempotency, preflight rejection, failed-health rollback including a first-deploy-without-known-good case, manual rollback, and production-pointer isolation in a disposable filesystem rehearsal.
- `release/rehearse_backup_restore.py --self-test` upgrades a restored disposable control-plane database to Alembic head and verifies database, site-config, public-file, and private-file recovery without using production data.
- `release/verify_upstream_clean.sh` fails on dirty or unpinned upstream Frappe/ERPNext trees, including when an expected SHA is missing.
- `release/secret_scan.py` reports only paths and never matching credential content.
- `deploy/deploy_saas_control.sh` is staging-only, performs automatic code-pointer rollback, and records a per-candidate successful staging-smoke marker.
- `deploy/promote_saas_control.sh` is the separate explicit production promotion path and rejects candidates without that exact staging-smoke marker.
