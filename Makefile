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

ci: lint check-migrations test

build:
	docker-compose -f docker-compose.yml up -d --build
