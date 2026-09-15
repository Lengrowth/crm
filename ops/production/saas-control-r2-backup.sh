#!/usr/bin/env bash
set -Eeuo pipefail

umask 077

ENV_FILE="${R2_BACKUP_ENV_FILE:-/etc/saas-control/r2-backup.env}"
if [[ ! -r "$ENV_FILE" ]]; then
  echo "R2 backup environment file is missing: $ENV_FILE" >&2
  exit 1
fi

# shellcheck disable=SC1090
source "$ENV_FILE"

: "${R2_ACCOUNT_ID:?R2_ACCOUNT_ID is required}"
: "${R2_ACCESS_KEY_ID:?R2_ACCESS_KEY_ID is required}"
: "${R2_SECRET_ACCESS_KEY:?R2_SECRET_ACCESS_KEY is required}"
: "${R2_BUCKET:?R2_BUCKET is required}"
: "${FRAPPE_BENCH_DIR:?FRAPPE_BENCH_DIR is required}"
: "${ERP_SITE:?ERP_SITE is required}"
: "${BACKEND_ENV_FILE:?BACKEND_ENV_FILE is required}"

R2_PREFIX="${R2_PREFIX:-automated/$(hostname -s)}"
WORK_ROOT="${R2_BACKUP_WORK_ROOT:-/var/lib/saas-control/r2-backups}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$WORK_ROOT/$RUN_ID"
ERP_BACKUP_DIR="$FRAPPE_BENCH_DIR/sites/$ERP_SITE/private/backups"
R2_ENDPOINT="https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
OBJECT_PREFIX="${R2_PREFIX%/}/$RUN_ID"

for command in aws sha256sum sqlite3 runuser; do
  command -v "$command" >/dev/null 2>&1 || {
    echo "Required command is missing: $command" >&2
    exit 1
  }
done

mkdir -p "$RUN_DIR/erp"
chmod 0700 "$WORK_ROOT" "$RUN_DIR" "$RUN_DIR/erp"
marker="$RUN_DIR/backup-started"
touch "$marker"

cleanup() {
  rm -f "$marker"
}
trap cleanup EXIT

# Load DATABASE_URL without printing the environment file. The production
# service owns this file and the backup job only uses the resulting path.
# shellcheck disable=SC1090
source "$BACKEND_ENV_FILE"
: "${DATABASE_URL:?DATABASE_URL is required in $BACKEND_ENV_FILE}"
if [[ "$DATABASE_URL" != sqlite:////* ]]; then
  echo "Only an absolute SQLite DATABASE_URL is supported by this backup job" >&2
  exit 1
fi
CONTROL_DB="${DATABASE_URL#sqlite:///}"
[[ -f "$CONTROL_DB" ]] || {
  echo "Control-plane SQLite database does not exist" >&2
  exit 1
}

echo "Creating ERP backup for $ERP_SITE"
runuser -u frappe -- bash -lc "cd '$FRAPPE_BENCH_DIR' && bench --site '$ERP_SITE' backup --with-files"

mapfile -t ERP_FILES < <(find "$ERP_BACKUP_DIR" -maxdepth 1 -type f -newer "$marker" -print | sort)
if (( ${#ERP_FILES[@]} < 4 )); then
  echo "Expected database, site-config, public-files, and private-files backups; found ${#ERP_FILES[@]}" >&2
  exit 1
fi

for source_file in "${ERP_FILES[@]}"; do
  cp -- "$source_file" "$RUN_DIR/erp/"
done

# sqlite3 .backup produces a consistent snapshot while the application is live.
sqlite3 "$CONTROL_DB" ".backup '$RUN_DIR/saas_control.db'"

manifest="$RUN_DIR/manifest.sha256"
(
  cd "$RUN_DIR"
  find erp -maxdepth 1 -type f -printf '%P\n' | sort | xargs -r sha256sum
  sha256sum saas_control.db
) > "$manifest"

export AWS_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="auto"
export AWS_EC2_METADATA_DISABLED="true"

upload() {
  local source_file="$1"
  local object_name="$2"
  aws s3 cp "$source_file" "s3://$R2_BUCKET/$OBJECT_PREFIX/$object_name" \
    --endpoint-url "$R2_ENDPOINT" --only-show-errors
}

for source_file in "$RUN_DIR"/erp/* "$RUN_DIR/saas_control.db" "$manifest"; do
  upload "$source_file" "$(basename "$source_file")"
done

# Download each object once and compare its digest with the local manifest.
verify_dir="$RUN_DIR/verified"
mkdir -p "$verify_dir"
while read -r expected_hash relative_name; do
  remote_file="$verify_dir/$(basename "$relative_name")"
  aws s3 cp "s3://$R2_BUCKET/$OBJECT_PREFIX/$relative_name" "$remote_file" \
    --endpoint-url "$R2_ENDPOINT" --only-show-errors
  actual_hash="$(sha256sum "$remote_file" | awk '{print $1}')"
  [[ "$actual_hash" == "$expected_hash" ]] || {
    echo "R2 hash verification failed for $relative_name" >&2
    exit 1
  }
done < "$manifest"

echo "R2 backup and byte-hash verification passed: $OBJECT_PREFIX"
