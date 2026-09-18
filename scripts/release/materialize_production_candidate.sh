#!/usr/bin/env bash
set -euo pipefail

RELEASE_ID="${RELEASE_ID:?Set RELEASE_ID to the exact tested staging candidate}"
SOURCE_REPO="${SOURCE_REPO:-${GITHUB_WORKSPACE:-$PWD}}"
STAGING_ROOT="${STAGING_RELEASE_ROOT:-/opt/saas-control-staging/releases}"
PRODUCTION_ROOT="${PRODUCTION_RELEASE_ROOT:-/opt/saas-control/releases}"
SOURCE_CANDIDATE="$STAGING_ROOT/$RELEASE_ID"
TARGET_CANDIDATE="$PRODUCTION_ROOT/$RELEASE_ID"

case "$SOURCE_CANDIDATE" in "$STAGING_ROOT"/*) ;; *) exit 1 ;; esac
case "$TARGET_CANDIDATE" in "$PRODUCTION_ROOT"/*) ;; *) exit 1 ;; esac

verify_remote_phase4_evidence() {
  [[ -n "${GITHUB_REPOSITORY:-}" && -n "${GITHUB_TOKEN:-}" ]] || {
    echo "Separate production hosts require GitHub Actions credentials to verify the tested staging artifact." >&2
    return 1
  }
  PROMOTION_RUN_ID="${PROMOTION_RUN_ID:-${GITHUB_RUN_ID:-}}" \
    python3 "$SOURCE_REPO/scripts/release/verify_phase4_evidence.py" \
      --release-id "$RELEASE_ID" \
      --repository "$GITHUB_REPOSITORY" \
      --token "$GITHUB_TOKEN"
}

# Verify before either the existing-candidate path or the build/copy path.
# A generic smoke marker is never sufficient Phase 4 evidence.
phase4_evidence_run_id="$(verify_remote_phase4_evidence)"

if [[ -e "$TARGET_CANDIDATE" ]]; then
  [[ -f "$TARGET_CANDIDATE/.candidate-complete" ]] || {
    echo "Production candidate path exists without completion marker: $TARGET_CANDIDATE" >&2
    exit 1
  }
  printf 'candidate_sha=%s\nevidence_run_id=%s\n' "$RELEASE_ID" "$phase4_evidence_run_id" > "$TARGET_CANDIDATE/.phase4-synthetic-evidence-verified"
  echo "Reusing immutable production candidate $TARGET_CANDIDATE after Phase 4 evidence run $phase4_evidence_run_id"
  exit 0
fi

if [[ -f "$SOURCE_CANDIDATE/.candidate-complete" ]]; then
  [[ -s "$SOURCE_CANDIDATE/.staging-smoke-passed" ]] || {
    echo "Tested staging candidate has no smoke marker: $SOURCE_CANDIDATE" >&2
    exit 1
  }
  grep -Fxq "$RELEASE_ID" "$SOURCE_CANDIDATE/.staging-smoke-passed" || {
    echo "Staging smoke marker does not match RELEASE_ID" >&2
    exit 1
  }
else
  git -C "$SOURCE_REPO" fetch --no-tags --depth=1 origin "$RELEASE_ID"
  git -C "$SOURCE_REPO" cat-file -e "$RELEASE_ID^{commit}"
  RELEASE_ROOT="$PRODUCTION_ROOT" \
    TARGET_REF="$RELEASE_ID" \
    RELEASE_ID="$RELEASE_ID" \
    DEPLOY_TARGET=staging \
    SOURCE_REPO="$SOURCE_REPO" \
    bash "$SOURCE_REPO/scripts/release/build_candidate.sh" >/dev/null
  printf '%s\n' "$RELEASE_ID" > "$TARGET_CANDIDATE/.staging-smoke-passed"
  printf 'candidate_sha=%s\nevidence_run_id=%s\n' "$RELEASE_ID" "$phase4_evidence_run_id" > "$TARGET_CANDIDATE/.phase4-synthetic-evidence-verified"
  echo "Materialized exact tested candidate from commit $RELEASE_ID (staging run $phase4_evidence_run_id)"
  exit 0
fi

mkdir -p "$PRODUCTION_ROOT"
temporary_candidate="$PRODUCTION_ROOT/.${RELEASE_ID}.incoming.$$"
cleanup() { rm -rf -- "$temporary_candidate"; }
trap cleanup EXIT
cp -a "$SOURCE_CANDIDATE" "$temporary_candidate"
printf 'candidate_sha=%s\nevidence_run_id=%s\n' "$RELEASE_ID" "$phase4_evidence_run_id" > "$temporary_candidate/.phase4-synthetic-evidence-verified"
mv -T "$temporary_candidate" "$TARGET_CANDIDATE"
trap - EXIT
echo "Materialized tested staging candidate at $TARGET_CANDIDATE"
