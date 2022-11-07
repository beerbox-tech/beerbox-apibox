"""
created by: thibault defeyter
created at: 2022/11/07
license: MIT

beerbox users resources integration tests
"""

from tests.factories import DatabaseContributionFactory
from tests.factories import DatabaseUserFactory
from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_get_contributions(client, session):
    """test get contributions resource"""
    DatabaseContributionFactory.create(
        amount=100,
        public_id="public-id",
        description="description",
        user__public_id="user-public-id",
    )

    response = client.get("/contributions")

    assert response.status_code == 200
    assert response.json() == [
        {
            "createdAt": AnyDatetimeString(),
            "modifiedAt": AnyDatetimeString(),
            "amount": 100,
            "description": "description",
            "publicId": "public-id",
            "userId": "user-public-id",
        }
    ]


def test_post_contributions(client, session):
    """test post contributions resource"""
    user = DatabaseUserFactory.create()
    data = {"userId": user.public_id, "amount": 100, "description": "description"}

    response = client.post("/contributions", json=data)

    assert response.status_code == 201
    assert response.json() == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "amount": 100,
        "description": "description",
        "publicId": AnyInstanceOf(str),
        "userId": user.public_id,
    }


def test_get_contribution(client, session):
    """test get readyz resource"""
    contribution = DatabaseContributionFactory.create()

    response = client.get(f"/contributions/{contribution.public_id}")

    assert response.status_code == 200
    assert response.json() == {
        "createdAt": contribution.created_at.isoformat(),
        "modifiedAt": contribution.modified_at.isoformat(),
        "amount": contribution.amount,
        "description": contribution.description,
        "publicId": contribution.public_id,
        "userId": contribution.user.public_id,
    }
