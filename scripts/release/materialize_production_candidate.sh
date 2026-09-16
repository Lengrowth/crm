#!/usr/bin/env bash
set -euo pipefail

RELEASE_ID="${RELEASE_ID:?Set RELEASE_ID to the exact tested staging candidate}"
STAGING_ROOT="${STAGING_RELEASE_ROOT:-/opt/saas-control-staging/releases}"
PRODUCTION_ROOT="${PRODUCTION_RELEASE_ROOT:-/opt/saas-control/releases}"
SOURCE_CANDIDATE="$STAGING_ROOT/$RELEASE_ID"
TARGET_CANDIDATE="$PRODUCTION_ROOT/$RELEASE_ID"

case "$SOURCE_CANDIDATE" in "$STAGING_ROOT"/*) ;; *) exit 1 ;; esac
case "$TARGET_CANDIDATE" in "$PRODUCTION_ROOT"/*) ;; *) exit 1 ;; esac

[[ -f "$SOURCE_CANDIDATE/.candidate-complete" ]] || {
  echo "Tested staging candidate is missing: $SOURCE_CANDIDATE" >&2
  exit 1
}
[[ -s "$SOURCE_CANDIDATE/.staging-smoke-passed" ]] || {
  echo "Tested staging candidate has no smoke marker: $SOURCE_CANDIDATE" >&2
  exit 1
}
grep -Fxq "$RELEASE_ID" "$SOURCE_CANDIDATE/.staging-smoke-passed" || {
  echo "Staging smoke marker does not match RELEASE_ID" >&2
  exit 1
}

if [[ -e "$TARGET_CANDIDATE" ]]; then
  [[ -f "$TARGET_CANDIDATE/.candidate-complete" ]] || {
    echo "Production candidate path exists without completion marker: $TARGET_CANDIDATE" >&2
    exit 1
  }
  echo "Reusing immutable production candidate $TARGET_CANDIDATE"
  exit 0
fi

mkdir -p "$PRODUCTION_ROOT"
temporary_candidate="$PRODUCTION_ROOT/.${RELEASE_ID}.incoming.$$"
cleanup() { rm -rf -- "$temporary_candidate"; }
trap cleanup EXIT
cp -a "$SOURCE_CANDIDATE" "$temporary_candidate"
mv -T "$temporary_candidate" "$TARGET_CANDIDATE"
trap - EXIT
echo "Materialized tested staging candidate at $TARGET_CANDIDATE"
