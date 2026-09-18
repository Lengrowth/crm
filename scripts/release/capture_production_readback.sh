#!/usr/bin/env bash
set -Eeuo pipefail

OUTPUT_FILE="${1:?Usage: capture_production_readback.sh <output-file>}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
BACKEND_ENV_FILE="${BACKEND_ENV_FILE:-$APP_ROOT/shared/env/backend.env}"
R2_ENV_FILE="${R2_ENV_FILE:-/etc/saas-control/r2-backup.env}"

[[ -r "$BACKEND_ENV_FILE" ]] || { echo "backend environment file is missing" >&2; exit 1; }
[[ -r "$R2_ENV_FILE" ]] || { echo "R2 environment file is missing" >&2; exit 1; }

# shellcheck disable=SC1090
source "$BACKEND_ENV_FILE"
# shellcheck disable=SC1090
source "$R2_ENV_FILE"
export DATABASE_URL

export AWS_ACCESS_KEY_ID="${R2_ACCESS_KEY_ID:?R2_ACCESS_KEY_ID is required}"
export AWS_SECRET_ACCESS_KEY="${R2_SECRET_ACCESS_KEY:?R2_SECRET_ACCESS_KEY is required}"
export AWS_DEFAULT_REGION="auto"
export AWS_EC2_METADATA_DISABLED="true"
R2_ENDPOINT="${R2_ENDPOINT_URL:-https://${R2_ACCOUNT_ID}.eu.r2.cloudflarestorage.com}"

mkdir -p "$(dirname "$OUTPUT_FILE")"
python3 - "$OUTPUT_FILE" "$APP_ROOT" "$R2_BUCKET" "$R2_ENDPOINT" <<'PY'
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

output, app_root, bucket, endpoint = sys.argv[1:]


def command(*args: str) -> str:
    result = subprocess.run(args, check=False, capture_output=True, text=True)
    return result.stdout.strip()


def service(name: str) -> str:
    return command("systemctl", "is-active", name) or "unknown"


def runtime_release() -> dict[str, object]:
    raw = command("curl", "-fsS", "--max-time", "10", "http://127.0.0.1:8001/runtime/release")
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {"available": False}
    return {
        "available": True,
        "release_id": payload.get("release_id"),
        "commit": payload.get("commit"),
        "environment": payload.get("environment"),
        "platform_phase1_shell": payload.get("feature_flags", {}).get("platform_phase1_shell"),
        "feature_flags": payload.get("feature_flags", {}),
        "manifest_build_environment": payload.get("manifest", {}).get("build_environment", payload.get("manifest", {}).get("environment")),
        "database_revision_before": payload.get("manifest", {}).get("database_revision_before"),
        "database_revision_after": payload.get("manifest", {}).get("database_revision_after"),
    }


def git_state(path: Path) -> dict[str, object]:
    if not (path / ".git").exists():
        return {"path": str(path), "present": False}
    head = command("git", "-c", f"safe.directory={path}", "-C", str(path), "rev-parse", "HEAD")
    dirty = command(
        "git",
        "-c",
        f"safe.directory={path}",
        "-C",
        str(path),
        "status",
        "--porcelain",
        "--untracked-files=all",
    )
    return {"path": str(path), "present": True, "head": head, "clean": not bool(dirty)}


def database_counts() -> dict[str, int | None]:
    database_url = os.environ.get("DATABASE_URL", "")
    if not database_url.startswith("sqlite:///"):
        return {"smoke_users": None, "smoke_organizations": None, "active_sessions": None}
    database_path = database_url.removeprefix("sqlite:///")
    sql = """
    SELECT
      (SELECT count(*) FROM saas_users WHERE email LIKE 'phase0-production-smoke-%@example.test'),
      (SELECT count(*) FROM organizations WHERE name LIKE 'Phase 0 Production Smoke %'),
      (SELECT count(*) FROM auth_sessions WHERE user_id IN (SELECT id FROM saas_users WHERE email LIKE 'phase0-production-smoke-%@example.test'));
    """
    result = subprocess.run(
        ["sqlite3", "-csv", database_path, sql],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return {"smoke_users": None, "smoke_organizations": None, "active_sessions": None}
    values = result.stdout.strip().split(",")
    if len(values) != 3:
        return {"smoke_users": None, "smoke_organizations": None, "active_sessions": None}
    return {
        "smoke_users": int(values[0]),
        "smoke_organizations": int(values[1]),
        "active_sessions": int(values[2]),
    }


def phase2_cleanup_evidence() -> dict[str, object]:
    path = Path(os.environ.get("PHASE2_CLEANUP_MANIFEST", "/run/saas-control/smoke/phase2-cleanup.json"))
    if not path.is_file():
        return {"available": False}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"available": False}
    created = payload.get("created", {})
    remaining = payload.get("post_cleanup_remaining", {})
    return {
        "available": True,
        "schema_version": payload.get("schema_version"),
        "status": payload.get("status"),
        "run_id": payload.get("run_id"),
        "created_counts": {
            key: len(value) if isinstance(value, list) else 0
            for key, value in created.items()
        },
        "post_cleanup_remaining": remaining,
        "all_remaining_counts_zero": payload.get("all_remaining_counts_zero") is True,
    }


def database_revision() -> dict[str, object]:
    database_url = os.environ.get("DATABASE_URL", "")
    if not database_url.startswith("sqlite:///"):
        return {"available": False, "reason": "non-sqlite revision query requires the configured application database adapter"}
    database_path = database_url.removeprefix("sqlite:///")
    result = subprocess.run(
        ["sqlite3", database_path, "SELECT version_num FROM alembic_version ORDER BY version_num DESC LIMIT 1;"],
        check=False,
        capture_output=True,
        text=True,
    )
    revision = result.stdout.strip() if result.returncode == 0 else ""
    return {"available": bool(revision), "revision": revision or None}


def phase4_cleanup_evidence() -> dict[str, object]:
    database_url = os.environ.get("DATABASE_URL", "")
    if not database_url.startswith("sqlite:///"):
        return {"available": False, "reason": "phase4 fixture query requires the configured application database adapter"}
    database_path = database_url.removeprefix("sqlite:///")
    queries = {
        "requests": "SELECT count(*) FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%';",
        "request_versions": "SELECT count(*) FROM onboarding_request_versions WHERE request_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "management_credentials": "SELECT count(*) FROM onboarding_management_credentials WHERE request_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "decisions": "SELECT count(*) FROM onboarding_decisions WHERE request_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "organizations": "SELECT count(*) FROM organizations WHERE id IN (SELECT organization_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "memberships": "SELECT count(*) FROM organization_memberships WHERE organization_id IN (SELECT organization_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "tenants": "SELECT count(*) FROM tenants WHERE id IN (SELECT tenant_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "projects": "SELECT count(*) FROM implementation_projects WHERE id IN (SELECT implementation_project_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "tasks": "SELECT count(*) FROM implementation_tasks WHERE implementation_project_id IN (SELECT implementation_project_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "domains": "SELECT count(*) FROM domain_mappings WHERE tenant_id IN (SELECT tenant_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "organization_modules": "SELECT count(*) FROM organization_modules WHERE organization_id IN (SELECT organization_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%') AND source_type = 'onboarding';",
        "module_entitlement_audits": "SELECT count(*) FROM module_entitlement_audits WHERE organization_id IN (SELECT organization_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%') AND source_type = 'onboarding';",
        "module_application_statuses": "SELECT count(*) FROM module_application_statuses WHERE tenant_id IN (SELECT tenant_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "jobs": "SELECT count(*) FROM provisioning_jobs WHERE onboarding_request_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "active_leases": "SELECT count(*) FROM provisioning_jobs WHERE onboarding_request_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%') AND lease_expires_at IS NOT NULL;",
        "steps": "SELECT count(*) FROM provisioning_steps WHERE job_id IN (SELECT provisioning_job_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "events": "SELECT count(*) FROM provisioning_events WHERE job_id IN (SELECT provisioning_job_id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "outbox_events": "SELECT count(*) FROM provisioning_outbox_events WHERE aggregate_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "first_login_handoffs": "SELECT count(*) FROM first_login_handoffs WHERE request_id IN (SELECT id FROM onboarding_requests WHERE idempotency_key LIKE 'phase4-%');",
        "synthetic_admins": "SELECT count(*) FROM saas_users WHERE email LIKE 'phase4-admin-%@acmephase4.com';",
    }
    counts: dict[str, int | None] = {}
    for key, sql in queries.items():
        result = subprocess.run(["sqlite3", database_path, sql], check=False, capture_output=True, text=True)
        value = result.stdout.strip()
        counts[key] = int(value) if result.returncode == 0 and value.isdigit() else None
    counts["all_remaining_counts_zero"] = all(value == 0 for value in counts.values() if isinstance(value, int)) and all(value is not None for value in counts.values())
    counts["database_path_exposed"] = False
    return {"available": True, "counts": counts}


def production_erp_phase4_site_count() -> int | None:
    sites_root = Path("/home/frappe/frappe-bench/sites")
    if not sites_root.is_dir():
        return None
    return sum(1 for path in sites_root.glob("phase4-*") if path.is_dir())


lifecycle_raw = subprocess.run(
    ["aws", "s3api", "get-bucket-lifecycle-configuration", "--bucket", bucket, "--endpoint-url", endpoint, "--output", "json"],
    check=False,
    capture_output=True,
    text=True,
)
lifecycle = {"query_ok": lifecycle_raw.returncode == 0}
if lifecycle_raw.returncode == 0:
    payload = json.loads(lifecycle_raw.stdout)
    lifecycle["rules"] = [
        {
            "id": rule.get("ID"),
            "status": rule.get("Status"),
            "filter": rule.get("Filter"),
            "expiration_days": rule.get("Expiration", {}).get("Days"),
            "noncurrent_expiration_days": rule.get("NoncurrentVersionExpiration", {}).get("NoncurrentDays"),
            "abort_multipart_days": rule.get("AbortIncompleteMultipartUpload", {}).get("DaysAfterInitiation"),
        }
        for rule in payload.get("Rules", [])
    ]
else:
    lifecycle["error"] = "query failed"

objects = subprocess.run(
    ["aws", "s3api", "list-objects-v2", "--bucket", bucket, "--endpoint-url", endpoint, "--output", "json"],
    check=False,
    capture_output=True,
    text=True,
)
if objects.returncode == 0:
    object_count = len(json.loads(objects.stdout).get("Contents", []))
else:
    object_count = None

data = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "current_release": os.path.realpath(f"{app_root}/current"),
    "previous_release": os.path.realpath(f"{app_root}/previous"),
    "runtime_release": runtime_release(),
    "services": {
        "backend": service("saas-backend"),
        "frontend": service("saas-frontend"),
        "nginx": service("nginx"),
        "r2_backup_timer": service("saas-control-r2-backup.timer"),
    },
    "r2_backup_timer_enabled": command("systemctl", "is-enabled", "saas-control-r2-backup.timer") or "unknown",
    "local_health_http": command("curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:8001/health"),
    "database_revision": database_revision(),
    "smoke_cleanup": database_counts(),
    "phase2_cleanup": phase2_cleanup_evidence(),
    "phase4_cleanup": phase4_cleanup_evidence(),
    "production_erp_phase4_site_count": production_erp_phase4_site_count(),
    "source_trees": [
        git_state(Path("/home/frappe/frappe-bench/apps/frappe")),
        git_state(Path("/home/frappe/frappe-bench/apps/erpnext")),
    ],
    "r2": {
        "bucket": bucket,
        "object_count": object_count,
        "lifecycle": lifecycle,
    },
}
Path(output).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
os.chmod(output, 0o644)
print(f"non-secret production readback written: {output}")
PY
