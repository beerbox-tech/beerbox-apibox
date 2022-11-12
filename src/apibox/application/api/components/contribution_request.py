"""
created by: thibault defeyter
created at: 2022/11/07
license: MIT

apibox api contribution request components
"""

from datetime import datetime
from datetime import timezone

from pydantic import conint

from apibox.application.api.components.base import APIComponent
from apibox.domain.contributions import Contribution
from apibox.utils.identifiers import generate_identifier

Amount = conint(gt=0, lt=10000)


class ContributionRequest(APIComponent):
    """API component representing a contribution creation request"""

    amount: Amount  # type: ignore
    description: str
    user_id: str

    def to_contribution(self) -> Contribution:
        """create a domain contribution from a contribution request"""
        return Contribution(
            amount=self.amount,
            description=self.description,
            user_id=self.user_id,
            public_id=generate_identifier(),
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
        )
