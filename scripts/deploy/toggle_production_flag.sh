#!/usr/bin/env bash
set -Eeuo pipefail

EXPECTED_CURRENT_RELEASE="${EXPECTED_CURRENT_RELEASE:?Set EXPECTED_CURRENT_RELEASE to the release already serving production}"
PHASE1_SHELL_STATE="${PHASE1_SHELL_STATE:?Set PHASE1_SHELL_STATE to on or off}"
AUTH_TOKEN_FILE="${AUTH_TOKEN_FILE:?Set AUTH_TOKEN_FILE to the temporary smoke token path}"
BASE_URL="${BASE_URL:?Set BASE_URL to the production application origin}"
BACKEND_URL="${BACKEND_URL:?Set BACKEND_URL to the production backend origin}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
BACKEND_ENV_FILE="${BACKEND_ENV_FILE:-$APP_ROOT/shared/env/backend.env}"
CURRENT_LINK="${CURRENT_LINK:-$APP_ROOT/current}"
BACKEND_SERVICE="${BACKEND_SERVICE:-saas-backend}"
SYSTEMCTL_BIN="${SYSTEMCTL_BIN:-/usr/bin/systemctl}"
LOCK_FILE="${LOCK_FILE:-/tmp/saas-control-production-flag.lock}"

case "$PHASE1_SHELL_STATE" in on|off) ;; *) echo "Invalid Phase 1 shell state" >&2; exit 1 ;; esac
[[ -r "$BACKEND_ENV_FILE" ]] || { echo "Production backend environment is missing" >&2; exit 1; }
actual_release="$(readlink -f "$CURRENT_LINK")"
[[ "$actual_release" == "$APP_ROOT/releases/$EXPECTED_CURRENT_RELEASE" ]] || {
  echo "Production release pointer changed; refusing flag-only update" >&2
  exit 1
}

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "Another production flag transition is running." >&2; exit 1; }

backup_file="/tmp/saas-control-production-flag.$$.env"
sudo cp -p "$BACKEND_ENV_FILE" "$backup_file"
restore() {
  sudo cp -p "$backup_file" "$BACKEND_ENV_FILE" 2>/dev/null || true
  sudo "$SYSTEMCTL_BIN" restart "$BACKEND_SERVICE" >/dev/null 2>&1 || true
  sudo rm -f -- "$backup_file"
}
cleanup() { sudo rm -f -- "$backup_file"; }
trap cleanup EXIT

sudo python3 - "$BACKEND_ENV_FILE" "$PHASE1_SHELL_STATE" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
state = sys.argv[2]
lines = path.read_text(encoding="utf-8").splitlines()
output = []
updated = False
feature_flags_pattern = re.compile(r"^\s*(?:export\s+)?FEATURE_FLAGS=")
for line in lines:
    if feature_flags_pattern.match(line):
        if updated:
            continue
        entries = [entry for entry in line.split("=", 1)[1].split(",") if entry and not entry.startswith("platform_phase1_shell=")]
        entries.append(f"platform_phase1_shell={state}")
        line = "FEATURE_FLAGS=" + ",".join(entries)
        updated = True
    output.append(line)
if not updated:
    output.append(f"FEATURE_FLAGS=platform_phase1_shell={state}")
path.write_text("\n".join(output) + "\n", encoding="utf-8")
PY

sudo "$SYSTEMCTL_BIN" restart "$BACKEND_SERVICE"
ready=false
for _ in {1..30}; do
  if curl -fsS -o /dev/null --max-time 3 "${PRODUCTION_BACKEND_LOCAL_URL:-http://127.0.0.1:8001}/health"; then ready=true; break; fi
  sleep 2
done
if [[ "$ready" != true ]]; then restore; exit 1; fi

if ! AUTH_TOKEN_FILE="$AUTH_TOKEN_FILE" BASE_URL="$BASE_URL" BACKEND_URL="$BACKEND_URL" EXPECTED_RELEASE="$EXPECTED_CURRENT_RELEASE" EXPECTED_PHASE_ONE_SHELL="$PHASE1_SHELL_STATE" bash "$APP_ROOT/current/scripts/release/shell_smoke.sh"; then
  restore
  exit 1
fi

[[ "$(readlink -f "$CURRENT_LINK")" == "$APP_ROOT/releases/$EXPECTED_CURRENT_RELEASE" ]] || { restore; exit 1; }
echo "Production flag-only transition completed for $EXPECTED_CURRENT_RELEASE: $PHASE1_SHELL_STATE"
