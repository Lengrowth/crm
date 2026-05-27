from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.schemas.auth import AuthLoginRequest, AuthRegisterRequest
from app.services.auth_service import AuthError, AuthService


class AuthFlowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "auth-test.db"
        cls.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            future=True,
        )
        Base.metadata.create_all(bind=cls.engine)
        cls.session_factory = sessionmaker(bind=cls.engine, autocommit=False, autoflush=False, future=True)
        cls.auth_service = AuthService()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()
        cls.temp_dir.cleanup()

    def test_register_login_me_and_logout_flow(self) -> None:
        register_session = self.session_factory()
        register_response = None
        try:
            register_response = self.auth_service.register(
                register_session,
                AuthRegisterRequest(
                    email="owner@example.test",
                    full_name="Local Owner",
                    password="local-password-123",
                    organization_name="Local Workspace",
                    membership_role="owner",
                    is_platform_admin=True,
                ),
            )
        finally:
            register_session.close()

        self.assertIsNotNone(register_response)
        assert register_response is not None
        self.assertEqual(register_response.user.email, "owner@example.test")
        self.assertTrue(register_response.user.is_platform_admin)
        self.assertEqual(register_response.user.memberships[0].organization_name, "Local Workspace")

        login_session = self.session_factory()
        login_response = None
        try:
            login_response = self.auth_service.login(
                login_session,
                AuthLoginRequest(email="owner@example.test", password="local-password-123"),
            )
        finally:
            login_session.close()

        self.assertIsNotNone(login_response)
        assert login_response is not None
        token = login_response.access_token

        me_session = self.session_factory()
        context = None
        try:
            context = self.auth_service.get_context(me_session, token)
            self.assertIsNotNone(context)
            assert context is not None
            self.assertEqual(context.user.full_name, "Local Owner")
            self.assertEqual(context.memberships[0].role, "owner")

            self.auth_service.logout(me_session, context.session)
        finally:
            me_session.close()

        expired_session = self.session_factory()
        try:
            with self.assertRaises(AuthError):
                self.auth_service.get_context(expired_session, token)
        finally:
            expired_session.close()


if __name__ == "__main__":
    unittest.main()
