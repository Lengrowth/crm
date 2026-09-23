#!/usr/bin/env bash
set -Eeuo pipefail

OUTPUT_FILE="${OUTPUT_FILE:?Set OUTPUT_FILE}"
BACKUP_EVIDENCE_FILE="${BACKUP_EVIDENCE_FILE:?Set BACKUP_EVIDENCE_FILE}"
RELEASE_ID="${RELEASE_ID:?Set RELEASE_ID}"
BENCH_DIR="${ERP_BENCH_DIR:-/home/frappe/frappe-bench}"
SITE="${ERP_SITE:-erp.lengrowth.com}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
PRODUCTION_RELEASE_ROOT="${PRODUCTION_RELEASE_ROOT:-/opt/saas-control/releases}"
RELEASE_DIR="$PRODUCTION_RELEASE_ROOT/$RELEASE_ID"
FRAPPE_VERSION="15.119.1"
FRAPPE_COMMIT="edae775dd36b6c4ad7acab10230262bd74040765"
ERPNEXT_VERSION="15.120.0"
ERPNEXT_COMMIT="945e825bee3d0d645f6cb59bcaab90fcbfb98ce3"
HRMS_COMMIT="e68a3deaa95ae5b2c3d743297d0a4ab505733fc1"
LENERP_VERSION="0.2.0"
LENERP_COMMIT="8d77cec7504d22f9c0a235034777e31fa07fc62"
HRMS_DIR="$BENCH_DIR/apps/hrms"
LENERP_DIR="$BENCH_DIR/apps/lenerp_core"
LENERP_SOURCE_DIR="$RELEASE_DIR/ops/staging/lenerp_core"
SUDO_BIN="${SUDO_BIN:-sudo}"
SUPERVISORCTL_BIN="${SUPERVISORCTL_BIN:-supervisorctl}"
MUTATION_STARTED=0
LENERP_WAS_PRESENT=0
ROLLBACK_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/phase2-hrms-rollback.XXXXXX")"

run_as_frappe() {
  "$SUDO_BIN" -n -u frappe bash -lc "$1"
}

run_root() {
  "$SUDO_BIN" -n "$@"
}

restart_configured_services() {
  local services
  services="$(run_root "$SUPERVISORCTL_BIN" status | awk '$1 ~ /^frappe-bench-(web|workers):/ {print $1}')"
  if [[ -z "$services" ]]; then
    echo "No configured ERP web/worker services were reported by Supervisor; skipping service restart."
    return 0
  fi
  mapfile -t service_names <<<"$services"
  run_root "$SUPERVISORCTL_BIN" restart "${service_names[@]}"
}

current_upstream_commit() {
  python3 - "$APP_ROOT/current/release-manifest.json" "$1" <<'PY'
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
app = sys.argv[2]
print(((manifest.get("installed_apps") or {}).get(app) or {}).get("upstream_commit") or "")
PY
}

[[ -s "$BACKUP_EVIDENCE_FILE" ]] || { echo "verified production backup evidence is required" >&2; exit 1; }
backup_dir="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["local_backup_dir"])' "$BACKUP_EVIDENCE_FILE")"
run_root test -d "$backup_dir/erp"
run_root test -s "$backup_dir/manifest.sha256"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
run_root bash "$SCRIPT_DIR/verify_backup_manifest.sh" "$backup_dir" >/dev/null

rollback_site() {
  echo "Phase 02 ERP mutation failed; restoring the verified pre-mutation ERP backup" >&2
  database="$(run_root find "$backup_dir/erp" -maxdepth 1 -type f -name '*-database.sql.gz' -print -quit)"
  public_files="$(run_root find "$backup_dir/erp" -maxdepth 1 -type f -name '*-files.tar' -not -name '*private-files.tar' -print -quit)"
  private_files="$(run_root find "$backup_dir/erp" -maxdepth 1 -type f -name '*-private-files.tar' -print -quit)"
  [[ -n "$database" && -n "$public_files" && -n "$private_files" ]] || return 1
  restore_root="$(run_root mktemp -d /tmp/phase2-hrms-restore.XXXXXX)"
  run_root cp "$database" "$restore_root/database.sql.gz"
  run_root cp "$public_files" "$restore_root/files.tar"
  run_root cp "$private_files" "$restore_root/private-files.tar"
  run_root chown -R frappe:frappe "$restore_root"
  run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' restore '$restore_root/database.sql.gz' --force --with-public-files '$restore_root/files.tar' --with-private-files '$restore_root/private-files.tar'"
  run_root rm -rf "$restore_root"
  if [[ "$LENERP_WAS_PRESENT" -eq 1 ]]; then
    run_root rm -rf "$LENERP_DIR"
    run_root cp -a "$ROLLBACK_ROOT/lenerp_core" "$LENERP_DIR"
  else
    run_root rm -rf "$LENERP_DIR"
  fi
  if [[ -f "$ROLLBACK_ROOT/apps.txt" ]]; then
    run_root cp "$ROLLBACK_ROOT/apps.txt" "$BENCH_DIR/sites/apps.txt"
  fi
  restart_configured_services
}
trap 'status=$?; if [[ "$status" -ne 0 && "$MUTATION_STARTED" -eq 1 ]]; then rollback_site || echo "CRITICAL: ERP backup restore failed" >&2; fi; exit "$status"' EXIT

run_root test -f "$LENERP_SOURCE_DIR/SOURCE_COMMIT.txt" || { echo "candidate lenerp_core source marker is absent" >&2; exit 1; }
test "$(tr -d '\r\n' < "$LENERP_SOURCE_DIR/SOURCE_COMMIT.txt")" = "$LENERP_COMMIT" || { echo "candidate lenerp_core source marker is not the approved pin" >&2; exit 1; }

apps="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
installed_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
if [[ -n "$installed_version" && "$installed_version" != "15.64.1" ]]; then
  echo "Installed HRMS version '$installed_version' is not the approved 15.64.1; no mutation was attempted." >&2
  exit 1
fi
grep -Eq "^frappe[[:space:]]+$FRAPPE_VERSION([[:space:]]|$)" <<<"$apps" || { echo "Frappe version is not the approved pin; no mutation was attempted." >&2; exit 1; }
grep -Eq "^erpnext[[:space:]]+$ERPNEXT_VERSION([[:space:]]|$)" <<<"$apps" || { echo "ERPNext version is not the approved pin; no mutation was attempted." >&2; exit 1; }
for app in frappe erpnext; do
  run_root test -d "$BENCH_DIR/apps/$app/.git" || { echo "$app source checkout is absent; no mutation was attempted." >&2; exit 1; }
done
run_root test -d "$HRMS_DIR/.git" || { echo "HRMS source checkout is absent or not a Git checkout; no mutation was attempted." >&2; exit 1; }
for app in frappe erpnext; do
  expected_commit="$FRAPPE_COMMIT"
  [[ "$app" == "erpnext" ]] && expected_commit="$ERPNEXT_COMMIT"
  actual_commit="$(run_as_frappe "git -c safe.directory='$BENCH_DIR/apps/$app' -C '$BENCH_DIR/apps/$app' rev-parse HEAD")"
  if [[ "$actual_commit" != "$expected_commit" ]]; then
    [[ "$(current_upstream_commit "$app")" == "$expected_commit" ]] || { echo "$app source commit is not the approved pin; no mutation was attempted." >&2; exit 1; }
  fi
done
test "$(run_as_frappe "git -c safe.directory='$HRMS_DIR' -C '$HRMS_DIR' rev-parse HEAD")" = "$HRMS_COMMIT" || { echo "HRMS source commit is not the approved pin; no mutation was attempted." >&2; exit 1; }

if run_root test -e "$LENERP_DIR"; then
  LENERP_WAS_PRESENT=1
  run_root cp -a "$LENERP_DIR" "$ROLLBACK_ROOT/lenerp_core"
fi
run_root cp "$BENCH_DIR/sites/apps.txt" "$ROLLBACK_ROOT/apps.txt"

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
apps="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"

if [[ "$LENERP_WAS_PRESENT" -eq 0 ]] || ! grep -Eq "^lenerp_core[[:space:]]+$LENERP_VERSION([[:space:]]|$)" <<<"$apps" || [[ "$(run_as_frappe "tr -d '\r\n' < '$LENERP_DIR/SOURCE_COMMIT.txt'")" != "$LENERP_COMMIT" ]]; then
  echo "Provisioning exact lenerp_core source through the reviewed candidate release."
  MUTATION_STARTED=1
  run_root rsync -a --delete --exclude='.git' "$LENERP_SOURCE_DIR/" "$LENERP_DIR/"
  run_root chown -R frappe:frappe "$LENERP_DIR"
  run_as_frappe "cd '$BENCH_DIR' && uv pip install --quiet --python '$BENCH_DIR/env/bin/python' --no-deps -e '$LENERP_DIR'"
  run_root python3 - "$BENCH_DIR/sites/apps.txt" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
if "lenerp_core" not in lines:
    lines.append("lenerp_core")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
  apps="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
  if ! grep -Eq '^lenerp_core[[:space:]]' <<<"$apps"; then
    run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' install-app lenerp_core"
  fi
  run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' migrate"
  run_as_frappe "cd '$BENCH_DIR' && bench build --app lenerp_core"
fi

run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' migrate"
run_as_frappe "cd '$BENCH_DIR' && bench build --app hrms"
restart_configured_services

apps="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' list-apps")"
grep -Eq '^hrms[[:space:]]' <<<"$apps"
installed_version="$(awk '$1 == "hrms" {print $2; exit}' <<<"$apps")"
[[ "$installed_version" == "15.64.1" ]]
grep -Eq "^lenerp_core[[:space:]]+$LENERP_VERSION([[:space:]]|$)" <<<"$apps"
[[ "$(run_as_frappe "tr -d '\r\n' < '$LENERP_DIR/SOURCE_COMMIT.txt'")" == "$LENERP_COMMIT" ]]
role_count="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --kwargs '{\"doctype\":\"Role\",\"filters\":{\"name\":[\"in\",[\"HR User\",\"HR Manager\",\"Champion Administrator\",\"Champion Dispatcher\",\"Champion Sales User\",\"Champion Accounting User\",\"Champion Inventory Manager\",\"Champion Field Technician\",\"Champion Platform Operator\"]]}}'" | tr -d '\r\n ' )"
[[ "$role_count" == "9" ]]
workspace_count="$(run_as_frappe "cd '$BENCH_DIR' && bench --site '$SITE' execute frappe.client.get_count --kwargs '{\"doctype\":\"Workspace\",\"filters\":{\"name\":[\"in\",[\"HR\",\"Payroll\",\"Champion ERP\"]]}}'" | tr -d '\r\n ' )"
[[ "$workspace_count" == "3" ]]

python3 - "$OUTPUT_FILE" "$HRMS_COMMIT" "$installed_version" "$role_count" "$workspace_count" "$LENERP_COMMIT" "$LENERP_VERSION" <<'PY'
import json
import sys
from datetime import datetime, timezone

output, commit, version, roles, workspaces, lenerp_commit, lenerp_version = sys.argv[1:]
payload = {
    "status": "passed",
    "site": "erp.lengrowth.com",
    "hrms_version": version,
    "hrms_commit": commit,
    "lenerp_core_version": lenerp_version,
    "lenerp_core_commit": lenerp_commit,
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
run_root rm -rf "$ROLLBACK_ROOT"
echo "Production Phase 02 HRMS install, migration, and readback passed"
