test-coverage:
	poetry run coverage report
lint:
	poetry run flake8 api
test:
	poetry run pytest
