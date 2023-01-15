"""
created by: thibault defeyter
created at: 2023/01/15
license: MIT

apibox alembic env configuration
"""
# pylint: disable=no-member

from logging.config import dictConfig

from alembic import context

# import models to make sure the metadata contains links to all database tables
import apibox.infrastructure.database.models  # pylint: disable=unused-import  # noqa
from apibox import config
from apibox.infrastructure.database.engine import engine
from apibox.infrastructure.database.models import DatabaseModel

# setup logging config
dictConfig(
    {
        "version": 1,
        "loggers": {
            "root": {"level": "WARN", "handlers": ("console",), "qualname": ""},  # type:ignore
            "sqlalchemy": {
                "level": "WARN",
                "handlers": None,
                "qualname": "sqlalchemy.engine",
            },  # type:ignore
            "alembic": {"level": "INFO", "handlers": None, "qualname": "alembic"},  # type:ignore
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "NOTSET",
                "formatter": "standard",
            }
        },
        "formatters": {
            "standard": {
                "format": "%(levelname)-5.5s [%(name)s] %(message)s",
                "datefmt": "%H:%M:%S",
            }
        },
    }
)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=config.POSTGRES_URL,
        target_metadata=DatabaseModel.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=DatabaseModel.metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
