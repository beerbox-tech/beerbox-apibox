"""
created by: thibault defeyter
created at: 2022/10/30
licene: MIT

unit testing of apibox users domain
"""


import pytest

from apibox.domain.users import InMemoryUserRepository
from apibox.domain.users import UserAlreadyExist
from apibox.domain.users import UserDoesNotExist
from tests.factories import DomainUserFactory


def test_repository_add_user():
    """test adding a user to the in memory repository"""
    user = DomainUserFactory.create()
    repository = InMemoryUserRepository()
    repository.add_user(user)
    assert repository.storage == {user.public_id: user}


def test_repository_add_user__already_exist():
    """test adding a user to the in memory repository"""
    user = DomainUserFactory.create()
    repository = InMemoryUserRepository(storage={user.public_id: user})
    with pytest.raises(UserAlreadyExist):
        repository.add_user(user)


def test_repository_get_users__empty():
    """test getting nothing from in memory repository"""
    repository = InMemoryUserRepository()
    assert not repository.get_users()


def test_repository_get_users__full():
    """test fetching users from in memory repository"""
    user = DomainUserFactory.create()
    repository = InMemoryUserRepository(storage={user.public_id: user})
    assert repository.get_users() == [user]


def test_repository_get_user__does_not_exist():
    """test getting nothing from in memory repository"""
    user = DomainUserFactory.create()
    repository = InMemoryUserRepository(storage={user.public_id: user})
    with pytest.raises(UserDoesNotExist):
        repository.get_user(public_id="does-not-exist")


def test_repository_get_user__exists():
    """test getting nothing from in memory repository"""
    user = DomainUserFactory.create()
    repository = InMemoryUserRepository(storage={user.public_id: user})
    assert repository.get_user(public_id=user.public_id) == user
