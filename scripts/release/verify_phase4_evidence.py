#!/usr/bin/env python3
"""Verify immutable, candidate-bound Phase 4 staging evidence."""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from typing import Any


WORKFLOW_FILE = ".github/workflows/deploy-saas-control.yml"
EVIDENCE_ARTIFACT_PREFIX = "phase4-synthetic-evidence-"
EVIDENCE_VERSION = 2


def parse_timestamp(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def run_timestamp(run: dict[str, Any], key: str) -> datetime:
    value = run.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"workflow run is missing {key}")
    return parse_timestamp(value)


def run_completed_before_promotion(run: dict[str, Any], promotion_time: datetime) -> bool:
    return (
        run_timestamp(run, "run_started_at") <= promotion_time
        and run_timestamp(run, "updated_at") <= promotion_time
    )


def evidence_passed(payload: dict[str, Any], *, recovery: bool) -> bool:
    cleanup = payload.get("cleanup")
    return (
        payload.get("status") == "passed"
        and payload.get("state") == "ready"
        and payload.get("worker_status") == "success"
        and payload.get("step_count") == 15
        and isinstance(cleanup, dict)
        and cleanup.get("status", "passed") != "failed"
        and cleanup.get("external_site_cleanup_verified") is True
        and cleanup.get("external_site_deleted") == 1
        and (not recovery or payload.get("recovery_run") is True)
    )


def metadata_matches(metadata: dict[str, Any], *, release_id: str, run: dict[str, Any]) -> bool:
    return (
        metadata.get("evidence_version") == EVIDENCE_VERSION
        and metadata.get("candidate_sha") == release_id
        and str(metadata.get("staging_run_id")) == str(run.get("id"))
        and metadata.get("workflow_file") == WORKFLOW_FILE
        and metadata.get("success_evidence_file") == "phase4-synthetic-evidence.json"
        and metadata.get("recovery_evidence_file") == "phase4-synthetic-recovery-evidence.json"
    )


def _request(url: str, token: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "LenERP-production-phase4-gate/2.0",
        },
    )


def read_json(url: str, token: str) -> dict[str, Any]:
    with urllib.request.urlopen(_request(url, token), timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("GitHub API returned a non-object payload")
    return payload


def read_artifact(artifact: dict[str, Any], token: str) -> dict[str, Any]:
    with urllib.request.urlopen(_request(artifact["archive_download_url"], token), timeout=60) as response:
        archive = response.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        files = {name.rsplit("/", 1)[-1]: name for name in bundle.namelist()}
        required = {
            "phase4-synthetic-evidence.json",
            "phase4-synthetic-recovery-evidence.json",
            "phase4-synthetic-evidence-metadata.json",
        }
        missing = required.difference(files)
        if missing:
            raise ValueError(f"evidence artifact is missing {', '.join(sorted(missing))}")
        return {name: json.loads(bundle.read(files[name])) for name in required}


def list_workflow_runs(api: str, repository: str, token: str) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for page in range(1, 11):
        query = urllib.parse.urlencode({"per_page": 100, "page": page})
        payload = read_json(
            f"{api}/repos/{repository}/actions/workflows/{WORKFLOW_FILE.split('/')[-1]}/runs?{query}",
            token,
        )
        page_runs = payload.get("workflow_runs", [])
        if not isinstance(page_runs, list):
            raise ValueError("GitHub API returned invalid workflow_runs")
        runs.extend(item for item in page_runs if isinstance(item, dict))
        if len(page_runs) < 100:
            break
    return runs


def verify(
    *,
    release_id: str,
    repository: str,
    token: str,
    promotion_run_id: str,
    promotion_requested_at: str | None = None,
    api_url: str = "https://api.github.com",
) -> str:
    if not release_id or len(release_id) != 40 or any(char not in "0123456789abcdef" for char in release_id):
        raise ValueError("release ID must be a full lowercase 40-character commit SHA")
    if not repository or not token or not promotion_run_id:
        raise ValueError("repository, token, and promotion run ID are required")

    api = api_url.rstrip("/")
    if promotion_requested_at:
        promotion_time = parse_timestamp(promotion_requested_at)
    else:
        promotion_run = read_json(f"{api}/repos/{repository}/actions/runs/{promotion_run_id}", token)
        promotion_time = run_timestamp(promotion_run, "created_at")

    candidates = sorted(
        list_workflow_runs(api, repository, token),
        key=lambda item: item.get("created_at", ""),
        reverse=True,
    )
    later_matching_run_seen = False
    for run in candidates:
        if str(run.get("id")) == str(promotion_run_id):
            continue
        if run.get("conclusion") != "success":
            continue
        if run.get("path") not in (None, WORKFLOW_FILE):
            continue
        if not run_completed_before_promotion(run, promotion_time):
            later_matching_run_seen = True
            continue

        artifacts = read_json(
            f"{api}/repos/{repository}/actions/runs/{run['id']}/artifacts?per_page=100", token
        ).get("artifacts", [])
        if not isinstance(artifacts, list):
            continue
        artifact = next(
            (
                item
                for item in artifacts
                if isinstance(item, dict)
                and item.get("name") == f"{EVIDENCE_ARTIFACT_PREFIX}{run['id']}"
                and not item.get("expired")
            ),
            None,
        )
        if artifact is None:
            continue
        try:
            evidence = read_artifact(artifact, token)
        except (KeyError, OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile):
            continue
        metadata = evidence["phase4-synthetic-evidence-metadata.json"]
        success = evidence["phase4-synthetic-evidence.json"]
        recovery = evidence["phase4-synthetic-recovery-evidence.json"]
        if not isinstance(metadata, dict) or not isinstance(success, dict) or not isinstance(recovery, dict):
            continue
        if not metadata_matches(metadata, release_id=release_id, run=run):
            continue
        if not evidence_passed(success, recovery=False) or not evidence_passed(recovery, recovery=True):
            continue
        print(run["id"])
        return str(run["id"])

    suffix = (
        " A later matching run was ignored because it started or completed after the promotion request."
        if later_matching_run_seen
        else ""
    )
    raise ValueError(
        "no candidate-bound successful Phase 4 success-and-recovery evidence existed "
        f"before the promotion request.{suffix}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    parser.add_argument("--promotion-run-id", default=os.environ.get("PROMOTION_RUN_ID", ""))
    parser.add_argument("--promotion-requested-at", default=os.environ.get("PROMOTION_REQUESTED_AT"))
    parser.add_argument("--api-url", default=os.environ.get("GITHUB_API_URL", "https://api.github.com"))
    args = parser.parse_args()
    try:
        verify(
            release_id=args.release_id,
            repository=args.repository,
            token=args.token,
            promotion_run_id=args.promotion_run_id,
            promotion_requested_at=args.promotion_requested_at,
            api_url=args.api_url,
        )
    except Exception as exc:  # never print request URLs or credentials
        print(f"Phase 4 staging evidence verification failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
