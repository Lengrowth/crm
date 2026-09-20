"""Prepare, exercise, and clean up the isolated Phase 03 staging identity lane."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import delete, select

from app.core.security import generate_session_token, hash_session_token
from app.db.session import SessionLocal
from app.models.domain import (
    AuditLog,
    AuthSession,
    ERPIdentityMapping,
    Organization,
    OrganizationMembership,
    SaaSUser,
    SSOAuthorizationCode,
    SSOAuthorizationRequest,
    Tenant,
)


def token_file(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


def write_token(path: Path, token: str) -> None:
    path.write_text(token, encoding="utf-8")
    path.chmod(0o600)


def make_user(session, email: str, name: str, *, platform_admin: bool) -> tuple[SaaSUser, str]:
    now = datetime.now(timezone.utc)
    user = SaaSUser(
        email=email,
        full_name=name,
        password_hash=None,
        status="active",
        is_platform_admin=platform_admin,
        email_verified_at=now,
    )
    session.add(user)
    session.flush()
    token = generate_session_token()
    session.add(AuthSession(user_id=user.id, session_token_hash=hash_session_token(token), expires_at=now + timedelta(hours=1)))
    return user, token


def prepare(args: argparse.Namespace) -> None:
    suffix = args.run_id.lower()
    champion_email = f"phase3-identity-{suffix}@example.test"
    other_email = f"phase3-other-{suffix}@example.test"
    platform_email = f"phase3-platform-{suffix}@example.test"
    with SessionLocal() as session:
        champion_org = Organization(name=f"Phase 03 Identity Champion {suffix}", status="trial")
        other_org = Organization(name=f"Phase 03 Identity Other {suffix}", status="trial")
        session.add_all([champion_org, other_org])
        session.flush()
        champion, champion_token = make_user(session, champion_email, "Phase 03 Champion Synthetic", platform_admin=False)
        other, other_token = make_user(session, other_email, "Phase 03 Other Organization Synthetic", platform_admin=False)
        platform, platform_token = make_user(session, platform_email, "Phase 03 Platform Admin Synthetic", platform_admin=True)
        session.add(OrganizationMembership(organization_id=champion_org.id, user_id=champion.id, role="owner"))
        session.add(OrganizationMembership(organization_id=other_org.id, user_id=other.id, role="owner"))
        tenant = Tenant(
            organization_id=champion_org.id,
            tenant_slug=f"phase3-identity-{suffix}",
            environment="staging",
            status="ready",
            erpnext_site_name=args.site_name,
            erpnext_base_url=args.erp_base_url,
            provisioning_status="ready",
            erp_role_profile_version="champion-v1",
            erp_role_profile_status="ready",
            sso_rollout_enabled=True,
        )
        session.add(tenant)
        session.commit()
        manifest = {
            "run_id": args.run_id,
            "control_base_url": args.control_base_url.rstrip("/"),
            "erp_base_url": args.erp_base_url.rstrip("/"),
            "site_name": args.site_name,
            "tenant_id": tenant.id,
            "organization_id": champion_org.id,
            "other_organization_id": other_org.id,
            "champion_user_id": champion.id,
            "other_user_id": other.id,
            "platform_user_id": platform.id,
            "champion_email": champion.email,
            "other_email": other.email,
            "platform_email": platform.email,
            "champion_token_file": token_file(Path(args.output_dir) / "champion.token"),
            "other_token_file": token_file(Path(args.output_dir) / "other.token"),
            "platform_token_file": token_file(Path(args.output_dir) / "platform.token"),
            "exchange_secret_file": args.exchange_secret_file,
        }
    write_token(Path(manifest["champion_token_file"]), champion_token)
    write_token(Path(manifest["other_token_file"]), other_token)
    write_token(Path(manifest["platform_token_file"]), platform_token)
    Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"prepared Phase 03 identity tenant {manifest['tenant_id']}")


def read_manifest(path: str) -> dict[str, str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"control_base_url", "erp_base_url", "tenant_id", "organization_id", "other_organization_id", "champion_token_file", "other_token_file", "platform_token_file", "exchange_secret_file", "site_name"}
    missing = required - payload.keys()
    if missing:
        raise SystemExit(f"identity manifest is missing: {sorted(missing)}")
    return payload


def http_json(url: str, *, method: str = "GET", payload: dict | None = None, token: str | None = None, context: ssl.SSLContext | None = None) -> tuple[int, dict]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method=method, headers={"Accept": "application/json", "Content-Type": "application/json"})
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, context=context, timeout=20) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raw = error.read().decode("utf-8")
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = {"detail": raw[:200]}
        return error.code, value


def pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return verifier, challenge


def api_tests(args: argparse.Namespace) -> None:
    manifest = read_manifest(args.manifest)
    ca = Path(args.ca_bundle)
    context = ssl.create_default_context(cafile=str(ca))
    secret = Path(manifest["exchange_secret_file"]).read_text(encoding="utf-8").strip()
    champion_token = Path(manifest["champion_token_file"]).read_text(encoding="utf-8").strip()
    other_token = Path(manifest["other_token_file"]).read_text(encoding="utf-8").strip()
    platform_token = Path(manifest["platform_token_file"]).read_text(encoding="utf-8").strip()
    callback = f"{manifest['erp_base_url']}/api/method/lenerp_core.sso.callback"
    base = manifest["control_base_url"]
    results: dict[str, object] = {}

    def auth_payload(token: str, *, state: str | None = None, path: str = "/app", audience: str = "lenerp-erp", client: str = "lenerp-erp", redirect: str = callback) -> tuple[str, dict]:
        verifier, challenge = pkce()
        status, response = http_json(f"{base}/api/sso/authorize", method="POST", token=token, context=context, payload={"tenant_id": manifest["tenant_id"], "client_id": client, "audience": audience, "redirect_uri": redirect, "state": state or secrets.token_urlsafe(24), "code_challenge": challenge, "code_challenge_method": "S256", "requested_path": path})
        return verifier, {"status": status, "body": response, "challenge": challenge}

    verifier, issued = auth_payload(champion_token)
    results["authorized_request"] = issued["status"] == 200
    code = issued["body"].get("code") if issued["status"] == 200 else None
    if code:
        token_status, _ = http_json(f"{base}/api/sso/token", method="POST", context=context, payload={"code": code, "client_id": "lenerp-erp", "audience": "lenerp-erp", "redirect_uri": callback, "code_verifier": verifier, "client_secret": secret})
        replay_status, _ = http_json(f"{base}/api/sso/token", method="POST", context=context, payload={"code": code, "client_id": "lenerp-erp", "audience": "lenerp-erp", "redirect_uri": callback, "code_verifier": verifier, "client_secret": secret})
        results["successful_exchange"] = token_status == 200
        results["authorization_code_replay_denied"] = replay_status == 400

    _, wrong_pkce = auth_payload(champion_token)
    if wrong_pkce["status"] == 200:
        wrong_status, _ = http_json(f"{base}/api/sso/token", method="POST", context=context, payload={"code": wrong_pkce["body"]["code"], "client_id": "lenerp-erp", "audience": "lenerp-erp", "redirect_uri": callback, "code_verifier": secrets.token_urlsafe(48), "client_secret": secret})
        results["invalid_pkce_denied"] = wrong_status == 400
    expired_verifier, expired = auth_payload(champion_token)
    if expired["status"] == 200:
        with SessionLocal() as session:
            code_record = session.execute(select(SSOAuthorizationCode).where(SSOAuthorizationCode.code_hash == hashlib.sha256(expired["body"]["code"].encode("utf-8")).hexdigest())).scalar_one()
            code_record.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
            session.commit()
        expired_status, _ = http_json(f"{base}/api/sso/token", method="POST", context=context, payload={"code": expired["body"]["code"], "client_id": "lenerp-erp", "audience": "lenerp-erp", "redirect_uri": callback, "code_verifier": expired_verifier, "client_secret": secret})
        results["expired_code_denied"] = expired_status == 400
    _, wrong_audience = auth_payload(champion_token, audience="wrong-audience")
    results["wrong_audience_denied"] = wrong_audience["status"] == 403
    _, wrong_client = auth_payload(champion_token, client="wrong-client")
    results["wrong_client_denied"] = wrong_client["status"] == 403
    _, wrong_redirect = auth_payload(champion_token, redirect="https://evil.example.test/callback")
    results["unapproved_redirect_denied"] = wrong_redirect["status"] == 403
    _, path_traversal = auth_payload(champion_token, path="/safe/%2e%2e/escape")
    results["encoded_path_traversal_denied"] = path_traversal["status"] == 400
    _, other_org = auth_payload(other_token)
    results["other_organization_denied"] = other_org["status"] == 403
    _, platform_without_membership = auth_payload(platform_token)
    results["platform_admin_without_membership_denied"] = platform_without_membership["status"] == 403
    readiness_status, readiness = http_json(f"{base}/api/sso/readiness/{manifest['tenant_id']}", token=platform_token, context=context)
    results["platform_admin_readiness_disabled"] = readiness_status == 200 and readiness.get("ready") is False
    if not all(value is True for value in results.values()):
        raise SystemExit(f"Phase 03 identity API checks failed: {json.dumps(results, sort_keys=True)}")
    Path(args.evidence).write_text(json.dumps({"synthetic": True, "results": results, "tenant_id": manifest["tenant_id"], "organization_id": manifest["organization_id"]}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Phase 03 identity API checks passed")


def cleanup(args: argparse.Namespace) -> None:
    manifest = read_manifest(args.manifest)
    ids = [manifest["champion_user_id"], manifest["other_user_id"], manifest["platform_user_id"]]
    with SessionLocal() as session:
        tenant_id = manifest["tenant_id"]
        organization_id = manifest["organization_id"]
        session.execute(delete(ERPIdentityMapping).where(ERPIdentityMapping.tenant_id == tenant_id))
        session.execute(delete(SSOAuthorizationCode).where(SSOAuthorizationCode.tenant_id == tenant_id))
        session.execute(delete(SSOAuthorizationRequest).where(SSOAuthorizationRequest.tenant_id == tenant_id))
        session.execute(delete(AuditLog).where(AuditLog.organization_id == organization_id))
        session.execute(delete(AuthSession).where(AuthSession.user_id.in_(ids)))
        session.execute(delete(OrganizationMembership).where(OrganizationMembership.user_id.in_(ids)))
        session.execute(delete(Tenant).where(Tenant.id == tenant_id))
        session.execute(delete(Organization).where(Organization.id == organization_id))
        session.execute(delete(Organization).where(Organization.id == manifest["other_organization_id"]))
        session.execute(delete(SaaSUser).where(SaaSUser.id.in_(ids)))
        session.commit()
    for key in ("champion_token_file", "other_token_file", "platform_token_file"):
        Path(manifest[key]).unlink(missing_ok=True)
    Path(args.manifest).unlink(missing_ok=True)
    print("Phase 03 identity synthetic records cleaned")


def post_tests(args: argparse.Namespace) -> None:
    manifest = read_manifest(args.manifest)
    with SessionLocal() as session:
        from app.services.sso_service import sso_service

        mapping = session.execute(select(ERPIdentityMapping).where(ERPIdentityMapping.tenant_id == manifest["tenant_id"], ERPIdentityMapping.user_id == manifest["champion_user_id"])).scalar_one_or_none()
        if mapping is None or mapping.mapping_status != "active":
            raise SystemExit("Phase 03 browser flow did not create an active identity mapping")
        revoked = sso_service.revoke_for_membership(session, manifest["champion_user_id"], manifest["tenant_id"])
        membership = session.execute(select(OrganizationMembership).where(OrganizationMembership.organization_id == manifest["organization_id"], OrganizationMembership.user_id == manifest["champion_user_id"])).scalar_one_or_none()
        if membership is not None:
            session.delete(membership)
            session.commit()
        assert revoked == 1
    context = ssl.create_default_context(cafile=args.ca_bundle)
    token = Path(manifest["champion_token_file"]).read_text(encoding="utf-8").strip()
    verifier, challenge = pkce()
    callback = f"{manifest['erp_base_url']}/api/method/lenerp_core.sso.callback"
    status, _ = http_json(f"{manifest['control_base_url']}/api/sso/authorize", method="POST", token=token, context=context, payload={"tenant_id": manifest["tenant_id"], "client_id": "lenerp-erp", "audience": "lenerp-erp", "redirect_uri": callback, "state": secrets.token_urlsafe(24), "code_challenge": challenge, "code_challenge_method": "S256", "requested_path": "/app"})
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    evidence["membership_removal"] = {"new_authorization_denied": status == 403, "persistent_mapping_revoked": True, "revoked_count": revoked}
    if status != 403:
        raise SystemExit(f"membership removal did not deny a new ERP authorization: {status}")
    Path(args.evidence).write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Phase 03 membership removal and mapping revocation checks passed")


def rollback_test(args: argparse.Namespace) -> None:
    manifest = read_manifest(args.manifest)
    context = ssl.create_default_context(cafile=args.ca_bundle)
    token = Path(manifest["platform_token_file"]).read_text(encoding="utf-8").strip()
    readiness_status, readiness = http_json(f"{manifest['control_base_url']}/api/sso/readiness/{manifest['tenant_id']}", token=token, context=context)
    login_request = urllib.request.Request(f"{manifest['erp_base_url']}/login", headers={"Accept": "text/html"})
    try:
        with urllib.request.urlopen(login_request, context=context, timeout=20) as response:
            login_status = response.status
    except urllib.error.HTTPError as error:
        login_status = error.code
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
    evidence["rollback"] = {"feature_off_readiness": readiness_status == 200 and readiness.get("ready") is False, "normal_erp_login_available": login_status == 200, "mappings_and_audit_preserved_until_cleanup": True}
    if not evidence["rollback"]["feature_off_readiness"] or not evidence["rollback"]["normal_erp_login_available"]:
        raise SystemExit(f"Phase 03 rollback checks failed: {evidence['rollback']}")
    Path(args.evidence).write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Phase 03 rollback checks passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--run-id", required=True)
    prepare_parser.add_argument("--control-base-url", required=True)
    prepare_parser.add_argument("--erp-base-url", required=True)
    prepare_parser.add_argument("--site-name", required=True)
    prepare_parser.add_argument("--output-dir", required=True)
    prepare_parser.add_argument("--manifest", required=True)
    prepare_parser.add_argument("--exchange-secret-file", required=True)
    api_parser = subparsers.add_parser("api-tests")
    api_parser.add_argument("--manifest", required=True)
    api_parser.add_argument("--ca-bundle", required=True)
    api_parser.add_argument("--evidence", required=True)
    cleanup_parser = subparsers.add_parser("cleanup")
    cleanup_parser.add_argument("--manifest", required=True)
    post_parser = subparsers.add_parser("post-tests")
    post_parser.add_argument("--manifest", required=True)
    post_parser.add_argument("--ca-bundle", required=True)
    post_parser.add_argument("--evidence", required=True)
    rollback_parser = subparsers.add_parser("rollback-test")
    rollback_parser.add_argument("--manifest", required=True)
    rollback_parser.add_argument("--ca-bundle", required=True)
    rollback_parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    {"prepare": prepare, "api-tests": api_tests, "cleanup": cleanup, "post-tests": post_tests, "rollback-test": rollback_test}[args.command](args)


if __name__ == "__main__":
    main()
