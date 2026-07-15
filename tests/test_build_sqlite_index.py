#!/usr/bin/env python3
"""Tests for the validated SQLite curriculum projection."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import sqlite3

import pytest

from scripts import build_sqlite_index


ROOT = Path(__file__).resolve().parents[1]


def test_sqlite_projects_curriculum_and_coverage(tmp_path: Path) -> None:
    output = tmp_path / "index.sqlite"
    counts = build_sqlite_index.build(ROOT, output)

    assert counts[:5] == (468, 32, 96, 96, 1075)
    with sqlite3.connect(output) as connection:
        assert connection.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
        assert connection.execute("SELECT COUNT(*) FROM curriculum_lessons").fetchone()[0] == 32
        assert connection.execute("SELECT COUNT(*) FROM objectives").fetchone()[0] == 96
        assert connection.execute(
            "SELECT coverage_status, COUNT(*) FROM coverage GROUP BY coverage_status ORDER BY coverage_status"
        ).fetchall() == [("complete", 42), ("not_started", 52), ("partial", 2)]
        assert connection.execute(
            "SELECT order_label FROM curriculum_lessons ORDER BY order_label LIMIT 1"
        ).fetchone()[0] == "A1"
        assert connection.execute(
            "SELECT COUNT(*) FROM edges WHERE edge_type = 'objective_refs'"
        ).fetchone()[0] == 87


def test_invalid_source_does_not_replace_existing_index(tmp_path: Path) -> None:
    for directory in ("schemas", "data", "curriculum", "lessons"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    lesson_path = tmp_path / "data" / "collections" / "lessons.ndjson"
    lessons = [
        json.loads(line)
        for line in lesson_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    lessons[0]["updated_at"] = "not-a-date"
    lesson_path.write_text(
        "".join(json.dumps(lesson, ensure_ascii=False) + "\n" for lesson in lessons),
        encoding="utf-8",
    )
    output = tmp_path / "build" / "index.sqlite"
    output.parent.mkdir()
    output.write_bytes(b"existing-index")

    with pytest.raises(RuntimeError, match="source validation failed"):
        build_sqlite_index.build(tmp_path, output)

    assert output.read_bytes() == b"existing-index"
