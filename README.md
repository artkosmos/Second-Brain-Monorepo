# Second Brain

Персональная база знаний. Сейчас это код урока 19 (заметки, JWT в HttpOnly cookie, Next.js), разложенный в монорепо. Дальше — [docs/ROADMAP.md](docs/ROADMAP.md).

Python-зависимости пока берутся из `~/Work/Python/Backend/.venv`. Свой `uv`/venv — задача T0.2.

## Локально

### База

Из корня репозитория:

```bash
docker compose -f infra/compose.yaml up -d
```

Postgres на порту `5433`, pgAdmin на `5051`. Учётка по умолчанию: `postgres` / `postgres`, база `notes_app`.

Скопируй примеры и подставь свои значения (файлы в git не попадают):

```bash
cp backend/.env.example backend/.env
cp backend/.env.supabase.example backend/.env.supabase
```

Локальный `.env` должен смотреть на Docker: `POSTGRES_HOST=localhost`, `POSTGRES_PORT=5433`, `POSTGRES_DB=notes_app`, `POSTGRES_USER=postgres`, `POSTGRES_PASSWORD=postgres`.

### Миграции и API

```bash
cd backend
npm run migrate_db_local
npm run local
```

API: http://127.0.0.1:8000/docs

Supabase: `npm run migrate_db_supabase`, затем `npm run supabase` (`DB_TARGET=supabase`, файл `.env.supabase`).

### Фронт

```bash
cd frontend
npm install
npm run dev
```

UI: http://127.0.0.1:3000

### Тесты

Тесты ходят в локальный Postgres (`notes_pytest`), не в Supabase. Compose должен быть запущен, `backend/.env` — на этот Postgres.

```bash
cd backend
../../Backend/.venv/bin/pytest -v
```
