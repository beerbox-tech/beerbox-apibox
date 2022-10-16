"""
created by: thibault defeyter
created at: 2022/10/21
license: MIT

beerbox api health resources
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from beerbox.application.api.components.health_response import HealthResponse
from beerbox.application.api.response import APIResponse
from beerbox.application.health import ApplicationReadiness
from beerbox.application.health import HealthIndicator
from beerbox.application.health import Status
from beerbox.infrastructure.database.health import DatabaseReadiness
from beerbox.infrastructure.database.session import get_session

router = APIRouter()


def get_application_readiness() -> HealthIndicator:
    """return an application readiness indicator"""
    return ApplicationReadiness()


def get_database_readiness(session: Session = Depends(get_session)) -> HealthIndicator:
    """return a database readiness indicator"""
    return DatabaseReadiness(session=session)


@router.get("/readyz")
async def get_readyz(
    application_ready: HealthIndicator = Depends(get_application_readiness),
    database_ready: HealthIndicator = Depends(get_database_readiness),
) -> APIResponse:
    """readyz resource controller
    the api is considered ready when the application and all its dependencies are ready
    """
    checks = [application_ready.get_check(), database_ready.get_check()]
    response = HealthResponse.from_checks(checks)
    status_code = status.HTTP_200_OK
    if response.status == Status.FAIL:
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return APIResponse(content=response, status_code=status_code)


@router.get("/livez")
async def get_livez(
    application_ready: HealthIndicator = Depends(get_application_readiness),
) -> APIResponse:
    """livez resource controller
    the api is considered alive when the application is ready
    """
    checks = [application_ready.get_check()]
    response = HealthResponse.from_checks(checks)
    return APIResponse(content=response, status_code=status.HTTP_200_OK)
