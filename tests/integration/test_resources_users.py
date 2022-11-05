"""
created by: thibault defeyter
created at: 2022/11/05
license: MIT

beerbox users resources integration tests
"""


from tests.factories import DatabaseUserFactory
from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_get_users(client, session):
    """test get users resource"""
    DatabaseUserFactory.create(username="user")

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {
            "createdAt": AnyDatetimeString(),
            "modifiedAt": AnyDatetimeString(),
            "publicId": AnyInstanceOf(str),
            "username": "user",
        }
    ]


def test_post_users(client, session):
    """test get readyz resource"""
    response = client.post("/users", json={"username": "user"})

    assert response.status_code == 201
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "username": "user",
    }


def test_get_user(client, session):
    """test get readyz resource"""
    user = DatabaseUserFactory.create()

    response = client.get(f"/users/{user.public_id}")

    assert response.status_code == 200
    assert response.json() == {
        "createdAt": user.created_at.isoformat(),
        "modifiedAt": user.modified_at.isoformat(),
        "publicId": user.public_id,
        "username": user.username,
    }
