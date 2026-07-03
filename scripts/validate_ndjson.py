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
VERSIONED_ID_RE = re.compile(r'^[a-z0-9]+(\.[a-z0-9]+)*\.v[0-9]+$')
REVISION_ID_RE = re.compile(r'^rev\.\d{8}\.\d{4}$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

FILES = {
    'lessons.ndjson': 'lesson',
    'problems.ndjson': 'problem',
    'answers.ndjson': 'answer',
    'rubrics.ndjson': 'rubric',
    'sources.ndjson': 'source',
    'revisions.ndjson': 'revision',
}

ALLOWED_STATUS = {
    'draft',
    'machine_checked',
    'human_review_requested',
    'approved',
    'published',
    'deprecated',
    'superseded',
}

ALLOWED_CHANGE_TYPES = {
    'create',
    'update',
    'supersede',
    'deprecate',
    'review_request',
    'publish',
}

CORE_REQUIRED = ['id', 'type', 'schema_version', 'status', 'created_at', 'updated_at']

REQUIRED = {
    'lesson': ['title', 'body_ref', 'learning_objectives'],
    'problem': ['question', 'question_type', 'lesson_refs', 'answer_refs', 'rubric_refs'],
    'answer': ['problem_id', 'canonical_answer', 'answer_type', 'review_status', 'revision'],
    'rubric': ['problem_id', 'criteria'],
    'source': ['title', 'source_type', 'url'],
    'revision': ['entity_id', 'change_type', 'reason', 'actor'],
}

LIST_FIELDS = {
    'lesson': ['learning_objectives'],
    'problem': ['lesson_refs', 'answer_refs', 'rubric_refs'],
    'answer': ['rubric_refs', 'source_refs'],
    'rubric': ['criteria'],
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


def is_blank(value: object) -> bool:
    return value is None or value == ''


def require_list(errors: list[str], obj: dict, field: str) -> list:
    value = obj.get(field)
    if value is None:
        return []
    if not isinstance(value, list):
        error(errors, obj, f'{field} must be a list')
        return []
    return value


def check_reference(errors: list[str], obj: dict, field: str, ref: object, by_id: dict[str, dict]) -> None:
    if not isinstance(ref, str) or not ref:
        error(errors, obj, f'invalid reference in {field}: {ref!r}')
        return
    if ref not in by_id:
        error(errors, obj, f'broken reference in {field}: {ref}')


def check_supersession(errors: list[str], obj: dict, by_id: dict[str, dict]) -> None:
    rec_id = obj.get('id')
    supersedes = obj.get('supersedes')
    if supersedes not in (None, ''):
        if not isinstance(supersedes, str):
            error(errors, obj, 'supersedes must be a string or null')
        elif supersedes == rec_id:
            error(errors, obj, 'supersedes cannot point to the same record')
        elif supersedes not in by_id:
            error(errors, obj, f'broken supersedes reference: {supersedes}')

    if 'superseded_by' not in obj or obj.get('superseded_by') in (None, ''):
        return
    value = obj.get('superseded_by')
    refs = value if isinstance(value, list) else [value]
    if not isinstance(value, (list, str)):
        error(errors, obj, 'superseded_by must be a string, list, or null')
        return
    for ref in refs:
        if not isinstance(ref, str) or not ref:
            error(errors, obj, f'invalid superseded_by reference: {ref!r}')
        elif ref == rec_id:
            error(errors, obj, 'superseded_by cannot point to the same record')
        elif ref not in by_id:
            error(errors, obj, f'broken superseded_by reference: {ref}')


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
            for key in CORE_REQUIRED + REQUIRED.get(expected_type, []):
                if key not in obj or is_blank(obj[key]):
                    error(errors, obj, f'missing required field: {key}')
            rec_id = obj.get('id')
            if rec_id:
                id_pattern = REVISION_ID_RE if expected_type == 'revision' else VERSIONED_ID_RE
                if not id_pattern.match(rec_id):
                    error(errors, obj, f'invalid id format: {rec_id}')
                if rec_id in by_id:
                    error(errors, obj, f'duplicate id: {rec_id}')
                by_id[rec_id] = obj
            if obj.get('schema_version') != '1.0':
                error(errors, obj, f"unsupported schema_version: {obj.get('schema_version')!r}")
            if obj.get('status') and obj.get('status') not in ALLOWED_STATUS:
                error(errors, obj, f"invalid status: {obj.get('status')!r}")
            for field in ['created_at', 'updated_at']:
                value = obj.get(field)
                if value and not DATE_RE.match(str(value)):
                    error(errors, obj, f'invalid {field} date: {value!r}')
            if expected_type == 'revision':
                entity_id = obj.get('entity_id')
                if entity_id and not ID_RE.match(str(entity_id)):
                    error(errors, obj, f'invalid entity_id format: {entity_id}')
                change_type = obj.get('change_type')
                if change_type and change_type not in ALLOWED_CHANGE_TYPES:
                    error(errors, obj, f'invalid change_type: {change_type!r}')
            for field in LIST_FIELDS.get(expected_type, []):
                values = require_list(errors, obj, field)
                if field in REQUIRED.get(expected_type, []) and not values:
                    error(errors, obj, f'{field} must not be empty')

    for obj in records:
        for field in ['lesson_refs', 'answer_refs', 'rubric_refs', 'source_refs']:
            for ref in require_list(errors, obj, field):
                check_reference(errors, obj, field, ref, by_id)
        if obj.get('type') == 'answer':
            ref = obj.get('problem_id')
            if ref and ref not in by_id:
                error(errors, obj, f'broken problem_id: {ref}')
            elif ref and by_id[ref].get('type') != 'problem':
                error(errors, obj, f'problem_id does not reference a problem: {ref}')
        if obj.get('type') == 'rubric':
            ref = obj.get('problem_id')
            if ref and ref not in by_id:
                error(errors, obj, f'broken problem_id: {ref}')
            elif ref and by_id[ref].get('type') != 'problem':
                error(errors, obj, f'problem_id does not reference a problem: {ref}')
        if obj.get('type') == 'problem':
            problem_id = obj.get('id')
            for ref in require_list(errors, obj, 'answer_refs'):
                if ref in by_id and by_id[ref].get('problem_id') != problem_id:
                    error(errors, obj, f'answer_refs target points to another problem: {ref}')
            for ref in require_list(errors, obj, 'rubric_refs'):
                if ref in by_id and by_id[ref].get('problem_id') != problem_id:
                    error(errors, obj, f'rubric_refs target points to another problem: {ref}')
        if obj.get('type') == 'lesson':
            body_ref = obj.get('body_ref')
            if body_ref and not (ROOT / body_ref).exists():
                error(errors, obj, f'missing body_ref file: {body_ref}')
        check_supersession(errors, obj, by_id)

    revision_targets = {
        obj.get('entity_id')
        for obj in records
        if obj.get('type') == 'revision' and obj.get('entity_id')
    }
    for obj in records:
        if obj.get('type') == 'revision':
            continue
        rec_id = obj.get('id')
        if rec_id and rec_id not in revision_targets:
            error(errors, obj, f'missing revision record for entity_id: {rec_id}')

    if errors:
        print('Validation failed:')
        for item in errors:
            print(f'- {item}')
        return 1

    print(f'Validation passed: {len(records)} records checked.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
