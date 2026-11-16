from pydantic import BaseModel


class ValidationErrorDetail(BaseModel):
    msg: str
    loc: str


class HTTPValidationError(BaseModel):
    details: ValidationErrorDetail


class AppError(BaseModel):
    details: str
