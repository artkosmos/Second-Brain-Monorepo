class NotesError(Exception):
    """Base application error."""


class NotFoundError(NotesError):
    """Entity was not found (HTTP 404)."""


class StorageError(NotesError):
    """Read or write failed (HTTP 500)."""
