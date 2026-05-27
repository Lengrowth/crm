from __future__ import annotations

import httpx
import pytest

from app.integrations.erpnext.http import ERPNextHTTPClient


def test_create_site_success(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = {"site_id": "site-123", "site_name": "site.example", "status": "success"}

    def fake_request(method: str, url: str, **_: object) -> httpx.Response:
        request = httpx.Request(method, url)
        return httpx.Response(201, json=payload, request=request)

    monkeypatch.setattr(httpx, "request", fake_request)

    client = ERPNextHTTPClient(base_url="https://erp.example")
    response = client.create_site("org1", "tenant1", {})

    assert response.get("status") == "success"
    assert response.get("site_id") == "site-123"


def test_create_site_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_request(method: str, url: str, **_: object) -> httpx.Response:
        request = httpx.Request(method, url)
        return httpx.Response(500, content=b"server error", request=request)

    monkeypatch.setattr(httpx, "request", fake_request)

    client = ERPNextHTTPClient(base_url="https://erp.example")
    response = client.create_site("org1", "tenant1", {})

    assert response.get("status") == "failed"
    assert "error" in response
