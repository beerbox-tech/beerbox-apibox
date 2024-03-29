"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
# pylint: disable=no-member,invalid-name

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    """upgrade database schema to next version"""
    ${upgrades if upgrades else "pass"}


def downgrade():
    """downgrade database schema to previous version"""
    ${downgrades if downgrades else "pass"}
