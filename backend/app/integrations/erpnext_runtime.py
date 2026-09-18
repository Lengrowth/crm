from __future__ import annotations

import logging
from typing import Literal, Optional
from urllib.parse import urlparse

from app.core.config import settings
from app.integrations.frappe_bench import FrappeBenchERPNextClient
from app.integrations.erpnext.http import ERPNextHTTPClient
from app.integrations.erpnext_client import ERPNextClient
from app.integrations.mock_erpnext import MockERPNextClient

logger = logging.getLogger(__name__)

ERPNextMode = Literal["mock", "live", "bench", "disabled"]


class ERPNextConfigurationError(RuntimeError):
    """Raised when ERPNext integration mode is unsafe or unavailable."""


def _normalize_mode(mode: Optional[str]) -> Optional[ERPNextMode]:
    if mode is None:
        return None

    normalized = mode.strip().lower()
    if normalized == "mock":
        return "mock"
    if normalized == "live":
        return "live"
    if normalized in {"bench", "staging_bench"}:
        return "bench"
    if normalized == "disabled":
        return "disabled"

    raise ERPNextConfigurationError("ERPNEXT_MODE must be one of: mock, live, bench, disabled.")


def _configured_auth_mode() -> Optional[str]:
    if settings.erpnext_api_key and settings.erpnext_api_secret:
        return "token"
    if settings.erpnext_api_key:
        return "bearer"
    return None


def _display_base_url() -> str:
    if not settings.erpnext_base_url:
        return "unconfigured"

    parsed = urlparse(settings.erpnext_base_url)
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"

    return settings.erpnext_base_url.rstrip("/") or "unconfigured"


def _validate_live_configuration() -> tuple[str, str]:
    base_url = (settings.erpnext_base_url or "").strip().rstrip("/")
    auth_mode = _configured_auth_mode()

    if not base_url:
        raise ERPNextConfigurationError(
            "ERPNEXT_MODE=live requires ERPNEXT_BASE_URL to be configured explicitly."
        )

    if not auth_mode:
        raise ERPNextConfigurationError(
            "ERPNEXT_MODE=live requires ERPNext credentials. Configure ERPNEXT_API_KEY "
            + "and ERPNEXT_API_SECRET for token auth, or at minimum ERPNEXT_API_KEY for "
            + "a bearer-style upstream integration."
        )

    return base_url, auth_mode


def get_erpnext_mode() -> ERPNextMode:
    explicit_mode = _normalize_mode(settings.erpnext_mode)
    if explicit_mode is not None:
        if (
            explicit_mode == "mock"
            and not settings.is_local_environment
            and not settings.erpnext_allow_mock_in_non_local
        ):
            raise ERPNextConfigurationError(
                "ERPNEXT_MODE=mock is blocked outside local/test environments unless "
                + "ERPNEXT_ALLOW_MOCK_IN_NON_LOCAL=true is set intentionally."
            )
        return explicit_mode

    if settings.erpnext_mock_enabled and settings.is_local_environment:
        return "mock"

    return "disabled"


def get_erpnext_client() -> ERPNextClient:
    mode = get_erpnext_mode()

    if mode == "mock":
        logger.info(
            "ERPNext client selection: mode=mock environment=%s",
            settings.normalized_environment,
        )
        return MockERPNextClient()

    if mode == "bench":
        if settings.normalized_environment != "staging" or not settings.erpnext_bench_root:
            raise ERPNextConfigurationError(
                "ERPNEXT_MODE=bench is restricted to staging and requires ERPNEXT_BENCH_ROOT."
            )
        logger.info(
            "ERPNext client selection: mode=bench environment=%s bench_root=%s",
            settings.normalized_environment,
            settings.erpnext_bench_root,
        )
        return FrappeBenchERPNextClient(
            bench_root=settings.erpnext_bench_root,
            site_prefix=settings.erpnext_bench_site_prefix,
            run_as_user=settings.erpnext_bench_run_as_user,
            bench_command=settings.erpnext_bench_command,
            web_url=settings.erpnext_bench_web_url,
            db_root_username=settings.erpnext_db_root_username,
            db_root_password=settings.erpnext_db_root_password,
        )

    if mode == "live":
        base_url, auth_mode = _validate_live_configuration()
        logger.info(
            "ERPNext client selection: mode=live environment=%s target=%s auth_mode=%s",
            settings.normalized_environment,
            _display_base_url(),
            auth_mode,
        )
        return ERPNextHTTPClient(base_url=base_url)

    raise ERPNextConfigurationError(
        "ERPNext integration is disabled for this environment. Use ERPNEXT_MODE=mock "
        + "for local development, ERPNEXT_MODE=bench only for the isolated staging bench, "
        + "or configure ERPNEXT_MODE=live intentionally for the approved production cutover."
    )


def get_erpnext_runtime_summary() -> dict[str, str]:
    try:
        mode = get_erpnext_mode()
    except ERPNextConfigurationError as exc:
        return {
            "environment": settings.normalized_environment,
            "mode": "invalid",
            "policy": "configuration_error",
            "message": str(exc),
        }

    if mode == "mock":
        return {
            "environment": settings.normalized_environment,
            "mode": "mock",
            "policy": "local_safe_default",
            "message": "Mock ERPNext behavior is active for local/test development only.",
            "target": "mock-runtime",
        }

    if mode == "bench":
        if settings.normalized_environment != "staging" or not settings.erpnext_bench_root:
            return {
                "environment": settings.normalized_environment,
                "mode": "invalid",
                "policy": "configuration_error",
                "message": "Staging bench ERPNext mode requires an explicit staging bench root.",
            }
        return {
            "environment": settings.normalized_environment,
            "mode": "bench",
            "policy": "isolated_staging_bench",
            "message": "The dedicated staging Frappe bench is active for isolated synthetic provisioning.",
            "target": settings.erpnext_bench_root,
        }

    if mode == "live":
        try:
            _, auth_mode = _validate_live_configuration()
        except ERPNextConfigurationError as exc:
            return {
                "environment": settings.normalized_environment,
                "mode": "invalid",
                "policy": "configuration_error",
                "message": str(exc),
                "target": _display_base_url(),
            }

        return {
            "environment": settings.normalized_environment,
            "mode": "live",
            "policy": "live_cutover_active",
            "message": "Live ERPNext integration is active and ready for Phase 18 cutover validation.",
            "target": _display_base_url(),
            "auth_mode": auth_mode,
        }

    return {
        "environment": settings.normalized_environment,
        "mode": "disabled",
        "policy": "production_safe_default",
        "message": "ERPNext integration is disabled until live cutover is enabled intentionally.",
        "target": _display_base_url(),
    }
