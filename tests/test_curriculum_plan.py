#!/usr/bin/env python3
"""Contract tests for the full Information I curriculum plan."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "curriculum" / "highschool_information_i.curriculum.json"
CONSERVATIVE_STATUSES = {"draft", "machine_checked", "human_review_requested"}
COVERAGE_STATUSES = {"not_started", "partial", "complete"}
COVERAGE_REQUIREMENT = "two_items_or_one_item_plus_performance_criterion"
OBJECTIVE_ID_PATTERN = re.compile(r"^obj\.[a-z0-9]+(?:\.[a-z0-9]+)*\.v[1-9][0-9]*$")


def load_curriculum() -> dict:
    return json.loads(CURRICULUM.read_text(encoding="utf-8"))


def load_collection(filename: str) -> list[dict]:
    path = ROOT / "data" / "collections" / filename
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_collection_ids(filename: str) -> set[str]:
    return {record["id"] for record in load_collection(filename)}


def test_full_scope_curriculum_contract() -> None:
    curriculum = load_curriculum()
    units = curriculum["units"]
    lessons = [lesson for unit in units for lesson in unit["lessons"]]

    assert curriculum["status"] in CONSERVATIVE_STATUSES
    assert curriculum["review_status"] == "needs_human_review"
    assert len(units) == 4
    assert len(lessons) == 32
    assert curriculum["global_prerequisites"]
    assert curriculum["numbering_convention"]
    prerequisites_text = " ".join(curriculum["global_prerequisites"]).lower()
    assert "no advanced statistics or prior programming is assumed" in prerequisites_text
    assert "arithmetic" in prerequisites_text
    assert "chart reading" in prerequisites_text

    lesson_ids = [lesson["lesson_id"] for lesson in lessons]
    assert len(lesson_ids) == len(set(lesson_ids))

    required_fields = {
        "order",
        "lesson_id",
        "title",
        "status",
        "learning_objectives",
        "prerequisites",
        "key_concepts",
        "assessment_intent",
        "depends_on",
        "source_refs",
        "instructional_time",
        "assessment_coverage",
    }
    objective_ids: list[str] = []
    for lesson in lessons:
        assert required_fields <= lesson.keys()
        assert lesson["status"] in CONSERVATIVE_STATUSES
        assert 2 <= len(lesson["learning_objectives"]) <= 4
        assert lesson["prerequisites"]
        assert lesson["key_concepts"]
        assert lesson["assessment_intent"]

        objectives = lesson["learning_objectives"]
        lesson_objective_ids = [objective["id"] for objective in objectives]
        assert all(OBJECTIVE_ID_PATTERN.fullmatch(objective_id) for objective_id in lesson_objective_ids)
        assert len(lesson_objective_ids) == len(set(lesson_objective_ids))
        objective_ids.extend(lesson_objective_ids)
        for index, objective in enumerate(objectives, start=1):
            assert objective["label"] == f'{lesson["order"]}.O{index}'
            assert objective["statement"]
            assert objective["expected_evidence"]

        coverage = lesson["assessment_coverage"]
        assert {entry["objective_ref"] for entry in coverage} == set(lesson_objective_ids)
        for entry in coverage:
            assert entry["requirement"] == COVERAGE_REQUIREMENT
            assert entry["status"] in COVERAGE_STATUSES
            assert isinstance(entry["assessment_item_refs"], list)
            assert isinstance(entry["performance_criterion_refs"], list)

        time = lesson["instructional_time"]
        for field in ("class_periods_50_min", "self_study_minutes"):
            minimum, maximum = time[field]
            assert isinstance(minimum, int) and isinstance(maximum, int)
            assert 0 < minimum <= maximum
        assert isinstance(time["is_multi_session_project"], bool)

    assert len(objective_ids) == len(set(objective_ids))


def test_time_and_assessment_baselines() -> None:
    curriculum = load_curriculum()
    lessons = [lesson for unit in curriculum["units"] for lesson in unit["lessons"]]
    problem_ids = load_collection_ids("problems.ndjson")
    rubrics = {record["id"]: record for record in load_collection("rubrics.ndjson")}

    period_minimum = sum(
        lesson["instructional_time"]["class_periods_50_min"][0]
        for lesson in lessons
    )
    period_maximum = sum(
        lesson["instructional_time"]["class_periods_50_min"][1]
        for lesson in lessons
    )
    project_orders = {
        lesson["order"]
        for lesson in lessons
        if lesson["instructional_time"]["is_multi_session_project"]
    }
    assert (period_minimum, period_maximum) == (70, 76)
    assert project_orders == {"A7", "B7", "C9", "D9"}

    for lesson in lessons:
        for entry in lesson["assessment_coverage"]:
            item_refs = entry["assessment_item_refs"]
            criterion_refs = entry["performance_criterion_refs"]
            assert len(item_refs) == len(set(item_refs))
            assert set(item_refs) <= problem_ids
            criterion_pairs = [
                (criterion_ref["rubric_ref"], criterion_ref["criterion_id"])
                for criterion_ref in criterion_refs
            ]
            assert len(criterion_pairs) == len(set(criterion_pairs))
            for criterion_ref in criterion_refs:
                assert set(criterion_ref) == {"rubric_ref", "criterion_id"}
                rubric = rubrics[criterion_ref["rubric_ref"]]
                assert rubric["problem_id"] in item_refs
                criterion_ids = {criterion["id"] for criterion in rubric["criteria"]}
                assert criterion_ref["criterion_id"] in criterion_ids

            complete = len(item_refs) >= 2 or (
                len(item_refs) >= 1 and len(criterion_refs) >= 1
            )
            has_evidence = bool(item_refs or criterion_refs)
            if entry["status"] == "not_started":
                assert not has_evidence
            elif entry["status"] == "partial":
                assert has_evidence and not complete
            else:
                assert complete

    c2 = next(lesson for lesson in lessons if lesson["order"] == "C2")
    assert c2["depends_on"] == []
    c2_objective_labels = {
        objective["id"]: objective["label"]
        for objective in c2["learning_objectives"]
    }
    assert {
        c2_objective_labels[entry["objective_ref"]]: entry["status"]
        for entry in c2["assessment_coverage"]
    } == {"C2.O1": "not_started", "C2.O2": "partial", "C2.O3": "partial"}


def test_curriculum_dependencies_are_resolved_and_acyclic() -> None:
    curriculum = load_curriculum()
    lessons = [lesson for unit in curriculum["units"] for lesson in unit["lessons"]]
    graph = {lesson["lesson_id"]: lesson["depends_on"] for lesson in lessons}

    assert not ({dependency for dependencies in graph.values() for dependency in dependencies} - graph.keys())

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(lesson_id: str) -> None:
        if lesson_id in visited:
            return
        assert lesson_id not in visiting, f"curriculum dependency cycle at {lesson_id}"
        visiting.add(lesson_id)
        for dependency in graph[lesson_id]:
            visit(dependency)
        visiting.remove(lesson_id)
        visited.add(lesson_id)

    for lesson_id in graph:
        visit(lesson_id)

    assert "lesson.info1.programming.loops.v1" in graph[
        "lesson.info1.programming.functions.v1"
    ]
    assert "lesson.info1.data.descriptive.analysis.v1" in graph[
        "lesson.info1.data.databases.queries.v1"
    ]


def test_curriculum_sources_and_existing_lessons_resolve() -> None:
    curriculum = load_curriculum()
    source_ids = load_collection_ids("sources.ndjson")
    canonical_lesson_ids = load_collection_ids("lessons.ndjson")
    planned_lessons = {
        lesson["lesson_id"]: lesson
        for unit in curriculum["units"]
        for lesson in unit["lessons"]
    }

    assert set(curriculum["source_refs"]) <= source_ids
    for unit in curriculum["units"]:
        assert unit["status"] in CONSERVATIVE_STATUSES
        assert unit["source_locator"]["normative"]
        assert unit["source_locator"]["commentary"]
        for lesson in unit["lessons"]:
            assert set(lesson["source_refs"]) <= source_ids

    assert canonical_lesson_ids <= planned_lessons.keys()
    for lesson_id in canonical_lesson_ids:
        assert planned_lessons[lesson_id]["status"] == "human_review_requested"
