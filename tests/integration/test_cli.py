"""
created by: thibault defeyter
created at: 2023/01/02
license: MIT

unit testing apibox health cli
"""

from click.testing import CliRunner

from apibox.application.cli.commands.health import healthcheck


def test_healthcheck():
    """test healthcheck commands"""
    runner = CliRunner()
    result = runner.invoke(healthcheck, [])
    assert result.exit_code == 0
    assert result.output == (
        "check           status          observed value  observed unit   \n"
        "---             ---             ---             ---             \n"
        "apibox:ready    pass            true            boolean         \n"
        "database:ready  pass            true            boolean         \n"
    )
