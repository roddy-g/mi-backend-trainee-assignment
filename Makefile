test-coverage:
	poetry run coverage xml
lint:
	poetry run flake8 api
test:
	poetry run pytest
