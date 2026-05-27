from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


ImplementationProjectStatus = Literal[
    "discovery",
    "planning",
    "setup",
    "configuration",
    "training",
    "go_live",
    "closed",
    "archived",
]


class ImplementationBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IdentifiedImplementationModel(ImplementationBaseModel):
    id: str
    created_at: datetime
    updated_at: datetime


class ImplementationTaskStatusCreateRequest(ImplementationBaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    sort_order: int = 0
    is_active: bool = True
    is_terminal: bool = False

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Task status code is required.")
        return normalized


class ImplementationTaskStatusUpdateRequest(ImplementationBaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    sort_order: int | None = None
    is_active: bool | None = None
    is_terminal: bool | None = None

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Task status code is required.")
        return normalized


class ImplementationTaskStatusRead(IdentifiedImplementationModel):
    code: str
    name: str
    description: str | None = None
    sort_order: int
    is_active: bool
    is_terminal: bool


class ImplementationTemplateCreateRequest(ImplementationBaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    industry: str | None = Field(default=None, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    default_modules_json: list[str] = Field(default_factory=list)
    default_roles_json: list[str] = Field(default_factory=list)
    default_checklists_json: list[str] = Field(default_factory=list)
    default_settings_json: dict[str, object] = Field(default_factory=dict)

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Template code is required.")
        return normalized


class ImplementationTemplateUpdateRequest(ImplementationBaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    industry: str | None = Field(default=None, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    default_modules_json: list[str] | None = None
    default_roles_json: list[str] | None = None
    default_checklists_json: list[str] | None = None
    default_settings_json: dict[str, object] | None = None

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Template code is required.")
        return normalized


class ImplementationTemplateRead(IdentifiedImplementationModel):
    code: str
    name: str
    industry: str | None = None
    description: str | None = None
    default_modules_json: list[str]
    default_roles_json: list[str]
    default_checklists_json: list[str]
    default_settings_json: dict[str, object]


class ImplementationProjectCreateRequest(ImplementationBaseModel):
    organization_id: str
    tenant_id: str
    template_id: str | None = None
    status: ImplementationProjectStatus = "discovery"
    owner_user_id: str | None = None
    target_go_live_date: datetime | None = None


class ImplementationProjectUpdateRequest(ImplementationBaseModel):
    template_id: str | None = None
    status: ImplementationProjectStatus | None = None
    owner_user_id: str | None = None
    target_go_live_date: datetime | None = None


class ImplementationProjectRead(IdentifiedImplementationModel):
    organization_id: str
    tenant_id: str
    template_id: str | None = None
    status: str
    owner_user_id: str | None = None
    target_go_live_date: datetime | None = None
    task_count: int = 0
    completed_task_count: int = 0
    progress_percent: int = 0


class ImplementationTaskCreateRequest(ImplementationBaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(default="todo", min_length=1, max_length=64)
    sort_order: int = 0
    assigned_to_user_id: str | None = None
    due_date: datetime | None = None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Task status is required.")
        return normalized


class ImplementationTaskUpdateRequest(ImplementationBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: str | None = Field(default=None, min_length=1, max_length=64)
    sort_order: int | None = None
    assigned_to_user_id: str | None = None
    due_date: datetime | None = None

    @field_validator("status")
    @classmethod
    def normalize_status(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower().replace(" ", "-")
        if not normalized:
            raise ValueError("Task status is required.")
        return normalized


class ImplementationTaskRead(IdentifiedImplementationModel):
    implementation_project_id: str
    title: str
    description: str | None = None
    status: str
    sort_order: int
    assigned_to_user_id: str | None = None
    due_date: datetime | None = None
