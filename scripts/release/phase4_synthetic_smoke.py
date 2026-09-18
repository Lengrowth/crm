#!/usr/bin/env python3
"""Run the Phase 4 onboarding workflow against an isolated synthetic lane.

This script is intentionally staging-only. It creates one synthetic request,
drives the public/operator state machine, waits for the already deployed worker
to finish, writes non-secret evidence, and removes only the exact records it
created. It never creates billing records, sends credentials, changes DNS, or
accepts a production hostname.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from app.db.session import SessionLocal
from app.integrations.erpnext_runtime import get_erpnext_client
from app.models.domain import (
    DomainMapping,
    FirstLoginHandoff,
    ImplementationProject,
    ImplementationTask,
    ModuleEntitlementAudit,
    ModuleApplicationStatus,
    OnboardingDecision,
    OnboardingManagementCredential,
    OnboardingRequest,
    OnboardingRequestVersion,
    Organization,
    OrganizationMembership,
    OrganizationModule,
    ProvisioningEvent,
    ProvisioningJob,
    ProvisioningOutboxEvent,
    ProvisioningStep,
    SaaSUser,
    Tenant,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=os.environ.get("STAGING_BACKEND_URL", "http://127.0.0.1:18001"))
    parser.add_argument("--admin-token-file", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--failure-step", default=None, choices=["health_checks"], help="Inject one controlled failure before recovery.")
    return parser.parse_args()


def request(base_url: str, method: str, path: str, *, token: str | None = None, onboarding_token: str | None = None, payload: dict[str, object] | None = None) -> tuple[int, dict[str, object]]:
    headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "LenERP-Phase4-Synthetic-Smoke/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if onboarding_token:
        headers["X-Onboarding-Token"] = onboarding_token
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    try:
        with urllib.request.urlopen(urllib.request.Request(f"{base_url.rstrip('/')}{path}", data=body, headers=headers, method=method), timeout=30) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            return error.code, json.loads(error.read().decode("utf-8"))
        except json.JSONDecodeError:
            return error.code, {"detail": "non-json error"}


def cleanup(request_id: str, admin_email: str, site_id: str | None) -> dict[str, object]:
    with SessionLocal() as session:
        onboarding = session.get(OnboardingRequest, request_id)
        if onboarding is None:
            return {"requests": 0, "external_site_deleted": 0}
        job_id, tenant_id, organization_id, project_id = onboarding.provisioning_job_id, onboarding.tenant_id, onboarding.organization_id, onboarding.implementation_project_id
        if site_id is None and job_id:
            job = session.get(ProvisioningJob, job_id)
            if job and job.target_environment == "staging" and (job.target_isolation_json or {}).get("lane") == "isolated_synthetic":
                site_id = str((job.external_refs_json or {}).get("site_id") or "") or None
        counts: dict[str, object] = {
            "requests": 1,
            "request_versions": 0,
            "management_credentials": 0,
            "decisions": 0,
            "organizations": 0,
            "memberships": 0,
            "tenants": 0,
            "projects": 0,
            "tasks": 0,
            "domains": 0,
            "organization_modules": 0,
            "module_entitlement_audits": 0,
            "module_application_statuses": 0,
            "jobs": 0,
            "steps": 0,
            "events": 0,
            "outbox_events": 0,
            "first_login_handoffs": 0,
            "synthetic_admins": 0,
            "external_site_deleted": 0,
        }
        if job_id:
            counts["events"] = session.query(ProvisioningEvent).filter(ProvisioningEvent.job_id == job_id).delete(synchronize_session=False)
            counts["steps"] = session.query(ProvisioningStep).filter(ProvisioningStep.job_id == job_id).delete(synchronize_session=False)
            counts["jobs"] = session.query(ProvisioningJob).filter(ProvisioningJob.id == job_id).delete(synchronize_session=False)
        counts["outbox_events"] = session.query(ProvisioningOutboxEvent).filter(ProvisioningOutboxEvent.aggregate_id == request_id).delete(synchronize_session=False)
        counts["first_login_handoffs"] = session.query(FirstLoginHandoff).filter(FirstLoginHandoff.request_id == request_id).delete(synchronize_session=False)
        counts["decisions"] = session.query(OnboardingDecision).filter(OnboardingDecision.request_id == request_id).delete(synchronize_session=False)
        counts["management_credentials"] = session.query(OnboardingManagementCredential).filter(OnboardingManagementCredential.request_id == request_id).delete(synchronize_session=False)
        counts["request_versions"] = session.query(OnboardingRequestVersion).filter(OnboardingRequestVersion.request_id == request_id).delete(synchronize_session=False)
        if tenant_id:
            counts["domains"] = session.query(DomainMapping).filter(DomainMapping.tenant_id == tenant_id).delete(synchronize_session=False)
            counts["module_application_statuses"] = session.query(ModuleApplicationStatus).filter(ModuleApplicationStatus.tenant_id == tenant_id).delete(synchronize_session=False)
            counts["tenants"] = session.query(Tenant).filter(Tenant.id == tenant_id).delete(synchronize_session=False)
        if project_id:
            counts["tasks"] = session.query(ImplementationTask).filter(ImplementationTask.implementation_project_id == project_id).delete(synchronize_session=False)
            counts["projects"] = session.query(ImplementationProject).filter(ImplementationProject.id == project_id).delete(synchronize_session=False)
        if organization_id:
            counts["module_entitlement_audits"] = session.query(ModuleEntitlementAudit).filter(ModuleEntitlementAudit.organization_id == organization_id, ModuleEntitlementAudit.source_type == "onboarding").delete(synchronize_session=False)
            counts["organization_modules"] = session.query(OrganizationModule).filter(OrganizationModule.organization_id == organization_id, OrganizationModule.source_type == "onboarding").delete(synchronize_session=False)
            counts["memberships"] = session.query(OrganizationMembership).filter(OrganizationMembership.organization_id == organization_id).delete(synchronize_session=False)
            counts["organizations"] = session.query(Organization).filter(Organization.id == organization_id).delete(synchronize_session=False)
        session.query(OnboardingRequest).filter(OnboardingRequest.id == request_id).delete(synchronize_session=False)
        counts["synthetic_admins"] = session.query(SaaSUser).filter(SaaSUser.email == admin_email).delete(synchronize_session=False)
        session.commit()
        if site_id:
            client = get_erpnext_client()
            result = client.delete_site(site_id)
            if result.get("status") not in {"success", "not_found"}:
                raise RuntimeError("isolated staging ERP site cleanup did not complete")
            counts["external_site_deleted"] = int(result.get("status") == "success")
            after = client.get_site_status(site_id)
            counts["external_site_cleanup_verified"] = after.get("status") == "not_found"
            if not counts["external_site_cleanup_verified"]:
                raise RuntimeError("isolated staging ERP site cleanup could not be verified")
        return counts


def main() -> int:
    parsed = parse_args()
    run_id = re.sub(r"[^a-z0-9-]", "-", parsed.run_id.lower()).strip("-")[:32]
    if not run_id:
        raise SystemExit("run-id must contain letters, numbers, or hyphens")
    base_url = parsed.base_url.rstrip("/")
    if any(host in base_url.lower() for host in ("lenerp.lengrowth.com", "lenerp-api.lengrowth.com", "erp.lengrowth.com")):
        raise SystemExit("Phase 4 synthetic smoke refuses production hostnames")
    admin_token = Path(parsed.admin_token_file).read_text(encoding="utf-8").strip()
    request_id: str | None = None
    job_id: str | None = None
    site_id: str | None = None
    last_status = "not_started"
    exit_code = 1
    admin_email = f"phase4-admin-{run_id}@acmephase4.com"
    evidence: dict[str, object] = {"status": "failed", "run_id": run_id, "started_at": datetime.now(timezone.utc).isoformat()}
    try:
        payload = {
            "company_name": f"Phase 4 Synthetic {run_id}",
            "legal_name": f"Phase 4 Synthetic {run_id} LLC",
            "industry": "synthetic_validation",
            "country": "US",
            "timezone": "UTC",
            "billing_email": admin_email,
            "administrator_name": "Phase 4 Synthetic Operator",
            "administrator_email": admin_email,
            "requested_modules": ["crm", "field_ops"],
            "branding": {"display_name": f"Phase 4 Synthetic {run_id}"},
            "expected_users": [{"role": "owner", "count": "1"}],
            "data_import_needs": "none; synthetic validation only",
            "desired_domain": f"phase4-{run_id}.staging.example.test",
            "desired_infrastructure": "isolated_synthetic",
            "billing_contact": admin_email,
            "implementation_notes": "Synthetic Phase 4 staging smoke; no Champion data.",
        }
        status, created = request(base_url, "POST", "/public/onboarding-requests", payload={"idempotency_key": f"phase4-{run_id}", "payload": payload})
        if created.get("request_id"):
            request_id = str(created["request_id"])
            evidence["request_id"] = request_id
        if status not in (200, 201) or not created.get("request_id") or not created.get("management_token"):
            detail = created.get("detail") or created.get("message") or "no response detail"
            raise RuntimeError(f"public synthetic onboarding request was not accepted (HTTP {status}: {detail})")
        management_token = str(created["management_token"])
        status, _ = request(base_url, "POST", f"/public/onboarding-requests/{request_id}/submit", onboarding_token=management_token)
        if status != 200:
            raise RuntimeError("synthetic onboarding request could not be submitted")
        review = {"version": 1, "reason": "Phase 4 synthetic staging smoke review."}
        for path in ("under-review", "approve"):
            status, _ = request(base_url, "POST", f"/operator/onboarding-requests/{request_id}/{path}", token=admin_token, payload=review)
            if status != 200:
                raise RuntimeError(f"operator {path} transition failed")
        status, converted = request(base_url, "POST", f"/operator/onboarding-requests/{request_id}/convert", token=admin_token)
        if status != 200 or not converted.get("provisioning_job_id"):
            raise RuntimeError("synthetic onboarding conversion failed")
        status, authorized = request(base_url, "POST", f"/operator/onboarding-requests/{request_id}/authorize-execution", token=admin_token, payload={"version": 1, "confirmation": "authorize_isolated_synthetic_execution", "reason": "Authorize the isolated synthetic staging lane."})
        if status != 200 or authorized.get("state") != "provisioning":
            raise RuntimeError("synthetic execution authorization failed")
        job_id = str(converted["provisioning_job_id"])
        evidence["job_id"] = job_id
        if parsed.failure_step:
            with SessionLocal() as session:
                version = session.execute(select(OnboardingRequestVersion).where(OnboardingRequestVersion.request_id == request_id, OnboardingRequestVersion.version == 1)).scalar_one()
                snapshot = dict(version.snapshot_json or {})
                snapshot["failure_inject_step"] = parsed.failure_step
                version.snapshot_json = snapshot
                session.commit()
        deadline = time.monotonic() + max(30, parsed.timeout_seconds)
        last_status = "provisioning"
        recovered = False
        while time.monotonic() < deadline:
            status, public_read = request(base_url, "GET", f"/public/onboarding-requests/{request_id}", onboarding_token=management_token)
            if status != 200:
                raise RuntimeError("synthetic public status read failed")
            last_status = str(public_read.get("state"))
            if parsed.failure_step and not recovered:
                status, failed_detail = request(base_url, "GET", f"/operator/provisioning-jobs/{job_id}", token=admin_token)
                if status == 200 and failed_detail.get("status") == "queued":
                    with SessionLocal() as session:
                        version = session.execute(select(OnboardingRequestVersion).where(OnboardingRequestVersion.request_id == request_id, OnboardingRequestVersion.version == 1)).scalar_one()
                        snapshot = dict(version.snapshot_json or {})
                        snapshot.pop("failure_inject_step", None)
                        version.snapshot_json = snapshot
                        job = session.get(ProvisioningJob, job_id)
                        if job:
                            job.next_attempt_at = datetime.now(timezone.utc)
                        session.commit()
                    recovered = True
            if last_status in {"ready", "failed", "cancelled"} and (not parsed.failure_step or recovered):
                break
            time.sleep(3)
        status, detail = request(base_url, "GET", f"/operator/provisioning-jobs/{job_id}", token=admin_token)
        if status != 200 or last_status != "ready" or detail.get("status") != "success":
            raise RuntimeError(f"synthetic worker did not reach ready state: {last_status}")
        for step in detail.get("steps", []):
            if step.get("step_key") == "create_isolated_site":
                evidence_json = step.get("evidence_json") or {}
                site_id = str(evidence_json.get("site_id") or "") or None
        provider_steps = {
            str(step.get("step_key")): step.get("evidence_json")
            for step in detail.get("steps", [])
            if step.get("step_key") in {"create_isolated_site", "health_checks", "verify_apps_modules"}
        }
        evidence.update({"status": "passed", "state": last_status, "step_count": len(detail.get("steps", [])), "worker_status": detail.get("status"), "recovery_run": bool(parsed.failure_step), "failure_step": parsed.failure_step, "provider_readback": provider_steps})
        exit_code = 0
    except Exception as exc:
        evidence["error"] = str(exc)[:500]
        evidence["state"] = last_status
        if request_id and job_id:
            try:
                status, failed_detail = request(base_url, "GET", f"/operator/provisioning-jobs/{job_id}", token=admin_token)
                if status == 200:
                    evidence["worker_status"] = failed_detail.get("status")
                    evidence["step_count"] = len(failed_detail.get("steps", []))
                    evidence["worker_error"] = failed_detail.get("error_message") or failed_detail.get("error")
                    evidence["worker_steps"] = [
                        {
                            "step_key": step.get("step_key"),
                            "status": step.get("status"),
                            "error_message": step.get("error_message"),
                            "evidence_json": step.get("evidence_json"),
                        }
                        for step in failed_detail.get("steps", [])
                    ]
            except Exception as detail_exc:
                evidence["worker_detail_error"] = str(detail_exc)[:300]
    finally:
        if request_id:
            try:
                evidence["cleanup"] = cleanup(request_id, admin_email, site_id)
            except Exception as exc:
                evidence["cleanup"] = {"status": "failed", "error": str(exc)[:500]}
                exit_code = 1
        Path(parsed.output).write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
