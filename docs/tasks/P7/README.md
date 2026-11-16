# P7 — Realtime и совместная работа

> Короткие карточки. Подробное ТЗ пишется перед стартом фазы.

**Цель фазы:** несколько людей в одной странице видят изменения друг друга сразу, без конфликтов.

**Python-фокус:** долгоживущие соединения в asyncio, отмена задач при разрыве, `TaskGroup` для reader / writer одного сокета.

| ID | Задача | Слой | Размер |
| -- | ------ | ---- | ------ |
| T7.1 | [WebSocket-шлюз](T7.1-websocket.md) | backend, system-design | L |
| T7.2 | [Presence и live-обновления](T7.2-presence.md) | backend, frontend | M |
| T7.3 | [Комментарии и уведомления](T7.3-comments-notifications.md) | backend, frontend | L |
| T7.4 | [Совместное редактирование (CRDT)](T7.4-crdt.md) | backend, frontend, system-design | L |
| T7.C | [Challenge: два инстанса за балансировщиком](T7.C-two-instances.md) | challenge | M |
