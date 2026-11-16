from dependencies.user import CurrentUserDep
from fastapi import APIRouter
from schemas.security import UserResponse

router = APIRouter(prefix="/user", tags=["User 🧑"])


@router.get("/me", summary="Current user 🧑")
async def me(user: CurrentUserDep) -> UserResponse:
    return UserResponse.model_validate(user)
