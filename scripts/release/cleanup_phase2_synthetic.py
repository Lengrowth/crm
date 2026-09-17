#!/usr/bin/env python3
"""Remove only the exact synthetic Phase 2 browser records from staging."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sqlalchemy import delete

from app.db.session import SessionLocal
from app.models.domain import (
    AuditLog,
    DomainMapping,
    ImplementationProject,
    ImplementationTask,
    Organization,
    OrganizationMembership,
    ProvisioningJob,
    Tenant,
)
from app.models.erpnext import ERPNextIntegrationMetadata, TenantProvisioningRecord


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.file).read_text(encoding="utf-8"))
    organization_ids = [str(value) for value in payload.get("organization_ids", [])]
    tenant_ids = [str(value) for value in payload.get("tenant_ids", [])]
    if not organization_ids or not tenant_ids or any(len(value) != 36 for value in [*organization_ids, *tenant_ids]):
        raise SystemExit("Phase 2 cleanup requires exact UUID identifiers for organizations and tenants")

    with SessionLocal() as session:
        project_ids = [row[0] for row in session.query(ImplementationProject.id).filter(ImplementationProject.organization_id.in_(organization_ids)).all()]
        if project_ids:
            session.execute(delete(ImplementationTask).where(ImplementationTask.implementation_project_id.in_(project_ids)))
            session.execute(delete(ImplementationProject).where(ImplementationProject.id.in_(project_ids)))
        session.execute(delete(DomainMapping).where(DomainMapping.tenant_id.in_(tenant_ids)))
        session.execute(delete(ProvisioningJob).where(ProvisioningJob.tenant_id.in_(tenant_ids)))
        session.execute(delete(TenantProvisioningRecord).where(TenantProvisioningRecord.tenant_id.in_(tenant_ids)))
        session.execute(delete(ERPNextIntegrationMetadata).where(ERPNextIntegrationMetadata.tenant_id.in_(tenant_ids)))
        session.execute(delete(AuditLog).where(AuditLog.organization_id.in_(organization_ids)))
        session.execute(delete(Tenant).where(Tenant.id.in_(tenant_ids), Tenant.organization_id.in_(organization_ids)))
        session.execute(delete(OrganizationMembership).where(OrganizationMembership.organization_id.in_(organization_ids)))
        session.execute(delete(Organization).where(Organization.id.in_(organization_ids)))
        session.commit()
    print(f"phase2 synthetic cleanup passed: organizations={len(organization_ids)} tenants={len(tenant_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
