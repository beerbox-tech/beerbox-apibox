"""
created by: thibault defeyter
created at: 2023/01/02
license: MIT

unit testing apibox health cli
"""

from unittest.mock import patch

from alembic.config import Config
from alembic.util.exc import CommandError

from apibox.application.cli.commands.database import downgrade
from apibox.application.cli.commands.database import revision
from apibox.application.cli.commands.database import upgrade
from tests.utils import AnyInstanceOf


@patch("apibox.application.cli.commands.database.command")
def test_downgrade(mock_command):
    """test downgrade commands"""
    downgrade.callback(revision="revision", sql=False)
    mock_command.downgrade.assert_called_once_with(AnyInstanceOf(Config), "revision", False)


@patch("apibox.application.cli.commands.database.command")
@patch("apibox.application.cli.commands.database.click")
def test_downgrade__failure(mock_click, mock_command):
    """test downgrade commands"""
    mock_command.downgrade.side_effect = CommandError("error")
    downgrade.callback(revision="revision", sql=False)
    mock_click.echo.assert_called_once_with("error")


@patch("apibox.application.cli.commands.database.command")
def test_revision(mock_command):
    """test revision commands"""
    revision.callback(message="message", autogenerate=True)
    mock_command.revision.assert_called_once_with(
        AnyInstanceOf(Config), message="message", autogenerate=True
    )


@patch("apibox.application.cli.commands.database.command")
@patch("apibox.application.cli.commands.database.click")
def test_revision__failure(mock_click, mock_command):
    """test revision commands"""
    mock_command.revision.side_effect = CommandError("error")
    revision.callback(message="message", autogenerate=True)
    mock_click.echo.assert_called_once_with("error")


@patch("apibox.application.cli.commands.database.command")
def test_upgrade(mock_command):
    """test upgrade commands"""
    upgrade.callback(revision="revision", sql=False)
    mock_command.upgrade.assert_called_once_with(AnyInstanceOf(Config), "revision", False)


@patch("apibox.application.cli.commands.database.command")
@patch("apibox.application.cli.commands.database.click")
def test_upgrade__failure(mock_click, mock_command):
    """test upgrade commands"""
    mock_command.upgrade.side_effect = CommandError("error")
    upgrade.callback(revision="revision", sql=False)
    mock_click.echo.assert_called_once_with("error")
