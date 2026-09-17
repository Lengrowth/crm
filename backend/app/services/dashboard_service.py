from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone

from sqlalchemy import func, select
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
    """Build a bounded, tenant-scoped operational read model in one request."""

    def build_summary(self, session: Session, current_user: SaaSUser) -> DashboardSummary:
        organization_query = select(Organization).order_by(Organization.name.asc())
        if not current_user.is_platform_admin:
            organization_query = organization_query.join(
                OrganizationMembership,
                OrganizationMembership.organization_id == Organization.id,
            ).where(OrganizationMembership.user_id == current_user.id)
        organizations = session.execute(organization_query).scalars().unique().all()
        organization_ids = [organization.id for organization in organizations]

        tenants = []
        if organization_ids:
            tenants = session.execute(
                select(Tenant).where(Tenant.organization_id.in_(organization_ids)).order_by(Tenant.tenant_slug.asc())
            ).scalars().all()
        tenant_ids = [tenant.id for tenant in tenants]

        provisioning_failures: list[dict[str, str | None]] = []
        failed_job_count = 0
        if tenant_ids:
            job_rows = session.execute(
                select(ProvisioningJob, Tenant.tenant_slug)
                .join(Tenant, Tenant.id == ProvisioningJob.tenant_id)
                .where(ProvisioningJob.tenant_id.in_(tenant_ids))
                .order_by(ProvisioningJob.updated_at.desc())
            ).all()
            failed_job_count = sum(1 for job, _ in job_rows if job.status in {"failed", "error"})
            for job, tenant_slug in job_rows:
                if job.status in {"failed", "error"} and len(provisioning_failures) < 25:
                    provisioning_failures.append({
                        "id": job.id,
                        "tenant_slug": tenant_slug,
                        "status": job.status,
                        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
                    })

        domain_warnings: list[dict[str, str | None]] = []
        if tenant_ids:
            domain_rows = session.execute(
                select(DomainMapping, Tenant.tenant_slug)
                .join(Tenant, Tenant.id == DomainMapping.tenant_id)
                .where(DomainMapping.tenant_id.in_(tenant_ids))
                .order_by(DomainMapping.updated_at.desc())
            ).all()
            for domain, tenant_slug in domain_rows:
                if self._domain_needs_attention(domain):
                    if len(domain_warnings) < 25:
                        domain_warnings.append({
                            "id": domain.id,
                            "domain": domain.domain,
                            "tenant_slug": tenant_slug,
                            "status": domain.status,
                            "ssl_status": domain.ssl_status,
                        })

        project_count = 0
        blocker_count = 0
        overdue_task_count = 0
        if organization_ids:
            project_rows = session.execute(
                select(ImplementationProject.id)
                .where(ImplementationProject.organization_id.in_(organization_ids))
            ).all()
            project_count = len(project_rows)
            project_ids = [row[0] for row in project_rows]
            if project_ids:
                terminal_codes = set(session.execute(
                    select(ImplementationTaskStatus.code).where(ImplementationTaskStatus.is_terminal.is_(True))
                ).scalars().all())
                now = datetime.now(timezone.utc)
                task_rows = session.execute(
                    select(ImplementationTask.status, ImplementationTask.due_date)
                    .where(ImplementationTask.implementation_project_id.in_(project_ids))
                ).all()
                blocker_count = sum(1 for status, _ in task_rows if status in {"blocked", "blocked_by_dependency"})
                overdue_task_count = sum(
                    1 for status, due_date in task_rows
                    if due_date is not None and self._is_before_now(due_date, now) and status not in terminal_codes
                )

        next_actions: list[DashboardAction] = []
        if not organizations:
            next_actions.append(DashboardAction(label="Create the first company", href="/app/organizations/new", tone="info"))
        if not tenants:
            next_actions.append(DashboardAction(label="Add an ERP site", href="/app/tenants/new", tone="info"))
        if failed_job_count:
            next_actions.append(DashboardAction(label="Review failed provisioning jobs", href="/app/tenants", tone="danger"))
        if domain_warnings:
            next_actions.append(DashboardAction(label="Resolve domain or SSL warnings", href="/app/tenants", tone="warning"))
        if blocker_count or overdue_task_count:
            next_actions.append(DashboardAction(label="Review implementation work", href="/app/implementation", tone="warning"))

        return DashboardSummary(
            generated_at=datetime.now(timezone.utc),
            organization_count=len(organizations),
            organization_status_counts=dict(Counter(organization.status for organization in organizations)),
            tenant_count=len(tenants),
            tenant_status_counts=dict(Counter(tenant.status for tenant in tenants)),
            provisioning_status_counts=dict(Counter(tenant.provisioning_status for tenant in tenants)),
            failed_job_count=failed_job_count,
            provisioning_failures=provisioning_failures,
            implementation_blocker_count=blocker_count,
            overdue_task_count=overdue_task_count,
            domain_warning_count=len(domain_warnings),
            domain_warnings=domain_warnings,
            next_actions=next_actions,
        )

    @staticmethod
    def _domain_needs_attention(domain: DomainMapping) -> bool:
        return bool(
            domain.manual_activation_required
            or not domain.is_active
            or domain.status not in {"active", "verified", "ready"}
            or domain.ssl_status not in {"active", "valid", "verified", "ready"}
        )

    @staticmethod
    def _is_before_now(value: datetime, now: datetime) -> bool:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value < now


dashboard_service = DashboardService()
