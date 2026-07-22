#!/usr/bin/env python3
"""Production-validator tests for canonical and deliberately invalid data."""
from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest

from scripts import validate_ndjson


ROOT = Path(__file__).resolve().parents[1]


def write_ndjson(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def read_ndjson(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


@pytest.fixture
def validation_root(tmp_path: Path) -> Path:
    for directory in ("schemas", "data", "curriculum", "lessons"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    return tmp_path


def validation_errors(root: Path) -> list[str]:
    errors, _ = validate_ndjson.validate_repository(root)
    return errors


def test_validate_current_repository() -> None:
    errors, count = validate_ndjson.validate_repository(ROOT)
    assert errors == []
    assert count == 1271


def test_invalid_calendar_date_is_rejected(validation_root: Path) -> None:
    path = validation_root / "data" / "collections" / "lessons.ndjson"
    records = read_ndjson(path)
    records[0]["created_at"] = "2026-99-99"
    write_ndjson(path, records)

    assert any("is not a 'date'" in error for error in validation_errors(validation_root))


def test_wrong_reference_type_is_rejected(validation_root: Path) -> None:
    path = validation_root / "data" / "collections" / "problems.ndjson"
    records = read_ndjson(path)
    records[0]["lesson_refs"] = ["ans.prob.info1.variables.001.v1"]
    write_ndjson(path, records)

    errors = validation_errors(validation_root)
    assert any("lesson_refs" in error and "answer" in error for error in errors)


def test_missing_revision_target_and_answer_counter_are_rejected(validation_root: Path) -> None:
    revision_path = validation_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    revisions[-1]["entity_id"] = "lesson.info1.missing.v1"
    write_ndjson(revision_path, revisions)

    answer_path = validation_root / "data" / "collections" / "answers.ndjson"
    answers = read_ndjson(answer_path)
    answers[0]["revision"] = 99
    write_ndjson(answer_path, answers)

    errors = validation_errors(validation_root)
    assert any("revision entity_id does not resolve" in error for error in errors)
    assert any("answer revision must be 3" in error for error in errors)


def test_cross_entity_revision_supersedes_is_rejected(validation_root: Path) -> None:
    revision_path = validation_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    revisions[1]["supersedes"] = revisions[0]["id"]
    write_ndjson(revision_path, revisions)

    assert any(
        "revision supersedes must reference the same entity_id" in error
        for error in validation_errors(validation_root)
    )


def test_revision_supersedes_must_point_backwards_without_cycles(validation_root: Path) -> None:
    revision_path = validation_root / "data" / "collections" / "revisions.ndjson"
    revisions = read_ndjson(revision_path)
    by_entity: dict[str, list[dict]] = {}
    for revision in revisions:
        by_entity.setdefault(revision["entity_id"], []).append(revision)
    older, newer = next(
        sorted(events, key=lambda item: (item["created_at"], item["id"]))[:2]
        for events in by_entity.values()
        if len(events) >= 2
    )
    older["supersedes"] = newer["id"]
    newer["supersedes"] = older["id"]
    write_ndjson(revision_path, revisions)

    errors = validation_errors(validation_root)
    assert any("revision supersedes must reference an older event" in error for error in errors)
    assert any("revision supersedes cycle detected" in error for error in errors)


def test_invalid_rubric_criteria_are_rejected(validation_root: Path) -> None:
    path = validation_root / "data" / "collections" / "rubrics.ndjson"
    records = read_ndjson(path)
    records[0]["criteria"] = [
        {"id": "c1", "description": "First", "points": 1},
        {"id": "c1", "description": "Duplicate", "points": -1},
    ]
    write_ndjson(path, records)

    errors = validation_errors(validation_root)
    assert any("less than the minimum" in error for error in errors)
    assert any("criterion ids must be unique" in error for error in errors)


def test_supersession_cycle_is_rejected(validation_root: Path) -> None:
    path = validation_root / "data" / "collections" / "sources.ndjson"
    records = read_ndjson(path)
    first_id = records[0]["id"]
    second_id = records[1]["id"]
    records[0]["supersedes"] = second_id
    records[0]["superseded_by"] = second_id
    records[1]["supersedes"] = first_id
    records[1]["superseded_by"] = first_id
    write_ndjson(path, records)

    assert any("supersession cycle detected" in error for error in validation_errors(validation_root))


def test_wrong_lesson_coverage_and_false_complete_are_rejected(validation_root: Path) -> None:
    curriculum_path = validation_root / "curriculum" / "highschool_information_i.curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    a1 = curriculum["units"][0]["lessons"][0]
    a1_coverage = a1["assessment_coverage"][0]
    a1_coverage["assessment_item_refs"] = [
        "prob.info1.variables.001.v1",
        "prob.info1.variables.002.v1",
    ]
    a1_coverage["status"] = "complete"

    c2 = curriculum["units"][2]["lessons"][1]
    c2_coverage = c2["assessment_coverage"][1]
    c2_coverage["assessment_item_refs"] = c2_coverage["assessment_item_refs"][:1]
    c2_coverage["status"] = "complete"
    curriculum_path.write_text(json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    errors = validation_errors(validation_root)
    assert any("does not belong to lesson.info1.society.information.media.v1" in error for error in errors)
    assert any("does not declare objective obj.info1.society.information.media.001.v1" in error for error in errors)
    assert any("complete status lacks two distinct assessment artifacts" in error for error in errors)


def test_duplicate_objective_coverage_is_rejected(validation_root: Path) -> None:
    curriculum_path = validation_root / "curriculum" / "highschool_information_i.curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    coverage = curriculum["units"][0]["lessons"][0]["assessment_coverage"]
    coverage.append(dict(coverage[0]))
    curriculum_path.write_text(
        json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    assert any(
        "coverage contains duplicate objective_ref values" in error
        for error in validation_errors(validation_root)
    )


def test_inconsistent_classroom_route_total_is_rejected(validation_root: Path) -> None:
    curriculum_path = validation_root / "curriculum" / "highschool_information_i.curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    curriculum["classroom_route"]["recommended_total_periods"] = 71
    curriculum_path.write_text(
        json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    assert any(
        "recommended classroom total must equal mandatory periods plus extensions"
        in error
        for error in validation_errors(validation_root)
    )


def test_mismatched_lesson_extension_is_rejected(validation_root: Path) -> None:
    curriculum_path = validation_root / "curriculum" / "highschool_information_i.curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    allocation = curriculum["classroom_route"]["extension_allocations"][0]
    allocation["lesson_ref"] = "lesson.info1.society.information.media.v1"
    curriculum_path.write_text(
        json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    assert any(
        "lesson extension allocations do not match instructional time ranges"
        in error
        for error in validation_errors(validation_root)
    )


def test_curriculum_identity_and_route_positions_are_stable(validation_root: Path) -> None:
    curriculum_path = validation_root / "curriculum" / "highschool_information_i.curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    first_lesson = curriculum["units"][0]["lessons"][0]
    first_lesson["lesson_id"] = "lesson.info1.society.information.changed.v1"
    first_lesson["order"] = "A8"
    first_lesson["learning_objectives"][0]["id"] = (
        "obj.info1.society.information.changed.001.v1"
    )
    curriculum_path.write_text(
        json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    errors = validation_errors(validation_root)
    assert any("explicit A1-D9 route position" in error for error in errors)
    assert any("stable 32-lesson baseline" in error for error in errors)
    assert any("stable 96-objective baseline" in error for error in errors)


def test_malformed_instructional_range_reports_errors_without_crashing(
    validation_root: Path,
) -> None:
    curriculum_path = validation_root / "curriculum" / "highschool_information_i.curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    curriculum["units"][0]["lessons"][0]["instructional_time"][
        "class_periods_50_min"
    ] = [1]
    curriculum_path.write_text(
        json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    errors = validation_errors(validation_root)
    assert any("class_periods_50_min" in error and "is too short" in error for error in errors)
    assert any("mandatory classroom total must match lesson minima" in error for error in errors)


def test_performance_criterion_requires_performance_task_problem(validation_root: Path) -> None:
    path = validation_root / "data" / "collections" / "problems.ndjson"
    records = read_ndjson(path)
    target = next(
        record
        for record in records
        if record["id"] == "prob.info1.society.inquiry.project.004.v1"
    )
    target["question_type"] = "extended_response"
    write_ndjson(path, records)

    assert any(
        "performance criterion problem prob.info1.society.inquiry.project.004.v1 must use question_type performance_task"
        in error
        for error in validation_errors(validation_root)
    )
