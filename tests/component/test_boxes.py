"""
created by: thibault defeyter
created at: 2022/02/04
license: MIT

testing apibox boxes resources behaviour
"""


import requests
from faker import Faker

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf

fake = Faker()


def test_box__nominal(host, port):
    """simple test scenario playing with boxes"""
    base = f"http://{host}:{port}"
    name = fake.word()

    # create a box with POST /boxes
    data = {"name": name}
    response = requests.post(f"{base}/boxes", json=data, timeout=1)
    public_id = response.json().get("publicId")
    assert response.status_code == 201
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "name": name,
    }

    # make sure we can get the created box with GET /boxes/:publicId
    response = requests.get(f"{base}/boxes/{public_id}", timeout=1)
    assert response.status_code == 200
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": public_id,
        "name": name,
    }

    # make sure we can get the created box with GET /boxes
    response = requests.get(f"{base}/boxes", timeout=1)
    assert response.status_code == 200
    assert (name, public_id) in [(i["name"], i["publicId"]) for i in response.json()]
