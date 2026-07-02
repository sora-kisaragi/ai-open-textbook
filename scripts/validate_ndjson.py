#!/usr/bin/env python3
"""Validate canonical NDJSON collections.

This script intentionally uses only the Python standard library.
It performs lightweight structural checks and cross-reference checks.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = ROOT / 'data' / 'collections'
ID_RE = re.compile(r'^[a-z0-9]+(\.[a-z0-9]+)*$')

FILES = {
    'lessons.ndjson': 'lesson',
    'problems.ndjson': 'problem',
    'answers.ndjson': 'answer',
    'rubrics.ndjson': 'rubric',
    'sources.ndjson': 'source',
    'revisions.ndjson': 'revision',
}

REQUIRED = {
    'lesson': ['id', 'type', 'schema_version', 'status', 'title', 'body_ref'],
    'problem': ['id', 'type', 'schema_version', 'status', 'question', 'answer_refs'],
    'answer': ['id', 'type', 'schema_version', 'status', 'problem_id', 'canonical_answer'],
    'rubric': ['id', 'type', 'schema_version', 'status', 'criteria'],
    'source': ['id', 'type', 'schema_version', 'title'],
    'revision': ['id', 'type', 'schema_version', 'entity_id', 'change_type'],
}


def read_ndjson(path: Path) -> list[dict]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'{path}:{line_no}: invalid JSON: {exc}') from exc
        obj['_file'] = path.name
        obj['_line'] = line_no
        rows.append(obj)
    return rows


def error(errors: list[str], obj: dict, message: str) -> None:
    loc = f"{obj.get('_file', '?')}:{obj.get('_line', '?')}"
    errors.append(f'{loc}: {message}')


def main() -> int:
    errors: list[str] = []
    records: list[dict] = []
    by_id: dict[str, dict] = {}

    for filename, expected_type in FILES.items():
        path = COLLECTIONS / filename
        if not path.exists():
            errors.append(f'missing collection: {filename}')
            continue
        for obj in read_ndjson(path):
            records.append(obj)
            if obj.get('type') != expected_type:
                error(errors, obj, f"expected type {expected_type!r}, got {obj.get('type')!r}")
            for key in REQUIRED.get(expected_type, []):
                if key not in obj or obj[key] in (None, ''):
                    error(errors, obj, f'missing required field: {key}')
            rec_id = obj.get('id')
            if rec_id:
                if not ID_RE.match(rec_id):
                    error(errors, obj, f'invalid id format: {rec_id}')
                if rec_id in by_id:
                    error(errors, obj, f'duplicate id: {rec_id}')
                by_id[rec_id] = obj

    for obj in records:
        for field in ['lesson_refs', 'answer_refs', 'rubric_refs', 'source_refs']:
            for ref in obj.get(field, []) or []:
                if ref not in by_id:
                    error(errors, obj, f'broken reference in {field}: {ref}')
        if obj.get('type') == 'answer':
            ref = obj.get('problem_id')
            if ref and ref not in by_id:
                error(errors, obj, f'broken problem_id: {ref}')
        if obj.get('type') == 'rubric':
            ref = obj.get('problem_id')
            if ref and ref not in by_id:
                error(errors, obj, f'broken problem_id: {ref}')
        if obj.get('type') == 'lesson':
            body_ref = obj.get('body_ref')
            if body_ref and not (ROOT / body_ref).exists():
                error(errors, obj, f'missing body_ref file: {body_ref}')

    if errors:
        print('Validation failed:')
        for item in errors:
            print(f'- {item}')
        return 1

    print(f'Validation passed: {len(records)} records checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
