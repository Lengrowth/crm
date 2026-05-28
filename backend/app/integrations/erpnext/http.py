from __future__ import annotations

from typing import Any, Optional

import httpx

from app.core.config import settings
from app.integrations.erpnext_client import (
    BackupRecord,
    ERPNextClient,
    OperationResult,
    ProvisionRecord,
    SiteStatus,
)


class ERPNextHTTPClient(ERPNextClient):
    """Synchronous HTTP client for the future live ERPNext integration path.

    This client remains available for tests and future cutover work, but Phase 15
    does not activate it in production flows yet.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self.base_url = (base_url or settings.erpnext_base_url or "").rstrip("/")
        self.api_key = api_key or settings.erpnext_api_key
        self.api_secret = api_secret or settings.erpnext_api_secret
        self.timeout_seconds = timeout_seconds

    def _auth_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.api_key and self.api_secret:
            headers["Authorization"] = f"token {self.api_key}:{self.api_secret}"
        elif self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(
        self, method: str, path: str, payload: Optional[dict[str, Any]] = None
    ) -> dict[str, object]:
        if not self.base_url:
            return {
                "status": "failed",
                "error": "erpnext_base_url_not_configured",
            }

        url = f"{self.base_url}{path}"
        try:
            response = httpx.request(
                method,
                url,
                json=payload,
                headers=self._auth_headers(),
                timeout=self.timeout_seconds,
            )
        except httpx.HTTPError as exc:
            return {"status": "failed", "error": str(exc)}

        try:
            response_payload = response.json()
        except ValueError:
            response_payload = {
                "status_code": response.status_code,
                "text": response.text,
            }

        if isinstance(response_payload, dict):
            data = dict(response_payload)
        else:
            data = {"data": response_payload}

        if response.is_success:
            data.setdefault("status", "success")
            return data

        return {
            "status": "failed",
            "error": str(
                data.get("text") or data.get("detail") or response.reason_phrase
            ),
            "status_code": response.status_code,
            **data,
        }

    def create_site(
        self, organization_id: str, tenant_id: str, site_options: dict[str, object]
    ) -> ProvisionRecord:
        return ProvisionRecord(
            self._request(
                "POST",
                "/api/v1/sites",
                {
                    "organization_id": organization_id,
                    "tenant_id": tenant_id,
                    "options": site_options,
                },
            )
        )

    def get_site_status(self, site_id: str) -> SiteStatus:
        return SiteStatus(self._request("GET", f"/api/v1/sites/{site_id}/status"))

    def install_app(self, site_id: str, app_name: str) -> OperationResult:
        return OperationResult(
            self._request("POST", f"/api/v1/sites/{site_id}/apps", {"app": app_name})
        )

    def bind_domain(self, site_id: str, domain: str) -> OperationResult:
        return OperationResult(
            self._request(
                "POST", f"/api/v1/sites/{site_id}/domains", {"domain": domain}
            )
        )

    def issue_ssl(self, site_id: str, domain: str) -> OperationResult:
        return OperationResult(
            self._request("POST", f"/api/v1/sites/{site_id}/ssl", {"domain": domain})
        )

    def backup_site(self, site_id: str) -> BackupRecord:
        return BackupRecord(self._request("POST", f"/api/v1/sites/{site_id}/backups"))

    def restore_site(self, site_id: str, backup_id: str) -> OperationResult:
        return OperationResult(
            self._request(
                "POST",
                f"/api/v1/sites/{site_id}/restore",
                {"backup_id": backup_id},
            )
        )

    def delete_site(self, site_id: str) -> OperationResult:
        return OperationResult(self._request("DELETE", f"/api/v1/sites/{site_id}"))


HttpERPNextClient = ERPNextHTTPClient
