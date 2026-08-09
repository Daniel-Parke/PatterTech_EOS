.PHONY: install lint test run

install:
	pip install -r requirements.txt -r requirements-dev.txt

lint:
	ruff check app tests

test:
	python -m pytest -q

run:
	flask --app app.main run --debug
