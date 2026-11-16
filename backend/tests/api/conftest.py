from collections.abc import Iterator

import pytest
from config import get_settings
from db.session import get_session
from fastapi.testclient import TestClient
from httpx2 import Response
from main import app
from psycopg import Connection
from schemas.note import NoteCreate, NoteResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool
from tests.db_url import postgres_url

_jwt_cookie_name = get_settings().jwt_cookie_name


@pytest.fixture
def db_session(postgresql: Connection) -> Iterator[Session]:
    info = postgresql.info
    engine = create_engine(
        postgres_url(
            user=info.user,
            password=info.password,
            host=info.host,
            port=info.port,
            dbname=info.dbname,
        ),
        poolclass=NullPool,
    )
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def api_client(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setattr(get_settings(), "jwt_cookie_secure", False)

    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    try:
        yield client
    finally:
        client.close()
        app.dependency_overrides.clear()


def register_user(client: TestClient, email: str, password: str = "secret123") -> Response:
    response = client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == 201
    assert client.cookies.get(_jwt_cookie_name)

    return response


@pytest.fixture
def auth_client(api_client: TestClient) -> TestClient:
    register_user(api_client, "user@example.com")

    return api_client


@pytest.fixture
def other_auth_client(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setattr(get_settings(), "jwt_cookie_secure", False)

    def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    try:
        register_user(client, "other@example.com")
        yield client
    finally:
        client.close()
        app.dependency_overrides.clear()


@pytest.fixture
def created_note_sample() -> NoteCreate:
    return NoteCreate(
        title="Test",
        content="Content",
    )


@pytest.fixture
def created_note(auth_client: TestClient, created_note_sample: NoteCreate) -> NoteResponse:
    response: Response = auth_client.post(url="/notes", json=created_note_sample.model_dump())
    assert response.status_code == 201

    return NoteResponse.model_validate(response.json())
