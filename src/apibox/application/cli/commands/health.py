"""
created by: thibault defeyter
created at: 2023/01/01
license: MIT

apibox CLI health sub-command
"""

import click

from apibox.application.health import ApplicationReadiness
from apibox.infrastructure.database.engine import engine
from apibox.infrastructure.database.health import DatabaseReadiness
from apibox.infrastructure.database.session import open_session


def _print(*args):
    click.echo("".join(f"{arg:<16}" for arg in args))


@click.command()
def healthcheck():
    """healthcheck command controller"""
    application_ready = ApplicationReadiness()
    with open_session(engine) as session:
        database_ready = DatabaseReadiness(session=session)
        checks = [application_ready.get_check(), database_ready.get_check()]
    _print("check", "status", "observed value", "observed unit")
    _print("---", "---", "---", "---")
    for check in checks:
        _print(
            check.name,
            check.status.value,
            check.observed_value,
            check.observed_unit,
        )
