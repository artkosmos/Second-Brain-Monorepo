from typing import Annotated

from db.models import UsersORM
from fastapi import Depends
from security.user import get_current_user

type CurrentUserDep = Annotated[UsersORM, Depends(get_current_user)]
