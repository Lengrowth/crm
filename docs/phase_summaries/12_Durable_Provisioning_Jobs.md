# Phase 12 — Durable Provisioning Jobs and Observability

Summary

This phase introduces a durable, DB-backed provisioning job table and a simple in-process worker for running provisioning workflows deterministically in tests and during operational re-runs.

What was added

- Model: `ProvisioningJob` (already present) is used to store queued provisioning work with `status`, `attempt_count`, `logs_json`, and `error_message`.
- Service: `app.services.provisioning_service` with methods:
  - `queue_provisioning_job(session, tenant_id, job_type, requested_by_user_id, payload)`
  - `get_job(session, job_id)`
  - `list_jobs_for_tenant(session, tenant_id)`
  - `append_job_log(session, job, entry)`
  - `update_job_status(session, job, status, err)`
- Worker: `app.workers.provisioning_worker.run_next_job(session, client=None, max_attempts=3)`
  - Picks the next queued job, marks it running, increments `attempt_count`, runs the provisioning via the existing `PersistentERPNextService`, records logs, and updates status.
  - On failure it will re-queue the job for retries until `max_attempts` is reached.
- API endpoints:
  - POST `/tenants/{tenant_id}/provisioning_jobs` — queue a provisioning job
  - GET `/tenants/{tenant_id}/provisioning_jobs` — list jobs for a tenant
  - GET `/provisioning_jobs/{job_id}` — get a job by id
- Tests: `backend/tests/test_provisioning_jobs.py` exercises queueing, worker retry, and successful completion.

Operational notes / Runbook

- Inspect jobs directly in the DB table `provisioning_jobs`. Important columns: `id`, `tenant_id`, `status`, `attempt_count`, `started_at`, `finished_at`, `error_message`, `logs_json`.
- To re-run failed or queued jobs manually in a dev environment you can run a small script that opens a DB session and calls `run_next_job(session)` repeatedly until no queued jobs remain.

Example quick re-run (python REPL):

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.workers.provisioning_worker import run_next_job
from app.core.config import settings
from app.db.session import SessionLocal

session = SessionLocal()
while True:
    job = run_next_job(session)
    if not job:
        break
    print(f"Ran job {job.id} status={job.status} attempts={job.attempt_count}")

Notes and next steps

- This phase intentionally avoids external queue systems (RabbitMQ/Celery/Kafka). The worker is synchronous and invokable directly by tests or an operator.
- Future phases should add a scheduler/queue adapter and support locking to handle multiple worker processes.
- Consider adding a `payload_json` column to the `ProvisioningJob` model for clearer semantics if payloads get more complex.
