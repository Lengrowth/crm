from __future__ import annotations

"""Provider adapter for the dedicated staging Frappe bench.

This is deliberately a different client from the in-memory test double. It
executes bench against the separately provisioned staging bench, its MariaDB
site database, its site files, and its dedicated Redis/web/worker lane. The
adapter is only selectable when the application environment is ``staging`` and
the bench root is explicitly configured.
"""

import getpass
import json
import os
import re
import secrets
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

from app.integrations.erpnext_client import (
    BackupRecord,
    ERPNextClient,
    OperationResult,
    ProvisionRecord,
    SiteStatus,
)


class FrappeBenchERPNextClient(ERPNextClient):
    def __init__(
        self,
        *,
        bench_root: str,
        site_prefix: str = "phase4-",
        run_as_user: Optional[str] = "frappe",
        bench_command: str = "/usr/local/bin/bench",
        web_url: str = "http://127.0.0.1:28000",
        db_root_password: Optional[str] = None,
        command_timeout_seconds: int = 300,
    ) -> None:
        self.bench_root = Path(bench_root).resolve()
        self.site_prefix = site_prefix.strip().lower()
        self.run_as_user = run_as_user.strip() if run_as_user else None
        self.bench_command = bench_command
        self.web_url = web_url.rstrip("/")
        self.db_root_password = db_root_password
        self.command_timeout_seconds = max(30, command_timeout_seconds)
        if not self.site_prefix or not re.fullmatch(r"[a-z0-9-]+", self.site_prefix):
            raise ValueError("ERPNEXT_BENCH_SITE_PREFIX must be a safe lowercase prefix.")
        if not self.bench_root.is_absolute():
            raise ValueError("ERPNEXT_BENCH_ROOT must be an absolute path.")

    @classmethod
    def from_environment(cls) -> "FrappeBenchERPNextClient":
        return cls(
            bench_root=os.environ["ERPNEXT_BENCH_ROOT"],
            site_prefix=os.environ.get("ERPNEXT_BENCH_SITE_PREFIX", "phase4-"),
            run_as_user=os.environ.get("ERPNEXT_BENCH_RUN_AS_USER", "frappe"),
            bench_command=os.environ.get("ERPNEXT_BENCH_COMMAND", "/usr/local/bin/bench"),
            web_url=os.environ.get("ERPNEXT_BENCH_WEB_URL", "http://127.0.0.1:28000"),
            db_root_password=os.environ.get("ERPNEXT_DB_ROOT_PASSWORD") or None,
            command_timeout_seconds=int(os.environ.get("ERPNEXT_BENCH_TIMEOUT_SECONDS", "300")),
        )

    def _command(self, args: list[str]) -> list[str]:
        command = [self.bench_command, *args]
        if self.run_as_user and getpass.getuser() != self.run_as_user:
            command = ["sudo", "-n", "-u", self.run_as_user, *command]
        return command

    def _run(self, args: list[str], *, input_data: Optional[str] = None) -> tuple[bool, str]:
        try:
            result = subprocess.run(
                self._command(args),
                cwd=self.bench_root,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=self.command_timeout_seconds,
                check=False,
                env={**os.environ, "BENCH_ROOT": str(self.bench_root)},
            )
        except (OSError, subprocess.SubprocessError):
            return False, "bench command could not be executed"
        if result.returncode != 0:
            # Provider stderr is intentionally never persisted in control-plane
            # evidence; it may contain database or site-local details.
            return False, "bench command failed"
        return True, result.stdout.strip()

    def _site_path(self, site_id: str) -> Path:
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,253}[a-z0-9]", site_id):
            raise ValueError("unsafe ERP site identifier")
        if not site_id.startswith(self.site_prefix):
            raise ValueError("ERP site is outside the isolated Phase 4 namespace")
        path = (self.bench_root / "sites" / site_id).resolve()
        sites_root = (self.bench_root / "sites").resolve()
        if sites_root not in path.parents:
            raise ValueError("ERP site path escaped the configured bench")
        return path

    def _site_exists(self, site_id: str) -> bool:
        return self._site_path(site_id).is_dir()

    def _site_name(self, tenant_id: str, site_options: dict[str, object]) -> str:
        requested = str(site_options.get("domain") or "").strip().lower()
        if requested and re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,253}[a-z0-9]", requested) and requested.startswith(self.site_prefix):
            return requested
        return f"{self.site_prefix}{re.sub(r'[^a-z0-9-]', '-', tenant_id.lower())[:32]}.staging.example.test"

    def _list_apps(self, site_id: str) -> dict[str, str]:
        ok, output = self._run(["--site", site_id, "list-apps"])
        if not ok:
            return {}
        apps: dict[str, str] = {}
        for line in output.splitlines():
            match = re.match(r"^\s*([a-zA-Z0-9_]+)\s+([^\s]+)\s*$", line)
            if match and match.group(1).lower() not in {"app", "name"}:
                apps[match.group(1)] = match.group(2)
        return apps

    def _show_config(self, site_id: str) -> dict[str, object]:
        ok, output = self._run(["--site", site_id, "show-config"])
        if not ok:
            return {}
        start = output.find("{")
        end = output.rfind("}")
        if start < 0 or end < start:
            return {}
        try:
            payload = json.loads(output[start : end + 1])
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _set_config(self, site_id: str, key: str, value: object) -> bool:
        encoded = json.dumps(value, separators=(",", ":"))
        ok, _ = self._run(["--site", site_id, "set-config", key, encoded, "--parse"])
        if ok:
            return True
        ok, _ = self._run(["--site", site_id, "set-config", "--parse", key, encoded])
        return ok

    @staticmethod
    def _config_value(config: dict[str, object], key: str, default: object) -> object:
        value = config.get(key, default)
        if isinstance(value, str) and value[:1] in {"[", "{"}:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return default
        return value

    def create_site(self, organization_id: str, tenant_id: str, site_options: dict[str, object]) -> ProvisionRecord:
        site_name = self._site_name(tenant_id, site_options)
        if self._site_exists(site_name):
            return ProvisionRecord({"status": "success", "site_id": site_name, "site_name": site_name, "provider": "frappe_staging_bench", "replayed": True})
        admin_password = secrets.token_urlsafe(32)
        args = ["new-site", site_name, "--admin-password", admin_password]
        if self.db_root_password:
            args.extend(["--db-root-password", self.db_root_password])
        ok, _ = self._run(args, input_data=(self.db_root_password + "\n") if self.db_root_password else None)
        if not ok and not self._site_exists(site_name):
            return ProvisionRecord({"status": "failed", "error": "isolated ERP site creation failed"})
        return ProvisionRecord({"status": "success", "site_id": site_name, "site_name": site_name, "provider": "frappe_staging_bench", "bench_root": str(self.bench_root), "database_isolated": True, "files_isolated": True, "queues_isolated": True})

    def get_site_status(self, site_id: str) -> SiteStatus:
        if not self._site_exists(site_id):
            return SiteStatus({"status": "not_found", "site_id": site_id, "provider": "frappe_staging_bench"})
        try:
            request = urllib.request.Request(
                f"{self.web_url}/api/method/frappe.auth.get_logged_user",
                headers={"Host": site_id, "User-Agent": "LenERP-Phase4-provider-check/1.0"},
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                http_status = response.status
        except urllib.error.HTTPError as error:
            http_status = error.code
        except (OSError, urllib.error.URLError):
            return SiteStatus({"status": "failed", "site_id": site_id, "provider": "frappe_staging_bench", "error": "isolated ERP web health check failed"})
        if http_status not in {200, 301, 302, 401, 403}:
            return SiteStatus({"status": "failed", "site_id": site_id, "provider": "frappe_staging_bench", "http_status": http_status})
        return SiteStatus({"status": "healthy", "site_id": site_id, "site_name": site_id, "provider": "frappe_staging_bench", "http_status": http_status})

    def install_app(self, site_id: str, app_name: str) -> OperationResult:
        if not self._site_exists(site_id):
            return OperationResult({"status": "not_found", "site_id": site_id})
        if app_name in self._list_apps(site_id):
            return OperationResult({"status": "success", "site_id": site_id, "app": app_name, "provider": "frappe_staging_bench", "replayed": True})
        ok, _ = self._run(["--site", site_id, "install-app", app_name])
        return OperationResult({"status": "success" if ok else "failed", "site_id": site_id, "app": app_name, "provider": "frappe_staging_bench", "provider_verified": ok})

    def apply_site_configuration(self, site_id: str, configuration: dict[str, object]) -> OperationResult:
        if not self._site_exists(site_id):
            return OperationResult({"status": "not_found", "site_id": site_id})
        keys = {"modules": "lenerp_phase4_modules", "roles": "lenerp_phase4_roles", "workspaces": "lenerp_phase4_workspaces", "branding": "lenerp_phase4_branding"}
        for source, target in keys.items():
            if source in configuration and not self._set_config(site_id, target, configuration[source]):
                return OperationResult({"status": "failed", "site_id": site_id, "error": "ERP site configuration failed"})
        inventory = self.get_site_inventory(site_id)
        return OperationResult({"status": "success" if inventory.get("status") == "success" else "failed", "site_id": site_id, "provider": "frappe_staging_bench", "provider_verified": inventory.get("status") == "success", "configuration": inventory.get("configuration", {})})

    def get_site_inventory(self, site_id: str) -> dict[str, object]:
        if not self._site_exists(site_id):
            return {"status": "not_found", "site_id": site_id, "provider": "frappe_staging_bench"}
        apps = self._list_apps(site_id)
        config = self._show_config(site_id)
        if not apps or not config:
            return {"status": "failed", "site_id": site_id, "provider": "frappe_staging_bench", "error": "ERP site inventory could not be read"}
        site_path = self._site_path(site_id)
        return {
            "status": "success",
            "site_id": site_id,
            "site_name": site_id,
            "provider": "frappe_staging_bench",
            "provider_verified": True,
            "bench_root": str(self.bench_root),
            "site_path": str(site_path),
            "database_name": str(config.get("db_name") or site_id.replace(".", "_")),
            "files_path": str(site_path),
            "queue_namespace": f"{site_id}:short,default",
            "installed_apps": apps,
            "configuration": {
                "modules": self._config_value(config, "lenerp_phase4_modules", []),
                "roles": self._config_value(config, "lenerp_phase4_roles", []),
                "workspaces": self._config_value(config, "lenerp_phase4_workspaces", []),
                "branding": self._config_value(config, "lenerp_phase4_branding", {}),
            },
        }

    def verify_site_configuration(self, site_id: str, requested_modules: list[str]) -> OperationResult:
        inventory = self.get_site_inventory(site_id)
        if inventory.get("status") != "success":
            return OperationResult(inventory)
        apps = set((inventory.get("installed_apps") or {}).keys())
        configuration = inventory.get("configuration") or {}
        modules = set(configuration.get("modules") or []) if isinstance(configuration, dict) else set()
        verified = {"frappe", "erpnext", "lenerp_core"}.issubset(apps) and set(requested_modules).issubset(modules)
        return OperationResult({"status": "success" if verified else "failed", "site_id": site_id, "provider": "frappe_staging_bench", "provider_verified": verified, "installed_apps": sorted(apps), "modules": sorted(modules), "inventory": inventory})

    def bind_domain(self, site_id: str, domain: str) -> OperationResult:
        if not self._site_exists(site_id):
            return OperationResult({"status": "not_found", "site_id": site_id})
        ok = self._set_config(site_id, "host_name", domain)
        return OperationResult({"status": "success" if ok else "failed", "site_id": site_id, "domain": domain, "provider": "frappe_staging_bench", "provider_verified": ok})

    def issue_ssl(self, site_id: str, domain: str) -> OperationResult:
        if not self._site_exists(site_id):
            return OperationResult({"status": "not_found", "site_id": site_id})
        return OperationResult({"status": "deferred", "site_id": site_id, "domain": domain, "ssl": "deferred_isolated_loopback", "provider": "frappe_staging_bench", "provider_verified": True})

    def backup_site(self, site_id: str) -> BackupRecord:
        return BackupRecord({"status": "unsupported", "site_id": site_id, "error": "Direct ERP backup mutation is operator-controlled."})

    def restore_site(self, site_id: str, backup_id: str) -> OperationResult:
        return OperationResult({"status": "unsupported", "site_id": site_id, "backup_id": backup_id, "error": "Direct ERP restore mutation is operator-controlled."})

    def delete_site(self, site_id: str) -> OperationResult:
        if not self._site_exists(site_id):
            return OperationResult({"status": "not_found", "site_id": site_id, "provider": "frappe_staging_bench"})
        ok, _ = self._run(["drop-site", site_id, "--force", "--no-backup"])
        if not ok and self._site_exists(site_id):
            return OperationResult({"status": "failed", "site_id": site_id, "provider": "frappe_staging_bench", "error": "isolated ERP site cleanup failed"})
        return OperationResult({"status": "success", "site_id": site_id, "provider": "frappe_staging_bench", "provider_verified": not self._site_exists(site_id)})
