"""
created by: thibault defeyter
created at: 2022/02/04
license: MIT

unit testing apibox box resources
"""

import json
from unittest.mock import Mock

import pytest

from apibox.application.api.components.box_request import BoxRequest
from apibox.application.api.resources.boxes import get_box
from apibox.application.api.resources.boxes import get_box_repository
from apibox.application.api.resources.boxes import get_boxes
from apibox.application.api.resources.boxes import post_boxes
from apibox.domain.boxes import Box
from apibox.domain.boxes import BoxRepository
from tests.factories import DomainBoxFactory
from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def mock_request(url: str) -> Mock:
    """create a mock request"""
    mock = Mock()
    mock.url.path = url
    return mock


def mock_box_repository(box: Box | None = None) -> Mock:
    """create a box repository"""
    mock = Mock()
    if box:
        mock.get_boxes.return_value = [box]
        mock.get_box.return_value = box
    return mock


def test_get_box_repository():
    """make sure get_box_repository returns a BoxRepository"""
    repository = get_box_repository()
    assert isinstance(repository, BoxRepository)


@pytest.mark.asyncio
async def test_get_boxes():
    """test GET /boxes resource"""
    box = DomainBoxFactory.create()
    repository = mock_box_repository(box)

    response = await get_boxes(repository)

    repository.get_boxes.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.body) == [
        {
            "createdAt": box.created_at.isoformat(),
            "modifiedAt": box.modified_at.isoformat(),
            "publicId": box.public_id,
            "name": box.name,
        },
    ]


@pytest.mark.asyncio
async def test_get_box():
    """test GET /box/:publicId resource"""
    box = DomainBoxFactory.create()
    repository = mock_box_repository(box)

    response = await get_box("public-id", repository)

    repository.get_box.assert_called_once()
    assert response.status_code == 200
    assert json.loads(response.body) == {
        "createdAt": box.created_at.isoformat(),
        "modifiedAt": box.modified_at.isoformat(),
        "publicId": box.public_id,
        "name": box.name,
    }


@pytest.mark.asyncio
async def test_post_boxes():
    """test POST /boxes resource"""
    repository = mock_box_repository()
    request = BoxRequest(name="test")

    response = await post_boxes(request, repository)

    repository.add_box.assert_called_once()
    assert response.status_code == 201
    assert json.loads(response.body) == {
        "createdAt": AnyDatetimeString(),
        "modifiedAt": AnyDatetimeString(),
        "publicId": AnyInstanceOf(str),
        "name": "test",
    }
