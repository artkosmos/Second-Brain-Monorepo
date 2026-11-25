# Second Brain

## Предусловия

- Docker
- Node.js 22 и pnpm 12. Если `pnpm` нет в `PATH`: `corepack enable && corepack prepare pnpm@12.4.1 --activate`
- Python 3. Из `backend` один раз `uv sync` (нужен бинарь `uv`; окружение появится в `backend/.venv`).

## База

Из корня репозитория:

```bash
docker compose -f infra/compose.yaml up -d
```

Postgres слушает `localhost:5433`. База, пользователь и пароль — свои, те же, что в `backend/.env`.

pgAdmin: http://127.0.0.1:5051. Почту и пароль задай сам, в репозиторий их не клади.

## Переменные окружения

Локальный `backend/.env`:

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=<database>
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>

APP_NAME=Notes API
ENVIRONMENT=development

JWT_COOKIE_NAME=access_token
JWT_REFRESH_COOKIE_NAME=refresh_token
JWT_SECRET=<secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRATION_TIME=900
JWT_REFRESH_EXPIRATION_TIME=259200
JWT_COOKIE_SECURE=false
```

Для локального HTTP оставь `JWT_COOKIE_SECURE=false`.

`backend/.env.supabase.example` — шаблон окружения для доступа к удалённой базе на Supabase. Поля те же, что у локального `.env`, плюс `POSTGRES_SSLMODE=require` и хост проекта:

```bash
POSTGRES_HOST=<supabase-host>
POSTGRES_PORT=5432
POSTGRES_DB=<database>
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_SSLMODE=require

APP_NAME=Notes API
ENVIRONMENT=dev

JWT_COOKIE_NAME=access_token
JWT_REFRESH_COOKIE_NAME=refresh_token
JWT_SECRET=<secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRATION_TIME=900
JWT_REFRESH_EXPIRATION_TIME=259200
JWT_COOKIE_SECURE=false
```

## API

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run python main.py
```

API: http://127.0.0.1:8000/docs

Те же команды есть в `backend/Makefile`: `make migrate-local`, `make local`, `make migrate-supabase`, `make supabase`.

Supabase:

```bash
cd backend
DB_TARGET=supabase uv run alembic upgrade head
DB_TARGET=supabase uv run python main.py
```

## Фронт

```bash
cd frontend
pnpm install
pnpm dev
```

UI: http://127.0.0.1:3000. Запросы идут на http://localhost:8000.