from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class DashboardAction(BaseModel):
    label: str
    href: str
    tone: str = "info"


class DashboardSummary(BaseModel):
    generated_at: datetime
    organization_count: int
    organization_status_counts: dict[str, int]
    tenant_count: int
    tenant_status_counts: dict[str, int]
    provisioning_status_counts: dict[str, int]
    failed_job_count: int
    provisioning_failures: list[dict[str, str | None]]
    implementation_blocker_count: int
    overdue_task_count: int
    domain_warning_count: int
    domain_warnings: list[dict[str, str | None]]
    next_actions: list[DashboardAction]
