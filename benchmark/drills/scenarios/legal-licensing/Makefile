PY ?= python3
export PYTHONPATH := .:vendor:third_party

.PHONY: test run scan lint

test:
	$(PY) -m pytest

run:
	$(PY) -m app.server

scan:
	$(PY) scripts/licence_scan.py --check

lint:
	$(PY) -m compileall -q app scripts
