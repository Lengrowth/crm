from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )


class UUIDMixin:
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )


class SaaSUser(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "saas_users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="invited")
    is_platform_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    password_changed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class AuthSession(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "auth_sessions"
    __table_args__ = (
        UniqueConstraint("session_token_hash", name="uq_auth_sessions_token_hash"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("saas_users.id"), nullable=False, index=True
    )
    session_token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class AuthToken(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "auth_tokens"
    __table_args__ = (
        UniqueConstraint("token_hash", name="uq_auth_tokens_token_hash"),
        Index("ix_auth_tokens_user_purpose", "user_id", "purpose"),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("saas_users.id"), nullable=False, index=True
    )
    purpose: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    sent_to_email: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Organization(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    legal_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    billing_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="lead")


class OrganizationMembership(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organization_memberships"
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_membership_org_user"),
    )

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("saas_users.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(64), nullable=False, default="viewer")


class Tenant(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tenants"
    __table_args__ = (UniqueConstraint("tenant_slug", name="uq_tenants_slug"),)

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, index=True
    )
    tenant_slug: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    environment: Mapped[str] = mapped_column(String(32), nullable=False, default="demo")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="planned")
    primary_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    custom_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    erpnext_site_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    erpnext_base_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    erpnext_api_key_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    erpnext_api_secret_ref: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    provisioning_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending"
    )


class Plan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "plans"
    __table_args__ = (UniqueConstraint("code", name="uq_plans_code"),)

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    monthly_price_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    annual_price_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Module(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "modules"
    __table_args__ = (UniqueConstraint("code", name="uq_modules_code"),)

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class OrganizationModule(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organization_modules"
    __table_args__ = (
        UniqueConstraint("organization_id", "module_id", name="uq_org_module"),
    )

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, index=True
    )
    module_id: Mapped[str] = mapped_column(
        ForeignKey("modules.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="enabled")
    enabled_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("saas_users.id"), nullable=True
    )
    enabled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    disabled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    settings_json: Mapped[dict[str, object]] = mapped_column(
        JSON, nullable=False, default=dict
    )


class Subscription(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, index=True
    )
    plan_id: Mapped[str] = mapped_column(
        ForeignKey("plans.id"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="trialing")
    billing_provider_customer_ref: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    billing_provider_subscription_ref: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    current_period_start: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    current_period_end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ImplementationTemplate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "implementation_templates"
    __table_args__ = (UniqueConstraint("code", name="uq_templates_code"),)

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_modules_json: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    default_roles_json: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    default_checklists_json: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    default_settings_json: Mapped[dict[str, object]] = mapped_column(
        JSON, nullable=False, default=dict
    )


class ImplementationProject(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "implementation_projects"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id"), nullable=False, index=True
    )
    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("tenants.id"), nullable=False, index=True
    )
    template_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("implementation_templates.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="discovery")
    owner_user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("saas_users.id"), nullable=True
    )
    target_go_live_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ImplementationTask(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "implementation_tasks"

    implementation_project_id: Mapped[str] = mapped_column(
        ForeignKey("implementation_projects.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="todo")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assigned_to_user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("saas_users.id"), nullable=True
    )
    due_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ImplementationTaskStatus(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "implementation_task_statuses"
    __table_args__ = (
        UniqueConstraint("code", name="uq_implementation_task_statuses_code"),
    )

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_terminal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class DomainMapping(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "domains"
    __table_args__ = (UniqueConstraint("domain", name="uq_domains_domain"),)

    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("tenants.id"), nullable=False, index=True
    )
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(
        String(32), nullable=False, default="system_subdomain"
    )
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending_dns"
    )
    dns_target: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    manual_activation_required: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    dns_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    ssl_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="unknown"
    )
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    manual_activation_by: Mapped[Optional[str]] = mapped_column(
        ForeignKey("saas_users.id"), nullable=True
    )
    manual_activation_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes_json: Mapped[dict[str, object]] = mapped_column(
        JSON, nullable=False, default=dict
    )


class ProvisioningJob(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "provisioning_jobs"

    tenant_id: Mapped[str] = mapped_column(
        ForeignKey("tenants.id"), nullable=False, index=True
    )
    job_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    requested_by_user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("saas_users.id"), nullable=True
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    logs_json: Mapped[list[dict[str, object]]] = mapped_column(
        JSON, nullable=False, default=list
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class AuditLog(Base, UUIDMixin):
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("saas_users.id"), nullable=True, index=True
    )
    organization_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("organizations.id"), nullable=True, index=True
    )
    tenant_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("tenants.id"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    metadata_json: Mapped[dict[str, object]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )


class IntegrationCredential(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "integration_credentials"
    __table_args__ = (
        UniqueConstraint("provider", "label", name="uq_integration_provider_label"),
    )

    organization_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("organizations.id"), nullable=True, index=True
    )
    tenant_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("tenants.id"), nullable=True, index=True
    )
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    secret_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
