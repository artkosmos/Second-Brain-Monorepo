from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db.session import get_session

type SessionDep = Annotated[Session, Depends(get_session)]
