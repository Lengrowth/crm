from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.integrations.mock_erpnext import MockERPNextClient
from app.models.domain import Organization, Tenant
from app.models.erpnext import ERPNextIntegrationMetadata, TenantProvisioningRecord
from app.workers.provisioning_worker import ProvisioningWorker


def make_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    return Session()


def test_provision_creates_records():
    session = make_session()
    client = MockERPNextClient()
    worker = ProvisioningWorker(client=client)

    organization = Organization(name="Provision Org", status="active")
    session.add(organization)
    session.flush()

    tenant = Tenant(
        organization_id=organization.id,
        tenant_slug="tenant-test",
        environment="staging",
        status="planned",
        provisioning_status="pending",
    )
    session.add(tenant)
    session.commit()
    session.refresh(tenant)

    site_options = {"domain": "example.test", "custom_app": "myapp"}

    prov_id = worker.run(session, organization.id, tenant.id, site_options)

    # assert provisioning record exists and is success
    rec = session.query(TenantProvisioningRecord).filter_by(id=prov_id).one_or_none()
    assert rec is not None
    assert rec.status == "success"
    details = rec.details or {}
    create_site_details = details.get("create_site")
    assert isinstance(create_site_details, dict)
    assert create_site_details.get("status") == "success"

    # assert integration metadata updated
    meta = (
        session.query(ERPNextIntegrationMetadata)
        .filter_by(tenant_id=tenant.id)
        .one_or_none()
    )
    assert meta is not None
    assert meta.site_id is not None
    assert meta.site_name is not None

    session.refresh(tenant)
    assert tenant.provisioning_status == "ready"
    assert tenant.status == "ready"
    assert tenant.erpnext_site_name == meta.site_name
