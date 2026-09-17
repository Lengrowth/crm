#!/usr/bin/env python3
"""Run the release smoke contract against disposable local services."""

from __future__ import annotations

import os
import json
import secrets
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
BACKEND_PYTHON = Path(os.environ.get("LOCAL_SMOKE_PYTHON", str(BACKEND / ".venv" / "Scripts" / "python.exe")))
ALEMBIC = Path(os.environ.get("LOCAL_SMOKE_ALEMBIC", str(BACKEND / ".venv" / "Scripts" / "alembic.exe")))
ALEMBIC_AS_MODULE = os.environ.get("LOCAL_SMOKE_ALEMBIC_AS_MODULE", "false").lower() in {"1", "true", "yes"}
NEXT_ENTRY = FRONTEND / "node_modules" / "next" / "dist" / "bin" / "next"
NODE = Path(shutil.which("node.exe") or shutil.which("node") or "")
GIT_BASH = Path(r"C:\Program Files\Git\bin\bash.exe")
BACKEND_PORT = "18001"
FRONTEND_PORT = "13000"


def wait_for(url: str, process: subprocess.Popen[bytes], host_header: str, timeout: float = 45) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"service exited before becoming ready: {url}")
        try:
            request = Request(url, headers={"Host": host_header})
            with urlopen(request, timeout=2) as response:
                if response.status < 500:
                    return
        except Exception:
            time.sleep(1)
    raise TimeoutError(f"service did not become ready: {url}")


def json_request(
    url: str,
    host_header: str,
    method: str = "GET",
    payload: dict[str, object] | None = None,
    token: str | None = None,
) -> tuple[int, dict[str, object]]:
    from urllib.request import Request

    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Host": host_header, "Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, {}


def git_bash_path(path: Path) -> str:
    return f"/{path.drive[0].lower()}{str(path)[2:].replace(chr(92), '/') }"


def alembic_command(*args: str) -> list[str]:
    if ALEMBIC_AS_MODULE:
        return [str(BACKEND_PYTHON), "-m", "alembic", *args]
    return [str(ALEMBIC), *args]


def create_platform_admin_session(email: str, database_path: Path) -> str:
    """Create a disposable platform-admin fixture for admin-only smoke routes."""
    if str(BACKEND) not in sys.path:
        sys.path.insert(0, str(BACKEND))
    from app.core.security import generate_session_token, hash_session_token
    from app.models.domain import AuthSession, SaaSUser
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    token = generate_session_token()
    now = datetime.now(timezone.utc)
    engine = create_engine(f"sqlite:///{database_path.as_posix()}", connect_args={"check_same_thread": False}, future=True)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    with Session() as session:
        user = SaaSUser(
            email=email,
            full_name="Phase 2 Local Smoke Admin",
            password_hash=None,
            status="active",
            is_platform_admin=True,
            email_verified_at=now,
        )
        session.add(user)
        session.flush()
        session.add(
            AuthSession(
                user_id=user.id,
                session_token_hash=hash_session_token(token),
                expires_at=now + timedelta(hours=1),
            )
        )
        session.commit()
    engine.dispose()
    return token


def main() -> int:
    required = (BACKEND_PYTHON, GIT_BASH, NODE, NEXT_ENTRY, FRONTEND / ".next")
    if not ALEMBIC_AS_MODULE:
        required = (*required, ALEMBIC)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"local smoke prerequisites missing: {', '.join(missing)}")

    db_path = BACKEND / "plat_p0_local_smoke.db"
    auth_file = BACKEND / "plat_p0_local_smoke_auth.token"
    admin_auth_file = BACKEND / "plat_p2_local_smoke_admin.token"
    manifest_path = BACKEND / "plat_p0_local_smoke_manifest.json"
    if db_path.exists():
        db_path.unlink()
    if auth_file.exists():
        auth_file.unlink()
    if admin_auth_file.exists():
        admin_auth_file.unlink()
    if manifest_path.exists():
        manifest_path.unlink()
    manifest_path.write_text(
        json.dumps(
            {
                "release_id": "PLAT-P0-local-smoke",
                "control_plane_commit": "local-smoke",
                "environment": "staging",
                "build_time_utc": "synthetic",
                "operator": "local-smoke",
                "upstream_frappe_commit": "synthetic-frappe",
                "upstream_erpnext_commit": "synthetic-erpnext",
                "custom_app_version": "0.1.0",
                "custom_app_commit": "synthetic-lenerp-core",
                "installed_apps": {
                    "frappe": {"commit": "synthetic-frappe"},
                    "erpnext": {"commit": "synthetic-erpnext"},
                    "lenerp_core": {
                        "version": "0.1.0",
                        "commit": "synthetic-lenerp-core",
                    },
                },
                "database_revision_before": "synthetic",
                "database_revision_after": "synthetic",
                "dependency_lock_hashes": {},
                "feature_flags": {"future_menu": False},
            }
        ),
        encoding="utf-8",
    )

    env = os.environ.copy()
    env.update(
        {
            "DATABASE_URL": "sqlite:///./plat_p0_local_smoke.db",
            "ENVIRONMENT": "staging",
            "ERPNEXT_MODE": "mock",
            "ERPNEXT_ALLOW_MOCK_IN_NON_LOCAL": "true",
            "RELEASE_ID": "PLAT-P0-local-smoke",
            "RELEASE_MANIFEST_PATH": str(manifest_path),
            "FEATURE_FLAGS": "future_menu=off",
        }
    )
    os.environ.update(env)
    backend_process: subprocess.Popen[bytes] | None = None
    frontend_process: subprocess.Popen[bytes] | None = None
    try:
        subprocess.run(alembic_command("upgrade", "head"), cwd=BACKEND, env=env, check=True)
        backend_process = subprocess.Popen(
            [str(BACKEND_PYTHON), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", BACKEND_PORT],
            cwd=BACKEND,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        frontend_process = subprocess.Popen(
            [str(NODE), str(NEXT_ENTRY), "start", "-p", FRONTEND_PORT],
            cwd=FRONTEND,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        host_header = "staging.example.test"
        wait_for(f"http://127.0.0.1:{BACKEND_PORT}/health", backend_process, host_header)
        wait_for(f"http://127.0.0.1:{FRONTEND_PORT}/", frontend_process, host_header)

        smoke_email = f"phase0-{secrets.token_urlsafe(10)}@example.test"
        smoke_password = secrets.token_urlsafe(24)
        register_status, register_payload = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/auth/register",
            host_header,
            method="POST",
            payload={
                "email": smoke_email,
                "full_name": "Phase 0 Smoke User",
                "password": smoke_password,
                "organization_name": "Phase 0 Synthetic Workspace",
                "membership_role": "owner",
            },
        )
        if register_status != 200 or not register_payload.get("access_token"):
            raise RuntimeError(f"synthetic registration failed with HTTP {register_status}")
        token = str(register_payload["access_token"])
        me_status, _ = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/auth/me", host_header, token=token
        )
        org_status, _ = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/organizations", host_header, token=token
        )
        unauthorized_status, _ = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/organizations", host_header
        )
        if me_status != 200 or org_status != 200 or unauthorized_status != 401:
            raise RuntimeError(
                f"authenticated/authorization smoke failed: me={me_status}, organizations={org_status}, unauthorized={unauthorized_status}"
            )
        login_status, login_payload = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/auth/login",
            host_header,
            method="POST",
            payload={"email": smoke_email, "password": smoke_password},
        )
        if login_status != 200 or not login_payload.get("access_token"):
            raise RuntimeError(f"synthetic login failed with HTTP {login_status}")
        auth_file.write_text(str(login_payload["access_token"]), encoding="utf-8")
        print("authenticated register/login/application route checks passed")

        admin_token = create_platform_admin_session(
            f"phase2-local-admin-{secrets.token_urlsafe(10)}@example.test",
            db_path,
        )
        admin_auth_file.write_text(admin_token, encoding="utf-8")
        admin_me_status, admin_me_payload = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/auth/me", host_header, token=admin_token
        )
        if admin_me_status != 200 or not admin_me_payload.get("user", {}).get("is_platform_admin"):
            raise RuntimeError(f"platform-admin fixture failed with HTTP {admin_me_status}")
        print("platform-admin implementation route fixture passed")

        membership = register_payload.get("user", {}).get("memberships", [])[0]
        organization_id = str(membership["organization_id"])
        tenant_status, tenant_payload = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/organizations/{organization_id}/tenants",
            host_header,
            method="POST",
            token=token,
            payload={
                "organization_id": organization_id,
                "tenant_slug": f"phase0-{secrets.token_urlsafe(8).lower()}",
                "environment": "staging",
                "primary_domain": host_header,
                "erpnext_site_name": host_header,
                "provisioning_status": "pending",
            },
        )
        if tenant_status != 201 or not tenant_payload.get("id"):
            raise RuntimeError(f"synthetic tenant creation failed with HTTP {tenant_status}")
        tenant_id = str(tenant_payload["id"])
        provision_status, provision_payload = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/organizations/{organization_id}/tenants/{tenant_id}/provision",
            host_header,
            method="POST",
            token=token,
            payload={"custom_app": "lenerp_core", "domain": host_header, "options": {}},
        )
        if provision_status != 202 or not provision_payload.get("id"):
            raise RuntimeError(f"synthetic provisioning request failed with HTTP {provision_status}")
        job_status, job_payload = json_request(
            f"http://127.0.0.1:{BACKEND_PORT}/provisioning/{provision_payload['id']}",
            host_header,
            token=token,
        )
        if job_status != 200 or job_payload.get("status") not in {"success", "running", "ready"}:
            raise RuntimeError(f"synthetic provisioning worker check failed with HTTP {job_status}")
        print("synthetic tenant provisioning/worker route checks passed")

        smoke_env = env | {
            "BASE_URL": f"http://127.0.0.1:{FRONTEND_PORT}",
            "BACKEND_URL": f"http://127.0.0.1:{BACKEND_PORT}",
            "EXPECTED_RELEASE": "PLAT-P0-local-smoke",
            "PYTHON_BIN": git_bash_path(BACKEND_PYTHON),
            "HOST_HEADER": host_header,
            "REQUIRE_AUTH_SMOKE": "true",
            "AUTH_TOKEN_FILE": git_bash_path(admin_auth_file),
        }
        result = subprocess.run(
            [str(GIT_BASH), "scripts/release/smoke.sh"],
            cwd=ROOT,
            env=smoke_env,
            check=False,
        )
        return result.returncode
    finally:
        for process in (frontend_process, backend_process):
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    if os.name == "nt":
                        subprocess.run(
                            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                            check=False,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    else:
                        process.kill()
                    process.wait(timeout=10)
        if db_path.exists():
            for _ in range(10):
                try:
                    db_path.unlink()
                    break
                except PermissionError:
                    time.sleep(0.5)
        if auth_file.exists():
            auth_file.unlink()
        if admin_auth_file.exists():
            admin_auth_file.unlink()
        if manifest_path.exists():
            manifest_path.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
