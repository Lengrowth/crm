from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.integrations.mock_erpnext import MockERPNextClient
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

    org = "org-test"
    tenant = "tenant-test"
    site_options = {"domain": "example.test", "custom_app": "myapp"}

    prov_id = worker.run(session, org, tenant, site_options)

    # assert provisioning record exists and is success
    rec = session.query(TenantProvisioningRecord).filter_by(id=prov_id).one_or_none()
    assert rec is not None
    assert rec.status == "success"
    assert rec.details.get("create_site", {}).get("status") == "success"

    # assert integration metadata updated
    meta = (
        session.query(ERPNextIntegrationMetadata)
        .filter_by(tenant_id=tenant)
        .one_or_none()
    )
    assert meta is not None
    assert meta.site_id is not None
    assert meta.site_name is not None
