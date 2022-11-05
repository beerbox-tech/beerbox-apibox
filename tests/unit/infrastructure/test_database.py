"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

unit testing beerbox database
"""

from datetime import datetime
from datetime import timezone
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future.engine import Engine
from sqlalchemy.orm import Session

from beerbox.application.health import Check
from beerbox.application.health import Status
from beerbox.domain.users import UserAlreadyExist
from beerbox.domain.users import UserDoesNotExist
from beerbox.infrastructure.database.engine import get_engine
from beerbox.infrastructure.database.health import DatabaseReadiness
from beerbox.infrastructure.database.models import DatabaseModel
from beerbox.infrastructure.database.repositories.user import DatabaseUserRepository
from beerbox.infrastructure.database.session import get_session
from beerbox.infrastructure.database.session import open_session
from tests.factories import DatabaseUserFactory
from tests.factories import DomainUserFactory

NOW = datetime(2020, 1, 1, tzinfo=timezone.utc)


def mock_datetime(now: datetime) -> Mock:
    """mock the datetime module and setup a now return value"""
    mock = Mock()
    mock.now.return_value = now
    return mock


def mock_session(raise_on_commit: Exception | None = None, **kwargs) -> Mock:
    """mock the database session"""
    mock = Mock()
    for key, value in kwargs.items():
        if isinstance(value, Exception):
            getattr(mock.execute.return_value, key).side_effect = value
        else:
            getattr(mock.execute.return_value, key).return_value = value
    if raise_on_commit:
        mock.commit.side_effect = raise_on_commit
    return mock


def get_query(session: Mock):
    """get the query string from a mocked session"""
    return str(session.execute.call_args.args[0])


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


def test_user_repository__get_users():
    """assert user database repository performs the right queries"""
    user = DatabaseUserFactory.build()
    session = mock_session(scalars=[user])
    repository = DatabaseUserRepository(session)

    results = repository.get_users()
    query = get_query(session)

    assert len(results) == 1
    assert results[0].created_at == user.created_at
    assert results[0].modified_at == user.modified_at
    assert results[0].public_id == user.public_id
    assert results[0].username == user.username
    assert query == (
        "SELECT users.id, users.public_id, users.created_at, users.modified_at, users.username \n"
        "FROM users"
    )


def test_user_repository__get_user():
    """assert user database repository performs the right queries"""
    user = DatabaseUserFactory.build()
    session = mock_session(scalar_one=user)
    repository = DatabaseUserRepository(session)

    result = repository.get_user(user.public_id)
    query = get_query(session)

    assert result.created_at == user.created_at
    assert result.modified_at == user.modified_at
    assert result.public_id == user.public_id
    assert result.username == user.username
    assert query == (
        "SELECT users.id, users.public_id, users.created_at, users.modified_at, users.username \n"
        "FROM users \n"
        "WHERE users.public_id = :public_id_1"
    )


def test_user_repository__get_user__error():
    """assert user database repository performs the right queries"""
    session = mock_session(scalar_one=ValueError("boom"))
    repository = DatabaseUserRepository(session)

    with pytest.raises(UserDoesNotExist):
        repository.get_user("public-id")

    session.rollback.assert_called_once()


def test_user_repository__add_user():
    """assert user database repository performs the right queries"""
    user = DomainUserFactory.build()
    session = mock_session()
    repository = DatabaseUserRepository(session)

    repository.add_user(user)
    query = get_query(session)

    assert query == (
        "INSERT INTO users (public_id, created_at, modified_at, username) "
        "VALUES (:public_id, :created_at, :modified_at, :username)"
    )


def test_user_repository__add_user__integrity_error():
    """assert user database repository performs the right queries"""
    user = DomainUserFactory.build()
    session = mock_session(raise_on_commit=IntegrityError(orig=None, params=None, statement=None))
    repository = DatabaseUserRepository(session)

    with pytest.raises(UserAlreadyExist):
        repository.add_user(user)

    session.rollback.assert_called_once()


def test_user_repository__add_user_error():
    """assert user database repository performs the right queries"""
    user = DomainUserFactory.build()
    session = mock_session(raise_on_commit=SQLAlchemyError())
    repository = DatabaseUserRepository(session)

    with pytest.raises(SQLAlchemyError):
        repository.add_user(user)

    session.rollback.assert_called_once()
