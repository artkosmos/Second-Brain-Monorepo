from dataclasses import asdict, dataclass

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_, select

from db.models import NotesORM
from dependencies.session import SessionDep
from exceptions.not_found_error import raise_not_found_note_error
from exceptions.storage_error import catch_storage_error
from models import NoteDraft, NotePatchDraft, NoteUpdateDraft


@dataclass
class NotesRepository:
    session: Session

    def get_notes(self, user_id: int) -> list[NotesORM]:
        with catch_storage_error():
            stmt = select(NotesORM).where(NotesORM.owner_id == user_id)

            return list(self.session.scalars(stmt))

    def get_note_by_id(self, id: int, user_id: int) -> NotesORM:
        with catch_storage_error():
            note = self.session.get(NotesORM, id)

            if note is None or note.owner_id != user_id:
                raise_not_found_note_error(id)

            return note

    def add_note(self, user_id: int, draft: NoteDraft) -> NotesORM:
        with catch_storage_error():
            note = NotesORM(title=draft.title, content=draft.content, owner_id=user_id)
            self.session.add(note)
            self.session.commit()

            return note

    def update_note(self, user_id: int, draft: NoteUpdateDraft) -> NotesORM:
        with catch_storage_error():
            note = self.session.get(NotesORM, draft.id)

            if note is None or note.owner_id != user_id:
                raise_not_found_note_error(draft.id)

            note.title = draft.title
            note.content = draft.content
            self.session.commit()

            return note

    def patch_update_note(
        self, user_id: int, id: int, draft_fields: NotePatchDraft
    ) -> NotesORM:
        with catch_storage_error():
            note = self.session.get(NotesORM, id)

            if note is None or note.owner_id != user_id:
                raise_not_found_note_error(id)

            for key, value in asdict(draft_fields).items():
                if value is not None and hasattr(note, key):
                    setattr(note, key, value)

            self.session.commit()

            return note

    def delete_note(self, user_id: int, id: int) -> None:
        with catch_storage_error():
            note = self.session.get(NotesORM, id)

            if note is None or note.owner_id != user_id:
                raise_not_found_note_error(id)

            self.session.delete(note)
            self.session.commit()

    def find_notes_by_query(self, user_id: int, query: str) -> list[NotesORM] | None:
        search_query = query.strip().lower()

        if not search_query:
            return None

        with catch_storage_error():
            stmt = (
                select(NotesORM)
                .select_from(NotesORM)
                .where(
                    NotesORM.owner_id == user_id,
                    or_(
                        NotesORM.title.icontains(search_query),
                        NotesORM.content.icontains(search_query),
                    ),
                )
            )
            result = self.session.scalars(stmt).all()

            return list(result)

    # SELECT FROM EXTERNAL TABLE IN DB
    # def find_notes_by_tag(self, tag: str) -> list[NotesORM] | None:
    #     prepared_query = tag.strip().lower()

    #     if not prepared_query:
    #         return None

    #     return [note for note in self._notes if note.has_tag(prepared_query)]


def get_repository(session: SessionDep) -> NotesRepository:
    return NotesRepository(session)
