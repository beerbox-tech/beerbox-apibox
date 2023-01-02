"""
created by: thibault defeyter
created at: 2022/10/21
licene: MIT

apibox applications' entrypoint
"""

from apibox.application.api.app import create_app
from apibox.application.cli.app import create_cli

app = create_app()
cli = create_cli()
