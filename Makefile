.PHONY: dev migrate migration test

dev:
	uvicorn app.main:app --reload

migration:
	alembic revision --autogenerate -m "$(name)"

migrate:
	alembic upgrade head

test:
	.venv/Scripts/python.exe -m pytest tests/ -v
