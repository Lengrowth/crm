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
GITHUB_TOKEN="$GITHUB_TOKEN" python3 - "$RELEASE_ID" "$STAGING_RUN_ID" "$GITHUB_REPOSITORY" "$ARTIFACT_ROOT" <<'PY'
import json
import os
import sys
import urllib.request
import urllib.parse
import zipfile

release_id, run_id, repository, artifact_root = sys.argv[1:]
token = os.environ["GITHUB_TOKEN"]
base = f"https://api.github.com/repos/{repository}"

def get_json(url):
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)

class GitHubRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        redirected = super().redirect_request(request, fp, code, msg, headers, newurl)
        if redirected is not None:
            old_host = urllib.parse.urlparse(request.full_url).hostname
            new_host = urllib.parse.urlparse(newurl).hostname
            if new_host in {"api.github.com", "github.com"} and old_host in {"api.github.com", "github.com"}:
                redirected.add_unredirected_header("Authorization", f"Bearer {token}")
            else:
                redirected.headers.pop("Authorization", None)
        return redirected

run = get_json(f"{base}/actions/runs/{run_id}")
if run.get("status") != "completed" or run.get("conclusion") != "success":
    raise SystemExit(f"staging run {run_id} is not a successful completed run")
if (run.get("name") or run.get("workflowName")) != "Build and deploy SaaS control plane to staging":
    raise SystemExit("staging run is not the protected staging workflow")

artifacts = get_json(f"{base}/actions/runs/{run_id}/artifacts").get("artifacts", [])
name = f"staging-browser-evidence-{release_id}"
artifact = next((item for item in artifacts if item.get("name") == name and not item.get("expired")), None)
if artifact is None:
    raise SystemExit("the exact staging evidence artifact is unavailable or expired")
request = urllib.request.Request(artifact["archive_download_url"], headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
opener = urllib.request.build_opener(GitHubRedirectHandler)
with opener.open(request, timeout=120) as response:
    archive = response.read()
archive_path = os.path.join(artifact_root, "evidence.zip")
with open(archive_path, "wb") as handle:
    handle.write(archive)
with zipfile.ZipFile(archive_path) as archive_file:
    root = os.path.realpath(artifact_root)
    for member in archive_file.infolist():
        target = os.path.realpath(os.path.join(artifact_root, member.filename))
        if target != root and not target.startswith(root + os.sep):
            raise SystemExit("staging evidence archive contains an unsafe path")
    archive_file.extractall(artifact_root)
os.unlink(archive_path)
PY

manifest="$(find "$ARTIFACT_ROOT" -type f -name candidate-bound-evidence-manifest.json -print -quit)"
runtime="$(find "$ARTIFACT_ROOT" -type f -path '*/erp/phase02-runtime-readback.json' -print -quit)"
cleanup="$(find "$ARTIFACT_ROOT" -type f -name phase2-cleanup.json -print -quit)"
[[ -s "$manifest" && -s "$runtime" && -s "$cleanup" ]] || {
  echo "Phase 02 staging artifact is missing required evidence files" >&2
  exit 1
}

MANIFEST="$manifest" RUNTIME="$runtime" CLEANUP="$cleanup" ARTIFACT_ROOT="$ARTIFACT_ROOT" python3 - "$RELEASE_ID" "$STAGING_RUN_ID" <<'PY'
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
bound_runtime = manifest.get("runtime_readback")
if not isinstance(bound_runtime, dict) or bound_runtime.get("commit") != release_id or bound_runtime.get("release_id") != release_id:
    raise SystemExit("runtime readback is not bound to the exact candidate")
if bound_runtime.get("environment") != "staging" or not runtime.get("provider_verified"):
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
release_manifest = manifest.get("release_manifest")
if not isinstance(release_manifest, dict):
    raise SystemExit("staging evidence does not contain the candidate release manifest")
if release_manifest.get("control_plane_commit") != release_id or release_manifest.get("environment") != "staging":
    raise SystemExit("candidate release manifest is not bound to the exact staging candidate")
lenerp = (release_manifest.get("installed_apps") or {}).get("lenerp_core") or {}
if lenerp.get("commit") != "8d77cec7504d22f9c0a235034777e31fa07fc62" or lenerp.get("version") != "0.2.0":
    raise SystemExit("candidate release manifest does not contain the approved exact LenERP application")
with open(os.path.join(os.environ["ARTIFACT_ROOT"], "phase2-release-manifest.json"), "w", encoding="utf-8") as handle:
    json.dump(release_manifest, handle, indent=2, sort_keys=True)
    handle.write("\n")
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
  # Keep the immutable staging candidate's runtime dependencies (including
  # frontend/node_modules) without duplicating their bytes on the shared
  # release volume. The staging and production release roots are on the same
  # deployment volume; hardlinks preserve rollback safety because cleanup of
  # the staging directory only removes its directory entries. The staging
  # service owns the source tree, so use the workflow's non-interactive sudo
  # path for protected hardlink creation, then restore release ownership.
  sudo -n cp -al -- "$source_candidate" "$incoming"
  sudo -n chown -R "$(id -u):$(id -g)" "$incoming"
  printf 'candidate_sha=%s\nstaging_run_id=%s\n' "$RELEASE_ID" "$STAGING_RUN_ID" > "$incoming/.phase2-staging-evidence-verified"
  mv -T -- "$incoming" "$target_candidate"
  trap - EXIT
fi
# The protected staging runtime readback is the authoritative candidate-bound
# release identity. Reinstall it into the production copy so materialization
# cannot silently retain a stale/incomplete manifest from the staging slot.
authoritative_manifest="$ARTIFACT_ROOT/phase2-release-manifest.json"
[[ -s "$authoritative_manifest" ]] || { echo "candidate-bound release manifest is missing" >&2; exit 1; }
manifest_tmp="$target_candidate/.release-manifest.phase2.$$"
install -m 0644 "$authoritative_manifest" "$manifest_tmp"
mv -f -- "$manifest_tmp" "$target_candidate/release-manifest.json"
printf 'candidate_sha=%s\nstaging_run_id=%s\n' "$RELEASE_ID" "$STAGING_RUN_ID" > "$target_candidate/.phase2-staging-evidence-verified"
echo "Phase 02 candidate materialized: $RELEASE_ID (staging run $STAGING_RUN_ID)"
