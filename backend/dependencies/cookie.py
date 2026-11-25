from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyCookie

from config import get_settings

cookie_scheme = APIKeyCookie(name=get_settings().jwt_cookie_name)
refresh_cookie_scheme = APIKeyCookie(name=get_settings().jwt_refresh_cookie_name)
logout_refresh_cookie_scheme = APIKeyCookie(
    name=get_settings().jwt_refresh_cookie_name,
    auto_error=False,
)

type AccessTokenDep = Annotated[str, Depends(cookie_scheme)]
type RefreshTokenDep = Annotated[str, Depends(refresh_cookie_scheme)]
type LogoutRefreshTokenDep = Annotated[
    str | None, Depends(logout_refresh_cookie_scheme)
]
