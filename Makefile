test-coverage:
	poetry run pytest --cov-report term --cov=api --cov-report xml tests/
lint:
	poetry run flake8 api
test:
	poetry run pytest
