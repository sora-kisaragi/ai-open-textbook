#!/usr/bin/env python3
"""Validate canonical NDJSON records and the Information I curriculum plan."""
from __future__ import annotations

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, FormatChecker


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
COLLECTION_FILES = {
    "lessons.ndjson": ("lesson", "lesson.schema.json"),
    "problems.ndjson": ("problem", "problem.schema.json"),
    "answers.ndjson": ("answer", "answer.schema.json"),
    "rubrics.ndjson": ("rubric", "rubric.schema.json"),
    "sources.ndjson": ("source", "source.schema.json"),
    "revisions.ndjson": ("revision", "revision.schema.json"),
}
CURRICULUM_PATH = Path("curriculum/highschool_information_i.curriculum.json")
CURRICULUM_SCHEMA = "curriculum.schema.json"
VERSION_RE = re.compile(r"^(?P<family>.+)\.v(?P<version>[1-9][0-9]*)$")
REVISION_DATE_RE = re.compile(r"^rev\.(?P<date>[0-9]{8})\.[0-9]{4}$")
LESSON_ID_DIGEST = "3e70077afec6375a2fd09ac48ac74ababf69a1bde2cdae916a9145daff5805f5"
OBJECTIVE_ID_DIGEST = "c516448693d76e035d8720de968f5dd5eff10a4711cf5d1703539b9479589c47"
EXPECTED_UNIT_PERIODS = {
    "mext.info1.1": 9,
    "mext.info1.2": 12,
    "mext.info1.3": 21,
    "mext.info1.4": 23,
}
EXPECTED_UNIT_ORDERS = {
    "mext.info1.1": [f"A{index}" for index in range(1, 8)],
    "mext.info1.2": [f"B{index}" for index in range(1, 8)],
    "mext.info1.3": [f"C{index}" for index in range(1, 10)],
    "mext.info1.4": [f"D{index}" for index in range(1, 10)],
}
EXPECTED_EXTENSION_LESSONS = {
    "lesson.info1.society.inquiry.project.v1",
    "lesson.info1.design.project.v1",
    "lesson.info1.programming.project.v1",
    "lesson.info1.data.investigation.project.v1",
}


class ValidationFailure(RuntimeError):
    """Raised when repository data cannot be loaded for validation."""


def id_digest(ids: Iterable[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationFailure(f"{path}: top-level value must be an object")
    value["_file"] = path.as_posix()
    value["_line"] = 1
    return value


def read_ndjson(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValidationFailure(f"{path}: {exc}") from exc
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationFailure(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise ValidationFailure(f"{path}:{line_no}: record must be an object")
        value["_file"] = path.as_posix()
        value["_line"] = line_no
        rows.append(value)
    return rows


def public_value(record: dict) -> dict:
    return {key: value for key, value in record.items() if not key.startswith("_")}


def location(record: dict) -> str:
    return f"{record.get('_file', '?')}:{record.get('_line', '?')}"


def add_error(errors: list[str], record: dict, message: str) -> None:
    errors.append(f"{location(record)}: {message}")


def json_path(parts: Iterable[object]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def validate_schema(errors: list[str], record: dict, schema: dict) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for failure in sorted(validator.iter_errors(public_value(record)), key=lambda item: list(item.absolute_path)):
        add_error(errors, record, f"schema {json_path(failure.absolute_path)}: {failure.message}")


def load_schema(root: Path, filename: str) -> dict:
    path = root / "schemas" / filename
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"{path}: invalid schema: {exc}") from exc
    Draft202012Validator.check_schema(value)
    return value


def references(value: object) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def check_reference(
    errors: list[str], record: dict, field: str, ref: object, expected_type: str, by_id: dict[str, dict]
) -> dict | None:
    if not isinstance(ref, str) or not ref:
        add_error(errors, record, f"invalid reference in {field}: {ref!r}")
        return None
    target = by_id.get(ref)
    if target is None:
        add_error(errors, record, f"broken reference in {field}: {ref}")
        return None
    if target.get("type") != expected_type:
        add_error(errors, record, f"{field} must reference {expected_type}, got {target.get('type')}: {ref}")
        return None
    return target


def check_typed_record_graph(errors: list[str], records: list[dict], by_id: dict[str, dict]) -> None:
    list_reference_types = {
        "lesson_refs": "lesson",
        "objective_refs": "objective",
        "answer_refs": "answer",
        "rubric_refs": "rubric",
        "source_refs": "source",
    }
    for record in records:
        for field, expected_type in list_reference_types.items():
            for ref in record.get(field, []) if isinstance(record.get(field), list) else []:
                check_reference(errors, record, field, ref, expected_type, by_id)

        record_type = record.get("type")
        if record_type in {"answer", "rubric"}:
            problem = check_reference(errors, record, "problem_id", record.get("problem_id"), "problem", by_id)
            if problem is not None:
                backref = "answer_refs" if record_type == "answer" else "rubric_refs"
                if record.get("id") not in problem.get(backref, []):
                    add_error(errors, record, f"problem {problem.get('id')} does not link back through {backref}")
        if record_type == "answer":
            for rubric_ref in record.get("rubric_refs", []) or []:
                rubric = by_id.get(rubric_ref)
                if rubric and rubric.get("problem_id") != record.get("problem_id"):
                    add_error(errors, record, f"rubric_refs target belongs to another problem: {rubric_ref}")
        if record_type == "rubric":
            criteria = record.get("criteria", [])
            criterion_ids = [item.get("id") for item in criteria if isinstance(item, dict)]
            if len(criterion_ids) != len(set(criterion_ids)):
                add_error(errors, record, "rubric criterion ids must be unique")


def check_repository_paths(errors: list[str], root: Path, records: list[dict]) -> None:
    root_resolved = root.resolve()
    for record in records:
        if record.get("type") != "lesson" or not isinstance(record.get("body_ref"), str):
            continue
        body = (root / record["body_ref"]).resolve()
        if not body.is_relative_to(root_resolved):
            add_error(errors, record, f"body_ref escapes repository root: {record['body_ref']}")
        elif not body.is_file():
            add_error(errors, record, f"missing body_ref file: {record['body_ref']}")


def version_parts(record_id: str) -> tuple[str, int] | None:
    match = VERSION_RE.fullmatch(record_id)
    if not match:
        return None
    return match.group("family"), int(match.group("version"))


def check_supersession(errors: list[str], records: list[dict], by_id: dict[str, dict]) -> None:
    graph: dict[str, str] = {}
    for record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str) or record.get("type") == "revision":
            continue
        supersedes = record.get("supersedes")
        if isinstance(supersedes, str):
            target = by_id.get(supersedes)
            if target is None:
                add_error(errors, record, f"broken supersedes reference: {supersedes}")
                continue
            if target.get("type") != record.get("type"):
                add_error(errors, record, f"supersedes target must have type {record.get('type')}: {supersedes}")
            current_version = version_parts(record_id)
            target_version = version_parts(supersedes)
            if current_version and target_version:
                if current_version[0] != target_version[0] or current_version[1] <= target_version[1]:
                    add_error(errors, record, f"supersedes must reference an older version in the same id family: {supersedes}")
            if record_id not in references(target.get("superseded_by")):
                add_error(errors, record, f"supersedes target does not link back through superseded_by: {supersedes}")
            graph[record_id] = supersedes
        for successor in references(record.get("superseded_by")):
            target = by_id.get(successor)
            if target is None:
                add_error(errors, record, f"broken superseded_by reference: {successor}")
            elif target.get("supersedes") != record_id:
                add_error(errors, record, f"superseded_by target does not link back through supersedes: {successor}")

    for start in graph:
        seen: set[str] = set()
        current = start
        while current in graph:
            if current in seen:
                add_error(errors, by_id[start], f"supersession cycle detected at {current}")
                break
            seen.add(current)
            current = graph[current]


def check_revisions(errors: list[str], records: list[dict], by_id: dict[str, dict]) -> None:
    revisions = [record for record in records if record.get("type") == "revision"]
    events: dict[str, list[dict]] = defaultdict(list)
    revision_by_id = {record.get("id"): record for record in revisions}
    revision_graph: dict[str, str] = {}
    for revision in revisions:
        entity_id = revision.get("entity_id")
        if not isinstance(entity_id, str) or entity_id not in by_id:
            add_error(errors, revision, f"revision entity_id does not resolve: {entity_id}")
        else:
            events[entity_id].append(revision)
        match = REVISION_DATE_RE.fullmatch(str(revision.get("id", "")))
        created_at = str(revision.get("created_at", ""))
        if match and match.group("date") != created_at.replace("-", ""):
            add_error(errors, revision, "revision id date must match created_at")
        supersedes = revision.get("supersedes")
        if isinstance(supersedes, str):
            target = revision_by_id.get(supersedes)
            if target is None:
                add_error(errors, revision, f"revision supersedes does not resolve: {supersedes}")
                continue
            if target.get("entity_id") != entity_id:
                add_error(errors, revision, "revision supersedes must reference the same entity_id")
            current_key = (str(revision.get("created_at")), str(revision.get("id")))
            target_key = (str(target.get("created_at")), str(target.get("id")))
            if target_key >= current_key:
                add_error(errors, revision, "revision supersedes must reference an older event")
            revision_graph[str(revision.get("id"))] = supersedes

    for start in revision_graph:
        seen: set[str] = set()
        current = start
        while current in revision_graph:
            if current in seen:
                add_error(errors, revision_by_id[start], f"revision supersedes cycle detected at {current}")
                break
            seen.add(current)
            current = revision_graph[current]

    entities = [record for record in by_id.values() if record.get("type") not in {"revision", "objective"}]
    for entity in entities:
        entity_id = str(entity.get("id"))
        entity_events = sorted(events.get(entity_id, []), key=lambda item: (str(item.get("created_at")), str(item.get("id"))))
        if not entity_events:
            add_error(errors, entity, f"missing revision record for entity_id: {entity_id}")
            continue
        create_events = [event for event in entity_events if event.get("change_type") == "create"]
        if len(create_events) != 1:
            add_error(errors, entity, f"expected exactly one create revision event, found {len(create_events)}")
        elif create_events[0].get("created_at") != entity.get("created_at"):
            add_error(errors, entity, "create revision date must match entity created_at")
        if entity_events[-1].get("created_at") != entity.get("updated_at"):
            add_error(errors, entity, "latest revision date must match entity updated_at")
        if entity.get("type") == "answer" and isinstance(entity.get("revision"), int):
            content_changes = sum(
                event.get("change_type") in {"update", "supersede", "deprecate"}
                for event in entity_events
            )
            expected_revision = 1 + content_changes
            if entity["revision"] != expected_revision:
                add_error(
                    errors,
                    entity,
                    f"answer revision must be {expected_revision} from content-changing revision events, got {entity['revision']}",
                )


def check_curriculum(
    errors: list[str], root: Path, curriculum: dict, records: list[dict], by_id: dict[str, dict]
) -> None:
    lessons = [lesson for unit in curriculum.get("units", []) for lesson in unit.get("lessons", [])]
    lesson_by_id: dict[str, dict] = {}
    objective_by_id: dict[str, tuple[dict, dict]] = {}
    objective_records: list[dict] = []

    unit_areas = [unit.get("area") for unit in curriculum.get("units", [])]
    if unit_areas != ["mext.info1.1", "mext.info1.2", "mext.info1.3", "mext.info1.4"]:
        add_error(errors, curriculum, f"unit source areas must be ordered mext.info1.1-4, got {unit_areas}")
    if len(lessons) != 32:
        add_error(errors, curriculum, f"expected 32 curriculum lessons, got {len(lessons)}")

    orders: list[str] = []
    for lesson in lessons:
        lesson_id = lesson.get("lesson_id")
        order = lesson.get("order")
        if isinstance(order, str):
            orders.append(order)
        if not isinstance(lesson_id, str):
            continue
        if lesson_id in lesson_by_id:
            add_error(errors, curriculum, f"duplicate curriculum lesson id: {lesson_id}")
        lesson_by_id[lesson_id] = lesson
        for objective in lesson.get("learning_objectives", []):
            objective_id = objective.get("id") if isinstance(objective, dict) else None
            if not isinstance(objective_id, str):
                continue
            if objective_id in objective_by_id:
                add_error(errors, curriculum, f"duplicate objective id: {objective_id}")
                continue
            objective_by_id[objective_id] = (lesson, objective)
            objective_record = deepcopy(objective)
            objective_record.update({"type": "objective", "lesson_id": lesson_id, "_file": curriculum["_file"], "_line": 1})
            objective_records.append(objective_record)
    if len(orders) != len(set(orders)):
        add_error(errors, curriculum, "curriculum lesson order labels must be unique")
    unit_orders = {
        unit.get("area"): [lesson.get("order") for lesson in unit.get("lessons", [])]
        for unit in curriculum.get("units", [])
    }
    if unit_orders != EXPECTED_UNIT_ORDERS:
        add_error(errors, curriculum, "every curriculum lesson must retain its explicit A1-D9 route position")
    if id_digest(lesson_by_id) != LESSON_ID_DIGEST:
        add_error(errors, curriculum, "curriculum lesson IDs differ from the stable 32-lesson baseline")
    if len(objective_by_id) != 96 or id_digest(objective_by_id) != OBJECTIVE_ID_DIGEST:
        add_error(errors, curriculum, "curriculum objective IDs differ from the stable 96-objective baseline")

    by_id.update({record["id"]: record for record in objective_records})
    for source_ref in curriculum.get("source_refs", []):
        check_reference(errors, curriculum, "source_refs", source_ref, "source", by_id)

    graph: dict[str, list[str]] = {}
    for lesson in lessons:
        lesson_id = lesson.get("lesson_id")
        if not isinstance(lesson_id, str):
            continue
        dependencies = lesson.get("depends_on", [])
        graph[lesson_id] = dependencies if isinstance(dependencies, list) else []
        for dependency in graph[lesson_id]:
            if dependency not in lesson_by_id:
                add_error(errors, curriculum, f"broken curriculum dependency for {lesson_id}: {dependency}")
            elif dependency == lesson_id:
                add_error(errors, curriculum, f"curriculum lesson cannot depend on itself: {lesson_id}")
        for source_ref in lesson.get("source_refs", []):
            check_reference(errors, curriculum, f"{lesson.get('order')}.source_refs", source_ref, "source", by_id)

        objectives = {objective.get("id") for objective in lesson.get("learning_objectives", []) if isinstance(objective, dict)}
        coverage = lesson.get("assessment_coverage", [])
        coverage_refs = [entry.get("objective_ref") for entry in coverage if isinstance(entry, dict)]
        coverage_objectives = set(coverage_refs)
        if len(coverage_refs) != len(coverage_objectives):
            add_error(errors, curriculum, f"{lesson.get('order')} coverage contains duplicate objective_ref values")
        if coverage_objectives != objectives:
            add_error(errors, curriculum, f"{lesson.get('order')} coverage must map every objective exactly once")
        for entry in coverage:
            if isinstance(entry, dict):
                check_coverage(errors, curriculum, lesson, entry, by_id)

        body_ref = lesson.get("existing_body_ref")
        canonical = by_id.get(lesson_id)
        if body_ref:
            if canonical is None or canonical.get("type") != "lesson":
                add_error(errors, curriculum, f"existing_body_ref lesson is missing from lessons.ndjson: {lesson_id}")
            elif canonical.get("body_ref") != body_ref:
                add_error(errors, curriculum, f"existing_body_ref differs from canonical lesson body_ref: {lesson_id}")
            body_path = (root / str(body_ref)).resolve()
            if not body_path.is_file():
                add_error(errors, curriculum, f"missing existing_body_ref: {body_ref}")

        time = lesson.get("instructional_time", {})
        for field in ("class_periods_50_min", "self_study_minutes"):
            values = time.get(field, []) if isinstance(time, dict) else []
            if isinstance(values, list) and len(values) == 2 and values[0] > values[1]:
                add_error(errors, curriculum, f"{lesson.get('order')} {field} minimum exceeds maximum")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(lesson_id: str) -> None:
        if lesson_id in visited:
            return
        if lesson_id in visiting:
            add_error(errors, curriculum, f"curriculum dependency cycle at {lesson_id}")
            return
        visiting.add(lesson_id)
        for dependency in graph.get(lesson_id, []):
            if dependency in graph:
                visit(dependency)
        visiting.remove(lesson_id)
        visited.add(lesson_id)

    for lesson_id in graph:
        visit(lesson_id)

    period_totals = tuple(
        sum(lesson.get("instructional_time", {}).get("class_periods_50_min", [0, 0])[index] for lesson in lessons)
        for index in (0, 1)
    )
    unit_periods = {
        unit.get("area"): sum(
            lesson.get("instructional_time", {}).get("class_periods_50_min", [0, 0])[0]
            for lesson in unit.get("lessons", [])
        )
        for unit in curriculum.get("units", [])
    }
    if unit_periods != EXPECTED_UNIT_PERIODS:
        add_error(errors, curriculum, f"mandatory classroom unit periods must be {EXPECTED_UNIT_PERIODS}, got {unit_periods}")

    route = curriculum.get("classroom_route", {})
    route = route if isinstance(route, dict) else {}
    mandatory_periods = route.get("mandatory_periods")
    extension_periods = route.get("recommended_extension_periods")
    recommended_periods = route.get("recommended_total_periods")
    if mandatory_periods != period_totals[0]:
        add_error(
            errors,
            curriculum,
            f"mandatory classroom total must match lesson minima, got {mandatory_periods} and {period_totals[0]}",
        )
    if all(isinstance(value, int) for value in (mandatory_periods, extension_periods, recommended_periods)):
        if mandatory_periods + extension_periods != recommended_periods:
            add_error(errors, curriculum, "recommended classroom total must equal mandatory periods plus extensions")

    allocations = route.get("extension_allocations", [])
    allocations = allocations if isinstance(allocations, list) else []
    allocation_total = sum(
        allocation.get("periods", 0)
        for allocation in allocations
        if isinstance(allocation, dict) and isinstance(allocation.get("periods", 0), int)
    )
    if allocation_total != extension_periods:
        add_error(errors, curriculum, "extension allocation total must match recommended extension periods")

    lesson_allocation_refs = [
        allocation.get("lesson_ref")
        for allocation in allocations
        if isinstance(allocation, dict) and allocation.get("kind") == "lesson"
    ]
    lesson_allocations = {
        allocation.get("lesson_ref"): allocation.get("periods")
        for allocation in allocations
        if isinstance(allocation, dict)
        and allocation.get("kind") == "lesson"
        and isinstance(allocation.get("lesson_ref"), str)
        and isinstance(allocation.get("periods"), int)
    }
    if len(lesson_allocation_refs) != len(set(lesson_allocation_refs)):
        add_error(errors, curriculum, "lesson extension allocations must not contain duplicate lesson refs")
    if set(lesson_allocations) != EXPECTED_EXTENSION_LESSONS:
        add_error(errors, curriculum, "lesson extensions must target A7, B7, C9, and D9")

    lesson_range_extensions = {
        lesson_id: lesson.get("instructional_time", {}).get("class_periods_50_min", [0, 0])[1]
        - lesson.get("instructional_time", {}).get("class_periods_50_min", [0, 0])[0]
        for lesson_id, lesson in lesson_by_id.items()
        if lesson.get("instructional_time", {}).get("class_periods_50_min", [0, 0])[1]
        > lesson.get("instructional_time", {}).get("class_periods_50_min", [0, 0])[0]
    }
    if lesson_allocations != lesson_range_extensions:
        add_error(errors, curriculum, "lesson extension allocations do not match instructional time ranges")

    cumulative_periods = sum(
        allocation.get("periods", 0)
        for allocation in allocations
        if isinstance(allocation, dict)
        and allocation.get("kind") == "cumulative"
        and isinstance(allocation.get("periods", 0), int)
    )
    if cumulative_periods != 1:
        add_error(errors, curriculum, "the classroom route must include one cumulative diagnostic period")
    if isinstance(recommended_periods, int) and period_totals[1] + cumulative_periods != recommended_periods:
        add_error(errors, curriculum, "recommended classroom total must include lesson and cumulative extensions")

    for problem in (record for record in records if record.get("type") == "problem"):
        for objective_ref in problem.get("objective_refs", []) or []:
            owner = objective_by_id.get(objective_ref)
            if owner is None:
                add_error(errors, problem, f"objective_refs target does not resolve: {objective_ref}")
            elif owner[0].get("lesson_id") not in (problem.get("lesson_refs", []) or []):
                add_error(errors, problem, f"objective {objective_ref} belongs to a lesson outside lesson_refs")


def check_coverage(
    errors: list[str], curriculum: dict, lesson: dict, entry: dict, by_id: dict[str, dict]
) -> None:
    objective_ref = entry.get("objective_ref")
    lesson_id = lesson.get("lesson_id")
    item_refs = entry.get("assessment_item_refs", []) if isinstance(entry.get("assessment_item_refs"), list) else []
    criterion_refs = entry.get("performance_criterion_refs", []) if isinstance(entry.get("performance_criterion_refs"), list) else []
    criterion_problem_ids: set[str] = set()

    for problem_ref in item_refs:
        problem = check_reference(errors, curriculum, "assessment_item_refs", problem_ref, "problem", by_id)
        if problem is None:
            continue
        if lesson_id not in (problem.get("lesson_refs", []) or []):
            add_error(errors, curriculum, f"coverage problem {problem_ref} does not belong to {lesson_id}")
        if objective_ref not in (problem.get("objective_refs", []) or []):
            add_error(errors, curriculum, f"coverage problem {problem_ref} does not declare objective {objective_ref}")

    for criterion_ref in criterion_refs:
        if not isinstance(criterion_ref, dict):
            continue
        rubric = check_reference(errors, curriculum, "performance_criterion_refs", criterion_ref.get("rubric_ref"), "rubric", by_id)
        if rubric is None:
            continue
        criterion_id = criterion_ref.get("criterion_id")
        criterion_ids = {criterion.get("id") for criterion in rubric.get("criteria", []) if isinstance(criterion, dict)}
        if criterion_id not in criterion_ids:
            add_error(errors, curriculum, f"performance criterion does not resolve: {rubric.get('id')}#{criterion_id}")
        problem_id = rubric.get("problem_id")
        problem = by_id.get(problem_id)
        if not isinstance(problem_id, str) or problem is None:
            continue
        criterion_problem_ids.add(problem_id)
        if problem.get("question_type") != "performance_task":
            add_error(
                errors,
                curriculum,
                f"performance criterion problem {problem_id} must use question_type performance_task",
            )
        if lesson_id not in (problem.get("lesson_refs", []) or []):
            add_error(errors, curriculum, f"performance criterion problem {problem_id} does not belong to {lesson_id}")
        if objective_ref not in (problem.get("objective_refs", []) or []):
            add_error(errors, curriculum, f"performance criterion problem {problem_id} does not declare objective {objective_ref}")

    distinct_item_refs = set(item_refs)
    complete = len(distinct_item_refs) >= 2 or (
        bool(distinct_item_refs) and bool(criterion_problem_ids - distinct_item_refs)
    )
    has_evidence = bool(distinct_item_refs or criterion_problem_ids)
    status = entry.get("status")
    if status == "not_started" and has_evidence:
        add_error(errors, curriculum, f"{lesson.get('order')} {objective_ref} is not_started but has evidence")
    elif status == "partial" and (not has_evidence or complete):
        add_error(errors, curriculum, f"{lesson.get('order')} {objective_ref} partial status does not match evidence")
    elif status == "complete" and not complete:
        add_error(errors, curriculum, f"{lesson.get('order')} {objective_ref} complete status lacks two distinct assessment artifacts")


def validate_repository(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    errors: list[str] = []
    records: list[dict] = []
    by_id: dict[str, dict] = {}

    for filename, (expected_type, schema_filename) in COLLECTION_FILES.items():
        path = root / "data" / "collections" / filename
        if not path.is_file():
            errors.append(f"{path}: missing collection")
            continue
        schema = load_schema(root, schema_filename)
        for record in read_ndjson(path):
            records.append(record)
            validate_schema(errors, record, schema)
            if record.get("type") != expected_type:
                add_error(errors, record, f"expected type {expected_type}, got {record.get('type')}")
            record_id = record.get("id")
            if isinstance(record_id, str):
                if record_id in by_id:
                    add_error(errors, record, f"duplicate id: {record_id}")
                else:
                    by_id[record_id] = record

    curriculum = read_json(root / CURRICULUM_PATH)
    validate_schema(errors, curriculum, load_schema(root, CURRICULUM_SCHEMA))
    curriculum_id = curriculum.get("id")
    if isinstance(curriculum_id, str):
        if curriculum_id in by_id:
            add_error(errors, curriculum, f"duplicate id: {curriculum_id}")
        by_id[curriculum_id] = curriculum

    check_curriculum(errors, root, curriculum, records, by_id)
    check_typed_record_graph(errors, records, by_id)
    check_repository_paths(errors, root, records)
    check_supersession(errors, records, by_id)
    check_revisions(errors, records, by_id)
    return errors, len(records) + 1


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Repository root to validate.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        errors, count = validate_repository(args.root)
    except (ValidationFailure, OSError, json.JSONDecodeError) as exc:
        print(f"Validation failed:\n- {exc}")
        return 1
    if errors:
        print("Validation failed:")
        for item in errors:
            print(f"- {item}")
        return 1
    print(f"Validation passed: {count} canonical records checked (including curriculum).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
