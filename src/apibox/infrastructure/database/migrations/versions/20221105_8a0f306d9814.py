"""create users table

Revision ID: 8a0f306d9814
Revises:
Create Date: 2022-11-05 16:57:50.501268
"""
# pylint: disable=no-member,invalid-name

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8a0f306d9814"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """upgrade database schema to next version"""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
        sa.UniqueConstraint("username"),
    )


def downgrade():
    """downgrade database schema to previous version"""
    op.drop_table("users")
