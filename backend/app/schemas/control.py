from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

OrganizationStatus = Literal["lead", "trial", "active", "suspended", "cancelled", "archived"]
TenantEnvironment = Literal["demo", "staging", "production"]
TenantStatus = Literal["planned", "provisioning", "ready", "suspended", "failed", "archived"]
ProvisioningStatus = Literal["pending", "queued", "running", "ready", "failed"]


class ControlBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrganizationCreateRequest(ControlBaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: str | None = Field(default=None, max_length=255)
    industry: str | None = Field(default=None, max_length=120)
    country: str | None = Field(default=None, max_length=120)
    timezone: str | None = Field(default=None, max_length=120)
    billing_email: str | None = Field(default=None, max_length=255)
    status: OrganizationStatus = "lead"


class OrganizationUpdateRequest(ControlBaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    legal_name: str | None = Field(default=None, max_length=255)
    industry: str | None = Field(default=None, max_length=120)
    country: str | None = Field(default=None, max_length=120)
    timezone: str | None = Field(default=None, max_length=120)
    billing_email: str | None = Field(default=None, max_length=255)
    status: OrganizationStatus | None = None


class TenantCreateRequest(ControlBaseModel):
    organization_id: str | None = None
    tenant_slug: str = Field(min_length=1, max_length=120)
    environment: TenantEnvironment = "demo"
    status: TenantStatus = "planned"
    primary_domain: str | None = Field(default=None, max_length=255)
    custom_domain: str | None = Field(default=None, max_length=255)
    erpnext_site_name: str | None = Field(default=None, max_length=255)
    erpnext_base_url: str | None = Field(default=None, max_length=255)
    provisioning_status: ProvisioningStatus = "pending"

    @field_validator("tenant_slug")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Tenant slug is required.")
        return normalized


class TenantUpdateRequest(ControlBaseModel):
    tenant_slug: str | None = Field(default=None, min_length=1, max_length=120)
    environment: TenantEnvironment | None = None
    status: TenantStatus | None = None
    primary_domain: str | None = Field(default=None, max_length=255)
    custom_domain: str | None = Field(default=None, max_length=255)
    erpnext_site_name: str | None = Field(default=None, max_length=255)
    erpnext_base_url: str | None = Field(default=None, max_length=255)
    provisioning_status: ProvisioningStatus | None = None

    @field_validator("tenant_slug")
    @classmethod
    def normalize_slug(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Tenant slug is required.")
        return normalized
