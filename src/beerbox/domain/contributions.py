"""
created by: thibault defeyter
created at: 2022/11/06
licene: MIT

beerbox contributions domain
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from typing import runtime_checkable

from beerbox.domain.users import User


@dataclass
class Contribution:
    """a beerbox contribution"""

    amount: int
    created_at: datetime
    description: str
    modified_at: datetime
    public_id: str
    user_id: str


class ContributionDoesNotExist(Exception):
    """error raised when accessing a contribution that does not exist"""

    def __init__(self, public_id: str):
        self.public_id = public_id

    def __repr__(self) -> str:
        return f"ContributionDoesNotExist(public_id='{self.public_id}')"


class ContributionUserDoesNotExist(Exception):
    """error raised when creating a contribution with unknown user"""

    def __init__(self, user_id: str):
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"ContributionUserDoesNotExist(user_id='{self.user_id}')"


@runtime_checkable
class ContributionRepository(Protocol):
    """protocol to be implemented by contribution concrete repositories"""

    def get_contributions(self) -> list[Contribution]:
        """get contributions matching filters"""
        ...

    def get_contribution(self, public_id: str) -> Contribution:
        """return the contribution matching public id"""
        ...

    def add_contribution(self, contribution: Contribution) -> None:
        """add a contribution to the repository"""
        ...


class InMemoryContributionRepository(ContributionRepository):
    """contribution repository managing data from in-memory dictionary"""

    def __init__(self, users: list[User] | None = None, storage: list[Contribution] | None = None):
        self.users = users or []
        self.storage = storage or []

    def get_contributions(self) -> list[Contribution]:
        return self.storage

    def get_contribution(self, public_id: str) -> Contribution:
        contributions = [item for item in self.storage if item.public_id == public_id]
        if not contributions:
            raise ContributionDoesNotExist(public_id)
        return contributions[0]

    def add_contribution(self, contribution: Contribution) -> None:
        if contribution.user_id not in [user.public_id for user in self.users]:
            raise ContributionUserDoesNotExist(contribution.user_id)
        self.storage.append(contribution)
