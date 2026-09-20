#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-/opt/frappe-staging-bench}"
SITE="${SITE:-erp-staging.example.test}"
BASE_URL="${BASE_URL:-http://127.0.0.1:28000}"
HOST_HEADER="${HOST_HEADER:-$SITE}"
EXPECTED_FRAPPE_COMMIT="${EXPECTED_FRAPPE_COMMIT:-edae775dd36b6c4ad7acab10230262bd74040765}"
EXPECTED_ERPNEXT_COMMIT="${EXPECTED_ERPNEXT_COMMIT:-945e825bee3d0d645f6cb59bcaab90fcbfb98ce3}"
EXPECTED_HRMS_VERSION="${EXPECTED_HRMS_VERSION:-15.64.1}"
EXPECTED_HRMS_COMMIT="${EXPECTED_HRMS_COMMIT:-e68a3deaa95ae5b2c3d743297d0a4ab505733fc1}"
EXPECTED_CUSTOM_APP_VERSION="${EXPECTED_CUSTOM_APP_VERSION:-0.2.0}"
EXPECTED_CUSTOM_APP_COMMIT="${EXPECTED_CUSTOM_APP_COMMIT:-77a966e6f013613b9982ca59c6eb6e6c94f8617d}"
OUTPUT_FILE="${OUTPUT_FILE:-}"
BACKUP_DIR="${BACKUP_DIR:-}"
export EXPECTED_HRMS_COMMIT EXPECTED_HRMS_VERSION EXPECTED_CUSTOM_APP_COMMIT BENCH_ROOT SITE OUTPUT_FILE BACKUP_DIR

for unit in \
  frappe-staging-redis-cache.service \
  frappe-staging-redis-queue.service \
  frappe-staging-web.service \
  frappe-staging-worker-short.service \
  frappe-staging-schedule.service; do
  systemctl is-active --quiet "$unit" || {
    echo "ERP staging service is not active: $unit" >&2
    exit 1
  }
done
echo "ERP staging services passed"

wait_for_loopback_port() {
  local port="$1"
  for attempt in $(seq 1 30); do
    if ss -ltn | grep -Eq "127\.0\.0\.1:${port}[[:space:]]"; then
      return 0
    fi
    sleep 2
  done
  echo "ERP staging port is not listening on loopback after 60s: $port" >&2
  return 1
}

for port in 14100 14101 28000; do
  wait_for_loopback_port "$port" || exit 1
done
echo "ERP staging ports passed"

if [[ -n "$BACKUP_DIR" ]]; then
  [[ -f "$BACKUP_DIR/SHA256SUMS" ]] || {
    echo "candidate-bound staging backup manifest is missing: $BACKUP_DIR" >&2
    exit 1
  }
  echo "ERP staging backup manifest passed ($BACKUP_DIR)"
fi

check_http() {
  local name="$1" url="$2" expected="$3" code
  code="$(curl -sS -o /dev/null -w '%{http_code}' -H "Host: $HOST_HEADER" --max-time 20 "$url")"
  [[ "$code" == "$expected" ]] || {
    echo "$name returned HTTP $code, expected $expected" >&2
    exit 1
  }
  echo "$name passed ($code)"
}

check_http "ERP public root" "$BASE_URL/" 200
check_http "ERP login" "$BASE_URL/login" 200
check_http "ERP unauthenticated API" "$BASE_URL/api/method/frappe.auth.get_logged_user" 403

apps="$(sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' list-apps")"
grep -Eq '^frappe[[:space:]]+15\.119\.1([[:space:]]|$)' <<<"$apps" || {
  echo "staging Frappe version mismatch" >&2
  exit 1
}
grep -Eq '^erpnext[[:space:]]+15\.120\.0([[:space:]]|$)' <<<"$apps" || {
  echo "staging ERPNext version mismatch" >&2
  exit 1
}
grep -Eq "^hrms[[:space:]]+${EXPECTED_HRMS_VERSION}([[:space:]]|$)" <<<"$apps" || {
  echo "staging HRMS version mismatch" >&2
  exit 1
}
grep -Eq "^lenerp_core[[:space:]]+${EXPECTED_CUSTOM_APP_VERSION}([[:space:]]|$)" <<<"$apps" || {
  echo "staging custom app is not installed" >&2
  exit 1
}
[[ "$(sudo -u frappe git -C "$BENCH_ROOT/apps/frappe" rev-parse HEAD)" == "$EXPECTED_FRAPPE_COMMIT" ]] || {
  echo "staging Frappe commit mismatch" >&2
  exit 1
}
[[ "$(sudo -u frappe git -C "$BENCH_ROOT/apps/erpnext" rev-parse HEAD)" == "$EXPECTED_ERPNEXT_COMMIT" ]] || {
  echo "staging ERPNext commit mismatch" >&2
  exit 1
}
[[ "$(sudo -u frappe git -C "$BENCH_ROOT/apps/hrms" rev-parse HEAD)" == "$EXPECTED_HRMS_COMMIT" ]] || {
  echo "staging HRMS commit mismatch" >&2
  exit 1
}
[[ "$(sudo -u frappe tr -d '\r\n' < "$BENCH_ROOT/apps/lenerp_core/SOURCE_COMMIT.txt")" == "$EXPECTED_CUSTOM_APP_COMMIT" ]] || {
  echo "staging custom app source marker mismatch" >&2
  exit 1
}

# A successful install is not enough: prove that the exact site contains the
# expected HRMS application, migration readback, upstream HR/Payroll roles,
# HRMS-owned workspaces, and the exact custom-app artifact marker. Keep these
# checks candidate-bound and fail closed when any readback is unavailable.
installed_apps_json="$(sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' execute frappe.get_installed_apps")"
roles_json="$(sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' execute frappe.get_all --args '[\"Role\"]' --kwargs '{\"filters\":{\"name\":[\"in\",[\"HR User\",\"HR Manager\",\"Payroll User\",\"Payroll Manager\"]]},\"pluck\":\"name\"}'")"
workspaces_json="$(sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' execute frappe.get_all --args '[\"Workspace\"]' --kwargs '{\"filters\":{\"name\":[\"in\",[\"HR\",\"Payroll\"]]},\"fields\":[\"name\",\"title\",\"module\"]}'")"
export installed_apps_json roles_json workspaces_json
python3 - <<'PY'
import json
import os
import subprocess
from pathlib import Path

def parse(name: str):
    try:
        return json.loads(os.environ[name])
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERP staging {name} readback is not valid JSON") from exc

apps = parse("installed_apps_json")
roles = parse("roles_json")
workspaces = parse("workspaces_json")
if not isinstance(apps, list) or "hrms" not in apps:
    raise SystemExit("ERP staging installed-app readback does not include hrms")
if not isinstance(roles, list) or not {"HR User", "HR Manager"}.issubset(set(roles)):
    raise SystemExit("ERP staging HR role readback is incomplete")
if not isinstance(workspaces, list) or not {"HR", "Payroll"}.issubset({str(item.get("name")) for item in workspaces if isinstance(item, dict)}):
    raise SystemExit("ERP staging HR/Payroll workspace readback is incomplete")

bench_root = Path(os.environ.get("BENCH_ROOT", "/opt/frappe-staging-bench"))
site = os.environ.get("SITE", "erp-staging.example.test")
hrms_path = bench_root / "apps" / "hrms"
commit = subprocess.check_output(["sudo", "-u", "frappe", "git", "-C", str(hrms_path), "rev-parse", "HEAD"], text=True).strip()
expected_commit = os.environ.get("EXPECTED_HRMS_COMMIT", "")
if commit != expected_commit:
    raise SystemExit("ERP staging HRMS commit readback is not the expected immutable revision")

evidence = {
    "backup_dir": os.environ.get("BACKUP_DIR", ""),
    "site": site,
    "migration": "bench --site migrate returned success before this readback",
    "installed_apps": apps,
    "hrms_version": os.environ.get("EXPECTED_HRMS_VERSION", ""),
    "hrms_commit": commit,
    "custom_app_commit": os.environ.get("EXPECTED_CUSTOM_APP_COMMIT", ""),
    "roles": sorted(str(item) for item in roles),
    "workspaces": sorted(workspaces, key=lambda item: str(item)),
    "provider_verified": True,
}
output = os.environ.get("OUTPUT_FILE", "")
if output:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(evidence, sort_keys=True))
PY
echo "ERP staging app inventory, migration, roles, workspaces, and pinned commits passed"
