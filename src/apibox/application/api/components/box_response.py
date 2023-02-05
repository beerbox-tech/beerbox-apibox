"""
created by: thibault defeyter
created at: 2022/02/04
license: MIT

apibox api box response components
"""

from __future__ import annotations

from datetime import datetime

from apibox.application.api.components.base import APIComponent
from apibox.domain.boxes import Box


class BoxResponse(APIComponent):
    """API component representing a box"""

    created_at: datetime
    modified_at: datetime
    public_id: str
    name: str

    @classmethod
    def from_box(cls, box: Box) -> BoxResponse:
        """create a box response from a domain box"""
        return cls(
            created_at=box.created_at,
            modified_at=box.modified_at,
            public_id=box.public_id,
            name=box.name,
        )
