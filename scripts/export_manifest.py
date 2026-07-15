#!/usr/bin/env python3
"""Export a simple file manifest."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRECTORIES = {'.git', '.pytest_cache', '.venv', 'build', '__pycache__', 'tmp'}
IGNORE_FILES = {'MANIFEST.json'}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def tracked_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"cannot list tracked repository files: {message}")
    return [Path(value.decode("utf-8")) for value in result.stdout.split(b"\0") if value]


def build_rows(root: Path, candidates: list[Path] | None = None) -> list[dict[str, str | int]]:
    rows = []
    relative_paths = tracked_paths(root) if candidates is None else candidates
    for rel in sorted(relative_paths, key=lambda path: path.as_posix()):
        p = root / rel
        if not p.is_file():
            continue
        if rel.name in IGNORE_FILES or any(part in IGNORE_DIRECTORIES for part in rel.parts):
            continue
        rows.append({'path': rel.as_posix(), 'sha256': digest(p), 'bytes': p.stat().st_size})
    return rows


def main() -> int:
    rows = build_rows(ROOT)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
