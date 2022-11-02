"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

beerbox api user response components
"""

from __future__ import annotations

from datetime import datetime

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.users import User


class UserResponse(APIComponent):
    """API component representing a user"""

    created_at: datetime
    modified_at: datetime
    public_id: str
    username: str

    @classmethod
    def from_user(cls, user: User) -> UserResponse:
        """create a user response from a domain user"""
        return cls(
            created_at=user.created_at,
            modified_at=user.modified_at,
            public_id=user.public_id,
            username=user.username,
        )
