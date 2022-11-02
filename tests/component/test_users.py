"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

testing beerbox users resources behaviour
"""


import requests
from faker import Faker

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf

fake = Faker()


def test_user__nominal(host, port):
    """simple test scenario playing with users"""
    base = f"http://{host}:{port}"
    username = fake.user_name()

    # create a user with POST /users
    data = {"username": username}
    response = requests.post(f"{base}/users", json=data, timeout=1)
    public_id = response.json().get("publicId")
    assert response.status_code == 201
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "username": username,
    }

    # make sure we can get the created user with GET /users/:publicId
    response = requests.get(f"{base}/users/{public_id}", timeout=1)
    assert response.status_code == 200
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": public_id,
        "username": username,
    }

    # make sure we can get the created user with GET /users
    response = requests.get(f"{base}/users", timeout=1)
    assert response.status_code == 200
    assert (username, public_id) in [(i["username"], i["publicId"]) for i in response.json()]
