from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.schemas.auth import AuthRegisterRequest
from app.schemas.control import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    TenantCreateRequest,
    TenantUpdateRequest,
)
from app.services.auth_service import AuthService
from app.services.control_plane_service import (
    ControlPlaneAccessError,
    ControlPlaneService,
    ControlPlaneValidationError,
)


class ControlPlaneTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "control-plane-test.db"
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

    def test_organization_and_tenant_crud_respects_memberships(self) -> None:
        admin_session = self.session_factory()
        admin_context = None
        client_org = None
        tenant = None
        try:
            admin_response = self.auth_service.register(
                admin_session,
                AuthRegisterRequest(
                    email="admin@example.test",
                    full_name="Admin User",
                    password="local-password-123",
                    organization_name="Admin Workspace",
                    membership_role="owner",
                    is_platform_admin=True,
                ),
            )
            admin_context = self.auth_service.get_context(admin_session, admin_response.access_token)
            client_org = self.control_service.create_organization(
                admin_session,
                admin_context.user,
                OrganizationCreateRequest(
                    name="Client Alpha",
                    legal_name="Client Alpha LLC",
                    industry="drilling",
                    country="United States",
                    timezone="UTC",
                    billing_email="finance@client-alpha.test",
                    status="trial",
                ),
            )
            tenant = self.control_service.create_tenant(
                admin_session,
                admin_context.user,
                TenantCreateRequest(
                    organization_id=client_org.id,
                    tenant_slug="client-alpha-demo",
                    environment="demo",
                    status="planned",
                    primary_domain="alpha.example.test",
                    custom_domain="ops.alpha.example.test",
                    erpnext_site_name="alpha.example.test",
                    erpnext_base_url="https://alpha.example.test",
                    provisioning_status="pending",
                ),
                client_org.id,
            )

            updated_org = self.control_service.update_organization(
                admin_session,
                admin_context.user,
                client_org.id,
                OrganizationUpdateRequest(status="active"),
            )
            with self.assertRaises(ControlPlaneValidationError):
                self.control_service.update_tenant(
                    admin_session,
                    admin_context.user,
                    tenant.id,
                    TenantUpdateRequest(status="ready"),
                )
            self.assertEqual(updated_org.status, "active")
            admin_session.refresh(tenant)
            self.assertEqual(tenant.status, "planned")
        finally:
            admin_session.close()

        member_session = self.session_factory()
        member_context = None
        try:
            member_response = self.auth_service.register(
                member_session,
                AuthRegisterRequest(
                    email="member@example.test",
                    full_name="Member User",
                    password="local-password-123",
                    organization_name="Member Workspace",
                    membership_role="admin",
                    is_platform_admin=False,
                ),
            )
            member_context = self.auth_service.get_context(member_session, member_response.access_token)

            visible_organizations = self.control_service.list_organizations(member_session, member_context.user)
            self.assertEqual(len(visible_organizations), 1)
            self.assertEqual(visible_organizations[0].name, "Member Workspace")

            with self.assertRaises(ControlPlaneAccessError):
                self.control_service.get_organization(member_session, member_context.user, client_org.id)

            with self.assertRaises(ControlPlaneAccessError):
                self.control_service.get_tenant(member_session, member_context.user, tenant.id)
        finally:
            member_session.close()


if __name__ == "__main__":
    unittest.main()
