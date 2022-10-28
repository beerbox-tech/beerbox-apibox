"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox unit tests configuration
"""

from datetime import datetime

import pytest

from beerbox.domain.contributions import Contribution
from beerbox.domain.users import User


@pytest.fixture(name="contribution", scope="session")
def fixture_contribution():
    """expose a host fixture"""
    return Contribution(
        amount=10,
        created_at=datetime(2020, 1, 1),
        modified_at=datetime(2020, 1, 1),
        public_id="id",
        username="user",
    )


@pytest.fixture(name="user", scope="session")
def fixture_user():
    """expose a host fixture"""
    return User(
        created_at=datetime(2020, 1, 1),
        modified_at=datetime(2020, 1, 1),
        public_id="id",
        username="user",
    )
