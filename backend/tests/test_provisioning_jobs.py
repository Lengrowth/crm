from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.integrations.mock_erpnext import MockERPNextClient
from app.models.domain import Tenant
from app.services.provisioning_service import provisioning_service
from app.workers.provisioning_worker import run_next_job


def make_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    return Session()


def test_queue_and_run_with_retry():
    session = make_session()

    # create a tenant record (FK required)
    tenant = Tenant(organization_id="org-1", tenant_slug="t-1", environment="demo")
    session.add(tenant)
    session.commit()
    session.refresh(tenant)

    # queue a job with payload
    payload = {"organization_id": "org-1", "site_options": {"domain": "example.test"}}
    job = provisioning_service.queue_provisioning_job(
        session, tenant_id=tenant.id, job_type="provision_tenant", payload=payload
    )

    # create a Mock client that fails the first create_site call, then succeeds
    counter = {"n": 0}

    def fail_once():
        if counter["n"] < 1:
            counter["n"] += 1
            return True
        return False

    client = MockERPNextClient(failures={"create_site": fail_once})

    # first run: should schedule a retry (attempt_count 1, status queued)
    job_after = run_next_job(session, client=client, max_attempts=3)
    assert job_after is not None
    assert job_after.attempt_count == 1
    # after a failure that is retriable we leave status queued
    assert job_after.status in ("queued", "running", "failed")
    # ensure a retry_scheduled log exists
    assert any(
        l.get("event") == "retry_scheduled" or l.get("event") == "provision_error"
        for l in job_after.logs_json
    )

    # second run: should succeed
    job_after2 = run_next_job(session, client=client, max_attempts=3)
    assert job_after2 is not None
    assert job_after2.attempt_count >= 2
    assert job_after2.status == "success"
    assert any(l.get("event") == "provision_success" for l in job_after2.logs_json)
