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
    "build_time_utc",
    "custom_app_version",
    "custom_app_commit",
    "upstream_frappe_commit",
    "upstream_erpnext_commit",
    "installed_apps",
    "dependency_lock_hashes",
    "feature_flags",
}
missing = sorted(required - payload.keys())
if missing:
    raise SystemExit(f"manifest missing required fields: {', '.join(missing)}")
if not payload["release_id"] or not payload["control_plane_commit"]:
    raise SystemExit("manifest release identity is empty")
if not isinstance(payload["installed_apps"], dict):
    raise SystemExit("manifest installed_apps must be an object")
for app_name in ("frappe", "erpnext"):
    if not isinstance(payload["installed_apps"].get(app_name), dict):
        raise SystemExit(f"manifest installed_apps is missing {app_name}")
if payload.get("custom_app_version") not in {None, "not-installed"}:
    candidate = path.parent / "custom-app"
    if not candidate.is_dir():
        raise SystemExit("manifest declares a custom app but candidate artifact is missing")
PY

printf 'Preflight passed for candidate %s\n' "$CANDIDATE_DIR"
