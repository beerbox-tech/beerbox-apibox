"""
created by: thibault defeyter
created at: 2022/11/05
licene: MIT

apibox users database model
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from apibox.infrastructure.database.models.base import DatabaseModel

if TYPE_CHECKING:
    from apibox.infrastructure.database.models.contribution import Contribution


class User(DatabaseModel):
    """database representation of a user"""

    __tablename__ = "users"

    # private and public ids
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(unique=True)

    # control dates
    created_at: Mapped[datetime]
    modified_at: Mapped[datetime]

    # data columns
    username: Mapped[str] = mapped_column(String(128), unique=True)

    contributions: Mapped[list["Contribution"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"<User #{self.id}>"
