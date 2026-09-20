"""add Phase 01 tenant and bundle attribution to module audits

Revision ID: 20260920_0012
Revises: 20260918_0011
"""

from alembic import op
import sqlalchemy as sa


revision = "20260920_0012"
down_revision = "20260918_0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("module_entitlement_audits") as batch:
        batch.add_column(sa.Column("tenant_id", sa.String(length=36), nullable=True))
        batch.add_column(sa.Column("tenant_ids_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")))
        batch.add_column(sa.Column("previous_bundle_key", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("previous_bundle_version", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("new_bundle_key", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("new_bundle_version", sa.Integer(), nullable=True))
        batch.create_foreign_key("fk_module_entitlement_audits_tenant_id", "tenants", ["tenant_id"], ["id"])
    op.create_index("ix_module_entitlement_audits_tenant_id", "module_entitlement_audits", ["tenant_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_module_entitlement_audits_tenant_id", table_name="module_entitlement_audits")
    with op.batch_alter_table("module_entitlement_audits") as batch:
        batch.drop_constraint("fk_module_entitlement_audits_tenant_id", type_="foreignkey")
        for name in ("new_bundle_version", "new_bundle_key", "previous_bundle_version", "previous_bundle_key", "tenant_ids_json", "tenant_id"):
            batch.drop_column(name)
