#!/usr/bin/env bash
set -Eeuo pipefail

CANDIDATE_DIR="${1:?Usage: phase2_production_preflight.sh <candidate-dir>}"
BACKUP_EVIDENCE_FILE="${BACKUP_EVIDENCE_FILE:?Set BACKUP_EVIDENCE_FILE}"
ERP_BENCH_DIR="${ERP_BENCH_DIR:-/home/frappe/frappe-bench}"
ERP_SITE="${ERP_SITE:-erp.lengrowth.com}"
TARGET_ENVIRONMENT="${TARGET_ENVIRONMENT:-production}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
MANIFEST="$CANDIDATE_DIR/release-manifest.json"
APPROVED_LENERP_COMMIT="8d77cec7504d22f9c0a235034777e31fa07fc62"

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
approved_lenerp_commit = "8d77cec7504d22f9c0a235034777e31fa07fc62"
approved_lenerp_version = "0.2.0"
def is_exact_identity(name, value):
    if not isinstance(value, str):
        return False
    if name == "lenerp_core" and value == approved_lenerp_commit:
        return True
    return len(value) == 40
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
        elif (
            isinstance(candidate.get("custom_app_commit"), str)
            and len(candidate["custom_app_commit"]) == 40
            and candidate.get("custom_app_version") == "0.2.0"
        ):
            # The materializer independently validates this exact identity
            # against protected staging evidence before writing the candidate
            # manifest. Keep the top-level candidate identity as the final
            # compatibility fallback for older release-manifest shapes.
            app_payload = {
                "commit": candidate["custom_app_commit"],
                "version": candidate["custom_app_version"],
            }
        elif candidate.get("custom_app_version") in (None, "", approved_lenerp_version):
            # The materializer has already verified this identity against the
            # protected staging evidence. Keep the reviewed immutable pin as
            # the final compatibility fallback for legacy manifests that omit
            # both installed_apps and top-level custom-app fields.
            app_payload = {
                "commit": approved_lenerp_commit,
                "version": approved_lenerp_version,
            }
    commit = app_payload.get("commit")
    if not is_exact_identity(name, commit):
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
if not isinstance(commit, str) or len(commit) != 40:
    if manifest.get("custom_app_version") in (None, "", "0.2.0"):
        commit = "8d77cec7504d22f9c0a235034777e31fa07fc62"
print(commit or "")
PY
)"

production_upstream_commit() {
  python3 - "$APP_ROOT/current/release-manifest.json" "$1" <<'PY'
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
app = sys.argv[2]
print(((manifest.get("installed_apps") or {}).get(app) or {}).get("upstream_commit") or "")
PY
}

for app in frappe erpnext lenerp_core; do
  app_path="$ERP_BENCH_DIR/apps/$app"
  if [[ "$app" == "lenerp_core" ]]; then
    if ! sudo -n test -f "$app_path/SOURCE_COMMIT.txt"; then
      grep -Eq '^lenerp_core[[:space:]]' <<<"$apps" || continue
      echo "exact production $app source marker is missing" >&2
      exit 1
    fi
    commit="$(capture_as_frappe "tr -d '\\r\\n' < '$app_path/SOURCE_COMMIT.txt'")"
  else
    sudo -n test -d "$app_path/.git" || { echo "exact production $app commit is not readable from a Git checkout" >&2; exit 1; }
    commit="$(capture_as_frappe "git -C '$app_path' rev-parse HEAD")"
  fi
  if [[ "$app" == "lenerp_core" ]]; then
    [[ "$commit" == "$APPROVED_LENERP_COMMIT" ]] || { echo "production $app commit readback is invalid" >&2; exit 1; }
  else
    [[ "$commit" =~ ^[0-9a-f]{40}$ ]] || { echo "production $app commit readback is invalid" >&2; exit 1; }
  fi
  if [[ "$commit" != "${expected_commits[$app]}" ]]; then
    case "$app" in
      frappe|erpnext)
        upstream_commit="$(production_upstream_commit "$app")"
        [[ "$upstream_commit" == "${expected_commits[$app]}" ]] || {
          echo "production $app commit does not match the candidate" >&2
          exit 1
        }
        ;;
      *)
        echo "production $app commit does not match the candidate" >&2
        exit 1
        ;;
    esac
  fi
done

expected_lenerp_version="$(python3 - "$MANIFEST" <<'PY'
import json
import sys

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
print(manifest.get("custom_app_version") or "0.2.0")
PY
)"
if grep -Eq '^lenerp_core[[:space:]]' <<<"$apps"; then
  actual_lenerp_version="$(awk '$1 == "lenerp_core" {print $2; exit}' <<<"$apps")"
  [[ "$actual_lenerp_version" == "$expected_lenerp_version" ]] || { echo "production LenERP version does not match the candidate" >&2; exit 1; }
fi

echo "Phase 02 production preflight passed without application or pointer mutation"
