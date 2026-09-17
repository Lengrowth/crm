from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PortfolioTask(BaseModel):
    id: str
    title: str
    status: str
    due_date: datetime | None = None


class PortfolioProject(BaseModel):
    id: str
    organization_id: str
    organization_name: str
    tenant_id: str
    tenant_slug: str
    status: str
    target_go_live_date: datetime | None = None
    task_count: int
    completed_task_count: int
    progress_percent: int
    blocker_count: int
    overdue_task_count: int
    tasks: list[PortfolioTask]


class ImplementationPortfolio(BaseModel):
    generated_at: datetime
    project_count: int
    blocker_count: int
    overdue_task_count: int
    truncated: bool = False
    projects: list[PortfolioProject]
