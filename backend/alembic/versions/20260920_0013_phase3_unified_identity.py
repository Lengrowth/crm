"""add additive Phase 03 unified identity mappings and broker state

Revision ID: 20260920_0013
Revises: 20260920_0012
"""

from alembic import op
import sqlalchemy as sa


revision = "20260920_0013"
down_revision = "20260920_0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("tenants") as batch:
        batch.add_column(sa.Column("erp_role_profile_version", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("erp_role_profile_status", sa.String(length=32), nullable=False, server_default="pending"))
        batch.add_column(sa.Column("sso_rollout_enabled", sa.Boolean(), nullable=False, server_default=sa.false()))

    op.create_table(
        "sso_authorization_requests",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("saas_users.id"), nullable=True),
        sa.Column("state_hash", sa.String(length=64), nullable=False),
        sa.Column("code_challenge", sa.String(length=128), nullable=False),
        sa.Column("code_challenge_method", sa.String(length=16), nullable=False),
        sa.Column("client_id", sa.String(length=128), nullable=False),
        sa.Column("audience", sa.String(length=255), nullable=False),
        sa.Column("redirect_uri", sa.String(length=500), nullable=False),
        sa.Column("requested_path", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="started"),
        sa.Column("denial_reason", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("state_hash", name="uq_sso_authorization_state_hash"),
    )
    op.create_index("ix_sso_authorization_requests_organization_id", "sso_authorization_requests", ["organization_id"])
    op.create_index("ix_sso_authorization_requests_tenant_id", "sso_authorization_requests", ["tenant_id"])
    op.create_index("ix_sso_authorization_requests_user_id", "sso_authorization_requests", ["user_id"])
    op.create_index("ix_sso_authorization_tenant_created", "sso_authorization_requests", ["tenant_id", "created_at"])

    op.create_table(
        "sso_authorization_codes",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.String(length=36), sa.ForeignKey("sso_authorization_requests.id"), nullable=False),
        sa.Column("code_hash", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("saas_users.id"), nullable=False),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("client_id", sa.String(length=128), nullable=False),
        sa.Column("audience", sa.String(length=255), nullable=False),
        sa.Column("redirect_uri", sa.String(length=500), nullable=False),
        sa.Column("code_challenge", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("code_hash", name="uq_sso_authorization_code_hash"),
    )
    for column in ("request_id", "user_id", "organization_id", "tenant_id"):
        op.create_index(f"ix_sso_authorization_codes_{column}", "sso_authorization_codes", [column])

    op.create_table(
        "erp_identity_mappings",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("saas_users.id"), nullable=False),
        sa.Column("organization_id", sa.String(length=36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("erp_site", sa.String(length=255), nullable=False),
        sa.Column("erp_user", sa.String(length=255), nullable=False),
        sa.Column("role_profile_version", sa.String(length=64), nullable=False),
        sa.Column("mapping_status", sa.String(length=32), nullable=False, server_default="active"),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "organization_id", "tenant_id", name="uq_erp_identity_mapping_scope"),
        sa.UniqueConstraint("tenant_id", "erp_user", name="uq_erp_identity_mapping_erp_user"),
    )
    for column in ("user_id", "organization_id", "tenant_id"):
        op.create_index(f"ix_erp_identity_mappings_{column}", "erp_identity_mappings", [column])
    op.create_index("ix_erp_identity_mapping_tenant_status", "erp_identity_mappings", ["tenant_id", "mapping_status"])


def downgrade() -> None:
    op.drop_index("ix_erp_identity_mapping_tenant_status", table_name="erp_identity_mappings")
    for column in ("tenant_id", "organization_id", "user_id"):
        op.drop_index(f"ix_erp_identity_mappings_{column}", table_name="erp_identity_mappings")
    op.drop_table("erp_identity_mappings")
    for column in ("tenant_id", "organization_id", "user_id", "request_id"):
        op.drop_index(f"ix_sso_authorization_codes_{column}", table_name="sso_authorization_codes")
    op.drop_table("sso_authorization_codes")
    op.drop_index("ix_sso_authorization_tenant_created", table_name="sso_authorization_requests")
    for column in ("user_id", "tenant_id", "organization_id"):
        op.drop_index(f"ix_sso_authorization_requests_{column}", table_name="sso_authorization_requests")
    op.drop_table("sso_authorization_requests")
    with op.batch_alter_table("tenants") as batch:
        batch.drop_column("sso_rollout_enabled")
        batch.drop_column("erp_role_profile_status")
        batch.drop_column("erp_role_profile_version")
