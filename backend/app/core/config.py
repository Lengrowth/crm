from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SaaS Control Backend"
    environment: str = "local"
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
    erpnext_mode: str | None = None
    erpnext_allow_mock_in_non_local: bool = False
    erpnext_base_url: str | None = None
    erpnext_api_key: str | None = None
    erpnext_api_secret: str | None = None

    auth_session_days: int = 30

    # Resend (marketing email) configuration
    resend_api_key: str | None = None
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


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
