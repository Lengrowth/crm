"""add auth sessions and platform admin flag

Revision ID: 20260522_0002
Revises: 20260522_0001
Create Date: 2026-05-22 00:02:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20260522_0002"
down_revision = "20260522_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "saas_users",
        sa.Column("is_platform_admin", sa.Boolean(), nullable=False, server_default=sa.text("0")),
    )
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("session_token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["saas_users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_token_hash", name="uq_auth_sessions_token_hash"),
    )


def downgrade() -> None:
    op.drop_table("auth_sessions")
    op.drop_column("saas_users", "is_platform_admin")
