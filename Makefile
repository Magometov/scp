all: lint check-migrations test

lint:
	poetry run black .
	poetry run ruff check .
	poetry run mypy .
	poetry run isort .

check-migrations:
	poetry run dj makemigrations --check

test:
	poetry run pytest
