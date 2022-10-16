"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

unit testing beerbox health resources
"""

import json
from datetime import datetime
from unittest.mock import Mock

import pytest

from beerbox.application.api.resources.health import get_application_readiness
from beerbox.application.api.resources.health import get_database_readiness
from beerbox.application.api.resources.health import get_livez
from beerbox.application.api.resources.health import get_readyz
from beerbox.application.health import ApplicationReadiness
from beerbox.application.health import Check
from beerbox.application.health import Status
from beerbox.infrastructure.database.health import DatabaseReadiness
from tests.utils import AnyInstanceOf


def mock_request(url: str) -> Mock:
    """create a mock request"""
    mock = Mock()
    mock.url.path = url
    return mock


def mock_health_provider(success: bool = True) -> Mock:
    """create a health provider mock"""
    mock = Mock()
    mock.get_check.return_value = Check(
        name="test",
        time=datetime(2020, 1, 1),
        status=Status.PASS if success else Status.FAIL,
        observed_value="true" if success else "false",
        observed_unit="boolean",
    )
    return mock


def test_get_application_readiness():
    """make sure get_application_readiness returns a ApplicationReadiness"""
    indicator = get_application_readiness()
    assert isinstance(indicator, ApplicationReadiness)


def test_get_database_readiness():
    """make sure get_database_readiness return a DatabaseReadiness"""
    indicator = get_database_readiness(session=Mock())
    assert isinstance(indicator, DatabaseReadiness)


@pytest.mark.asyncio
async def test_readyz__success():
    """test readyz resource"""
    health_provider = mock_health_provider()

    response = await get_readyz(
        application_ready=health_provider,
        database_ready=health_provider,
    )

    assert response.status_code == 200
    assert json.loads(response.body) == {
        "checks": [
            {
                "name": "test",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": "2020-01-01T00:00:00",
            },
            {
                "name": "test",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": "2020-01-01T00:00:00",
            },
        ],
        "service": "beerbox-backend",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }


@pytest.mark.asyncio
async def test_readyz__failure():
    """test readyz resource"""

    response = await get_readyz(
        application_ready=mock_health_provider(success=True),
        database_ready=mock_health_provider(success=False),
    )

    assert response.status_code == 503
    assert json.loads(response.body) == {
        "checks": [
            {
                "name": "test",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": "2020-01-01T00:00:00",
            },
            {
                "name": "test",
                "observedUnit": "boolean",
                "observedValue": "false",
                "status": "fail",
                "time": "2020-01-01T00:00:00",
            },
        ],
        "service": "beerbox-backend",
        "status": "fail",
        "version": AnyInstanceOf(str),
    }


@pytest.mark.asyncio
async def test_livez():
    """test livez resource"""
    health_provider = mock_health_provider()

    response = await get_livez(application_ready=health_provider)

    assert response.status_code == 200
    assert json.loads(response.body) == {
        "checks": [
            {
                "name": "test",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": "2020-01-01T00:00:00",
            }
        ],
        "service": "beerbox-backend",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }
