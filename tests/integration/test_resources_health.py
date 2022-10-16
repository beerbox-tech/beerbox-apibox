"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox health resources integration tests
"""


import pytest

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


@pytest.mark.asyncio
async def test_livez(client):
    """test get livez resource"""
    response = client.get("/livez")

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "beerbox-backend:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            }
        ],
        "service": "beerbox-backend",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }


@pytest.mark.asyncio
async def test_readyz(client):
    """test get readyz resource"""
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "beerbox-backend:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            },
            {
                "name": "database:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            },
        ],
        "service": "beerbox-backend",
        "status": "pass",
        "version": "dev",
    }
