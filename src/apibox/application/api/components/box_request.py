"""
created by: thibault defeyter
created at: 2022/02/04
license: MIT

apibox api box request component
"""

from datetime import datetime
from datetime import timezone

from pydantic import constr

from apibox.application.api.components.base import APIComponent
from apibox.domain.boxes import Box
from apibox.utils.identifiers import generate_identifier

Boxname = constr(regex=r"[a-zA-Z0-9\s]+")


class BoxRequest(APIComponent):
    """API component representing a box creation request"""

    name: Boxname  # type: ignore

    def to_box(self) -> Box:
        """create a domain box from a box request"""
        return Box(
            public_id=generate_identifier(),
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
            name=self.name,
        )
