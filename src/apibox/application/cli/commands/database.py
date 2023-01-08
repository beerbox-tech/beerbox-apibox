"""
created by: thibault defeyter
created at: 2023/01/01
license: MIT

apibox CLI database management sub-command
"""

import click
from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError

config = Config("migrations/alembic.ini")


@click.group()
def database():
    """wrapper around alembic database migrations"""


@database.command()
@click.argument("revision")
@click.option(
    "--sql",
    is_flag=True,
    help="don't emit SQL to database, dump to standard output.",
)
def downgrade(revision, sql):  # pylint: disable=redefined-outer-name
    """revert to a previous version"""
    try:
        command.downgrade(config, revision, sql)
    except CommandError as error:
        click.echo(str(error))


@database.command()
@click.option(
    "-m",
    "--message",
    help="Message string to use with revision.",
)
@click.option(
    "--autogenerate",
    is_flag=True,
    help=(
        "populate revision script with candidate migration operations, "
        "based on comparison of database to model."
    ),
)
def revision(message, autogenerate):
    """create a new revision"""
    try:
        command.revision(config, message=message, autogenerate=autogenerate)
    except CommandError as error:
        click.echo(str(error))


@database.command()
@click.argument("revision")
@click.option(
    "--sql",
    is_flag=True,
    help="don't emit SQL to database, dump to standard output.",
)
def upgrade(revision, sql):  # pylint: disable=redefined-outer-name
    """upgrade to a later version"""
    try:
        command.upgrade(config, revision, sql)
    except CommandError as error:
        click.echo(str(error))
