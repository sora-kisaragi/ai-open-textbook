.PHONY: sync browser revision-check validate sqlite examples site site-check pdf test prose check clean

sync:
	uv sync --locked --extra dev

browser:
	uv run python -m playwright install chromium

revision-check:
	uv run python scripts/check_revision_history.py --base-ref $(BASE_REF)

validate:
	uv run python scripts/validate_ndjson.py

sqlite:
	uv run python scripts/build_sqlite_index.py

examples:
	uv run python scripts/check_examples.py

site:
	uv run python scripts/build_static_site.py

site-check: site
	uv run python scripts/verify_static_site.py

pdf: site-check
	uv run python scripts/build_pdf.py

test:
	uv run python -m pytest

prose:
	uv run python scripts/check_prose_warnings.py

check: validate sqlite examples site-check pdf test prose

clean:
	uv run python -c "from pathlib import Path; import shutil; shutil.rmtree(Path('build'), ignore_errors=True)"
