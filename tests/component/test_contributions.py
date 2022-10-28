"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

testing beerbox contributions resources behaviour
"""


import requests

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_contribution__nominal(host, port):
    """simple test scenario playing with contributions"""
    base = f"http://{host}:{port}"

    # test a simple GET /contributions
    response = requests.get(f"{base}/contributions", timeout=1)
    assert response.status_code == 200
    assert response.json() == []

    # create a contribution with POST /contributions
    data = {"amount": 100, "username": "user"}
    response = requests.post(f"{base}/contributions", json=data, timeout=1)
    public_id = response.json().get("publicId")
    assert response.status_code == 201
    assert response.json() == {
        "amount": 100,
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "username": "user",
    }

    # make sure we can get the created contribution with GET /contributions/:publicId
    response = requests.get(f"{base}/contributions/{public_id}", timeout=1)
    assert response.status_code == 200
    assert response.json() == {
        "amount": 100,
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": public_id,
        "username": "user",
    }

    # make sure we can get the created contribution with GET /contributions
    response = requests.get(f"{base}/contributions", timeout=1)
    assert response.status_code == 200
    assert response.json() == [
        {
            "amount": 100,
            "createdAt": AnyDatetimeString(),
            "modifiedAt": AnyDatetimeString(),
            "publicId": public_id,
            "username": "user",
        },
    ]
