from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.types import created_at_datetime, int_pk


class RefreshTokensORM(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int_pk]
    jti: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[created_at_datetime]
