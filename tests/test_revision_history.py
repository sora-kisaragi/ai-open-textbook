#!/usr/bin/env python3
"""Tests for Git-aware canonical revision enforcement."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pytest

from scripts import check_revision_history


ROOT = Path(__file__).resolve().parents[1]


def run_git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        text=True,
        capture_output=True,
    )


def read_ndjson(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_ndjson(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


@pytest.fixture
def history_root(tmp_path: Path) -> Path:
    for directory in ("data", "curriculum", "lessons", "teacher_guides"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    run_git(tmp_path, "init", "-b", "main")
    run_git(tmp_path, "config", "user.email", "tests@example.invalid")
    run_git(tmp_path, "config", "user.name", "Revision Tests")
    run_git(tmp_path, "add", ".")
    run_git(tmp_path, "commit", "-m", "baseline")
    return tmp_path


def test_changed_record_requires_new_revision(history_root: Path) -> None:
    path = history_root / "data" / "collections" / "problems.ndjson"
    records = read_ndjson(path)
    records[0]["question"] += " Changed without revision."
    write_ndjson(path, records)

    errors = check_revision_history.check_repository(history_root, "HEAD")

    assert errors == ["prob.info1.variables.001.v1: canonical change requires a new revision event"]


def test_changed_record_with_revision_passes(history_root: Path) -> None:
    problem_path = history_root / "data" / "collections" / "problems.ndjson"
    problems = read_ndjson(problem_path)
    problems[0]["common_mistakes"].append("A new reviewed wording example.")
    problems[0]["updated_at"] = "2026-07-15"
    write_ndjson(problem_path, problems)

    revision_path = history_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    revisions.append(
        {
            "actor": "tests",
            "change_type": "update",
            "created_at": "2099-01-01",
            "entity_id": problems[0]["id"],
            "id": "rev.20990101.0001",
            "reason": "Test revision.",
            "schema_version": "1.0",
            "status": "draft",
            "supersedes": None,
            "type": "revision",
            "updated_at": "2099-01-01",
        }
    )
    write_ndjson(revision_path, revisions)

    assert check_revision_history.check_repository(history_root, "HEAD") == []


def test_lesson_body_change_requires_lesson_revision(history_root: Path) -> None:
    lesson = history_root / "lessons/highschool_information_i/programming/01_variables.md"
    lesson.write_text(lesson.read_text(encoding="utf-8") + "\nAdditional text.\n", encoding="utf-8")

    errors = check_revision_history.check_repository(history_root, "HEAD")

    assert errors == ["lesson.info1.programming.variables.v1: canonical change requires a new revision event"]


def test_revision_events_are_append_only(history_root: Path) -> None:
    revision_path = history_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    revisions[0]["reason"] = "Rewritten history."
    write_ndjson(revision_path, revisions)

    errors = check_revision_history.check_repository(history_root, "HEAD")

    assert errors == [f"{revisions[0]['id']}: revision history is append-only; event was modified"]


def test_direct_publish_transition_is_rejected(history_root: Path) -> None:
    problem_path = history_root / "data" / "collections" / "problems.ndjson"
    problems = read_ndjson(problem_path)
    problems[0]["status"] = "published"
    problems[0]["updated_at"] = "2026-07-15"
    write_ndjson(problem_path, problems)

    revision_path = history_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    revisions.append(
        {
            "actor": "tests",
            "change_type": "update",
            "created_at": "2099-01-01",
            "entity_id": problems[0]["id"],
            "id": "rev.20990101.0001",
            "reason": "Invalid direct publication.",
            "schema_version": "1.0",
            "status": "draft",
            "supersedes": None,
            "type": "revision",
            "updated_at": "2099-01-01",
        }
    )
    write_ndjson(revision_path, revisions)

    errors = check_revision_history.check_repository(history_root, "HEAD")

    assert errors == [
        f"{problems[0]['id']}: published requires prior approved status and a publish revision"
    ]


def test_content_change_cannot_use_review_request_revision(history_root: Path) -> None:
    answer_path = history_root / "data" / "collections" / "answers.ndjson"
    answers = read_ndjson(answer_path)
    answers[0]["explanation"] += " Changed learner-facing explanation."
    answers[0]["updated_at"] = "2026-07-15"
    write_ndjson(answer_path, answers)

    revision_path = history_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    revisions.append(
        {
            "actor": "tests",
            "change_type": "review_request",
            "created_at": "2099-01-01",
            "entity_id": answers[0]["id"],
            "id": "rev.20990101.0001",
            "reason": "Invalid event type for content change.",
            "schema_version": "1.0",
            "status": "draft",
            "supersedes": None,
            "type": "revision",
            "updated_at": "2099-01-01",
        }
    )
    write_ndjson(revision_path, revisions)

    errors = check_revision_history.check_repository(history_root, "HEAD")

    assert errors == [
        f"{answers[0]['id']}: content change requires an update, supersede, or deprecate revision"
    ]
