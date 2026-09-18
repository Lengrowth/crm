from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
from datetime import timedelta, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.domain import (
    DomainMapping,
    FirstLoginHandoff,
    ImplementationProject,
    ImplementationTask,
    ModuleEntitlementAudit,
    OnboardingDecision,
    OnboardingManagementCredential,
    OnboardingRequest,
    OnboardingRequestVersion,
    Organization,
    OrganizationMembership,
    OrganizationModule,
    ProvisioningJob,
    ProvisioningEvent,
    ProvisioningOutboxEvent,
    ProvisioningStep,
    SaaSUser,
    Tenant,
    utcnow,
)
from app.schemas.control import OrganizationCreateRequest, TenantCreateRequest
from app.schemas.onboarding import (
    OnboardingPayload,
    OperatorExecutionAuthorization,
    OperatorReviewAction,
    OperatorOnboardingRead,
    PublicOnboardingCreate,
    PublicOnboardingRead,
    PublicOnboardingResult,
    PublicOnboardingRevision,
    OperatorRetryRequest,
    ProvisioningEventRead,
    ProvisioningJobDetailRead,
    ProvisioningStepRead,
)
from app.services.billing_service import BillingService
from app.services.control_plane_service import ControlPlaneService
from app.services.module_entitlement_service import ModuleEntitlementError, module_entitlement_service
from app.services.provisioning_service import provisioning_service
from app.workers.provisioning_worker import run_next_job


ONBOARDING_STATES = {"draft", "submitted", "under_review", "approved", "provisioning", "validation", "failed", "ready", "rejected", "cancelled"}
STEP_DEFINITIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("validate_approved_request", ()),
    ("reserve_site_name", ("validate_approved_request",)),
    ("create_isolated_site", ("reserve_site_name",)),
    ("install_pinned_erpnext", ("create_isolated_site",)),
    ("install_lenerp_custom_app", ("install_pinned_erpnext",)),
    ("apply_approved_modules", ("install_lenerp_custom_app",)),
    ("apply_roles_workspaces", ("apply_approved_modules",)),
    ("apply_branding_configuration", ("apply_roles_workspaces",)),
    ("prepare_domain_binding", ("apply_branding_configuration",)),
    ("bind_domain_ssl", ("prepare_domain_binding",)),
    ("create_admin_handoff", ("apply_branding_configuration",)),
    ("health_checks", ("create_admin_handoff", "bind_domain_ssl")),
    ("verify_apps_modules", ("health_checks",)),
    ("prepare_first_login", ("verify_apps_modules",)),
    ("mark_ready", ("prepare_first_login",)),
)


class OnboardingError(Exception):
    pass


class OnboardingConflict(OnboardingError):
    pass


class OnboardingNotFound(OnboardingError):
    pass


class OnboardingAccessError(OnboardingError):
    pass


class OnboardingTransitionError(OnboardingError):
    pass


class OnboardingValidationError(OnboardingError):
    pass


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _payload_hash(payload: OnboardingPayload) -> str:
    encoded = json.dumps(payload.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return _hash(encoded)


def _safe_slug(value: str, suffix: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "company"
    return f"{base[:90]}-{suffix[:8]}"[:120]


class Phase4OnboardingService:
    """Public intake, operator decisions, and atomic control-plane conversion."""

    def _flag(self, name: str, default: bool = False) -> bool:
        return settings.feature_flag_map.get(name, default)

    def create_public(self, session: Session, payload: PublicOnboardingCreate) -> PublicOnboardingResult:
        if not self._flag("onboarding_public_intake"):
            raise OnboardingAccessError("Public onboarding intake is disabled by runtime policy.")
        request_hash = _payload_hash(payload.payload)
        existing = session.execute(select(OnboardingRequest).where(OnboardingRequest.idempotency_key == payload.idempotency_key)).scalar_one_or_none()
        if existing:
            if not hmac.compare_digest(existing.request_hash, request_hash):
                raise OnboardingConflict("This idempotency key was already used with a different request.")
            return self._result(existing, replayed=True)

        management_token = secrets.token_urlsafe(32)
        request = OnboardingRequest(idempotency_key=payload.idempotency_key, request_hash=request_hash, management_token_hash=_hash(management_token), state="draft", applicant_visible_status="draft", current_version=1)
        session.add(request)
        session.flush()
        session.add(self._make_version(request, payload.payload, payload.idempotency_key, 1, None))
        session.add(OnboardingManagementCredential(request_id=request.id, token_hash=_hash(management_token), expires_at=utcnow() + timedelta(days=30)))
        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise OnboardingConflict("The request could not be created safely; retry with a new idempotency key.") from exc
        session.refresh(request)
        return self._result(request, management_token=management_token)

    def read_public(self, session: Session, request_id: str, management_token: str) -> PublicOnboardingRead:
        return self._public_read(session, self._authorize_management(session, request_id, management_token))

    def revise_public(self, session: Session, request_id: str, management_token: str, payload: PublicOnboardingRevision) -> PublicOnboardingResult:
        if not self._flag("onboarding_public_intake"):
            raise OnboardingAccessError("Public onboarding intake is disabled by runtime policy.")
        request = self._authorize_management(session, request_id, management_token)
        if request.state not in {"draft", "submitted", "rejected"}:
            raise OnboardingTransitionError("This request cannot be revised in its current state.")
        request_hash = _payload_hash(payload.payload)
        prior = session.execute(select(OnboardingRequestVersion).where(OnboardingRequestVersion.request_id == request.id, OnboardingRequestVersion.version_idempotency_key == payload.idempotency_key)).scalar_one_or_none()
        if prior:
            if prior.request_hash != request_hash:
                raise OnboardingConflict("This revision idempotency key was already used with a different request.")
            return self._result(request, replayed=True)
        old_version = request.current_version
        request.current_version = old_version + 1
        request.state = "draft"
        request.applicant_visible_status = "draft"
        request.submitted_version = None
        request.approved_version = None
        request.approved_bundle_key = None
        request.approved_bundle_version = None
        request.approved_by_user_id = None
        request.approved_at = None
        request.execution_authorized_by_user_id = None
        request.execution_authorized_at = None
        request.rejection_reason = None
        session.add(self._make_version(request, payload.payload, payload.idempotency_key, request.current_version, old_version))
        session.commit()
        session.refresh(request)
        return self._result(request)

    def submit_public(self, session: Session, request_id: str, management_token: str) -> PublicOnboardingResult:
        if not self._flag("onboarding_public_intake"):
            raise OnboardingAccessError("Public onboarding intake is disabled by runtime policy.")
        request = self._authorize_management(session, request_id, management_token)
        if request.state != "draft":
            raise OnboardingTransitionError("Only a draft request can be submitted.")
        version = self._current_version(session, request)
        try:
            module_entitlement_service.validate_requested_selection(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
        except ModuleEntitlementError as exc:
            raise OnboardingValidationError(str(exc)) from exc
        version.submitted_at = utcnow()
        request.submitted_version = version.version
        request.state = "submitted"
        request.applicant_visible_status = "submitted"
        session.commit()
        session.refresh(request)
        return self._result(request)

    def list_operator(self, session: Session, state: Optional[str] = None, limit: int = 100) -> list[OperatorOnboardingRead]:
        statement = select(OnboardingRequest).order_by(OnboardingRequest.updated_at.desc()).limit(max(1, min(limit, 200)))
        if state:
            if state not in ONBOARDING_STATES:
                raise OnboardingValidationError("Unknown onboarding state.")
            statement = statement.where(OnboardingRequest.state == state)
        return [self._operator_read(session, item) for item in session.execute(statement).scalars().all()]

    def get_operator(self, session: Session, request_id: str) -> OperatorOnboardingRead:
        return self._operator_read(session, self._get_request(session, request_id))

    def begin_review(self, session: Session, actor: SaaSUser, request_id: str, action: OperatorReviewAction) -> OperatorOnboardingRead:
        request = self._get_request(session, request_id)
        self._require_version(request, action.version)
        self._transition(request, {"submitted"}, "under_review")
        request.applicant_visible_status = "under_review"
        self._decision(session, request, action.version, actor, "under_review", action.reason)
        session.commit()
        return self._operator_read(session, request)

    def approve(self, session: Session, actor: SaaSUser, request_id: str, action: OperatorReviewAction) -> OperatorOnboardingRead:
        request = self._get_request(session, request_id)
        version = self._current_version(session, request)
        self._require_version(request, action.version)
        if request.state != "under_review":
            raise OnboardingTransitionError("Only a request under review can be approved.")
        try:
            module_entitlement_service.validate_requested_selection(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
        except ModuleEntitlementError as exc:
            raise OnboardingValidationError(str(exc)) from exc
        request.state = "approved"
        request.applicant_visible_status = "approved"
        request.approved_version = version.version
        request.approved_bundle_key = version.bundle_key
        request.approved_bundle_version = version.bundle_version
        request.approved_by_user_id = actor.id
        request.approved_at = utcnow()
        request.rejection_reason = None
        self._decision(session, request, version.version, actor, "approved", action.reason, version.bundle_key, version.bundle_version)
        session.commit()
        return self._operator_read(session, request)

    def reject(self, session: Session, actor: SaaSUser, request_id: str, action: OperatorReviewAction) -> OperatorOnboardingRead:
        request = self._get_request(session, request_id)
        self._require_version(request, action.version)
        if request.state not in {"submitted", "under_review", "approved"}:
            raise OnboardingTransitionError("This request cannot be rejected in its current state.")
        request.state = "rejected"
        request.applicant_visible_status = "rejected"
        request.rejection_reason = action.reason
        self._decision(session, request, action.version, actor, "rejected", action.reason)
        session.commit()
        return self._operator_read(session, request)

    def cancel(self, session: Session, actor: SaaSUser, request_id: str, action: OperatorReviewAction) -> OperatorOnboardingRead:
        request = self._get_request(session, request_id)
        self._require_version(request, action.version)
        if request.state in {"ready", "cancelled"}:
            raise OnboardingTransitionError("This request is already terminal.")
        request.state = "cancelled"
        request.applicant_visible_status = "cancelled"
        request.cancellation_reason = action.reason
        if request.provisioning_job_id:
            job = session.get(ProvisioningJob, request.provisioning_job_id)
            if job and job.status not in {"success", "failed", "cancelled"}:
                job.cancel_requested_at = utcnow()
        self._decision(session, request, action.version, actor, "cancelled", action.reason)
        session.commit()
        return self._operator_read(session, request)

    def convert(self, session: Session, actor: SaaSUser, request_id: str) -> OperatorOnboardingRead:
        if not self._flag("onboarding_conversion"):
            raise OnboardingAccessError("Onboarding conversion is disabled by runtime policy.")
        request = self._get_request(session, request_id)
        if request.state != "approved" or request.approved_version != request.current_version:
            raise OnboardingTransitionError("The approved request version is stale or not convertible.")
        if request.organization_id:
            return self._operator_read(session, request)
        version = self._current_version(session, request)
        try:
            modules = module_entitlement_service.resolve_requested_codes(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
        except ModuleEntitlementError as exc:
            raise OnboardingValidationError(str(exc)) from exc
        snapshot = version.snapshot_json
        requested_domain = str(snapshot.get("desired_domain") or "").strip().lower() or None
        if requested_domain:
            if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]{0,251}[a-z0-9])?", requested_domain) or ".." in requested_domain:
                raise OnboardingValidationError("The requested domain is not a valid hostname.")
            if requested_domain in {"lenerp.lengrowth.com", "lenerp-api.lengrowth.com", "erp.lengrowth.com", "www.lengrowth.com"}:
                raise OnboardingValidationError("Production control-plane and ERP domains cannot be used for synthetic onboarding.")
            if session.execute(select(DomainMapping).where(DomainMapping.domain == requested_domain)).scalar_one_or_none():
                raise OnboardingConflict("The requested domain is already reserved.")
        now = utcnow()
        org = Organization(name=str(snapshot["company_name"]), legal_name=snapshot.get("legal_name"), industry=snapshot.get("industry"), country=snapshot.get("country"), timezone=snapshot.get("timezone"), billing_email=snapshot.get("billing_email"), status="trial")
        session.add(org)
        session.flush()
        admin_email = str(snapshot["administrator_email"]).lower()
        admin = session.execute(select(SaaSUser).where(SaaSUser.email == admin_email)).scalar_one_or_none()
        if admin is None:
            admin = SaaSUser(email=admin_email, full_name=str(snapshot["administrator_name"]), status="invited", password_hash=None)
            session.add(admin)
            session.flush()
        session.add(OrganizationMembership(organization_id=org.id, user_id=admin.id, role="owner"))
        tenant = Tenant(organization_id=org.id, tenant_slug=_safe_slug(str(snapshot["company_name"]), request.id), environment="staging", status="planned", primary_domain=requested_domain, provisioning_status="pending")
        session.add(tenant)
        session.flush()
        project = ImplementationProject(organization_id=org.id, tenant_id=tenant.id, status="discovery", owner_user_id=actor.id)
        session.add(project)
        session.flush()
        for order, title in enumerate(("Validate onboarding scope", "Confirm users and roles", "Configure approved modules", "Complete isolated verification", "Prepare first login"), start=1):
            session.add(ImplementationTask(implementation_project_id=project.id, title=title, status="todo", sort_order=order * 10))
        for code in modules:
            module = module_entitlement_service.module_by_code(session, code)
            if module is None:
                raise OnboardingValidationError(f"Module {code} is unavailable.")
            session.add(OrganizationModule(organization_id=org.id, module_id=module.id, status="enabled", enabled_by=actor.id, enabled_at=now, explicit_state="enabled", requested_state="enabled", entitled_state="entitled", source_type="onboarding", source_ref=f"{request.id}@{version.version}", reason="Approved onboarding conversion", last_idempotency_key=f"onboarding:{request.id}:{version.version}", requested_at=now))
        session.add(ModuleEntitlementAudit(actor_user_id=actor.id, organization_id=org.id, operation="onboarding_conversion", previous_requested_json={"enabled": [], "disabled": []}, new_requested_json={"enabled": modules, "disabled": []}, previous_effective_json={"codes": [], "items": []}, new_effective_json={"codes": modules}, source_type="onboarding", source_ref=f"{request.id}@{version.version}", reason="Approved onboarding conversion", idempotency_key=f"onboarding:{request.id}:{version.version}", result="applied"))
        if requested_domain:
            session.add(DomainMapping(tenant_id=tenant.id, domain=requested_domain, type="custom_domain", status="reserved", is_active=False, manual_activation_required=True, ssl_status="unknown", notes_json={"source": "approved_onboarding", "dns_mutation": "deferred"}))
        job = ProvisioningJob(tenant_id=tenant.id, job_type="onboarding_provisioning", status="awaiting_execution_authorization", requested_by_user_id=actor.id, onboarding_request_id=request.id, onboarding_version=version.version, workflow_version="phase4-1", max_attempts=5, target_environment="staging", target_isolation_json={"lane": "isolated_synthetic", "site_namespace": f"phase4-{request.id[:8]}", "dns_mutation": "manual_only"}, logs_json=[{"event": "converted", "ts": now.isoformat(), "message": "Approved onboarding converted; execution remains separately authorized."}])
        session.add(job)
        session.flush()
        for ordinal, (key, deps) in enumerate(STEP_DEFINITIONS, start=1):
            session.add(ProvisioningStep(job_id=job.id, step_key=key, ordinal=ordinal, dependency_keys_json=list(deps)))
        session.add(ProvisioningOutboxEvent(aggregate_type="onboarding_request", aggregate_id=request.id, event_type="onboarding.conversion_committed", idempotency_key=f"onboarding-conversion:{request.id}:{version.version}", payload_json={"request_id": request.id, "version": version.version, "job_id": job.id}))
        session.add(FirstLoginHandoff(request_id=request.id, tenant_id=tenant.id, user_id=admin.id, status="pending_provisioning", delivery_status="disabled"))
        request.organization_id, request.tenant_id, request.implementation_project_id, request.provisioning_job_id, request.converted_at = org.id, tenant.id, project.id, job.id, now
        try:
            session.commit()
        except Exception as exc:
            session.rollback()
            raise OnboardingError("Approved onboarding conversion rolled back safely.") from exc
        session.refresh(request)
        return self._operator_read(session, request)

    def authorize_execution(self, session: Session, actor: SaaSUser, request_id: str, action: OperatorExecutionAuthorization) -> OperatorOnboardingRead:
        if not self._flag("onboarding_execution"):
            raise OnboardingAccessError("Provisioning execution is disabled by runtime policy.")
        request = self._get_request(session, request_id)
        self._require_version(request, action.version)
        if request.state != "approved" or request.approved_version != action.version or not request.provisioning_job_id:
            raise OnboardingTransitionError("Only an approved, converted request can authorize execution.")
        version = self._current_version(session, request)
        if version.snapshot_json.get("desired_infrastructure") != "isolated_synthetic":
            raise OnboardingAccessError("Only isolated synthetic targets may be executed in this phase.")
        if not self._flag("onboarding_synthetic_allowlist") or self._flag("onboarding_real_execution"):
            raise OnboardingAccessError("Synthetic execution is not enabled by the current runtime policy.")
        job = session.get(ProvisioningJob, request.provisioning_job_id)
        if job is None:
            raise OnboardingNotFound("Provisioning workflow not found.")
        request.execution_authorized_by_user_id, request.execution_authorized_at = actor.id, utcnow()
        request.state, request.applicant_visible_status, job.status, job.next_attempt_at = "provisioning", "provisioning", "queued", utcnow()
        self._decision(session, request, action.version, actor, "execution_authorized", action.reason, request.approved_bundle_key, request.approved_bundle_version, execution_authorized=True)
        session.commit()
        return self._operator_read(session, request)

    def job_detail(self, session: Session, job_id: str) -> ProvisioningJobDetailRead:
        job = session.get(ProvisioningJob, job_id)
        if job is None:
            raise OnboardingNotFound("Provisioning workflow not found.")
        steps = session.execute(select(ProvisioningStep).where(ProvisioningStep.job_id == job.id).order_by(ProvisioningStep.ordinal)).scalars().all()
        return ProvisioningJobDetailRead(job_id=job.id, tenant_id=job.tenant_id, onboarding_request_id=job.onboarding_request_id, status=job.status, workflow_version=job.workflow_version, attempt_count=job.attempt_count, next_attempt_at=job.next_attempt_at, lease_expires_at=job.lease_expires_at, steps=[ProvisioningStepRead.model_validate(step) for step in steps])

    def job_events(self, session: Session, job_id: str, limit: int = 200) -> list[ProvisioningEventRead]:
        if session.get(ProvisioningJob, job_id) is None:
            raise OnboardingNotFound("Provisioning workflow not found.")
        rows = session.execute(select(ProvisioningEvent).where(ProvisioningEvent.job_id == job_id).order_by(ProvisioningEvent.created_at.desc()).limit(max(1, min(limit, 500)))).scalars().all()
        return [ProvisioningEventRead.model_validate(row) for row in rows]

    def retry_step(self, session: Session, actor: SaaSUser, job_id: str, action: OperatorRetryRequest) -> ProvisioningJobDetailRead:
        job = session.get(ProvisioningJob, job_id)
        if job is None:
            raise OnboardingNotFound("Provisioning workflow not found.")
        step = session.execute(select(ProvisioningStep).where(ProvisioningStep.job_id == job.id, ProvisioningStep.step_key == action.step_key)).scalar_one_or_none()
        if step is None:
            raise OnboardingNotFound("Provisioning step not found.")
        if job.status in {"success", "cancelled"} or step.status not in {"failed", "queued"}:
            raise OnboardingTransitionError("This provisioning step is not eligible for retry.")
        if step.step_key in {"create_isolated_site", "bind_domain_ssl"} and action.confirmation != "confirm_irreversible_step":
            raise OnboardingAccessError("This step requires explicit operator confirmation before retry.")
        step.status, step.failure_category, step.sanitized_error, step.rollback_state = "pending", None, None, "not_started"
        job.status, job.worker_id, job.lease_token, job.lease_expires_at, job.next_attempt_at = "queued", None, None, None, utcnow()
        if request := session.get(OnboardingRequest, job.onboarding_request_id) if job.onboarding_request_id else None:
            if request.state == "failed":
                request.state = "provisioning"
                request.applicant_visible_status = "provisioning"
                session.add(request)
        provisioning_service._append_without_commit(job, {"event": "operator_retry_authorized", "message": action.reason, "step_key": action.step_key, "actor": actor.id})
        session.add_all([job, step])
        session.commit()
        return self.job_detail(session, job.id)

    def _make_version(self, request: OnboardingRequest, payload: OnboardingPayload, key: str, version: int, supersedes: Optional[int]) -> OnboardingRequestVersion:
        dump = payload.model_dump(mode="json")
        return OnboardingRequestVersion(request_id=request.id, version=version, version_idempotency_key=key, request_hash=_payload_hash(payload), snapshot_json=dump, requested_module_codes_json=list(payload.requested_modules), bundle_key=payload.bundle_key, bundle_version=payload.bundle_version, source="public", supersedes_version=supersedes)

    def _authorize_management(self, session: Session, request_id: str, token: str) -> OnboardingRequest:
        if not token or len(token) > 256:
            raise OnboardingAccessError("Request access denied.")
        request = session.get(OnboardingRequest, request_id)
        credential = session.execute(select(OnboardingManagementCredential).where(OnboardingManagementCredential.request_id == request_id, OnboardingManagementCredential.revoked_at.is_(None))).scalars().first() if request else None
        expires_at = credential.expires_at.replace(tzinfo=timezone.utc) if credential and credential.expires_at.tzinfo is None else (credential.expires_at if credential else None)
        if request is None or credential is None or expires_at <= utcnow() or not hmac.compare_digest(credential.token_hash, _hash(token)):
            raise OnboardingAccessError("Request access denied.")
        credential.last_used_at = utcnow()
        return request

    def _get_request(self, session: Session, request_id: str) -> OnboardingRequest:
        request = session.get(OnboardingRequest, request_id)
        if request is None:
            raise OnboardingNotFound("Onboarding request not found.")
        return request

    def _current_version(self, session: Session, request: OnboardingRequest) -> OnboardingRequestVersion:
        version = session.execute(select(OnboardingRequestVersion).where(OnboardingRequestVersion.request_id == request.id, OnboardingRequestVersion.version == request.current_version)).scalar_one_or_none()
        if version is None:
            raise OnboardingNotFound("Onboarding request version not found.")
        return version

    def _require_version(self, request: OnboardingRequest, version: int) -> None:
        if request.current_version != version:
            raise OnboardingTransitionError("The request version is stale.")

    def _transition(self, request: OnboardingRequest, allowed: set[str], destination: str) -> None:
        if request.state not in allowed or destination not in ONBOARDING_STATES:
            raise OnboardingTransitionError(f"Invalid onboarding transition from {request.state} to {destination}.")
        request.state = destination

    def _decision(self, session: Session, request: OnboardingRequest, version: int, actor: SaaSUser, decision: str, reason: str, bundle_key: Optional[str] = None, bundle_version: Optional[int] = None, execution_authorized: bool = False) -> None:
        session.add(OnboardingDecision(request_id=request.id, version=version, actor_user_id=actor.id, decision=decision, reason=reason, bundle_key=bundle_key, bundle_version=bundle_version, execution_authorized=execution_authorized))

    def _result(self, request: OnboardingRequest, management_token: Optional[str] = None, replayed: bool = False) -> PublicOnboardingResult:
        return PublicOnboardingResult(request_id=request.id, version=request.current_version, state=request.state, applicant_visible_status=request.applicant_visible_status, management_token=management_token, replayed=replayed)

    def _public_read(self, session: Session, request: OnboardingRequest) -> PublicOnboardingRead:
        version = self._current_version(session, request)
        job = session.get(ProvisioningJob, request.provisioning_job_id) if request.provisioning_job_id else None
        return PublicOnboardingRead(request_id=request.id, version=version.version, state=request.state, applicant_visible_status=request.applicant_visible_status, requested_modules=list(version.requested_module_codes_json), bundle_key=version.bundle_key, bundle_version=version.bundle_version, submitted_at=version.submitted_at, converted=bool(request.organization_id), provisioning_status=job.status if job else None)

    def _operator_read(self, session: Session, request: OnboardingRequest) -> OperatorOnboardingRead:
        version = self._current_version(session, request)
        return OperatorOnboardingRead(request_id=request.id, state=request.state, applicant_visible_status=request.applicant_visible_status, current_version=request.current_version, submitted_version=request.submitted_version, approved_version=request.approved_version, snapshot=dict(version.snapshot_json or {}), requested_modules=list(version.requested_module_codes_json), bundle_key=version.bundle_key, bundle_version=version.bundle_version, organization_id=request.organization_id, tenant_id=request.tenant_id, provisioning_job_id=request.provisioning_job_id, approved_at=request.approved_at, execution_authorized_at=request.execution_authorized_at, rejection_reason=request.rejection_reason)


class OnboardingService:
    """Legacy pilot orchestration retained for compatibility tests only."""

    def __init__(self, billing_provider: Optional[Any] = None) -> None:
        self.control = ControlPlaneService()
        self.billing = BillingService(provider=billing_provider)

    def onboard_pilot_organization(self, session: Session, current_user: object, org_payload: dict[str, Any], tenant_payload: dict[str, Any], plan_slug: str, site_options: Optional[dict[str, Any]] = None, run_provision_now: bool = False, provisioning_client: Optional[Any] = None) -> dict[str, Any]:
        organization = self.control.create_organization(session, current_user, OrganizationCreateRequest(**org_payload))
        tenant_payload = dict(tenant_payload or {})
        tenant_payload["organization_id"] = organization.id
        tenant = self.control.create_tenant(session, current_user, TenantCreateRequest(**tenant_payload))
        subscription = self.billing.subscribe_organization(session, organization.id, plan_slug, tenant_id=tenant.id)
        invoice = self.billing.generate_invoice_for_subscription(session, subscription.id)
        job = provisioning_service.queue_provisioning_job(session, tenant_id=tenant.id, job_type="initial_provision", payload={"organization_id": organization.id, "site_options": site_options or {}})
        result = {"organization": organization, "tenant": tenant, "subscription": subscription, "invoice": invoice, "provisioning_job": job}
        if run_provision_now:
            run_next_job(session, client=provisioning_client)
            session.refresh(job)
            session.refresh(tenant)
        return result


phase4_onboarding_service = Phase4OnboardingService()
onboarding_service = OnboardingService()
