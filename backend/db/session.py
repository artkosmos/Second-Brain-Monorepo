from sqlalchemy.orm import sessionmaker

from db.base import engine

local_session = sessionmaker(bind=engine, expire_on_commit=False)


def get_session():
    with local_session() as session:
        yield session
