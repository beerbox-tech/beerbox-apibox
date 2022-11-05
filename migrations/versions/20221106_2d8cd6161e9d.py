"""add contributions table

Revision ID: 2d8cd6161e9d
Revises: 8a0f306d9814
Create Date: 2022-11-06 21:37:35.924905

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2d8cd6161e9d"
down_revision = "8a0f306d9814"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "contributions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("modified_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )


def downgrade():
    op.drop_table("contributions")
