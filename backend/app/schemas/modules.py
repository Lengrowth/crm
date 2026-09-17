from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


ModuleState = Literal["marketed", "requested", "entitled", "applied", "verified"]
ApplicationState = Literal["not_applicable", "pending", "applied", "failed"]
VerificationState = Literal["pending", "verified", "failed"]


class ModuleCatalogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    public_description: Optional[str] = None
    internal_description: Optional[str] = None
    is_active: bool
    is_marketed: bool
    display_order: int
    dependency_codes: list[str] = Field(default_factory=list)
    incompatibility_codes: list[str] = Field(default_factory=list)
    required_app: Optional[str] = None
    minimum_app_version: Optional[str] = None
    compatible_app_version: Optional[str] = None
    default_roles: list[str] = Field(default_factory=list)
    default_workspaces: list[str] = Field(default_factory=list)
    configuration_schema: dict[str, object] = Field(default_factory=dict)
    administrative_visibility: str
    alias_of: Optional[str] = None
    deprecated_at: Optional[datetime] = None
    metadata_version: int


class PublicModuleRead(BaseModel):
    code: str
    name: str
    category: Optional[str] = None
    description: str
    display_order: int


class ModuleBundleItemRead(BaseModel):
    code: str
    name: str
    sort_order: int


class ModuleBundleRead(BaseModel):
    id: str
    bundle_key: str
    version: int
    name: str
    description: Optional[str] = None
    source: str
    modules: list[ModuleBundleItemRead] = Field(default_factory=list)


class ModuleChangeRequest(BaseModel):
    organization_id: str
    enable_codes: list[str] = Field(default_factory=list)
    disable_codes: list[str] = Field(default_factory=list)
    clear_codes: list[str] = Field(default_factory=list)
    bundle_key: Optional[str] = None
    bundle_version: Optional[int] = Field(default=None, ge=1)
    reason: Optional[str] = Field(default=None, max_length=500)
    preview_hash: Optional[str] = Field(default=None, min_length=64, max_length=64)
    idempotency_key: Optional[str] = Field(default=None, min_length=8, max_length=128)


class ModuleReversalRequest(BaseModel):
    organization_id: str
    audit_id: str
    reason: Optional[str] = Field(default=None, max_length=500)
    preview_hash: Optional[str] = None
    idempotency_key: Optional[str] = Field(default=None, min_length=8, max_length=128)


class ModuleEffectiveItem(BaseModel):
    code: str
    name: str
    category: Optional[str] = None
    requested: bool
    entitled: bool
    marketed: bool
    explicit: bool
    source: list[str] = Field(default_factory=list)
    explanation: list[str] = Field(default_factory=list)
    application_state: ApplicationState
    verification_state: VerificationState
    tenant_states: list[dict[str, object]] = Field(default_factory=list)


class ModuleEffectiveRead(BaseModel):
    organization_id: str
    requested_codes: list[str]
    effective_codes: list[str]
    items: list[ModuleEffectiveItem]
    warnings: list[str] = Field(default_factory=list)
    generated_at: datetime


class ModulePreviewRead(BaseModel):
    organization_id: str
    requested_enable_codes: list[str]
    requested_disable_codes: list[str]
    requested_clear_codes: list[str] = Field(default_factory=list)
    dependency_additions: list[str]
    dependency_removals: list[str]
    conflicts: list[str]
    effective: ModuleEffectiveRead
    warnings: list[str]
    preview_hash: str
    is_current: bool


class ModuleChangeResult(BaseModel):
    operation: str
    replayed: bool = False
    audit_id: Optional[str] = None
    effective: ModuleEffectiveRead


class ModuleAuditRead(BaseModel):
    id: str
    created_at: datetime
    actor_user_id: Optional[str] = None
    organization_id: str
    operation: str
    previous_requested: dict[str, object]
    new_requested: dict[str, object]
    previous_effective: dict[str, object]
    new_effective: dict[str, object]
    source_type: str
    source_ref: Optional[str] = None
    reason: Optional[str] = None
    idempotency_key: str
    result: str
