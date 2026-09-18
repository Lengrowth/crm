#!/usr/bin/env python3
"""Create a non-secret release manifest for a built candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--control-plane-commit", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--operator", default="ci")
    parser.add_argument("--database-revision-before", default="unknown")
    parser.add_argument("--database-revision-after", default="unknown")
    parser.add_argument("--upstream-frappe-commit", default="unknown")
    parser.add_argument("--upstream-erpnext-commit", default="unknown")
    parser.add_argument("--custom-app-version", default="not-installed")
    parser.add_argument("--custom-app-commit", default="unknown")
    parser.add_argument("--runtime-frappe-commit", default="unknown")
    parser.add_argument("--runtime-erpnext-commit", default="unknown")
    parser.add_argument("--runtime-baseline", type=Path)
    parser.add_argument("--feature-flags", default="")
    args = parser.parse_args()

    baseline = {}
    if args.runtime_baseline and args.runtime_baseline.is_file():
        try:
            baseline = json.loads(args.runtime_baseline.read_text(encoding="utf-8"))
        except (OSError, TypeError, ValueError) as exc:
            raise SystemExit(f"invalid runtime baseline: {args.runtime_baseline}: {exc}") from exc
        if not isinstance(baseline, dict) or baseline.get("schema_version") != 1:
            raise SystemExit("runtime baseline must be a JSON object with schema_version 1")

    runtime_apps = baseline.get("runtime_apps", {})
    frappe_runtime = runtime_apps.get("frappe", {}) if isinstance(runtime_apps, dict) else {}
    erpnext_runtime = runtime_apps.get("erpnext", {}) if isinstance(runtime_apps, dict) else {}
    lenerp_core_runtime = runtime_apps.get("lenerp_core", {}) if isinstance(runtime_apps, dict) else {}

    def baseline_value(current: str, *values: object, fallback: str) -> str:
        if current not in {"unknown", "not-installed"}:
            return current
        for value in values:
            if isinstance(value, str) and value:
                return value
        return fallback

    database_before = baseline_value(
        args.database_revision_before,
        baseline.get("database_revision"),
        fallback="unknown",
    )
    database_after = baseline_value(
        args.database_revision_after,
        baseline.get("database_revision"),
        fallback="unknown",
    )
    upstream_frappe = baseline_value(
        args.upstream_frappe_commit,
        baseline.get("upstream_frappe_commit"),
        fallback="unknown",
    )
    upstream_erpnext = baseline_value(
        args.upstream_erpnext_commit,
        baseline.get("upstream_erpnext_commit"),
        fallback="unknown",
    )
    runtime_frappe = baseline_value(
        args.runtime_frappe_commit,
        frappe_runtime.get("commit"),
        upstream_frappe,
        fallback="unknown",
    )
    runtime_erpnext = baseline_value(
        args.runtime_erpnext_commit,
        erpnext_runtime.get("commit"),
        upstream_erpnext,
        fallback="unknown",
    )
    custom_app_version = baseline_value(
        args.custom_app_version,
        lenerp_core_runtime.get("version"),
        fallback="not-installed",
    )
    custom_app_commit = baseline_value(
        args.custom_app_commit,
        lenerp_core_runtime.get("commit"),
        fallback="unknown",
    )

    locks = {}
    for relative_path in ("frontend/package-lock.json", "backend/pyproject.toml"):
        path = args.root / relative_path
        file_hash = sha256_file(path)
        if file_hash:
            locks[relative_path] = file_hash

    feature_flags = {}
    for item in args.feature_flags.split(","):
        if "=" not in item:
            continue
        name, value = item.split("=", 1)
        if name.strip():
            feature_flags[name.strip()] = value.strip().lower()

    installed_apps = {
        "frappe": {"commit": runtime_frappe, "upstream_commit": upstream_frappe},
        "erpnext": {"commit": runtime_erpnext, "upstream_commit": upstream_erpnext},
    }
    if custom_app_version != "not-installed" or custom_app_commit != "unknown":
        installed_apps["lenerp_core"] = {
            "version": custom_app_version,
            "commit": custom_app_commit,
        }

    manifest = {
        "release_id": args.release_id,
        "control_plane_commit": args.control_plane_commit,
        "environment": args.environment,
        "build_environment": args.environment,
        "build_time_utc": datetime.now(timezone.utc).isoformat(),
        "operator": args.operator,
        "upstream_frappe_commit": upstream_frappe,
        "upstream_erpnext_commit": upstream_erpnext,
        "custom_app_version": custom_app_version,
        "custom_app_commit": custom_app_commit,
        "installed_apps": installed_apps,
        "database_revision_before": database_before,
        "database_revision_after": database_after,
        "runtime_baseline": (
            "ops/production/release-runtime-baseline.json"
            if args.runtime_baseline
            else None
        ),
        "dependency_lock_hashes": locks,
        "feature_flags": feature_flags,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
