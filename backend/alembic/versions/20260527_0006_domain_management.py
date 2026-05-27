"""add domain management fields

Revision ID: 20260527_0006
Revises: 20260527_0005_billing_tables
Create Date: 2026-05-27 00:00:00
"""

import sqlalchemy as sa

from alembic import op

revision = "20260527_0006"
down_revision = "20260527_0005_billing_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add white-label and manual activation fields to domains table
    op.add_column(
        "domains",
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")
        ),
    )
    op.add_column(
        "domains",
        sa.Column(
            "manual_activation_required",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "domains",
        sa.Column("dns_verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "domains",
        sa.Column("manual_activation_by", sa.String(length=36), nullable=True),
    )
    op.add_column(
        "domains",
        sa.Column("manual_activation_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "domains",
        sa.Column(
            "notes_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")
        ),
    )

    # Create foreign key for manual_activation_by to saas_users
    op.create_foreign_key(
        "fk_domains_manual_activation_by_saas_users",
        "domains",
        "saas_users",
        ["manual_activation_by"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_domains_manual_activation_by_saas_users", "domains", type_="foreignkey"
    )
    op.drop_column("domains", "notes_json")
    op.drop_column("domains", "manual_activation_at")
    op.drop_column("domains", "manual_activation_by")
    op.drop_column("domains", "dns_verified_at")
    op.drop_column("domains", "manual_activation_required")
    op.drop_column("domains", "is_active")
