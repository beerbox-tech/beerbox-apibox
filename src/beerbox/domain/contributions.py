"""
created by: thibault defeyter
created at: 2022/10/28
licene: MIT

beerbox contributions domain
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class Contribution:
    """a beerbox contribution"""

    amount: int
    created_at: datetime
    modified_at: datetime
    public_id: str
    username: str


class ContributionDoesNotExist(Exception):
    """error raised when trying to access a contribution that does not exist"""

    def __init__(self, public_id: str):
        self.public_id = public_id

    def __repr__(self) -> str:
        return f"ContributionDoesNotExist(public_id='{self.public_id}')"


class ContributionAlreadyExist(Exception):
    """error raised when trying to create a contribution that already exist"""

    def __init__(self, public_id: str):
        self.public_id = public_id

    def __repr__(self) -> str:
        return f"ContributionAlreadyExist(public_id='{self.public_id}')"


class ContributionRepository(Protocol):
    """protocol to be implemented by contribution concrete repositories"""

    def get_contributions(self, username: str | None = None) -> list[Contribution]:
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

    def __init__(self, storage: dict[str, Contribution] | None = None):
        self.storage = storage or {}

    def get_contributions(self, username: str | None = None) -> list[Contribution]:
        contributions = list(self.storage.values())
        if username:
            return [c for c in contributions if c.username == username]
        return contributions

    def get_contribution(self, public_id: str) -> Contribution:
        try:
            return self.storage[public_id]
        except KeyError as error:
            raise ContributionDoesNotExist(public_id) from error

    def add_contribution(self, contribution: Contribution) -> None:
        if contribution.public_id in self.storage:
            raise ContributionAlreadyExist(contribution.public_id)
        self.storage[contribution.public_id] = contribution
