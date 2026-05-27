import pytest

from app.core.config import settings
from app.integrations.erpnext_runtime import (
    ERPNextConfigurationError,
    get_erpnext_client,
    get_erpnext_runtime_summary,
)
from app.integrations.mock_erpnext import MockERPNextClient


@pytest.fixture(autouse=True)
def restore_erpnext_settings(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(settings, "environment", "local")
    monkeypatch.setattr(settings, "erpnext_mode", None)
    monkeypatch.setattr(settings, "erpnext_mock_enabled", True)
    monkeypatch.setattr(settings, "erpnext_allow_mock_in_non_local", False)


def test_local_environment_keeps_mock_client() -> None:
    client = get_erpnext_client()
    assert isinstance(client, MockERPNextClient)


def test_production_like_environment_disables_implicit_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "production")

    with pytest.raises(ERPNextConfigurationError):
        get_erpnext_client()


def test_explicit_mock_requires_override_outside_local(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "erpnext_mode", "mock")

    with pytest.raises(ERPNextConfigurationError):
        get_erpnext_client()


def test_runtime_summary_reports_live_cutover_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "erpnext_mode", "live")

    summary = get_erpnext_runtime_summary()

    assert summary["mode"] == "live"
    assert summary["policy"] == "phase_18_cutover_required"
