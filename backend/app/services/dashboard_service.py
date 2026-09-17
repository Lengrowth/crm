from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.models.domain import (
    DomainMapping,
    ImplementationProject,
    ImplementationTask,
    ImplementationTaskStatus,
    Organization,
    OrganizationMembership,
    ProvisioningJob,
    SaaSUser,
    Tenant,
)
from app.schemas.dashboard import DashboardAction, DashboardSummary


class DashboardService:
    """Build a tenant-scoped operational read model with bounded detail lists."""

    DETAIL_LIMIT = 25

    def build_summary(self, session: Session, current_user: SaaSUser) -> DashboardSummary:
        organization_count_statement = select(func.count(Organization.id))
        organization_status_statement = select(Organization.status, func.count(Organization.id)).group_by(Organization.status)
        if not current_user.is_platform_admin:
            organization_count_statement = organization_count_statement.join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            ).where(OrganizationMembership.user_id == current_user.id)
            organization_status_statement = organization_status_statement.join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            ).where(OrganizationMembership.user_id == current_user.id)

        organization_count = int(session.scalar(organization_count_statement) or 0)
        organization_status_counts = {
            str(status): int(count)
            for status, count in session.execute(organization_status_statement).all()
        }

        tenant_scope = select(Tenant).join(Organization, Organization.id == Tenant.organization_id)
        if not current_user.is_platform_admin:
            tenant_scope = tenant_scope.join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            ).where(OrganizationMembership.user_id == current_user.id)
        tenant_scope_subquery = tenant_scope.subquery()
        tenant_count = int(session.scalar(select(func.count()).select_from(tenant_scope_subquery)) or 0)
        tenant_status_rows = session.execute(
            select(tenant_scope_subquery.c.status, func.count(tenant_scope_subquery.c.id))
            .group_by(tenant_scope_subquery.c.status)
        ).all()
        tenant_status_counts = {str(status): int(count) for status, count in tenant_status_rows}
        provisioning_status_rows = session.execute(
            select(tenant_scope_subquery.c.provisioning_status, func.count(tenant_scope_subquery.c.id))
            .group_by(tenant_scope_subquery.c.provisioning_status)
        ).all()
        provisioning_status_counts = {
            str(status): int(count) for status, count in provisioning_status_rows
        }

        job_scope = (
            select(ProvisioningJob, Tenant.tenant_slug)
            .join(Tenant, Tenant.id == ProvisioningJob.tenant_id)
            .join(Organization, Organization.id == Tenant.organization_id)
        )
        if not current_user.is_platform_admin:
            job_scope = job_scope.join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            ).where(OrganizationMembership.user_id == current_user.id)
        failed_job_filter = ProvisioningJob.status.in_({"failed", "error"})
        failed_job_count = int(
            session.scalar(
                select(func.count()).select_from(job_scope.where(failed_job_filter).subquery())
            )
            or 0
        )
        failure_rows = session.execute(
            job_scope.where(failed_job_filter)
            .order_by(ProvisioningJob.updated_at.desc())
            .limit(self.DETAIL_LIMIT)
        ).all()
        provisioning_failures = [
            {
                "id": job.id,
                "tenant_slug": tenant_slug,
                "status": job.status,
                "updated_at": job.updated_at.isoformat() if job.updated_at else None,
            }
            for job, tenant_slug in failure_rows
        ]

        domain_filter = self._domain_needs_attention_filter()
        domain_scope = (
            select(DomainMapping, Tenant.tenant_slug)
            .join(Tenant, Tenant.id == DomainMapping.tenant_id)
            .join(Organization, Organization.id == Tenant.organization_id)
        )
        if not current_user.is_platform_admin:
            domain_scope = domain_scope.join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            ).where(OrganizationMembership.user_id == current_user.id)
        domain_warning_count = int(
            session.scalar(
                select(func.count()).select_from(domain_scope.where(domain_filter).subquery())
            )
            or 0
        )
        domain_rows = session.execute(
            domain_scope.where(domain_filter)
            .order_by(DomainMapping.updated_at.desc())
            .limit(self.DETAIL_LIMIT)
        ).all()
        domain_warnings = [
            {
                "id": domain.id,
                "domain": domain.domain,
                "tenant_slug": tenant_slug,
                "status": domain.status,
                "ssl_status": domain.ssl_status,
            }
            for domain, tenant_slug in domain_rows
        ]

        terminal_codes = set(
            session.execute(
                select(ImplementationTaskStatus.code).where(
                    ImplementationTaskStatus.is_terminal.is_(True)
                )
            ).scalars().all()
        )
        now = datetime.now(timezone.utc)
        blocker_filter = ImplementationTask.status.in_({"blocked", "blocked_by_dependency"})
        overdue_filter = and_(
            ImplementationTask.due_date.is_not(None),
            ImplementationTask.due_date < now,
            ~ImplementationTask.status.in_(terminal_codes),
        )

        def task_count(filter_clause) -> int:
            statement = (
                select(func.count())
                .select_from(ImplementationTask)
                .join(
                    ImplementationProject,
                    ImplementationProject.id == ImplementationTask.implementation_project_id,
                )
                .join(Organization, Organization.id == ImplementationProject.organization_id)
            )
            if not current_user.is_platform_admin:
                statement = statement.join(
                    OrganizationMembership,
                    OrganizationMembership.organization_id == Organization.id,
                ).where(OrganizationMembership.user_id == current_user.id)
            return int(session.scalar(statement.where(filter_clause)) or 0)

        blocker_count = task_count(blocker_filter)
        overdue_task_count = task_count(overdue_filter)

        next_actions: list[DashboardAction] = []
        if not organization_count:
            next_actions.append(DashboardAction(label="Create the first company", href="/app/organizations/new", tone="info"))
        if not tenant_count:
            next_actions.append(DashboardAction(label="Add an ERP site", href="/app/tenants/new", tone="info"))
        if failed_job_count:
            next_actions.append(DashboardAction(label="Review failed provisioning jobs", href="/app/tenants", tone="danger"))
        if domain_warning_count:
            next_actions.append(DashboardAction(label="Resolve domain or SSL warnings", href="/app/tenants", tone="warning"))
        if blocker_count or overdue_task_count:
            next_actions.append(DashboardAction(label="Review implementation work", href="/app/implementation", tone="warning"))

        return DashboardSummary(
            generated_at=now,
            organization_count=organization_count,
            organization_status_counts=organization_status_counts,
            tenant_count=tenant_count,
            tenant_status_counts=tenant_status_counts,
            provisioning_status_counts=provisioning_status_counts,
            failed_job_count=failed_job_count,
            provisioning_failures=provisioning_failures,
            provisioning_failures_truncated=failed_job_count > len(provisioning_failures),
            implementation_blocker_count=blocker_count,
            overdue_task_count=overdue_task_count,
            domain_warning_count=domain_warning_count,
            domain_warnings=domain_warnings,
            domain_warnings_truncated=domain_warning_count > len(domain_warnings),
            next_actions=next_actions,
        )

    @staticmethod
    def _domain_needs_attention_filter():
        return or_(
            DomainMapping.manual_activation_required.is_(True),
            DomainMapping.is_active.is_(False),
            DomainMapping.status.is_(None),
            ~DomainMapping.status.in_({"active", "verified", "ready"}),
            DomainMapping.ssl_status.is_(None),
            ~DomainMapping.ssl_status.in_({"active", "valid", "verified", "ready"}),
        )


dashboard_service = DashboardService()
