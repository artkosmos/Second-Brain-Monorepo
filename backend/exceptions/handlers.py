from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from exceptions.errors import NotFoundError, StorageError
from exceptions.http_responses import ERROR_RESPONSES, ErrorStatusCode


def _error_response(
    status_code: ErrorStatusCode, details: dict[str, str | dict[str, str]]
) -> JSONResponse:
    model = ERROR_RESPONSES[status_code]

    return JSONResponse(
        status_code=status_code, content=model.model_validate(details).model_dump()
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_error(_request: Request, exc: NotFoundError) -> JSONResponse:
        return _error_response(404, {"details": str(exc)})

    @app.exception_handler(StorageError)
    async def storage_error(_request: Request, exc: StorageError) -> JSONResponse:
        return _error_response(500, {"details": str(exc)})

    @app.exception_handler(RequestValidationError)
    async def validation_error(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        first_error = exc.errors()[0]
        loc = first_error["loc"]
        field = loc[-1] if len(loc) > 1 and isinstance(loc[-1], str) else ""

        return _error_response(
            422, {"details": {"msg": first_error["msg"], "loc": field}}
        )
