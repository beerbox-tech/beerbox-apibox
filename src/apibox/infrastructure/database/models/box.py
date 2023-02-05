"""
created by: thibault defeyter
created at: 2022/02/04
licene: MIT

apibox box database model
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from apibox.infrastructure.database.models.base import DatabaseModel


class Box(DatabaseModel):
    """database representation of a box"""

    __tablename__ = "boxes"

    # private and public ids
    id: int = Column(Integer, primary_key=True)
    public_id: str = Column(String(16), nullable=False, unique=True)

    # control dates
    created_at: datetime = Column(DateTime(timezone=True), nullable=False)
    modified_at: datetime = Column(DateTime(timezone=True), nullable=False)

    # data columns
    name: str = Column(String(128), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Box #{self.id}>"
