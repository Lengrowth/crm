from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.integrations.mock_erpnext import MockERPNextClient
from app.models.domain import Organization, SaaSUser, Tenant
from app.services.billing_provider import MockBillingProvider
from app.services.billing_service import BillingService
from app.services.onboarding_service import OnboardingService
from app.workers.provisioning_worker import run_next_job


def make_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    return Session()


def test_full_onboarding_flow():
    session = make_session()

    # create a user to act as the organization owner
    user = SaaSUser(email="owner@example.test", full_name="Owner", status="active")
    session.add(user)
    session.commit()
    session.refresh(user)

    # create a plan
    billing = BillingService(provider=MockBillingProvider())
    plan = billing.create_plan(session, name="Pilot", slug="pilot", price_cents=5000)

    # run onboarding orchestration
    onboarding = OnboardingService(billing_provider=MockBillingProvider())

    org_payload = {"name": "Pilot Org", "billing_email": "billing@pilot.test"}
    tenant_payload = {"tenant_slug": "pilot-org"}
    result = onboarding.onboard_pilot_organization(
        session,
        user,
        org_payload,
        tenant_payload,
        plan_slug=plan.slug,
        site_options={"domain": "pilot.local"},
        run_provision_now=False,  # we will run worker explicitly below
    )

    # verify intermediate records
    org = result["organization"]
    tenant = result["tenant"]
    subscription = result["subscription"]
    invoice = result["invoice"]
    job = result["provisioning_job"]

    assert isinstance(org, Organization)
    assert tenant.organization_id == org.id
    assert subscription.organization_id == org.id
    assert invoice.organization_id == org.id
    assert job.tenant_id == tenant.id
    assert job.status in ("queued", "queued")

    # run provisioning worker (use MockERPNextClient so no external calls)
    client = MockERPNextClient()
    job_after = run_next_job(session, client=client)
    assert job_after is not None
    assert job_after.status == "success"

    # refresh tenant and assert provisioning status updated by worker
    session.refresh(tenant)
    assert tenant.provisioning_status == "ready"
    assert tenant.status == "ready"

    # simulate invoice.paid webhook
    billing.process_webhook(
        session, {"event": "invoice.paid", "data": {"invoice_id": invoice.id}}
    )
    session.refresh(invoice)
    assert invoice.status == "paid"
    assert invoice.paid_at is not None

    # ensure subscription still active
    session.refresh(subscription)
    assert subscription.status == "active"
