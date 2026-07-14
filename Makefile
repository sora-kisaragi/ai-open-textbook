.PHONY: validate sqlite site clean

validate:
	python3 scripts/validate_ndjson.py

sqlite:
	python3 scripts/build_sqlite_index.py

site:
	python3 scripts/build_static_site.py

clean:
	rm -rf build
