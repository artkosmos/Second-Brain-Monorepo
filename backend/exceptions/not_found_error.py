from typing import NoReturn

from exceptions.errors import NotFoundError


def raise_not_found_note_error(note_id: int) -> NoReturn:
    raise NotFoundError(f"Note with id {note_id} was not found")
