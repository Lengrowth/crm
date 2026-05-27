from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


class ProvisionRequest(BaseModel):
    custom_app: Optional[str] = None
    domain: Optional[str] = None
    options: Dict[str, Any] = {}


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
