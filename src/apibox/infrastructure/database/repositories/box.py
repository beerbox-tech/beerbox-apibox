"""
created by: thibault defeyter
created at: 2022/02/04
licene: MIT

apibox boxes database repository
"""

from dataclasses import asdict

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

from apibox.domain.boxes import Box as DomainBox
from apibox.domain.boxes import BoxAlreadyExist
from apibox.domain.boxes import BoxDoesNotExist
from apibox.domain.boxes import BoxRepository
from apibox.infrastructure.database.models import Box as DatabaseBox


class DatabaseBoxRepository(BoxRepository):
    """box repository managing data from database"""

    def __init__(self, session):
        self.session = session

    def _transform(self, box: DatabaseBox) -> DomainBox:
        return DomainBox(
            created_at=box.created_at,
            modified_at=box.modified_at,
            public_id=box.public_id,
            name=box.name,
        )

    def get_boxes(self) -> list[DomainBox]:
        query = select(DatabaseBox)
        return [self._transform(box) for box in self.session.execute(query).scalars()]

    def get_box(self, public_id: str) -> DomainBox:
        query = select(DatabaseBox).where(DatabaseBox.public_id == public_id)
        try:
            box = self.session.execute(query).scalar_one()
        except (SQLAlchemyError, ValueError) as error:
            self.session.rollback()
            raise BoxDoesNotExist(public_id) from error
        return self._transform(box)

    def add_box(self, box: DomainBox) -> None:
        query = insert(DatabaseBox).values(asdict(box))  # type: ignore
        try:
            self.session.execute(query)
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise BoxAlreadyExist(box.name) from error
        except SQLAlchemyError as error:
            self.session.rollback()
            raise error
