from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models as _models  # noqa: F401
from app.db.base import Base
from app.models.domain import (
    DomainMapping,
    ImplementationProject,
    ImplementationTask,
    ImplementationTaskStatus,
    OrganizationMembership,
    ProvisioningJob,
    SaaSUser,
)
from app.schemas.auth import AuthRegisterRequest
from app.schemas.control import OrganizationCreateRequest, TenantCreateRequest
from app.services.auth_service import AuthService
from app.services.control_plane_service import ControlPlaneService
from app.services.dashboard_service import DashboardService
from app.api.implementation import get_portfolio


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, future=True)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)()


def test_dashboard_read_model_is_tenant_scoped_and_safe():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    admin_response = auth.register(session, AuthRegisterRequest(email="p2-admin@example.test", full_name="P2 Admin", password="local-password-123", organization_name="Admin Workspace", membership_role="owner", is_platform_admin=True))
    admin = auth.get_context(session, admin_response.access_token).user
    org_a = control.create_organization(session, admin, OrganizationCreateRequest(name="Synthetic Alpha"))
    org_b = control.create_organization(session, admin, OrganizationCreateRequest(name="Synthetic Beta"))
    tenant_a = control.create_tenant(session, admin, TenantCreateRequest(organization_id=org_a.id, tenant_slug="synthetic-alpha", environment="demo"), org_a.id)
    tenant_b = control.create_tenant(session, admin, TenantCreateRequest(organization_id=org_b.id, tenant_slug="synthetic-beta", environment="staging"), org_b.id)
    session.add_all([
        DomainMapping(tenant_id=tenant_b.id, domain="beta.example.test", status="pending_dns", ssl_status="unknown", manual_activation_required=True),
        ProvisioningJob(tenant_id=tenant_b.id, job_type="provision_tenant", status="failed"),
        ImplementationTaskStatus(code="done", name="Done", is_terminal=True),
        ImplementationTaskStatus(code="blocked", name="Blocked"),
    ])
    session.commit()
    project = ImplementationProject(organization_id=org_a.id, tenant_id=tenant_a.id, status="configuration")
    session.add(project)
    session.commit()
    session.add(ImplementationTask(implementation_project_id=project.id, title="Resolve dependency", status="blocked", due_date=datetime.now(timezone.utc) - timedelta(days=1)))
    session.commit()

    admin_summary = DashboardService().build_summary(session, admin)
    assert admin_summary.organization_count == 3  # registration workspace plus both synthetic companies
    assert admin_summary.failed_job_count == 1
    assert admin_summary.domain_warning_count == 1
    assert admin_summary.implementation_blocker_count == 1
    assert all("error_message" not in item for item in admin_summary.provisioning_failures)

    member = SaaSUser(email="alpha-member@example.test", full_name="Alpha Member", status="active")
    session.add(member)
    session.commit()
    session.add(OrganizationMembership(organization_id=org_a.id, user_id=member.id, role="admin"))
    session.commit()
    member_summary = DashboardService().build_summary(session, member)
    assert member_summary.organization_count == 1
    assert member_summary.tenant_count == 1
    assert member_summary.failed_job_count == 0
    assert member_summary.domain_warning_count == 0

    portfolio = get_portfolio(session, admin)
    assert portfolio.project_count == 1
    assert portfolio.projects[0].organization_name == "Synthetic Alpha"
    assert portfolio.projects[0].blocker_count == 1
    assert portfolio.projects[0].progress_percent == 0


def test_dashboard_domain_warning_total_is_independent_of_detail_cap():
    session = make_session()
    auth = AuthService()
    control = ControlPlaneService()
    response = auth.register(session, AuthRegisterRequest(email="warning-admin@example.test", full_name="Warning Admin", password="local-password-123", organization_name="Warning Workspace", membership_role="owner", is_platform_admin=True))
    admin = auth.get_context(session, response.access_token).user
    organization = control.create_organization(session, admin, OrganizationCreateRequest(name="Warning Company"))
    tenant = control.create_tenant(session, admin, TenantCreateRequest(organization_id=organization.id, tenant_slug="warning-site", environment="demo"), organization.id)
    session.add_all([
        DomainMapping(tenant_id=tenant.id, domain=f"warning-{index}.example.test", status="pending_dns", ssl_status="unknown", manual_activation_required=True)
        for index in range(26)
    ])
    session.commit()

    summary = DashboardService().build_summary(session, admin)

    assert summary.domain_warning_count == 26
    assert len(summary.domain_warnings) == 25
    assert summary.domain_warnings_truncated is True
