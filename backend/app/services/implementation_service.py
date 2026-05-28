from __future__ import annotations

from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.domain import (
    ImplementationProject,
    ImplementationTask,
    ImplementationTaskStatus,
    ImplementationTemplate,
    Organization,
    OrganizationMembership,
    SaaSUser,
    Tenant,
)
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
from app.services.control_plane_service import WRITE_ROLES


class ImplementationError(Exception):
    pass


class ImplementationNotFoundError(ImplementationError):
    pass


class ImplementationAccessError(ImplementationError):
    pass


class ImplementationValidationError(ImplementationError):
    pass


class ImplementationService:
    def list_task_statuses(self, session: Session, current_user: SaaSUser) -> list[ImplementationTaskStatusRead]:
        self._require_platform_admin(current_user)
        statement = select(ImplementationTaskStatus).order_by(
            ImplementationTaskStatus.sort_order.asc(),
            ImplementationTaskStatus.name.asc(),
        )
        statuses = session.execute(statement).scalars().all()
        return [ImplementationTaskStatusRead.model_validate(status) for status in statuses]

    def create_task_status(
        self,
        session: Session,
        current_user: SaaSUser,
        payload: ImplementationTaskStatusCreateRequest,
    ) -> ImplementationTaskStatusRead:
        self._require_platform_admin(current_user)
        status = ImplementationTaskStatus(
            code=payload.code,
            name=payload.name.strip(),
            description=payload.description.strip() if payload.description else None,
            sort_order=payload.sort_order,
            is_active=payload.is_active,
            is_terminal=payload.is_terminal,
        )
        session.add(status)
        self._commit_with_integrity_guard(session, "Task status code already exists.")
        session.refresh(status)
        return ImplementationTaskStatusRead.model_validate(status)

    def get_task_status(self, session: Session, current_user: SaaSUser, status_id: str) -> ImplementationTaskStatusRead:
        self._require_platform_admin(current_user)
        status = self._fetch_task_status(session, status_id)
        if status is None:
            raise ImplementationNotFoundError("Task status not found.")
        return ImplementationTaskStatusRead.model_validate(status)

    def update_task_status(
        self,
        session: Session,
        current_user: SaaSUser,
        status_id: str,
        payload: ImplementationTaskStatusUpdateRequest,
    ) -> ImplementationTaskStatusRead:
        self._require_platform_admin(current_user)
        status = self._fetch_task_status(session, status_id)
        if status is None:
            raise ImplementationNotFoundError("Task status not found.")

        if payload.code is not None and payload.code != status.code:
            raise ImplementationValidationError("Task status code cannot be changed after creation.")

        for field, value in payload.model_dump(exclude_unset=True).items():
            if field == "code":
                continue
            if isinstance(value, str):
                value = value.strip()
            setattr(status, field, value)

        self._commit_with_integrity_guard(session, "Task status code already exists.")
        session.refresh(status)
        return ImplementationTaskStatusRead.model_validate(status)

    def delete_task_status(self, session: Session, current_user: SaaSUser, status_id: str) -> None:
        self._require_platform_admin(current_user)
        status = self._fetch_task_status(session, status_id)
        if status is None:
            raise ImplementationNotFoundError("Task status not found.")

        task_count = session.scalar(
            select(func.count(ImplementationTask.id)).where(ImplementationTask.status == status.code)
        )
        if task_count:
            raise ImplementationValidationError("Task status is in use by one or more tasks.")

        session.delete(status)
        session.commit()

    def list_templates(self, session: Session, current_user: SaaSUser) -> list[ImplementationTemplateRead]:
        self._require_platform_admin(current_user)
        statement = select(ImplementationTemplate).order_by(ImplementationTemplate.name.asc())
        templates = session.execute(statement).scalars().all()
        return [ImplementationTemplateRead.model_validate(template) for template in templates]

    def create_template(
        self,
        session: Session,
        current_user: SaaSUser,
        payload: ImplementationTemplateCreateRequest,
    ) -> ImplementationTemplateRead:
        self._require_platform_admin(current_user)
        template = ImplementationTemplate(
            code=payload.code,
            name=payload.name.strip(),
            industry=payload.industry.strip() if payload.industry else None,
            description=payload.description.strip() if payload.description else None,
            default_modules_json=list(payload.default_modules_json),
            default_roles_json=list(payload.default_roles_json),
            default_checklists_json=list(payload.default_checklists_json),
            default_settings_json=dict(payload.default_settings_json),
        )
        session.add(template)
        self._commit_with_integrity_guard(session, "Template code already exists.")
        session.refresh(template)
        return ImplementationTemplateRead.model_validate(template)

    def get_template(self, session: Session, current_user: SaaSUser, template_id: str) -> ImplementationTemplateRead:
        self._require_platform_admin(current_user)
        template = self._fetch_template(session, template_id)
        if template is None:
            raise ImplementationNotFoundError("Template not found.")
        return ImplementationTemplateRead.model_validate(template)

    def update_template(
        self,
        session: Session,
        current_user: SaaSUser,
        template_id: str,
        payload: ImplementationTemplateUpdateRequest,
    ) -> ImplementationTemplateRead:
        self._require_platform_admin(current_user)
        template = self._fetch_template(session, template_id)
        if template is None:
            raise ImplementationNotFoundError("Template not found.")

        for field, value in payload.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()
            setattr(template, field, value)

        self._commit_with_integrity_guard(session, "Template code already exists.")
        session.refresh(template)
        return ImplementationTemplateRead.model_validate(template)

    def delete_template(self, session: Session, current_user: SaaSUser, template_id: str) -> None:
        self._require_platform_admin(current_user)
        template = self._fetch_template(session, template_id)
        if template is None:
            raise ImplementationNotFoundError("Template not found.")

        usage_count = session.scalar(
            select(func.count(ImplementationProject.id)).where(ImplementationProject.template_id == template.id)
        )
        if usage_count:
            raise ImplementationValidationError("Template is in use by one or more implementation projects.")

        session.delete(template)
        session.commit()

    def list_projects(
        self,
        session: Session,
        current_user: SaaSUser,
        organization_id: str,
    ) -> list[ImplementationProjectRead]:
        self._ensure_organization_access(session, current_user, organization_id)
        statement = (
            select(ImplementationProject)
            .where(ImplementationProject.organization_id == organization_id)
            .order_by(ImplementationProject.created_at.desc())
        )
        projects = session.execute(statement).scalars().all()
        return [self._project_read_model(session, project) for project in projects]

    def create_project(
        self,
        session: Session,
        current_user: SaaSUser,
        payload: ImplementationProjectCreateRequest,
    ) -> ImplementationProjectRead:
        self._ensure_organization_write_access(session, current_user, payload.organization_id)
        self._require_tenant_belongs_to_organization(session, payload.organization_id, payload.tenant_id)
        self._require_template_exists(session, payload.template_id)
        self._require_user_exists(session, payload.owner_user_id)

        project = ImplementationProject(
            organization_id=payload.organization_id,
            tenant_id=payload.tenant_id,
            template_id=payload.template_id,
            status=payload.status,
            owner_user_id=payload.owner_user_id,
            target_go_live_date=payload.target_go_live_date,
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        return self._project_read_model(session, project)

    def get_project(self, session: Session, current_user: SaaSUser, project_id: str) -> ImplementationProjectRead:
        project = self._fetch_project(session, project_id)
        if project is None:
            raise ImplementationNotFoundError("Implementation project not found.")
        self._ensure_organization_access(session, current_user, project.organization_id)
        return self._project_read_model(session, project)

    def update_project(
        self,
        session: Session,
        current_user: SaaSUser,
        project_id: str,
        payload: ImplementationProjectUpdateRequest,
    ) -> ImplementationProjectRead:
        project = self._fetch_project(session, project_id)
        if project is None:
            raise ImplementationNotFoundError("Implementation project not found.")
        self._ensure_organization_write_access(session, current_user, project.organization_id)

        data = payload.model_dump(exclude_unset=True)
        if "template_id" in data:
            self._require_template_exists(session, data["template_id"])
        if "owner_user_id" in data:
            self._require_user_exists(session, data["owner_user_id"])

        for field, value in data.items():
            setattr(project, field, value)

        session.commit()
        session.refresh(project)
        return self._project_read_model(session, project)

    def delete_project(self, session: Session, current_user: SaaSUser, project_id: str) -> None:
        project = self._fetch_project(session, project_id)
        if project is None:
            raise ImplementationNotFoundError("Implementation project not found.")
        self._ensure_organization_write_access(session, current_user, project.organization_id)

        tasks = session.execute(
            select(ImplementationTask).where(ImplementationTask.implementation_project_id == project.id)
        ).scalars().all()
        for task in tasks:
            session.delete(task)
        session.delete(project)
        session.commit()

    def list_tasks(self, session: Session, current_user: SaaSUser, project_id: str) -> list[ImplementationTaskRead]:
        project = self._fetch_project(session, project_id)
        if project is None:
            raise ImplementationNotFoundError("Implementation project not found.")
        self._ensure_organization_access(session, current_user, project.organization_id)

        statement = (
            select(ImplementationTask)
            .where(ImplementationTask.implementation_project_id == project.id)
            .order_by(ImplementationTask.sort_order.asc(), ImplementationTask.created_at.asc())
        )
        tasks = session.execute(statement).scalars().all()
        return [ImplementationTaskRead.model_validate(task) for task in tasks]

    def create_task(
        self,
        session: Session,
        current_user: SaaSUser,
        project_id: str,
        payload: ImplementationTaskCreateRequest,
    ) -> ImplementationTaskRead:
        project = self._fetch_project(session, project_id)
        if project is None:
            raise ImplementationNotFoundError("Implementation project not found.")
        self._ensure_organization_write_access(session, current_user, project.organization_id)
        self._require_user_exists(session, payload.assigned_to_user_id)
        self._require_task_status_exists(session, payload.status)

        task = ImplementationTask(
            implementation_project_id=project.id,
            title=payload.title.strip(),
            description=payload.description.strip() if payload.description else None,
            status=payload.status,
            sort_order=payload.sort_order,
            assigned_to_user_id=payload.assigned_to_user_id,
            due_date=payload.due_date,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return ImplementationTaskRead.model_validate(task)

    def get_task(self, session: Session, current_user: SaaSUser, task_id: str) -> ImplementationTaskRead:
        task = self._fetch_task(session, task_id)
        if task is None:
            raise ImplementationNotFoundError("Implementation task not found.")
        self._ensure_organization_access(session, current_user, self._task_organization_id(session, task))
        return ImplementationTaskRead.model_validate(task)

    def update_task(
        self,
        session: Session,
        current_user: SaaSUser,
        task_id: str,
        payload: ImplementationTaskUpdateRequest,
    ) -> ImplementationTaskRead:
        task = self._fetch_task(session, task_id)
        if task is None:
            raise ImplementationNotFoundError("Implementation task not found.")
        organization_id = self._task_organization_id(session, task)
        self._ensure_organization_write_access(session, current_user, organization_id)

        data = payload.model_dump(exclude_unset=True)
        if "assigned_to_user_id" in data:
            self._require_user_exists(session, data["assigned_to_user_id"])
        if "status" in data and data["status"] is not None:
            self._require_task_status_exists(session, data["status"])

        for field, value in data.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(task, field, value)

        session.commit()
        session.refresh(task)
        return ImplementationTaskRead.model_validate(task)

    def delete_task(self, session: Session, current_user: SaaSUser, task_id: str) -> None:
        task = self._fetch_task(session, task_id)
        if task is None:
            raise ImplementationNotFoundError("Implementation task not found.")
        self._ensure_organization_write_access(session, current_user, self._task_organization_id(session, task))

        session.delete(task)
        session.commit()

    def _project_read_model(self, session: Session, project: ImplementationProject) -> ImplementationProjectRead:
        total_tasks = session.scalar(
            select(func.count(ImplementationTask.id)).where(ImplementationTask.implementation_project_id == project.id)
        )
        completed_tasks = session.scalar(
            select(func.count(ImplementationTask.id))
            .join(ImplementationTaskStatus, ImplementationTask.status == ImplementationTaskStatus.code)
            .where(
                ImplementationTask.implementation_project_id == project.id,
                ImplementationTaskStatus.is_terminal.is_(True),
            )
        )
        total_tasks = int(total_tasks or 0)
        completed_tasks = int(completed_tasks or 0)
        progress_percent = int((completed_tasks / total_tasks) * 100) if total_tasks else 0
        return ImplementationProjectRead.model_validate(project).model_copy(
            update={
                "task_count": total_tasks,
                "completed_task_count": completed_tasks,
                "progress_percent": progress_percent,
            }
        )

    def _require_platform_admin(self, current_user: SaaSUser) -> None:
        if not current_user.is_platform_admin:
            raise ImplementationAccessError("Platform admin access required.")

    def _ensure_organization_access(self, session: Session, current_user: SaaSUser, organization_id: str) -> None:
        self._require_organization_exists(session, organization_id)
        if current_user.is_platform_admin:
            return

        statement = select(OrganizationMembership.role).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == current_user.id,
        )
        role = session.execute(statement).scalar_one_or_none()
        if role is None:
            raise ImplementationAccessError("Organization access denied.")

    def _ensure_organization_write_access(self, session: Session, current_user: SaaSUser, organization_id: str) -> None:
        self._require_organization_exists(session, organization_id)
        if current_user.is_platform_admin:
            return

        statement = select(OrganizationMembership.role).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == current_user.id,
        )
        role = session.execute(statement).scalar_one_or_none()
        if role is None or role not in WRITE_ROLES:
            raise ImplementationAccessError("Organization write access denied.")

    @staticmethod
    def _require_organization_exists(session: Session, organization_id: str) -> Organization:
        organization = session.get(Organization, organization_id)
        if organization is None:
            raise ImplementationNotFoundError("Organization not found.")
        return organization

    @staticmethod
    def _require_tenant_belongs_to_organization(session: Session, organization_id: str, tenant_id: str) -> Tenant:
        tenant = session.get(Tenant, tenant_id)
        if tenant is None:
            raise ImplementationNotFoundError("Tenant not found.")
        if tenant.organization_id != organization_id:
            raise ImplementationValidationError("Tenant does not belong to the selected organization.")
        return tenant

    @staticmethod
    def _require_template_exists(session: Session, template_id: Optional[str]) -> Optional[ImplementationTemplate]:
        if template_id is None:
            return None
        template = session.get(ImplementationTemplate, template_id)
        if template is None:
            raise ImplementationNotFoundError("Template not found.")
        return template

    @staticmethod
    def _require_user_exists(session: Session, user_id: Optional[str]) -> Optional[SaaSUser]:
        if user_id is None:
            return None
        user = session.get(SaaSUser, user_id)
        if user is None:
            raise ImplementationNotFoundError("User not found.")
        return user

    @staticmethod
    def _require_task_status_exists(session: Session, status_code: Optional[str]) -> Optional[ImplementationTaskStatus]:
        if status_code is None:
            return None
        statement = select(ImplementationTaskStatus).where(ImplementationTaskStatus.code == status_code)
        status = session.execute(statement).scalar_one_or_none()
        if status is None:
            raise ImplementationValidationError("Task status is not defined.")
        if not status.is_active:
            raise ImplementationValidationError("Task status is inactive.")
        return status

    @staticmethod
    def _fetch_project(session: Session, project_id: str) -> Optional[ImplementationProject]:
        return session.get(ImplementationProject, project_id)

    @staticmethod
    def _fetch_task(session: Session, task_id: str) -> Optional[ImplementationTask]:
        return session.get(ImplementationTask, task_id)

    @staticmethod
    def _fetch_task_status(session: Session, status_id: str) -> Optional[ImplementationTaskStatus]:
        return session.get(ImplementationTaskStatus, status_id)

    @staticmethod
    def _fetch_template(session: Session, template_id: str) -> Optional[ImplementationTemplate]:
        return session.get(ImplementationTemplate, template_id)

    @staticmethod
    def _task_organization_id(session: Session, task: ImplementationTask) -> str:
        statement = select(ImplementationProject.organization_id).where(ImplementationProject.id == task.implementation_project_id)
        organization_id = session.execute(statement).scalar_one_or_none()
        if organization_id is None:
            raise ImplementationNotFoundError("Implementation project not found.")
        return organization_id

    @staticmethod
    def _commit_with_integrity_guard(session: Session, duplicate_message: str) -> None:
        from sqlalchemy.exc import IntegrityError

        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise ImplementationValidationError(duplicate_message) from exc
