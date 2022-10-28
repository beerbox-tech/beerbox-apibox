"""
created by: thibault defeyter
created at: 2022/10/28
licene: MIT

beerbox users domain
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from typing import runtime_checkable


@dataclass
class User:
    """a beerbox user"""

    created_at: datetime
    modified_at: datetime
    public_id: str
    username: str


class UserDoesNotExist(Exception):
    """error raised when trying to access a user that does not exist"""

    def __init__(self, public_id: str):
        self.public_id = public_id

    def __repr__(self) -> str:
        return f"UserDoesNotExist(public_id='{self.public_id}')"


class UserAlreadyExist(Exception):
    """error raised when trying to create a user that already exist"""

    def __init__(self, username: str):
        self.username = username

    def __repr__(self) -> str:
        return f"UserAlreadyExist(username='{self.username}')"


@runtime_checkable
class UserRepository(Protocol):
    """protocol to be implemented by user concrete repositories"""

    def get_users(self) -> list[User]:
        """get all users"""
        ...

    def get_user(self, public_id: str) -> User:
        """return the user matching public id"""
        ...

    def add_user(self, user: User) -> None:
        """add a user to the repository"""
        ...


class InMemoryUserRepository(UserRepository):
    """user repository managing data from in-memory dictionary"""

    def __init__(self, storage: dict[str, User] | None = None):
        self.storage = storage or {}

    def get_users(self) -> list[User]:
        return list(self.storage.values())

    def get_user(self, public_id: str) -> User:
        try:
            return self.storage[public_id]
        except KeyError as error:
            raise UserDoesNotExist(public_id) from error

    def add_user(self, user: User) -> None:
        if any(user.username == user.username for user in self.storage.values()):
            raise UserAlreadyExist(user.username)
        self.storage[user.public_id] = user
