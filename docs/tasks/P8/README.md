# P8 — Базы данных Notion и публичный API

> Короткие карточки. Подробное ТЗ пишется перед стартом фазы.

**Цель фазы:** таблицы с типизированными свойствами и разными представлениями — главная «продуктовая» фишка Notion; плюс выход наружу для интеграций — API-токены и webhooks.

**Python-фокус:** Pydantic discriminated unions, кастомные валидаторы, построение SQL через SQLAlchemy Core без конкатенации строк, `hmac` и constant-time сравнение.

| ID | Задача | Слой | Размер |
| -- | ------ | ---- | ------ |
| T8.1 | [Database-страница и свойства](T8.1-database-properties.md) | backend, frontend, python | L |
| T8.2 | [Представления table / board / calendar](T8.2-views.md) | backend, frontend | L |
| T8.3 | [Шаблоны и дублирование](T8.3-templates-duplicate.md) | backend, frontend | M |
| T8.4 | [Публичный API: токены со scope и исходящие webhooks](T8.4-api-tokens-webhooks.md) | backend, frontend, system-design | L |
| T8.C | [Challenge: формулы](T8.C-formulas.md) | challenge, python | L |
