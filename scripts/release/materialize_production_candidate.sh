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

if [[ -e "$TARGET_CANDIDATE" ]]; then
  [[ -f "$TARGET_CANDIDATE/.candidate-complete" ]] || {
    echo "Production candidate path exists without completion marker: $TARGET_CANDIDATE" >&2
    exit 1
  }
  echo "Reusing immutable production candidate $TARGET_CANDIDATE"
  exit 0
fi

verify_remote_phase4_evidence() {
  [[ -n "${GITHUB_REPOSITORY:-}" && -n "${GITHUB_TOKEN:-}" ]] || {
    echo "Separate production hosts require GitHub Actions credentials to verify the tested staging artifact." >&2
    return 1
  }
  RELEASE_ID="$RELEASE_ID" python3 - <<'PY'
import io
import json
import os
import sys
import urllib.request
import zipfile

release_id = os.environ["RELEASE_ID"]
repo = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
api = os.environ.get("GITHUB_API_URL", "https://api.github.com").rstrip("/")


def read_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "LenERP-production-materializer/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def evidence_passed(payload: dict, recovery: bool) -> bool:
    cleanup = payload.get("cleanup")
    return (
        payload.get("status") == "passed"
        and isinstance(cleanup, dict)
        and cleanup.get("status", "passed") != "failed"
        and (not recovery or payload.get("recovery_run") is True)
    )


try:
    runs = read_json(
        f"{api}/repos/{repo}/actions/workflows/deploy-saas-control.yml/runs"
        f"?head_sha={release_id}&status=success&per_page=100"
    ).get("workflow_runs", [])
    runs = sorted(runs, key=lambda item: item.get("created_at", ""), reverse=True)
    for run in runs:
        if run.get("head_sha") != release_id or run.get("conclusion") != "success":
            continue
        artifacts = read_json(
            f"{api}/repos/{repo}/actions/runs/{run['id']}/artifacts?per_page=100"
        ).get("artifacts", [])
        artifact = next(
            (
                item
                for item in artifacts
                if item.get("name", "").startswith("phase4-synthetic-evidence-")
                and not item.get("expired")
            ),
            None,
        )
        if artifact is None:
            continue
        request = urllib.request.Request(
            artifact["archive_download_url"],
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "LenERP-production-materializer/1.0",
            },
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            archive = response.read()
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            files = {name.rsplit("/", 1)[-1]: name for name in bundle.namelist()}
            success = json.loads(bundle.read(files["phase4-synthetic-evidence.json"]))
            recovery = json.loads(bundle.read(files["phase4-synthetic-recovery-evidence.json"]))
        if evidence_passed(success, False) and evidence_passed(recovery, True):
            print(run["id"])
            raise SystemExit(0)
    raise RuntimeError("no successful exact-candidate Phase 4 staging artifact was found")
except Exception as exc:
    print(f"Phase 4 staging evidence verification failed: {type(exc).__name__}", file=sys.stderr)
    raise SystemExit(1)
PY
}

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
  verify_remote_phase4_evidence >/tmp/saas-control-phase4-evidence-run-id
  git -C "$SOURCE_REPO" fetch --no-tags --depth=1 origin "$RELEASE_ID"
  git -C "$SOURCE_REPO" cat-file -e "$RELEASE_ID^{commit}"
  RELEASE_ROOT="$PRODUCTION_ROOT" \
    TARGET_REF="$RELEASE_ID" \
    RELEASE_ID="$RELEASE_ID" \
    DEPLOY_TARGET=staging \
    SOURCE_REPO="$SOURCE_REPO" \
    bash "$SOURCE_REPO/scripts/release/build_candidate.sh" >/dev/null
  printf '%s\n' "$RELEASE_ID" > "$TARGET_CANDIDATE/.staging-smoke-passed"
  echo "Materialized exact tested candidate from commit $RELEASE_ID (staging run $(cat /tmp/saas-control-phase4-evidence-run-id))"
  rm -f -- /tmp/saas-control-phase4-evidence-run-id
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
