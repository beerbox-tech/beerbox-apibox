"""
created by: thibault defeyter
created at: 2022/02/04
licene: MIT

apibox boxes domain
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from typing import runtime_checkable


@dataclass
class Box:
    """a beer box"""

    name: str
    created_at: datetime
    modified_at: datetime
    public_id: str


class BoxDoesNotExist(Exception):
    """error raised when trying to access a box that does not exist"""

    def __init__(self, public_id: str):
        self.public_id = public_id

    def __repr__(self) -> str:
        return f"BoxDoesNotExist(public_id='{self.public_id}')"


class BoxAlreadyExist(Exception):
    """error raised when trying to create a box that already exist"""

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"BoxAlreadyExist(name='{self.name}')"


@runtime_checkable
class BoxRepository(Protocol):
    """protocol to be implemented by box concrete repositories"""

    def get_boxes(self) -> list[Box]:
        """get boxes matching filters"""
        ...

    def get_box(self, public_id: str) -> Box:
        """return the box matching public id"""
        ...

    def add_box(self, box: Box) -> None:
        """add a box to the repository"""
        ...


class InMemoryBoxRepository(BoxRepository):
    """box repository managing data from in-memory dictionary"""

    def __init__(self, storage: dict[str, Box] | None = None):
        self.storage = storage if storage is not None else {}

    def get_boxes(self) -> list[Box]:
        return list(self.storage.values())

    def get_box(self, public_id: str) -> Box:
        try:
            return self.storage[public_id]
        except KeyError as error:
            raise BoxDoesNotExist(public_id) from error

    def add_box(self, box: Box) -> None:
        if any(box.name == b.name for b in self.storage.values()):
            raise BoxAlreadyExist(box.name)
        self.storage[box.public_id] = box
