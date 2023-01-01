"""
created by: thibault defeyter
created at: 2023/01/01
license: MIT

apibox CLI application
"""

from click import Group

from apibox.application.cli.commands.health import healthcheck


def create_cli() -> Group:
    """create a cli entrypoint"""
    cli = Group("apibox")
    cli.add_command(healthcheck)
    return cli
