from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

OrganizationStatus = Literal["lead", "trial", "active", "suspended", "cancelled", "archived"]
TenantEnvironment = Literal["demo", "staging", "production"]
TenantStatus = Literal["planned", "provisioning", "ready", "suspended", "failed", "archived"]
ProvisioningStatus = Literal["pending", "queued", "running", "ready", "failed"]


class ControlBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrganizationCreateRequest(ControlBaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: Optional[str] = Field(default=None, max_length=255)
    industry: Optional[str] = Field(default=None, max_length=120)
    country: Optional[str] = Field(default=None, max_length=120)
    timezone: Optional[str] = Field(default=None, max_length=120)
    billing_email: Optional[str] = Field(default=None, max_length=255)
    status: OrganizationStatus = "lead"


class OrganizationUpdateRequest(ControlBaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    legal_name: Optional[str] = Field(default=None, max_length=255)
    industry: Optional[str] = Field(default=None, max_length=120)
    country: Optional[str] = Field(default=None, max_length=120)
    timezone: Optional[str] = Field(default=None, max_length=120)
    billing_email: Optional[str] = Field(default=None, max_length=255)
    status: Optional[OrganizationStatus] = None


class TenantCreateRequest(ControlBaseModel):
    organization_id: Optional[str] = None
    tenant_slug: str = Field(min_length=1, max_length=120)
    environment: TenantEnvironment = "demo"
    status: TenantStatus = "planned"
    primary_domain: Optional[str] = Field(default=None, max_length=255)
    custom_domain: Optional[str] = Field(default=None, max_length=255)
    erpnext_site_name: Optional[str] = Field(default=None, max_length=255)
    erpnext_base_url: Optional[str] = Field(default=None, max_length=255)
    provisioning_status: ProvisioningStatus = "pending"

    @field_validator("tenant_slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Tenant slug is required.")
        return normalized


class TenantUpdateRequest(ControlBaseModel):
    tenant_slug: Optional[str] = Field(default=None, min_length=1, max_length=120)
    environment: Optional[TenantEnvironment] = None
    status: Optional[TenantStatus] = None
    primary_domain: Optional[str] = Field(default=None, max_length=255)
    custom_domain: Optional[str] = Field(default=None, max_length=255)
    erpnext_site_name: Optional[str] = Field(default=None, max_length=255)
    erpnext_base_url: Optional[str] = Field(default=None, max_length=255)
    provisioning_status: Optional[ProvisioningStatus] = None

    @field_validator("tenant_slug")
    @classmethod
    def normalize_slug(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Tenant slug is required.")
        return normalized


class TenantLifecycleActionRequest(ControlBaseModel):
    reason: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=1000)
