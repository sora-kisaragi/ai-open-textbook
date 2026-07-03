#!/usr/bin/env python3
"""Build a generated SQLite index from NDJSON collections."""
from __future__ import annotations

import json
import os
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ROOT / 'data' / 'collections'
BUILD = ROOT / 'build'
DB = BUILD / 'index.sqlite'


def iter_records():
    for path in sorted(COLLECTIONS.glob('*.ndjson')):
        collection = path.stem
        for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
            if not line.strip():
                continue
            obj = json.loads(line)
            yield collection, line_no, obj


def extract_edges(obj: dict):
    src = obj.get('id')
    if not src:
        return
    for field in ['lesson_refs', 'answer_refs', 'rubric_refs', 'source_refs']:
        for dst in obj.get(field, []) or []:
            yield src, dst, field
    for field in ['problem_id', 'entity_id']:
        dst = obj.get(field)
        if dst:
            yield src, dst, field


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    temp_fd, temp_name = tempfile.mkstemp(prefix='index.', suffix='.tmp.sqlite', dir=BUILD)
    os.close(temp_fd)
    temp_db = Path(temp_name)
    con = None

    try:
        con = sqlite3.connect(temp_db)
        cur = con.cursor()
        cur.execute('CREATE TABLE documents (id TEXT PRIMARY KEY, collection TEXT NOT NULL, schema_version TEXT, status TEXT, json_text TEXT NOT NULL, updated_at TEXT)')
        cur.execute('CREATE TABLE edges (src_id TEXT NOT NULL, dst_id TEXT NOT NULL, edge_type TEXT NOT NULL)')
        try:
            cur.execute('CREATE VIRTUAL TABLE doc_fts USING fts5(id, collection, body)')
            has_fts = True
        except sqlite3.OperationalError:
            has_fts = False

        count = 0
        edge_count = 0
        for collection, line_no, obj in iter_records():
            rec_id = obj['id']
            text = json.dumps(obj, ensure_ascii=False, sort_keys=True)
            cur.execute(
                'INSERT INTO documents (id, collection, schema_version, status, json_text, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
                (rec_id, collection, obj.get('schema_version'), obj.get('status'), text, obj.get('updated_at')),
            )
            if has_fts:
                cur.execute('INSERT INTO doc_fts (id, collection, body) VALUES (?, ?, ?)', (rec_id, collection, text))
            for src, dst, edge_type in extract_edges(obj):
                cur.execute('INSERT INTO edges (src_id, dst_id, edge_type) VALUES (?, ?, ?)', (src, dst, edge_type))
                edge_count += 1
            count += 1

        con.commit()
        con.close()
        con = None
        try:
            os.replace(temp_db, DB)
        except OSError as exc:
            print(
                f'Failed to replace {DB} with the generated SQLite index: {exc}. '
                'If this is Windows, close any application or shell session that has '
                'build/index.sqlite open and rerun the command.'
            )
            return 1
    finally:
        if con is not None:
            con.close()
        if temp_db.exists():
            temp_db.unlink()

    print(f'Built {DB} with {count} records and {edge_count} edges. FTS5={has_fts}.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
