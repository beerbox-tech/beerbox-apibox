"""
created by: thibault defeyter
created at: 2022/10/30
license: MIT

beerbox api user resources
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from beerbox.application.api.components.user_request import UserRequest
from beerbox.application.api.components.user_response import UserResponse
from beerbox.application.api.response import APIResponse
from beerbox.domain.users import InMemoryUserRepository
from beerbox.domain.users import UserRepository

router = APIRouter()
_repository = InMemoryUserRepository()


def get_user_repository() -> UserRepository:
    """return a user repository, to be used as dependency injector"""
    return _repository


@router.get("/users")
async def get_users(
    repository: UserRepository = Depends(get_user_repository),
) -> APIResponse:
    """users collection resource controller"""
    users = repository.get_users()
    return APIResponse(
        content=[UserResponse.from_user(u) for u in users],
        status_code=status.HTTP_200_OK,
    )


@router.get("/users/{public_id}")
async def get_user(
    public_id: str,
    repository: UserRepository = Depends(get_user_repository),
) -> APIResponse:
    """user resource controller"""
    user = repository.get_user(public_id)
    return APIResponse(
        content=UserResponse.from_user(user),
        status_code=status.HTTP_200_OK,
    )


@router.post("/users")
async def post_users(
    request: UserRequest,
    repository: UserRepository = Depends(get_user_repository),
) -> APIResponse:
    """users creation resource controller"""
    user = request.to_user()
    repository.add_user(user)
    return APIResponse(
        content=UserResponse.from_user(user),
        status_code=status.HTTP_201_CREATED,
    )
