from db.models import UsersORM
from dependencies.session import SessionDep
from dependencies.token import TokenPayloadDep
from fastapi import HTTPException


def get_current_user(session: SessionDep, token_payload: TokenPayloadDep) -> UsersORM:
    user = session.get(UsersORM, token_payload["user_id"])

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
