from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.domain import IdentifiedModel


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DomainOut(IdentifiedModel, ORMBaseModel):
    tenant_id: str
    domain: str
    type: str
    status: str
    dns_target: Optional[str] = None
    is_active: bool
    manual_activation_required: bool
    dns_verified_at: Optional[datetime] = None
    ssl_status: str
    verified_at: Optional[datetime] = None
    manual_activation_by: Optional[str] = None
    manual_activation_at: Optional[datetime] = None
    notes_json: dict[str, object]


class DomainCreateRequest(ORMBaseModel):
    domain: str
    type: Optional[str] = "custom"
    dns_target: Optional[str] = None
    manual_activation_required: Optional[bool] = False


class DomainUpdateRequest(ORMBaseModel):
    domain: Optional[str] = None
    dns_target: Optional[str] = None
    is_active: Optional[bool] = None
    manual_activation_required: Optional[bool] = None
    ssl_status: Optional[str] = None
    notes_json: Optional[dict[str, object]] = None


class ManualActivationRequest(ORMBaseModel):
    activate: bool
    notes: Optional[str] = None
