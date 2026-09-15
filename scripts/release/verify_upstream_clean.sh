#!/usr/bin/env bash
set -euo pipefail

check_repo() {
  local name="$1"
  local repo="$2"
  local expected="${3:-}"
  if [[ ! -d "$repo/.git" ]]; then
    printf '%s repository missing: %s\n' "$name" "$repo" >&2
    return 1
  fi
  if [[ -n "$(git -C "$repo" status --porcelain --untracked-files=all)" ]]; then
    printf '%s repository is not clean: %s\n' "$name" "$repo" >&2
    return 1
  fi
  if [[ -z "$expected" ]]; then
    printf '%s expected commit is not configured; refusing an unpinned verification\n' "$name" >&2
    return 1
  fi
  local actual
  actual="$(git -C "$repo" rev-parse HEAD)"
  if [[ "$actual" != "$expected" ]]; then
    printf '%s repository is not pinned to the expected commit\n' "$name" >&2
    return 1
  fi
  printf '%s clean at %s\n' "$name" "$actual"
}

check_repo "frappe" "${UPSTREAM_FRAPPE_DIR:?Set UPSTREAM_FRAPPE_DIR}" "${UPSTREAM_FRAPPE_COMMIT:-}"
check_repo "erpnext" "${UPSTREAM_ERPNEXT_DIR:?Set UPSTREAM_ERPNEXT_DIR}" "${UPSTREAM_ERPNEXT_COMMIT:-}"
