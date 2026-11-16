from datetime import datetime
from typing import Annotated

from models import NoteDraft, NotePatchDraft, NoteUpdateDraft
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

# Non-empty tag string after trimming whitespace.
Tag = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class NoteCreate(BaseModel):
    """Request body for creating a note (POST /notes)."""

    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    # tags: list[Tag] = Field(default_factory=list)

    def to_draft(self) -> NoteDraft:
        return NoteDraft(title=self.title, content=self.content)


class NoteResponse(BaseModel):
    """API response contract for a note (what the client receives)."""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Field(gt=0)]
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    created_at: datetime
    updated_at: datetime


class NoteUpdate(NoteCreate):
    """Request body for full note replacement (PUT /notes/{id}).

    Same required fields as NoteCreate; id comes from the path.
    """

    def to_draft(self, note_id: int) -> NoteUpdateDraft:
        return NoteUpdateDraft(id=note_id, title=self.title, content=self.content)


class NotePatch(BaseModel):
    """Request body for partial note update (PATCH /notes/{id}).

    Only sent fields are applied. At least one field is required.
    """

    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None = None
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] | None = None
    # tags: list[Tag] | None = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        """Reject an empty patch body (no fields were set)."""

        if not bool(self.model_dump(exclude_unset=True)):
            raise ValueError("At least one field is required")

        return self

    def to_patch_draft(self) -> NotePatchDraft:
        data = self.model_dump(exclude_unset=True)

        return NotePatchDraft(
            title=data.get("title"),
            content=data.get("content"),
        )
