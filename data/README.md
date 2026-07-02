# Data Directory

Canonical records are NDJSON files in `data/collections/`.
Each line is one JSON object.

Generated indexes are written to `build/` and should not be edited.

Run:

```bash
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py
```
