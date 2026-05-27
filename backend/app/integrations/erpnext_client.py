from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


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
