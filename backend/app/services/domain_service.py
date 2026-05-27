from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.domain import DomainMapping, SaaSUser


class DomainError(Exception):
    pass


class DomainNotFoundError(DomainError):
    pass


class DomainValidationError(DomainError):
    pass


class DomainAccessError(DomainError):
    pass


@dataclass(slots=True)
class DomainSummary:
    id: str
    tenant_id: str
    domain: str
    status: str


class DomainService:
    DOMAIN_REGEX = re.compile(r"^(?!-)[A-Za-z0-9-\.]{3,253}$")

    def list_domains(self, session: Session, tenant_id: str) -> list[DomainMapping]:
        statement = (
            select(DomainMapping)
            .where(DomainMapping.tenant_id == tenant_id)
            .order_by(DomainMapping.created_at.asc())
        )
        rows = session.execute(statement).scalars().all()
        return rows

    def create_domain(self, session: Session, tenant_id: str, payload) -> DomainMapping:
        # Basic domain validation
        domain = payload.domain.strip().lower()
        if not self._is_valid_domain(domain):
            raise DomainValidationError("Invalid domain format.")

        # ensure uniqueness
        existing = session.execute(
            select(DomainMapping).where(DomainMapping.domain == domain)
        ).scalar_one_or_none()
        if existing is not None:
            raise DomainValidationError("Domain already exists.")

        record = DomainMapping(
            tenant_id=tenant_id,
            domain=domain,
            type=payload.type or "custom",
            dns_target=payload.dns_target,
            manual_activation_required=bool(payload.manual_activation_required),
            status="pending_dns",
        )
        session.add(record)
        session.flush()
        session.commit()
        return record

    def update_domain(self, session: Session, domain_id: str, payload) -> DomainMapping:
        record = session.get(DomainMapping, domain_id)
        if record is None:
            raise DomainNotFoundError("Domain not found.")

        if payload.domain:
            domain = payload.domain.strip().lower()
            if not self._is_valid_domain(domain):
                raise DomainValidationError("Invalid domain format.")
            record.domain = domain

        if payload.dns_target is not None:
            record.dns_target = payload.dns_target

        if payload.is_active is not None:
            record.is_active = payload.is_active

        if payload.manual_activation_required is not None:
            record.manual_activation_required = payload.manual_activation_required

        if payload.ssl_status is not None:
            record.ssl_status = payload.ssl_status

        if payload.notes_json is not None:
            record.notes_json = payload.notes_json

        session.add(record)
        session.flush()
        session.commit()
        return record

    def mark_dns_verified(self, session: Session, domain_id: str) -> DomainMapping:
        record = session.get(DomainMapping, domain_id)
        if record is None:
            raise DomainNotFoundError("Domain not found.")
        record.dns_verified_at = datetime.now(timezone.utc)
        # do not change is_active or status automatically; operator will decide
        session.add(record)
        session.flush()
        session.commit()
        return record

    def set_ssl_status(
        self, session: Session, domain_id: str, status: str
    ) -> DomainMapping:
        record = session.get(DomainMapping, domain_id)
        if record is None:
            raise DomainNotFoundError("Domain not found.")
        record.ssl_status = status
        session.add(record)
        session.flush()
        session.commit()
        return record

    def manual_activate(
        self, session: Session, domain_id: str, user: SaaSUser, request
    ) -> DomainMapping:
        record = session.get(DomainMapping, domain_id)
        if record is None:
            raise DomainNotFoundError("Domain not found.")

        # Toggle manual activation state
        if request.activate:
            record.is_active = True
            record.manual_activation_by = user.id
            record.manual_activation_at = datetime.now(timezone.utc)
            record.status = "active"
        else:
            record.is_active = False
            record.manual_activation_by = user.id
            record.manual_activation_at = datetime.now(timezone.utc)
            record.status = "disabled"

        # append note if provided
        notes = record.notes_json or {}
        notes_entry = {
            "by": user.id,
            "at": datetime.now(timezone.utc).isoformat(),
            "activate": bool(request.activate),
        }
        if request.notes:
            notes_entry["notes"] = request.notes
        # append to a list inside notes_json under 'manual_activations'
        manual_list = notes.get("manual_activations", [])
        manual_list.append(notes_entry)
        notes["manual_activations"] = manual_list
        record.notes_json = notes

        session.add(record)
        session.flush()
        session.commit()
        return record

    def _is_valid_domain(self, domain: str) -> bool:
        # Very lightweight check suitable for metadata-only validation
        if " " in domain or len(domain) < 3:
            return False
        if "." not in domain:
            return False
        if not self.DOMAIN_REGEX.match(domain):
            return False
        return True
