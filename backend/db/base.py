from sqlalchemy import create_engine

from config import get_settings
from db.models import Base

engine = create_engine(get_settings().database_url, echo=True)


def create_tables() -> None:
    Base.metadata.create_all(engine)


def delete_tables() -> None:
    Base.metadata.drop_all(engine)
