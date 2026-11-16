# P5 — Redis, фоновые задачи, отказоустойчивость

> Короткие карточки. Подробное ТЗ пишется перед стартом фазы.

**Цель фазы:** вынести тяжёлое из запроса, научить систему переживать отказы зависимостей и не терять события.

**Python-фокус:** asyncio глубоко — `TaskGroup`, отмена и `CancelledError`, `asyncio.timeout`, `Semaphore`, очереди и backpressure, graceful shutdown воркера.

| ID | Задача | Слой | Размер |
| -- | ------ | ---- | ------ |
| T5.1 | [Redis и кэш](T5.1-redis-cache.md) | backend, system-design | M |
| T5.2 | [Rate limiting](T5.2-rate-limiting.md) | backend, frontend, system-design | M |
| T5.3 | [Очередь задач, экспорт и импорт](T5.3-task-queue-export.md) | backend, frontend | L |
| T5.4 | [Transactional outbox](T5.4-outbox.md) | backend, system-design | L |
| T5.5 | [Устойчивость к отказам](T5.5-resilience.md) | backend, system-design, python | M |
| T5.6 | [Файлы и изображения](T5.6-files.md) | backend, frontend, infra | L |
| T5.7 | [Audit log на outbox-событиях](T5.7-audit-log.md) | backend, frontend, python | M |
| T5.C | [Challenge: chaos](T5.C-chaos.md) | challenge | M |

После P5 рекомендуется взять T11.1 (суммаризация со стримингом) — её зависимости T5.2 и T5.5 уже готовы.
