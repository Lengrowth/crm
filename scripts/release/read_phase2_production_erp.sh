#!/usr/bin/env bash
set -Eeuo pipefail

OUTPUT_FILE="${1:?Usage: read_phase2_production_erp.sh <output-file>}"
BENCH_DIR="${ERP_BENCH_DIR:-/home/frappe/frappe-bench}"
SITE="${ERP_SITE:-erp.lengrowth.com}"
HRMS_DIR="$BENCH_DIR/apps/hrms"

sudo -n test -d "$BENCH_DIR/sites/$SITE"
sudo -n -u frappe test -f "$BENCH_DIR/sites/$SITE/site_config.json"

apps="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
hrms_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
hrms_commit=""
hrms_clean=false
if sudo -n -u frappe test -d "$HRMS_DIR/.git"; then
  hrms_commit="$(sudo -n -u frappe git -c safe.directory="$HRMS_DIR" -C "$HRMS_DIR" rev-parse HEAD)"
  [[ -z "$(sudo -n -u frappe git -c safe.directory="$HRMS_DIR" -C "$HRMS_DIR" status --porcelain --untracked-files=all)" ]]
  hrms_clean=true
fi

pending_migrations="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' show-pending-migrations" 2>&1 || true)"
role_count="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Role\",\"filters\":{\"name\":[\"in\",[\"HR User\",\"HR Manager\"]]}}'" | tr -d '\r\n ' )"
workspace_count="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Workspace\",\"filters\":{\"name\":[\"in\",[\"HR\",\"Payroll\"]]}}'" | tr -d '\r\n ' )"

python3 - "$OUTPUT_FILE" "$SITE" "$hrms_version" "$hrms_commit" "$hrms_clean" "$role_count" "$workspace_count" "$apps" "$pending_migrations" <<'PY'
import json
import sys
from datetime import datetime, timezone

output, site, hrms_version, hrms_commit, hrms_clean, roles, workspaces, apps, pending = sys.argv[1:]
payload = {
    "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    "site": site,
    "installed_apps_raw": apps.splitlines(),
    "hrms": {
        "present": bool(hrms_version),
        "version": hrms_version or None,
        "commit": hrms_commit or None,
        "clean": hrms_clean == "true",
    },
    "migration": {
        "read_only_command": "bench --site show-pending-migrations",
        "pending_output": pending.splitlines(),
    },
    "roles": {"HR User": None, "HR Manager": None, "count": int(roles) if roles.isdigit() else None},
    "workspaces": {"HR": None, "Payroll": None, "count": int(workspaces) if workspaces.isdigit() else None},
    "site_config_present": True,
}
with open(output, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
chmod 600 "$OUTPUT_FILE"
echo "Non-mutating Phase 02 production ERP readback written: $OUTPUT_FILE"
