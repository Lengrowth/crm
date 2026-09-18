from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_current_user
from app.api.router import api_router
from app.db.base import Base
from app.db.session import get_db_session
from app.integrations.mock_erpnext import MockERPNextClient
from app.models.domain import Organization, OrganizationMembership, SaaSUser, Tenant
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
    # Use a disposable authenticated tenant so this test covers the protected route.
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "erpnext-integration.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(
        bind=engine, autocommit=False, autoflush=False, future=True
    )
    session = session_factory()

    organization = Organization(name="Integration Org", status="active")
    session.add(organization)
    session.flush()
    user = SaaSUser(
        email="integration-owner@example.test",
        full_name="Integration Owner",
        status="active",
        is_platform_admin=True,
    )
    session.add(user)
    session.flush()
    session.add(
        OrganizationMembership(
            organization_id=organization.id, user_id=user.id, role="owner"
        )
    )
    tenant = Tenant(
        organization_id=organization.id,
        tenant_slug="tenant-api",
        environment="staging",
        status="planned",
        provisioning_status="pending",
    )
    session.add(tenant)
    session.commit()

    def override_get_db_session():
        yield session

    def override_get_current_user():
        return user

    test_app = FastAPI()
    test_app.include_router(api_router)
    test_app.dependency_overrides[get_db_session] = override_get_db_session
    test_app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        with TestClient(test_app) as client:
            payload = {"custom_app": None, "domain": None, "options": {}}
            r = client.post(
                f"/organizations/{organization.id}/tenants/{tenant.id}/provision",
                json=payload,
            )
            assert r.status_code == 403
            assert r.json()["detail"] == "Direct provisioning is disabled. Use an approved onboarding request."
            restore = client.post(
                f"/tenants/{tenant.id}/restore",
                params={"site_id": "caller-controlled-site"},
                json={"backup_id": "caller-controlled-backup"},
            )
            assert restore.status_code == 403
            assert "Direct ERP restore mutation is disabled" in restore.json()["detail"]
    finally:
        test_app.dependency_overrides.clear()
        session.close()
        engine.dispose()
        temp_dir.cleanup()


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
