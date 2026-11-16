# Second Brain

## Предусловия

- Docker
- Node.js
- Python 3 и виртуальное окружение с зависимостями бэкенда. Перед командами API и миграций окружение должно быть активировано.

## База

Из корня репозитория:

```bash
docker compose -f infra/compose.yaml up -d
```

Postgres слушает `localhost:5433`. База, пользователь и пароль — свои, те же, что в `backend/.env`.

pgAdmin: http://127.0.0.1:5051. Почту и пароль задай сам, в репозиторий их не клади.

## Переменные окружения

Файлы не коммитятся. Скопируй примеры и подставь значения ниже.

```bash
cp backend/.env.example backend/.env
cp backend/.env.supabase.example backend/.env.supabase
```

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

`backend/.env.supabase` — те же поля, плюс хост своего проекта Supabase:

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

Из `backend`, с активированным виртуальным окружением:

```bash
cd backend
alembic upgrade head
python main.py
```

API: http://127.0.0.1:8000/docs

Supabase, из того же каталога:

```bash
DB_TARGET=supabase alembic upgrade head
DB_TARGET=supabase python main.py
```

## Фронт

```bash
cd frontend
npm install
npm run dev
```

UI: http://127.0.0.1:3000. Запросы идут на http://localhost:8000.
