from typing import Annotated

from db.session import get_session
from fastapi import Depends
from sqlalchemy.orm import Session

type SessionDep = Annotated[Session, Depends(get_session)]
