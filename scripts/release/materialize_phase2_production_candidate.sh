#!/usr/bin/env bash
set -Eeuo pipefail

# Phase 02-only materializer. The general production materializer has a Phase
# 04 evidence prerequisite and is intentionally not used here.
RELEASE_ID="${RELEASE_ID:?Set RELEASE_ID to the exact staging candidate}"
STAGING_RUN_ID="${STAGING_RUN_ID:?Set STAGING_RUN_ID to the protected staging run}"
GITHUB_REPOSITORY="${GITHUB_REPOSITORY:?Set GITHUB_REPOSITORY}"
GITHUB_TOKEN="${GITHUB_TOKEN:?Set GITHUB_TOKEN}"
STAGING_ROOT="${STAGING_RELEASE_ROOT:-/opt/saas-control-staging/releases}"
PRODUCTION_ROOT="${PRODUCTION_RELEASE_ROOT:-/opt/saas-control/releases}"
ARTIFACT_ROOT="${ARTIFACT_ROOT:-${RUNNER_TEMP:-/tmp}/phase2-staging-evidence-${RELEASE_ID}-${STAGING_RUN_ID}}"

[[ "$RELEASE_ID" =~ ^[0-9a-f]{40}$ ]] || { echo "RELEASE_ID must be a full lowercase commit SHA" >&2; exit 1; }
[[ "$STAGING_RUN_ID" =~ ^[0-9]+$ ]] || { echo "STAGING_RUN_ID must be numeric" >&2; exit 1; }
case "$ARTIFACT_ROOT" in */phase2-staging-evidence-*) ;; *) echo "unsafe artifact path" >&2; exit 1 ;; esac

rm -rf -- "$ARTIFACT_ROOT"
mkdir -p -- "$ARTIFACT_ROOT"
export GH_TOKEN="$GITHUB_TOKEN"

run_json="$(gh run view "$STAGING_RUN_ID" --repo "$GITHUB_REPOSITORY" --json status,conclusion,workflowName,event -q '.')"
RUN_JSON="$run_json" python3 - "$RELEASE_ID" "$STAGING_RUN_ID" <<'PY'
import json
import os
import sys

release_id, run_id = sys.argv[1:]
run = json.loads(os.environ["RUN_JSON"])
if run.get("status") != "completed" or run.get("conclusion") != "success":
    raise SystemExit(f"staging run {run_id} is not a successful completed run")
if run.get("workflowName") != "Build and deploy SaaS control plane to staging":
    raise SystemExit("staging run is not the protected staging workflow")
PY

gh run download "$STAGING_RUN_ID" --repo "$GITHUB_REPOSITORY" \
  --name "staging-browser-evidence-$RELEASE_ID" --dir "$ARTIFACT_ROOT"

manifest="$(find "$ARTIFACT_ROOT" -type f -name candidate-bound-evidence-manifest.json -print -quit)"
runtime="$(find "$ARTIFACT_ROOT" -type f -path '*/erp/phase02-runtime-readback.json' -print -quit)"
cleanup="$(find "$ARTIFACT_ROOT" -type f -name phase2-cleanup.json -print -quit)"
[[ -s "$manifest" && -s "$runtime" && -s "$cleanup" ]] || {
  echo "Phase 02 staging artifact is missing required evidence files" >&2
  exit 1
}

MANIFEST="$manifest" RUNTIME="$runtime" CLEANUP="$cleanup" python3 - "$RELEASE_ID" "$STAGING_RUN_ID" <<'PY'
import json
import os
import sys

release_id, run_id = sys.argv[1:]
with open(os.environ["MANIFEST"], encoding="utf-8") as handle:
    manifest = json.load(handle)
with open(os.environ["RUNTIME"], encoding="utf-8") as handle:
    runtime = json.load(handle)
with open(os.environ["CLEANUP"], encoding="utf-8") as handle:
    cleanup = json.load(handle)

if manifest.get("candidate_sha") != release_id:
    raise SystemExit("staging evidence candidate does not match release id")
if manifest.get("workflow_run_id") != int(run_id):
    raise SystemExit("staging evidence run does not match requested staging run")
if runtime.get("commit") != release_id or runtime.get("release_id") != release_id:
    raise SystemExit("runtime readback is not bound to the exact candidate")
if runtime.get("environment") != "staging" or not runtime.get("provider_verified"):
    raise SystemExit("runtime readback is not a verified staging readback")
if runtime.get("hrms_commit") != "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1":
    raise SystemExit("staging HRMS commit is not the approved exact revision")
if runtime.get("hrms_version") != "15.64.1":
    raise SystemExit("staging HRMS version is not the approved exact revision")
if not {"frappe", "erpnext", "hrms", "lenerp_core"}.issubset(set(runtime.get("installed_apps", []))):
    raise SystemExit("staging installed-app readback is incomplete")
if not {"HR User", "HR Manager"}.issubset(set(runtime.get("roles", []))):
    raise SystemExit("staging HR role readback is incomplete")
if not {"HR", "Payroll"}.issubset({item.get("name") for item in runtime.get("workspaces", [])}):
    raise SystemExit("staging HR/Payroll workspace readback is incomplete")
if not runtime.get("backup_dir", "").startswith("/opt/saas-control-staging/shared/backups/"):
    raise SystemExit("staging backup path is not protected")
if not isinstance(cleanup.get("organization_ids"), list) or not isinstance(cleanup.get("tenant_ids"), list):
    raise SystemExit("Phase 02 cleanup evidence is incomplete")
PY

source_candidate="$STAGING_ROOT/$RELEASE_ID"
target_candidate="$PRODUCTION_ROOT/$RELEASE_ID"
[[ -f "$source_candidate/.candidate-complete" ]] || { echo "staging candidate is incomplete" >&2; exit 1; }
[[ -s "$source_candidate/.staging-smoke-passed" ]] || { echo "staging smoke marker is missing" >&2; exit 1; }
grep -Fxq "$RELEASE_ID" "$source_candidate/.staging-smoke-passed" || { echo "staging smoke marker mismatch" >&2; exit 1; }

if [[ ! -e "$target_candidate" ]]; then
  mkdir -p -- "$PRODUCTION_ROOT"
  incoming="$PRODUCTION_ROOT/.${RELEASE_ID}.phase2-incoming.$$"
  trap 'rm -rf -- "$incoming"' EXIT
  cp -a -- "$source_candidate" "$incoming"
  printf 'candidate_sha=%s\nstaging_run_id=%s\n' "$RELEASE_ID" "$STAGING_RUN_ID" > "$incoming/.phase2-staging-evidence-verified"
  mv -T -- "$incoming" "$target_candidate"
  trap - EXIT
fi
printf 'candidate_sha=%s\nstaging_run_id=%s\n' "$RELEASE_ID" "$STAGING_RUN_ID" > "$target_candidate/.phase2-staging-evidence-verified"
echo "Phase 02 candidate materialized: $RELEASE_ID (staging run $STAGING_RUN_ID)"
