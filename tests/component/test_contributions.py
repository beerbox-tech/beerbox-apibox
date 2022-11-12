"""
created by: thibault defeyter
created at: 2022/11/07
license: MIT

testing apibox contributions resources behaviour
"""


import requests
from faker import Faker

from tests.utils import AnyDatetimeString

fake = Faker()


def test_contribution__nominal(host, port):
    """simple test scenario playing with contributions"""
    base = f"http://{host}:{port}"
    username = fake.user_name()

    # create a user with POST /users
    data = {"username": username}
    response = requests.post(f"{base}/users", json=data, timeout=1)
    user_id = response.json().get("publicId")

    # create a contribution with POST /contributions
    data = {"amount": 100, "userId": user_id, "description": "description"}
    response = requests.post(f"{base}/contributions", json=data, timeout=1)
    public_id = response.json().get("publicId")
    assert response.status_code == 201
    assert response.json() == {
        "amount": 100,
        "createdAt": AnyDatetimeString(),
        "description": "description",
        "modifiedAt": AnyDatetimeString(),
        "publicId": public_id,
        "userId": user_id,
    }

    # make sure we can get the created contribution with GET /contributions/:publicId
    response = requests.get(f"{base}/contributions/{public_id}", timeout=1)
    assert response.status_code == 200
    assert response.json() == {
        "amount": 100,
        "createdAt": AnyDatetimeString(),
        "description": "description",
        "modifiedAt": AnyDatetimeString(),
        "publicId": public_id,
        "userId": user_id,
    }

    # make sure we can get the created contribution with GET /contributions
    response = requests.get(f"{base}/contributions", timeout=1)
    assert response.status_code == 200
    assert (public_id, 100, "description", user_id) in [
        (i["publicId"], i["amount"], i["description"], i["userId"]) for i in response.json()
    ]
