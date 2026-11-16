# P11 — AI

> Короткие карточки. Подробное ТЗ пишется перед стартом фазы.
> **T11.1 рекомендуется брать сразу после P5** — её зависимости (T5.2, T5.5) к тому моменту готовы.

**Цель фазы:** AI поверх надёжной платформы. Стриминг, очереди, outbox, права, rate limit, feature flags и публичный API уже есть — AI-функции на них опираются. К концу фазы: суммаризация, гибридный поиск, RAG-чат с цитатами, агент с инструментами и approval, MCP-сервер для внешних клиентов, eval в CI и observability стоимости.

**Python-фокус:** async-генераторы для стриминга, structured output через Pydantic, абстракция провайдера через `Protocol`, агентный цикл руками (и затем на Pydantic AI), генерация JSON Schema из моделей, MCP Python SDK.

| ID | Задача | Слой | Размер |
| -- | ------ | ---- | ------ |
| T11.1 | [Суммаризация со стримингом](T11.1-summarize-streaming.md) | backend, frontend | M |
| T11.2 | [Embeddings, гибридный поиск, reranking](T11.2-embeddings-hybrid.md) | backend, system-design | L |
| T11.3 | [RAG-чат](T11.3-rag-chat.md) | backend, frontend | L |
| T11.4 | [Eval, guardrails, threat model](T11.4-eval.md) | backend | L |
| T11.5 | [Tool calling и агентный цикл](T11.5-tool-calling-agent.md) | backend, frontend, python | L |
| T11.6 | [MCP-сервер Second Brain](T11.6-mcp-server.md) | backend, python | L |
| T11.7 | [LLM-observability, роутинг моделей, кэш](T11.7-llm-observability.md) | backend, system-design | M |
| T11.8 | [Capstone: архитектура, демо, портфолио](T11.8-capstone.md) | docs | M |

Рекомендуемый порядок внутри фазы: T11.1 (рано) → T11.2 → T11.3 → T11.4 → T11.5 → T11.7 → T11.6 → T11.8. T11.4 стоит начинать параллельно с T11.3: eval-набор нужен уже для выбора чанкинга в T11.2.

Бывший T11.C «AI-действия над страницей» вошёл в T11.5.
