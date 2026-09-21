#!/usr/bin/env bash
set -euo pipefail

CANDIDATE_DIR="${1:?Usage: preflight.sh <candidate-dir>}"
MANIFEST="$CANDIDATE_DIR/release-manifest.json"

[[ -d "$CANDIDATE_DIR/backend" ]] || { echo "candidate backend is missing" >&2; exit 1; }
[[ -d "$CANDIDATE_DIR/frontend/.next" ]] || { echo "candidate frontend build is missing" >&2; exit 1; }
[[ -s "$MANIFEST" ]] || { echo "candidate release manifest is missing" >&2; exit 1; }

python3 - "$MANIFEST" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
required = {
    "release_id",
    "control_plane_commit",
    "environment",
    "build_environment",
    "build_time_utc",
    "custom_app_version",
    "custom_app_commit",
    "upstream_frappe_commit",
    "upstream_erpnext_commit",
    "installed_apps",
    "dependency_lock_hashes",
    "feature_flags",
    "application_dependencies",
    "application_records",
    "database_revision_before",
    "database_revision_after",
}
missing = sorted(required - payload.keys())
if missing:
    raise SystemExit(f"manifest missing required fields: {', '.join(missing)}")
if not payload["release_id"] or not payload["control_plane_commit"]:
    raise SystemExit("manifest release identity is empty")
if payload.get("build_environment") != payload.get("environment"):
    raise SystemExit("manifest build_environment must match artifact environment")
if not isinstance(payload["installed_apps"], dict):
    raise SystemExit("manifest installed_apps must be an object")
for app_name in ("frappe", "erpnext"):
    if not isinstance(payload["installed_apps"].get(app_name), dict):
        raise SystemExit(f"manifest installed_apps is missing {app_name}")
    app = payload["installed_apps"][app_name]
    if app.get("commit") in {None, "", "unknown"}:
        raise SystemExit(f"manifest installed_apps has unknown {app_name} commit")
dependencies = payload.get("application_dependencies")
if not isinstance(dependencies, dict) or dependencies.get("schema_version") != 1:
    raise SystemExit("manifest application dependency pin is missing")
hrms = dependencies.get("module_dependencies", {}).get("hrms", {})
if hrms.get("commit") != "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1" or hrms.get("version") != "15.64.1":
    raise SystemExit("manifest HRMS pin is not the reviewed immutable revision")
compatibility = hrms.get("compatibility") or {}
if compatibility.get("metadata_sufficiency") != "broad major-version constraints are not sufficient to prove install compatibility":
    raise SystemExit("manifest does not record the HRMS compatibility limitation")
if compatibility.get("upstream_issue") != "https://github.com/frappe/hrms/issues/1639":
    raise SystemExit("manifest does not bind the authoritative HRMS install evidence")
if compatibility.get("status") != "verified":
    raise SystemExit("candidate is blocked: HRMS has no clean-install compatibility evidence for the declared baseline")
records = payload.get("application_records")
hrms_record = records.get("hrms") if isinstance(records, dict) else None
if not isinstance(hrms_record, dict):
    raise SystemExit("manifest does not record HRMS as a required runtime application")
if hrms_record.get("intended_version") != "15.64.1" or hrms_record.get("intended_commit") != "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1":
    raise SystemExit("manifest HRMS application identity is incomplete")
if hrms_record.get("verification_status") == "verified" and hrms_record.get("compatibility_status") != "verified":
    raise SystemExit("manifest cannot mark unverified HRMS as runtime verified")
for field in (
    "custom_app_commit",
    "custom_app_version",
    "upstream_frappe_commit",
    "upstream_erpnext_commit",
    "database_revision_before",
    "database_revision_after",
):
    if payload.get(field) in {None, "", "unknown", "not-installed"}:
        raise SystemExit(f"manifest has incomplete runtime field: {field}")
baseline_ref = payload.get("runtime_baseline")
if not isinstance(baseline_ref, str) or not baseline_ref:
    raise SystemExit("candidate runtime baseline reference is missing")
baseline_path = path.parent / baseline_ref
if not baseline_path.is_file():
    raise SystemExit("candidate runtime baseline is missing")
baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
if baseline.get("schema_version") != 1:
    raise SystemExit("candidate runtime baseline has an unsupported schema")
runtime_apps = baseline.get("runtime_apps", {})
expected = {
    "upstream_frappe_commit": baseline.get("upstream_frappe_commit"),
    "upstream_erpnext_commit": baseline.get("upstream_erpnext_commit"),
    "database_revision_before": baseline.get("database_revision"),
    "database_revision_after": baseline.get("database_revision"),
    "custom_app_commit": runtime_apps.get("lenerp_core", {}).get("commit"),
    "custom_app_version": runtime_apps.get("lenerp_core", {}).get("version"),
}
for field, value in expected.items():
    if payload.get(field) != value:
        raise SystemExit(f"manifest {field} does not match the checked-in runtime baseline")
for app_name in ("frappe", "erpnext"):
    expected_commit = runtime_apps.get(app_name, {}).get("commit")
    actual_commit = payload["installed_apps"][app_name].get("commit")
    if actual_commit != expected_commit:
        raise SystemExit(f"manifest installed_apps {app_name} does not match the runtime baseline")
# The ERP app inventory is a non-secret runtime baseline for the co-hosted
# Frappe/ERPNext service. It is not required to be packaged into the
# control-plane candidate; when CUSTOM_APP_REPO is supplied, build_candidate.sh
# may additionally include a custom-app artifact.
PY

printf 'Preflight passed for candidate %s\n' "$CANDIDATE_DIR"
