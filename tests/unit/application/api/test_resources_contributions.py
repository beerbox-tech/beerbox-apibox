"""
created by: thibault defeyter
created at: 2022/11/07
license: MIT

unit testing beerbox contributions resources
"""

import json
from unittest.mock import Mock

import pytest

from beerbox.application.api.components.contribution_request import ContributionRequest
from beerbox.application.api.resources.contributions import get_contribution
from beerbox.application.api.resources.contributions import get_contribution_repository
from beerbox.application.api.resources.contributions import get_contributions
from beerbox.application.api.resources.contributions import post_contributions
from beerbox.domain.contributions import Contribution
from beerbox.domain.contributions import ContributionRepository
from tests.factories import DomainContributionFactory
from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def mock_request(url: str) -> Mock:
    """create a mock request"""
    mock = Mock()
    mock.url.path = url
    return mock


def mock_contribution_repository(contribution: Contribution | None = None) -> Mock:
    """create a contribution repository mock"""
    mock = Mock()
    if contribution:
        mock.get_contributions.return_value = [contribution]
        mock.get_contribution.return_value = contribution
    return mock


def test_get_contribution_repository():
    """make sure get_contribution_repository returns a ContributionRepository"""
    repository = get_contribution_repository()
    assert isinstance(repository, ContributionRepository)


@pytest.mark.asyncio
async def test_get_contributions():
    """test GET /contributions resource"""
    contribution = DomainContributionFactory.create()
    repository = mock_contribution_repository(contribution)

    response = await get_contributions(repository)

    repository.get_contributions.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.body) == [
        {
            "createdAt": contribution.created_at.isoformat(),
            "modifiedAt": contribution.modified_at.isoformat(),
            "publicId": contribution.public_id,
            "userId": contribution.user_id,
            "amount": contribution.amount,
            "description": contribution.description,
        },
    ]


@pytest.mark.asyncio
async def test_get_contribution():
    """test GET /contribution/:publicId resource"""
    contribution = DomainContributionFactory.create()
    repository = mock_contribution_repository(contribution)

    response = await get_contribution("public-id", repository)

    repository.get_contribution.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.body) == {
        "createdAt": contribution.created_at.isoformat(),
        "modifiedAt": contribution.modified_at.isoformat(),
        "publicId": contribution.public_id,
        "userId": contribution.user_id,
        "amount": contribution.amount,
        "description": contribution.description,
    }


@pytest.mark.asyncio
async def test_post_contributions():
    """test POST /contributions resource"""
    repository = mock_contribution_repository()
    request = ContributionRequest(user_id="test", amount=10, description="description")

    response = await post_contributions(request, repository)

    repository.add_contribution.assert_called_once()
    assert response.status_code == 201
    assert json.loads(response.body) == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "userId": "test",
        "amount": 10,
        "description": "description",
    }
