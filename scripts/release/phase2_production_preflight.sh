#!/usr/bin/env bash
set -Eeuo pipefail

CANDIDATE_DIR="${1:?Usage: phase2_production_preflight.sh <candidate-dir>}"
BACKUP_EVIDENCE_FILE="${BACKUP_EVIDENCE_FILE:?Set BACKUP_EVIDENCE_FILE}"
ERP_BENCH_DIR="${ERP_BENCH_DIR:-/home/frappe/frappe-bench}"
ERP_SITE="${ERP_SITE:-erp.lengrowth.com}"
TARGET_ENVIRONMENT="${TARGET_ENVIRONMENT:-production}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
MANIFEST="$CANDIDATE_DIR/release-manifest.json"

[[ "$TARGET_ENVIRONMENT" == "production" ]] || { echo "production preflight requires TARGET_ENVIRONMENT=production" >&2; exit 1; }
[[ "$ERP_SITE" == "erp.lengrowth.com" ]] || { echo "unexpected production ERP site" >&2; exit 1; }
[[ -s "$MANIFEST" ]] || { echo "candidate manifest is missing" >&2; exit 1; }
[[ -s "$BACKUP_EVIDENCE_FILE" ]] || { echo "verified production backup evidence is missing" >&2; exit 1; }
grep -q '"status": "passed"' "$BACKUP_EVIDENCE_FILE" || { echo "production backup evidence is not passed" >&2; exit 1; }

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
backup_dir="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["local_backup_dir"])' "$BACKUP_EVIDENCE_FILE")"
sudo -n bash "$SCRIPT_DIR/verify_backup_manifest.sh" "$backup_dir" >/dev/null

python3 - "$MANIFEST" "$APP_ROOT/current/release-manifest.json" <<'PY'
import json
import os
import sys

candidate = json.load(open(sys.argv[1], encoding="utf-8"))
current = json.load(open(sys.argv[2], encoding="utf-8"))
if candidate.get("environment") != "staging" or candidate.get("build_environment") != "staging":
    raise SystemExit("production may promote only a staging-built candidate")
candidate_before = candidate.get("database_revision_before")
candidate_after = candidate.get("database_revision_after")
current_after = current.get("database_revision_after")
if candidate_before != current_after:
    if os.environ.get("PHASE3_MIGRATION_APPROVED", "no") != "yes":
        raise SystemExit("production database revision does not match candidate preflight expectation; explicit additive migration approval is required")
    if current_after != "20260918_0011" or candidate_before != "20260921_0014" or candidate_after != "20260921_0014":
        raise SystemExit("unreviewed production database revision transition")
apps = candidate.get("installed_apps") or {}
for name in ("frappe", "erpnext", "lenerp_core"):
    app_payload = apps.get(name) or {}
    # Older staging slots can carry the ERP identity in the checked-in
    # dependency baseline even when their generated installed_apps map is
    # incomplete. Accept that exact, candidate-bound fallback only when the
    # top-level custom-app identity agrees with it.
    if name == "lenerp_core" and (
        not isinstance(app_payload.get("commit"), str) or len(app_payload.get("commit", "")) != 40
    ):
        baseline = ((candidate.get("application_dependencies") or {}).get("baseline") or {}).get(name) or {}
        if (
            isinstance(baseline.get("commit"), str)
            and len(baseline["commit"]) == 40
            and baseline.get("version") == candidate.get("custom_app_version")
            and baseline.get("commit") == candidate.get("custom_app_commit")
        ):
            app_payload = baseline
    commit = app_payload.get("commit")
    if not isinstance(commit, str) or len(commit) != 40:
        raise SystemExit(f"candidate is missing exact {name} commit")
if (candidate.get("custom_app_version") or "") == "not-installed":
    raise SystemExit("candidate is missing the required LenERP application version")
PY

capture_as_frappe() {
  sudo -n -u frappe bash -lc "$1"
}

apps="$(capture_as_frappe "cd '$ERP_BENCH_DIR' && bench --site '$ERP_SITE' list-apps")"
grep -Eq '^frappe[[:space:]]+15\.119\.1([[:space:]]|$)' <<<"$apps" || { echo "production Frappe version baseline mismatch" >&2; exit 1; }
grep -Eq '^erpnext[[:space:]]+15\.120\.0([[:space:]]|$)' <<<"$apps" || { echo "production ERPNext version baseline mismatch" >&2; exit 1; }

declare -A expected_commits
expected_commits[frappe]="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["installed_apps"]["frappe"]["commit"])' "$MANIFEST")"
expected_commits[erpnext]="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["installed_apps"]["erpnext"]["commit"])' "$MANIFEST")"
expected_commits[lenerp_core]="$(python3 - "$MANIFEST" <<'PY'
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
installed = (manifest.get("installed_apps") or {}).get("lenerp_core") or {}
commit = installed.get("commit")
if not isinstance(commit, str) or len(commit) != 40:
    commit = (((manifest.get("application_dependencies") or {}).get("baseline") or {}).get("lenerp_core") or {}).get("commit")
print(commit or "")
PY
)"
for app in frappe erpnext lenerp_core; do
  app_path="$ERP_BENCH_DIR/apps/$app"
  if [[ "$app" == "lenerp_core" ]]; then
    sudo -n test -f "$app_path/SOURCE_COMMIT.txt" || { echo "exact production $app source marker is missing" >&2; exit 1; }
    commit="$(capture_as_frappe "tr -d '\\r\\n' < '$app_path/SOURCE_COMMIT.txt'")"
  else
    sudo -n test -d "$app_path/.git" || { echo "exact production $app commit is not readable from a Git checkout" >&2; exit 1; }
    commit="$(capture_as_frappe "git -C '$app_path' rev-parse HEAD")"
  fi
  [[ "$commit" =~ ^[0-9a-f]{40}$ ]] || { echo "production $app commit readback is invalid" >&2; exit 1; }
  [[ "$commit" == "${expected_commits[$app]}" ]] || { echo "production $app commit does not match the candidate" >&2; exit 1; }
done

expected_lenerp_version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["custom_app_version"])' "$MANIFEST")"
actual_lenerp_version="$(awk '$1 == "lenerp_core" {print $2; exit}' <<<"$apps")"
[[ "$actual_lenerp_version" == "$expected_lenerp_version" ]] || { echo "production LenERP version does not match the candidate" >&2; exit 1; }

echo "Phase 02 production preflight passed without application or pointer mutation"
