from fastapi.testclient import TestClient
from httpx2 import Response
from pydantic import TypeAdapter

from schemas.note import NoteCreate, NotePatch, NoteResponse


def test_get_notes(auth_client: TestClient, created_note: NoteResponse) -> None:
    response: Response = auth_client.get(url="/notes")
    assert response.status_code == 200
    data = response.json()
    assert data != []
    TypeAdapter(list[NoteResponse]).validate_python(data)


def test_get_note(auth_client: TestClient, created_note: NoteResponse) -> None:
    response: Response = auth_client.get(url=f"/notes/{created_note.id}")
    assert response.status_code == 200
    NoteResponse.model_validate(response.json())


def test_create_note(auth_client: TestClient, created_note_sample: NoteCreate) -> None:
    response: Response = auth_client.post(
        url="/notes", json=created_note_sample.model_dump()
    )
    assert response.status_code == 201
    data = NoteResponse.model_validate(response.json())
    assert data.title == "Test"
    assert data.content == "Content"


def test_update_note(auth_client: TestClient, created_note: NoteResponse) -> None:
    new_title = "New Title"
    new_content = "New Content"
    response: Response = auth_client.put(
        url=f"/notes/{created_note.id}",
        json={"title": new_title, "content": new_content},
    )
    assert response.status_code == 200
    data = NoteResponse.model_validate(response.json())
    assert data.title == new_title
    assert data.content == new_content


def test_update_note_partially(
    auth_client: TestClient, created_note: NoteResponse
) -> None:
    new_title = "Hello World"
    patch = NotePatch(title=new_title)
    response: Response = auth_client.patch(
        url=f"/notes/{created_note.id}", json=patch.model_dump(exclude_unset=True)
    )
    assert response.status_code == 200
    validated_note = NoteResponse.model_validate(response.json())
    assert validated_note.title == new_title


def test_delete_note(auth_client: TestClient, created_note: NoteResponse) -> None:
    delete_response: Response = auth_client.delete(url=f"/notes/{created_note.id}")
    assert delete_response.status_code == 204
    get_response: Response = auth_client.get(url=f"/notes/{created_note.id}")
    assert get_response.status_code == 404


def test_update_partially_wrong_value(
    auth_client: TestClient, created_note: NoteResponse
) -> None:
    response: Response = auth_client.patch(url=f"/notes/{created_note.id}", json={})
    assert response.status_code == 422


def test_get_non_existing_note(
    auth_client: TestClient, created_note: NoteResponse
) -> None:
    response: Response = auth_client.get(url=f"/notes/{created_note.id + 1}")
    assert response.status_code == 404


def test_create_note_with_wrong_values(auth_client: TestClient) -> None:
    response: Response = auth_client.post(
        url="/notes",
        json={"title": "", "content": "", "tags": []},
    )
    assert response.status_code == 422


def test_delete_non_existing_note(
    auth_client: TestClient, created_note: NoteResponse
) -> None:
    response: Response = auth_client.delete(url=f"/notes/{created_note.id + 1}")
    assert response.status_code == 404


def test_other_user_cannot_get_note(
    auth_client: TestClient,
    other_auth_client: TestClient,
    created_note: NoteResponse,
) -> None:
    response: Response = other_auth_client.get(url=f"/notes/{created_note.id}")
    assert response.status_code == 404


def test_other_user_list_excludes_foreign_notes(
    auth_client: TestClient,
    other_auth_client: TestClient,
    created_note: NoteResponse,
) -> None:
    _ = auth_client, created_note
    response: Response = other_auth_client.get(url="/notes")
    assert response.status_code == 200
    assert response.json() == []
