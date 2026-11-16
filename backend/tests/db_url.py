from urllib.parse import quote_plus


def postgres_url(
    *,
    user: str,
    password: str | None,
    host: str,
    port: int | str,
    dbname: str,
) -> str:
    user_q = quote_plus(user)
    password_q = quote_plus(password or "")

    return f"postgresql+psycopg://{user_q}:{password_q}@{host}:{port}/{dbname}"
