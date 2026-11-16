from dependencies.notes import RepositoryDep
from dependencies.user import CurrentUserDep
from fastapi import APIRouter
from schemas.note import NoteCreate, NotePatch, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["Notes 📒"])


@router.get("", summary="List all notes")
async def get_notes(
    user: CurrentUserDep,
    repository: RepositoryDep,
) -> list[NoteResponse]:
    return [NoteResponse.model_validate(note) for note in repository.get_notes(user.id)]


@router.get("/{note_id}", summary="Get one note by id")
async def get_note(
    note_id: int,
    user: CurrentUserDep,
    repository: RepositoryDep,
) -> NoteResponse:
    return NoteResponse.model_validate(repository.get_note_by_id(note_id, user.id))


@router.post("", summary="Create note", status_code=201)
async def create_note(
    payload: NoteCreate,
    user: CurrentUserDep,
    repository: RepositoryDep,
) -> NoteResponse:
    added_note = repository.add_note(user.id, payload.to_draft())

    return NoteResponse.model_validate(added_note)


@router.put("/{note_id}", summary="Update note")
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    user: CurrentUserDep,
    repository: RepositoryDep,
) -> NoteResponse:
    return NoteResponse.model_validate(
        repository.update_note(user.id, payload.to_draft(note_id))
    )


@router.patch("/{note_id}", summary="Update note partially")
async def update_note_partially(
    note_id: int,
    payload: NotePatch,
    user: CurrentUserDep,
    repository: RepositoryDep,
) -> NoteResponse:
    return NoteResponse.model_validate(
        repository.patch_update_note(user.id, note_id, payload.to_patch_draft())
    )


@router.delete("/{note_id}", summary="Delete note by id", status_code=204)
async def delete_note(
    note_id: int,
    user: CurrentUserDep,
    repository: RepositoryDep,
) -> None:
    repository.delete_note(user.id, note_id)
