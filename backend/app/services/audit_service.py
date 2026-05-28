from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.domain import AuditLog


class AuditService:
    def record_event(
        self,
        session: Session,
        *,
        actor_user_id: Optional[str],
        organization_id: Optional[str],
        tenant_id: Optional[str],
        action: str,
        entity_type: str,
        entity_id: str,
        metadata_json: Optional[dict[str, object]] = None,
        ip_address: Optional[str] = None,
    ) -> AuditLog:
        record = AuditLog(
            actor_user_id=actor_user_id,
            organization_id=organization_id,
            tenant_id=tenant_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata_json=metadata_json or {},
            ip_address=ip_address,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

    def list_events(
        self,
        session: Session,
        *,
        organization_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        statement = select(AuditLog).order_by(AuditLog.created_at.desc())
        if organization_id is not None:
            statement = statement.where(AuditLog.organization_id == organization_id)
        if tenant_id is not None:
            statement = statement.where(AuditLog.tenant_id == tenant_id)

        safe_limit = max(1, min(limit, 500))
        return session.execute(statement.limit(safe_limit)).scalars().all()


audit_service = AuditService()
