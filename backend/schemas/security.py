from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class BaseAuthRequest(BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8)


class LoginRequest(BaseAuthRequest):
    pass


class RegistrationRequest(BaseAuthRequest):
    pass


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(gt=0)]
    email: EmailStr
    created_at: datetime
