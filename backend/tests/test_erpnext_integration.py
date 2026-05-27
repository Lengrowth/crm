from __future__ import annotations

from fastapi.testclient import TestClient

from app.api.integrations import erp_service
from app.api.router import api_router
from app.integrations.mock_erpnext import MockERPNextClient
from app.services.erpnext_service import ERPNextService


def test_mock_client_create_and_status():
    client = MockERPNextClient()
    res = client.create_site("org1", "tenant1", {})
    assert res.get("status") == "success"
    site_id = str(res.get("site_id"))
    status = client.get_site_status(site_id)
    assert status.get("status") == "healthy"


def test_service_provision_success():
    mock = MockERPNextClient()
    svc = ERPNextService(mock)
    rec = svc.provision_tenant(
        "org1", "tenant-x", {"custom_app": "custom_app", "domain": "acme.example"}
    )
    assert rec["status"] == "success"
    assert "site_id" in rec


def test_service_handles_failures():
    # configure mock to fail on install_app
    mock = MockERPNextClient(failures={"install_app": True})
    svc = ERPNextService(mock)
    rec = svc.provision_tenant("org1", "tenant-fail", {})
    assert rec["status"] == "failed"


def test_api_provision_and_poll():
    # use TestClient with our api_router; the integration router uses a default mock service
    client = TestClient(api_router)

    payload = {"custom_app": None, "domain": None, "options": {}}
    r = client.post("/organizations/org1/tenants/tenant-api/provision", json=payload)
    assert r.status_code == 202
    body = r.json()
    # should contain a provision record structure
    assert body["organization_id"] == "org1"
    provision_id = body["id"]

    # poll
    r2 = client.get(f"/provisioning/{provision_id}")
    assert r2.status_code == 200
    r2b = r2.json()
    assert r2b["status"] in ("running", "success")


def test_api_backup_restore_bind_domain():
    # create a fresh mock client and service, wire into module for testing
    mock = MockERPNextClient()
    svc = ERPNextService(mock)
    # create site
    res = mock.create_site("org1", "tenant-test", {})
    assert res.get("status") == "success"
    site_id = str(res.get("site_id"))

    # backup
    b = svc.backup_site(site_id)
    assert b.get("status") == "success"
    backup_id = str(b.get("backup_id"))

    # restore
    r = svc.restore_site(site_id, backup_id)
    assert r.get("status") == "success"

    # bind domain
    br = svc.bind_domain(site_id, "example.test")
    assert br.get("status") == "success"
