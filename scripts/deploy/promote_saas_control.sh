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
AUTH_TOKEN_FILE="${AUTH_TOKEN_FILE:-/run/saas-control/smoke/auth-token}"
REQUIRE_AUTH_SMOKE="${REQUIRE_AUTH_SMOKE:-true}"
CANDIDATE_DIR="$RELEASE_ROOT/$RELEASE_ID"

atomic_link() {
  local target="$1"
  local link="$2"
  local tmp="${link}.next.$$"
  ln -s "$target" "$tmp"
  mv -Tf "$tmp" "$link"
}
restart_services() {
  sudo "$SYSTEMCTL_BIN" restart "${BACKEND_SERVICE:-saas-backend}" "${FRONTEND_SERVICE:-saas-frontend}"
  for _ in {1..30}; do
    if curl -fsS -o /dev/null --max-time 3 "${PRODUCTION_BACKEND_LOCAL_URL:-http://127.0.0.1:8001}/health" \
      && curl -fsS -o /dev/null --max-time 3 "${PRODUCTION_FRONTEND_LOCAL_URL:-http://127.0.0.1:3000}/"; then
      return 0
    fi
    sleep 2
  done
  echo "Production services did not become ready in time." >&2
  return 1
}
validate_nginx() {
  sudo "$NGINX_BIN" -t
  sudo "$SYSTEMCTL_BIN" reload nginx
}
rollback() {
  local old_target="$1" old_previous="$2" recovery_status=0
  echo "Restoring previous production release" >&2
  if [[ -n "$old_target" ]]; then
    atomic_link "$old_target" "$CURRENT_LINK" || recovery_status=1
  else
    rm -f "$CURRENT_LINK" || recovery_status=1
  fi
  if [[ -n "$old_previous" ]]; then
    atomic_link "$old_previous" "$PREVIOUS_LINK" || recovery_status=1
  else
    rm -f "$PREVIOUS_LINK" || recovery_status=1
  fi
  if [[ -n "$old_target" ]]; then
    restart_services || recovery_status=1
  else
    sudo "$SYSTEMCTL_BIN" stop "${BACKEND_SERVICE:-saas-backend}" "${FRONTEND_SERVICE:-saas-frontend}" || recovery_status=1
  fi
  validate_nginx || recovery_status=1
  return "$recovery_status"
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

if [[ "$REQUIRE_AUTH_SMOKE" == "true" ]]; then
  [[ -r "$AUTH_TOKEN_FILE" ]] || {
    echo "Production promotion requires a readable AUTH_TOKEN_FILE: $AUTH_TOKEN_FILE" >&2
    exit 1
  }
fi

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "Another production promotion is already running." >&2; exit 1; }

OLD_TARGET="$(readlink -f "$CURRENT_LINK" 2>/dev/null || true)"
OLD_PREVIOUS="$(readlink -f "$PREVIOUS_LINK" 2>/dev/null || true)"
atomic_link "$CANDIDATE_DIR" "$CURRENT_LINK"
if ! restart_services; then
  rollback "$OLD_TARGET" "$OLD_PREVIOUS" || echo "CRITICAL: production rollback after restart failure was not fully verified." >&2
  exit 1
fi
if ! validate_nginx; then
  rollback "$OLD_TARGET" "$OLD_PREVIOUS" || echo "CRITICAL: production rollback after nginx validation failure was not fully verified." >&2
  exit 1
fi

if ! AUTH_TOKEN_FILE="$AUTH_TOKEN_FILE" REQUIRE_AUTH_SMOKE="$REQUIRE_AUTH_SMOKE" \
  BASE_URL="${PRODUCTION_BASE_URL:?Set PRODUCTION_BASE_URL}" \
  BACKEND_URL="${PRODUCTION_BACKEND_URL:?Set PRODUCTION_BACKEND_URL}" \
  EXPECTED_RELEASE="$RELEASE_ID" bash "$CANDIDATE_DIR/scripts/release/smoke.sh"; then
  rollback "$OLD_TARGET" "$OLD_PREVIOUS" || echo "CRITICAL: production rollback after smoke failure was not fully verified." >&2
  echo "Production smoke failed; previous release restored." >&2
  exit 1
fi

if [[ -n "$OLD_TARGET" && "$OLD_TARGET" != "$CANDIDATE_DIR" ]]; then
  atomic_link "$OLD_TARGET" "$PREVIOUS_LINK"
fi

printf 'Production promotion completed for %s\n' "$RELEASE_ID"
