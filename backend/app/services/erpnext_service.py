from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.integrations.erpnext_client import (
    BackupRecord,
    ERPNextClient,
    OperationResult,
    SiteStatus,
)
from app.models.domain import Tenant
from app.models.erpnext import (
    ERPNextIntegrationMetadata,
    TenantProvisioningRecord,
    utcnow,
)


class ERPNextService:
    """High-level operations that use an ERPNextClient implementation.

    This service keeps an in-memory map of provisioning records (to avoid DB coupling in tests).
    Integrators can extend this to persist records to the DB (models + migrations added in this phase).
    """

    def __init__(self, client: ERPNextClient) -> None:
        self.client = client
        # simple in-memory provisioning records keyed by provision_id
        self._provisioning: dict[str, dict[str, Any]] = {}

    def provision_tenant(
        self, organization_id: str, tenant_id: str, site_options: dict[str, Any]
    ) -> dict[str, Any]:
        # create a provision record
        provision_id = str(uuid4())
        now = datetime.utcnow().isoformat()
        self._provisioning[provision_id] = {
            "id": provision_id,
            "organization_id": organization_id,
            "tenant_id": tenant_id,
            "status": "running",
            "started_at": now,
            "finished_at": None,
            "details": {},
        }

        # Step 1: create site
        res = self.client.create_site(organization_id, tenant_id, site_options)
        self._provisioning[provision_id]["details"]["create_site"] = dict(res)
        if res.get("status") != "success":
            self._fail_provision(provision_id, f"create_site failed: {res}")
            return self._provisioning[provision_id]

        site_id = res.get("site_id")
        if not site_id:
            self._fail_provision(
                provision_id, f"create_site returned no site_id: {res}"
            )
            return self._provisioning[provision_id]
        site_id = str(site_id)

        # Step 2: install ERPNext core (optional in mock)
        res_install = self.client.install_app(site_id, "erpnext")
        self._provisioning[provision_id]["details"]["install_erpnext"] = dict(
            res_install
        )
        if res_install.get("status") != "success":
            self._fail_provision(provision_id, f"install_erpnext failed: {res_install}")
            return self._provisioning[provision_id]

        # Step 3: install custom app if provided
        custom_app = site_options.get("custom_app")
        if custom_app:
            res_custom = self.client.install_app(site_id, str(custom_app))
            self._provisioning[provision_id]["details"]["install_custom_app"] = dict(
                res_custom
            )
            if res_custom.get("status") != "success":
                self._fail_provision(
                    provision_id, f"install_custom_app failed: {res_custom}"
                )
                return self._provisioning[provision_id]

        # Step 4: bind domain
        domain = site_options.get("domain")
        if domain:
            res_bind = self.client.bind_domain(site_id, str(domain))

            # issue ssl
            res_ssl = self.client.issue_ssl(site_id, str(domain))
            self._provisioning[provision_id]["details"]["issue_ssl"] = dict(res_ssl)
            if res_ssl.get("status") != "success":
                self._fail_provision(provision_id, f"issue_ssl failed: {res_ssl}")
                return self._provisioning[provision_id]

            # success
            self._provisioning[provision_id]["details"]["bind_domain"] = dict(res_bind)
            if res_bind.get("status") != "success":
                self._fail_provision(provision_id, f"bind_domain failed: {res_bind}")
                return self._provisioning[provision_id]

        now2 = datetime.utcnow().isoformat()
        self._provisioning[provision_id]["status"] = "success"
        self._provisioning[provision_id]["finished_at"] = now2
        self._provisioning[provision_id]["site_id"] = site_id
        return self._provisioning[provision_id]

    def _fail_provision(self, provision_id: str, message: str):
        now = datetime.utcnow().isoformat()
        self._provisioning[provision_id]["status"] = "failed"
        self._provisioning[provision_id]["finished_at"] = now
        self._provisioning[provision_id]["error_message"] = message

    def get_provisioning_record(self, provision_id: str) -> Optional[dict[str, Any]]:
        return self._provisioning.get(provision_id)

    def get_site_status(self, site_id: str) -> SiteStatus:
        return self.client.get_site_status(site_id)

    def backup_site(self, site_id: str) -> BackupRecord:
        return self.client.backup_site(site_id)

    def restore_site(self, site_id: str, backup_id: str) -> OperationResult:
        return self.client.restore_site(site_id, backup_id)

    def bind_domain(self, site_id: str, domain: str) -> OperationResult:
        return self.client.bind_domain(site_id, domain)

    def issue_ssl(self, site_id: str, domain: str) -> OperationResult:
        return self.client.issue_ssl(site_id, domain)

    def delete_site(self, site_id: str) -> OperationResult:
        return self.client.delete_site(site_id)


class PersistentERPNextService(ERPNextService):
    """Database-backed provisioner.

    This class uses SQLAlchemy Session objects to persist TenantProvisioningRecord and
    ERPNextIntegrationMetadata. It keeps method signatures compatible for service call sites
    but exposes helpers to create a DB-backed provisioning record and run provisioning.
    """

    def create_provision_record(
        self, session: Session, organization_id: str, tenant_id: str
    ) -> TenantProvisioningRecord:
        rec = (
            session.query(TenantProvisioningRecord)
            .filter_by(organization_id=organization_id, tenant_id=tenant_id)
            .one_or_none()
        )
        if rec is None:
            rec = TenantProvisioningRecord(
                organization_id=organization_id,
                tenant_id=tenant_id,
                status="running",
                started_at=utcnow(),
                details={},
            )
            session.add(rec)
        elif rec.status == "success":
            return rec
        else:
            # Reuse the unique per-tenant record for safe retries instead of
            # inserting a duplicate after a failed or interrupted attempt.
            rec.status = "running"
            rec.started_at = utcnow()
            rec.finished_at = None
            rec.details = {}
            rec.error_message = None
            session.add(rec)

        tenant = session.get(Tenant, tenant_id)
        if tenant is not None:
            tenant.provisioning_status = "running"
            tenant.status = "provisioning"
            session.add(tenant)

        session.commit()
        session.refresh(rec)
        return rec

    def _update_details(
        self,
        session: Session,
        rec: TenantProvisioningRecord,
        key: str,
        value: dict[str, Any],
    ) -> None:
        d = dict(rec.details or {})
        d[key] = value
        rec.details = d
        session.add(rec)
        session.commit()

    def _finalize_success(
        self,
        session: Session,
        rec: TenantProvisioningRecord,
        site_id: str,
        site_name: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        rec.status = "success"
        rec.finished_at = utcnow()
        rec.details = dict(rec.details or {})
        # persist
        session.add(rec)

        tenant = session.get(Tenant, rec.tenant_id)
        if tenant is not None:
            tenant.provisioning_status = "ready"
            tenant.status = "ready"
            if site_name:
                tenant.erpnext_site_name = site_name
            if base_url:
                tenant.erpnext_base_url = base_url
            session.add(tenant)

        # update or create integration metadata
        meta = (
            session.query(ERPNextIntegrationMetadata)
            .filter_by(tenant_id=rec.tenant_id)
            .one_or_none()
        )
        if not meta:
            meta = ERPNextIntegrationMetadata(
                tenant_id=rec.tenant_id,
                site_id=site_id,
                site_name=site_name,
                base_url=base_url,
                metadata_json={},
            )
            session.add(meta)
        else:
            meta.site_id = site_id
            if site_name:
                meta.site_name = site_name
            if base_url:
                meta.base_url = base_url
            session.add(meta)
        session.commit()

    def _finalize_failure(
        self, session: Session, rec: TenantProvisioningRecord, message: str
    ) -> None:
        rec.status = "failed"
        rec.finished_at = utcnow()
        rec.error_message = message
        session.add(rec)

        tenant = session.get(Tenant, rec.tenant_id)
        if tenant is not None:
            tenant.provisioning_status = "failed"
            tenant.status = "failed"
            session.add(tenant)

        session.commit()

    def provision_tenant_persistent(
        self,
        session: Session,
        rec: TenantProvisioningRecord,
        site_options: dict[str, Any],
    ) -> TenantProvisioningRecord:
        """Run provisioning updating the given TenantProvisioningRecord in-place.

        This method is idempotent-safe when re-run against a record that is not `running`.
        """
        # guard: do not run if already finished
        if rec.status not in ("running", "pending"):
            return rec

        # Step 1: create site
        res = self.client.create_site(rec.organization_id, rec.tenant_id, site_options)
        self._update_details(session, rec, "create_site", dict(res))
        if res.get("status") != "success":
            self._finalize_failure(session, rec, f"create_site failed: {res}")
            return rec

        site_id = res.get("site_id")
        if not site_id:
            self._finalize_failure(
                session, rec, f"create_site returned no site_id: {res}"
            )
            return rec
        site_id = str(site_id)

        # install erpnext
        res_install = self.client.install_app(site_id, "erpnext")
        self._update_details(session, rec, "install_erpnext", dict(res_install))
        if res_install.get("status") != "success":
            self._finalize_failure(
                session, rec, f"install_erpnext failed: {res_install}"
            )
            return rec

        # optional custom app
        custom_app = site_options.get("custom_app")
        if custom_app:
            res_custom = self.client.install_app(site_id, str(custom_app))
            self._update_details(session, rec, "install_custom_app", dict(res_custom))
            if res_custom.get("status") != "success":
                self._finalize_failure(
                    session, rec, f"install_custom_app failed: {res_custom}"
                )
                return rec

        domain = site_options.get("domain")
        if domain:
            res_bind = self.client.bind_domain(site_id, str(domain))
            self._update_details(session, rec, "bind_domain", dict(res_bind))
            res_ssl = self.client.issue_ssl(site_id, str(domain))
            self._update_details(session, rec, "issue_ssl", dict(res_ssl))
            if res_ssl.get("status") != "success":
                self._finalize_failure(session, rec, f"issue_ssl failed: {res_ssl}")
                return rec
            if res_bind.get("status") != "success":
                self._finalize_failure(session, rec, f"bind_domain failed: {res_bind}")
                return rec

        # success
        # try to infer site_name/base_url from create_site response
        raw_site_name = res.get("site_name")
        site_name = str(raw_site_name) if raw_site_name is not None else None
        raw_base_url = res.get("base_url")
        base_url = str(raw_base_url) if raw_base_url is not None else None
        self._finalize_success(
            session, rec, site_id, site_name=site_name, base_url=base_url
        )
        return rec
