from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db_session
from app.models.domain import SaaSUser
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
