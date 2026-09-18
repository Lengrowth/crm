#!/usr/bin/env bash
set -euo pipefail

# main is staging-only. Production uses promote_saas_control.sh with explicit approval.
DEPLOY_TARGET="${DEPLOY_TARGET:-staging}"
if [[ "$DEPLOY_TARGET" != "staging" ]]; then
  echo "This workflow only deploys staging. Use scripts/deploy/promote_saas_control.sh for production." >&2
  exit 1
fi

SOURCE_REPO="${SOURCE_REPO:-${GITHUB_WORKSPACE:-$PWD}}"
APP_ROOT="${APP_ROOT:-/opt/saas-control-staging}"
RELEASE_ROOT="${RELEASE_ROOT:-$APP_ROOT/releases}"
CURRENT_LINK="${CURRENT_LINK:-$APP_ROOT/current}"
PREVIOUS_LINK="${PREVIOUS_LINK:-$APP_ROOT/previous}"
BACKEND_VENV="${BACKEND_VENV:-$APP_ROOT/shared/backend-venv}"
BACKEND_ENV_FILE="${BACKEND_ENV_FILE:-$APP_ROOT/shared/env/staging-backend.env}"
FRONTEND_ENV_FILE="${FRONTEND_ENV_FILE:-$APP_ROOT/shared/env/staging-frontend.env}"
STAGING_SERVICE_USER="${STAGING_SERVICE_USER:-saas-staging}"
BACKEND_SERVICE="${BACKEND_SERVICE:-saas-control-staging-backend}"
FRONTEND_SERVICE="${FRONTEND_SERVICE:-saas-control-staging-frontend}"
WORKER_SERVICE="${WORKER_SERVICE:-saas-control-staging-worker}"
SYSTEMCTL_BIN="${SYSTEMCTL_BIN:-/usr/bin/systemctl}"
NGINX_BIN="${NGINX_BIN:-/usr/sbin/nginx}"
LOCK_FILE="${LOCK_FILE:-/tmp/saas-control-staging-deploy.lock}"
TARGET_REF="${TARGET_REF:-${GITHUB_SHA:-$(git -C "$SOURCE_REPO" rev-parse HEAD)}}"
RELEASE_ID="${RELEASE_ID:-$(git -C "$SOURCE_REPO" rev-parse "$TARGET_REF")}"

log() { printf '\n[%s] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"; }
load_env_file() {
  local env_file="$1"
  [[ -f "$env_file" ]] || { printf 'Required environment file is missing: %s\n' "$env_file" >&2; exit 1; }
  set -a
  # shellcheck disable=SC1090
  source "$env_file"
  set +a
}
atomic_link() {
  local target="$1" link="$2"
  local tmp="${link}.next.$$"
  [[ "$target" != "$link" ]] || { echo "Refusing self-referential release link: $link" >&2; return 1; }
  [[ -d "$target" ]] || { echo "Release target is not a directory: $target" >&2; return 1; }
  rm -f "$tmp"
  ln -s "$target" "$tmp"
  mv -Tf "$tmp" "$link"
}
restart_services() {
  [[ "${SKIP_SERVICE_RESTART:-false}" == "true" ]] && return 0
  sudo "$SYSTEMCTL_BIN" restart "$BACKEND_SERVICE" "$FRONTEND_SERVICE" "$WORKER_SERVICE"
  for _ in {1..30}; do
    if curl -fsS -o /dev/null --max-time 3 "${STAGING_BACKEND_URL:-http://127.0.0.1:18001}/health" \
      && curl -fsS -o /dev/null --max-time 3 "${STAGING_BASE_URL:-http://127.0.0.1:13001}/"; then
      return 0
    fi
    sleep 2
  done
  echo "Staging services did not become ready in time." >&2
  return 1
}
validate_nginx() {
  [[ "${VALIDATE_NGINX:-false}" != "true" ]] && return 0
  sudo "$NGINX_BIN" -t
  sudo "$SYSTEMCTL_BIN" reload nginx
}
rollback() {
  local old_target="$1" old_previous="$2"
  log "Smoke failed; restoring previous release"
  if [[ -n "$old_target" ]]; then
    atomic_link "$old_target" "$CURRENT_LINK"
  else
    rm -f "$CURRENT_LINK"
  fi
  if [[ -n "$old_previous" ]]; then
    atomic_link "$old_previous" "$PREVIOUS_LINK"
  else
    rm -f "$PREVIOUS_LINK"
  fi
  if [[ -n "$old_target" ]]; then
    restart_services || true
  else
    sudo "$SYSTEMCTL_BIN" stop "$BACKEND_SERVICE" "$FRONTEND_SERVICE" || true
  fi
  validate_nginx || log "Nginx validation after staging rollback failed; manual recovery may be required."
}
install_worker_unit() {
  local unit_file="$CANDIDATE_DIR/ops/staging/saas-control-staging-worker.service"
  [[ -f "$unit_file" ]] || { echo "Staging worker unit is missing from the candidate." >&2; return 1; }
  sudo install -m 0644 "$unit_file" "/etc/systemd/system/$WORKER_SERVICE.service"
  sudo "$SYSTEMCTL_BIN" daemon-reload
}

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "Another staging deployment is already running." >&2; exit 1; }

mkdir -p "$APP_ROOT" "$RELEASE_ROOT"
load_env_file "$BACKEND_ENV_FILE"
load_env_file "$FRONTEND_ENV_FILE"

log "Building candidate $RELEASE_ID from immutable ref $TARGET_REF"
CANDIDATE_DIR="$(SOURCE_REPO="$SOURCE_REPO" RELEASE_ROOT="$RELEASE_ROOT" TARGET_REF="$TARGET_REF" RELEASE_ID="$RELEASE_ID" DEPLOY_TARGET=staging BACKEND_VENV="$BACKEND_VENV" bash "$SOURCE_REPO/scripts/release/build_candidate.sh" | tail -n 1)"
bash "$CANDIDATE_DIR/scripts/release/preflight.sh" "$CANDIDATE_DIR"

if id "$STAGING_SERVICE_USER" >/dev/null 2>&1; then
  sudo chown -R "$STAGING_SERVICE_USER:$STAGING_SERVICE_USER" "$CANDIDATE_DIR"
  sudo chmod -R a+rX "$CANDIDATE_DIR"
fi

if [[ "${RUN_DB_MIGRATION:-true}" == "true" ]]; then
  log "Applying compatible staging migrations"
  if id "$STAGING_SERVICE_USER" >/dev/null 2>&1; then
    (cd "$CANDIDATE_DIR/backend" && sudo -n -E -u "$STAGING_SERVICE_USER" "$BACKEND_VENV/bin/alembic" -c alembic.ini upgrade head)
  else
    (cd "$CANDIDATE_DIR/backend" && "$BACKEND_VENV/bin/alembic" -c alembic.ini upgrade head)
  fi
  log "Synchronizing additive reference catalog and bundles"
  if id "$STAGING_SERVICE_USER" >/dev/null 2>&1; then
    (cd "$CANDIDATE_DIR/backend" && sudo -n -E -u "$STAGING_SERVICE_USER" env PYTHONPATH="$CANDIDATE_DIR/backend" "$BACKEND_VENV/bin/python" -m app.db.seed)
  else
    (cd "$CANDIDATE_DIR/backend" && PYTHONPATH="$CANDIDATE_DIR/backend" "$BACKEND_VENV/bin/python" -m app.db.seed)
  fi
fi

OLD_TARGET="$(readlink -f "$CURRENT_LINK" 2>/dev/null || true)"
OLD_PREVIOUS="$(readlink -f "$PREVIOUS_LINK" 2>/dev/null || true)"
[[ "$OLD_TARGET" == "$CURRENT_LINK" || ! -d "$OLD_TARGET" ]] && OLD_TARGET=""
[[ "$OLD_PREVIOUS" == "$PREVIOUS_LINK" || ! -d "$OLD_PREVIOUS" ]] && OLD_PREVIOUS=""
atomic_link "$CANDIDATE_DIR" "$CURRENT_LINK"
if ! install_worker_unit; then
  rollback "$OLD_TARGET" "$OLD_PREVIOUS"
  exit 1
fi
if ! restart_services; then
  rollback "$OLD_TARGET" "$OLD_PREVIOUS"
  exit 1
fi
if ! validate_nginx; then
  log "Nginx validation failed after staging switch; rolling back."
  rollback "$OLD_TARGET" "$OLD_PREVIOUS" || log "Nginx validation after staging rollback failed; manual recovery may be required."
  exit 1
fi

if [[ "${REQUIRE_AUTH_SMOKE:-false}" == "true" ]]; then
  if id "$STAGING_SERVICE_USER" >/dev/null 2>&1; then
    if ! sudo -n -E -u "$STAGING_SERVICE_USER" env \
      PYTHONPATH="$CANDIDATE_DIR/backend" \
      "$BACKEND_VENV/bin/python" \
      "$CANDIDATE_DIR/scripts/release/prepare_staging_smoke_auth.py" \
      --token-file "${AUTH_TOKEN_FILE:-/run/saas-control-staging/smoke/auth-token}"; then
      rollback "$OLD_TARGET" "$OLD_PREVIOUS"
      exit 1
    fi
  else
    if ! PYTHONPATH="$CANDIDATE_DIR/backend" "$BACKEND_VENV/bin/python" \
      "$CANDIDATE_DIR/scripts/release/prepare_staging_smoke_auth.py" \
      --token-file "${AUTH_TOKEN_FILE:-/run/saas-control-staging/smoke/auth-token}"; then
      rollback "$OLD_TARGET" "$OLD_PREVIOUS"
      exit 1
    fi
  fi
fi

smoke_command=(
  env
  BASE_URL="${STAGING_BASE_URL:-http://127.0.0.1:13001}"
  BACKEND_URL="${STAGING_BACKEND_URL:-http://127.0.0.1:18001}"
  EXPECTED_RELEASE="$RELEASE_ID"
  HOST_HEADER="staging.example.test"
  bash "$CANDIDATE_DIR/scripts/release/smoke.sh"
)
if id "$STAGING_SERVICE_USER" >/dev/null 2>&1; then
  smoke_command=(sudo -n -E -u "$STAGING_SERVICE_USER" "${smoke_command[@]}")
fi
if ! "${smoke_command[@]}"; then
  rollback "$OLD_TARGET" "$OLD_PREVIOUS"
  exit 1
fi
if id "$STAGING_SERVICE_USER" >/dev/null 2>&1; then
  printf '%s\n' "$RELEASE_ID" | sudo -n -u "$STAGING_SERVICE_USER" tee "$CANDIDATE_DIR/.staging-smoke-passed" >/dev/null
else
  printf '%s\n' "$RELEASE_ID" > "$CANDIDATE_DIR/.staging-smoke-passed"
fi

if [[ -n "$OLD_TARGET" && "$OLD_TARGET" != "$CANDIDATE_DIR" ]]; then
  atomic_link "$OLD_TARGET" "$PREVIOUS_LINK"
fi

log "Staging deployment completed for $RELEASE_ID"
