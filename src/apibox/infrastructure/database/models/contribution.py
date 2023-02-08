"""
created by: thibault defeyter
created at: 2022/11/05
licene: MIT

apibox users database model
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from apibox.infrastructure.database.models.base import DatabaseModel

if TYPE_CHECKING:
    from apibox.infrastructure.database.models.user import User


class Contribution(DatabaseModel):
    """database representation of a contribution"""

    __tablename__ = "contributions"

    # private and public ids
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(16), unique=True)

    # control dates
    created_at: Mapped[datetime]
    modified_at: Mapped[datetime]

    # data columns
    amount: Mapped[int]
    description: Mapped[str] = mapped_column(String(128))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # relationships
    user: Mapped["User"] = relationship(back_populates="contributions")

    def __repr__(self) -> str:
        return f"<Contribution #{self.id}>"
