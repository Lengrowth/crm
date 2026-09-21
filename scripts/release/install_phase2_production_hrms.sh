#!/usr/bin/env bash
set -Eeuo pipefail

OUTPUT_FILE="${OUTPUT_FILE:?Set OUTPUT_FILE}"
BACKUP_EVIDENCE_FILE="${BACKUP_EVIDENCE_FILE:?Set BACKUP_EVIDENCE_FILE}"
BENCH_DIR="${ERP_BENCH_DIR:-/home/frappe/frappe-bench}"
SITE="${ERP_SITE:-erp.lengrowth.com}"
FRAPPE_VERSION="15.119.1"
FRAPPE_COMMIT="edae775dd36b6c4ad7acab10230262bd74040765"
ERPNEXT_VERSION="15.120.0"
ERPNEXT_COMMIT="945e825bee3d0d645f6cb59bcaab90fcbfb98ce3"
HRMS_COMMIT="e68a3deaa95ae5b2c3d743297d0a4ab505733fc1"
LENERP_VERSION="0.2.0"
LENERP_COMMIT="a7e47208baf6583295f5f2632f4787262cd3f475"
HRMS_DIR="$BENCH_DIR/apps/hrms"
LENERP_DIR="$BENCH_DIR/apps/lenerp_core"
SUDO_BIN="${SUDO_BIN:-sudo}"
SUPERVISORCTL_BIN="${SUPERVISORCTL_BIN:-supervisorctl}"
MUTATION_STARTED=0

run_as_frappe() {
  "$SUDO_BIN" -n -u frappe bash -lc "$1"
}

run_root() {
  "$SUDO_BIN" -n "$@"
}

[[ -s "$BACKUP_EVIDENCE_FILE" ]] || { echo "verified production backup evidence is required" >&2; exit 1; }
backup_dir="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["local_backup_dir"])' "$BACKUP_EVIDENCE_FILE")"
run_root test -d "$backup_dir/erp"
run_root test -s "$backup_dir/manifest.sha256"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
run_root bash "$SCRIPT_DIR/verify_backup_manifest.sh" "$backup_dir" >/dev/null

rollback_site() {
  echo "Phase 02 ERP mutation failed; restoring the verified pre-mutation ERP backup" >&2
  database="$(find "$backup_dir/erp" -maxdepth 1 -type f -name '*-database.sql.gz' -print -quit)"
  public_files="$(find "$backup_dir/erp" -maxdepth 1 -type f -name '*-files.tar' -not -name '*private-files.tar' -print -quit)"
  private_files="$(find "$backup_dir/erp" -maxdepth 1 -type f -name '*-private-files.tar' -print -quit)"
  [[ -n "$database" && -n "$public_files" && -n "$private_files" ]] || return 1
  run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' restore '$database' --force --with-public-files '$public_files' --with-private-files '$private_files'"
  run_root "$SUPERVISORCTL_BIN" restart frappe-bench-web:frappe-bench-frappe-web frappe-bench-web:frappe-bench-node-socketio frappe-bench-workers:frappe-bench-frappe-short-worker frappe-bench-workers:frappe-bench-frappe-long-worker frappe-bench-workers:frappe-bench-frappe-schedule
}
trap 'status=$?; if [[ "$status" -ne 0 && "$MUTATION_STARTED" -eq 1 ]]; then rollback_site || echo "CRITICAL: ERP backup restore failed" >&2; fi; exit "$status"' EXIT

apps="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
installed_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
if [[ -n "$installed_version" && "$installed_version" != "15.64.1" ]]; then
  echo "Installed HRMS version '$installed_version' is not the approved 15.64.1; no mutation was attempted." >&2
  exit 1
fi
grep -Eq "^frappe[[:space:]]+$FRAPPE_VERSION([[:space:]]|$)" <<<"$apps" || { echo "Frappe version is not the approved pin; no mutation was attempted." >&2; exit 1; }
grep -Eq "^erpnext[[:space:]]+$ERPNEXT_VERSION([[:space:]]|$)" <<<"$apps" || { echo "ERPNext version is not the approved pin; no mutation was attempted." >&2; exit 1; }
grep -Eq "^lenerp_core[[:space:]]+$LENERP_VERSION([[:space:]]|$)" <<<"$apps" || { echo "lenerp_core version is not the approved pin; no mutation was attempted." >&2; exit 1; }
for app in frappe erpnext; do
  run_root test -d "$BENCH_DIR/apps/$app/.git" || { echo "$app source checkout is absent; no mutation was attempted." >&2; exit 1; }
done
run_root test -d "$HRMS_DIR/.git" || { echo "HRMS source checkout is absent or not a Git checkout; no mutation was attempted." >&2; exit 1; }
run_root test -f "$LENERP_DIR/SOURCE_COMMIT.txt" || { echo "lenerp_core source marker is absent; no mutation was attempted." >&2; exit 1; }
test "$(run_as_frappe "git -c safe.directory='$BENCH_DIR/apps/frappe' -C '$BENCH_DIR/apps/frappe' rev-parse HEAD")" = "$FRAPPE_COMMIT" || { echo "Frappe source commit is not the approved pin; no mutation was attempted." >&2; exit 1; }
test "$(run_as_frappe "git -c safe.directory='$BENCH_DIR/apps/erpnext' -C '$BENCH_DIR/apps/erpnext' rev-parse HEAD")" = "$ERPNEXT_COMMIT" || { echo "ERPNext source commit is not the approved pin; no mutation was attempted." >&2; exit 1; }
test "$(run_as_frappe "git -c safe.directory='$HRMS_DIR' -C '$HRMS_DIR' rev-parse HEAD")" = "$HRMS_COMMIT" || { echo "HRMS source commit is not the approved pin; no mutation was attempted." >&2; exit 1; }
test "$(run_as_frappe "tr -d '\r\n' < '$LENERP_DIR/SOURCE_COMMIT.txt'")" = "$LENERP_COMMIT" || { echo "lenerp_core source marker is not the approved pin; no mutation was attempted." >&2; exit 1; }

if [[ -z "$installed_version" ]]; then
  echo "HRMS is absent; installing the approved source once through Bench."
  MUTATION_STARTED=1
  run_as_frappe "cd '$BENCH_DIR' && bench setup requirements hrms"
  run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' install-app hrms"
else
  echo "HRMS 15.64.1 is already installed at the approved source; replaying without reinstall."
  MUTATION_STARTED=1
  run_as_frappe "cd '$BENCH_DIR' && bench setup requirements hrms"
fi
run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' migrate"
run_as_frappe "cd '$BENCH_DIR' && bench build --app hrms"
run_root "$SUPERVISORCTL_BIN" restart frappe-bench-web:frappe-bench-frappe-web frappe-bench-web:frappe-bench-node-socketio frappe-bench-workers:frappe-bench-frappe-short-worker frappe-bench-workers:frappe-bench-frappe-long-worker frappe-bench-workers:frappe-bench-frappe-schedule

apps="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
grep -Eq '^hrms[[:space:]]' <<<"$apps"
installed_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
[[ "$installed_version" == "15.64.1" ]]
role_count="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Role\",\"filters\":{\"name\":[\"in\",[\"HR User\",\"HR Manager\",\"Champion Administrator\",\"Champion Dispatcher\",\"Champion Sales User\",\"Champion Accounting User\",\"Champion Inventory Manager\",\"Champion Field Technician\",\"Champion Platform Operator\"]]}}'" | tr -d '\r\n ' )"
[[ "$role_count" == "9" ]]
workspace_count="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Workspace\",\"filters\":{\"name\":[\"in\",[\"HR\",\"Payroll\",\"Champion ERP\"]]}}'" | tr -d '\r\n ' )"
[[ "$workspace_count" == "3" ]]

python3 - "$OUTPUT_FILE" "$HRMS_COMMIT" "$installed_version" "$role_count" "$workspace_count" <<'PY'
import json
import sys
from datetime import datetime, timezone

output, commit, version, roles, workspaces = sys.argv[1:]
payload = {
    "status": "passed",
    "site": "erp.lengrowth.com",
    "hrms_version": version,
    "hrms_commit": commit,
    "installed_apps_verified": True,
    "migration": "bench --site migrate returned success",
    "roles": ["HR User", "HR Manager", "Champion Administrator", "Champion Dispatcher", "Champion Sales User", "Champion Accounting User", "Champion Inventory Manager", "Champion Field Technician", "Champion Platform Operator"],
    "role_count": int(roles),
    "workspaces": ["HR", "Payroll", "Champion ERP"],
    "workspace_count": int(workspaces),
    "verified_at_utc": datetime.now(timezone.utc).isoformat(),
}
with open(output, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
trap - EXIT
echo "Production Phase 02 HRMS install, migration, and readback passed"
