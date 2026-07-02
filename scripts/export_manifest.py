#!/usr/bin/env python3
"""Export a simple file manifest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {'.git', 'build', '__pycache__'}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    rows = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if any(part in IGNORE for part in rel.parts):
            continue
        rows.append({'path': str(rel), 'sha256': digest(p), 'bytes': p.stat().st_size})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
