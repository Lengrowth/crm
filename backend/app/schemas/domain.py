from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdentifiedModel(ORMBaseModel):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class OrganizationRead(IdentifiedModel):
    name: str
    legal_name: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    billing_email: Optional[str] = None
    status: str


class TenantRead(IdentifiedModel):
    organization_id: str
    tenant_slug: str
    environment: str
    status: str
    primary_domain: Optional[str] = None
    custom_domain: Optional[str] = None
    erpnext_site_name: Optional[str] = None
    erpnext_base_url: Optional[str] = None
    provisioning_status: str


class PlanRead(IdentifiedModel):
    code: str
    name: str
    description: Optional[str] = None
    monthly_price_cents: int
    annual_price_cents: int
    is_active: bool


class ModuleRead(IdentifiedModel):
    code: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    is_active: bool


class AuditLogRead(ORMBaseModel):
    id: str
    created_at: datetime
    actor_user_id: Optional[str] = None
    organization_id: Optional[str] = None
    tenant_id: Optional[str] = None
    action: str
    entity_type: str
    entity_id: str
    metadata_json: dict[str, object]
    ip_address: Optional[str] = None
