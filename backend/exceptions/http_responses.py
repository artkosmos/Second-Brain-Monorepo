from typing import Literal

from pydantic import BaseModel
from schemas.errors import AppError, HTTPValidationError

type ErrorStatusCode = Literal[404, 422, 500]

ERROR_RESPONSES: dict[ErrorStatusCode, type[BaseModel]] = {
    404: AppError,
    422: HTTPValidationError,
    500: AppError,
}

ERROR_DESCRIPTIONS: dict[ErrorStatusCode, str] = {
    404: "Not found",
    422: "Validation Error",
    500: "Storage error",
}

ERROR_RESPONSES_SCHEMAS: dict[int | str, dict[str, str | type[BaseModel]]] = {
    code: {"model": schema, "description": ERROR_DESCRIPTIONS[code]}
    for code, schema in ERROR_RESPONSES.items()
}
