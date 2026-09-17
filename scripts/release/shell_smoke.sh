#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:?Set BASE_URL to the authenticated application origin}"
BACKEND_URL="${BACKEND_URL:?Set BACKEND_URL to the backend origin}"
EXPECTED_RELEASE="${EXPECTED_RELEASE:-}"
EXPECTED_PHASE_ONE_SHELL="${EXPECTED_PHASE_ONE_SHELL:?Set EXPECTED_PHASE_ONE_SHELL to true or false}"
AUTH_TOKEN_FILE="${AUTH_TOKEN_FILE:?Set AUTH_TOKEN_FILE to the temporary smoke token path}"
AUTH_COOKIE_NAME="${AUTH_COOKIE_NAME:-crm-auth-token}"
HOST_HEADER="${HOST_HEADER:-}"
curl_args=()
if [[ -n "$HOST_HEADER" ]]; then curl_args+=( -H "Host: $HOST_HEADER" ); fi

[[ -r "$AUTH_TOKEN_FILE" ]] || { echo "Shell smoke token file is missing" >&2; exit 1; }
token="$(<"$AUTH_TOKEN_FILE")"
[[ -n "$token" ]] || { echo "Shell smoke token file is empty" >&2; exit 1; }

release_payload="$(curl "${curl_args[@]}" -fsS --max-time 20 "$BACKEND_URL/runtime/release")"
python3 - "$EXPECTED_RELEASE" "$EXPECTED_PHASE_ONE_SHELL" "$release_payload" <<'PY'
import json
import sys

expected_release, expected_flag, raw = sys.argv[1:]
payload = json.loads(raw)
if expected_release and payload.get("release_id") != expected_release:
    raise SystemExit("shell smoke release identity mismatch")
actual = bool(payload.get("feature_flags", {}).get("platform_phase1_shell", False))
if actual != (expected_flag.lower() == "true"):
    raise SystemExit("shell smoke feature flag mismatch")
PY

organization_id="$(curl "${curl_args[@]}" -fsS --max-time 20 -H "Authorization: Bearer $token" "$BACKEND_URL/organizations" | python3 -c 'import json,sys; p=json.load(sys.stdin); items=p if isinstance(p,list) else p.get("items",p.get("data",[])); print(items[0].get("id", "") if items else "")')"
tenant_id="$(curl "${curl_args[@]}" -fsS --max-time 20 -H "Authorization: Bearer $token" "$BACKEND_URL/tenants" | python3 -c 'import json,sys; p=json.load(sys.stdin); items=p if isinstance(p,list) else p.get("items",p.get("data",[])); print(items[0].get("id", "") if items else "")')"
organization_id="${organization_id:-synthetic-organization}"
tenant_id="${tenant_id:-synthetic-tenant}"

routes=(
  "/app"
  "/app/organizations"
  "/app/organizations/new"
  "/app/organizations/${organization_id}"
  "/app/organizations/${organization_id}/tenants"
  "/app/tenants"
  "/app/tenants/new"
  "/app/tenants/${tenant_id}"
  "/app/implementation"
  "/app/modules"
  "/app/settings"
)

for route in "${routes[@]}"; do
  response="$(curl "${curl_args[@]}" -fsS --max-time 20 -H "Cookie: ${AUTH_COOKIE_NAME}=${token}" "$BASE_URL$route")"
  [[ -n "$response" ]] || {
    echo "shell smoke returned an empty document for $route" >&2
    exit 1
  }
done

echo "Shell smoke passed: ${#routes[@]} authenticated routes, flag=${EXPECTED_PHASE_ONE_SHELL}"
