from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from exceptions.errors import StorageError


@contextmanager
def catch_storage_error() -> Iterator[None]:
    try:
        yield
    except SQLAlchemyError as error:
        raise StorageError("Failed to complete the database operation") from error
