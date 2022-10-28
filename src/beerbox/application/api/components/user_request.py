"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox api user request components
"""

from datetime import datetime
from datetime import timezone

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.users import User
from beerbox.utils.identifiers import generate_identifier


class UserRequest(APIComponent):
    """API component representing a user creation request"""

    username: str

    def to_user(self) -> User:
        """create a domain user from a domain request"""
        return User(
            public_id=generate_identifier(),
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
            username=self.username,
        )
