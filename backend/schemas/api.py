from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class AppInfoResponse(BaseModel):
    app_name: str
    environment: str
