from __future__ import annotations

from typing import Literal

from app.core.config import settings
from app.integrations.erpnext.http import ERPNextHTTPClient
from app.integrations.erpnext_client import ERPNextClient
from app.integrations.mock_erpnext import MockERPNextClient

ERPNextMode = Literal["mock", "live", "disabled"]


class ERPNextConfigurationError(RuntimeError):
    """Raised when ERPNext integration mode is unsafe or unavailable."""


def _normalize_mode(mode: str | None) -> ERPNextMode | None:
    if mode is None:
        return None

    normalized = mode.strip().lower()
    if normalized in {"mock", "live", "disabled"}:
        return normalized

    raise ERPNextConfigurationError(
        "ERPNEXT_MODE must be one of: mock, live, disabled."
    )


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
                "ERPNEXT_ALLOW_MOCK_IN_NON_LOCAL=true is set intentionally."
            )
        return explicit_mode

    if settings.erpnext_mock_enabled and settings.is_local_environment:
        return "mock"

    return "disabled"


def get_erpnext_client() -> ERPNextClient:
    mode = get_erpnext_mode()

    if mode == "mock":
        return MockERPNextClient()

    if mode == "live":
        raise ERPNextConfigurationError(
            "Live ERPNext integration remains gated until Phase 18 cutover. "
            "Phase 15 keeps live behavior explicit and safe, but does not enable it yet."
        )

    raise ERPNextConfigurationError(
        "ERPNext integration is disabled for this environment. Use ERPNEXT_MODE=mock "
        "for local development, or wait for the Phase 18 live cutover path."
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
        }

    if mode == "live":
        return {
            "environment": settings.normalized_environment,
            "mode": "live",
            "policy": "phase_18_cutover_required",
            "message": "Live ERPNext mode is configured but intentionally gated until Phase 18.",
        }

    return {
        "environment": settings.normalized_environment,
        "mode": "disabled",
        "policy": "production_safe_default",
        "message": "ERPNext integration is disabled until a later cutover phase enables the live path.",
    }
