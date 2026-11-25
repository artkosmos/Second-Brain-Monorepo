from fastapi import APIRouter

from dependencies.user import CurrentUserDep
from schemas.security import UserResponse

router = APIRouter(prefix="/user", tags=["User 🧑"])


@router.get("/me", summary="Current user 🧑")
async def me(user: CurrentUserDep) -> UserResponse:
    return UserResponse.model_validate(user)
