#!/usr/bin/env bash
set -euo pipefail

# Staging-only smoke for the LenERP custom app. It intentionally uses the
# explicit opt-in seed and never accepts a production hostname.
BENCH_ROOT="${BENCH_ROOT:-/opt/frappe-staging-bench}"
SITE="${SITE:-erp-staging.example.test}"
KEEP_DEMO="${KEEP_DEMO:-1}"
EXPECTED_CUSTOM_APP_VERSION="${EXPECTED_CUSTOM_APP_VERSION:-0.3.0}"

case "$SITE" in
  erp-staging.example.test|*.staging.example.test) ;;
  *) echo "ERP demo smoke only accepts a staging site" >&2; exit 1 ;;
esac

apps="$(sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' list-apps")"
grep -Eq "^lenerp_core[[:space:]]+${EXPECTED_CUSTOM_APP_VERSION}([[:space:]]|$)" <<<"$apps" || {
  echo "Expected lenerp_core ${EXPECTED_CUSTOM_APP_VERSION} on ${SITE}" >&2
  exit 1
}

execute() {
  sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' execute '$1'"
}

seed_output="$(execute lenerp_core.demo_seed.seed)"
status_output="$(execute lenerp_core.demo_seed.status)"
grep -q 'DEMO-CHAMPION-' <<<"$seed_output" || { echo "demo seed returned no demo marker" >&2; exit 1; }
grep -q 'LenERP Drilling Job' <<<"$status_output" || { echo "demo status did not include jobs" >&2; exit 1; }
for expected in \
  '"Customer"[[:space:]]*:[[:space:]]*3' \
  '"LenERP Well Site"[[:space:]]*:[[:space:]]*3' \
  '"LenERP Drilling Job"[[:space:]]*:[[:space:]]*4' \
  '"Supplier"[[:space:]]*:[[:space:]]*1' \
  '"Item"[[:space:]]*:[[:space:]]*2' \
  '"Quotation"[[:space:]]*:[[:space:]]*1' \
  '"Sales Invoice"[[:space:]]*:[[:space:]]*1' \
  '"Payment Entry"[[:space:]]*:[[:space:]]*1' \
  '"Purchase Receipt"[[:space:]]*:[[:space:]]*1' \
  '"Stock Entry"[[:space:]]*:[[:space:]]*1' \
  '"Asset"[[:space:]]*:[[:space:]]*2' \
  '"Asset Maintenance"[[:space:]]*:[[:space:]]*2'; do
  grep -Eq "$expected" <<<"$status_output" || { echo "demo status missing expected persisted count: $expected" >&2; exit 1; }
done

echo "ERP synthetic demonstration seed passed for ${SITE}"
echo "$seed_output"
echo "$status_output"

if [[ "$KEEP_DEMO" != "1" ]]; then
  reset_output="$(execute lenerp_core.demo_seed.reset)"
  verify_output="$(execute lenerp_core.demo_seed.status)"
  echo "$reset_output"
  grep -q "'LenERP Drilling Job': 0" <<<"$verify_output" || { echo "demo reset left job records" >&2; exit 1; }
  echo "ERP synthetic demonstration reset passed"
fi
