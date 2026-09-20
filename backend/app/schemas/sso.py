from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SSOBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SSOAuthorizationRequest(SSOBaseModel):
    tenant_id: str = Field(min_length=1, max_length=36)
    client_id: str = Field(min_length=1, max_length=128)
    audience: str = Field(min_length=1, max_length=255)
    redirect_uri: str = Field(min_length=1, max_length=500)
    state: str = Field(min_length=16, max_length=512)
    code_challenge: str = Field(min_length=43, max_length=128)
    code_challenge_method: Literal["S256"]
    requested_path: str = Field(default="/app", min_length=1, max_length=500)


class SSOAuthorizationResponse(SSOBaseModel):
    code: str
    state: str
    redirect_uri: str
    expires_in: int
    tenant_id: str
    organization_id: str


class SSOTokenRequest(SSOBaseModel):
    code: str = Field(min_length=16, max_length=512)
    client_id: str = Field(min_length=1, max_length=128)
    audience: str = Field(min_length=1, max_length=255)
    redirect_uri: str = Field(min_length=1, max_length=500)
    code_verifier: str = Field(min_length=43, max_length=128)
    client_secret: Optional[str] = Field(default=None, min_length=1, max_length=512)


class SSOTokenResponse(SSOBaseModel):
    issuer: str
    audience: str
    client_id: str
    control_plane_user_id: str
    email: str
    full_name: str
    organization_id: str
    tenant_id: str
    erp_user_key: str
    role_profile_version: str
    mapping_handle: str
    expires_in: int


class SSOIdentityMappingRequest(SSOBaseModel):
    exchange_handle: str = Field(min_length=16, max_length=512)
    client_secret: Optional[str] = Field(default=None, min_length=1, max_length=512)
    erp_user: str = Field(min_length=1, max_length=255)

    @field_validator("erp_user")
    @classmethod
    def normalize_erp_user(cls, value: str) -> str:
        return value.strip().lower()


class SSOIdentityMappingResponse(SSOBaseModel):
    mapping_id: str
    mapping_status: str
    role_profile_version: str
    replayed: bool


class SSOReadinessResponse(SSOBaseModel):
    tenant_id: str
    organization_id: str
    organization_name: str
    tenant_slug: str
    environment: str
    destination: Optional[str] = None
    enabled: bool
    ready: bool
    explanation: str
