.PHONY: validate sqlite clean

validate:
	python3 scripts/validate_ndjson.py

sqlite:
	python3 scripts/build_sqlite_index.py

clean:
	rm -rf build
