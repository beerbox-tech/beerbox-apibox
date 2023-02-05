"""add boxes tables

Revision ID: 2380d792edb8
Revises: 2d8cd6161e9d
Create Date: 2023-02-04 15:58:32.007041
"""
# pylint: disable=no-member,invalid-name

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2380d792edb8"
down_revision = "2d8cd6161e9d"
branch_labels = None
depends_on = None


def upgrade():
    """upgrade database schema to next version"""
    op.create_table(
        "boxes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("public_id"),
    )


def downgrade():
    """downgrade database schema to previous version"""
    op.drop_table("boxes")
