from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.api.dependencies import get_db_session
from app.db.base import Base
from app.main import app
from app.schemas.auth import AuthRegisterRequest
from app.services.auth_service import AuthService


class AuthApiErrorTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        db_path = Path(cls.temp_dir.name) / "auth-api-errors.db"
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
        self.email = f"{self._testMethodName}@example.test"
        AuthService().register(
            self.session,
            AuthRegisterRequest(
                email=self.email,
                full_name="API Errors",
                password="correct-password-123",
                organization_name="API Errors Workspace",
                membership_role="owner",
                is_platform_admin=False,
            ),
        )

        def get_test_db():
            yield self.session

        app.dependency_overrides[get_db_session] = get_test_db
        self.client = TestClient(app)

    def tearDown(self) -> None:
        self.client.close()
        app.dependency_overrides.clear()
        self.session.close()

    def test_invalid_login_is_a_client_error_with_json_detail(self) -> None:
        response = self.client.post(
            "/auth/login",
            json={"email": self.email, "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid email or password."})

    def test_invalid_reset_token_is_a_client_error_with_json_detail(self) -> None:
        response = self.client.post(
            "/auth/password-reset/confirm",
            json={"token": "not-a-real-token", "new_password": "new-password-123"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid or expired token."})


if __name__ == "__main__":
    unittest.main()
