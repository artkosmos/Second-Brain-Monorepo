from typing import Annotated

from fastapi import Depends
from security.token import (
    get_refresh_token_payload_from_cookie,
    get_token_payload_from_cookie,
)
from security.types import RefreshTokenPayload, TokenPayload

type TokenPayloadDep = Annotated[TokenPayload, Depends(get_token_payload_from_cookie)]
type RefreshTokenPayloadDep = Annotated[
    RefreshTokenPayload, Depends(get_refresh_token_payload_from_cookie)
]
