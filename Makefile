include ../../../make.inc

.PHONY: test
test: pytest-and-write-output

test_process_store:
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes tests/test_process_store.py

test_bq_assets:
	PYTHONDONTWRITEBYTECODE=1 poetry run pytest -v --color=yes --disable-warnings tests/test_bigquery_assets.py
