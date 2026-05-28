from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_current_user
from app.db.base import Base
from app.db.session import get_db_session
from app.main import app
from app.models.domain import Organization, SaaSUser, Tenant
from app.models.erpnext import ERPNextIntegrationMetadata


@pytest.fixture()
def client_with_tenant():
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "erpnext-cutover-mapping.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    session = Session()

    organization = Organization(name="Cutover Org", status="active")
    session.add(organization)
    session.flush()

    user = SaaSUser(
        email="cutover-admin@example.test",
        full_name="Cutover Admin",
        is_platform_admin=True,
        status="active",
    )
    session.add(user)
    session.flush()

    tenant = Tenant(
        organization_id=organization.id,
        tenant_slug="champion",
        environment="production",
        status="planned",
        provisioning_status="pending",
    )
    session.add(tenant)
    session.commit()
    session.refresh(user)
    session.refresh(tenant)

    def override_get_db_session():
        try:
            yield session
        finally:
            pass

    def override_get_current_user():
        return user

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        with TestClient(app) as client:
            yield client, session, tenant
    finally:
        app.dependency_overrides.clear()
        session.close()
        engine.dispose()
        temp_dir.cleanup()


def test_get_tenant_mapping_defaults_before_cutover(client_with_tenant) -> None:
    client, _, tenant = client_with_tenant

    response = client.get(f"/tenants/{tenant.id}/integration/erpnext")

    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"] == tenant.id
    assert data["configured"] is False
    assert data["site_id"] is None
    assert data["provisioning_status"] == "pending"
    assert data["tenant_status"] == "planned"


def test_put_tenant_mapping_persists_manual_cutover_state(client_with_tenant) -> None:
    client, session, tenant = client_with_tenant

    payload = {
        "site_id": "champion.lenquant.com",
        "site_name": "champion.lenquant.com",
        "base_url": "https://demo-erp.lenquant.com/",
        "api_key_ref": "sm://erpnext/champion/api-key",
        "api_secret_ref": "sm://erpnext/champion/api-secret",
        "metadata": {"cutover_batch": "pilot-1", "validated_by": "ops"},
    }

    response = client.put(f"/tenants/{tenant.id}/integration/erpnext", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["configured"] is True
    assert data["site_id"] == "champion.lenquant.com"
    assert data["site_name"] == "champion.lenquant.com"
    assert data["base_url"] == "https://demo-erp.lenquant.com"
    assert data["api_key_ref"] == "sm://erpnext/champion/api-key"
    assert data["api_secret_ref"] == "sm://erpnext/champion/api-secret"
    assert data["provisioning_status"] == "ready"
    assert data["tenant_status"] == "ready"
    assert data["metadata"]["cutover_batch"] == "pilot-1"
    assert data["metadata"]["mapping_source"] == "phase_18_manual_cutover"

    session.refresh(tenant)
    assert tenant.erpnext_site_name == "champion.lenquant.com"
    assert tenant.erpnext_base_url == "https://demo-erp.lenquant.com"
    assert tenant.erpnext_api_key_ref == "sm://erpnext/champion/api-key"
    assert tenant.erpnext_api_secret_ref == "sm://erpnext/champion/api-secret"
    assert tenant.provisioning_status == "ready"
    assert tenant.status == "ready"

    metadata = (
        session.query(ERPNextIntegrationMetadata)
        .filter_by(tenant_id=tenant.id)
        .one_or_none()
    )
    assert metadata is not None
    assert metadata.site_id == "champion.lenquant.com"
    assert metadata.site_name == "champion.lenquant.com"
    assert metadata.base_url == "https://demo-erp.lenquant.com"
    assert metadata.metadata_json["validated_by"] == "ops"
