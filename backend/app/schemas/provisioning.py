from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from app.schemas.domain import ORMBaseModel


class ProvisioningJobLogEntry(BaseModel):
    ts: datetime
    event: str
    payload: Optional[dict[str, Any]] = None
    message: Optional[str] = None


class ProvisioningJobCreate(BaseModel):
    job_type: str
    payload: Optional[dict[str, Any]] = None


class ProvisioningJobRead(ORMBaseModel):
    id: str
    tenant_id: str
    job_type: str
    status: str
    requested_by_user_id: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    attempt_count: int
    logs_json: list[dict[str, Any]]
    error_message: Optional[str] = None
