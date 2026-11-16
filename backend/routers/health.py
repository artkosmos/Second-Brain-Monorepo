import asyncio

from dependencies.settings import SettingsDep
from fastapi import APIRouter
from schemas.api import AppInfoResponse, HealthResponse

router = APIRouter()


@router.get("/health", tags=["Health 🫩"], summary="Check that the server is up")
async def health() -> HealthResponse:
    await asyncio.sleep(0.1)

    return HealthResponse(status="ok")


@router.get("/info", tags=["Info ⚙️"], summary="App name and environment")
async def info(settings: SettingsDep) -> AppInfoResponse:
    return AppInfoResponse(
        app_name=settings.app_name,
        environment=settings.environment,
    )
