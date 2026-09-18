import pytest

from app.core.config import settings
from app.integrations.frappe_bench import FrappeBenchERPNextClient
from app.integrations.erpnext.http import ERPNextHTTPClient
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
    monkeypatch.setattr(settings, "erpnext_base_url", None)
    monkeypatch.setattr(settings, "erpnext_api_key", None)
    monkeypatch.setattr(settings, "erpnext_api_secret", None)


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


def test_staging_bench_passes_database_admin_username(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "erpnext_mode", "bench")
    monkeypatch.setattr(settings, "erpnext_bench_root", str(tmp_path))
    monkeypatch.setattr(settings, "erpnext_db_root_username", "saas_phase4_bench")
    monkeypatch.setattr(settings, "erpnext_db_root_password", "staging-secret")

    client = get_erpnext_client()

    assert isinstance(client, FrappeBenchERPNextClient)
    assert client.db_root_username == "saas_phase4_bench"
    assert client.db_root_password == "staging-secret"


def test_live_mode_returns_http_client_when_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "production")
    monkeypatch.setattr(settings, "erpnext_mode", "live")
    monkeypatch.setattr(settings, "erpnext_base_url", "https://demo-erp.lenquant.com")
    monkeypatch.setattr(settings, "erpnext_api_key", "key")
    monkeypatch.setattr(settings, "erpnext_api_secret", "secret")

    client = get_erpnext_client()

    assert isinstance(client, ERPNextHTTPClient)
    assert client.base_url == "https://demo-erp.lenquant.com"


def test_live_mode_requires_explicit_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "erpnext_mode", "live")

    with pytest.raises(ERPNextConfigurationError):
        get_erpnext_client()


def test_runtime_summary_reports_active_live_cutover(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "erpnext_mode", "live")
    monkeypatch.setattr(
        settings, "erpnext_base_url", "https://demo-erp.lenquant.com/api"
    )
    monkeypatch.setattr(settings, "erpnext_api_key", "key")
    monkeypatch.setattr(settings, "erpnext_api_secret", "secret")

    summary = get_erpnext_runtime_summary()

    assert summary["mode"] == "live"
    assert summary["policy"] == "live_cutover_active"
    assert summary["target"] == "https://demo-erp.lenquant.com"
    assert summary["auth_mode"] == "token"


def test_runtime_summary_reports_invalid_live_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(settings, "environment", "staging")
    monkeypatch.setattr(settings, "erpnext_mode", "live")

    summary = get_erpnext_runtime_summary()

    assert summary["mode"] == "invalid"
    assert summary["policy"] == "configuration_error"
