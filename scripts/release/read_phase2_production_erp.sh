#!/usr/bin/env bash
set -Eeuo pipefail

OUTPUT_FILE="${1:?Usage: read_phase2_production_erp.sh <output-file>}"
BENCH_DIR="${ERP_BENCH_DIR:-/home/frappe/frappe-bench}"
SITE="${ERP_SITE:-erp.lengrowth.com}"
HRMS_DIR="$BENCH_DIR/apps/hrms"

capture_as_frappe() {
  local command="$1"
  local output status
  set +e
  output="$(sudo -n -u frappe bash -lc "$command" 2>&1)"
  status=$?
  set -e
  CAPTURE_STATUS="$status"
  CAPTURE_OUTPUT="$output"
}

set +e
sudo -n test -d "$BENCH_DIR/sites/$SITE"
site_dir_status=$?
sudo -n -u frappe test -f "$BENCH_DIR/sites/$SITE/site_config.json"
site_config_status=$?
set -e

capture_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps"
apps_status="$CAPTURE_STATUS"
apps="$CAPTURE_OUTPUT"
hrms_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
hrms_commit=""
hrms_clean=false
set +e
sudo -n -u frappe test -d "$HRMS_DIR/.git"
hrms_git_dir_status=$?
set -e
if [[ "$hrms_git_dir_status" -eq 0 ]]; then
  capture_as_frappe "git -c safe.directory='$HRMS_DIR' -C '$HRMS_DIR' rev-parse HEAD"
  hrms_commit_status="$CAPTURE_STATUS"
  hrms_commit="$CAPTURE_OUTPUT"
  capture_as_frappe "git -c safe.directory='$HRMS_DIR' -C '$HRMS_DIR' status --porcelain --untracked-files=all"
  hrms_status_status="$CAPTURE_STATUS"
  hrms_status="$CAPTURE_OUTPUT"
  if [[ "$hrms_status_status" -eq 0 && -z "$hrms_status" ]]; then
    hrms_clean=true
  fi
else
  hrms_commit_status=1
  hrms_status_status=1
  hrms_status="HRMS git directory is absent"
fi

capture_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' show-pending-migrations"
pending_status="$CAPTURE_STATUS"
pending_migrations="$CAPTURE_OUTPUT"
capture_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Role\",\"filters\":{\"name\":[\"in\",[\"HR User\",\"HR Manager\"]]}}'"
roles_status="$CAPTURE_STATUS"
roles_output="$CAPTURE_OUTPUT"
capture_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Workspace\",\"filters\":{\"name\":[\"in\",[\"HR\",\"Payroll\"]]}}'"
workspaces_status="$CAPTURE_STATUS"
workspaces_output="$CAPTURE_OUTPUT"

python3 - "$OUTPUT_FILE" "$SITE" "$site_dir_status" "$site_config_status" "$apps_status" "$hrms_version" "$hrms_commit_status" "$hrms_commit" "$hrms_clean" "$hrms_status_status" "$hrms_status" "$pending_status" "$pending_migrations" "$roles_status" "$roles_output" "$workspaces_status" "$workspaces_output" "$apps" <<'PY'
import json
import re
import sys
from datetime import datetime, timezone

(
    output, site, site_dir_status, site_config_status, apps_status, hrms_version,
    hrms_commit_status, hrms_commit, hrms_clean, hrms_status_status, hrms_status,
    pending_status, pending, roles_status, roles_output, workspaces_status,
    workspaces_output, apps,
) = sys.argv[1:]

def safe_lines(value: str) -> list[str]:
    value = re.sub(r"(?i)(password|secret|token|api[_ -]?key)\s*([:=])\s*\S+", r"\1\2<redacted>", value)
    return [line[:500] for line in value.splitlines()[:100]]

def integer(value: str):
    value = value.strip()
    return int(value) if value.isdigit() else None

payload = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "site": site,
    "site_state": {
        "bench_site_directory_status": int(site_dir_status),
        "site_config_status": int(site_config_status),
        "site_config_present": site_config_status == "0",
    },
    "installed_apps_raw": safe_lines(apps),
    "installed_apps_command": {"status": int(apps_status), "stderr_or_output": safe_lines(apps)},
    "hrms": {
        "present": bool(hrms_version),
        "version": hrms_version or None,
        "commit": hrms_commit.strip() or None,
        "commit_command_status": int(hrms_commit_status),
        "git_status_command_status": int(hrms_status_status),
        "git_status": safe_lines(hrms_status),
        "clean": hrms_clean == "true",
    },
    "migration": {
        "read_only_command": "bench --site show-pending-migrations",
        "command_status": int(pending_status),
        "pending_output": safe_lines(pending),
    },
    "roles": {"command_status": int(roles_status), "output": safe_lines(roles_output), "count": integer(roles_output)},
    "workspaces": {"command_status": int(workspaces_status), "output": safe_lines(workspaces_output), "count": integer(workspaces_output)},
}
with open(output, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
chmod 600 "$OUTPUT_FILE"
echo "Non-mutating Phase 02 production ERP readback written: $OUTPUT_FILE"
