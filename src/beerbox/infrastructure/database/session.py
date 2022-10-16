"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox database session manamagement
"""

from fastapi import Depends
from sqlalchemy.future.engine import Engine
from sqlalchemy.orm import Session

from beerbox.infrastructure.database.engine import get_engine


def open_session(engine: Engine) -> Session:
    """Open a database session, to be used as a context manager"""
    return Session(engine, future=True)


def get_session(engine: Engine = Depends(get_engine)):
    """Open a database session, to be used as a dependency injector"""
    with open_session(engine) as session:
        yield session
