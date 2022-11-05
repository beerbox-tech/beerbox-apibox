"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox database models
"""

from beerbox.infrastructure.database.models.base import DatabaseModel
from beerbox.infrastructure.database.models.contribution import Contribution
from beerbox.infrastructure.database.models.user import User

__all__ = [
    "Contribution",
    "DatabaseModel",
    "User",
]
