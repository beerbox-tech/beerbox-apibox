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
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from apibox.infrastructure.database.models.base import DatabaseModel
from apibox.infrastructure.database.models.user import User


class Contribution(DatabaseModel):
    """database representation of a contribution"""

    __tablename__ = "contributions"

    # private and public ids
    id: int = Column(Integer, primary_key=True)
    public_id: str = Column(String(16), nullable=False, unique=True)

    # control dates
    created_at: datetime = Column(DateTime(timezone=True), nullable=False)
    modified_at: datetime = Column(DateTime(timezone=True), nullable=False)

    # data columns
    amount: int = Column(Integer, nullable=False)
    description: str = Column(String(128), nullable=False)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    # relationships
    user: User = relationship(User)

    def __repr__(self) -> str:
        return f"<Contribution #{self.id}>"
