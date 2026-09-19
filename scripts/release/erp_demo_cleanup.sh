#!/usr/bin/env bash
set -euo pipefail

BENCH_ROOT="${BENCH_ROOT:-/opt/frappe-staging-bench}"
SITE="${SITE:-erp-staging.example.test}"
OUTPUT_FILE="${OUTPUT_FILE:-erp-reset-evidence.json}"

case "$SITE" in
  erp-staging.example.test|*.staging.example.test) ;;
  *) echo "ERP demo cleanup only accepts a staging site" >&2; exit 1 ;;
esac

execute() {
  sudo -u frappe bash -lc "cd '$BENCH_ROOT' && bench --site '$SITE' execute '$1'"
}

before="$(execute lenerp_core.demo_seed.status)"
reset="$(execute lenerp_core.demo_seed.reset)"
after="$(execute lenerp_core.demo_seed.status)"
python3 - "$OUTPUT_FILE" "$before" "$reset" "$after" <<'PY'
import ast
import json
import re
import sys
from datetime import datetime, timezone

def parse(value):
    matches = re.findall(r"\{.*\}", value, flags=re.S)
    if not matches:
        raise SystemExit(f"no JSON object in bench output: {value}")
    text = matches[-1]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return ast.literal_eval(text)

payload = {"captured_at_utc": datetime.now(timezone.utc).isoformat(), "before": parse(sys.argv[2]), "reset": parse(sys.argv[3]), "after": parse(sys.argv[4])}
nonzero = {key: value for key, value in payload["after"].items() if int(value) != 0}
if nonzero:
    raise SystemExit(f"synthetic ERP records remain after reset: {nonzero}")
with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, sort_keys=True)
PY
echo "ERP synthetic demonstration reset and read-only zero-count verification passed for ${SITE}"
cat "$OUTPUT_FILE"
