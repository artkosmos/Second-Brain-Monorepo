.PHONY: sync local supabase migrate-local migrate-supabase revision-local revision-supabase test lint format typecheck hooks

sync:
	uv sync

local:
	uv run python main.py

supabase:
	DB_TARGET=supabase uv run python main.py

migrate-local:
	uv run alembic upgrade head

migrate-supabase:
	DB_TARGET=supabase uv run alembic upgrade head

revision-local:
	uv run alembic revision --autogenerate -m "$(m)"

revision-supabase:
	DB_TARGET=supabase uv run alembic revision --autogenerate -m "$(m)"

test:
	uv run pytest -v

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

typecheck:
	uv run mypy

hooks:
	uv run pre-commit install
	uv run pre-commit run --all-files