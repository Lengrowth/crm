#!/usr/bin/env bash
set -Eeuo pipefail

BACKUP_DIR="${1:?Usage: verify_backup_manifest.sh <backup-dir>}"
MANIFEST="$BACKUP_DIR/manifest.sha256"

[[ -d "$BACKUP_DIR" && -s "$MANIFEST" ]] || {
  echo "backup manifest or directory is missing" >&2
  exit 1
}

while read -r expected_hash relative_name; do
  [[ "$expected_hash" =~ ^[0-9a-fA-F]{64}$ && -n "$relative_name" ]] || {
    echo "invalid backup manifest entry" >&2
    exit 1
  }
  candidate="$BACKUP_DIR/$relative_name"
  if [[ ! -f "$candidate" && "$relative_name" != */* && -f "$BACKUP_DIR/erp/$relative_name" ]]; then
    candidate="$BACKUP_DIR/erp/$relative_name"
  fi
  [[ -f "$candidate" ]] || {
    echo "backup manifest file is missing: $relative_name" >&2
    exit 1
  }
  actual_hash="$(sha256sum "$candidate" | awk '{print $1}')"
  [[ "$actual_hash" == "$expected_hash" ]] || {
    echo "backup manifest hash mismatch: $relative_name" >&2
    exit 1
  }
done < "$MANIFEST"

echo "Verified backup manifest: $BACKUP_DIR"
