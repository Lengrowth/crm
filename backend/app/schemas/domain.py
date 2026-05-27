from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdentifiedModel(ORMBaseModel):
    id: str
    created_at: datetime
    updated_at: datetime | None = None


class OrganizationRead(IdentifiedModel):
    name: str
    legal_name: str | None = None
    industry: str | None = None
    country: str | None = None
    timezone: str | None = None
    billing_email: str | None = None
    status: str


class TenantRead(IdentifiedModel):
    organization_id: str
    tenant_slug: str
    environment: str
    status: str
    primary_domain: str | None = None
    custom_domain: str | None = None
    erpnext_site_name: str | None = None
    erpnext_base_url: str | None = None
    provisioning_status: str


class PlanRead(IdentifiedModel):
    code: str
    name: str
    description: str | None = None
    monthly_price_cents: int
    annual_price_cents: int
    is_active: bool


class ModuleRead(IdentifiedModel):
    code: str
    name: str
    description: str | None = None
    category: str | None = None
    is_active: bool
