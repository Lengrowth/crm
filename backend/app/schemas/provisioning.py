from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.domain import ORMBaseModel


class ProvisioningJobLogEntry(BaseModel):
    ts: datetime
    event: str
    payload: dict[str, Any] | None = None
    message: str | None = None


class ProvisioningJobCreate(BaseModel):
    job_type: str
    payload: dict[str, Any] | None = None


class ProvisioningJobRead(ORMBaseModel):
    id: str
    tenant_id: str
    job_type: str
    status: str
    requested_by_user_id: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    attempt_count: int
    logs_json: list[dict[str, Any]]
    error_message: str | None = None
