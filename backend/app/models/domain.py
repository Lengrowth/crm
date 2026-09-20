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
    erp_role_profile_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    erp_role_profile_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    sso_rollout_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class SSOAuthorizationRequest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sso_authorization_requests"
    __table_args__ = (
        UniqueConstraint("state_hash", name="uq_sso_authorization_state_hash"),
        Index("ix_sso_authorization_tenant_created", "tenant_id", "created_at"),
    )

    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("saas_users.id"), nullable=True, index=True)
    state_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    code_challenge: Mapped[str] = mapped_column(String(128), nullable=False)
    code_challenge_method: Mapped[str] = mapped_column(String(16), nullable=False)
    client_id: Mapped[str] = mapped_column(String(128), nullable=False)
    audience: Mapped[str] = mapped_column(String(255), nullable=False)
    redirect_uri: Mapped[str] = mapped_column(String(500), nullable=False)
    requested_path: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="started")
    denial_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class SSOAuthorizationCode(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sso_authorization_codes"
    __table_args__ = (
        UniqueConstraint("code_hash", name="uq_sso_authorization_code_hash"),
        Index("ix_sso_authorization_code_request", "request_id"),
    )

    request_id: Mapped[str] = mapped_column(ForeignKey("sso_authorization_requests.id"), nullable=False, index=True)
    code_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("saas_users.id"), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    client_id: Mapped[str] = mapped_column(String(128), nullable=False)
    audience: Mapped[str] = mapped_column(String(255), nullable=False)
    redirect_uri: Mapped[str] = mapped_column(String(500), nullable=False)
    code_challenge: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class ERPIdentityMapping(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "erp_identity_mappings"
    __table_args__ = (
        UniqueConstraint("user_id", "organization_id", "tenant_id", name="uq_erp_identity_mapping_scope"),
        UniqueConstraint("tenant_id", "erp_user", name="uq_erp_identity_mapping_erp_user"),
        Index("ix_erp_identity_mapping_tenant_status", "tenant_id", "mapping_status"),
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("saas_users.id"), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    erp_site: Mapped[str] = mapped_column(String(255), nullable=False)
    erp_user: Mapped[str] = mapped_column(String(255), nullable=False)
    role_profile_version: Mapped[str] = mapped_column(String(64), nullable=False)
    mapping_status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Plan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "plans"
    __table_args__ = (UniqueConstraint("code", name="uq_plans_code"),)

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    monthly_price_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    annual_price_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    default_modules_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)


class Module(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "modules"
    __table_args__ = (UniqueConstraint("code", name="uq_modules_code"),)

    code: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    public_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    internal_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_marketed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dependency_codes_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    incompatibility_codes_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    required_app: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    minimum_app_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    compatible_app_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    default_roles_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    default_workspaces_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    configuration_schema_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    administrative_visibility: Mapped[str] = mapped_column(String(32), nullable=False, default="public")
    alias_of: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    deprecated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


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
    explicit_state: Mapped[str] = mapped_column(String(32), nullable=False, default="enabled")
    requested_state: Mapped[str] = mapped_column(String(32), nullable=False, default="enabled")
    entitled_state: Mapped[str] = mapped_column(String(32), nullable=False, default="entitled")
    source_type: Mapped[str] = mapped_column(String(32), nullable=False, default="organization")
    source_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    last_idempotency_key: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    requested_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


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


class ModuleBundle(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "module_bundles"
    __table_args__ = (UniqueConstraint("bundle_key", "version", name="uq_module_bundle_key_version"),)

    bundle_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    source: Mapped[str] = mapped_column(String(255), nullable=False, default="platform")


class ModuleBundleItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "module_bundle_items"
    __table_args__ = (
        UniqueConstraint("bundle_id", "module_id", name="uq_module_bundle_item"),
    )

    bundle_id: Mapped[str] = mapped_column(ForeignKey("module_bundles.id"), nullable=False, index=True)
    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id"), nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ModuleEntitlementRequest(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "module_entitlement_requests"
    __table_args__ = (
        UniqueConstraint("organization_id", "idempotency_key", name="uq_module_request_org_key"),
    )

    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    actor_user_id: Mapped[str] = mapped_column(ForeignKey("saas_users.id"), nullable=False, index=True)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    operation: Mapped[str] = mapped_column(String(32), nullable=False)
    response_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="applied")


class ModuleEntitlementAudit(Base):
    __tablename__ = "module_entitlement_audits"
    __table_args__ = (Index("ix_module_entitlement_audits_org_created", "organization_id", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    actor_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("saas_users.id"), nullable=True, index=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    tenant_id: Mapped[Optional[str]] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    tenant_ids_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    operation: Mapped[str] = mapped_column(String(32), nullable=False)
    previous_requested_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    new_requested_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    previous_effective_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    new_effective_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False, default="organization")
    source_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    previous_bundle_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    previous_bundle_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    new_bundle_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    new_bundle_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    result: Mapped[str] = mapped_column(String(32), nullable=False, default="applied")


class ModuleApplicationStatus(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "module_application_statuses"
    __table_args__ = (
        UniqueConstraint("tenant_id", "module_id", name="uq_module_application_tenant_module"),
    )

    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    module_id: Mapped[str] = mapped_column(ForeignKey("modules.id"), nullable=False, index=True)
    application_state: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    verification_state: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    evidence_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    applied_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


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
    onboarding_request_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("onboarding_requests.id"), nullable=True, index=True
    )
    onboarding_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    workflow_version: Mapped[str] = mapped_column(String(32), nullable=False, default="legacy-1")
    worker_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    lease_token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    lease_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    heartbeat_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_attempt_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    cancel_requested_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    external_refs_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    target_environment: Mapped[str] = mapped_column(String(32), nullable=False, default="staging")
    target_isolation_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)


class OnboardingRequest(Base, UUIDMixin, TimestampMixin):
    """Durable public intake identity; all applicant data is versioned separately."""

    __tablename__ = "onboarding_requests"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_onboarding_request_idempotency"),
    )

    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    management_token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="draft", index=True)
    applicant_visible_status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    current_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    submitted_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    approved_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    approved_bundle_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    approved_bundle_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    approved_by_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("saas_users.id"), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    execution_authorized_by_user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("saas_users.id"), nullable=True)
    execution_authorized_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    converted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    organization_id: Mapped[Optional[str]] = mapped_column(ForeignKey("organizations.id"), nullable=True, index=True)
    tenant_id: Mapped[Optional[str]] = mapped_column(ForeignKey("tenants.id"), nullable=True, index=True)
    implementation_project_id: Mapped[Optional[str]] = mapped_column(ForeignKey("implementation_projects.id"), nullable=True)
    provisioning_job_id: Mapped[Optional[str]] = mapped_column(ForeignKey("provisioning_jobs.id"), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class OnboardingRequestVersion(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "onboarding_request_versions"
    __table_args__ = (
        UniqueConstraint("request_id", "version", name="uq_onboarding_request_version"),
        UniqueConstraint("request_id", "version_idempotency_key", name="uq_onboarding_version_idempotency"),
    )

    request_id: Mapped[str] = mapped_column(ForeignKey("onboarding_requests.id"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    version_idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    snapshot_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    requested_module_codes_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    bundle_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    bundle_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="public")
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    supersedes_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class OnboardingManagementCredential(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "onboarding_management_credentials"

    request_id: Mapped[str] = mapped_column(ForeignKey("onboarding_requests.id"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class OnboardingDecision(Base, UUIDMixin):
    __tablename__ = "onboarding_decisions"

    request_id: Mapped[str] = mapped_column(ForeignKey("onboarding_requests.id"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    actor_user_id: Mapped[str] = mapped_column(ForeignKey("saas_users.id"), nullable=False, index=True)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    bundle_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    bundle_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    execution_authorized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class ProvisioningStep(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "provisioning_steps"
    __table_args__ = (UniqueConstraint("job_id", "step_key", name="uq_provisioning_step_job_key"),)

    job_id: Mapped[str] = mapped_column(ForeignKey("provisioning_jobs.id"), nullable=False, index=True)
    step_key: Mapped[str] = mapped_column(String(64), nullable=False)
    ordinal: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_attempt_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    worker_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    lease_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    failure_category: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    sanitized_error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    evidence_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    external_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rollback_state: Mapped[str] = mapped_column(String(32), nullable=False, default="not_started")
    dependency_keys_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)


class ProvisioningEvent(Base, UUIDMixin):
    __tablename__ = "provisioning_events"

    step_id: Mapped[str] = mapped_column(ForeignKey("provisioning_steps.id"), nullable=False, index=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("provisioning_jobs.id"), nullable=False, index=True)
    attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    event_code: Mapped[str] = mapped_column(String(64), nullable=False)
    public_message: Mapped[str] = mapped_column(String(500), nullable=False)
    context_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class ProvisioningOutboxEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "provisioning_outbox_events"
    __table_args__ = (UniqueConstraint("idempotency_key", name="uq_provisioning_outbox_idempotency"),)

    aggregate_type: Mapped[str] = mapped_column(String(64), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    payload_json: Mapped[dict[str, object]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class FirstLoginHandoff(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "first_login_handoffs"

    request_id: Mapped[str] = mapped_column(ForeignKey("onboarding_requests.id"), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("saas_users.id"), nullable=False, index=True)
    token_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    token_secret_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="prepared")
    delivery_status: Mapped[str] = mapped_column(String(32), nullable=False, default="disabled")
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    consumed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    delivery_reference: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


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
