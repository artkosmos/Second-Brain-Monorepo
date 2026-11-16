from typing import Annotated

from fastapi import Depends
from repositories.refresh_tokens import RefreshTokensRepository, get_repository

type RefreshTokensRepositoryDep = Annotated[RefreshTokensRepository, Depends(get_repository)]
