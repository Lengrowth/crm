from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_platform_admin
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.schemas.domain import AuditLogRead
from app.services.audit_service import audit_service

router = APIRouter(tags=["audit"])


@router.get("/audit-logs", response_model=list[AuditLogRead])
def list_audit_logs(
    organization_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    limit: int = 100,
    session: Session = Depends(get_db_session),
    _: SaaSUser = Depends(require_platform_admin),
):
    return audit_service.list_events(
        session,
        organization_id=organization_id,
        tenant_id=tenant_id,
        limit=limit,
    )
