from typing import Annotated

from fastapi import Depends

from db.models import UsersORM
from security.user import get_current_user

type CurrentUserDep = Annotated[UsersORM, Depends(get_current_user)]
