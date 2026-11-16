# Урок 18 — JWT-авторизация (HttpOnly cookie)

Скелет из 16/17. Auth: register/login ставят JWT в cookie; `/notes` только для владельца.

## Режимы БД

| Режим | БД | Как |
| ----- | -- | --- |
| API → Supabase | remote + SSL | `.env.supabase` + `npm run supabase` |
| тесты | local Docker `:5433` | `docker compose up -d` + `pytest -v` |
| API → local | Docker `notes_app` | `.env` + `npm run local` |

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
# корень Backend
docker compose up -d

cd lessons/lesson_18_jwt
pytest -v
```

`pytest-postgresql` + `dependency_overrides` на `get_session`. `TestClient` хранит cookie jar после register/login.

## База / миграции

```bash
# корень Backend
docker compose up -d

# local
cd lessons/lesson_18_jwt
alembic upgrade head

# Supabase
DB_TARGET=supabase alembic upgrade head
```

Если в `notes` уже есть строки, миграция `3a1afb64b26a` сама создаёт пользователя `legacy-notes@local` и проставляет его в `owner_id`, затем ставит `NOT NULL`. Пароль у этого пользователя нерабочий. На пустой таблице seed не создаётся.

## Запуск API

```bash
cd lessons/lesson_18_jwt
npm run local          # .env
npm run supabase       # .env.supabase
```

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
