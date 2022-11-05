"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox integration tests configuration
"""

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from beerbox.infrastructure.database.engine import get_engine
from beerbox.main import app

session = scoped_session(sessionmaker(bind=get_engine()))


@pytest.fixture(name="config", scope="session")
def fixture_config():
    """expose alembic config fixture"""
    return Config("migrations/alembic.ini")


@pytest.fixture(name="engine", scope="session")
def fixture_engine():
    """expose a database session fixture"""
    return get_engine()


@pytest.fixture(name="session", scope="function")
def fixture_session(engine, config):
    """expose a database session fixture"""
    command.upgrade(config=config, revision="head", sql=False, tag=None)
    yield session
    session.remove()


@pytest.fixture(name="client", scope="session")
def fixture_client():
    """return a test client"""
    return TestClient(app)
