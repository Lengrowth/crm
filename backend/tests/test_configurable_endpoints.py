from __future__ import annotations

from app.core.config import settings
from app.services.communication_service import CommunicationService


def test_email_provider_endpoint_is_configurable(monkeypatch) -> None:
    monkeypatch.setattr(settings, "resend_api_url", "https://mail.example.test/send")

    service = CommunicationService()

    assert service.api_url == "https://mail.example.test/send"
