from typing import Annotated

from fastapi import Depends
from repositories.notes import NotesRepository, get_repository

type RepositoryDep = Annotated[NotesRepository, Depends(get_repository)]
