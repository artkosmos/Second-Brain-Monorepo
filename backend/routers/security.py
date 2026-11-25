from fastapi import APIRouter, HTTPException, Response
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select

from db.models import UsersORM
from dependencies.cookie import LogoutRefreshTokenDep
from dependencies.refresh_tokens import RefreshTokensRepositoryDep
from dependencies.session import SessionDep
from dependencies.settings import SettingsDep
from dependencies.token import RefreshTokenPayloadDep
from exceptions.storage_error import catch_storage_error
from schemas.security import LoginRequest, RegistrationRequest
from security.session import add_refresh_token
from security.token import (
    clear_auth_cookies,
    create_refresh_token,
    decode_refresh_token,
    set_auth_cookies,
)
from security.types import TokenPayload

router = APIRouter(prefix="/auth", tags=["Auth 🔒"])
password_hash = PasswordHash.recommended()


@router.post("/login", summary="Login")
async def login(
    payload: LoginRequest,
    settings: SettingsDep,
    session: SessionDep,
    repository: RefreshTokensRepositoryDep,
    response: Response,
) -> None:
    user = session.scalar(select(UsersORM).where(UsersORM.email == payload.email))

    if not user or not password_hash.verify(
        payload.password.get_secret_value(), user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    refresh_token = add_refresh_token(settings, repository, user.id)

    with catch_storage_error():
        session.commit()

    set_auth_cookies(
        response=response,
        data=TokenPayload(user_id=user.id),
        settings=settings,
        refresh_token=refresh_token,
    )


@router.post("/register", summary="Register", status_code=201)
async def register(
    payload: RegistrationRequest,
    settings: SettingsDep,
    session: SessionDep,
    repository: RefreshTokensRepositoryDep,
    response: Response,
) -> None:
    user = session.scalar(select(UsersORM).where(UsersORM.email == payload.email))

    if user:
        raise HTTPException(status_code=409, detail="User already exists")

    new_user = UsersORM(
        email=payload.email,
        hashed_password=password_hash.hash(payload.password.get_secret_value()),
    )
    session.add(new_user)

    with catch_storage_error():
        try:
            session.flush()
            refresh_token = add_refresh_token(settings, repository, new_user.id)
            session.commit()
        except IntegrityError as error:
            session.rollback()
            raise HTTPException(
                status_code=409, detail="User already exists"
            ) from error

    set_auth_cookies(
        response=response,
        data=TokenPayload(user_id=new_user.id),
        settings=settings,
        refresh_token=refresh_token,
    )


@router.post("/refresh", summary="Refresh access token")
async def refresh_token(
    settings: SettingsDep,
    response: Response,
    repository: RefreshTokensRepositoryDep,
    token_payload: RefreshTokenPayloadDep,
) -> None:
    data = TokenPayload(user_id=token_payload["user_id"])
    refresh_token = create_refresh_token(data, settings)
    rotated = repository.rotate(
        old_jti=token_payload["jti"],
        new_jti=refresh_token.jti,
        user_id=token_payload["user_id"],
        expires_at=refresh_token.expires_at,
    )

    if not rotated:
        clear_auth_cookies(response=response, settings=settings)
        raise HTTPException(status_code=401, detail="Invalid token")

    set_auth_cookies(
        response=response,
        data=data,
        settings=settings,
        refresh_token=refresh_token.token,
    )


@router.post("/logout", summary="Logout")
async def logout(
    settings: SettingsDep,
    response: Response,
    repository: RefreshTokensRepositoryDep,
    refresh_token: LogoutRefreshTokenDep,
) -> None:
    if refresh_token is not None:
        try:
            payload = decode_refresh_token(refresh_token, settings)
        except HTTPException:
            payload = None

        if payload is not None:
            repository.delete(payload["jti"])

    clear_auth_cookies(response=response, settings=settings)
