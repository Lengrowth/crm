from __future__ import annotations

import re
import tempfile
from pathlib import Path
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.schemas.auth import (
    AuthEmailVerificationConfirm,
    AuthEmailVerificationRequest,
    AuthLoginRequest,
    AuthPasswordResetConfirm,
    AuthPasswordResetRequest,
    AuthRegisterRequest,
)
from app.services.auth_service import AuthError, AuthService


class RecordingEmailSender:
    def __init__(self) -> None:
        self.messages: list[dict[str, object]] = []

    def send_transactional_email(self, to: list[str], subject: str, text: str) -> None:
        self.messages.append({"to": to, "subject": subject, "text": text})


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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.engine.dispose()
        cls.temp_dir.cleanup()

    def _make_service(self) -> tuple[AuthService, RecordingEmailSender]:
        sender = RecordingEmailSender()
        return AuthService(email_sender=sender), sender

    @staticmethod
    def _extract_token(message_text: str) -> str:
        match = re.search(r"[?&]token=([A-Za-z0-9_\-]+)", message_text)
        assert match is not None, f"Could not find token in email body: {message_text}"
        return match.group(1)

    def test_register_login_me_and_logout_flow(self) -> None:
        auth_service, sender = self._make_service()
        register_session = self.session_factory()
        register_response = None
        try:
            register_response = auth_service.register(
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
        self.assertIsNone(register_response.user.email_verified_at)
        self.assertEqual(len(sender.messages), 1)

        login_session = self.session_factory()
        login_response = None
        try:
            login_response = auth_service.login(
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
            context = auth_service.get_context(me_session, token)
            self.assertIsNotNone(context)
            assert context is not None
            self.assertEqual(context.user.full_name, "Local Owner")
            self.assertEqual(context.memberships[0].role, "owner")

            auth_service.logout(me_session, context.session)
        finally:
            me_session.close()

        expired_session = self.session_factory()
        try:
            with self.assertRaises(AuthError):
                auth_service.get_context(expired_session, token)
        finally:
            expired_session.close()

    def test_email_verification_flow_is_one_time_use(self) -> None:
        auth_service, sender = self._make_service()
        register_session = self.session_factory()
        try:
            auth_service.register(
                register_session,
                AuthRegisterRequest(
                    email="verify@example.test",
                    full_name="Verify User",
                    password="local-password-123",
                    organization_name="Verification Workspace",
                    membership_role="owner",
                    is_platform_admin=False,
                ),
            )
            register_session.commit()
        finally:
            register_session.close()

        initial_token = self._extract_token(str(sender.messages[-1]["text"]))

        resend_session = self.session_factory()
        try:
            resend_response = auth_service.request_email_verification(
                resend_session,
                AuthEmailVerificationRequest(email="verify@example.test"),
            )
            self.assertIn("verification link", resend_response.detail.lower())
            resend_session.commit()
        finally:
            resend_session.close()

        resend_token = self._extract_token(str(sender.messages[-1]["text"]))
        self.assertNotEqual(initial_token, resend_token)

        verify_session = self.session_factory()
        try:
            verify_response = auth_service.verify_email(
                verify_session,
                AuthEmailVerificationConfirm(token=resend_token),
            )
            self.assertEqual(verify_response.detail, "Email address verified successfully.")
            verify_session.commit()
        finally:
            verify_session.close()

        assert self.session_factory is not None
        check_session = self.session_factory()
        try:
            user = auth_service._get_user_by_email(check_session, "verify@example.test")
            self.assertIsNotNone(user)
            assert user is not None
            self.assertIsNotNone(user.email_verified_at)

            with self.assertRaises(AuthError):
                auth_service.verify_email(
                    check_session,
                    AuthEmailVerificationConfirm(token=resend_token),
                )
            with self.assertRaises(AuthError):
                auth_service.verify_email(
                    check_session,
                    AuthEmailVerificationConfirm(token=initial_token),
                )
        finally:
            check_session.close()

    def test_password_reset_flow_revokes_sessions_and_changes_password(self) -> None:
        auth_service, sender = self._make_service()
        register_session = self.session_factory()
        try:
            auth_service.register(
                register_session,
                AuthRegisterRequest(
                    email="reset@example.test",
                    full_name="Reset User",
                    password="old-password-123",
                    organization_name="Reset Workspace",
                    membership_role="owner",
                    is_platform_admin=False,
                ),
            )
        finally:
            register_session.close()

        login_session = self.session_factory()
        try:
            login_response = auth_service.login(
                login_session,
                AuthLoginRequest(email="reset@example.test", password="old-password-123"),
            )
        finally:
            login_session.close()

        token_before_reset = login_response.access_token

        reset_request_session = self.session_factory()
        try:
            reset_response = auth_service.request_password_reset(
                reset_request_session,
                AuthPasswordResetRequest(email="reset@example.test"),
            )
            self.assertIn("password reset link", reset_response.detail.lower())
        finally:
            reset_request_session.close()

        reset_token = self._extract_token(str(sender.messages[-1]["text"]))

        reset_confirm_session = self.session_factory()
        try:
            confirm_response = auth_service.reset_password(
                reset_confirm_session,
                AuthPasswordResetConfirm(token=reset_token, new_password="new-password-456"),
            )
            self.assertEqual(confirm_response.detail, "Password updated successfully.")
        finally:
            reset_confirm_session.close()

        check_session = self.session_factory()
        try:
            with self.assertRaises(AuthError):
                auth_service.get_context(check_session, token_before_reset)

            with self.assertRaises(AuthError):
                auth_service.login(
                    check_session,
                    AuthLoginRequest(email="reset@example.test", password="old-password-123"),
                )

            new_login = auth_service.login(
                check_session,
                AuthLoginRequest(email="reset@example.test", password="new-password-456"),
            )
            self.assertEqual(new_login.user.email, "reset@example.test")

            with self.assertRaises(AuthError):
                auth_service.reset_password(
                    check_session,
                    AuthPasswordResetConfirm(token=reset_token, new_password="another-password-789"),
                )
        finally:
            check_session.close()


if __name__ == "__main__":
    unittest.main()
