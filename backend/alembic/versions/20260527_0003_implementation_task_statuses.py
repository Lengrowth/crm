"""add implementation task statuses

Revision ID: 20260527_0003
Revises: 20260522_0002
Create Date: 2026-05-27 00:03:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20260527_0003"
down_revision = "20260522_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "implementation_task_statuses",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_terminal", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_implementation_task_statuses_code"),
    )


def downgrade() -> None:
    op.drop_table("implementation_task_statuses")
