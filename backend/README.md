## Запуск

Из этого каталога `uv sync` создаёт `.venv` и ставит зависимости. `uv run` выполняет команду уже внутри него.

```bash
uv sync
uv run alembic upgrade head
uv run python main.py
```

Supabase: `DB_TARGET=supabase uv run alembic upgrade head`, затем `DB_TARGET=supabase uv run python main.py`. Те же команды есть в `Makefile`: `make local`, `make supabase`.

## Проверки

Конфиг в `pyproject.toml`. **ruff** проверяет ошибки и форматирует код. **mypy** в режиме strict проверяет типы; плагин `pydantic.mypy` понимает модели Pydantic.

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Режимы БД

| Режим | БД | Как |
| ----- | -- | --- |
| API → Supabase | remote + SSL | `.env.supabase` + `make supabase` |
| тесты | local Docker `:5433` | из корня: `docker compose -f infra/compose.yaml up -d`; в `backend`: `uv run pytest -v` |
| API → local | Docker `notes_app` | `.env` + `make local` |

Тесты **не** гонять в облако. Секреты только в `.env` / `.env.supabase` (gitignore).

Таблицы в `public` на Supabase видны через Data API по anon — не ходи к ним из браузера с anon.

## JWT / cookie

В `.env` и `.env.supabase` (см. `.env.example` / `.env.supabase.example`):

```
JWT_COOKIE_NAME=access_token
JWT_REFRESH_COOKIE_NAME=refresh_token
JWT_SECRET=...
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRATION_TIME=900
JWT_REFRESH_EXPIRATION_TIME=259200
JWT_COOKIE_SECURE=false
```

- `JWT_COOKIE_SECURE=false` — local HTTP и pytest; на HTTPS-проде — `true`
- Cookie: HttpOnly, SameSite=lax; токен в JSON-теле не отдаём
- Нет cookie / битый JWT → **401**; чужая заметка → **404**

## Тесты

```bash
docker compose -f infra/compose.yaml up -d

cd backend
uv run pytest -v
```

`pytest-postgresql` + `dependency_overrides` на `get_session`. `TestClient` хранит cookie jar после register/login.

## База / миграции

```bash
docker compose -f infra/compose.yaml up -d

# local
cd backend
uv run alembic upgrade head

# Supabase
DB_TARGET=supabase uv run alembic upgrade head
```

Если в `notes` уже есть строки, миграция `3a1afb64b26a` сама создаёт пользователя `legacy-notes@local` и проставляет его в `owner_id`, затем ставит `NOT NULL`. Пароль у этого пользователя нерабочий. На пустой таблице seed не создаётся.

Порт 8000, docs: http://127.0.0.1:8000/docs

### curl (cookie jar)

```bash
curl -s -c cookies.txt -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.c","password":"secret123"}'

curl -s -b cookies.txt -c cookies.txt -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"a@b.c","password":"secret123"}'

curl -s -b cookies.txt http://127.0.0.1:8000/notes
```

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/auth/register` | 201 + Set-Cookie |
| POST | `/auth/login` | 200 + Set-Cookie |
| GET | `/health` | сервер жив |
| GET | `/info` | имя и окружение |
| GET | `/notes` | свои заметки |
| GET | `/notes/{id}` | одна своя |
| POST | `/notes` | создать (201), `owner_id` с сервера |
| PUT | `/notes/{id}` | полная замена |
| PATCH | `/notes/{id}` | частичное обновление |
| DELETE | `/notes/{id}` | удалить (204) |

Ошибки: нет/битый auth → 401, невалидное тело → 422, нет id / чужой → 404, дубликат email → 409.
