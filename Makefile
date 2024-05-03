lint:
	poetry run black .
	poetry run ruff check .
	poetry run mypy .
	poetry run isort .

check-migrations:
	run dj makemigrations --check

test:
	poetry run pytest

ci: lint check-migrations test
