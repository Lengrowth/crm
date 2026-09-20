#!/usr/bin/env python3
"""Remove only the exact synthetic Phase 2 browser records from staging."""

from __future__ import annotations

import argparse
import json
import re
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
    ModuleApplicationStatus,
    ModuleEntitlementAudit,
    ModuleEntitlementRequest,
    OrganizationModule,
)
from app.models.erpnext import ERPNextIntegrationMetadata, TenantProvisioningRecord


STALE_PHASE2_ORGANIZATION_PATTERNS = (
    re.compile(r"^Phase 2 Browser (Alpha|Beta)(?: Updated)? [a-z0-9-]+$", re.IGNORECASE),
    re.compile(r"^Phase 2 Browser UI Company [a-z0-9-]+$", re.IGNORECASE),
)


def discover_stale_phase2_records() -> dict[str, list[str]]:
    with SessionLocal() as session:
        rows = session.query(Organization.id, Organization.name, Organization.status).all()
        organization_ids = [
            str(row.id)
            for row in rows
            if row.status in {"trial", "lead"}
            and any(pattern.fullmatch(row.name or "") for pattern in STALE_PHASE2_ORGANIZATION_PATTERNS)
        ]
        tenant_ids = [
            str(row[0])
            for row in session.query(Tenant.id)
            .filter(Tenant.organization_id.in_(organization_ids))
            .all()
        ] if organization_ids else []
    return {"organization_ids": organization_ids, "tenant_ids": tenant_ids}


def remove_records(payload: dict[str, object]) -> tuple[int, int]:
    organization_ids = [str(value) for value in payload.get("organization_ids", [])]
    tenant_ids = [str(value) for value in payload.get("tenant_ids", [])]
    if not organization_ids:
        return 0, 0
    if any(len(value) != 36 for value in [*organization_ids, *tenant_ids]):
        raise SystemExit("Phase 2 cleanup requires exact UUID identifiers for organizations and optional tenants")

    with SessionLocal() as session:
        discovered_tenant_ids = [row[0] for row in session.query(Tenant.id).filter(Tenant.organization_id.in_(organization_ids)).all()]
        tenant_ids = list(dict.fromkeys([*tenant_ids, *discovered_tenant_ids]))
        project_ids = [row[0] for row in session.query(ImplementationProject.id).filter(ImplementationProject.organization_id.in_(organization_ids)).all()]
        if project_ids:
            session.execute(delete(ImplementationTask).where(ImplementationTask.implementation_project_id.in_(project_ids)))
            session.execute(delete(ImplementationProject).where(ImplementationProject.id.in_(project_ids)))
        session.execute(delete(DomainMapping).where(DomainMapping.tenant_id.in_(tenant_ids)))
        session.execute(delete(ProvisioningJob).where(ProvisioningJob.tenant_id.in_(tenant_ids)))
        session.execute(delete(TenantProvisioningRecord).where(TenantProvisioningRecord.tenant_id.in_(tenant_ids)))
        session.execute(delete(ERPNextIntegrationMetadata).where(ERPNextIntegrationMetadata.tenant_id.in_(tenant_ids)))
        session.execute(delete(ModuleApplicationStatus).where(ModuleApplicationStatus.tenant_id.in_(tenant_ids)))
        session.execute(delete(ModuleEntitlementAudit).where(ModuleEntitlementAudit.organization_id.in_(organization_ids)))
        session.execute(delete(ModuleEntitlementRequest).where(ModuleEntitlementRequest.organization_id.in_(organization_ids)))
        session.execute(delete(OrganizationModule).where(OrganizationModule.organization_id.in_(organization_ids)))
        session.execute(delete(AuditLog).where(AuditLog.organization_id.in_(organization_ids)))
        session.execute(delete(Tenant).where(Tenant.id.in_(tenant_ids), Tenant.organization_id.in_(organization_ids)))
        session.execute(delete(OrganizationMembership).where(OrganizationMembership.organization_id.in_(organization_ids)))
        session.execute(delete(Organization).where(Organization.id.in_(organization_ids)))
        session.commit()
    return len(organization_ids), len(tenant_ids)


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file")
    source.add_argument("--discover-stale", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    if args.discover_stale:
        payload = discover_stale_phase2_records()
    else:
        payload = json.loads(Path(args.file).read_text(encoding="utf-8"))
    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    organizations, tenants = remove_records(payload)
    print(f"phase2 synthetic cleanup passed: organizations={organizations} tenants={tenants}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
