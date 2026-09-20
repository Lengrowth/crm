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

[[ -s "$BACKUP_EVIDENCE_FILE" ]] || { echo "verified production backup evidence is required" >&2; exit 1; }
backup_dir="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["local_backup_dir"])' "$BACKUP_EVIDENCE_FILE")"
sudo -n test -d "$backup_dir/erp"
sudo -n test -s "$backup_dir/manifest.sha256"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
sudo -n bash "$SCRIPT_DIR/verify_backup_manifest.sh" "$backup_dir" >/dev/null

rollback_site() {
  echo "Phase 02 ERP mutation failed; restoring the verified pre-mutation ERP backup" >&2
  database="$(find "$backup_dir/erp" -maxdepth 1 -type f -name '*-database.sql.gz' -print -quit)"
  public_files="$(find "$backup_dir/erp" -maxdepth 1 -type f -name '*-files.tar' -not -name '*private-files.tar' -print -quit)"
  private_files="$(find "$backup_dir/erp" -maxdepth 1 -type f -name '*-private-files.tar' -print -quit)"
  [[ -n "$database" && -n "$public_files" && -n "$private_files" ]] || return 1
  sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' restore '$database' --force --with-public-files '$public_files' --with-private-files '$private_files'"
  sudo -n supervisorctl restart frappe-bench-web:frappe-bench-frappe-web frappe-bench-web:frappe-bench-node-socketio frappe-bench-workers:frappe-bench-frappe-short-worker frappe-bench-workers:frappe-bench-frappe-long-worker frappe-bench-workers:frappe-bench-frappe-schedule
}
trap 'status=$?; if [[ "$status" -ne 0 ]]; then rollback_site || echo "CRITICAL: ERP backup restore failed" >&2; fi; exit "$status"' EXIT

apps="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
if ! grep -Eq '^hrms[[:space:]]+15\.64\.1([[:space:]]|$)' <<<"$apps"; then
  echo "Pinned HRMS is not already installed; the Phase 02 production gate refuses an unreviewed production mutation." >&2
  exit 1
fi
grep -Eq "^frappe[[:space:]]+$FRAPPE_VERSION([[:space:]]|$)" <<<"$apps"
grep -Eq "^erpnext[[:space:]]+$ERPNEXT_VERSION([[:space:]]|$)" <<<"$apps"
grep -Eq "^lenerp_core[[:space:]]+$LENERP_VERSION([[:space:]]|$)" <<<"$apps"
for app in frappe erpnext hrms; do
  sudo -n test -d "$BENCH_DIR/apps/$app/.git"
done
sudo -n test -f "$LENERP_DIR/SOURCE_COMMIT.txt"
test "$(sudo -n -u frappe git -C "$BENCH_DIR/apps/frappe" rev-parse HEAD)" = "$FRAPPE_COMMIT"
test "$(sudo -n -u frappe git -C "$BENCH_DIR/apps/erpnext" rev-parse HEAD)" = "$ERPNEXT_COMMIT"
test "$(sudo -n -u frappe git -C "$HRMS_DIR" rev-parse HEAD)" = "$HRMS_COMMIT"
test "$(sudo -n -u frappe tr -d '\r\n' < "$LENERP_DIR/SOURCE_COMMIT.txt")" = "$LENERP_COMMIT"
sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench setup requirements hrms"
sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' migrate"
sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench build --app hrms"
sudo -n supervisorctl restart frappe-bench-web:frappe-bench-frappe-web frappe-bench-web:frappe-bench-node-socketio frappe-bench-workers:frappe-bench-frappe-short-worker frappe-bench-workers:frappe-bench-frappe-long-worker frappe-bench-workers:frappe-bench-frappe-schedule

apps="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
grep -Eq '^hrms[[:space:]]' <<<"$apps"
installed_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
[[ "$installed_version" == "15.64.1" ]]
role_count="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Role\",\"filters\":{\"name\":[\"in\",[\"HR User\",\"HR Manager\",\"Champion Administrator\",\"Champion Dispatcher\",\"Champion Sales User\",\"Champion Accounting User\",\"Champion Inventory Manager\",\"Champion Field Technician\",\"Champion Platform Operator\"]]}}'" | tr -d '\r\n ' )"
[[ "$role_count" == "9" ]]
workspace_count="$(sudo -n -u frappe bash -lc "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --args '{\"doctype\":\"Workspace\",\"filters\":{\"name\":[\"in\",[\"HR\",\"Payroll\",\"Champion ERP\"]]}}'" | tr -d '\r\n ' )"
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
