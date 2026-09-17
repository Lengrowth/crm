from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.domain import SaaSUser
from app.models.domain import ImplementationProject, ImplementationTask, ImplementationTaskStatus, Organization, Tenant
from app.schemas.portfolio import ImplementationPortfolio, PortfolioProject, PortfolioTask
from app.api.dependencies import require_platform_admin
from datetime import datetime, timezone
from app.schemas.implementation import (
    ImplementationProjectCreateRequest,
    ImplementationProjectRead,
    ImplementationProjectUpdateRequest,
    ImplementationTaskCreateRequest,
    ImplementationTaskRead,
    ImplementationTaskStatusCreateRequest,
    ImplementationTaskStatusRead,
    ImplementationTaskStatusUpdateRequest,
    ImplementationTaskUpdateRequest,
    ImplementationTemplateCreateRequest,
    ImplementationTemplateRead,
    ImplementationTemplateUpdateRequest,
)
from app.services.implementation_service import (
    ImplementationAccessError,
    ImplementationError,
    ImplementationNotFoundError,
    ImplementationService,
    ImplementationValidationError,
)

router = APIRouter(tags=["implementation"])
implementation_service = ImplementationService()


@router.get("/implementation/portfolio", response_model=ImplementationPortfolio)
def get_portfolio(
    session: Session = Depends(get_db_session),
    _: SaaSUser = Depends(require_platform_admin),
) -> ImplementationPortfolio:
    """Return a bounded portfolio read model for the platform operator page."""
    projects = session.execute(
        select(ImplementationProject, Organization.name, Tenant.tenant_slug)
        .join(Organization, Organization.id == ImplementationProject.organization_id)
        .join(Tenant, Tenant.id == ImplementationProject.tenant_id)
        .order_by(ImplementationProject.created_at.desc())
        .limit(250)
    ).all()
    project_ids = [project.id for project, _, _ in projects]
    task_rows = session.execute(
        select(ImplementationTask)
        .where(ImplementationTask.implementation_project_id.in_(project_ids))
        .order_by(ImplementationTask.sort_order.asc(), ImplementationTask.created_at.asc())
    ).scalars().all() if project_ids else []
    tasks_by_project: dict[str, list[ImplementationTask]] = {}
    for task in task_rows:
        tasks_by_project.setdefault(task.implementation_project_id, []).append(task)
    terminal_statuses = set(session.execute(
        select(ImplementationTaskStatus.code).where(ImplementationTaskStatus.is_terminal.is_(True))
    ).scalars().all())
    now = datetime.now(timezone.utc)
    portfolio: list[PortfolioProject] = []
    total_blockers = 0
    total_overdue = 0
    for project, organization_name, tenant_slug in projects:
        tasks = tasks_by_project.get(project.id, [])
        blockers = [task for task in tasks if task.status in {"blocked", "blocked_by_dependency"}]
        overdue = [task for task in tasks if task.due_date is not None and _is_before_now(task.due_date, now) and task.status not in terminal_statuses]
        completed = sum(1 for task in tasks if task.status in terminal_statuses)
        total = len(tasks)
        total_blockers += len(blockers)
        total_overdue += len(overdue)
        portfolio.append(PortfolioProject(
            id=project.id,
            organization_id=project.organization_id,
            organization_name=organization_name,
            tenant_id=project.tenant_id,
            tenant_slug=tenant_slug,
            status=project.status,
            target_go_live_date=project.target_go_live_date,
            task_count=total,
            completed_task_count=completed,
            progress_percent=int((completed / total) * 100) if total else 0,
            blocker_count=len(blockers),
            overdue_task_count=len(overdue),
            tasks=[PortfolioTask(id=task.id, title=task.title, status=task.status, due_date=task.due_date) for task in tasks[:100]],
        ))
    return ImplementationPortfolio(
        generated_at=now,
        project_count=len(portfolio),
        blocker_count=total_blockers,
        overdue_task_count=total_overdue,
        truncated=len(projects) >= 250,
        projects=portfolio,
    )


def _is_before_now(value: datetime, now: datetime) -> bool:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value < now


def _raise_implementation_error(exc: ImplementationError) -> None:
    if isinstance(exc, ImplementationNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, ImplementationValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc


@router.get("/implementation/task-statuses", response_model=list[ImplementationTaskStatusRead])
def list_task_statuses(
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.list_task_statuses(session, current_user)
    except ImplementationAccessError as exc:
        _raise_implementation_error(exc)


@router.post("/implementation/task-statuses", response_model=ImplementationTaskStatusRead, status_code=status.HTTP_201_CREATED)
def create_task_status(
    payload: ImplementationTaskStatusCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.create_task_status(session, current_user, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/implementation/task-statuses/{status_id}", response_model=ImplementationTaskStatusRead)
def get_task_status(
    status_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.get_task_status(session, current_user, status_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.patch("/implementation/task-statuses/{status_id}", response_model=ImplementationTaskStatusRead)
def update_task_status(
    status_id: str,
    payload: ImplementationTaskStatusUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.update_task_status(session, current_user, status_id, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.delete("/implementation/task-statuses/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_status(
    status_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        implementation_service.delete_task_status(session, current_user, status_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/implementation/templates", response_model=list[ImplementationTemplateRead])
def list_templates(
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.list_templates(session, current_user)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.post("/implementation/templates", response_model=ImplementationTemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(
    payload: ImplementationTemplateCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.create_template(session, current_user, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/implementation/templates/{template_id}", response_model=ImplementationTemplateRead)
def get_template(
    template_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.get_template(session, current_user, template_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.patch("/implementation/templates/{template_id}", response_model=ImplementationTemplateRead)
def update_template(
    template_id: str,
    payload: ImplementationTemplateUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.update_template(session, current_user, template_id, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.delete("/implementation/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        implementation_service.delete_template(session, current_user, template_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/organizations/{organization_id}/implementation-projects", response_model=list[ImplementationProjectRead])
def list_projects(
    organization_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.list_projects(session, current_user, organization_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.post(
    "/organizations/{organization_id}/implementation-projects",
    response_model=ImplementationProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    organization_id: str,
    payload: ImplementationProjectCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    if payload.organization_id != organization_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization mismatch.")
    try:
        return implementation_service.create_project(session, current_user, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/implementation-projects/{project_id}", response_model=ImplementationProjectRead)
def get_project(
    project_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.get_project(session, current_user, project_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.patch("/implementation-projects/{project_id}", response_model=ImplementationProjectRead)
def update_project(
    project_id: str,
    payload: ImplementationProjectUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.update_project(session, current_user, project_id, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.delete("/implementation-projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        implementation_service.delete_project(session, current_user, project_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/implementation-projects/{project_id}/tasks", response_model=list[ImplementationTaskRead])
def list_tasks(
    project_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.list_tasks(session, current_user, project_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.post(
    "/implementation-projects/{project_id}/tasks",
    response_model=ImplementationTaskRead,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: str,
    payload: ImplementationTaskCreateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.create_task(session, current_user, project_id, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.get("/implementation-tasks/{task_id}", response_model=ImplementationTaskRead)
def get_task(
    task_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.get_task(session, current_user, task_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.patch("/implementation-tasks/{task_id}", response_model=ImplementationTaskRead)
def update_task(
    task_id: str,
    payload: ImplementationTaskUpdateRequest,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        return implementation_service.update_task(session, current_user, task_id, payload)
    except ImplementationError as exc:
        _raise_implementation_error(exc)


@router.delete("/implementation-tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    session: Session = Depends(get_db_session),
    current_user: SaaSUser = Depends(get_current_user),
):
    try:
        implementation_service.delete_task(session, current_user, task_id)
    except ImplementationError as exc:
        _raise_implementation_error(exc)
