"""created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox database integration tests
"""

from alembic import command
from alembic.util.exc import CommandError
from sqlalchemy import select

from beerbox.infrastructure.database.models import User
from tests.factories import DatabaseUserFactory


def test_migrations(config, clean_session):
    """test migrations up and down"""
    command.upgrade(config=config, revision="head", sql=False, tag=None)
    result = clean_session.execute("select count(*) from alembic_version").scalar()
    assert result == 1

    while True:
        try:
            command.downgrade(config=config, revision="-1", sql=False, tag=None)
        except CommandError:
            break
    result = clean_session.execute("select count(*) from alembic_version").scalar()
    assert result == 0


def test_select_users_empty(session):
    """test users table accessibility"""
    results = session.execute(select(User)).scalars()
    assert results.all() == []


def test_select_users_filled(session):
    """test user factory generated data accessiblity"""
    user = DatabaseUserFactory.create()
    result = session.execute(select(User)).scalar()
    assert result == user
