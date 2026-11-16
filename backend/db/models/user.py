from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.types import created_at_datetime, int_pk


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at_datetime]
