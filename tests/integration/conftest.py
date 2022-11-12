"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

apibox integration tests configuration
"""

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from apibox.infrastructure.database.engine import get_engine
from apibox.infrastructure.database.models import DatabaseModel
from apibox.main import app

session = scoped_session(sessionmaker(bind=get_engine()))


@pytest.fixture(name="config", scope="session")
def fixture_config():
    """expose alembic config fixture"""
    return Config("migrations/alembic.ini")


@pytest.fixture(name="engine", scope="session")
def fixture_engine():
    """expose a database session fixture"""
    return get_engine()


@pytest.fixture(name="clean_session", scope="function")
def fixture_clean_session(engine, config):
    """expose a clean database session fixture"""
    DatabaseModel.metadata.drop_all(engine)
    session.execute("drop table if exists alembic_version")
    session.commit()

    yield session

    DatabaseModel.metadata.drop_all(engine)
    session.execute("drop table if exists alembic_version")
    session.commit()


@pytest.fixture(name="session", scope="function")
def fixture_session(engine):
    """expose a database session fixture"""
    DatabaseModel.metadata.create_all(engine)

    yield session

    session.commit()
    DatabaseModel.metadata.drop_all(engine)


@pytest.fixture(name="client", scope="session")
def fixture_client():
    """return a test client"""
    return TestClient(app)
