from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional
from uuid import uuid4

from app.integrations.erpnext_client import (
    BackupRecord,
    ERPNextClient,
    OperationResult,
    ProvisionRecord,
    SiteStatus,
)


class MockERPNextClient(ERPNextClient):
    """In-memory mock ERPNext client.

    Behavior:
    - Keeps per-site state in memory.
    - Deterministic by default; failure modes can be injected via `failures` dict.
    - Optionally can persist state to a JSON file path (not enabled by default).
    """

    def __init__(self, *, failures: Optional[dict[str, Any]] = None, clock=None) -> None:
        # failures map keys like "create_site", "install_app", "backup_site" -> bool or callable
        self.failures = failures or {}
        self.clock = clock or datetime.utcnow
        self.sites: dict[str, dict[str, Any]] = {}
        self.backups: dict[str, dict[str, Any]] = {}

    def _should_fail(self, op: str) -> bool:
        v = self.failures.get(op)
        if v is None:
            return False
        if callable(v):
            try:
                return bool(v())
            except Exception:
                return True
        return bool(v)

    def create_site(
        self, organization_id: str, tenant_id: str, site_options: dict[str, Any]
    ) -> ProvisionRecord:
        if self._should_fail("create_site"):
            return ProvisionRecord(
                {"status": "failed", "error": "simulated create_site failure"}
            )

        site_id = str(uuid4())
        site_name = f"{tenant_id}.mock.erp"
        now = self.clock()
        self.sites[site_id] = {
            "site_id": site_id,
            "site_name": site_name,
            "organization_id": organization_id,
            "tenant_id": tenant_id,
            "created_at": now.isoformat(),
            "status": "creating",
            "apps": [],
            "domains": [],
            "ssl": {},
            "configuration": {"modules": [], "roles": [], "workspaces": [], "branding": {}},
        }

        # Simulate creation finishing shortly after
        self.sites[site_id]["status"] = "healthy"

        return ProvisionRecord(
            {
                "status": "success",
                "site_id": site_id,
                "site_name": site_name,
                "created_at": now.isoformat(),
                "mock": True,
            }
        )

    def get_site_status(self, site_id: str) -> SiteStatus:
        s = self.sites.get(site_id)
        if not s:
            return SiteStatus({"status": "not_found", "site_id": site_id})
        # allow forcing failure via "get_site_status"
        if self._should_fail("get_site_status"):
            return SiteStatus(
                {"status": "failed", "site_id": site_id, "error": "simulated"}
            )
        return SiteStatus(
            {
                "status": s.get("status", "unknown"),
                "site_id": site_id,
                "site_name": s.get("site_name"),
            }
        )

    def install_app(self, site_id: str, app_name: str) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if self._should_fail("install_app"):
            return OperationResult(
                {
                    "status": "failed",
                    "site_id": site_id,
                    "app": app_name,
                    "error": "simulated",
                }
            )
        self.sites[site_id]["apps"].append(app_name)
        return OperationResult(
            {"status": "success", "site_id": site_id, "app": app_name, "provider": "mock"}
        )

    def apply_site_configuration(self, site_id: str, configuration: dict[str, object]) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if self._should_fail("apply_site_configuration"):
            return OperationResult({"status": "failed", "site_id": site_id, "error": "simulated"})
        self.sites[site_id]["configuration"].update(configuration)
        return OperationResult({"status": "success", "site_id": site_id, "provider": "mock", "provider_verified": True, "configuration": self.sites[site_id]["configuration"]})

    def get_site_inventory(self, site_id: str) -> dict[str, object]:
        site = self.sites.get(site_id)
        if site is None:
            return {"status": "not_found", "site_id": site_id}
        return {"status": "success", "site_id": site_id, "provider": "mock", "provider_verified": True, "site_name": site["site_name"], "installed_apps": sorted(site["apps"]), "configuration": site["configuration"]}

    def verify_site_configuration(self, site_id: str, requested_modules: list[str]) -> OperationResult:
        inventory = self.get_site_inventory(site_id)
        if inventory.get("status") != "success":
            return OperationResult(inventory)
        configuration = inventory.get("configuration") or {}
        installed = set(inventory.get("installed_apps") or [])
        modules = set(configuration.get("modules") or []) if isinstance(configuration, dict) else set()
        verified = {"erpnext", "lenerp_core"}.issubset(installed) and set(requested_modules).issubset(modules)
        return OperationResult({"status": "success" if verified else "failed", "site_id": site_id, "provider": "mock", "provider_verified": verified, "installed_apps": sorted(installed), "modules": sorted(modules)})

    def bind_domain(self, site_id: str, domain: str) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if self._should_fail("bind_domain"):
            return OperationResult(
                {
                    "status": "failed",
                    "site_id": site_id,
                    "domain": domain,
                    "error": "simulated",
                }
            )
        self.sites[site_id]["domains"].append(
            {"domain": domain, "status": "dns_pending"}
        )
        return OperationResult(
            {"status": "success", "site_id": site_id, "domain": domain, "provider": "mock", "provider_verified": True}
        )

    def issue_ssl(self, site_id: str, domain: str) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if self._should_fail("issue_ssl"):
            return OperationResult(
                {
                    "status": "failed",
                    "site_id": site_id,
                    "domain": domain,
                    "error": "simulated",
                }
            )
        # mark ssl issued
        self.sites[site_id]["ssl"][domain] = {
            "status": "issued",
            "issued_at": self.clock().isoformat(),
        }
        return OperationResult(
            {"status": "success", "site_id": site_id, "domain": domain, "ssl": "issued", "provider": "mock", "provider_verified": True}
        )

    def backup_site(self, site_id: str) -> BackupRecord:
        if site_id not in self.sites:
            return BackupRecord({"status": "not_found", "site_id": site_id})
        if self._should_fail("backup_site"):
            return BackupRecord(
                {"status": "failed", "site_id": site_id, "error": "simulated"}
            )
        backup_id = str(uuid4())
        now = self.clock()
        self.backups[backup_id] = {
            "backup_id": backup_id,
            "site_id": site_id,
            "created_at": now.isoformat(),
            "size_bytes": 1024,
            "status": "available",
        }
        return BackupRecord(
            {"status": "success", "backup_id": backup_id, "site_id": site_id}
        )

    def restore_site(self, site_id: str, backup_id: str) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if backup_id not in self.backups:
            return OperationResult({"status": "not_found", "backup_id": backup_id})
        if self._should_fail("restore_site"):
            return OperationResult(
                {
                    "status": "failed",
                    "site_id": site_id,
                    "backup_id": backup_id,
                    "error": "simulated",
                }
            )
        # simulate restore by updating a restored_at on site
        self.sites[site_id]["restored_at"] = self.clock().isoformat()
        return OperationResult(
            {"status": "success", "site_id": site_id, "backup_id": backup_id}
        )

    def delete_site(self, site_id: str) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if self._should_fail("delete_site"):
            return OperationResult(
                {"status": "failed", "site_id": site_id, "error": "simulated"}
            )
        del self.sites[site_id]
        return OperationResult({"status": "success", "site_id": site_id})
