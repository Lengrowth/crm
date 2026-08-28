#!/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-main}"
TARGET_REF="${2:-}"
APP_ROOT="${APP_ROOT:-/opt/saas-control}"
REPO_DIR="${REPO_DIR:-$APP_ROOT/repo}"
BACKEND_DIR="$REPO_DIR/backend"
FRONTEND_DIR="$REPO_DIR/frontend"
BACKEND_VENV="${BACKEND_VENV:-$APP_ROOT/shared/backend-venv}"
BACKEND_ENV_FILE="${BACKEND_ENV_FILE:-$APP_ROOT/shared/env/backend.env}"
FRONTEND_ENV_FILE="${FRONTEND_ENV_FILE:-$APP_ROOT/shared/env/frontend.env}"
SYSTEMCTL_BIN="${SYSTEMCTL_BIN:-/usr/bin/systemctl}"
NGINX_BIN="${NGINX_BIN:-/usr/sbin/nginx}"
LOCK_FILE="${LOCK_FILE:-/tmp/saas-control-deploy.lock}"

log() {
  printf '\n[%s] %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*"
}

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    echo "Required file not found: $path" >&2
    exit 1
  fi
}

require_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    echo "Required directory not found: $path" >&2
    exit 1
  fi
}

load_env_file() {
  local env_file="$1"
  set -a
  # shellcheck disable=SC1090
  source "$env_file"
  set +a
}

retry() {
  local attempts="$1"
  local delay_seconds="$2"
  shift 2

  local try=1
  until "$@"; do
    if (( try >= attempts )); then
      echo "Command failed after ${attempts} attempts: $*" >&2
      return 1
    fi
    log "Attempt ${try}/${attempts} failed. Retrying in ${delay_seconds}s: $*"
    sleep "$delay_seconds"
    try=$((try + 1))
  done
}

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "Another deployment is already running. Lock file: $LOCK_FILE" >&2
  exit 1
fi

require_dir "$REPO_DIR"
require_dir "$BACKEND_DIR"
require_dir "$FRONTEND_DIR"
require_dir "$BACKEND_VENV"
require_file "$BACKEND_ENV_FILE"
require_file "$FRONTEND_ENV_FILE"

log "Starting SaaS deploy from $REPO_DIR"
cd "$REPO_DIR"

log "Fetching latest git refs"
git fetch --prune origin

git checkout "$BRANCH"

if [[ -n "$TARGET_REF" ]]; then
  log "Resetting repository to target ref $TARGET_REF"
  git reset --hard "$TARGET_REF"
else
  log "Resetting repository to origin/$BRANCH"
  git reset --hard "origin/$BRANCH"
fi

log "Installing backend package into shared virtual environment"
cd "$BACKEND_DIR"
"$BACKEND_VENV/bin/pip" install .

log "Running backend database migrations"
load_env_file "$BACKEND_ENV_FILE"
"$BACKEND_VENV/bin/alembic" upgrade head

log "Seeding reference data"
PYTHONPATH="$BACKEND_DIR" "$BACKEND_VENV/bin/python" -m app.db.seed

log "Installing frontend dependencies"
cd "$FRONTEND_DIR"
load_env_file "$FRONTEND_ENV_FILE"
npm install

log "Building frontend production bundle"
npm run build

log "Restarting backend service"
sudo "$SYSTEMCTL_BIN" restart saas-backend

log "Restarting frontend service"
sudo "$SYSTEMCTL_BIN" restart saas-frontend

log "Validating nginx config"
sudo "$NGINX_BIN" -t

log "Reloading nginx"
sudo "$SYSTEMCTL_BIN" reload nginx

log "Waiting for backend health endpoint"
retry 10 3 curl -fsS http://127.0.0.1:8001/health >/tmp/saas-backend-health.json
cat /tmp/saas-backend-health.json

log "Waiting for ERPNext runtime endpoint"
retry 10 3 curl -fsS http://127.0.0.1:8001/integrations/erpnext/runtime >/tmp/saas-erpnext-runtime.json
cat /tmp/saas-erpnext-runtime.json

log "Waiting for frontend root route"
retry 10 3 curl -IfsS http://127.0.0.1:3000/ >/tmp/saas-frontend-head.txt
cat /tmp/saas-frontend-head.txt

log "Checking service status"
sudo "$SYSTEMCTL_BIN" --no-pager --full status saas-backend
sudo "$SYSTEMCTL_BIN" --no-pager --full status saas-frontend
sudo "$SYSTEMCTL_BIN" --no-pager --full status nginx

log "Deployment completed successfully"
