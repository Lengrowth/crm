from __future__ import annotations

from datetime import timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.core.config import settings
from app.db.base import Base
from app.db.seed import seed_reference_data
from app.integrations.mock_erpnext import MockERPNextClient
from app.models.domain import (
    OnboardingRequest,
    OnboardingRequestVersion,
    ProvisioningJob,
    ProvisioningStep,
    SaaSUser,
    Tenant,
    utcnow,
)
from app.schemas.onboarding import (
    OnboardingPayload,
    OperatorExecutionAuthorization,
    OperatorReviewAction,
    PublicOnboardingCreate,
    PublicOnboardingRevision,
)
from app.services.onboarding_service import (
    OnboardingConflict,
    OnboardingTransitionError,
    phase4_onboarding_service,
)
from app.services.provisioning_service import provisioning_service
from app.workers.provisioning_worker import run_next_job


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)()
    seed_reference_data(session)
    return session


def payload() -> OnboardingPayload:
    return OnboardingPayload(
        company_name="Synthetic Second Company",
        legal_name="Synthetic Second Company LLC",
        industry="field_service",
        administrator_name="Synthetic Operator",
        administrator_email="synthetic-admin@acmephase4.com",
        requested_modules=["crm", "field_ops"],
        desired_domain="synthetic-second.example.test",
        desired_infrastructure="isolated_synthetic",
        implementation_notes="Synthetic Phase 4 validation only.",
    )


def test_public_request_is_versioned_and_idempotent_without_side_effects():
    session = make_session()
    original_flags = settings.feature_flags
    settings.feature_flags = "onboarding_public_intake=true"
    try:
        result = phase4_onboarding_service.create_public(session, PublicOnboardingCreate(idempotency_key="phase4-idempotency-1", payload=payload()))
        replay = phase4_onboarding_service.create_public(session, PublicOnboardingCreate(idempotency_key="phase4-idempotency-1", payload=payload()))
        assert replay.request_id == result.request_id
        assert replay.replayed is True
        assert replay.management_token is None
        try:
            phase4_onboarding_service.create_public(session, PublicOnboardingCreate(idempotency_key="phase4-idempotency-1", payload=payload().model_copy(update={"company_name": "Different Company"})))
        except OnboardingConflict:
            pass
        else:
            raise AssertionError("conflicting idempotency payload must be rejected")
        assert session.query(OnboardingRequest).count() == 1
        assert session.query(Tenant).count() == 0
        assert session.query(ProvisioningJob).count() == 0
        revised = phase4_onboarding_service.revise_public(session, result.request_id, result.management_token or "", PublicOnboardingRevision(idempotency_key="phase4-revision-1", payload=payload().model_copy(update={"requested_modules": ["crm"]})))
        assert revised.version == 2
    finally:
        settings.feature_flags = original_flags
        session.close()


def test_approval_conversion_and_durable_synthetic_provisioning():
    session = make_session()
    original_flags = settings.feature_flags
    settings.feature_flags = "onboarding_public_intake=true,onboarding_conversion=true,onboarding_execution=true,onboarding_synthetic_allowlist=true,onboarding_real_execution=false"
    try:
        operator = SaaSUser(email="phase4-operator@example.test", full_name="Phase 4 Operator", status="active", is_platform_admin=True)
        session.add(operator)
        session.commit()
        created = phase4_onboarding_service.create_public(session, PublicOnboardingCreate(idempotency_key="phase4-e2e-1", payload=payload()))
        phase4_onboarding_service.submit_public(session, created.request_id, created.management_token or "")
        phase4_onboarding_service.begin_review(session, operator, created.request_id, OperatorReviewAction(version=1, reason="Synthetic review started."))
        approved = phase4_onboarding_service.approve(session, operator, created.request_id, OperatorReviewAction(version=1, reason="Synthetic scope approved."))
        converted = phase4_onboarding_service.convert(session, operator, created.request_id)
        assert converted.organization_id and converted.tenant_id and converted.provisioning_job_id
        assert session.query(Tenant).count() == 1
        job = session.get(ProvisioningJob, converted.provisioning_job_id)
        assert job is not None and job.status == "awaiting_execution_authorization"
        assert session.query(ProvisioningStep).filter(ProvisioningStep.job_id == job.id).count() == 15
        authorized = phase4_onboarding_service.authorize_execution(session, operator, created.request_id, OperatorExecutionAuthorization(version=1, confirmation="authorize_isolated_synthetic_execution", reason="Synthetic isolated target confirmed."))
        assert authorized.state == "provisioning"
        first_claim = provisioning_service.claim_next_job(session, "worker-one")
        assert first_claim is not None
        assert provisioning_service.claim_next_job(session, "worker-two") is None
        first_claim.status, first_claim.worker_id, first_claim.lease_expires_at = "queued", None, None
        session.commit()
        completed = run_next_job(session)
        assert completed is not None and completed.status == "success"
        request = session.get(OnboardingRequest, created.request_id)
        assert request is not None and request.state == "ready"
        assert session.query(ProvisioningStep).filter(ProvisioningStep.job_id == completed.id, ProvisioningStep.status != "success").count() == 0
        assert all("password" not in str(item).lower() and "token" not in str(item).lower() for item in completed.logs_json)
    finally:
        settings.feature_flags = original_flags
        session.close()


def test_failed_step_is_not_ready_and_can_resume_after_injection_removed():
    session = make_session()
    original_flags = settings.feature_flags
    settings.feature_flags = "onboarding_public_intake=true,onboarding_conversion=true,onboarding_execution=true,onboarding_synthetic_allowlist=true,onboarding_real_execution=false"
    try:
        operator = SaaSUser(email="phase4-recovery@example.test", full_name="Recovery Operator", status="active", is_platform_admin=True)
        session.add(operator)
        session.commit()
        created = phase4_onboarding_service.create_public(session, PublicOnboardingCreate(idempotency_key="phase4-recovery-1", payload=payload()))
        phase4_onboarding_service.submit_public(session, created.request_id, created.management_token or "")
        phase4_onboarding_service.begin_review(session, operator, created.request_id, OperatorReviewAction(version=1, reason="Review."))
        phase4_onboarding_service.approve(session, operator, created.request_id, OperatorReviewAction(version=1, reason="Approve synthetic recovery."))
        converted = phase4_onboarding_service.convert(session, operator, created.request_id)
        phase4_onboarding_service.authorize_execution(session, operator, created.request_id, OperatorExecutionAuthorization(version=1, confirmation="authorize_isolated_synthetic_execution", reason="Confirm recovery lane."))
        version = session.execute(select(OnboardingRequestVersion).where(OnboardingRequestVersion.request_id == created.request_id, OnboardingRequestVersion.version == 1)).scalar_one()
        snapshot = dict(version.snapshot_json)
        snapshot["failure_inject_step"] = "health_checks"
        version.snapshot_json = snapshot
        session.commit()
        client = MockERPNextClient()
        failed_attempt = run_next_job(session, client=client)
        assert failed_attempt is not None and failed_attempt.status == "queued"
        request = session.get(OnboardingRequest, created.request_id)
        assert request is not None and request.state == "validation"
        version.snapshot_json = {key: value for key, value in snapshot.items() if key != "failure_inject_step"}
        job = session.get(ProvisioningJob, converted.provisioning_job_id)
        assert job is not None
        job.next_attempt_at = utcnow()
        session.commit()
        recovered = run_next_job(session, client=client)
        assert recovered is not None and recovered.status == "success"
        session.refresh(request)
        assert request.state == "ready"
    finally:
        settings.feature_flags = original_flags
        session.close()


def test_expired_validation_lease_is_reclaimed_and_fenced():
    session = make_session()
    tenant = Tenant(organization_id="org-lease", tenant_slug="lease-tenant", environment="staging")
    session.add(tenant)
    session.commit()
    job = provisioning_service.queue_provisioning_job(session, tenant.id, "provision_tenant")
    first = provisioning_service.claim_next_job(session, "crashed-worker")
    assert first is not None
    first.status = "validation"
    first.lease_expires_at = utcnow() - timedelta(seconds=1)
    stale_token = first.lease_token
    first.lease_token = stale_token
    step = ProvisioningStep(job_id=first.id, step_key="validate_approved_request", ordinal=1, status="running", worker_id="crashed-worker")
    session.add_all([first, step])
    session.commit()

    reclaimed = provisioning_service.claim_next_job(session, "replacement-worker")
    assert reclaimed is not None
    assert reclaimed.status == "running"
    assert reclaimed.worker_id == "replacement-worker"
    assert reclaimed.lease_token and reclaimed.lease_token != stale_token
    session.refresh(step)
    assert step.status == "queued"
    assert step.worker_id is None
