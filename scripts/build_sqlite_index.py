#!/usr/bin/env python3
"""Build a validated SQLite search and curriculum index."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from typing import Iterable

try:
    from scripts import validate_ndjson
except ModuleNotFoundError:  # Direct script execution places scripts/ on sys.path.
    import validate_ndjson


DEFAULT_ROOT = Path(__file__).resolve().parents[1]


def iter_records(root: Path) -> Iterable[tuple[str, dict]]:
    collections = root / "data" / "collections"
    for path in sorted(collections.glob("*.ndjson")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield path.stem, json.loads(line)
    curriculum_path = root / validate_ndjson.CURRICULUM_PATH
    yield "curriculum", json.loads(curriculum_path.read_text(encoding="utf-8"))


def extract_record_edges(record: dict) -> Iterable[tuple[str, str, str]]:
    source = record.get("id")
    if not isinstance(source, str):
        return
    for field in ("lesson_refs", "objective_refs", "answer_refs", "rubric_refs", "source_refs"):
        for target in record.get(field, []) or []:
            if isinstance(target, str):
                yield source, target, field
    for field in ("problem_id", "entity_id", "supersedes"):
        target = record.get(field)
        if isinstance(target, str):
            yield source, target, field
    superseded_by = record.get("superseded_by")
    targets = superseded_by if isinstance(superseded_by, list) else [superseded_by]
    for target in targets:
        if isinstance(target, str):
            yield source, target, "superseded_by"


def create_schema(cursor: sqlite3.Cursor) -> bool:
    cursor.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE documents (
            id TEXT PRIMARY KEY,
            collection TEXT NOT NULL,
            record_type TEXT NOT NULL,
            schema_version TEXT,
            status TEXT,
            json_text TEXT NOT NULL,
            updated_at TEXT
        );
        CREATE TABLE curriculum_lessons (
            lesson_id TEXT PRIMARY KEY,
            unit_id TEXT NOT NULL,
            order_label TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            json_text TEXT NOT NULL
        );
        CREATE TABLE objectives (
            objective_id TEXT PRIMARY KEY,
            lesson_id TEXT NOT NULL,
            display_label TEXT NOT NULL UNIQUE,
            statement TEXT NOT NULL,
            expected_evidence TEXT NOT NULL,
            FOREIGN KEY (lesson_id) REFERENCES curriculum_lessons(lesson_id)
        );
        CREATE TABLE coverage (
            objective_id TEXT PRIMARY KEY,
            coverage_status TEXT NOT NULL,
            assessment_item_count INTEGER NOT NULL,
            performance_criterion_count INTEGER NOT NULL,
            json_text TEXT NOT NULL,
            FOREIGN KEY (objective_id) REFERENCES objectives(objective_id)
        );
        CREATE TABLE edges (
            src_id TEXT NOT NULL,
            dst_id TEXT NOT NULL,
            edge_type TEXT NOT NULL,
            UNIQUE (src_id, dst_id, edge_type)
        );
        CREATE INDEX documents_collection_idx ON documents(collection);
        CREATE INDEX documents_status_idx ON documents(status);
        CREATE INDEX curriculum_lessons_unit_order_idx ON curriculum_lessons(unit_id, order_label);
        CREATE INDEX objectives_lesson_idx ON objectives(lesson_id);
        CREATE INDEX coverage_status_idx ON coverage(coverage_status);
        CREATE INDEX edges_src_idx ON edges(src_id);
        CREATE INDEX edges_dst_idx ON edges(dst_id);
        """
    )
    try:
        cursor.execute("CREATE VIRTUAL TABLE doc_fts USING fts5(id, collection, body)")
        return True
    except sqlite3.OperationalError:
        return False


def insert_edge(cursor: sqlite3.Cursor, source: object, target: object, edge_type: str) -> None:
    if isinstance(source, str) and isinstance(target, str):
        cursor.execute(
            "INSERT OR IGNORE INTO edges (src_id, dst_id, edge_type) VALUES (?, ?, ?)",
            (source, target, edge_type),
        )


def insert_curriculum_projection(cursor: sqlite3.Cursor, curriculum: dict) -> tuple[int, int, int]:
    lesson_count = 0
    objective_count = 0
    coverage_count = 0
    curriculum_id = curriculum["id"]
    for source_ref in curriculum.get("source_refs", []):
        insert_edge(cursor, curriculum_id, source_ref, "source_refs")
    for unit in curriculum["units"]:
        unit_id = unit["id"]
        for lesson in unit["lessons"]:
            lesson_id = lesson["lesson_id"]
            cursor.execute(
                "INSERT INTO curriculum_lessons VALUES (?, ?, ?, ?, ?, ?)",
                (
                    lesson_id,
                    unit_id,
                    lesson["order"],
                    lesson["title"],
                    lesson["status"],
                    json.dumps(lesson, ensure_ascii=False, sort_keys=True),
                ),
            )
            insert_edge(cursor, curriculum_id, lesson_id, "planned_lesson")
            for dependency in lesson.get("depends_on", []):
                insert_edge(cursor, lesson_id, dependency, "depends_on")
            for source_ref in lesson.get("source_refs", []):
                insert_edge(cursor, lesson_id, source_ref, "source_refs")
            coverage_by_objective = {
                entry["objective_ref"]: entry for entry in lesson["assessment_coverage"]
            }
            for objective in lesson["learning_objectives"]:
                objective_id = objective["id"]
                cursor.execute(
                    "INSERT INTO objectives VALUES (?, ?, ?, ?, ?)",
                    (
                        objective_id,
                        lesson_id,
                        objective["label"],
                        objective["statement"],
                        objective["expected_evidence"],
                    ),
                )
                insert_edge(cursor, lesson_id, objective_id, "learning_objective")
                entry = coverage_by_objective[objective_id]
                cursor.execute(
                    "INSERT INTO coverage VALUES (?, ?, ?, ?, ?)",
                    (
                        objective_id,
                        entry["status"],
                        len(entry["assessment_item_refs"]),
                        len(entry["performance_criterion_refs"]),
                        json.dumps(entry, ensure_ascii=False, sort_keys=True),
                    ),
                )
                for problem_ref in entry["assessment_item_refs"]:
                    insert_edge(cursor, objective_id, problem_ref, "assessment_item")
                for criterion_ref in entry["performance_criterion_refs"]:
                    insert_edge(cursor, objective_id, criterion_ref["rubric_ref"], "performance_criterion")
                objective_count += 1
                coverage_count += 1
            lesson_count += 1
    return lesson_count, objective_count, coverage_count


def verify_integrity(cursor: sqlite3.Cursor) -> None:
    integrity = cursor.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity != "ok":
        raise RuntimeError(f"SQLite integrity check failed: {integrity}")
    foreign_key_errors = cursor.execute("PRAGMA foreign_key_check").fetchall()
    if foreign_key_errors:
        raise RuntimeError(f"SQLite foreign key check failed: {foreign_key_errors}")
    dangling = cursor.execute(
        """
        SELECT src_id, dst_id, edge_type
        FROM edges
        WHERE dst_id NOT IN (SELECT id FROM documents)
          AND dst_id NOT IN (SELECT lesson_id FROM curriculum_lessons)
          AND dst_id NOT IN (SELECT objective_id FROM objectives)
        LIMIT 1
        """
    ).fetchone()
    if dangling:
        raise RuntimeError(f"SQLite edge target is not indexed: {dangling}")


def build(root: Path, output: Path) -> tuple[int, int, int, int, int, bool]:
    errors, _ = validate_ndjson.validate_repository(root)
    if errors:
        raise RuntimeError("source validation failed:\n" + "\n".join(f"- {item}" for item in errors))

    root = root.resolve()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_fd, temp_name = tempfile.mkstemp(prefix="index.", suffix=".tmp.sqlite", dir=output.parent)
    os.close(temp_fd)
    temp_db = Path(temp_name)
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(temp_db)
        cursor = connection.cursor()
        has_fts = create_schema(cursor)
        document_count = 0
        curriculum: dict | None = None
        for collection, record in iter_records(root):
            record_id = record["id"]
            record_text = json.dumps(record, ensure_ascii=False, sort_keys=True)
            cursor.execute(
                "INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    record_id,
                    collection,
                    record["type"],
                    record.get("schema_version"),
                    record.get("status"),
                    record_text,
                    record.get("updated_at"),
                ),
            )
            if has_fts:
                cursor.execute("INSERT INTO doc_fts VALUES (?, ?, ?)", (record_id, collection, record_text))
            for edge in extract_record_edges(record):
                insert_edge(cursor, *edge)
            if record["type"] == "curriculum":
                curriculum = record
            document_count += 1
        if curriculum is None:
            raise RuntimeError("curriculum document was not projected")
        lesson_count, objective_count, coverage_count = insert_curriculum_projection(cursor, curriculum)
        verify_integrity(cursor)
        edge_count = cursor.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        connection.commit()
        connection.close()
        connection = None
        os.replace(temp_db, output)
        return document_count, lesson_count, objective_count, coverage_count, edge_count, has_fts
    finally:
        if connection is not None:
            connection.close()
        if temp_db.exists():
            temp_db.unlink()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Repository root.")
    parser.add_argument("--output", type=Path, help="Output database path. Defaults to ROOT/build/index.sqlite.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output = args.output or root / "build" / "index.sqlite"
    try:
        documents, lessons, objectives, coverage, edges, has_fts = build(root, output)
    except (OSError, RuntimeError, sqlite3.Error, json.JSONDecodeError) as exc:
        print(f"SQLite build failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"Built {output.resolve()} with {documents} documents, {lessons} curriculum lessons, "
        f"{objectives} objectives, {coverage} coverage rows, and {edges} edges. FTS5={has_fts}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
