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


def _existing_columns(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return {column["name"] for column in inspector.get_columns(table_name)}


def _is_sqlite() -> bool:
    return op.get_bind().dialect.name == "sqlite"


def upgrade() -> None:
    existing = _existing_columns("domains")

    if "is_active" not in existing:
        op.add_column(
            "domains",
            sa.Column(
                "is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")
            ),
        )
    if "manual_activation_required" not in existing:
        op.add_column(
            "domains",
            sa.Column(
                "manual_activation_required",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("0"),
            ),
        )
    if "dns_verified_at" not in existing:
        op.add_column(
            "domains",
            sa.Column("dns_verified_at", sa.DateTime(timezone=True), nullable=True),
        )
    if "manual_activation_by" not in existing:
        op.add_column(
            "domains",
            sa.Column("manual_activation_by", sa.String(length=36), nullable=True),
        )
    if "manual_activation_at" not in existing:
        op.add_column(
            "domains",
            sa.Column(
                "manual_activation_at", sa.DateTime(timezone=True), nullable=True
            ),
        )
    if "notes_json" not in existing:
        op.add_column(
            "domains",
            sa.Column(
                "notes_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")
            ),
        )

    # SQLite does not support adding this FK via ALTER TABLE in the simple way
    # Alembic emits here. The local/dev SQLite path can safely proceed without the
    # FK constraint because application-level references still use the column and
    # non-SQLite production databases will create the FK normally.
    if not _is_sqlite():
        op.create_foreign_key(
            "fk_domains_manual_activation_by_saas_users",
            "domains",
            "saas_users",
            ["manual_activation_by"],
            ["id"],
        )


def downgrade() -> None:
    if not _is_sqlite():
        op.drop_constraint(
            "fk_domains_manual_activation_by_saas_users", "domains", type_="foreignkey"
        )

    existing = _existing_columns("domains")

    if "notes_json" in existing:
        op.drop_column("domains", "notes_json")
    if "manual_activation_at" in existing:
        op.drop_column("domains", "manual_activation_at")
    if "manual_activation_by" in existing:
        op.drop_column("domains", "manual_activation_by")
    if "dns_verified_at" in existing:
        op.drop_column("domains", "dns_verified_at")
    if "manual_activation_required" in existing:
        op.drop_column("domains", "manual_activation_required")
    if "is_active" in existing:
        op.drop_column("domains", "is_active")
