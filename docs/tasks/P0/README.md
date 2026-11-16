# P0 — Фундамент репозитория

**Цель фазы:** из учебной папки сделать проект, с которым можно жить годами: воспроизводимое окружение, линтеры и типы, CI на каждый PR, единый формат логов и ошибок, типобезопасный контракт фронт ↔ бэк.

**Python-фокус:** src-layout и пакеты, `pyproject.toml`, typing (`Protocol`, `TypeVar`, generics), `contextvars`, фабрика приложения.

**Итог фазы:** PR в `main` невозможно смержить с красным линтером или тестами; фронт использует сгенерированный клиент; каждый запрос имеет `request_id` в логах и в ответе.

| ID | Задача | Слой | Размер |
| -- | ------ | ---- | ------ |
| T0.1 | [Монорепо из урока 19](T0.1-monorepo.md) | infra | S |
| T0.2 | [Инструменты Python: uv, ruff, mypy, pre-commit](T0.2-python-tooling.md) | backend, python | M |
| T0.3 | [Feature-модули и фабрика приложения](T0.3-feature-modules.md) | backend, python | L |
| T0.4 | [CI на GitHub Actions](T0.4-ci.md) | infra | M |
| T0.5 | [Логи, request-id, Problem Details](T0.5-logging-errors.md) | backend, system-design | M |
| T0.6 | [Контракт OpenAPI → TypeScript + TanStack Query](T0.6-api-client.md) | frontend, backend | L |

Размер: S — вечер, M — 2–3 вечера, L — неделя.
