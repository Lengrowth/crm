"""bind Phase 03 mapping handles and durable SSO rate-limit buckets

Revision ID: 20260921_0014
Revises: 20260920_0013
"""

from alembic import op
import sqlalchemy as sa


revision = "20260921_0014"
down_revision = "20260920_0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("sso_authorization_codes") as batch:
        batch.add_column(sa.Column("mapping_handle_hash", sa.String(length=64), nullable=True))
        batch.add_column(sa.Column("mapping_handle_expires_at", sa.DateTime(timezone=True), nullable=True))
        batch.add_column(sa.Column("mapping_handle_consumed_at", sa.DateTime(timezone=True), nullable=True))
        batch.create_unique_constraint("uq_sso_authorization_code_mapping_handle_hash", ["mapping_handle_hash"])

    op.create_table(
        "sso_rate_limit_buckets",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("bucket_key", sa.String(length=255), nullable=False),
        sa.Column("window_started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_count", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("bucket_key", name="uq_sso_rate_limit_bucket_key"),
    )


def downgrade() -> None:
    op.drop_table("sso_rate_limit_buckets")
    with op.batch_alter_table("sso_authorization_codes") as batch:
        batch.drop_constraint("uq_sso_authorization_code_mapping_handle_hash", type_="unique")
        batch.drop_column("mapping_handle_consumed_at")
        batch.drop_column("mapping_handle_expires_at")
        batch.drop_column("mapping_handle_hash")
