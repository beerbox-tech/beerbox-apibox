"""
created by: thibault defeyter
created at: 2022/10/25
license: MIT

beerbox api contribution resources
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from beerbox.application.api.components.contribution_request import ContributionRequest
from beerbox.application.api.components.contribution_response import ContributionResponse
from beerbox.application.api.response import APIResponse
from beerbox.domain.contributions import ContributionRepository
from beerbox.domain.contributions import InMemoryContributionRepository

router = APIRouter()
_repository = InMemoryContributionRepository()


def get_contribution_repository() -> ContributionRepository:
    """return a contribution repository, to be used as a dependency injector"""
    return _repository


@router.get("/contributions")
async def get_contributions(
    username: str | None = None,
    repository: ContributionRepository = Depends(get_contribution_repository),
) -> APIResponse:
    """contributions collection resource controller"""
    contributions = repository.get_contributions(username=username)
    return APIResponse(
        content=[ContributionResponse.from_contribution(c) for c in contributions],
        status_code=status.HTTP_200_OK,
    )


@router.get("/contributions/{public_id}")
async def get_contribution(
    public_id: str,
    repository: ContributionRepository = Depends(get_contribution_repository),
) -> APIResponse:
    """contributions collection resource controller"""
    contribution = repository.get_contribution(public_id)
    return APIResponse(
        content=ContributionResponse.from_contribution(contribution),
        status_code=status.HTTP_200_OK,
    )


@router.post("/contributions")
async def post_contributions(
    request: ContributionRequest,
    repository: ContributionRepository = Depends(get_contribution_repository),
) -> APIResponse:
    """contributions collection resource controller"""
    contribution = request.to_contribution()
    repository.add_contribution(contribution)
    return APIResponse(
        content=ContributionResponse.from_contribution(contribution),
        status_code=status.HTTP_201_CREATED,
    )
