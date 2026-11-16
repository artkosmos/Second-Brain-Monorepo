from config import get_settings
from db.models import Base
from pytest_postgresql import factories
from sqlalchemy import create_engine

from tests.db_url import postgres_url

_settings = get_settings()


def _load_schema(**kwargs) -> None:
    engine = create_engine(
        postgres_url(
            user=kwargs["user"],
            password=kwargs["password"],
            host=kwargs["host"],
            port=kwargs["port"],
            dbname=kwargs["dbname"],
        )
    )
    Base.metadata.create_all(engine)
    engine.dispose()


postgresql_noproc = factories.postgresql_noproc(
    host=_settings.postgres_host,
    port=_settings.postgres_port,
    user=_settings.postgres_user,
    password=_settings.postgres_password,
    dbname="notes_pytest",
    load=[_load_schema],
)

postgresql = factories.postgresql("postgresql_noproc")
