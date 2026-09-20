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
            "apps": ["frappe"],
            "app_versions": {"frappe": "15.119.1"},
            "app_commits": {"frappe": "edae775dd36b6c4ad7acab10230262bd74040765"},
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
        if app_name in self.sites[site_id]["apps"]:
            return OperationResult({"status": "success", "site_id": site_id, "app": app_name, "provider": "mock", "replayed": True, "provider_verified": True})
        self.sites[site_id]["apps"].append(app_name)
        self.sites[site_id]["app_versions"][app_name] = {"erpnext": "15.120.0", "hrms": "15.64.1", "lenerp_core": "0.2.0"}.get(app_name, "")
        self.sites[site_id]["app_commits"][app_name] = {"erpnext": "945e825bee3d0d645f6cb59bcaab90fcbfb98ce3", "hrms": "e68a3deaa95ae5b2c3d743297d0a4ab505733fc1", "lenerp_core": "95b482abdeb284a138b73f056699c50290dc445f"}.get(app_name, "")
        return OperationResult(
            {"status": "success", "site_id": site_id, "app": app_name, "provider": "mock", "provider_verified": True, "version": self.sites[site_id]["app_versions"][app_name]}
        )

    def migrate_site(self, site_id: str) -> OperationResult:
        if site_id not in self.sites:
            return OperationResult({"status": "not_found", "site_id": site_id})
        if self._should_fail("migrate_site"):
            return OperationResult({"status": "failed", "site_id": site_id, "error": "simulated"})
        self.sites[site_id]["migrated"] = True
        return OperationResult({"status": "success", "site_id": site_id, "provider": "mock", "provider_verified": True, "replayed": bool(self.sites[site_id].get("migrated"))})

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
        return {"status": "success", "site_id": site_id, "provider": "mock", "provider_verified": True, "site_name": site["site_name"], "installed_apps": {app: site["app_versions"].get(app, "") for app in sorted(site["apps"])}, "installed_app_commits": {app: site["app_commits"].get(app, "") for app in sorted(site["apps"])}, "configuration": site["configuration"], "migrated": bool(site.get("migrated"))}

    def verify_site_configuration(self, site_id: str, requested_modules: list[str], required_apps: Optional[dict[str, str]] = None, required_roles: Optional[list[str]] = None, required_workspaces: Optional[list[str]] = None, required_app_versions: Optional[dict[str, str]] = None, required_app_commits: Optional[dict[str, str]] = None) -> OperationResult:
        inventory = self.get_site_inventory(site_id)
        if inventory.get("status") != "success":
            return OperationResult(inventory)
        configuration = inventory.get("configuration") or {}
        installed_payload = inventory.get("installed_apps") or {}
        installed = set(installed_payload.keys()) if isinstance(installed_payload, dict) else set(installed_payload)
        modules = set(configuration.get("modules") or []) if isinstance(configuration, dict) else set()
        requirements = required_apps or {}
        missing_required_apps = sorted({app for app in requirements.values() if app and app not in installed})
        current_roles = set(configuration.get("roles") or []) if isinstance(configuration, dict) else set()
        current_workspaces = set(configuration.get("workspaces") or []) if isinstance(configuration, dict) else set()
        missing_required_roles = sorted(set(required_roles or []) - current_roles)
        missing_required_workspaces = sorted(set(required_workspaces or []) - current_workspaces)
        missing_versions = sorted(f"{app} (expected {version}, read {installed_payload.get(app) or 'unknown'})" for app, version in (required_app_versions or {}).items() if app in installed and installed_payload.get(app) != version)
        installed_commits = inventory.get("installed_app_commits") or {}
        missing_commits = sorted(f"{app} (expected {commit}, read {installed_commits.get(app) or 'unknown'})" for app, commit in (required_app_commits or {}).items() if app in installed and installed_commits.get(app) != commit)
        verified = {"frappe", "erpnext", "lenerp_core"}.issubset(installed) and set(requested_modules).issubset(modules) and not missing_required_apps and not missing_required_roles and not missing_required_workspaces and not missing_versions and not missing_commits
        return OperationResult({"status": "success" if verified else "failed", "site_id": site_id, "provider": "mock", "provider_verified": verified, "installed_apps": sorted(installed), "app_versions": installed_payload, "installed_app_commits": installed_commits, "modules": sorted(modules), "required_apps": requirements, "missing_required_apps": missing_required_apps, "incompatible_apps": [*missing_versions, *missing_commits], "missing_required_roles": missing_required_roles, "missing_required_workspaces": missing_required_workspaces})

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
