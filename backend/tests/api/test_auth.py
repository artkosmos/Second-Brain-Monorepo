from config import get_settings
from fastapi.testclient import TestClient
from httpx2 import Response
from schemas.security import UserResponse

_jwt_cookie_name = get_settings().jwt_cookie_name
_refresh_cookie_name = get_settings().jwt_refresh_cookie_name


def test_register_sets_cookie(api_client: TestClient):
    response: Response = api_client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    assert api_client.cookies.get(_jwt_cookie_name)


def test_register_duplicate_email(auth_client: TestClient):
    response: Response = auth_client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert response.status_code == 409


def test_login_sets_cookie(api_client: TestClient):
    register: Response = api_client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "secret123"},
    )
    assert register.status_code == 201
    api_client.cookies.clear()

    response: Response = api_client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    assert api_client.cookies.get(_jwt_cookie_name)


def test_refresh_rejects_used_token(api_client: TestClient):
    api_client.post(
        "/auth/register",
        json={"email": "refresh@example.com", "password": "secret123"},
    )
    old_refresh = api_client.cookies.get(_refresh_cookie_name) or ""
    refreshed = api_client.post("/auth/refresh")
    assert refreshed.status_code == 200
    assert api_client.cookies.get(_refresh_cookie_name) != old_refresh

    api_client.cookies.set(_refresh_cookie_name, old_refresh)
    reused = api_client.post("/auth/refresh")
    assert reused.status_code == 401


def test_login_invalid_credentials(api_client: TestClient):
    api_client.post(
        "/auth/register",
        json={"email": "badlogin@example.com", "password": "secret123"},
    )
    response: Response = api_client.post(
        "/auth/login",
        json={"email": "badlogin@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_me_returns_current_user(auth_client: TestClient):
    response: Response = auth_client.get("/user/me")
    assert response.status_code == 200
    data = UserResponse.model_validate(response.json())
    assert data.email == "user@example.com"
    assert "hashed_password" not in response.json()


def test_me_without_cookie_returns_401(api_client: TestClient):
    response: Response = api_client.get("/user/me")
    assert response.status_code == 401


def test_me_invalid_token_returns_401(api_client: TestClient):
    api_client.cookies.set(_jwt_cookie_name, "not-a-token")
    response: Response = api_client.get("/user/me")
    assert response.status_code == 401


def test_me_rejects_refresh_token_as_access(api_client: TestClient):
    api_client.post(
        "/auth/register",
        json={"email": "swap@example.com", "password": "secret123"},
    )
    refresh_token = api_client.cookies.get(_refresh_cookie_name) or ""
    api_client.cookies.set(_jwt_cookie_name, refresh_token)
    response: Response = api_client.get("/user/me")
    assert response.status_code == 401


def test_notes_without_cookie_returns_401(api_client: TestClient):
    # APIKeyCookie(auto_error=True) → 401 Not authenticated
    response: Response = api_client.get("/notes")
    assert response.status_code == 401
