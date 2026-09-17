#!/usr/bin/env bash
set -euo pipefail

SOURCE_REPO="${SOURCE_REPO:-${GITHUB_WORKSPACE:-$PWD}}"
FRONTEND_DIR="$SOURCE_REPO/frontend"
BACKEND_PYTHON="${BACKEND_PYTHON:-python3}"

cleanup() {
  rm -rf -- "$FRONTEND_DIR/node_modules" "$FRONTEND_DIR/.next"
}
trap cleanup EXIT

npm --prefix "$FRONTEND_DIR" ci --include=dev --ignore-scripts --no-audit --no-fund
npm --prefix "$FRONTEND_DIR" test
npm --prefix "$FRONTEND_DIR" run typecheck
npm --prefix "$FRONTEND_DIR" run build
"$BACKEND_PYTHON" -m pytest "$SOURCE_REPO/backend/tests" -q
"$BACKEND_PYTHON" -m compileall -q "$SOURCE_REPO/backend"
"$BACKEND_PYTHON" "$SOURCE_REPO/scripts/release/secret_scan.py"

echo "Candidate validation passed for $(git -C "$SOURCE_REPO" rev-parse HEAD)"
