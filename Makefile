test-coverage:
	poetry run pytest --cov=api tests/ --cov-report xml
lint:
	poetry run flake8 api
test:
	poetry run pytest
