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
    parser.add_argument("--feature-flags", default="")
    args = parser.parse_args()

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
        "frappe": {"commit": args.upstream_frappe_commit},
        "erpnext": {"commit": args.upstream_erpnext_commit},
    }
    if args.custom_app_version != "not-installed" or args.custom_app_commit != "unknown":
        installed_apps["lenerp_core"] = {
            "version": args.custom_app_version,
            "commit": args.custom_app_commit,
        }

    manifest = {
        "release_id": args.release_id,
        "control_plane_commit": args.control_plane_commit,
        "environment": args.environment,
        "build_time_utc": datetime.now(timezone.utc).isoformat(),
        "operator": args.operator,
        "upstream_frappe_commit": args.upstream_frappe_commit,
        "upstream_erpnext_commit": args.upstream_erpnext_commit,
        "custom_app_version": args.custom_app_version,
        "custom_app_commit": args.custom_app_commit,
        "installed_apps": installed_apps,
        "database_revision_before": args.database_revision_before,
        "database_revision_after": args.database_revision_after,
        "dependency_lock_hashes": locks,
        "feature_flags": feature_flags,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
