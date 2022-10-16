"""created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox database integration tests
"""

import pytest
from alembic import command
from alembic.util.exc import CommandError
from sqlalchemy.exc import ProgrammingError


def test_migrations(config, session):
    """test migrations up and down"""
    with pytest.raises(ProgrammingError):
        result = session.execute("select count(*) from alembic_version").scalar()
    session.rollback()

    command.upgrade(config=config, revision="head", sql=False, tag=None)
    result = session.execute("select count(*) from alembic_version").scalar()
    assert result == 0

    with pytest.raises(CommandError):
        command.downgrade(config=config, revision="-1", sql=False, tag=None)
    session.rollback()
