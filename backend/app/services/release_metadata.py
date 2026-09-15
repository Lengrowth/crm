from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.config import settings

_SAFE_MANIFEST_KEYS = {
    "release_id",
    "control_plane_commit",
    "environment",
    "build_time_utc",
    "custom_app_version",
    "custom_app_commit",
    "installed_apps",
    "database_revision_before",
    "database_revision_after",
    "upstream_frappe_commit",
    "upstream_erpnext_commit",
    "dependency_lock_hashes",
    "feature_flags",
}


def _manifest_values() -> dict[str, Any]:
    manifest_path = (settings.release_manifest_path or "").strip()
    if not manifest_path:
        return {}

    try:
        payload = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    except (OSError, TypeError, ValueError):
        return {}

    if not isinstance(payload, dict):
        return {}
    return {key: payload[key] for key in _SAFE_MANIFEST_KEYS if key in payload}


def get_release_metadata() -> dict[str, object]:
    manifest = _manifest_values()
    return {
        "release_id": manifest.get("release_id", settings.release_id),
        "commit": manifest.get("control_plane_commit", settings.release_commit),
        "environment": manifest.get("environment", settings.normalized_environment),
        "feature_flags": settings.feature_flag_map,
        "manifest": manifest,
    }
