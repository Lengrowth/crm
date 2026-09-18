#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:?Set BASE_URL for the lane under test}"
BACKEND_URL="${BACKEND_URL:-$BASE_URL}"
EXPECTED_RELEASE="${EXPECTED_RELEASE:-}"
EXPECTED_RUNTIME_ENVIRONMENT="${EXPECTED_RUNTIME_ENVIRONMENT:-}"
EXPECTED_BUILD_ENVIRONMENT="${EXPECTED_BUILD_ENVIRONMENT:-}"
EXPECTED_DATABASE_REVISION="${EXPECTED_DATABASE_REVISION:-}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
AUTH_TOKEN_FILE="${AUTH_TOKEN_FILE:-}"
REQUIRE_AUTH_SMOKE="${REQUIRE_AUTH_SMOKE:-false}"
CURL_ARGS=()
if [[ -n "${HOST_HEADER:-}" ]]; then
  CURL_ARGS=(-H "Host: $HOST_HEADER")
fi

check_http() {
  local name="$1"
  local url="$2"
  local expected_code="${3:-200}"
  local code
  code="$(curl "${CURL_ARGS[@]}" -fsS -o /dev/null -w '%{http_code}' --max-time 20 "$url")"
  if [[ "$code" != "$expected_code" ]]; then
    printf '%s returned HTTP %s, expected %s\n' "$name" "$code" "$expected_code" >&2
    return 1
  fi
  printf '%s passed (%s)\n' "$name" "$code"
}

check_http "public root" "$BASE_URL/"
check_http "backend health" "$BACKEND_URL/health"
check_http "ERP runtime summary" "$BACKEND_URL/integrations/erpnext/runtime"
release_payload="$(curl "${CURL_ARGS[@]}" -fsS --max-time 20 "$BACKEND_URL/runtime/release")"
"$PYTHON_BIN" - "$EXPECTED_RELEASE" "$EXPECTED_RUNTIME_ENVIRONMENT" "$EXPECTED_BUILD_ENVIRONMENT" "$EXPECTED_DATABASE_REVISION" "$release_payload" <<'PY'
import json
import sys
expected, expected_runtime_environment, expected_build_environment, expected_database_revision, raw = sys.argv[1:]
payload = json.loads(raw)
if expected and payload.get("release_id") != expected:
    raise SystemExit(f"release identity mismatch: expected {expected}")
if expected_runtime_environment and payload.get("environment") != expected_runtime_environment:
    raise SystemExit(f"runtime environment mismatch: expected {expected_runtime_environment}")
manifest = payload.get("manifest")
if not isinstance(manifest, dict):
    raise SystemExit("release manifest is missing from runtime metadata")
if expected_build_environment and manifest.get("build_environment", manifest.get("environment")) != expected_build_environment:
    raise SystemExit(f"release build environment mismatch: expected {expected_build_environment}")
required = {
    "control_plane_commit",
    "custom_app_commit",
    "custom_app_version",
    "upstream_frappe_commit",
    "upstream_erpnext_commit",
    "installed_apps",
}
missing = sorted(required - manifest.keys())
if missing:
    raise SystemExit(f"release manifest missing installed-app fields: {', '.join(missing)}")
installed_apps = manifest["installed_apps"]
if not isinstance(installed_apps, dict):
    raise SystemExit("release manifest installed_apps is not an object")
for app_name in ("frappe", "erpnext"):
    if not isinstance(installed_apps.get(app_name), dict):
        raise SystemExit(f"release manifest installed_apps missing {app_name}")
    if installed_apps[app_name].get("commit") in {None, "", "unknown"}:
        raise SystemExit(f"release manifest has unknown {app_name} runtime commit")
for field in (
    "custom_app_commit",
    "custom_app_version",
    "upstream_frappe_commit",
    "upstream_erpnext_commit",
    "database_revision_before",
    "database_revision_after",
):
    if manifest.get(field) in {None, "", "unknown", "not-installed"}:
        raise SystemExit(f"release manifest has incomplete runtime field: {field}")
if expected_database_revision and manifest.get("database_revision_after") != expected_database_revision:
    raise SystemExit(f"release database revision mismatch: expected {expected_database_revision}")
PY
printf 'release metadata and installed-app inventory passed\n'

unauthorized_code="$(curl "${CURL_ARGS[@]}" -sS -o /dev/null -w '%{http_code}' --max-time 20 "$BACKEND_URL/organizations")"
if [[ "$unauthorized_code" != "401" && "$unauthorized_code" != "403" ]]; then
  printf 'unauthenticated organizations request returned HTTP %s\n' "$unauthorized_code" >&2
  exit 1
fi
printf 'unauthenticated denial passed (%s)\n' "$unauthorized_code"

if [[ -n "$AUTH_TOKEN_FILE" ]]; then
  [[ -r "$AUTH_TOKEN_FILE" ]] || { echo "AUTH_TOKEN_FILE is not readable" >&2; exit 1; }
  auth_token="$(<"$AUTH_TOKEN_FILE")"
  [[ -n "$auth_token" ]] || { echo "AUTH_TOKEN_FILE is empty" >&2; exit 1; }
  auth_me_payload="$(curl "${CURL_ARGS[@]}" -fsS --max-time 20 -H "Authorization: Bearer $auth_token" "$BACKEND_URL/auth/me")"
  "$PYTHON_BIN" - "$auth_me_payload" <<'PY'
import json
import sys
payload = json.loads(sys.argv[1])
if not payload.get("user", {}).get("id"):
    raise SystemExit("authenticated session payload has no user identity")
PY
  curl "${CURL_ARGS[@]}" -fsS --max-time 20 -H "Authorization: Bearer $auth_token" "$BACKEND_URL/organizations" >/dev/null
  curl "${CURL_ARGS[@]}" -fsS --max-time 20 -H "Authorization: Bearer $auth_token" "$BACKEND_URL/dashboard/summary" >/dev/null
  curl "${CURL_ARGS[@]}" -fsS --max-time 20 -H "Authorization: Bearer $auth_token" "$BACKEND_URL/implementation/portfolio" >/dev/null
  printf 'authenticated application/API checks passed\n'
elif [[ "$REQUIRE_AUTH_SMOKE" == "true" ]]; then
  echo "REQUIRE_AUTH_SMOKE=true but AUTH_TOKEN_FILE is not configured" >&2
  exit 1
else
  printf 'authenticated session checks skipped: AUTH_TOKEN_FILE not configured\n'
fi
