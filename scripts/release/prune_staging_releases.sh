#!/usr/bin/env bash
set -Eeuo pipefail

APP_ROOT="${APP_ROOT:-/opt/saas-control-staging}"
RELEASE_ROOT="${RELEASE_ROOT:-$APP_ROOT/releases}"
CURRENT_LINK="${CURRENT_LINK:-$APP_ROOT/current}"
PREVIOUS_LINK="${PREVIOUS_LINK:-$APP_ROOT/previous}"

[[ "$RELEASE_ROOT" == "$APP_ROOT/releases" ]] || { echo "Refusing unexpected staging release root: $RELEASE_ROOT" >&2; exit 1; }
[[ -d "$RELEASE_ROOT" ]] || exit 0
current="$(readlink -f "$CURRENT_LINK" 2>/dev/null || true)"
previous="$(readlink -f "$PREVIOUS_LINK" 2>/dev/null || true)"
while IFS= read -r -d '' candidate; do
  [[ "$candidate" == "$current" || "$candidate" == "$previous" ]] && continue
  [[ "$candidate" == "$RELEASE_ROOT/"* ]] || { echo "Refusing candidate outside staging release root" >&2; exit 1; }
  rm -rf -- "$candidate"
done < <(find "$RELEASE_ROOT" -mindepth 1 -maxdepth 1 -type d -print0)
