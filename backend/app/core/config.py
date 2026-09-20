from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SaaS Control Backend"
    product_name: str = "LenERP"
    environment: str = "local"
    release_id: str = "local"
    release_commit: str = "unknown"
    release_manifest_path: Optional[str] = None
    feature_flags: str = ""
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_base_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000"
    database_url: str = "sqlite:///./saas_control.db"
    database_echo: bool = False

    # ERPNext integration mode selection.
    # - Local/test environments may continue using the mock client via the legacy
    #   boolean fallback below.
    # - Production-like environments default to a safe disabled state unless an
    #   explicit mode is chosen.
    erpnext_mock_enabled: bool = True
    erpnext_mode: Optional[str] = None
    erpnext_allow_mock_in_non_local: bool = False
    erpnext_base_url: Optional[str] = None
    erpnext_api_key: Optional[str] = None
    erpnext_api_secret: Optional[str] = None
    erpnext_bench_root: Optional[str] = None
    erpnext_bench_site_prefix: str = "phase4-"
    erpnext_bench_run_as_user: Optional[str] = "frappe"
    erpnext_bench_command: str = "/usr/local/bin/bench"
    erpnext_bench_web_url: str = "http://127.0.0.1:28000"
    erpnext_db_root_username: str = "root"
    erpnext_db_root_password: Optional[str] = None

    auth_session_days: int = 30
    auth_password_reset_token_minutes: int = 60
    auth_email_verification_token_hours: int = 24

    billing_provider: Optional[str] = None
    billing_allow_mock_in_non_local: bool = False
    billing_webhook_secret: Optional[str] = None

    security_headers_enabled: bool = True
    rate_limit_enabled: bool = False
    rate_limit_max_requests: int = 120
    rate_limit_window_seconds: int = 60
    rate_limit_exempt_paths: str = "/health,/docs,/openapi.json,/redoc"

    # Phase 03 uses a deliberately isolated authorization-code broker until a
    # maintained OIDC provider can replace it. The flag is off by default.
    sso_client_id: str = "lenerp-erp"
    sso_audience: str = "lenerp-erp"
    sso_exchange_secret: Optional[str] = None
    sso_code_ttl_seconds: int = 120
    sso_callback_path: str = "/api/method/lenerp_core.sso.callback"
    sso_jit_provisioning_enabled: bool = False

    # Resend (marketing email) configuration
    resend_api_key: Optional[str] = None
    resend_api_url: str = "https://api.resend.com/emails"
    resend_from_email: str = "hello@local-saas.test"
    # Recipient for marketing intake emails (contact/demo)
    marketing_contact_recipient: str = "hello@local-saas.test"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]

    @property
    def normalized_environment(self) -> str:
        return self.environment.strip().lower()

    @property
    def is_local_environment(self) -> bool:
        return self.normalized_environment in {"local", "development", "dev", "test"}

    @property
    def rate_limit_exempt_path_list(self) -> list[str]:
        return [path.strip() for path in self.rate_limit_exempt_paths.split(",") if path.strip()]

    @property
    def rate_limit_effective_enabled(self) -> bool:
        return bool(self.rate_limit_enabled and not self.is_local_environment)

    @property
    def feature_flag_map(self) -> dict[str, bool]:
        """Parse server-controlled flags without exposing environment secrets."""
        flags: dict[str, bool] = {}
        for item in self.feature_flags.split(","):
            name, separator, value = item.partition("=")
            if not separator:
                continue
            normalized_name = name.strip()
            if not normalized_name:
                continue
            normalized_value = value.strip().lower()
            if normalized_value in {"1", "true", "on", "yes", "enabled"}:
                flags[normalized_name] = True
            elif normalized_value in {"0", "false", "off", "no", "disabled"}:
                flags[normalized_name] = False
        return flags


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
