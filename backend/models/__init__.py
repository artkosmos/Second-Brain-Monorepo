from dataclasses import dataclass

# from typing import TypedDict


@dataclass(kw_only=True)
class NoteDraft:
    title: str
    content: str


@dataclass(kw_only=True)
class NoteUpdateDraft(NoteDraft):
    id: int


@dataclass(kw_only=True)
class NotePatchDraft:
    title: str | None = None
    content: str | None = None
