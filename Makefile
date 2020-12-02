test-coverage:
	poetry run coverage
lint:
	poetry run flake8 api
test:
	poetry run pytest
