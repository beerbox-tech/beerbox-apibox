"""
created by: thibault defeyter
created at: 2022/10/25
license: MIT

beerbox api contribution request components
"""

from datetime import datetime
from datetime import timezone

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.contributions import Contribution
from beerbox.utils.identifiers import generate_identifier


class ContributionRequest(APIComponent):
    """API component representing a contribution creation request"""

    amount: int
    username: str

    def to_contribution(self) -> Contribution:
        """create a domain contribution from a domain request"""
        return Contribution(
            amount=self.amount,
            username=self.username,
            public_id=generate_identifier(),
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
        )
