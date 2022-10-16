"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox database engine
"""

from sqlalchemy import create_engine
from sqlalchemy.future.engine import Engine

from beerbox import config

engine = create_engine(config.POSTGRES_URL, echo=config.POSTGRES_ECHO, future=True)


def get_engine() -> Engine:
    """Return the database engine, to be used as a dependency injector"""
    return engine
