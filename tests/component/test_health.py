"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

testing apibox health resources behaviour
"""

import requests

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_livez(host, port):
    """test the /livez endpoint"""
    url = f"http://{host}:{port}/livez"

    response = requests.get(url, timeout=1)

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "apibox:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            },
        ],
        "service": "apibox",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }


def test_readyz(host, port):
    """test the /readyz endpoint"""
    url = f"http://{host}:{port}/readyz"

    response = requests.get(url, timeout=1)

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "apibox:ready",
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
        "service": "apibox",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }
