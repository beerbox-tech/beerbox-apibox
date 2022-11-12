"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

apibox api error response
"""

from typing import Any
from typing import Optional

from apibox.application.api.components.base import APIComponent


class ErrorResponse(APIComponent):
    """API component representing any error"""

    code: str
    data: Optional[Any] = None
    message: str
