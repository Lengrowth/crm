#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-/opt/frappe-staging-bench}"
SITE="${SITE:-erp-staging.example.test}"
BASE_URL="${BASE_URL:-http://127.0.0.1:28000}"
HOST_HEADER="${HOST_HEADER:-$SITE}"
EXPECTED_FRAPPE_COMMIT="${EXPECTED_FRAPPE_COMMIT:-edae775dd36b6c4ad7acab10230262bd74040765}"
EXPECTED_ERPNEXT_COMMIT="${EXPECTED_ERPNEXT_COMMIT:-945e825bee3d0d645f6cb59bcaab90fcbfb98ce3}"
EXPECTED_HRMS_VERSION="${EXPECTED_HRMS_VERSION:-15.64.1}"
EXPECTED_HRMS_COMMIT="${EXPECTED_HRMS_COMMIT:-e68a3deaa95ae5b2c3d743297d0a4ab505733fc1}"
EXPECTED_CUSTOM_APP_VERSION="${EXPECTED_CUSTOM_APP_VERSION:-0.2.0}"

for unit in \
  frappe-staging-redis-cache.service \
  frappe-staging-redis-queue.service \
  frappe-staging-web.service \
  frappe-staging-worker-short.service \
  frappe-staging-schedule.service; do
  systemctl is-active --quiet "$unit" || {
    echo "ERP staging service is not active: $unit" >&2
    exit 1
  }
done
echo "ERP staging services passed"

wait_for_loopback_port() {
  local port="$1"
  for attempt in $(seq 1 30); do
    if ss -ltn | grep -Eq "127\.0\.0\.1:${port}[[:space:]]"; then
      return 0
    fi
    sleep 2
  done
  echo "ERP staging port is not listening on loopback after 60s: $port" >&2
  return 1
}

for port in 14100 14101 28000; do
  wait_for_loopback_port "$port" || exit 1
done
echo "ERP staging ports passed"

check_http() {
  local name="$1" url="$2" expected="$3" code
  code="$(curl -sS -o /dev/null -w '%{http_code}' -H "Host: $HOST_HEADER" --max-time 20 "$url")"
  [[ "$code" == "$expected" ]] || {
    echo "$name returned HTTP $code, expected $expected" >&2
    exit 1
  }
  echo "$name passed ($code)"
}

check_http "ERP public root" "$BASE_URL/" 200
check_http "ERP login" "$BASE_URL/login" 200
check_http "ERP unauthenticated API" "$BASE_URL/api/method/frappe.auth.get_logged_user" 403

apps="$(sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' list-apps")"
grep -Eq '^frappe[[:space:]]+15\.119\.1([[:space:]]|$)' <<<"$apps" || {
  echo "staging Frappe version mismatch" >&2
  exit 1
}
grep -Eq '^erpnext[[:space:]]+15\.120\.0([[:space:]]|$)' <<<"$apps" || {
  echo "staging ERPNext version mismatch" >&2
  exit 1
}
grep -Eq "^hrms[[:space:]]+${EXPECTED_HRMS_VERSION}([[:space:]]|$)" <<<"$apps" || {
  echo "staging HRMS version mismatch" >&2
  exit 1
}
grep -Eq "^lenerp_core[[:space:]]+${EXPECTED_CUSTOM_APP_VERSION}([[:space:]]|$)" <<<"$apps" || {
  echo "staging custom app is not installed" >&2
  exit 1
}
[[ "$(sudo -u frappe git -C "$BENCH_ROOT/apps/frappe" rev-parse HEAD)" == "$EXPECTED_FRAPPE_COMMIT" ]] || {
  echo "staging Frappe commit mismatch" >&2
  exit 1
}
[[ "$(sudo -u frappe git -C "$BENCH_ROOT/apps/erpnext" rev-parse HEAD)" == "$EXPECTED_ERPNEXT_COMMIT" ]] || {
  echo "staging ERPNext commit mismatch" >&2
  exit 1
}
[[ "$(sudo -u frappe git -C "$BENCH_ROOT/apps/hrms" rev-parse HEAD)" == "$EXPECTED_HRMS_COMMIT" ]] || {
  echo "staging HRMS commit mismatch" >&2
  exit 1
}
echo "ERP staging app inventory and pinned commits passed"
