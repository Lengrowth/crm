#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-/opt/frappe-staging-bench}"
SITE="${SITE:-erp-staging.example.test}"
RUN_ID="${RUN_ID:-manual}"
ROLE_PASSWORD_FILE="${ROLE_PASSWORD_FILE:-/run/saas-control-staging/erp-role-password-${RUN_ID}}"
ROLE_EMAIL_PREFIX="${ROLE_EMAIL_PREFIX:-champion-demo-role-${RUN_ID}}"
OUTPUT_FILE="${OUTPUT_FILE:-erp-role-permission-evidence.json}"

case "$SITE" in
  erp-staging.example.test|*.staging.example.test) ;;
  *) echo "ERP role smoke only accepts a staging site" >&2; exit 1 ;;
esac

sudo install -d -o frappe -g frappe -m 0700 "$(dirname "$ROLE_PASSWORD_FILE")"
if [[ ! -s "$ROLE_PASSWORD_FILE" ]]; then
  sudo openssl rand -hex 32 | sudo tee "$ROLE_PASSWORD_FILE" >/dev/null
  sudo chown frappe:frappe "$ROLE_PASSWORD_FILE"
  sudo chmod 0600 "$ROLE_PASSWORD_FILE"
fi

output="$(sudo -u frappe env DEMO_ROLE_PASSWORD_FILE="$ROLE_PASSWORD_FILE" DEMO_ROLE_EMAIL_PREFIX="$ROLE_EMAIL_PREFIX" bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' execute lenerp_core.permission_smoke.run")"
grep -q 'Champion Platform Operator' <<<"$output" || { echo "role smoke did not exercise platform operator" >&2; exit 1; }
grep -q 'platform_operator_denied' <<<"$output" || { echo "role smoke did not emit denial evidence" >&2; exit 1; }
mkdir -p "$(dirname "$OUTPUT_FILE")"
printf '%s\n' "$output" > "$OUTPUT_FILE"
echo "ERP role-principal permission smoke passed for ${SITE}"
cat "$OUTPUT_FILE"
