#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${PRODUCTION_PROMOTION_APPROVED:-}" != "yes" ]]; then
  echo "Phase 02 production promotion requires the protected Phase 02 workflow." >&2
  exit 1
fi
if [[ "${PHASE3_MIGRATION_APPROVED:-no}" != "no" ]]; then
  echo "Phase 02 promotion refuses any Phase 03 migration approval." >&2
  exit 1
fi
RELEASE_ID="${RELEASE_ID:?Set RELEASE_ID}"
BACKUP_EVIDENCE_FILE="${BACKUP_EVIDENCE_FILE:?Set BACKUP_EVIDENCE_FILE}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
RELEASE_ROOT="${RELEASE_ROOT:-$APP_ROOT/releases}"
CURRENT_LINK="${CURRENT_LINK:-$APP_ROOT/current}"
PREVIOUS_LINK="${PREVIOUS_LINK:-$APP_ROOT/previous}"
SYSTEMCTL_BIN="${SYSTEMCTL_BIN:-/usr/bin/systemctl}"
NGINX_BIN="${NGINX_BIN:-/usr/sbin/nginx}"
LOCK_FILE="${LOCK_FILE:-/tmp/saas-control-phase2-promote.lock}"
AUTH_TOKEN_FILE="${AUTH_TOKEN_FILE:?Set AUTH_TOKEN_FILE}"
CANDIDATE_DIR="$RELEASE_ROOT/$RELEASE_ID"

[[ "$RELEASE_ID" =~ ^[0-9a-f]{40}$ ]] || { echo "RELEASE_ID must be a full lowercase SHA" >&2; exit 1; }
[[ -f "$BACKUP_EVIDENCE_FILE" ]] || { echo "verified production backup evidence is missing" >&2; exit 1; }
grep -q '"status": "passed"' "$BACKUP_EVIDENCE_FILE" || { echo "production backup did not pass" >&2; exit 1; }
[[ -f "$CANDIDATE_DIR/.candidate-complete" ]] || { echo "candidate is not complete" >&2; exit 1; }
[[ -s "$CANDIDATE_DIR/.staging-smoke-passed" ]] || { echo "candidate has no staging smoke marker" >&2; exit 1; }
grep -Fxq "$RELEASE_ID" "$CANDIDATE_DIR/.staging-smoke-passed" || { echo "staging smoke marker mismatch" >&2; exit 1; }
[[ -s "$CANDIDATE_DIR/.phase2-staging-evidence-verified" ]] || { echo "candidate has no verified Phase 02 staging evidence" >&2; exit 1; }
grep -Fxq "candidate_sha=$RELEASE_ID" "$CANDIDATE_DIR/.phase2-staging-evidence-verified" || { echo "Phase 02 evidence marker mismatch" >&2; exit 1; }

python3 - "$CANDIDATE_DIR/release-manifest.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    manifest = json.load(handle)
if manifest.get("environment") != "staging" or manifest.get("build_environment") != "staging":
    raise SystemExit("production can promote only a staging-built candidate")
PY
bash "$CANDIDATE_DIR/scripts/release/preflight.sh" "$CANDIDATE_DIR"
[[ -r "$AUTH_TOKEN_FILE" ]] || { echo "authenticated production smoke token is missing" >&2; exit 1; }

atomic_link() {
  local target="$1" link="$2" tmp="${2}.next.$$"
  ln -s "$target" "$tmp"
  mv -Tf "$tmp" "$link"
}
restart_services() {
  sudo "$SYSTEMCTL_BIN" restart saas-backend.service saas-frontend.service
  for _ in {1..30}; do
    if curl -fsS -o /dev/null --max-time 3 "${PRODUCTION_BACKEND_LOCAL_URL:-http://127.0.0.1:8001}/health" && curl -fsS -o /dev/null --max-time 3 "${PRODUCTION_FRONTEND_LOCAL_URL:-http://127.0.0.1:3000}/"; then
      return 0
    fi
    sleep 2
  done
  return 1
}
validate_nginx() { sudo "$NGINX_BIN" -t && sudo "$SYSTEMCTL_BIN" reload nginx; }
rollback() {
  local old_target="$1" old_previous="$2" status=0
  if [[ -n "$old_target" ]]; then atomic_link "$old_target" "$CURRENT_LINK" || status=1; else rm -f "$CURRENT_LINK" || status=1; fi
  if [[ -n "$old_previous" ]]; then atomic_link "$old_previous" "$PREVIOUS_LINK" || status=1; else rm -f "$PREVIOUS_LINK" || status=1; fi
  if [[ -n "$old_target" ]]; then restart_services || status=1; fi
  validate_nginx || status=1
  return "$status"
}

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "another production promotion is running" >&2; exit 1; }
old_target="$(readlink -f "$CURRENT_LINK" 2>/dev/null || true)"
old_previous="$(readlink -f "$PREVIOUS_LINK" 2>/dev/null || true)"
atomic_link "$CANDIDATE_DIR" "$CURRENT_LINK"
if ! restart_services || ! validate_nginx; then
  rollback "$old_target" "$old_previous" || echo "CRITICAL: production code rollback was not fully verified" >&2
  exit 1
fi

if ! AUTH_TOKEN_FILE="$AUTH_TOKEN_FILE" REQUIRE_AUTH_SMOKE=true BASE_URL="${PRODUCTION_BASE_URL:?Set PRODUCTION_BASE_URL}" BACKEND_URL="${PRODUCTION_BACKEND_URL:?Set PRODUCTION_BACKEND_URL}" EXPECTED_RELEASE="$RELEASE_ID" EXPECTED_RUNTIME_ENVIRONMENT=production EXPECTED_BUILD_ENVIRONMENT=staging EXPECTED_DATABASE_REVISION=20260918_0011 bash "$CANDIDATE_DIR/scripts/release/smoke.sh"; then
  rollback "$old_target" "$old_previous" || echo "CRITICAL: production rollback after smoke failure was not fully verified" >&2
  exit 1
fi
if [[ -n "$old_target" && "$old_target" != "$CANDIDATE_DIR" ]]; then atomic_link "$old_target" "$PREVIOUS_LINK"; fi
promotion_dir="/opt/saas-control/shared/phase2-promotions/$RELEASE_ID"
sudo install -d -m 0750 "$promotion_dir"
sudo install -m 0640 "$BACKUP_EVIDENCE_FILE" "$promotion_dir/production-backup.json"
printf 'candidate_sha=%s\nprevious_release=%s\nphase3_migration=not-run\n' "$RELEASE_ID" "${old_target##*/}" | sudo tee "$promotion_dir/promotion-readback.txt" >/dev/null
echo "Phase 02 production promotion completed for $RELEASE_ID"
