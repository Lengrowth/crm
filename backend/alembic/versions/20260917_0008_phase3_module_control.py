"""add additive Phase 3 module catalog, bundles, entitlements, and ERP state

Revision ID: 20260917_0008
Revises: 20260528_0007
"""

from alembic import op
import sqlalchemy as sa

revision = "20260917_0008"
down_revision = "20260528_0007"
branch_labels = None
depends_on = None


def _json_default() -> sa.TextClause:
    return sa.text("'[]'")


def _object_default() -> sa.TextClause:
    return sa.text("'{}'")


def upgrade() -> None:
    module_columns = [
        sa.Column("public_description", sa.Text(), nullable=True),
        sa.Column("internal_description", sa.Text(), nullable=True),
        sa.Column("is_marketed", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("dependency_codes_json", sa.JSON(), nullable=False, server_default=_json_default()),
        sa.Column("incompatibility_codes_json", sa.JSON(), nullable=False, server_default=_json_default()),
        sa.Column("required_app", sa.String(length=120), nullable=True),
        sa.Column("minimum_app_version", sa.String(length=64), nullable=True),
        sa.Column("compatible_app_version", sa.String(length=64), nullable=True),
        sa.Column("default_roles_json", sa.JSON(), nullable=False, server_default=_json_default()),
        sa.Column("default_workspaces_json", sa.JSON(), nullable=False, server_default=_json_default()),
        sa.Column("configuration_schema_json", sa.JSON(), nullable=False, server_default=_object_default()),
        sa.Column("administrative_visibility", sa.String(length=32), nullable=False, server_default="public"),
        sa.Column("alias_of", sa.String(length=64), nullable=True),
        sa.Column("deprecated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_version", sa.Integer(), nullable=False, server_default=sa.text("1")),
    ]
    for column in module_columns:
        op.add_column("modules", column)
    op.create_index("ix_modules_alias_of", "modules", ["alias_of"], unique=False)
    op.add_column("plans", sa.Column("default_modules_json", sa.JSON(), nullable=False, server_default=_json_default()))

    org_module_columns = [
        sa.Column("explicit_state", sa.String(length=32), nullable=False, server_default="enabled"),
        sa.Column("requested_state", sa.String(length=32), nullable=False, server_default="enabled"),
        sa.Column("entitled_state", sa.String(length=32), nullable=False, server_default="entitled"),
        sa.Column("source_type", sa.String(length=32), nullable=False, server_default="organization"),
        sa.Column("source_ref", sa.String(length=255), nullable=True),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("last_idempotency_key", sa.String(length=128), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=True),
    ]
    for column in org_module_columns:
        op.add_column("organization_modules", column)

    # Existing organization_modules rows predate the Phase 3 state model.  The
    # server defaults above are only for new rows; legacy rows must derive their
    # new state from the old status or a disabled assignment could be silently
    # entitled after upgrade.
    op.execute(
        sa.text(
            """
            UPDATE organization_modules
            SET explicit_state = CASE WHEN lower(status) = 'enabled' THEN 'enabled' ELSE 'disabled' END,
                requested_state = CASE WHEN lower(status) = 'enabled' THEN 'enabled' ELSE 'disabled' END,
                entitled_state = CASE WHEN lower(status) = 'enabled' THEN 'entitled' ELSE 'not_entitled' END
            """
        )
    )

    op.create_table(
        "module_bundles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("bundle_key", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("source", sa.String(length=255), nullable=False, server_default="platform"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bundle_key", "version", name="uq_module_bundle_key_version"),
    )
    op.create_index("ix_module_bundles_bundle_key", "module_bundles", ["bundle_key"], unique=False)
    op.create_table(
        "module_bundle_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("bundle_id", sa.String(length=36), nullable=False),
        sa.Column("module_id", sa.String(length=36), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.ForeignKeyConstraint(["bundle_id"], ["module_bundles.id"]),
        sa.ForeignKeyConstraint(["module_id"], ["modules.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("bundle_id", "module_id", name="uq_module_bundle_item"),
    )
    op.create_index("ix_module_bundle_items_bundle_id", "module_bundle_items", ["bundle_id"], unique=False)
    op.create_index("ix_module_bundle_items_module_id", "module_bundle_items", ["module_id"], unique=False)

    op.create_table(
        "module_entitlement_requests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("actor_user_id", sa.String(length=36), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        sa.Column("operation", sa.String(length=32), nullable=False),
        sa.Column("response_json", sa.JSON(), nullable=False, server_default=_object_default()),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="applied"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.ForeignKeyConstraint(["actor_user_id"], ["saas_users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "idempotency_key", name="uq_module_request_org_key"),
    )
    op.create_index("ix_module_entitlement_requests_organization_id", "module_entitlement_requests", ["organization_id"], unique=False)
    op.create_index("ix_module_entitlement_requests_actor_user_id", "module_entitlement_requests", ["actor_user_id"], unique=False)

    op.create_table(
        "module_entitlement_audits",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_user_id", sa.String(length=36), nullable=True),
        sa.Column("organization_id", sa.String(length=36), nullable=False),
        sa.Column("operation", sa.String(length=32), nullable=False),
        sa.Column("previous_requested_json", sa.JSON(), nullable=False, server_default=_object_default()),
        sa.Column("new_requested_json", sa.JSON(), nullable=False, server_default=_object_default()),
        sa.Column("previous_effective_json", sa.JSON(), nullable=False, server_default=_object_default()),
        sa.Column("new_effective_json", sa.JSON(), nullable=False, server_default=_object_default()),
        sa.Column("source_type", sa.String(length=32), nullable=False, server_default="organization"),
        sa.Column("source_ref", sa.String(length=255), nullable=True),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("result", sa.String(length=32), nullable=False, server_default="applied"),
        sa.ForeignKeyConstraint(["actor_user_id"], ["saas_users.id"]),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_module_entitlement_audits_actor_user_id", "module_entitlement_audits", ["actor_user_id"], unique=False)
    op.create_index("ix_module_entitlement_audits_organization_id", "module_entitlement_audits", ["organization_id"], unique=False)
    op.create_index("ix_module_entitlement_audits_org_created", "module_entitlement_audits", ["organization_id", "created_at"], unique=False)

    op.create_table(
        "module_application_statuses",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("module_id", sa.String(length=36), nullable=False),
        sa.Column("application_state", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("verification_state", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("evidence_ref", sa.String(length=255), nullable=True),
        sa.Column("failure_reason", sa.String(length=500), nullable=True),
        sa.Column("applied_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
        sa.ForeignKeyConstraint(["module_id"], ["modules.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "module_id", name="uq_module_application_tenant_module"),
    )
    op.create_index("ix_module_application_statuses_tenant_id", "module_application_statuses", ["tenant_id"], unique=False)
    op.create_index("ix_module_application_statuses_module_id", "module_application_statuses", ["module_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_module_application_statuses_module_id", table_name="module_application_statuses")
    op.drop_index("ix_module_application_statuses_tenant_id", table_name="module_application_statuses")
    op.drop_table("module_application_statuses")
    op.drop_index("ix_module_entitlement_audits_org_created", table_name="module_entitlement_audits")
    op.drop_index("ix_module_entitlement_audits_organization_id", table_name="module_entitlement_audits")
    op.drop_index("ix_module_entitlement_audits_actor_user_id", table_name="module_entitlement_audits")
    op.drop_table("module_entitlement_audits")
    op.drop_index("ix_module_entitlement_requests_actor_user_id", table_name="module_entitlement_requests")
    op.drop_index("ix_module_entitlement_requests_organization_id", table_name="module_entitlement_requests")
    op.drop_table("module_entitlement_requests")
    op.drop_index("ix_module_bundle_items_module_id", table_name="module_bundle_items")
    op.drop_index("ix_module_bundle_items_bundle_id", table_name="module_bundle_items")
    op.drop_table("module_bundle_items")
    op.drop_index("ix_module_bundles_bundle_key", table_name="module_bundles")
    op.drop_table("module_bundles")
    for name in ("requested_at", "last_idempotency_key", "reason", "source_ref", "source_type", "entitled_state", "requested_state", "explicit_state"):
        op.drop_column("organization_modules", name)
    op.drop_column("plans", "default_modules_json")
    op.drop_index("ix_modules_alias_of", table_name="modules")
    for name in ("metadata_version", "deprecated_at", "alias_of", "administrative_visibility", "configuration_schema_json", "default_workspaces_json", "default_roles_json", "compatible_app_version", "minimum_app_version", "required_app", "incompatibility_codes_json", "dependency_codes_json", "display_order", "is_marketed", "internal_description", "public_description"):
        op.drop_column("modules", name)
