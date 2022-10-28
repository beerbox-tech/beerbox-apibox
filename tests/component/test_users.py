"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

testing beerbox users resources behaviour
"""


import requests

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_user__nominal(host, port):
    """simple test scenario playing with users"""
    base = f"http://{host}:{port}"

    # test a simple GET /users
    response = requests.get(f"{base}/users", timeout=1)
    assert response.status_code == 200
    assert response.json() == []

    # create a user with POST /users
    data = {"username": "user"}
    response = requests.post(f"{base}/users", json=data, timeout=1)
    public_id = response.json().get("publicId")
    assert response.status_code == 201
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "username": "user",
    }

    # make sure we can get the created user with GET /users/:publicId
    response = requests.get(f"{base}/users/{public_id}", timeout=1)
    assert response.status_code == 200
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": public_id,
        "username": "user",
    }

    # make sure we can get the created user with GET /users
    response = requests.get(f"{base}/users", timeout=1)
    assert response.status_code == 200
    assert response.json() == [
        {
            "createdAt": AnyDatetimeString(),
            "modifiedAt": AnyDatetimeString(),
            "publicId": public_id,
            "username": "user",
        },
    ]
