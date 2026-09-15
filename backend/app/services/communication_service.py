from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings


class CommunicationError(Exception):
    pass


class CommunicationService:
    """Small service to send marketing/contact emails using Resend HTTP API.

    Expects RESEND_API_KEY and RESEND_FROM_EMAIL to be set in environment/settings.
    """

    def __init__(self) -> None:
        self.api_key = settings.resend_api_key
        self.api_url = settings.resend_api_url
        self.from_email = settings.resend_from_email
        self.contact_recipient = settings.marketing_contact_recipient

    def _auth_headers(self) -> dict[str, str]:
        if not self.api_key:
            raise CommunicationError("Resend API key is not configured")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send_contact_message(self, name: str, email: str, message: str) -> Any:
        subject = f"Website contact from {name} <{email}>"
        text = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}\n"
        return self._send_email(subject=subject, text=text, to=[self.contact_recipient])

    def send_demo_request(self, name: str, email: str, message: str) -> Any:
        subject = f"Demo request from {name} <{email}>"
        text = f"Name: {name}\nEmail: {email}\n\nRequest:\n{message}\n"
        return self._send_email(subject=subject, text=text, to=[self.contact_recipient])

    def send_transactional_email(self, to: list[str], subject: str, text: str) -> Any:
        return self._send_email(subject=subject, text=text, to=to)

    def _send_email(self, subject: str, text: str, to: list[str]) -> Any:
        payload = {
            "from": self.from_email,
            "to": to,
            "subject": subject,
            "text": text,
        }
        headers = self._auth_headers()
        with httpx.Client() as client:
            resp = client.post(
                self.api_url, json=payload, headers=headers, timeout=15.0
            )
        if resp.status_code >= 400:
            raise CommunicationError(
                f"failed to send email: {resp.status_code} - {resp.text}"
            )
        return resp.json()


communication_service = CommunicationService()
