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
- `release/phase4_synthetic_smoke.py` drives one isolated, synthetic-only
  onboarding request through review, conversion, separately authorized worker
  execution, status/event checks, and exact cleanup; it refuses production
  hostnames and never sends first-login credentials or creates billing records.
- Set `REQUIRE_AUTH_SMOKE=true` and provide an operator token through `AUTH_TOKEN_FILE` for authenticated `/auth/me` and API checks; the token contents are never printed.
- `release/local_smoke.py` runs that smoke contract against disposable local frontend/backend services and a temporary SQLite database.
  When the repository-local `backend/.venv` is unavailable, pass an explicit
  valid environment with `LOCAL_SMOKE_PYTHON=<python.exe>` and
  `LOCAL_SMOKE_ALEMBIC_AS_MODULE=true`; the smoke remains disposable and does
  not silently claim the missing default environment.
- `release/cleanup_phase2_synthetic.py` removes only the exact company/site IDs
  emitted by the candidate-bound Phase 2 browser artifact.
- `release/rehearse_slots.py` proves candidate idempotency, preflight rejection, failed-health rollback including a first-deploy-without-known-good case, manual rollback, and production-pointer isolation in a disposable filesystem rehearsal.
- `release/rehearse_backup_restore.py --self-test` upgrades a restored disposable control-plane database to Alembic head and verifies database, site-config, public-file, and private-file recovery without using production data.
- `release/verify_upstream_clean.sh` fails on dirty or unpinned upstream Frappe/ERPNext trees, including when an expected SHA is missing.
- `release/secret_scan.py` reports only paths and never matching credential content.
- `deploy/deploy_saas_control.sh` is staging-only, performs automatic code-pointer rollback, and records a per-candidate successful staging-smoke marker.
- `release/verify_phase4_evidence.py` verifies candidate-bound Phase 4 success and recovery artifacts and rejects evidence that started or completed after the promotion request.
- `release/materialize_production_candidate.sh` verifies Phase 4 evidence on every path, including an already-materialized production candidate, then copies only the exact, smoke-marked staging candidate into the production release root.
- `release/production_smoke_auth.py` creates and removes the uniquely named, disposable authenticated smoke identity used by the protected production workflow; it never prints token values.
- `deploy/promote_saas_control.sh` is the separate explicit production promotion path and rejects candidates without the exact staging-smoke marker and the materializer's verified Phase 4 evidence marker.
