"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

unit testing beerbox database
"""

from datetime import datetime
from datetime import timezone
from typing import Any
from unittest.mock import Mock
from unittest.mock import patch

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.exc import OperationalError
from sqlalchemy.future.engine import Engine
from sqlalchemy.orm import Session

from beerbox.application.health import Check
from beerbox.application.health import Status
from beerbox.infrastructure.database.engine import get_engine
from beerbox.infrastructure.database.health import DatabaseReadiness
from beerbox.infrastructure.database.models import DatabaseModel
from beerbox.infrastructure.database.session import get_session
from beerbox.infrastructure.database.session import open_session

NOW = datetime(2020, 1, 1, tzinfo=timezone.utc)


def mock_datetime(now: datetime) -> Mock:
    """mock the datetime module and setup a now return value"""
    mock = Mock()
    mock.now.return_value = now
    return mock


def mock_session(scalar: Any) -> Mock:
    """mock the database session and setup a scalar return value"""
    mock = Mock()
    if isinstance(scalar, Exception):
        mock.execute.return_value.scalar.side_effect = scalar
    else:
        mock.execute.return_value.scalar.return_value = scalar
    return mock


def test_get_engine():
    """make sure engine returns a future engine"""
    engine = get_engine()
    assert isinstance(engine, Engine)


def test_open_session():
    """make sure open sessio returns a future session"""
    with open_session(engine=get_engine()) as session:
        assert isinstance(session, Session)
        assert session.future


def test_get_session():
    """make sure get session returns a future session"""
    for session in get_session():
        assert isinstance(session, Session)
        assert session.future


def test_database_model():
    """test database model"""

    class _(DatabaseModel):
        __tablename__ = "dummy"
        id = Column(Integer, primary_key=True)

    assert "dummy" in DatabaseModel.metadata.tables


def test_database_readiness__available():
    """test database readiness indicator with available database"""
    mocked_session = mock_session(scalar=NOW)
    assert DatabaseReadiness(mocked_session).get_check() == Check(
        name="database:ready",
        time=NOW,
        status=Status.PASS,
        observed_value="true",
        observed_unit="boolean",
    )


@patch("beerbox.infrastructure.database.health.datetime", new=mock_datetime(now=NOW))
def test_database_readiness__unavailable():
    """test database readiness indicator without available database"""
    mocked_session = mock_session(scalar=OperationalError(statement=None, params=None, orig=None))
    assert DatabaseReadiness(mocked_session).get_check() == Check(
        name="database:ready",
        time=NOW,
        status=Status.FAIL,
        observed_value="false",
        observed_unit="boolean",
    )
