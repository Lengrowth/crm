from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.api.dependencies import get_current_user, get_db_session
from app.core.config import settings
from app.core.hardening import rate_limiter
from app.db.base import Base
from app.main import app
from app.models.domain import AuditLog, Tenant
from app.schemas.auth import AuthRegisterRequest
from app.schemas.control import OrganizationCreateRequest, TenantCreateRequest, TenantLifecycleActionRequest
from app.services.auth_service import AuthService
from app.services.control_plane_service import ControlPlaneService


class Phase19HardeningTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "phase19-test.db"
        cls.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            future=True,
        )
        Base.metadata.create_all(bind=cls.engine)
        cls.session_factory = sessionmaker(bind=cls.engine, autocommit=False, autoflush=False, future=True)
        cls.auth_service = AuthService()
        cls.control_service = ControlPlaneService()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()
        cls.temp_dir.cleanup()

    def setUp(self) -> None:
        self.session = self.session_factory()
        rate_limiter.reset()
        self._previous_environment = settings.environment
        self._previous_rate_limit_enabled = settings.rate_limit_enabled
        self._previous_rate_limit_max_requests = settings.rate_limit_max_requests
        self._previous_rate_limit_window_seconds = settings.rate_limit_window_seconds
        self._previous_rate_limit_exempt_paths = settings.rate_limit_exempt_paths
        self._previous_security_headers_enabled = settings.security_headers_enabled

        admin_email = f"phase19-admin+{self._testMethodName}@example.test"
        register_response = self.auth_service.register(
            self.session,
            AuthRegisterRequest(
                email=admin_email,
                full_name="Phase 19 Admin",
                password="local-password-123",
                organization_name="Phase 19 Workspace",
                membership_role="owner",
                is_platform_admin=True,
            ),
        )
        context = self.auth_service.get_context(self.session, register_response.access_token)
        self.user = context.user

        organization = self.control_service.create_organization(
            self.session,
            self.user,
            OrganizationCreateRequest(
                name="Phase 19 Client",
                legal_name="Phase 19 Client LLC",
                industry="drilling",
                country="United States",
                timezone="UTC",
                billing_email="ops@phase19.example.test",
                status="trial",
            ),
        )
        self.organization = organization
        # This fixture represents a tenant that already completed the protected
        # provisioning workflow; direct control-plane creation cannot set ready.
        self.tenant = Tenant(
            organization_id=organization.id,
            tenant_slug=f"phase19-client-{self._testMethodName}",
            environment="production",
            status="ready",
            primary_domain="phase19.example.test",
            custom_domain="ops.phase19.example.test",
            erpnext_site_name="phase19.example.test",
            erpnext_base_url="https://phase19.example.test",
            provisioning_status="ready",
        )
        self.session.add(self.tenant)
        self.session.commit()
        self.session.refresh(self.tenant)

        def override_get_db_session():
            try:
                yield self.session
            finally:
                pass

        def override_get_current_user():
            return self.user

        app.dependency_overrides[get_db_session] = override_get_db_session
        app.dependency_overrides[get_current_user] = override_get_current_user
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        rate_limiter.reset()
        settings.environment = self._previous_environment
        settings.rate_limit_enabled = self._previous_rate_limit_enabled
        settings.rate_limit_max_requests = self._previous_rate_limit_max_requests
        settings.rate_limit_window_seconds = self._previous_rate_limit_window_seconds
        settings.rate_limit_exempt_paths = self._previous_rate_limit_exempt_paths
        settings.security_headers_enabled = self._previous_security_headers_enabled
        self.client.close()
        self.session.rollback()
        self.session.close()

    def test_tenant_suspend_and_reactivate_are_audited(self) -> None:
        suspend_response = self.client.post(
            f"/tenants/{self.tenant.id}/suspend",
            json={"reason": "billing hold"},
        )
        self.assertEqual(suspend_response.status_code, 200)
        self.assertEqual(suspend_response.json()["status"], "suspended")

        reactivate_response = self.client.post(
            f"/tenants/{self.tenant.id}/reactivate",
            json={"reason": "billing cleared"},
        )
        self.assertEqual(reactivate_response.status_code, 200)
        self.assertEqual(reactivate_response.json()["status"], "ready")

        audit_rows = (
            self.session.query(AuditLog)
            .filter(AuditLog.tenant_id == self.tenant.id)
            .order_by(AuditLog.created_at.asc())
            .all()
        )
        self.assertEqual([row.action for row in audit_rows], ["tenant.suspended", "tenant.reactivated"])
        self.assertEqual(audit_rows[0].metadata_json["reason"], "billing hold")
        self.assertEqual(audit_rows[1].metadata_json["reason"], "billing cleared")

    def test_audit_log_endpoint_lists_recent_events_for_admin(self) -> None:
        self.client.post(f"/tenants/{self.tenant.id}/suspend", json={"reason": "ops"})
        response = self.client.get(f"/audit-logs?tenant_id={self.tenant.id}&limit=10")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertGreaterEqual(len(body), 1)
        self.assertEqual(body[0]["tenant_id"], self.tenant.id)
        self.assertEqual(body[0]["action"], "tenant.suspended")

    def test_rate_limit_triggers_when_enabled(self) -> None:
        settings.environment = "production"
        settings.rate_limit_enabled = True
        settings.rate_limit_max_requests = 1
        settings.rate_limit_window_seconds = 60
        settings.rate_limit_exempt_paths = "/health,/docs,/openapi.json,/redoc"
        rate_limiter.reset()

        first_response = self.client.get("/")
        second_response = self.client.get("/")

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 429)
        self.assertEqual(second_response.json()["detail"], "Rate limit exceeded.")


if __name__ == "__main__":
    unittest.main()
