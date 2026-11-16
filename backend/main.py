from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from alembic.command import check
from alembic.config import Config
from exceptions.handlers import register_exception_handlers
from exceptions.http_responses import ERROR_RESPONSES_SCHEMAS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.health import router as health_router
from routers.notes import router as notes_router
from routers.security import router as security_router
from routers.user import router as user_router

_ALEMBIC_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_app: FastAPI):
    check(Config(_ALEMBIC_DIR / "alembic.ini"))
    yield


app = FastAPI(title="Fast API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health_router, responses=ERROR_RESPONSES_SCHEMAS)
app.include_router(notes_router, responses=ERROR_RESPONSES_SCHEMAS)
app.include_router(security_router, responses=ERROR_RESPONSES_SCHEMAS)
app.include_router(user_router, responses=ERROR_RESPONSES_SCHEMAS)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
