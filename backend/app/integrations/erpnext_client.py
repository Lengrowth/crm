from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class ProvisionRecord(dict[str, object]):
    """Lightweight dict-like record for provision responses."""


class SiteStatus(dict[str, object]):
    pass


class OperationResult(dict[str, object]):
    pass


class BackupRecord(dict[str, object]):
    pass


class ERPNextClient(ABC):
    """Abstraction for ERPNext/Frappe operations used by the SaaS control plane.

    Implementations should be deterministic (or configurable) for testing.
    Methods may be synchronous; async usage is supported by calling from an async context.
    """

    @abstractmethod
    def create_site(
        self, organization_id: str, tenant_id: str, site_options: dict[str, object]
    ) -> ProvisionRecord:
        raise NotImplementedError

    @abstractmethod
    def get_site_status(self, site_id: str) -> SiteStatus:
        raise NotImplementedError

    @abstractmethod
    def install_app(self, site_id: str, app_name: str) -> OperationResult:
        raise NotImplementedError

    def migrate_site(self, site_id: str) -> OperationResult:
        return OperationResult({"status": "unsupported", "site_id": site_id})

    @abstractmethod
    def bind_domain(self, site_id: str, domain: str) -> OperationResult:
        raise NotImplementedError

    @abstractmethod
    def issue_ssl(self, site_id: str, domain: str) -> OperationResult:
        raise NotImplementedError

    @abstractmethod
    def backup_site(self, site_id: str) -> BackupRecord:
        raise NotImplementedError

    @abstractmethod
    def restore_site(self, site_id: str, backup_id: str) -> OperationResult:
        raise NotImplementedError

    @abstractmethod
    def delete_site(self, site_id: str) -> OperationResult:
        raise NotImplementedError

    def apply_site_configuration(self, site_id: str, configuration: dict[str, object]) -> OperationResult:
        return OperationResult({"status": "unsupported", "site_id": site_id})

    def get_site_inventory(self, site_id: str) -> dict[str, object]:
        return {"status": "unsupported", "site_id": site_id}

    def verify_site_configuration(self, site_id: str, requested_modules: list[str], required_apps: Optional[dict[str, str]] = None, required_roles: Optional[list[str]] = None, required_workspaces: Optional[list[str]] = None, required_app_versions: Optional[dict[str, str]] = None) -> OperationResult:
        return OperationResult({"status": "unsupported", "site_id": site_id, "requested_modules": requested_modules, "required_apps": required_apps or {}, "required_roles": required_roles or [], "required_workspaces": required_workspaces or [], "required_app_versions": required_app_versions or {}})
