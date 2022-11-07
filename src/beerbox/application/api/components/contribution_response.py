"""
created by: thibault defeyter
created at: 2022/11/07
license: MIT

beerbox api contribution response components
"""

from __future__ import annotations

from datetime import datetime

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.contributions import Contribution


class ContributionResponse(APIComponent):
    """API component representing a contribution"""

    amount: int
    created_at: datetime
    description: str
    modified_at: datetime
    public_id: str
    user_id: str

    @classmethod
    def from_contribution(cls, contribution: Contribution) -> ContributionResponse:
        """create a contribution response from a domain contribution"""
        return cls(
            amount=contribution.amount,
            created_at=contribution.created_at,
            description=contribution.description,
            modified_at=contribution.modified_at,
            public_id=contribution.public_id,
            user_id=contribution.user_id,
        )
