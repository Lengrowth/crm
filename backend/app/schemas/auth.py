from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AuthBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


OrganizationMembershipRole = Literal["owner", "admin", "implementation_manager", "support", "viewer"]


class AuthMembershipRead(AuthBaseModel):
    organization_id: str
    organization_name: str
    role: OrganizationMembershipRole


class AuthUserRead(AuthBaseModel):
    id: str
    email: str
    full_name: str
    status: str
    is_platform_admin: bool
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    memberships: list[AuthMembershipRead] = Field(default_factory=list)


class AuthSessionRead(AuthBaseModel):
    id: str
    user_id: str
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class AuthRegisterRequest(AuthBaseModel):
    email: str = Field(min_length=3, max_length=255)
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=255)
    organization_name: str = Field(default="Local SaaS Workspace", min_length=1, max_length=255)
    membership_role: OrganizationMembershipRole = "owner"
    is_platform_admin: bool = False

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Enter a valid email address.")
        return normalized


class AuthEmailAddressRequest(AuthBaseModel):
    email: str = Field(min_length=3, max_length=255)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Enter a valid email address.")
        return normalized


class AuthPasswordResetRequest(AuthEmailAddressRequest):
    pass


class AuthPasswordResetConfirm(AuthBaseModel):
    token: str = Field(min_length=16, max_length=512)
    new_password: str = Field(min_length=8, max_length=255)


class AuthEmailVerificationRequest(AuthEmailAddressRequest):
    pass


class AuthEmailVerificationConfirm(AuthBaseModel):
    token: str = Field(min_length=16, max_length=512)


class AuthLoginRequest(AuthBaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=255)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Enter a valid email address.")
        return normalized


class AuthTokenResponse(AuthBaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_at: datetime
    user: AuthUserRead
    session: AuthSessionRead


class AuthMeResponse(AuthBaseModel):
    user: AuthUserRead


class AuthLogoutResponse(AuthBaseModel):
    detail: str


class AuthMessageResponse(AuthBaseModel):
    detail: str
