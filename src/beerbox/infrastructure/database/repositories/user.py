"""
created by: thibault defeyter
created at: 2022/11/05
licene: MIT

beerbox users database repository
"""

from dataclasses import asdict

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from beerbox.domain.users import User as DomainUser
from beerbox.domain.users import UserAlreadyExist
from beerbox.domain.users import UserDoesNotExist
from beerbox.domain.users import UserRepository
from beerbox.infrastructure.database.models import User as DatabaseUser


class DatabaseUserRepository(UserRepository):
    """user repository managing data from database"""

    def __init__(self, session):
        self.session = session

    def _transform(self, user: DatabaseUser) -> DomainUser:
        return DomainUser(
            created_at=user.created_at,
            modified_at=user.modified_at,
            public_id=user.public_id,
            username=user.username,
        )

    def get_users(self) -> list[DomainUser]:
        query = select(DatabaseUser)
        return [self._transform(user) for user in self.session.execute(query).scalars()]

    def get_user(self, public_id: str) -> DomainUser:
        query = select(DatabaseUser).where(DatabaseUser.public_id == public_id)
        try:
            user = self.session.execute(query).scalar_one()
        except (SQLAlchemyError, ValueError) as error:
            self.session.rollback()
            raise UserDoesNotExist(public_id) from error
        return self._transform(user)

    def add_user(self, user: DomainUser) -> None:
        query = insert(DatabaseUser).values(asdict(user))
        try:
            self.session.execute(query)
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise UserAlreadyExist(user.username) from error
        except SQLAlchemyError as error:
            self.session.rollback()
            raise error
