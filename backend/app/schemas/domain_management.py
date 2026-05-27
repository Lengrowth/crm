from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.domain import IdentifiedModel


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DomainOut(IdentifiedModel, ORMBaseModel):
    tenant_id: str
    domain: str
    type: str
    status: str
    dns_target: str | None = None
    is_active: bool
    manual_activation_required: bool
    dns_verified_at: datetime | None = None
    ssl_status: str
    verified_at: datetime | None = None
    manual_activation_by: str | None = None
    manual_activation_at: datetime | None = None
    notes_json: dict[str, object]


class DomainCreateRequest(ORMBaseModel):
    domain: str
    type: str | None = "custom"
    dns_target: str | None = None
    manual_activation_required: bool | None = False


class DomainUpdateRequest(ORMBaseModel):
    domain: str | None = None
    dns_target: str | None = None
    is_active: bool | None = None
    manual_activation_required: bool | None = None
    ssl_status: str | None = None
    notes_json: dict[str, object] | None = None


class ManualActivationRequest(ORMBaseModel):
    activate: bool
    notes: str | None = None
