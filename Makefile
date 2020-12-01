test-coverage:
	pytest --cov-report term --cov=api --cov-report xml tests/
lint:
	flake8 api
test:
	pytest
