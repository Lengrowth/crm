from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_runtime_release_exposes_identity_and_server_flags(monkeypatch, tmp_path) -> None:
    manifest_path = tmp_path / "release-manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "release_id": "PLAT-P0-test",
                "control_plane_commit": "abc123",
                "environment": "staging",
                "custom_app_version": "0.1.0",
                "custom_app_commit": "custom-commit",
                "upstream_frappe_commit": "frappe-commit",
                "upstream_erpnext_commit": "erpnext-commit",
                "installed_apps": {
                    "frappe": {"commit": "frappe-commit"},
                    "erpnext": {"commit": "erpnext-commit"},
                    "lenerp_core": {"version": "0.1.0", "commit": "custom-commit"},
                },
                "feature_flags": {"future_menu": False},
                "secret_value": "must-not-be-exposed",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(settings, "release_manifest_path", str(manifest_path))
    monkeypatch.setattr(settings, "release_id", "fallback")
    monkeypatch.setattr(settings, "release_commit", "fallback-commit")
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "feature_flags", "future_menu=off,new_flow=on")

    response = TestClient(app).get("/runtime/release")

    assert response.status_code == 200
    payload = response.json()
    assert payload["release_id"] == "PLAT-P0-test"
    assert payload["commit"] == "abc123"
    assert payload["environment"] == "staging"
    assert payload["feature_flags"] == {"future_menu": False, "new_flow": True}
    assert payload["manifest"]["installed_apps"]["lenerp_core"]["version"] == "0.1.0"
    assert "secret_value" not in payload["manifest"]


def test_runtime_environment_is_server_controlled_not_build_manifest(monkeypatch, tmp_path) -> None:
    manifest_path = tmp_path / "release-manifest.json"
    manifest_path.write_text(
        json.dumps({"release_id": "candidate", "control_plane_commit": "abc", "environment": "staging", "build_environment": "staging"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(settings, "release_manifest_path", str(manifest_path))
    monkeypatch.setattr(settings, "environment", "production")

    response = TestClient(app).get("/runtime/release")

    assert response.status_code == 200
    assert response.json()["environment"] == "production"
    assert response.json()["manifest"]["build_environment"] == "staging"
