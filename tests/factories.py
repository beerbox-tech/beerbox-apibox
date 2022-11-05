"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

beerbox data factories
"""


import factory

from beerbox.config import IDENTIFIER_ALPHABET
from beerbox.config import IDENTIFIER_SIZE
from beerbox.domain.contributions import Contribution as DomainContribution
from beerbox.domain.users import User as DomainUser
from beerbox.infrastructure.database.models import Contribution as DatabaseContribution
from beerbox.infrastructure.database.models import User as DatabaseUser
from tests.integration.conftest import session


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


class DatabaseUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """database users factory"""

    public_id = factory.Faker(
        "lexify",
        text="?" * IDENTIFIER_SIZE,
        letters=IDENTIFIER_ALPHABET,
    )  # type: ignore
    created_at = factory.Faker("date_time")  # type: ignore
    modified_at = factory.Faker("date_time")  # type: ignore
    username = factory.Faker("user_name")  # type: ignore

    class Meta:
        model = DatabaseUser
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"


class DomainContributionFactory(factory.Factory):
    """domain users factory"""

    public_id = factory.Faker(
        "lexify",
        text="?" * IDENTIFIER_SIZE,
        letters=IDENTIFIER_ALPHABET,
    )  # type: ignore
    created_at = factory.Faker("date_time")  # type: ignore
    modified_at = factory.Faker("date_time")  # type: ignore
    amount = factory.Faker("pyint")  # type: ignore
    description = factory.Faker("sentence")  # type: ignore
    user_id = factory.Faker(
        "lexify",
        text="?" * IDENTIFIER_SIZE,
        letters=IDENTIFIER_ALPHABET,
    )  # type: ignore

    class Meta:
        model = DomainContribution


class DatabaseContributionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """database contributions factory"""

    public_id = factory.Faker(
        "lexify",
        text="?" * IDENTIFIER_SIZE,
        letters=IDENTIFIER_ALPHABET,
    )  # type: ignore
    created_at = factory.Faker("date_time")  # type: ignore
    modified_at = factory.Faker("date_time")  # type: ignore
    amount = factory.Faker("pyint")  # type: ignore
    description = factory.Faker("word")  # type: ignore
    user_id = factory.LazyAttribute(lambda o: o.user.public_id)  # type: ignore
    user = factory.SubFactory(DatabaseUserFactory)  # type: ignore

    class Meta:
        model = DatabaseContribution
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"
