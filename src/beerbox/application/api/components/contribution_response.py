"""
created by: thibault defeyter
created at: 2022/10/25
license: MIT

beerbox api contribution request components
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

from beerbox.application.api.components.base import APIComponent
from beerbox.domain.contributions import Contribution


class ContributionResponse(APIComponent):
    """API component representing a contribution"""

    amount: int
    created_at: datetime
    modified_at: datetime
    public_id: str
    username: str

    @classmethod
    def from_contribution(cls, contribution: Contribution) -> ContributionResponse:
        """create a domain user from a domain request"""
        return cls(**asdict(contribution))
