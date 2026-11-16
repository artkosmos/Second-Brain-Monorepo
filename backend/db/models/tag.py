from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.types import created_at_datetime, int_pk


class TagsORM(Base):
    __tablename__ = "tags"

    id: Mapped[int_pk]
    name: Mapped[str]
    created_at: Mapped[created_at_datetime]


class TagsToNoteORM(Base):
    __tablename__ = "tags_notes"

    note_id: Mapped[int] = mapped_column(
        ForeignKey("notes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )
