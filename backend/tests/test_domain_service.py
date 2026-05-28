from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.schemas.auth import AuthRegisterRequest
from app.schemas.domain_management import DomainCreateRequest, ManualActivationRequest
from app.services.auth_service import AuthService
from app.services.domain_service import DomainService, DomainValidationError


class DomainServiceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "domain-service-test.db"
        cls.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            future=True,
        )
        Base.metadata.create_all(bind=cls.engine)
        cls.session_factory = sessionmaker(
            bind=cls.engine, autocommit=False, autoflush=False, future=True
        )
        cls.auth_service = AuthService()
        cls.domain_service = DomainService()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()
        cls.temp_dir.cleanup()

    def test_create_and_manual_activate(self) -> None:
        session = self.session_factory()
        try:
            # create an admin user/organization/tenant via auth_service.register
            register_response = self.auth_service.register(
                session,
                AuthRegisterRequest(
                    email="owner@example.test",
                    full_name="Local Owner",
                    password="local-password-123",
                    organization_name="Local Workspace",
                    membership_role="owner",
                    is_platform_admin=True,
                ),
            )
            context = self.auth_service.get_context(
                session, register_response.access_token
            )
            user = context.user

            org_id = context.memberships[0].organization_id
            from app.models.domain import Tenant

            tenant = Tenant(
                organization_id=org_id,
                tenant_slug="acme-test",
                environment="demo",
                status="planned",
            )
            session.add(tenant)
            session.flush()

            payload = DomainCreateRequest(
                domain="example.test", dns_target="target.example.test"
            )
            created = self.domain_service.create_domain(session, tenant.id, payload)

            self.assertEqual(created.domain, "example.test")
            self.assertFalse(
                created.manual_activation_required is True
                and created.is_active is False
            )

            # manual activate
            man_req = ManualActivationRequest(
                activate=True, notes="manual enable for test"
            )
            activated = self.domain_service.manual_activate(
                session, tenant.id, created.id, user, man_req
            )
            self.assertTrue(activated.is_active)
            self.assertIsNotNone(activated.manual_activation_by)
            self.assertIn("manual_activations", activated.notes_json)
        finally:
            session.close()

    def test_invalid_domain_fails(self) -> None:
        session = self.session_factory()
        try:
            # create tenant
            from app.models.domain import Tenant

            tenant = Tenant(
                organization_id="org-x",
                tenant_slug="bad-domain-test",
                environment="demo",
                status="planned",
            )
            session.add(tenant)
            session.flush()

            payload = DomainCreateRequest(domain="not a domain")
            with self.assertRaises(DomainValidationError):
                self.domain_service.create_domain(session, tenant.id, payload)
        finally:
            session.close()


if __name__ == "__main__":
    unittest.main()
