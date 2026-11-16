from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt
from config import Settings
from dependencies.cookie import AccessTokenDep, RefreshTokenDep
from dependencies.settings import SettingsDep
from fastapi import HTTPException, Response

from security.types import RefreshToken, RefreshTokenPayload, TokenPayload


def decode_token(token: str, settings: SettingsDep) -> TokenPayload:
    try:
        payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        if payload.get("type") == "refresh":
            raise jwt.InvalidTokenError

        return TokenPayload(user_id=int(payload["sub"]))
    except jwt.InvalidTokenError as error:
        raise HTTPException(status_code=401, detail="Invalid token") from error


def get_token_payload_from_cookie(settings: SettingsDep, token: AccessTokenDep) -> TokenPayload:
    return decode_token(token, settings)


def decode_refresh_token(token: str, settings: Settings) -> RefreshTokenPayload:
    try:
        payload = jwt.decode(token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        if payload.get("type") != "refresh":
            raise jwt.InvalidTokenError

        return RefreshTokenPayload(user_id=int(payload["sub"]), jti=UUID(payload["jti"]))
    except (jwt.InvalidTokenError, KeyError, ValueError) as error:
        raise HTTPException(status_code=401, detail="Invalid token") from error


def get_refresh_token_payload_from_cookie(
    settings: SettingsDep, token: RefreshTokenDep
) -> RefreshTokenPayload:
    return decode_refresh_token(token, settings)


def create_access_token(data: TokenPayload, settings: Settings) -> str:
    created_at = datetime.now(UTC)
    expires_delta = timedelta(seconds=settings.jwt_access_expiration_time)
    expire = created_at + expires_delta
    payload: dict[str, str | int | datetime] = {
        "sub": str(data["user_id"]),
        "exp": expire,
        "iat": created_at,
    }

    return jwt.encode(payload=payload, key=settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_refresh_token(data: TokenPayload, settings: Settings) -> RefreshToken:
    created_at = datetime.now(UTC)
    expires_delta = timedelta(seconds=settings.jwt_refresh_expiration_time)
    expire = created_at + expires_delta
    jti = uuid4()
    payload: dict[str, str | int | datetime] = {
        "sub": str(data["user_id"]),
        "exp": expire,
        "iat": created_at,
        "jti": str(jti),
        "type": "refresh",
    }
    token = jwt.encode(payload=payload, key=settings.jwt_secret, algorithm=settings.jwt_algorithm)

    return RefreshToken(token=token, jti=jti, expires_at=expire)


def set_auth_cookies(
    response: Response,
    data: TokenPayload,
    settings: Settings,
    refresh_token: str,
) -> None:
    response.set_cookie(
        key=settings.jwt_cookie_name,
        value=create_access_token(data=data, settings=settings),
        httponly=True,
        secure=settings.jwt_cookie_secure,
        samesite="lax",
        max_age=settings.jwt_access_expiration_time,
    )
    response.set_cookie(
        key=settings.jwt_refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=settings.jwt_cookie_secure,
        samesite="lax",
        max_age=settings.jwt_refresh_expiration_time,
    )


def clear_auth_cookies(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=settings.jwt_cookie_name,
        path="/",
        secure=settings.jwt_cookie_secure,
        httponly=True,
        samesite="lax",
    )
    response.delete_cookie(
        key=settings.jwt_refresh_cookie_name,
        path="/",
        secure=settings.jwt_cookie_secure,
        httponly=True,
        samesite="lax",
    )
