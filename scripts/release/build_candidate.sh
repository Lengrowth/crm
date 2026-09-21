#!/usr/bin/env bash
set -euo pipefail

SOURCE_REPO="${SOURCE_REPO:-${GITHUB_WORKSPACE:-$PWD}}"
RELEASE_ROOT="${RELEASE_ROOT:-/opt/saas-control/releases}"
TARGET_REF="${TARGET_REF:-${GITHUB_SHA:-$(git -C "$SOURCE_REPO" rev-parse HEAD)}}"
RELEASE_ID="${RELEASE_ID:-$(git -C "$SOURCE_REPO" rev-parse "$TARGET_REF")}"
CANDIDATE_DIR="$RELEASE_ROOT/$RELEASE_ID"
RUNTIME_BASELINE_FILE="${RUNTIME_BASELINE_FILE:-$SOURCE_REPO/ops/${DEPLOY_TARGET:-staging}/release-runtime-baseline.json}"

mkdir -p "$RELEASE_ROOT"
if [[ -f "$CANDIDATE_DIR/.candidate-complete" ]]; then
  printf 'Reusing immutable candidate %s\n' "$CANDIDATE_DIR"
  printf '%s\n' "$CANDIDATE_DIR"
  exit 0
fi

if [[ -e "$CANDIDATE_DIR" ]]; then
  printf 'Candidate directory exists without completion marker: %s\n' "$CANDIDATE_DIR" >&2
  exit 1
fi

mkdir "$CANDIDATE_DIR"
git -C "$SOURCE_REPO" archive "$TARGET_REF" | tar -x -C "$CANDIDATE_DIR"

CUSTOM_APP_VERSION_VALUE="${CUSTOM_APP_VERSION:-not-installed}"
CUSTOM_APP_COMMIT_VALUE="${CUSTOM_APP_COMMIT:-unknown}"
if [[ -n "${CUSTOM_APP_REPO:-}" ]]; then
  [[ -d "$CUSTOM_APP_REPO/.git" ]] || { echo "custom app repository is missing: $CUSTOM_APP_REPO" >&2; exit 1; }
  [[ -z "$(git -C "$CUSTOM_APP_REPO" status --porcelain --untracked-files=all)" ]] || { echo "custom app repository is not clean" >&2; exit 1; }
  CUSTOM_APP_REF="${CUSTOM_APP_REF:-$(git -C "$CUSTOM_APP_REPO" rev-parse HEAD)}"
  CUSTOM_APP_COMMIT_VALUE="$(git -C "$CUSTOM_APP_REPO" rev-parse "$CUSTOM_APP_REF")"
  mkdir "$CANDIDATE_DIR/custom-app"
  git -C "$CUSTOM_APP_REPO" archive "$CUSTOM_APP_REF" | tar -x -C "$CANDIDATE_DIR/custom-app"
  CUSTOM_APP_VERSION_VALUE="$(python3 - "$CANDIDATE_DIR/custom-app/pyproject.toml" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8") if path.is_file() else ""
match = re.search(r"^version\s*=\s*['\"]([^'\"]+)", text, flags=re.MULTILINE)
print(match.group(1) if match else "unknown")
PY
)"
fi

python3 "$SOURCE_REPO/scripts/release/build_manifest.py" \
  --root "$CANDIDATE_DIR" \
  --output "$CANDIDATE_DIR/release-manifest.json" \
  --release-id "$RELEASE_ID" \
  --control-plane-commit "$(git -C "$SOURCE_REPO" rev-parse "$TARGET_REF")" \
  --environment "${DEPLOY_TARGET:-staging}" \
  --operator "${RELEASE_OPERATOR:-ci}" \
  --database-revision-before "${DATABASE_REVISION_BEFORE:-unknown}" \
  --database-revision-after "${DATABASE_REVISION_AFTER:-unknown}" \
  --upstream-frappe-commit "${UPSTREAM_FRAPPE_COMMIT:-unknown}" \
  --upstream-erpnext-commit "${UPSTREAM_ERPNEXT_COMMIT:-unknown}" \
  --custom-app-version "$CUSTOM_APP_VERSION_VALUE" \
  --custom-app-commit "$CUSTOM_APP_COMMIT_VALUE" \
  --runtime-baseline "$RUNTIME_BASELINE_FILE" \
  --feature-flags "${FEATURE_FLAGS:-}" \
  --application-dependencies "$CANDIDATE_DIR/ops/staging/application-dependencies.json"

if [[ -f "$CANDIDATE_DIR/frontend/package-lock.json" ]]; then
  npm --prefix "$CANDIDATE_DIR/frontend" ci --include=dev
  npm --prefix "$CANDIDATE_DIR/frontend" run build
fi

if [[ -n "${BACKEND_VENV:-}" && -x "$BACKEND_VENV/bin/pip" ]]; then
  "$BACKEND_VENV/bin/pip" install --no-deps "$CANDIDATE_DIR/backend" >/dev/null
fi

touch "$CANDIDATE_DIR/.candidate-complete"
printf 'Built immutable candidate %s\n' "$CANDIDATE_DIR"
printf '%s\n' "$CANDIDATE_DIR"
