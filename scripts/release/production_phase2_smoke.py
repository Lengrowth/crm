"""Exercise the Phase 2 production API with disposable records and clean them exactly."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import delete

from app.core.security import generate_session_token, hash_session_token
from app.db.session import SessionLocal
from app.models.domain import (
    AuditLog,
    AuthSession,
    AuthToken,
    DomainMapping,
    ImplementationProject,
    ImplementationTask,
    Organization,
    OrganizationMembership,
    ProvisioningJob,
    SaaSUser,
    Tenant,
)
from app.models.erpnext import ERPNextIntegrationMetadata, TenantProvisioningRecord


def api_call(base_url: str, token: str, path: str, method: str = "GET", payload: dict | None = None) -> tuple[int, object]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "lenerp-phase2-production-smoke/1.0",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read()
            return response.status, json.loads(raw.decode("utf-8")) if raw else None
    except urllib.error.HTTPError as error:
        raw = error.read()
        try:
            detail = json.loads(raw.decode("utf-8")) if raw else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = None
        return error.code, detail


def cleanup(session, organization_ids: list[str], tenant_ids: list[str], user_id: str | None) -> None:
    discovered_tenants = [row[0] for row in session.query(Tenant.id).filter(Tenant.organization_id.in_(organization_ids)).all()]
    tenant_ids = list(dict.fromkeys([*tenant_ids, *discovered_tenants]))
    project_ids = [row[0] for row in session.query(ImplementationProject.id).filter(ImplementationProject.organization_id.in_(organization_ids)).all()]
    if project_ids:
        session.execute(delete(ImplementationTask).where(ImplementationTask.implementation_project_id.in_(project_ids)))
        session.execute(delete(ImplementationProject).where(ImplementationProject.id.in_(project_ids)))
    session.execute(delete(DomainMapping).where(DomainMapping.tenant_id.in_(tenant_ids)))
    session.execute(delete(ProvisioningJob).where(ProvisioningJob.tenant_id.in_(tenant_ids)))
    session.execute(delete(TenantProvisioningRecord).where(TenantProvisioningRecord.tenant_id.in_(tenant_ids)))
    session.execute(delete(ERPNextIntegrationMetadata).where(ERPNextIntegrationMetadata.tenant_id.in_(tenant_ids)))
    session.execute(delete(AuditLog).where(AuditLog.organization_id.in_(organization_ids)))
    session.execute(delete(Tenant).where(Tenant.id.in_(tenant_ids), Tenant.organization_id.in_(organization_ids)))
    session.execute(delete(OrganizationMembership).where(OrganizationMembership.organization_id.in_(organization_ids)))
    session.execute(delete(Organization).where(Organization.id.in_(organization_ids)))
    if user_id:
        session.execute(delete(AuthSession).where(AuthSession.user_id == user_id))
        session.execute(delete(AuthToken).where(AuthToken.user_id == user_id))
        session.execute(delete(OrganizationMembership).where(OrganizationMembership.user_id == user_id))
        session.execute(delete(SaaSUser).where(SaaSUser.id == user_id))
    session.commit()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", required=True)
    args = parser.parse_args()
    base_url = os.environ.get("PRODUCTION_BACKEND_URL", "https://lenerp-api.lengrowth.com")
    admin_token = Path(args.token_file).read_text(encoding="utf-8").strip()
    if not admin_token:
        raise SystemExit("production Phase 2 smoke token is empty")

    suffix = f"{os.environ.get('GITHUB_RUN_ID', 'local')}-{secrets.token_hex(4)}"
    organization_ids: list[str] = []
    tenant_ids: list[str] = []
    non_admin_user_id: str | None = None
    try:
        status_me, me_payload = api_call(base_url, admin_token, "/auth/me")
        if status_me != 200 or not isinstance(me_payload, dict) or not me_payload.get("user", {}).get("is_platform_admin"):
            raise RuntimeError(f"production Phase 2 smoke identity is not platform admin: {status_me}/{me_payload}")

        status_a, org_a = api_call(base_url, admin_token, "/organizations", "POST", {"name": f"Phase 2 Production Alpha {suffix}", "status": "trial"})
        status_b, org_b = api_call(base_url, admin_token, "/organizations", "POST", {"name": f"Phase 2 Production Beta {suffix}", "status": "lead"})
        if status_a != 201 or status_b != 201 or not isinstance(org_a, dict) or not isinstance(org_b, dict):
            raise RuntimeError(f"production Phase 2 organization CRUD setup failed: {status_a}/{org_a}; {status_b}/{org_b}")
        organization_ids.extend([str(org_a["id"]), str(org_b["id"])])

        status_ta, tenant_a = api_call(base_url, admin_token, f"/organizations/{org_a['id']}/tenants", "POST", {"tenant_slug": f"p2-production-alpha-{suffix}".lower(), "environment": "staging", "status": "planned"})
        status_tb, tenant_b = api_call(base_url, admin_token, f"/organizations/{org_b['id']}/tenants", "POST", {"tenant_slug": f"p2-production-beta-{suffix}".lower(), "environment": "staging", "status": "planned"})
        if status_ta != 201 or status_tb != 201 or not isinstance(tenant_a, dict) or not isinstance(tenant_b, dict):
            raise RuntimeError(f"production Phase 2 tenant CRUD setup failed: {status_ta}/{status_tb}")
        tenant_ids.extend([str(tenant_a["id"]), str(tenant_b["id"])])

        status_update, _ = api_call(base_url, admin_token, f"/organizations/{org_a['id']}", "PATCH", {"name": f"Phase 2 Production Alpha Updated {suffix}"})
        status_read, organizations = api_call(base_url, admin_token, "/organizations")
        if status_update != 200 or status_read != 200 or not isinstance(organizations, list) or not {item.get("id") for item in organizations}.issuperset(set(organization_ids)):
            raise RuntimeError("production Phase 2 organization read/update verification failed")

        now = datetime.now(timezone.utc)
        non_admin_token = generate_session_token()
        non_admin_email = f"phase2-production-non-admin-{suffix}@example.test"
        with SessionLocal() as session:
            user = SaaSUser(email=non_admin_email, full_name="Phase 2 Production Synthetic Non-Admin", password_hash=None, status="active", is_platform_admin=False, email_verified_at=now)
            session.add(user)
            session.flush()
            non_admin_user_id = str(user.id)
            session.add(OrganizationMembership(organization_id=org_a["id"], user_id=user.id, role="owner"))
            session.add(AuthSession(user_id=user.id, session_token_hash=hash_session_token(non_admin_token), expires_at=now + timedelta(hours=1)))
            session.commit()
        isolation_status, _ = api_call(base_url, non_admin_token, f"/organizations/{org_b['id']}")
        if isolation_status not in {403, 404}:
            raise RuntimeError(f"production Phase 2 tenant isolation failed with HTTP {isolation_status}")
        print("production Phase 2 CRUD and tenant-isolation smoke passed")
        return 0
    finally:
        with SessionLocal() as session:
            cleanup(session, organization_ids, tenant_ids, non_admin_user_id)


if __name__ == "__main__":
    raise SystemExit(main())
