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


def git_state(path: Path) -> dict[str, object]:
    if not (path / ".git").exists():
        return {"path": str(path), "present": False}
    head = command("git", "-C", str(path), "rev-parse", "HEAD")
    dirty = command("git", "-C", str(path), "status", "--porcelain", "--untracked-files=all")
    return {"path": str(path), "present": True, "head": head, "clean": not bool(dirty)}


def database_counts() -> dict[str, int | None]:
    try:
        sys.path.insert(0, str(Path(app_root) / "current" / "backend"))
        from sqlalchemy import func, select
        from app.db.session import SessionLocal
        from app.models.domain import AuthSession, Organization, SaaSUser

        with SessionLocal() as session:
            prefix = "phase0-production-smoke-%"
            return {
                "smoke_users": session.scalar(
                    select(func.count()).select_from(SaaSUser).where(SaaSUser.email.like(prefix + "@example.test"))
                ),
                "smoke_organizations": session.scalar(
                    select(func.count()).select_from(Organization).where(Organization.name.like("Phase 0 Production Smoke %"))
                ),
                "active_sessions": session.scalar(
                    select(func.count()).select_from(AuthSession).where(AuthSession.expires_at > __import__("datetime").datetime.now(__import__("datetime").timezone.utc))
                ),
            }
    except Exception:
        return {"smoke_users": None, "smoke_organizations": None, "active_sessions": None}


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
        }
        for rule in payload.get("Rules", [])
    ]
else:
    lifecycle["error"] = "query failed"

objects = subprocess.run(
    ["aws", "s3api", "list-objects-v2", "--bucket", bucket, "--endpoint-url", endpoint, "--query", "KeyCount", "--output", "text"],
    check=False,
    capture_output=True,
    text=True,
)

data = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "current_release": os.path.realpath(f"{app_root}/current"),
    "previous_release": os.path.realpath(f"{app_root}/previous"),
    "services": {
        "backend": service("saas-backend"),
        "frontend": service("saas-frontend"),
        "nginx": service("nginx"),
        "r2_backup_timer": service("saas-control-r2-backup.timer"),
    },
    "r2_backup_timer_enabled": command("systemctl", "is-enabled", "saas-control-r2-backup.timer") or "unknown",
    "local_health_http": command("curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:8001/health"),
    "smoke_cleanup": database_counts(),
    "source_trees": [
        git_state(Path("/home/frappe/frappe-bench/apps/frappe")),
        git_state(Path("/home/frappe/frappe-bench/apps/erpnext")),
    ],
    "r2": {
        "bucket": bucket,
        "object_count": objects.stdout.strip() if objects.returncode == 0 else None,
        "lifecycle": lifecycle,
    },
}
Path(output).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
os.chmod(output, 0o644)
print(f"non-secret production readback written: {output}")
PY
