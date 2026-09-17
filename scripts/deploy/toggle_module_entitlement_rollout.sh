#!/usr/bin/env bash
set -euo pipefail

ROLLOUT_STAGE="${MODULE_ROLLOUT_STAGE:?Set MODULE_ROLLOUT_STAGE to read-only, operator-only, or general}"
EXPECTED_CURRENT_RELEASE="${EXPECTED_CURRENT_RELEASE:?Set EXPECTED_CURRENT_RELEASE to the immutable production candidate}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
ENV_FILE="${ENV_FILE:-$APP_ROOT/shared/env/backend.env}"
CURRENT_LINK="${CURRENT_LINK:-$APP_ROOT/current}"

case "$ROLLOUT_STAGE" in
  read-only) writes=off; operator=off; general=off ;;
  operator-only) writes=on; operator=on; general=off ;;
  general) writes=on; operator=off; general=on ;;
  *) echo "Invalid module entitlement rollout stage" >&2; exit 1 ;;
esac

current_release="$(readlink -f "$CURRENT_LINK" | xargs -r basename)"
[[ "$current_release" == "$EXPECTED_CURRENT_RELEASE" ]] || {
  echo "Refusing module rollout for unexpected current release" >&2
  exit 1
}
[[ -f "$CURRENT_LINK/release-manifest.json" ]] || { echo "Current release manifest is missing" >&2; exit 1; }

sudo python3 - "$ENV_FILE" "$writes" "$operator" "$general" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
values = sys.argv[2:]
lines = path.read_text(encoding="utf-8").splitlines()
output = []
updated = False
for line in lines:
    if line.startswith("FEATURE_FLAGS="):
        entries = [entry for entry in line.removeprefix("FEATURE_FLAGS=").split(",") if entry and not entry.split("=", 1)[0].strip().startswith("module_entitlement_")]
        entries.extend([
            f"module_entitlement_writes={values[0]}",
            f"module_entitlement_operator_only={values[1]}",
            f"module_entitlement_general={values[2]}",
        ])
        line = "FEATURE_FLAGS=" + ",".join(entries)
        updated = True
    output.append(line)
if not updated:
    output.append("FEATURE_FLAGS=" + ",".join([
        f"module_entitlement_writes={values[0]}",
        f"module_entitlement_operator_only={values[1]}",
        f"module_entitlement_general={values[2]}",
    ]))
path.write_text("\n".join(output) + "\n", encoding="utf-8")
PY

sudo systemctl restart "${BACKEND_SERVICE:-saas-backend}"
ready=false
for _ in {1..30}; do
  if curl -fsS -o /dev/null --max-time 3 "${PRODUCTION_BACKEND_LOCAL_URL:-http://127.0.0.1:8001}/health"; then
    ready=true
    break
  fi
  sleep 2
done
if [[ "$ready" != true ]]; then
  echo "Production backend did not become ready after the rollout restart." >&2
  exit 1
fi
echo "Module entitlement rollout set to $ROLLOUT_STAGE for $EXPECTED_CURRENT_RELEASE"
