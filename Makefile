test-coverage:
	pytest --cov-report term --cov=api tests/
lint:
	flake8 ./api
test:
	pytest