from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.main import app
from app.schemas.auth import AuthRegisterRequest
from app.schemas.domain_management import DomainCreateRequest
from app.services.auth_service import AuthService


class DomainAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "domain-api-test.db"
        cls.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            future=True,
        )
        Base.metadata.create_all(bind=cls.engine)
        cls.Session = sessionmaker(
            bind=cls.engine, autocommit=False, autoflush=False, future=True
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()
        cls.temp_dir.cleanup()

    def setUp(self) -> None:
        self.session = self.Session()
        self.auth_service = AuthService()

        # Create a platform admin user for testing
        reg = self.auth_service.register(
            self.session,
            AuthRegisterRequest(
                email="api-admin@example.test",
                full_name="API Admin",
                password="pw",
                organization_name="API Org",
                membership_role="owner",
                is_platform_admin=True,
            ),
        )
        # fetch user from session
        context = self.auth_service.get_context(self.session, reg.access_token)
        self.user = context.user

        # create a tenant directly
        from app.models.domain import Tenant

        tenant = Tenant(
            organization_id=self.user.id,
            tenant_slug="api-tenant",
            environment="demo",
            status="planned",
        )
        self.session.add(tenant)
        self.session.flush()
        self.tenant = tenant

        # override dependencies to use test session and user
        def _get_test_db():
            try:
                yield self.session
            finally:
                pass

        def _get_current_user():
            return self.user

        app.dependency_overrides["get_db_session"] = _get_test_db  # type: ignore[index]
        app.dependency_overrides["get_current_user"] = _get_current_user  # type: ignore[index]

        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.session.close()
        app.dependency_overrides.clear()

    def test_create_update_and_manual_activate(self) -> None:
        # create domain
        payload = {"domain": "api.example.test", "dns_target": "target.api.test"}
        resp = self.client.post(f"/tenants/{self.tenant.id}/domains", json=payload)
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["domain"], "api.example.test")
        domain_id = data["id"]

        # patch domain
        patch = {"dns_target": "new.target.test", "is_active": False}
        resp2 = self.client.patch(
            f"/tenants/{self.tenant.id}/domains/{domain_id}", json=patch
        )
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertEqual(data2["dns_target"], "new.target.test")
        self.assertFalse(data2["is_active"])

        # manual activate (activate true)
        resp3 = self.client.post(
            f"/tenants/{self.tenant.id}/domains/{domain_id}/manual_activate",
            json={"activate": True, "notes": "ops enable"},
        )
        self.assertEqual(resp3.status_code, 200)
        data3 = resp3.json()
        self.assertTrue(data3["is_active"])
        self.assertEqual(data3["manual_activation_by"], self.user.id)


if __name__ == "__main__":
    unittest.main()
