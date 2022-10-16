"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox database health provider
"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from beerbox.application.health import Check
from beerbox.application.health import HealthIndicator
from beerbox.application.health import Status


class DatabaseReadiness(HealthIndicator):
    """database readiness health indicator"""

    def __init__(self, session: Session):
        self.session = session

    def get_check(self) -> Check:
        try:
            time = self.session.execute(select(func.now())).scalar()
            status = Status.PASS
            value = "true"
        except OperationalError:
            time = datetime.now()
            status = Status.FAIL
            value = "false"
        return Check(
            name="database:ready",
            time=time,  # type: ignore
            status=status,
            observed_value=value,
            observed_unit="boolean",
        )
