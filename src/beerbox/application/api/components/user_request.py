"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

beerbox api user request components
"""

from datetime import datetime
from datetime import timezone

from pydantic import constr

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.users import User
from beerbox.utils.identifiers import generate_identifier

Username = constr(regex=r"[a-zA-Z0-9]+")


class UserRequest(APIComponent):
    """API component representing a user creation request"""

    username: Username  # type: ignore

    def to_user(self) -> User:
        """create a domain user from a user request"""
        return User(
            public_id=generate_identifier(),
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
            username=self.username,
        )
