#!/usr/bin/env bash
set -Eeuo pipefail

OUTPUT_FILE="${1:?Usage: run_verified_production_backup.sh <output-file>}"
SERVICE="saas-control-r2-backup.service"
START_EPOCH="$(date +%s)"
sudo -n systemctl start "$SERVICE"
log="$(sudo -n journalctl -u "$SERVICE" --since "@${START_EPOCH}" --no-pager -o cat)"
prefix="$(printf '%s\n' "$log" | sed -n 's/^R2 backup and byte-hash verification passed: //p' | tail -n 1)"
[[ "$prefix" =~ ^automated/production/[0-9]{8}T[0-9]{6}Z$ ]] || {
  echo "no fresh verified production R2 backup was recorded" >&2
  exit 1
}
run_id="${prefix##*/}"
local_dir="/var/lib/saas-control/r2-backups/$run_id"
sudo -n test -d "$local_dir/erp"
sudo -n test -s "$local_dir/manifest.sha256"
sudo -n bash -lc "cd '$local_dir' && sha256sum -c manifest.sha256" >/dev/null

python3 - "$OUTPUT_FILE" "$prefix" "$run_id" "$local_dir" <<'PY'
import json
import sys
from datetime import datetime, timezone

output, prefix, run_id, local_dir = sys.argv[1:]
payload = {
    "status": "passed",
    "service": "saas-control-r2-backup.service",
    "verified_at_utc": datetime.now(timezone.utc).isoformat(),
    "r2_prefix": prefix,
    "run_id": run_id,
    "local_backup_dir": local_dir,
    "sha256_manifest_verified": True,
}
with open(output, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
chmod 600 "$OUTPUT_FILE"
echo "Verified fresh production backup: $prefix"
