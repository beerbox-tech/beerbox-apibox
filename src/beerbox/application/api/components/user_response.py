"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox api user response components
"""

from dataclasses import asdict
from datetime import datetime

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.users import User


class UserResponse(APIComponent):
    """API component representing a user"""

    public_id: str
    username: str
    created_at: datetime
    modified_at: datetime

    @classmethod
    def from_user(cls, user: User):
        """create a user response from a domain user"""
        return cls(**asdict(user))
