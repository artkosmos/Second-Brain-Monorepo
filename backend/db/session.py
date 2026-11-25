from collections.abc import Iterator

from sqlalchemy.orm import Session, sessionmaker

from db.base import engine

local_session = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    with local_session() as session:
        yield session
