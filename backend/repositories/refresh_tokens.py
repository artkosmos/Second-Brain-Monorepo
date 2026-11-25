from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.orm import Session

from db.models import RefreshTokensORM
from dependencies.session import SessionDep
from exceptions.storage_error import catch_storage_error


@dataclass
class RefreshTokensRepository:
    session: Session

    def rotate(
        self, old_jti: UUID, new_jti: UUID, user_id: int, expires_at: datetime
    ) -> bool:
        with catch_storage_error():
            deleted_jti = self.session.scalar(
                delete(RefreshTokensORM)
                .where(
                    RefreshTokensORM.jti == old_jti, RefreshTokensORM.user_id == user_id
                )
                .returning(RefreshTokensORM.jti)
            )

            if deleted_jti is None:
                self.session.rollback()

                return False

            self.session.add(
                RefreshTokensORM(jti=new_jti, user_id=user_id, expires_at=expires_at)
            )
            self.session.commit()

            return True

    def add(self, jti: UUID, user_id: int, expires_at: datetime) -> RefreshTokensORM:
        with catch_storage_error():
            token = RefreshTokensORM(
                jti=jti,
                user_id=user_id,
                expires_at=expires_at,
            )
            self.session.add(token)

            return token

    def consume(self, jti: UUID) -> bool:
        with catch_storage_error():
            deleted_jti = self.session.scalar(
                delete(RefreshTokensORM)
                .where(RefreshTokensORM.jti == jti)
                .returning(RefreshTokensORM.jti)
            )
            self.session.commit()

            return deleted_jti is not None

    def delete_garbage(self) -> None:
        with catch_storage_error():
            self.session.execute(
                delete(RefreshTokensORM).where(
                    RefreshTokensORM.expires_at < datetime.now(UTC)
                )
            )
            self.session.commit()

    def delete(self, jti: UUID) -> None:
        with catch_storage_error():
            self.session.execute(
                delete(RefreshTokensORM).where(RefreshTokensORM.jti == jti)
            )
            self.session.commit()


def get_repository(session: SessionDep) -> RefreshTokensRepository:
    return RefreshTokensRepository(session)
