"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

beerbox data factories
"""


import factory

from beerbox.config import IDENTIFIER_ALPHABET
from beerbox.config import IDENTIFIER_SIZE
from beerbox.domain.users import User as DomainUser


class DomainUserFactory(factory.Factory):
    """domain users factory"""

    public_id = factory.Faker(
        "lexify",
        text="?" * IDENTIFIER_SIZE,
        letters=IDENTIFIER_ALPHABET,
    )  # type: ignore
    created_at = factory.Faker("date_time")  # type: ignore
    modified_at = factory.Faker("date_time")  # type: ignore
    username = factory.Faker("user_name")  # type: ignore

    class Meta:
        model = DomainUser
