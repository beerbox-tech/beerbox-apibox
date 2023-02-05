"""
created by: thibault defeyter
created at: 2022/02/04
license: MIT

apibox api boxes resources
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session

from apibox.application.api.components.box_request import BoxRequest
from apibox.application.api.components.box_response import BoxResponse
from apibox.application.api.response import APIResponse
from apibox.domain.boxes import BoxRepository
from apibox.infrastructure.database.repositories.box import DatabaseBoxRepository
from apibox.infrastructure.database.session import get_session

router = APIRouter()


def get_box_repository(session: Session = Depends(get_session)) -> BoxRepository:
    """return a box repository, to be used as dependency injector"""
    return DatabaseBoxRepository(session)


@router.get("/boxes")
async def get_boxes(
    repository: BoxRepository = Depends(get_box_repository),
) -> APIResponse:
    """boxes collection resource controller"""
    boxes = repository.get_boxes()
    return APIResponse(
        content=[BoxResponse.from_box(box) for box in boxes],
        status_code=status.HTTP_200_OK,
    )


@router.get("/boxes/{public_id}")
async def get_box(
    public_id: str,
    repository: BoxRepository = Depends(get_box_repository),
) -> APIResponse:
    """box resource controller"""
    box = repository.get_box(public_id)
    return APIResponse(
        content=BoxResponse.from_box(box),
        status_code=status.HTTP_200_OK,
    )


@router.post("/boxes")
async def post_boxes(
    request: BoxRequest,
    repository: BoxRepository = Depends(get_box_repository),
) -> APIResponse:
    """boxes creation resource controller"""
    box = request.to_box()
    repository.add_box(box)
    return APIResponse(
        content=BoxResponse.from_box(box),
        status_code=status.HTTP_201_CREATED,
    )
