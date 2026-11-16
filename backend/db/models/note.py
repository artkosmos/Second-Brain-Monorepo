from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from db.models.base import Base
from db.types import created_at_datetime, int_pk, updated_at_datetime


class NotesORM(MappedAsDataclass, Base, kw_only=True):
    __tablename__ = "notes"

    id: Mapped[int_pk] = mapped_column(init=False)
    title: Mapped[str]
    content: Mapped[str]
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    created_at: Mapped[created_at_datetime] = mapped_column(init=False)
    updated_at: Mapped[updated_at_datetime] = mapped_column(init=False)
