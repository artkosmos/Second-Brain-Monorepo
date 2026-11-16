from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict
from uuid import UUID


class TokenPayload(TypedDict):
    user_id: int


class RefreshTokenPayload(TypedDict):
    user_id: int
    jti: UUID


@dataclass(frozen=True)
class RefreshToken:
    token: str
    jti: UUID
    expires_at: datetime
