"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox integration tests configuration
"""

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient

from beerbox.infrastructure.database.engine import get_engine
from beerbox.infrastructure.database.session import open_session
from beerbox.main import app


@pytest.fixture(name="config", scope="session")
def fixture_config():
    """expose alembic config fixture"""
    return Config("migrations/alembic.ini")


@pytest.fixture(name="engine", scope="session")
def fixture_engine():
    """expose a database session fixture"""
    return get_engine()


@pytest.fixture(name="session", scope="function")
def fixture_session(engine):
    """expose a database session fixture"""
    with open_session(engine) as _session:
        yield _session
        _session.commit()


@pytest.fixture(name="client", scope="session")
def fixture_client():
    """return a test client"""
    return TestClient(app)
