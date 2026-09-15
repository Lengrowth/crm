#!/usr/bin/env bash
set -euo pipefail

if [[ "$(id -u)" != "0" ]]; then
  echo "Run this bootstrap as root." >&2
  exit 1
fi

APP_ROOT="${APP_ROOT:-/opt/saas-control-staging}"
SOURCE_REPO="${SOURCE_REPO:-/opt/saas-control/repo}"
STAGING_USER="${STAGING_USER:-saas-staging}"
STAGING_GROUP="${STAGING_GROUP:-saas-staging}"
VENV="$APP_ROOT/shared/backend-venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$(command -v python3.11 || command -v python3)}"

if ! getent group "$STAGING_GROUP" >/dev/null; then
  groupadd --system "$STAGING_GROUP"
fi
if ! id "$STAGING_USER" >/dev/null 2>&1; then
  useradd --system --home-dir "$APP_ROOT" --shell /usr/sbin/nologin --gid "$STAGING_GROUP" "$STAGING_USER"
fi

install -d -o ubuntu -g "$STAGING_GROUP" -m 0775 \
  "$APP_ROOT" "$APP_ROOT/releases" "$APP_ROOT/shared" "$APP_ROOT/shared/env"
install -d -o "$STAGING_USER" -g "$STAGING_GROUP" -m 0750 \
  "$APP_ROOT/shared/data" "$APP_ROOT/shared/logs" /run/saas-control-staging/smoke

if [[ ! -x "$VENV/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$VENV"
fi
"$VENV/bin/pip" install "$SOURCE_REPO/backend" >/dev/null
chmod -R a+rX "$VENV"
chown -R ubuntu:"$STAGING_GROUP" "$VENV"

install -m 0644 "$SCRIPT_DIR/ec2-staging-backend.env" "$APP_ROOT/shared/env/staging-backend.env"
install -m 0644 "$SCRIPT_DIR/ec2-staging-frontend.env" "$APP_ROOT/shared/env/staging-frontend.env"
install -m 0644 "$SCRIPT_DIR/saas-control-staging-backend.service" /etc/systemd/system/saas-control-staging-backend.service
install -m 0644 "$SCRIPT_DIR/saas-control-staging-frontend.service" /etc/systemd/system/saas-control-staging-frontend.service

chown -R "$STAGING_USER:$STAGING_GROUP" "$APP_ROOT/shared/data" "$APP_ROOT/shared/logs" /run/saas-control-staging
chmod 0750 "$APP_ROOT/shared/data" "$APP_ROOT/shared/logs" /run/saas-control-staging
systemctl daemon-reload
systemctl enable saas-control-staging-backend.service saas-control-staging-frontend.service
echo "Staging control-plane lane bootstrapped at $APP_ROOT; services are enabled but not started until a candidate is deployed."
