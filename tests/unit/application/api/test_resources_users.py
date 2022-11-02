"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

unit testing beerbox user resources
"""

import json
from unittest.mock import Mock

import pytest

from beerbox.application.api.components.user_request import UserRequest
from beerbox.application.api.resources.users import get_user
from beerbox.application.api.resources.users import get_user_repository
from beerbox.application.api.resources.users import get_users
from beerbox.application.api.resources.users import post_users
from beerbox.domain.users import User
from beerbox.domain.users import UserRepository
from tests.factories import DomainUserFactory
from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def mock_request(url: str) -> Mock:
    """create a mock request"""
    mock = Mock()
    mock.url.path = url
    return mock


def mock_user_repository(user: User | None = None) -> Mock:
    """create a user repository"""
    mock = Mock()
    if user:
        mock.get_users.return_value = [user]
        mock.get_user.return_value = user
    return mock


def test_get_user_repository():
    """make sure get_user_repository returns a UserRepository"""
    repository = get_user_repository()
    assert isinstance(repository, UserRepository)


@pytest.mark.asyncio
async def test_get_users():
    """test GET /users resource"""
    user = DomainUserFactory.create()
    repository = mock_user_repository(user)

    response = await get_users(repository)

    repository.get_users.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.body) == [
        {
            "createdAt": user.created_at.isoformat(),
            "modifiedAt": user.modified_at.isoformat(),
            "publicId": user.public_id,
            "username": user.username,
        },
    ]


@pytest.mark.asyncio
async def test_get_user():
    """test GET /user/:publicId resource"""
    user = DomainUserFactory.create()
    repository = mock_user_repository(user)

    response = await get_user("public-id", repository)

    repository.get_user.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.body) == {
        "createdAt": user.created_at.isoformat(),
        "modifiedAt": user.modified_at.isoformat(),
        "publicId": user.public_id,
        "username": user.username,
    }


@pytest.mark.asyncio
async def test_post_users():
    """test POST /users resource"""
    repository = mock_user_repository()
    request = UserRequest(username="test")

    response = await post_users(request, repository)

    repository.add_user.assert_called_once()
    assert response.status_code == 201
    assert json.loads(response.body) == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "username": "test",
    }
