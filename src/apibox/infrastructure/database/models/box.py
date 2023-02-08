"""
created by: thibault defeyter
created at: 2022/02/04
licene: MIT

apibox box database model
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from apibox.infrastructure.database.models.base import DatabaseModel


class Box(DatabaseModel):
    """database representation of a box"""

    __tablename__ = "boxes"

    # private and public ids
    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(16), unique=True)

    # control dates
    created_at: Mapped[datetime]
    modified_at: Mapped[datetime]

    # data columns
    name: Mapped[str] = mapped_column(String(128), unique=True)

    def __repr__(self) -> str:
        return f"<Box #{self.id}>"
