from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class ProvisionRequest(BaseModel):
    custom_app: Optional[str] = None
    domain: Optional[str] = None
    options: Dict[str, Any] = Field(default_factory=dict)


class ProvisionResponse(BaseModel):
    id: str
    organization_id: str
    tenant_id: str
    status: str
    started_at: Optional[str]
    finished_at: Optional[str]
    details: Dict[str, Any]
    site_id: Optional[str] = None


class SiteStatus(BaseModel):
    status: str
    site_id: Optional[str] = None
    site_name: Optional[str] = None
    error: Optional[str] = None


class BackupRecord(BaseModel):
    status: str
    backup_id: Optional[str] = None
    site_id: Optional[str] = None


class OperationResult(BaseModel):
    status: str
    site_id: Optional[str] = None
    domain: Optional[str] = None
    app: Optional[str] = None
    backup_id: Optional[str] = None
    error: Optional[str] = None


class ERPNextTenantMappingUpdateRequest(BaseModel):
    site_id: str = Field(min_length=1, max_length=255)
    site_name: Optional[str] = Field(default=None, max_length=255)
    base_url: Optional[str] = Field(default=None, max_length=255)
    api_key_ref: Optional[str] = Field(default=None, max_length=255)
    api_secret_ref: Optional[str] = Field(default=None, max_length=255)
    provisioning_status: Optional[str] = Field(default="ready", max_length=32)
    tenant_status: Optional[str] = Field(default="ready", max_length=32)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("site_id", "site_name", "api_key_ref", "api_secret_ref")
    @classmethod
    def normalize_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip().rstrip("/")
        return normalized or None

    @field_validator("provisioning_status", "tenant_status")
    @classmethod
    def normalize_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip().lower().replace(" ", "_")
        return normalized or None


class ERPNextTenantMappingResponse(BaseModel):
    tenant_id: str
    organization_id: str
    configured: bool
    site_id: Optional[str] = None
    site_name: Optional[str] = None
    base_url: Optional[str] = None
    api_key_ref: Optional[str] = None
    api_secret_ref: Optional[str] = None
    provisioning_status: str
    tenant_status: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
