#!/usr/bin/env python3
"""Synthetic Phase 3 production verification with exact-identifier cleanup.

The script exercises only the control plane. It never customizes an ERP site
and treats missing trusted application/verification evidence as the expected
safe result. Bearer values are written to runtime files and never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import delete, select

from app.core.security import generate_session_token, hash_session_token
from app.db.session import SessionLocal
from app.models.domain import (
    AuthSession,
    ModuleApplicationStatus,
    ModuleEntitlementAudit,
    ModuleEntitlementRequest,
    Organization,
    OrganizationMembership,
    OrganizationModule,
    SaaSUser,
    Tenant,
)


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--admin-token-file", required=True)
    parser.add_argument("--member-token-file", required=True)
    parser.add_argument("--other-token-file", required=True)
    parser.add_argument("--run-id", required=True)
    return parser.parse_args()


def write_token(path: str, token: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(token)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def prepare(run_id: str, token_paths: tuple[str, str, str]) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    names = {
        "admin_email": f"phase3-operator-{run_id}@example.test",
        "member_email": f"phase3-member-{run_id}@example.test",
        "other_email": f"phase3-other-{run_id}@example.test",
        "target_name": f"Phase 3 Synthetic Target {run_id}",
        "other_name": f"Phase 3 Synthetic Second {run_id}",
    }
    tokens = [generate_session_token() for _ in token_paths]
    with SessionLocal() as session:
        admin = SaaSUser(email=names["admin_email"], full_name="Phase 3 Synthetic Operator", status="active", is_platform_admin=True, email_verified_at=now)
        member = SaaSUser(email=names["member_email"], full_name="Phase 3 Synthetic Member", status="active", is_platform_admin=False, email_verified_at=now)
        other = SaaSUser(email=names["other_email"], full_name="Phase 3 Synthetic Second User", status="active", is_platform_admin=False, email_verified_at=now)
        target = Organization(name=names["target_name"], status="trial")
        second = Organization(name=names["other_name"], status="trial")
        session.add_all([admin, member, other, target, second])
        session.flush()
        session.add_all([
            OrganizationMembership(organization_id=target.id, user_id=admin.id, role="owner"),
            OrganizationMembership(organization_id=target.id, user_id=member.id, role="viewer"),
            OrganizationMembership(organization_id=second.id, user_id=other.id, role="viewer"),
            Tenant(organization_id=target.id, tenant_slug=f"phase3-{run_id}", environment="staging", status="planned"),
        ])
        session.flush()
        for user, token in zip([admin, member, other], tokens):
            session.add(AuthSession(user_id=user.id, session_token_hash=hash_session_token(token), expires_at=now + timedelta(hours=1)))
        session.commit()
        ids = {"admin_id": admin.id, "member_id": member.id, "other_id": other.id, "target_id": target.id, "second_id": second.id}
    for path, token in zip(token_paths, tokens):
        write_token(path, token)
    return ids


def request(method: str, path: str, token: str | None = None, payload: dict[str, object] | None = None) -> tuple[int, dict[str, object]]:
    base = os.environ.get("PRODUCTION_BACKEND_URL", "https://lenerp-api.lengrowth.com").rstrip("/")
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"User-Agent": "LenERP-Phase3-Synthetic-Smoke/1.0", "Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{base}{path}", data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        body = error.read().decode()
        try:
            return error.code, json.loads(body)
        except json.JSONDecodeError:
            return error.code, {"detail": "non-json error"}


def main() -> int:
    parsed = args()
    token_paths = (parsed.admin_token_file, parsed.member_token_file, parsed.other_token_file)
    ids = prepare(parsed.run_id, token_paths)
    admin_token, member_token, other_token = [Path(path).read_text(encoding="utf-8") for path in token_paths]
    evidence: dict[str, object] = {"status": "failed", "ids": ids, "candidate": os.environ.get("EXPECTED_RELEASE"), "feature_flags": os.environ.get("FEATURE_FLAGS_SAFE", "operator-only"), "started_at": datetime.now(timezone.utc).isoformat()}
    try:
        status, catalog = request("GET", "/catalog/modules", admin_token)
        assert status == 200
        catalog_codes = {str(item["code"]) for item in catalog}
        status, public = request("GET", "/public/modules")
        assert status == 200
        public_codes = {str(item["code"]) for item in public}
        assert public_codes.issubset(catalog_codes)
        evidence["catalog"] = {"internal_count": len(catalog_codes), "public_count": len(public_codes), "identities_agree": True}

        preview_payload = {"organization_id": ids["target_id"], "bundle_key": "champion-drilling", "bundle_version": 1, "idempotency_key": f"phase3-preview-{parsed.run_id}"}
        status, preview = request("POST", f"/organizations/{ids['target_id']}/modules/preview", admin_token, preview_payload)
        assert status == 200 and "well_mapping" in preview["effective"]["effective_codes"]
        apply_payload = {**preview_payload, "preview_hash": preview["preview_hash"], "idempotency_key": f"phase3-apply-{parsed.run_id}"}
        status, applied = request("POST", f"/organizations/{ids['target_id']}/modules/apply", admin_token, apply_payload)
        assert status == 200
        status, replay = request("POST", f"/organizations/{ids['target_id']}/modules/apply", admin_token, apply_payload)
        assert status == 200 and replay.get("replayed") is True
        status, audit_before_reverse = request("GET", f"/organizations/{ids['target_id']}/modules/audit", admin_token)
        assert status == 200 and len(audit_before_reverse) == 1
        status, invalid = request("POST", f"/organizations/{ids['target_id']}/modules/preview", admin_token, {"organization_id": ids["target_id"], "enable_codes": ["unknown-phase3-module"], "idempotency_key": f"phase3-invalid-{parsed.run_id}"})
        assert status == 400
        evidence["bundle"] = {"preview": True, "apply": True, "retry_replayed": True, "invalid_rejected": True, "audit_before_reverse": len(audit_before_reverse)}

        status, target_read = request("GET", f"/organizations/{ids['target_id']}/modules", member_token)
        assert status == 200
        status, denied_mutation = request("POST", f"/organizations/{ids['target_id']}/modules/apply", member_token, {"organization_id": ids["target_id"], "enable_codes": ["crm"], "idempotency_key": f"phase3-member-deny-{parsed.run_id}"})
        assert status == 403
        status, cross_read = request("GET", f"/organizations/{ids['target_id']}/modules", other_token)
        assert status == 403
        status, cross_mutation = request("POST", f"/organizations/{ids['target_id']}/modules/apply", other_token, {"organization_id": ids["target_id"], "enable_codes": ["crm"], "idempotency_key": f"phase3-cross-deny-{parsed.run_id}"})
        assert status == 403
        assert all(item["verification_state"] != "verified" for item in target_read["items"] if item["entitled"])
        evidence["authorization"] = {"member_read": True, "member_mutation_denied": True, "cross_company_read_denied": True, "cross_company_mutation_denied": True}
        evidence["erp_state_separation"] = {"entitled": True, "trusted_verification_present": False, "verified_reported": False}

        status, reversed_result = request("POST", f"/organizations/{ids['target_id']}/modules/reverse", admin_token, {"organization_id": ids["target_id"], "audit_id": applied["audit_id"], "idempotency_key": f"phase3-reverse-{parsed.run_id}"})
        assert status == 200 and reversed_result["effective"]["effective_codes"] == []
        status, audit_after_reverse = request("GET", f"/organizations/{ids['target_id']}/modules/audit", admin_token)
        assert status == 200 and len(audit_after_reverse) == 2
        evidence["reversal"] = {"passed": True, "audit_after_reverse": len(audit_after_reverse)}
        evidence["status"] = "passed"
        return 0
    finally:
        with SessionLocal() as session:
            target_ids = [ids["target_id"], ids["second_id"]]
            tenant_ids = [row[0] for row in session.execute(select(Tenant.id).where(Tenant.organization_id.in_(target_ids))).all()]
            session.execute(delete(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id.in_(tenant_ids))) if tenant_ids else None
            session.execute(delete(ModuleEntitlementAudit).where(ModuleEntitlementAudit.organization_id.in_(target_ids)))
            session.execute(delete(ModuleEntitlementRequest).where(ModuleEntitlementRequest.organization_id.in_(target_ids)))
            session.execute(delete(OrganizationModule).where(OrganizationModule.organization_id.in_(target_ids)))
            session.execute(delete(Tenant).where(Tenant.id.in_(tenant_ids))) if tenant_ids else None
            session.execute(delete(OrganizationMembership).where(OrganizationMembership.organization_id.in_(target_ids)))
            session.execute(delete(AuthSession).where(AuthSession.user_id.in_([ids["admin_id"], ids["member_id"], ids["other_id"]])))
            session.execute(delete(SaaSUser).where(SaaSUser.id.in_([ids["admin_id"], ids["member_id"], ids["other_id"]])))
            session.execute(delete(Organization).where(Organization.id.in_(target_ids)))
            session.commit()
            evidence["cleanup"] = {"organizations": session.execute(select(Organization.id).where(Organization.id.in_(target_ids))).scalars().all(), "users": session.execute(select(SaaSUser.id).where(SaaSUser.id.in_([ids["admin_id"], ids["member_id"], ids["other_id"]]))).scalars().all(), "module_audits": session.execute(select(ModuleEntitlementAudit.id).where(ModuleEntitlementAudit.organization_id.in_(target_ids))).scalars().all(), "module_assignments": session.execute(select(OrganizationModule.id).where(OrganizationModule.organization_id.in_(target_ids))).scalars().all()}
        Path(parsed.output).write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        for path in token_paths:
            try: Path(path).unlink()
            except FileNotFoundError: pass


if __name__ == "__main__":
    raise SystemExit(main())
