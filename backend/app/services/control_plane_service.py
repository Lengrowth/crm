from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.domain import Organization, OrganizationMembership, SaaSUser, Tenant
from app.schemas.control import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    TenantCreateRequest,
    TenantUpdateRequest,
)

WRITE_ROLES = {"owner", "admin", "implementation_manager"}


class ControlPlaneError(Exception):
    pass


class ControlPlaneNotFoundError(ControlPlaneError):
    pass


class ControlPlaneAccessError(ControlPlaneError):
    pass


class ControlPlaneValidationError(ControlPlaneError):
    pass


class ControlPlaneService:
    def list_organizations(self, session: Session, current_user: SaaSUser) -> list[Organization]:
        if current_user.is_platform_admin:
            statement = select(Organization).order_by(Organization.created_at.desc())
            return session.execute(statement).scalars().all()

        statement = (
            select(Organization)
            .join(OrganizationMembership, OrganizationMembership.organization_id == Organization.id)
            .where(OrganizationMembership.user_id == current_user.id)
            .order_by(Organization.created_at.desc())
        )
        return session.execute(statement).scalars().all()

    def create_organization(
        self,
        session: Session,
        current_user: SaaSUser,
        payload: OrganizationCreateRequest,
    ) -> Organization:
        organization = Organization(
            name=payload.name.strip(),
            legal_name=payload.legal_name.strip() if payload.legal_name else None,
            industry=payload.industry.strip() if payload.industry else None,
            country=payload.country.strip() if payload.country else None,
            timezone=payload.timezone.strip() if payload.timezone else None,
            billing_email=payload.billing_email.strip().lower() if payload.billing_email else None,
            status=payload.status,
        )
        session.add(organization)
        session.flush()

        membership = OrganizationMembership(
            organization_id=organization.id,
            user_id=current_user.id,
            role="owner",
        )
        session.add(membership)
        session.commit()
        session.refresh(organization)
        return organization

    def get_organization(self, session: Session, current_user: SaaSUser, organization_id: str) -> Organization:
        organization = self._fetch_organization(session, organization_id)
        if organization is None:
            raise ControlPlaneNotFoundError("Organization not found.")
        self._ensure_organization_access(session, current_user, organization.id)
        return organization

    def update_organization(
        self,
        session: Session,
        current_user: SaaSUser,
        organization_id: str,
        payload: OrganizationUpdateRequest,
    ) -> Organization:
        organization = self._fetch_organization(session, organization_id)
        if organization is None:
            raise ControlPlaneNotFoundError("Organization not found.")
        self._ensure_organization_write_access(session, current_user, organization.id)

        for field, value in payload.model_dump(exclude_unset=True).items():
            if isinstance(value, str):
                value = value.strip()
            setattr(organization, field, value.lower() if field == "billing_email" and isinstance(value, str) else value)

        session.commit()
        session.refresh(organization)
        return organization

    def list_tenants(
        self,
        session: Session,
        current_user: SaaSUser,
        organization_id: str | None = None,
    ) -> list[Tenant]:
        statement = select(Tenant).order_by(Tenant.created_at.desc())

        if organization_id is not None:
            self._require_organization_exists(session, organization_id)
            self._ensure_organization_access(session, current_user, organization_id)
            statement = statement.where(Tenant.organization_id == organization_id)
        elif not current_user.is_platform_admin:
            statement = (
                statement.join(Organization, Organization.id == Tenant.organization_id)
                .join(OrganizationMembership, OrganizationMembership.organization_id == Organization.id)
                .where(OrganizationMembership.user_id == current_user.id)
            )

        return session.execute(statement).scalars().all()

    def create_tenant(
        self,
        session: Session,
        current_user: SaaSUser,
        payload: TenantCreateRequest,
        organization_id: str | None = None,
    ) -> Tenant:
        resolved_organization_id = organization_id or payload.organization_id
        if not resolved_organization_id:
            raise ControlPlaneValidationError("An organization_id is required to create a tenant.")

        self._require_organization_exists(session, resolved_organization_id)
        self._ensure_organization_write_access(session, current_user, resolved_organization_id)

        tenant = Tenant(
            organization_id=resolved_organization_id,
            tenant_slug=payload.tenant_slug,
            environment=payload.environment,
            status=payload.status,
            primary_domain=payload.primary_domain.strip().lower() if payload.primary_domain else None,
            custom_domain=payload.custom_domain.strip().lower() if payload.custom_domain else None,
            erpnext_site_name=payload.erpnext_site_name.strip() if payload.erpnext_site_name else None,
            erpnext_base_url=payload.erpnext_base_url.strip() if payload.erpnext_base_url else None,
            provisioning_status=payload.provisioning_status,
        )
        session.add(tenant)
        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise ControlPlaneValidationError("A tenant with that slug already exists.") from exc
        session.refresh(tenant)
        return tenant

    def get_tenant(self, session: Session, current_user: SaaSUser, tenant_id: str) -> Tenant:
        tenant = self._fetch_tenant(session, tenant_id)
        if tenant is None:
            raise ControlPlaneNotFoundError("Tenant not found.")
        self._ensure_organization_access(session, current_user, tenant.organization_id)
        return tenant

    def update_tenant(
        self,
        session: Session,
        current_user: SaaSUser,
        tenant_id: str,
        payload: TenantUpdateRequest,
    ) -> Tenant:
        tenant = self._fetch_tenant(session, tenant_id)
        if tenant is None:
            raise ControlPlaneNotFoundError("Tenant not found.")
        self._ensure_organization_write_access(session, current_user, tenant.organization_id)

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if isinstance(value, str):
                value = value.strip()
            if field in {"primary_domain", "custom_domain"} and isinstance(value, str):
                value = value.lower()
            setattr(tenant, field, value)

        try:
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise ControlPlaneValidationError("A tenant with that slug already exists.") from exc
        session.refresh(tenant)
        return tenant

    def _ensure_organization_access(
        self,
        session: Session,
        current_user: SaaSUser,
        organization_id: str,
    ) -> None:
        self._require_organization_exists(session, organization_id)
        if current_user.is_platform_admin:
            return

        statement = select(OrganizationMembership.role).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == current_user.id,
        )
        role = session.execute(statement).scalar_one_or_none()
        if role is None:
            raise ControlPlaneAccessError("Organization access denied.")

    def _ensure_organization_write_access(
        self,
        session: Session,
        current_user: SaaSUser,
        organization_id: str,
    ) -> None:
        self._require_organization_exists(session, organization_id)
        if current_user.is_platform_admin:
            return

        statement = select(OrganizationMembership.role).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == current_user.id,
        )
        role = session.execute(statement).scalar_one_or_none()
        if role is None or role not in WRITE_ROLES:
            raise ControlPlaneAccessError("Organization write access denied.")

    @staticmethod
    def _fetch_organization(session: Session, organization_id: str) -> Organization | None:
        return session.get(Organization, organization_id)

    @staticmethod
    def _fetch_tenant(session: Session, tenant_id: str) -> Tenant | None:
        return session.get(Tenant, tenant_id)

    def _require_organization_exists(self, session: Session, organization_id: str) -> Organization:
        organization = self._fetch_organization(session, organization_id)
        if organization is None:
            raise ControlPlaneNotFoundError("Organization not found.")
        return organization
