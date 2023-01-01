"""
created by: thibault defeyter
created at: 2023/01/02
license: MIT

unit testing apibox health cli
"""

from unittest.mock import call
from unittest.mock import patch

from apibox.application.cli.commands.health import healthcheck


@patch("apibox.application.cli.commands.health.click")
def test_healthcheck(mock_click):
    """test healthcheck commands"""
    healthcheck.callback()
    assert mock_click.echo.call_args_list == [
        call("check           status          observed value  observed unit   "),
        call("---             ---             ---             ---             "),
        call("apibox:ready    pass            true            boolean         "),
        call("database:ready  fail            false           boolean         "),
    ]
