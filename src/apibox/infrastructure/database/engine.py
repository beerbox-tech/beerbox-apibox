"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

apibox database engine
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from apibox import config

engine = create_engine(config.POSTGRES_URL, echo=config.POSTGRES_ECHO)


def get_engine() -> Engine:
    """Return the database engine, to be used as a dependency injector"""
    return engine
