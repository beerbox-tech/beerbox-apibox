"""
created by: thibault defeyter
created at: 2022/02/04
license: MIT

apibox boxes resources integration tests
"""


from tests.factories import DatabaseBoxFactory
from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_get_boxes(client, session):
    """test get boxes resource"""
    DatabaseBoxFactory.create(name="box")

    response = client.get("/boxes")

    assert response.status_code == 200
    assert response.json() == [
        {
            "createdAt": AnyDatetimeString(),
            "modifiedAt": AnyDatetimeString(),
            "publicId": AnyInstanceOf(str),
            "name": "box",
        }
    ]


def test_post_boxes(client, session):
    """test post boxes resource"""
    response = client.post("/boxes", json={"name": "box"})

    assert response.status_code == 201
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "name": "box",
    }


def test_get_box(client, session):
    """test get readyz resource"""
    box = DatabaseBoxFactory.create()

    response = client.get(f"/boxes/{box.public_id}")

    assert response.status_code == 200
    assert response.json() == {
        "createdAt": box.created_at.isoformat(),
        "modifiedAt": box.modified_at.isoformat(),
        "publicId": box.public_id,
        "name": box.name,
    }
