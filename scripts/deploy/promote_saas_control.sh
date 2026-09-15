#!/usr/bin/env bash
set -euo pipefail

if [[ "${PRODUCTION_PROMOTION_APPROVED:-}" != "yes" ]]; then
  echo "Set PRODUCTION_PROMOTION_APPROVED=yes only from the separately approved promotion workflow." >&2
  exit 1
fi
if [[ "${PRODUCTION_BACKUP_VERIFIED:-}" != "yes" || "${OFFHOST_BACKUP_VERIFIED:-}" != "yes" ]]; then
  echo "Production promotion requires verified application/site backups and an off-host copy." >&2
  exit 1
fi
RELEASE_ID="${RELEASE_ID:?Set RELEASE_ID to an existing tested staging candidate}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
RELEASE_ROOT="${RELEASE_ROOT:-$APP_ROOT/releases}"
CURRENT_LINK="${CURRENT_LINK:-$APP_ROOT/current}"
PREVIOUS_LINK="${PREVIOUS_LINK:-$APP_ROOT/previous}"
SYSTEMCTL_BIN="${SYSTEMCTL_BIN:-/usr/bin/systemctl}"
NGINX_BIN="${NGINX_BIN:-/usr/sbin/nginx}"
LOCK_FILE="${LOCK_FILE:-/tmp/saas-control-production-promote.lock}"
CANDIDATE_DIR="$RELEASE_ROOT/$RELEASE_ID"

atomic_link() {
  local target="$1" link="$2" tmp="${link}.next.$$"
  ln -s "$target" "$tmp"
  mv -Tf "$tmp" "$link"
}
restart_services() {
  sudo "$SYSTEMCTL_BIN" restart "${BACKEND_SERVICE:-saas-backend}" "${FRONTEND_SERVICE:-saas-frontend}"
}
validate_nginx() {
  sudo "$NGINX_BIN" -t
  sudo "$SYSTEMCTL_BIN" reload nginx
}

[[ -f "$CANDIDATE_DIR/.candidate-complete" ]] || { echo "Candidate is not built: $CANDIDATE_DIR" >&2; exit 1; }
[[ -s "$CANDIDATE_DIR/.staging-smoke-passed" ]] || {
  echo "Candidate has no recorded successful staging smoke: $CANDIDATE_DIR" >&2
  exit 1
}
grep -Fxq "$RELEASE_ID" "$CANDIDATE_DIR/.staging-smoke-passed" || {
  echo "Candidate staging smoke marker does not match RELEASE_ID" >&2
  exit 1
}
bash "$CANDIDATE_DIR/scripts/release/preflight.sh" "$CANDIDATE_DIR"
python3 - "$CANDIDATE_DIR/release-manifest.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    manifest = json.load(handle)
if manifest.get("environment") != "staging":
    raise SystemExit("production can promote only a candidate previously built for staging")
PY

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "Another production promotion is already running." >&2; exit 1; }

OLD_TARGET="$(readlink -f "$CURRENT_LINK" 2>/dev/null || true)"
OLD_PREVIOUS="$(readlink -f "$PREVIOUS_LINK" 2>/dev/null || true)"
atomic_link "$CANDIDATE_DIR" "$CURRENT_LINK"
restart_services
validate_nginx

if ! BASE_URL="${PRODUCTION_BASE_URL:?Set PRODUCTION_BASE_URL}" \
  BACKEND_URL="${PRODUCTION_BACKEND_URL:?Set PRODUCTION_BACKEND_URL}" \
  EXPECTED_RELEASE="$RELEASE_ID" bash "$CANDIDATE_DIR/scripts/release/smoke.sh"; then
  if [[ -n "$OLD_TARGET" ]]; then
    atomic_link "$OLD_TARGET" "$CURRENT_LINK"
  else
    rm -f "$CURRENT_LINK"
  fi
  if [[ -n "$OLD_PREVIOUS" ]]; then
    atomic_link "$OLD_PREVIOUS" "$PREVIOUS_LINK"
  else
    rm -f "$PREVIOUS_LINK"
  fi
  restart_services
  validate_nginx
  echo "Production smoke failed; previous release restored." >&2
  exit 1
fi

if [[ -n "$OLD_TARGET" && "$OLD_TARGET" != "$CANDIDATE_DIR" ]]; then
  atomic_link "$OLD_TARGET" "$PREVIOUS_LINK"
fi

printf 'Production promotion completed for %s\n' "$RELEASE_ID"
