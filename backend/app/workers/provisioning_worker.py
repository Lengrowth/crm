from __future__ import annotations

import hashlib
import secrets
from datetime import timedelta
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.integrations.erpnext_client import ERPNextClient
from app.integrations.erpnext_runtime import get_erpnext_client
from app.models.domain import (
    FirstLoginHandoff,
    Module,
    ModuleApplicationStatus,
    OnboardingRequest,
    OnboardingRequestVersion,
    OrganizationModule,
    ProvisioningJob,
    ProvisioningStep,
    Tenant,
    utcnow,
)
from app.models.erpnext import TenantProvisioningRecord
from app.services.erpnext_service import PersistentERPNextService
from app.services.application_resolver import calculate_required_applications, compare_installed_applications
from app.services.module_entitlement_service import ModuleEntitlementError, module_entitlement_service
from app.services.provisioning_service import provisioning_service, sanitize_value


PHASE4_STEP_KEYS = (
    "validate_approved_request",
    "reserve_site_name",
    "create_isolated_site",
    "install_pinned_erpnext",
    "install_pinned_hrms",
    "install_lenerp_custom_app",
    "apply_approved_modules",
    "apply_roles_workspaces",
    "apply_branding_configuration",
    "prepare_domain_binding",
    "bind_domain_ssl",
    "create_admin_handoff",
    "health_checks",
    "verify_apps_modules",
    "prepare_first_login",
    "mark_ready",
)


class StepFailure(RuntimeError):
    def __init__(self, message: str, category: str = "retryable", *, manual_confirmation: bool = False) -> None:
        super().__init__(message)
        self.category = category
        self.manual_confirmation = manual_confirmation


class LeaseLost(RuntimeError):
    """The worker lost its fenced lease while an external operation was running."""


def _module_runtime_requirements(session: Session, codes: list[str]) -> tuple[dict[str, str], list[str], list[str]]:
    required_apps: dict[str, str] = {}
    required_roles: set[str] = set()
    required_workspaces: set[str] = set()
    for code in codes:
        module = module_entitlement_service.module_by_code(session, code)
        if module is None:
            raise StepFailure("An approved module is unavailable.", "validation", manual_confirmation=True)
        if module.required_app:
            required_apps[code] = module.required_app
        required_roles.update(module.default_roles_json or [])
        required_workspaces.update(module.default_workspaces_json or [])
    return required_apps, sorted(required_roles), sorted(required_workspaces)


def _application_resolution(session: Session, codes: list[str]):
    modules = [module_entitlement_service.module_by_code(session, code) for code in codes]
    if any(module is None for module in modules):
        raise StepFailure("An approved module is unavailable.", "validation", manual_confirmation=True)
    try:
        return calculate_required_applications(module for module in modules if module is not None)
    except ValueError as exc:
        raise StepFailure("The approved application dependency plan is invalid.", "validation", manual_confirmation=True) from exc


def _installed_app_names(inventory: dict[str, object]) -> set[str]:
    installed = inventory.get("installed_apps") or {}
    return set(installed.keys()) if isinstance(installed, dict) else {str(app) for app in installed}


def _missing_runtime_requirements(inventory: dict[str, object], required_apps: dict[str, str], required_roles: list[str], required_workspaces: list[str]) -> tuple[list[str], list[str], list[str]]:
    installed = _installed_app_names(inventory)
    configuration = inventory.get("configuration") or {}
    roles = set(configuration.get("roles") or []) if isinstance(configuration, dict) else set()
    workspaces = set(configuration.get("workspaces") or []) if isinstance(configuration, dict) else set()
    return (sorted({app for app in required_apps.values() if app and app not in installed}), sorted(set(required_roles) - roles), sorted(set(required_workspaces) - workspaces))


class ProvisioningWorker:
    def __init__(self, client: Optional[ERPNextClient] = None) -> None:
        self.client = client or get_erpnext_client()
        self.service = PersistentERPNextService(self.client)

    def run(self, session: Session, organization_id: str, tenant_id: str, site_options: dict[str, Any]) -> str:
        record = self.service.create_provision_record(session, organization_id, tenant_id)
        self.service.provision_tenant_persistent(session, record, site_options)
        return record.id


def run_next_job(session: Session, client: Optional[ERPNextClient] = None, max_attempts: int = 3) -> Optional[ProvisioningJob]:
    """Claim one job with compare-and-set semantics and execute it.

    The legacy compatibility path remains for existing records, but Phase 4
    jobs use persisted steps and never deserialize caller-provided log payloads.
    """
    worker_id = f"worker-{uuid4()}"
    job = provisioning_service.claim_next_job(session, worker_id, lease_seconds=120)
    if job is None:
        return None
    lease_token = job.lease_token
    if job.workflow_version == "phase4-1":
        erp_client = client or get_erpnext_client()
        return _run_phase4_job(session, job, erp_client, worker_id, lease_token)
    erp_client = client or get_erpnext_client()
    return _run_legacy_job(session, job, erp_client, worker_id, max_attempts)


def _run_legacy_job(session: Session, job: ProvisioningJob, client: ERPNextClient, worker_id: str, max_attempts: int) -> ProvisioningJob:
    payload = dict((job.external_refs_json or {}).get("legacy_payload") or {})
    raw_site_options = payload.get("site_options") if isinstance(payload.get("site_options"), dict) else {}
    try:
        organization_id = str(payload.get("organization_id") or "")
        record = PersistentERPNextService(client).create_provision_record(session, organization_id, job.tenant_id)
        PersistentERPNextService(client).provision_tenant_persistent(session, record, raw_site_options)
        if record.status != "success":
            raise StepFailure("The compatibility provisioning step failed.", "retryable")
        provisioning_service.append_job_log(session, job, {"event": "provision_success", "message": "Compatibility provisioning completed."})
        return provisioning_service.update_job_status(session, job, "success")
    except Exception:
        session.rollback()
        job = session.get(ProvisioningJob, job.id) or job
        if job.attempt_count >= min(max_attempts, job.max_attempts or max_attempts):
            provisioning_service.append_job_log(session, job, {"event": "provision_failed", "message": "Compatibility provisioning failed after the maximum attempts."})
            return provisioning_service.update_job_status(session, job, "failed", err="Compatibility provisioning failed.")
        return provisioning_service.release_for_retry(session, job, worker_id, 0, "Compatibility provisioning will retry safely.")


def _run_phase4_job(session: Session, job: ProvisioningJob, client: ERPNextClient, worker_id: str, lease_token: Optional[str]) -> ProvisioningJob:
    request = session.get(OnboardingRequest, job.onboarding_request_id) if job.onboarding_request_id else None
    version = session.execute(select(OnboardingRequestVersion).where(OnboardingRequestVersion.request_id == request.id, OnboardingRequestVersion.version == job.onboarding_version)).scalar_one_or_none() if request else None
    tenant = session.get(Tenant, job.tenant_id)
    if request is None or version is None or tenant is None:
        return _fail_job(session, job, worker_id, "The approved onboarding context is unavailable.", "manual_recovery")
    snapshot = dict(version.snapshot_json or {})
    if job.cancel_requested_at is not None or request.state == "cancelled":
        return _cancel_job(session, job, request, tenant, worker_id, lease_token)
    if request.state not in {"provisioning", "validation"} or request.execution_authorized_at is None:
        return _fail_job(session, job, worker_id, "Execution authorization is missing or stale.", "authorization")
    steps = session.execute(select(ProvisioningStep).where(ProvisioningStep.job_id == job.id).order_by(ProvisioningStep.ordinal)).scalars().all()
    if steps and steps[0].status == "success" and request.state == "provisioning":
        request.state, request.applicant_visible_status = "validation", "validation"
        session.add(request)
        session.commit()
    for step in steps:
        if job.cancel_requested_at is not None or request.state == "cancelled":
            return _cancel_job(session, job, request, tenant, worker_id, lease_token)
        if not provisioning_service.renew_lease(session, job.id, worker_id, lease_seconds=120, lease_token=lease_token):
            return session.get(ProvisioningJob, job.id) or job
        if step.status == "success":
            continue
        if step.status == "failed" and step.attempt_count >= job.max_attempts:
            return _fail_job(session, job, worker_id, "A provisioning step reached its maximum attempts.", step.failure_category or "retryable")
        if not _dependencies_satisfied(steps, step):
            return _fail_job(session, job, worker_id, "A provisioning dependency is incomplete.", "dependency")
        try:
            _run_step(session, job, step, request, version, tenant, snapshot, client, worker_id, lease_token)
        except StepFailure as exc:
            return _handle_step_failure(session, job, step, worker_id, exc)
        except LeaseLost:
            session.rollback()
            return session.get(ProvisioningJob, job.id) or job
        except Exception as exc:
            detail = sanitize_value(str(exc))
            return _handle_step_failure(session, job, step, worker_id, StepFailure(f"{type(exc).__name__}: {detail}", "manual_recovery"))
    return _finish_phase4(session, job, request, tenant, worker_id, lease_token)


def _run_step(session: Session, job: ProvisioningJob, step: ProvisioningStep, request: OnboardingRequest, version: OnboardingRequestVersion, tenant: Tenant, snapshot: dict[str, Any], client: ERPNextClient, worker_id: str, lease_token: Optional[str]) -> None:
    step.status, step.worker_id, step.attempt_count, step.started_at = "running", worker_id, step.attempt_count + 1, utcnow()
    session.add(step)
    session.commit()
    injected = snapshot.get("failure_inject_step")
    if injected == step.step_key:
        raise StepFailure("Synthetic failure injection requested.", "injected")
    refs = dict(job.external_refs_json or {})
    site_id = str(refs.get("site_id") or "")
    evidence: dict[str, Any] = {}
    if step.step_key == "validate_approved_request":
        if request.approved_version != version.version or request.current_version != version.version:
            raise StepFailure("The approved request version is stale.", "authorization", manual_confirmation=True)
        try:
            codes = module_entitlement_service.validate_requested_selection(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
            resolution = _application_resolution(session, codes)
        except ModuleEntitlementError as exc:
            raise StepFailure("The approved module bundle is invalid.", "validation", manual_confirmation=True) from exc
        for code in codes:
            module = module_entitlement_service.module_by_code(session, code)
            if module is None:
                raise StepFailure("An approved module is unavailable.", "validation", manual_confirmation=True)
            row = session.execute(select(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id == tenant.id, ModuleApplicationStatus.module_id == module.id)).scalar_one_or_none()
            if row is None:
                session.add(ModuleApplicationStatus(tenant_id=tenant.id, module_id=module.id, application_state="pending", verification_state="pending"))
        session.flush()
        job.status = "validation"
        session.add(job)
        request.state, request.applicant_visible_status = "validation", "validation"
        session.add(request)
        evidence = {"version": version.version, "bundle_key": version.bundle_key, "bundle_version": version.bundle_version, "required_applications": list(resolution.applications), "required_versions": resolution.exact_versions}
    elif step.step_key == "reserve_site_name":
        evidence = {"site_namespace": job.target_isolation_json.get("site_namespace"), "environment": job.target_environment, "isolated": True}
    elif step.step_key == "create_isolated_site":
        if site_id:
            provider_status = client.get_site_status(site_id)
            if provider_status.get("status") == "not_found":
                site_id = ""
                refs.pop("site_id", None)
            elif provider_status.get("status") not in {"healthy", "ready", "success"}:
                raise StepFailure("The existing isolated ERP site is not healthy for replay.", "retryable")
            else:
                evidence = {"site_id": site_id, "replayed": True, "provider_health": sanitize_value(provider_status), "provider_verified": True}
        if not site_id:
            result = client.create_site(request.organization_id or "", tenant.id, {"domain": f"{job.target_isolation_json.get('site_namespace', tenant.tenant_slug)}.example.test", "idempotency_key": f"phase4:{job.id}"})
            if result.get("status") != "success" or not result.get("site_id"):
                raise StepFailure(f"The isolated site could not be created: {sanitize_value(result.get('error') or 'provider rejected site creation')}", "retryable")
            site_id = str(result["site_id"])
            refs["site_id"] = site_id
            refs["site_name"] = str(result.get("site_name") or "")
            evidence = {"site_id": site_id, "site_name": refs["site_name"], "isolated": True, "provider_verified": True, "provider": str(result.get("provider") or client.__class__.__name__), "provider_readback": sanitize_value(result)}
    elif step.step_key in {"install_pinned_erpnext", "install_pinned_hrms", "install_lenerp_custom_app"}:
        if not site_id:
            raise StepFailure("The isolated site reference is missing.", "manual_recovery")
        app = {"install_pinned_erpnext": "erpnext", "install_pinned_hrms": "hrms", "install_lenerp_custom_app": "lenerp_core"}[step.step_key]
        codes = module_entitlement_service.resolve_requested_codes(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
        resolution = _application_resolution(session, codes)
        expected_version = resolution.exact_versions.get(app, "")
        installed = set(refs.get("installed_apps") or [])
        inventory = client.get_site_inventory(site_id)
        installed_payload = inventory.get("installed_apps") or {}
        actual_apps = set(installed_payload.keys()) if isinstance(installed_payload, dict) else set(installed_payload)
        actual_version = installed_payload.get(app, "") if isinstance(installed_payload, dict) else ""
        if app in actual_apps and expected_version and actual_version != expected_version:
            raise StepFailure(f"Installed {app} does not match the pinned version.", "dependency", manual_confirmation=True)
        if app in installed and app in actual_apps:
            evidence = {"app": app, "version": actual_version or expected_version, "replayed": True, "provider_verified": True}
        else:
            result = client.install_app(site_id, app)
            if result.get("status") != "success" or result.get("provider_verified") is False:
                raise StepFailure(f"The pinned application {app} could not be installed.", "retryable")
            refreshed = client.get_site_inventory(site_id)
            refreshed_apps = refreshed.get("installed_apps") or {}
            refreshed_names = set(refreshed_apps.keys()) if isinstance(refreshed_apps, dict) else set(refreshed_apps)
            refreshed_version = refreshed_apps.get(app, "") if isinstance(refreshed_apps, dict) else ""
            if app not in refreshed_names or (expected_version and refreshed_version != expected_version):
                for code in codes:
                    module = module_entitlement_service.module_by_code(session, code)
                    if module is not None and module.required_app == app:
                        row = session.execute(select(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id == tenant.id, ModuleApplicationStatus.module_id == module.id)).scalar_one_or_none()
                        if row is not None:
                            row.application_state, row.verification_state, row.failure_reason, row.last_checked_at = "pending", "pending", f"Required application `{app}` is missing or incompatible in the verified installed-app readback.", utcnow()
                session.flush()
                raise StepFailure(f"The installed-app readback did not confirm pinned {app}.", "dependency")
            installed.add(app)
            refs["installed_apps"] = sorted(installed)
            evidence = {"app": app, "version": refreshed_version, "pinned": True, "provider_readback": sanitize_value(result), "installed_app_readback": sanitize_value(refreshed)}
    elif step.step_key == "apply_approved_modules":
        codes = module_entitlement_service.resolve_requested_codes(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
        if not site_id:
            raise StepFailure("The isolated site reference is missing.", "manual_recovery")
        resolution = _application_resolution(session, codes)
        migration = client.migrate_site(site_id)
        if migration.get("status") != "success" or migration.get("provider_verified") is not True:
            raise StepFailure("The ERP migration was not confirmed by the provider.", "retryable")
        provider_result = client.apply_site_configuration(site_id, {"modules": codes})
        if provider_result.get("status") != "success" or provider_result.get("provider_verified") is not True:
            raise StepFailure("The approved modules were not confirmed by the ERP runtime.", "retryable")
        requirements, required_roles, required_workspaces = _module_runtime_requirements(session, codes)
        inventory = client.get_site_inventory(site_id)
        if inventory.get("status") != "success" or inventory.get("provider_verified") is not True:
            raise StepFailure("The tenant installed-app readback could not be verified before applying modules.", "retryable")
        missing_apps, _, _ = _missing_runtime_requirements(inventory, requirements, [], [])
        _, incompatible_apps = compare_installed_applications(inventory.get("installed_apps") or {}, resolution)
        for code in codes:
            module = module_entitlement_service.module_by_code(session, code)
            row = session.execute(select(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id == tenant.id, ModuleApplicationStatus.module_id == module.id)).scalar_one_or_none()
            if row is None:
                row = ModuleApplicationStatus(tenant_id=tenant.id, module_id=module.id)
                session.add(row)
            required_app = requirements.get(code)
            if required_app and (required_app in missing_apps or any(item.startswith(f"{required_app} ") for item in incompatible_apps)):
                row.application_state, row.verification_state, row.failure_reason, row.last_checked_at = "pending", "pending", f"Required application `{required_app}` is missing from the verified installed-app readback. Install it, rerun the readback, then retry verification.", utcnow()
            else:
                row.application_state, row.failure_reason, row.last_checked_at = "applied", None, utcnow()
        evidence = {"requested": list(version.requested_module_codes_json), "effective": codes, "migration": sanitize_value(migration), "provider_readback": sanitize_value(provider_result), "installed_app_readback": sanitize_value(inventory), "missing_required_apps": missing_apps, "incompatible_apps": incompatible_apps, "verification": "provider_pending"}
        if missing_apps or incompatible_apps:
            raise StepFailure("Required ERP applications are missing or incompatible with the pinned readback. Install the exact dependency versions and retry.", "dependency")
    elif step.step_key == "apply_roles_workspaces":
        if not site_id:
            raise StepFailure("The isolated site reference is missing.", "manual_recovery")
        role_codes = sorted({role for code in module_entitlement_service.resolve_requested_codes(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version) for role in (module_entitlement_service.module_by_code(session, code).default_roles_json if module_entitlement_service.module_by_code(session, code) else [])})
        workspace_codes = sorted({workspace for code in module_entitlement_service.resolve_requested_codes(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version) for workspace in (module_entitlement_service.module_by_code(session, code).default_workspaces_json if module_entitlement_service.module_by_code(session, code) else [])})
        provider_result = client.apply_site_configuration(site_id, {"roles": role_codes, "workspaces": workspace_codes})
        if provider_result.get("status") != "success" or provider_result.get("provider_verified") is not True:
            raise StepFailure("ERP roles and workspaces were not confirmed by the ERP runtime.", "retryable")
        evidence = {"roles": role_codes, "workspaces": workspace_codes, "provider_readback": sanitize_value(provider_result)}
    elif step.step_key == "apply_branding_configuration":
        if not site_id:
            raise StepFailure("The isolated site reference is missing.", "manual_recovery")
        branding = {key: value for key, value in dict(snapshot.get("branding") or {}).items() if key in {"display_name", "primary_color", "logo_ref", "favicon_ref"}}
        provider_result = client.apply_site_configuration(site_id, {"branding": branding})
        if provider_result.get("status") != "success" or provider_result.get("provider_verified") is not True:
            raise StepFailure("ERP branding was not confirmed by the ERP runtime.", "retryable")
        evidence = {"branding": branding, "provider_readback": sanitize_value(provider_result)}
    elif step.step_key == "prepare_domain_binding":
        evidence = {"domain": snapshot.get("desired_domain"), "dns_mutation": "deferred_manual_activation"}
    elif step.step_key == "bind_domain_ssl":
        domain = str(snapshot.get("desired_domain") or "")
        if domain and domain.endswith(".example.test") and site_id:
            bind = client.bind_domain(site_id, domain)
            ssl = client.issue_ssl(site_id, domain)
            if bind.get("status") != "success" or ssl.get("status") not in {"success", "deferred"} or ssl.get("provider_verified") is not True:
                raise StepFailure("The synthetic domain binding did not complete.", "retryable")
            evidence = {"domain": domain, "bind": sanitize_value(bind), "ssl": sanitize_value(ssl), "provider_verified": True}
        else:
            evidence = {"domain": domain or None, "status": "manual_activation_required", "dns_mutation": "not_performed"}
    elif step.step_key == "create_admin_handoff":
        handoff = session.execute(select(FirstLoginHandoff).where(FirstLoginHandoff.request_id == request.id, FirstLoginHandoff.tenant_id == tenant.id)).scalars().first()
        if handoff is None:
            raise StepFailure("The administrator handoff record is missing.", "manual_recovery")
        if not handoff.token_hash:
            raw = secrets.token_urlsafe(32)
            handoff.token_hash = hashlib.sha256(raw.encode()).hexdigest()
            handoff.token_secret_ref = f"synthetic-handoff:{handoff.id}"
        handoff.status, handoff.delivery_status, handoff.expires_at = "prepared", "disabled", utcnow() + timedelta(hours=24)
        evidence = {"handoff_id": handoff.id, "delivery": "disabled", "token_exposed": False}
    elif step.step_key == "health_checks":
        if not site_id:
            raise StepFailure("The isolated site reference is missing.", "manual_recovery")
        status = client.get_site_status(site_id)
        if status.get("status") not in {"healthy", "ready", "success"}:
            raise StepFailure("The isolated site health check did not pass.", "retryable")
        inventory = client.get_site_inventory(site_id)
        if inventory.get("status") != "success" or inventory.get("provider_verified") is not True:
            raise StepFailure("The isolated ERP runtime inventory could not be verified.", "retryable")
        evidence = {"status": str(status.get("status")), "site_id": site_id, "provider_health": sanitize_value(status), "provider_inventory": sanitize_value(inventory)}
    elif step.step_key == "verify_apps_modules":
        statuses = session.execute(select(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id == tenant.id)).scalars().all()
        if not site_id:
            raise StepFailure("The isolated site reference is missing.", "manual_recovery")
        codes = module_entitlement_service.resolve_requested_codes(session, version.requested_module_codes_json, version.bundle_key, version.bundle_version)
        requirements, required_roles, required_workspaces = _module_runtime_requirements(session, codes)
        resolution = _application_resolution(session, codes)
        provider_result = client.verify_site_configuration(site_id, codes, required_apps=requirements, required_roles=required_roles, required_workspaces=required_workspaces, required_app_versions=resolution.exact_versions)
        missing_apps = list(provider_result.get("missing_required_apps") or [])
        incompatible_apps = list(provider_result.get("incompatible_apps") or [])
        missing_roles = list(provider_result.get("missing_required_roles") or [])
        missing_workspaces = list(provider_result.get("missing_required_workspaces") or [])
        for row in statuses:
            module = session.get(Module, row.module_id)
            required_app = module.required_app if module else None
            if required_app and (required_app in missing_apps or any(item.startswith(f"{required_app} ") for item in incompatible_apps)):
                row.application_state, row.verification_state, row.verified_at, row.failure_reason = "pending", "pending", None, f"Required application `{required_app}` is missing from the verified installed-app readback. Install it, rerun the readback, then retry verification."
            elif missing_roles or missing_workspaces:
                missing_detail = ", ".join([*(f"role:{item}" for item in missing_roles), *(f"workspace:{item}" for item in missing_workspaces)])
                row.verification_state, row.verified_at, row.failure_reason = "pending", None, f"Required role/workspace readback is incomplete ({missing_detail}). Configure it, rerun the readback, then retry verification."
            elif incompatible_apps:
                row.application_state, row.verification_state, row.verified_at, row.failure_reason = "pending", "pending", None, "Pinned application version readback is incompatible. Install the exact reviewed application revision and retry."
            elif provider_result.get("status") == "success" and provider_result.get("provider_verified") is True:
                row.verification_state, row.verified_at, row.failure_reason = "verified", row.verified_at or utcnow(), None
            else:
                row.verification_state, row.verified_at, row.failure_reason = "pending", None, "Provider verification failed; review the installed-app/module/role/workspace readback and retry."
            row.last_checked_at = utcnow()
        evidence = {"verified_module_count": len(statuses) if not (missing_apps or incompatible_apps or missing_roles or missing_workspaces) else 0, "provider_readback": sanitize_value(provider_result), "missing_required_apps": missing_apps, "incompatible_apps": incompatible_apps, "missing_required_roles": missing_roles, "missing_required_workspaces": missing_workspaces, "trusted_evidence": not (missing_apps or incompatible_apps or missing_roles or missing_workspaces)}
        if missing_apps:
            raise StepFailure(f"Required ERP applications are missing from the verified readback: {', '.join(missing_apps)}. Install them and retry.", "dependency")
        if incompatible_apps:
            raise StepFailure("Required ERP applications have incompatible versions in the verified readback. Install the exact reviewed revisions and retry.", "dependency")
        if missing_roles or missing_workspaces:
            raise StepFailure("Required ERP roles or workspaces are missing from the verified readback. Configure them and retry.", "verification")
        if provider_result.get("status") != "success" or provider_result.get("provider_verified") is not True:
            raise StepFailure("The ERP runtime did not verify the installed apps and approved modules.", "retryable")
    elif step.step_key == "prepare_first_login":
        handoff = session.execute(select(FirstLoginHandoff).where(FirstLoginHandoff.request_id == request.id, FirstLoginHandoff.tenant_id == tenant.id)).scalars().first()
        if handoff is None or handoff.status != "prepared":
            raise StepFailure("First-login preparation did not complete.", "manual_recovery")
        evidence = {"handoff_id": handoff.id, "expiry_present": bool(handoff.expires_at)}
    elif step.step_key == "mark_ready":
        evidence = {"ready_requires_verified": True}
    else:
        raise StepFailure("Unknown provisioning step.", "manual_recovery")
    try:
        provisioning_service.assert_lease(session, job.id, worker_id, lease_token)
    except RuntimeError as exc:
        raise LeaseLost(str(exc)) from exc
    job.external_refs_json = sanitize_value(refs)
    step.status, step.finished_at, step.worker_id, step.lease_expires_at, step.evidence_json = "success", utcnow(), None, None, sanitize_value(evidence)
    provisioning_service.add_event(session, step, job.id, "step_succeeded", "Provisioning step completed.", {"step_key": step.step_key, "attempt": step.attempt_count})
    session.add_all([job, step])
    session.commit()


def _dependencies_satisfied(steps: list[ProvisioningStep], step: ProvisioningStep) -> bool:
    by_key = {item.step_key: item for item in steps}
    return all(by_key.get(key) is not None and by_key[key].status == "success" for key in (step.dependency_keys_json or []))


def _handle_step_failure(session: Session, job: ProvisioningJob, step: ProvisioningStep, worker_id: str, failure: StepFailure) -> ProvisioningJob:
    step.status = "failed" if step.attempt_count >= job.max_attempts or failure.manual_confirmation else "queued"
    step.failure_category, step.sanitized_error, step.finished_at, step.worker_id, step.lease_expires_at = failure.category, str(failure)[:500], utcnow(), None, None
    step.rollback_state = "confirmation_required" if failure.manual_confirmation else "available"
    provisioning_service.add_event(session, step, job.id, "step_failed", "Provisioning step failed; review the sanitized recovery state.", {"failure_category": failure.category, "retryable": step.status == "queued"})
    session.add(step)
    session.commit()
    if step.status == "queued":
        return provisioning_service.release_for_retry(session, job, worker_id, _backoff(step.attempt_count), "The failed step is scheduled for a bounded retry.")
    return _fail_job(session, job, worker_id, "Provisioning stopped at a recoverable failure.", failure.category)


def _fail_job(session: Session, job: ProvisioningJob, worker_id: str, message: str, category: str) -> ProvisioningJob:
    job.status, job.error_message, job.finished_at, job.worker_id, job.lease_token, job.lease_expires_at = "failed", message[:500], utcnow(), None, None, None
    provisioning_service.append_job_log(session, job, {"event": "workflow_failed", "message": message, "failure_category": category})
    tenant = session.get(Tenant, job.tenant_id)
    if tenant:
        tenant.provisioning_status, tenant.status = "failed", "failed"
    request = session.get(OnboardingRequest, job.onboarding_request_id) if job.onboarding_request_id else None
    if request and request.state not in {"cancelled", "ready"}:
        request.state, request.applicant_visible_status = "failed", "failed"
        session.add(request)
    session.add_all([job, tenant] if tenant else [job])
    session.commit()
    return session.get(ProvisioningJob, job.id) or job


def _cancel_job(session: Session, job: ProvisioningJob, request: OnboardingRequest, tenant: Tenant, worker_id: str, lease_token: Optional[str]) -> ProvisioningJob:
    try:
        provisioning_service.assert_lease(session, job.id, worker_id, lease_token)
    except RuntimeError:
        session.rollback()
        return session.get(ProvisioningJob, job.id) or job
    job.status, job.finished_at, job.worker_id, job.lease_token, job.lease_expires_at = "cancelled", utcnow(), None, None, None
    request.state, request.applicant_visible_status = "cancelled", "cancelled"
    tenant.provisioning_status, tenant.status = "cancelled", "cancelled"
    for step in session.execute(select(ProvisioningStep).where(ProvisioningStep.job_id == job.id, ProvisioningStep.status.not_in(("success", "failed")))).scalars().all():
        step.status, step.worker_id, step.lease_expires_at, step.finished_at = "cancelled", None, None, utcnow()
        session.add(step)
    session.add_all([job, request, tenant])
    session.commit()
    return session.get(ProvisioningJob, job.id) or job


def _finish_phase4(session: Session, job: ProvisioningJob, request: OnboardingRequest, tenant: Tenant, worker_id: str, lease_token: Optional[str]) -> ProvisioningJob:
    try:
        provisioning_service.assert_lease(session, job.id, worker_id, lease_token)
    except RuntimeError:
        session.rollback()
        return session.get(ProvisioningJob, job.id) or job
    job.status, job.finished_at, job.worker_id, job.lease_token, job.lease_expires_at = "success", utcnow(), None, None, None
    request.state, request.applicant_visible_status = "ready", "ready"
    tenant.provisioning_status, tenant.status = "ready", "ready"
    session.add_all([job, request, tenant])
    session.commit()
    return session.get(ProvisioningJob, job.id) or job


def _backoff(attempt: int) -> int:
    return min(3600, 2 ** max(0, min(attempt, 10)))
