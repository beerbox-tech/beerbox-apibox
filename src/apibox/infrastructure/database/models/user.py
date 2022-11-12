"""
created by: thibault defeyter
created at: 2022/11/05
licene: MIT

apibox users database model
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from apibox.infrastructure.database.models.base import DatabaseModel


class User(DatabaseModel):
    """database representation of a user"""

    __tablename__ = "users"

    # private and public ids
    id: int = Column(Integer, primary_key=True)
    public_id: str = Column(String(16), nullable=False, unique=True)

    # control dates
    created_at: datetime = Column(DateTime(timezone=True), nullable=False)
    modified_at: datetime = Column(DateTime(timezone=True), nullable=False)

    # data columns
    username: str = Column(String(128), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<User #{self.id}>"
