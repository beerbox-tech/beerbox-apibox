"""
created by: thibault defeyter
created at: 2022/10/21
licene: MIT

beerbox applications' entrypoint
"""

from beerbox.application.api.app import create_app

app = create_app()
