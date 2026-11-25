from config import Settings
from repositories.refresh_tokens import RefreshTokensRepository
from security.token import create_refresh_token
from security.types import TokenPayload


def add_refresh_token(
    settings: Settings,
    repository: RefreshTokensRepository,
    user_id: int,
) -> str:
    refresh_token = create_refresh_token(TokenPayload(user_id=user_id), settings)
    repository.add(refresh_token.jti, user_id, refresh_token.expires_at)

    return refresh_token.token
