"""
created by: thibault defeyter
created at: 2022/11/05
licene: MIT

beerbox contributions database repository
"""

from dataclasses import asdict

from sqlalchemy import bindparam
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.elements import BindParameter

from beerbox.domain.contributions import Contribution as DomainContribution
from beerbox.domain.contributions import ContributionDoesNotExist
from beerbox.domain.contributions import ContributionRepository
from beerbox.domain.contributions import ContributionUserDoesNotExist
from beerbox.infrastructure.database.models import Contribution as DatabaseContribution
from beerbox.infrastructure.database.models import User as DatabaseUser


class DatabaseContributionRepository(ContributionRepository):
    """contribution repository managing data from database"""

    def __init__(self, session):
        self.session = session

    def _transform(self, contribution: DatabaseContribution) -> DomainContribution:
        return DomainContribution(
            created_at=contribution.created_at,
            description=contribution.description,
            modified_at=contribution.modified_at,
            public_id=contribution.public_id,
            user_id=contribution.user.public_id,
            amount=contribution.amount,
        )

    def get_contributions(self) -> list[DomainContribution]:
        query = select(DatabaseContribution)
        return [self._transform(contrib) for contrib in self.session.execute(query).scalars()]

    def get_contribution(self, public_id: str) -> DomainContribution:
        query = select(DatabaseContribution).where(DatabaseContribution.public_id == public_id)
        try:
            contribution = self.session.execute(query).scalar_one()
        except (SQLAlchemyError, ValueError) as error:
            self.session.rollback()
            raise ContributionDoesNotExist(public_id) from error
        return self._transform(contribution)

    def add_contribution(self, contribution: DomainContribution) -> None:
        user: BindParameter = bindparam("user_id")
        subquery = select(DatabaseUser.id).where(DatabaseUser.public_id == user).scalar_subquery()
        query = insert(DatabaseContribution).values(user_id=subquery)
        try:
            self.session.execute(query, asdict(contribution))
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise ContributionUserDoesNotExist(contribution.user_id) from error
        except SQLAlchemyError as error:
            self.session.rollback()
            raise error
