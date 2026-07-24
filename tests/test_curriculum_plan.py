#!/usr/bin/env python3
"""Contract tests for the full Information I curriculum plan."""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "curriculum" / "highschool_information_i.curriculum.json"
CONSERVATIVE_STATUSES = {"draft", "machine_checked", "human_review_requested"}
COVERAGE_STATUSES = {"not_started", "partial", "complete"}
COVERAGE_REQUIREMENT = "two_items_or_one_item_plus_performance_criterion"
OBJECTIVE_ID_PATTERN = re.compile(r"^obj\.[a-z0-9]+(?:\.[a-z0-9]+)*\.v[1-9][0-9]*$")
LESSON_ID_DIGEST = "3e70077afec6375a2fd09ac48ac74ababf69a1bde2cdae916a9145daff5805f5"
OBJECTIVE_ID_DIGEST = "c516448693d76e035d8720de968f5dd5eff10a4711cf5d1703539b9479589c47"


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


def id_digest(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()


def learner_facing_text() -> str:
    paths = [
        *sorted((ROOT / "lessons").rglob("*.md")),
        *sorted((ROOT / "teacher_guides").rglob("*.md")),
        ROOT / "data" / "collections" / "lessons.ndjson",
        ROOT / "data" / "collections" / "problems.ndjson",
        ROOT / "data" / "collections" / "answers.ndjson",
        ROOT / "data" / "collections" / "rubrics.ndjson",
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_selected_display_terminology_is_consistent() -> None:
    text = learner_facing_text()
    for rejected in ("情報Ⅰ", "Ｗｅｂ", "データーベース", "シュミレーション"):
        assert rejected not in text


def test_full_scope_curriculum_contract() -> None:
    curriculum = load_curriculum()
    units = curriculum["units"]
    lessons = [lesson for unit in units for lesson in unit["lessons"]]

    assert curriculum["status"] in CONSERVATIVE_STATUSES
    assert curriculum["review_status"] == "needs_human_review"
    assert curriculum["scope_version"] == "0.3"
    assert curriculum["tracking_issue"] == 59
    assert len(units) == 4
    assert len(lessons) == 32
    assert {
        unit["area"]: [lesson["order"] for lesson in unit["lessons"]]
        for unit in units
    } == {
        "mext.info1.1": [f"A{index}" for index in range(1, 8)],
        "mext.info1.2": [f"B{index}" for index in range(1, 8)],
        "mext.info1.3": [f"C{index}" for index in range(1, 10)],
        "mext.info1.4": [f"D{index}" for index in range(1, 10)],
    }
    assert curriculum["global_prerequisites"]
    assert curriculum["numbering_convention"]
    prerequisites_text = " ".join(curriculum["global_prerequisites"]).lower()
    assert "no advanced statistics or prior programming is assumed" in prerequisites_text
    assert "arithmetic" in prerequisites_text
    assert "chart reading" in prerequisites_text

    lesson_ids = [lesson["lesson_id"] for lesson in lessons]
    assert len(lesson_ids) == len(set(lesson_ids))
    assert id_digest(lesson_ids) == LESSON_ID_DIGEST

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
    assert len(objective_ids) == 96
    assert id_digest(objective_ids) == OBJECTIVE_ID_DIGEST


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
    route = curriculum["classroom_route"]
    assert route["period_minutes"] == 50
    assert route["mandatory_periods"] == 66
    assert route["recommended_extension_periods"] == 4
    assert route["recommended_total_periods"] == 70
    assert period_minimum == route["mandatory_periods"]

    unit_periods = {
        unit["area"]: sum(
            lesson["instructional_time"]["class_periods_50_min"][0]
            for lesson in unit["lessons"]
        )
        for unit in curriculum["units"]
    }
    assert unit_periods == {
        "mext.info1.1": 11,
        "mext.info1.2": 12,
        "mext.info1.3": 21,
        "mext.info1.4": 22,
    }

    for periods in unit_periods.values():
        share = periods / route["mandatory_periods"]
        assert 0.15 <= share <= 0.35

    allocations = route["extension_allocations"]
    assert sum(allocation["periods"] for allocation in allocations) == 4
    lesson_allocations = {
        allocation["lesson_ref"]: allocation["periods"]
        for allocation in allocations
        if allocation["kind"] == "lesson"
    }
    assert lesson_allocations == {
        "lesson.info1.society.inquiry.project.v1": 1,
        "lesson.info1.design.project.v1": 1,
        "lesson.info1.programming.project.v1": 1,
        "lesson.info1.data.investigation.project.v1": 1,
    }
    assert all(allocation["kind"] == "lesson" for allocation in allocations)
    assert period_maximum == period_minimum + sum(lesson_allocations.values())
    assert route["recommended_total_periods"] == period_maximum
    for lesson in lessons:
        minimum, maximum = lesson["instructional_time"]["class_periods_50_min"]
        assert maximum - minimum == lesson_allocations.get(lesson["lesson_id"], 0)

    assert project_orders == {"A7", "B7", "C9", "D9"}
    c9 = next(lesson for lesson in lessons if lesson["order"] == "C9")
    assert c9["instructional_time"]["class_periods_50_min"] == [5, 6]

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
                assert rubric["problem_id"] not in item_refs
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

    unit_c = next(unit for unit in curriculum["units"] if unit["id"] == "unit.info1.programming.v1")
    unit_c_lessons = unit_c["lessons"]
    unit_c_lesson_ids = {lesson["lesson_id"] for lesson in unit_c_lessons}
    unit_c_problem_counts = {
        lesson_id: sum(
            lesson_id in problem["lesson_refs"]
            for problem in load_collection("problems.ndjson")
        )
        for lesson_id in unit_c_lesson_ids
    }
    assert unit_c_problem_counts == {
        "lesson.info1.programming.computer.systems.v1": 4,
        "lesson.info1.programming.variables.v1": 8,
        "lesson.info1.programming.conditionals.v1": 8,
        "lesson.info1.programming.loops.v1": 8,
        "lesson.info1.programming.collections.strings.v1": 4,
        "lesson.info1.programming.functions.v1": 4,
        "lesson.info1.programming.algorithms.v1": 4,
        "lesson.info1.programming.modeling.simulation.v1": 4,
        "lesson.info1.programming.project.v1": 4,
    }
    assert sum(unit_c_problem_counts.values()) == 48
    assert all(
        entry["status"] == "complete"
        for lesson in unit_c_lessons
        for entry in lesson["assessment_coverage"]
    )

    c2 = next(lesson for lesson in unit_c_lessons if lesson["order"] == "C2")
    assert c2["depends_on"] == []
    c2_objective_labels = {
        objective["id"]: objective["label"]
        for objective in c2["learning_objectives"]
    }
    assert {
        c2_objective_labels[entry["objective_ref"]]: entry["status"]
        for entry in c2["assessment_coverage"]
    } == {"C2.O1": "complete", "C2.O2": "complete", "C2.O3": "complete"}
    c2_coverage_refs = {
        c2_objective_labels[entry["objective_ref"]]: entry["assessment_item_refs"]
        for entry in c2["assessment_coverage"]
    }
    assert c2_coverage_refs == {
        "C2.O1": [
            "prob.info1.variables.003.v1",
            "prob.info1.variables.004.v1",
            "prob.info1.variables.008.v1",
        ],
        "C2.O2": [
            "prob.info1.variables.005.v1",
            "prob.info1.variables.007.v1",
            "prob.info1.variables.008.v1",
        ],
        "C2.O3": [
            "prob.info1.variables.006.v1",
            "prob.info1.variables.007.v1",
            "prob.info1.variables.008.v1",
        ],
    }
    assert all(
        "prob.info1.variables.001.v1" not in item_refs
        and "prob.info1.variables.002.v1" not in item_refs
        for item_refs in c2_coverage_refs.values()
    )

    c9 = next(lesson for lesson in unit_c_lessons if lesson["order"] == "C9")
    assert {
        entry["objective_ref"]: (
            entry["assessment_item_refs"],
            entry["performance_criterion_refs"],
        )
        for entry in c9["assessment_coverage"]
    } == {
        "obj.info1.programming.project.001.v1": (
            ["prob.info1.programming.project.001.v1"],
            [
                {
                    "rubric_ref": "rubric.prob.info1.programming.project.004.v1",
                    "criterion_id": "c1_validation",
                },
                {
                    "rubric_ref": "rubric.prob.info1.programming.project.004.v1",
                    "criterion_id": "c2_fifo_ordering",
                },
                {
                    "rubric_ref": "rubric.prob.info1.programming.project.004.v1",
                    "criterion_id": "c5_executable_evidence",
                },
            ],
        ),
        "obj.info1.programming.project.002.v1": (
            ["prob.info1.programming.project.002.v1"],
            [{
                "rubric_ref": "rubric.prob.info1.programming.project.004.v1",
                "criterion_id": "c6_test_classes",
            }],
        ),
        "obj.info1.programming.project.003.v1": (
            ["prob.info1.programming.project.003.v1"],
            [
                {
                    "rubric_ref": "rubric.prob.info1.programming.project.004.v1",
                    "criterion_id": "c7_requirement_evaluation",
                },
                {
                    "rubric_ref": "rubric.prob.info1.programming.project.004.v1",
                    "criterion_id": "c8_limitations_retest",
                },
            ],
        ),
    }

    unit_d = next(
        unit for unit in curriculum["units"]
        if unit["id"] == "unit.info1.networks.data.v1"
    )
    unit_d_lessons = unit_d["lessons"]
    unit_d_lesson_ids = {lesson["lesson_id"] for lesson in unit_d_lessons}
    unit_d_problem_counts = {
        lesson_id: sum(
            lesson_id in problem["lesson_refs"]
            for problem in load_collection("problems.ndjson")
        )
        for lesson_id in unit_d_lesson_ids
    }
    assert unit_d_problem_counts == {
        "lesson.info1.networks.protocols.v1": 4,
        "lesson.info1.networks.internet.web.v1": 4,
        "lesson.info1.networks.security.v1": 4,
        "lesson.info1.data.lifecycle.v1": 4,
        "lesson.info1.data.cleaning.v1": 4,
        "lesson.info1.data.descriptive.analysis.v1": 4,
        "lesson.info1.data.visualization.interpretation.v1": 4,
        "lesson.info1.data.databases.queries.v1": 4,
        "lesson.info1.data.investigation.project.v1": 4,
    }
    assert sum(unit_d_problem_counts.values()) == 36
    unit_d_statuses = {
        entry["objective_ref"]: entry["status"]
        for lesson in unit_d_lessons
        for entry in lesson["assessment_coverage"]
    }
    assert sum(status == "complete" for status in unit_d_statuses.values()) == 26
    assert {
        objective_id for objective_id, status in unit_d_statuses.items()
        if status == "partial"
    } == {"obj.info1.data.descriptive.analysis.002.v1"}

    d9 = next(lesson for lesson in unit_d_lessons if lesson["order"] == "D9")
    assert {
        entry["objective_ref"]: (
            entry["assessment_item_refs"],
            entry["performance_criterion_refs"],
        )
        for entry in d9["assessment_coverage"]
    } == {
        "obj.info1.data.investigation.project.001.v1": (
            ["prob.info1.data.investigation.project.001.v1"],
            [{
                "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                "criterion_id": "c1_question_ethics",
            }],
        ),
        "obj.info1.data.investigation.project.002.v1": (
            ["prob.info1.data.investigation.project.002.v1"],
            [
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c2_reproducible_workflow",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c3_accessible_evidence",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c6_provenance_dictionary",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c7_transformation_log",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c8_independent_check",
                },
            ],
        ),
        "obj.info1.data.investigation.project.003.v1": (
            ["prob.info1.data.investigation.project.003.v1"],
            [
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c4_bounded_conclusion",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c5_limits_improvement",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c9_sensitivity_results",
                },
                {
                    "rubric_ref": "rubric.prob.info1.data.investigation.project.004.v1",
                    "criterion_id": "c10_presentation_revision",
                },
            ],
        ),
    }


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


def test_unit_c_review_contracts() -> None:
    curriculum = load_curriculum()
    unit_c = next(
        unit for unit in curriculum["units"]
        if unit["id"] == "unit.info1.programming.v1"
    )
    planned = {lesson["order"]: lesson for lesson in unit_c["lessons"]}
    lessons = {
        record["id"]: record for record in load_collection("lessons.ndjson")
    }
    assert "lesson.info1.programming.collections.strings.v1" in planned["C6"]["depends_on"]
    assert "C5: Collections and Strings." in planned["C6"]["prerequisites"]
    problems = {
        record["id"]: record for record in load_collection("problems.ndjson")
    }
    answers = {
        record["id"]: record for record in load_collection("answers.ndjson")
    }
    rubrics = {
        record["id"]: record for record in load_collection("rubrics.ndjson")
    }
    sources = {
        record["id"]: record for record in load_collection("sources.ndjson")
    }

    assert any(
        "All unit objectives, sequencing, and assessments are project-authored interpretations, not MEXT wording"
        in note
        for note in curriculum["notes"]
    )
    assert planned["C2"]["prerequisites"] == [
        "No prior programming is assumed; required arithmetic expressions and ordered execution are introduced and checked inside this lesson."
    ]

    unit_c_lesson_ids = {
        lesson["lesson_id"] for lesson in unit_c["lessons"]
    }
    unit_c_problems = [
        problem for problem in problems.values()
        if unit_c_lesson_ids.intersection(problem["lesson_refs"])
    ]
    assert len(unit_c_problems) == 48

    c1_text = " ".join([
        *[objective["statement"] for objective in planned["C1"]["learning_objectives"]],
        problems["prob.info1.programming.computer.systems.001.v1"]["question"],
        problems["prob.info1.programming.computer.systems.003.v1"]["question"],
    ])
    for term in ("operating system", "OS", "処理装置", "丸め誤差", "資源"):
        assert term in c1_text
    c1_integrated = " ".join([
        problems["prob.info1.programming.computer.systems.004.v1"]["question"],
        answers["ans.prob.info1.programming.computer.systems.004.v1"]["canonical_answer"],
    ])
    for term in ("OS", "255", "23.5", "+0.03", "16 MB", "1020 MB"):
        assert term in c1_integrated

    c3 = planned["C3"]
    assert all(term in " ".join(c3["key_concepts"]) for term in ("and", "or", "not"))
    c3_transfer = problems["prob.info1.conditionals.001.v1"]["question"]
    assert "Pythonを使わず" in c3_transfer
    assert all(term in c3_transfer for term in ("and", "or", "not"))

    c7 = planned["C7"]
    assert "linear search" in c7["learning_objectives"][0]["statement"].lower()
    assert "sorting" in c7["learning_objectives"][0]["statement"].lower()
    c7_text = []
    for number in range(1, 5):
        suffix = f"{number:03d}.v1"
        problem = problems[f"prob.info1.programming.algorithms.{suffix}"]
        answer = answers[f"ans.prob.info1.programming.algorithms.{suffix}"]
        rubric = rubrics[f"rubric.prob.info1.programming.algorithms.{suffix}"]
        c7_text.append(" ".join([
            problem["question"],
            answer["canonical_answer"],
            answer["explanation"],
            *[criterion["description"] for criterion in rubric["criteria"]],
        ]))
    combined_c7 = " ".join(c7_text)
    assert "線形探索" in combined_c7
    assert "選択ソート" in combined_c7
    assert "28回" in combined_c7
    assert "FIFO" not in combined_c7
    assert "Pythonなし" in problems["prob.info1.programming.algorithms.004.v1"]["question"]

    c8 = planned["C8"]
    assert "deterministic" in c8["learning_objectives"][1]["statement"].lower()
    assert "two deterministic assumption sets" in c8["learning_objectives"][2]["statement"].lower()
    c8_comparison = problems["prob.info1.programming.modeling.simulation.003.v1"]["question"]
    assert all(term in c8_comparison for term in ("モデルA", "モデルB", "0.75", "2.25"))

    c9_problem = problems["prob.info1.programming.project.004.v1"]["question"]
    for signature in (
        "validation_error(arrival, sheets)",
        "keep_valid_jobs(jobs)",
        "fifo_order(jobs)",
        "simulate_fifo(ordered_jobs, speed)",
        "average_wait(results)",
    ):
        assert signature in c9_problem
    c9_answer = answers["ans.prob.info1.programming.project.004.v1"]
    c9_rubric = rubrics["rubric.prob.info1.programming.project.004.v1"]
    assert c9_answer["verification_evidence"][-1]["expected"].startswith(
        "all 14 show_check calls"
    )
    assert "assert" not in c9_answer["canonical_answer"]
    assert "assert" not in " ".join(
        criterion["description"] for criterion in c9_rubric["criteria"]
    )
    assert "項目不足" not in c9_answer["canonical_answer"]
    assert " or " not in c9_answer["canonical_answer"]
    assert "依頼数は10件以下" in c9_answer["canonical_answer"]
    assert "期待値:" in c9_answer["canonical_answer"]
    assert "実際値:" in c9_answer["canonical_answer"]
    for term in ("非減少順", "同時到着", "降順", "待ち時間非負"):
        assert term in c9_answer["canonical_answer"]
    for schema in (
        "[id, arrival, sheets]",
        "[id, reason]",
        "[id, start, finish, wait]",
    ):
        assert schema in c9_problem
        assert schema in c9_answer["canonical_answer"]
        assert schema in " ".join(
            criterion["description"] for criterion in c9_rubric["criteria"]
        )

    namespace: dict[str, object] = {}
    exec(c9_answer["canonical_answer"], namespace)
    keep_valid_jobs = namespace["keep_valid_jobs"]
    fifo_order = namespace["fifo_order"]
    simulate_fifo = namespace["simulate_fifo"]
    assert callable(keep_valid_jobs)
    assert callable(fifo_order)
    assert callable(simulate_fifo)

    ordered = [["N1", 0, 8], ["N2", 1, 4]]
    ordered_split = keep_valid_jobs(ordered)
    ordered_results = simulate_fifo(fifo_order(ordered_split[0]), 4)
    assert ordered_results == [["N1", 0, 2, 0], ["N2", 2, 3, 1]]

    tied = [["T2", 2, 8], ["T1", 2, 4]]
    tied_split = keep_valid_jobs(tied)
    tied_results = simulate_fifo(fifo_order(tied_split[0]), 4)
    assert tied_results == [["T2", 2, 4, 0], ["T1", 4, 5, 2]]

    descending = [["D2", 2, 8], ["D1", 1, 4]]
    assert keep_valid_jobs(descending) == [
        [],
        [["D2", "到着時刻は非減少順"], ["D1", "到着時刻は非減少順"]],
    ]
    assert keep_valid_jobs([]) == [[], []]
    assert keep_valid_jobs([["I0", 0, 0]]) == [
        [], [["I0", "枚数は1〜40"]]
    ]
    assert all(row[3] >= 0 for row in ordered_results + tied_results)

    total_points = sum(criterion["points"] for criterion in c9_rubric["criteria"])
    assert max(criterion["points"] for criterion in c9_rubric["criteria"]) / total_points <= 0.35
    python_points = sum(
        criterion["points"] for criterion in c9_rubric["criteria"]
        if "Python実装" in criterion["description"]
    )
    assert python_points / total_points <= 0.25

    for number in range(2, 5):
        suffix = f"{number:03d}.v1"
        problem = problems[f"prob.info1.programming.project.{suffix}"]
        answer = answers[f"ans.prob.info1.programming.project.{suffix}"]
        rubric = rubrics[f"rubric.prob.info1.programming.project.{suffix}"]
        evidence_text = " ".join([
            problem["question"],
            answer["canonical_answer"],
            *[criterion["description"] for criterion in rubric["criteria"]],
        ])
        for term in ("期待値", "実際値", "一致"):
            assert term in evidence_text
        assert answer["verification_status"] == "machine_checked"
        assert answer["verification_evidence"][-1]["result"] == "passed"
    for suffix in ("003", "004"):
        improvement_text = " ".join([
            problems[f"prob.info1.programming.project.{suffix}.v1"]["question"],
            answers[f"ans.prob.info1.programming.project.{suffix}.v1"]["canonical_answer"],
        ])
        assert "改善" in improvement_text
        assert "再テスト" in improvement_text

    c8_answer = answers["ans.prob.info1.programming.modeling.simulation.004.v1"]
    c8_tree = ast.parse(c8_answer["canonical_answer"])
    assert not any(isinstance(node, (ast.Assert, ast.Tuple)) for node in ast.walk(c8_tree))
    assert not any(
        isinstance(node, ast.Call)
        and (
            isinstance(node.func, ast.Name) and node.func.id in {"len", "max"}
            or isinstance(node.func, ast.Attribute) and node.func.attr == "append"
        )
        for node in ast.walk(c8_tree)
    )
    assert "simulate_and_display" in c8_answer["canonical_answer"]
    assert "setup" in c8_answer["canonical_answer"]

    c6_problem = problems["prob.info1.programming.functions.004.v1"]
    c6_answer = answers["ans.prob.info1.programming.functions.004.v1"]
    c6_rubric = rubrics["rubric.prob.info1.programming.functions.004.v1"]
    assert "display_result(job_id, sheets)" in c6_problem["question"]
    assert 'print(job_id, sheets, "枚")' in c6_answer["canonical_answer"]
    assert "str(" not in c6_answer["canonical_answer"]
    assert "make_message" not in c6_answer["canonical_answer"]
    assert "表示" in " ".join(
        criterion["description"] for criterion in c6_rubric["criteria"]
    )

    for suffix in ("003", "008"):
        assignment_answer = answers[f"ans.prob.info1.variables.{suffix}.v1"]
        assert "初心者向けモデル" in assignment_answer["canonical_answer"]
        assert "結び付け" in assignment_answer["canonical_answer"]
        assert assignment_answer["source_refs"] == [
            "src.python.assignment.reference.v1"
        ]

    c8_problem = problems[
        "prob.info1.programming.modeling.simulation.002.v1"
    ]["question"]
    assert "for job in jobs:" in c8_problem
    assert "job[0]" in c8_problem
    assert "max(" not in c8_problem
    assert "for job_id," not in c8_problem

    required_sources = {
        "src.python.assignment.reference.v1",
        "src.python.compound.statements.v1",
        "src.python.sequence.types.v1",
        "src.python.functions.tutorial.v1",
        "src.nist.csrc.storage.glossary.v1",
    }
    assert required_sources <= set(sources)
    assert "src.nist.csrc.storage.glossary.v1" in lessons[
        "lesson.info1.programming.computer.systems.v1"
    ]["source_refs"]
    for suffix in ("001", "003", "004"):
        answer = answers[
            f"ans.prob.info1.programming.computer.systems.{suffix}.v1"
        ]
        assert "src.nist.csrc.storage.glossary.v1" not in answer["source_refs"]
    assert "Appendix A" in sources["src.nist.csrc.storage.glossary.v1"]["notes"]
    assert "PDF page 42" in sources["src.nist.csrc.storage.glossary.v1"]["notes"]
    for source_id in (
        "src.mext.highschool.curriculum2018.v1",
        "src.mext.information.commentary2018.v1",
    ):
        assert "project-authored interpretations" in sources[source_id]["notes"]
        assert "not prescribed MEXT wording or requirements" in sources[source_id]["notes"]
    assert "src.python.assignment.reference.v1" in lessons[
        "lesson.info1.programming.variables.v1"
    ]["source_refs"]
    assert "src.python.sequence.types.v1" in lessons[
        "lesson.info1.programming.collections.strings.v1"
    ]["source_refs"]
    assert "src.python.functions.tutorial.v1" in lessons[
        "lesson.info1.programming.functions.v1"
    ]["source_refs"]


def test_b7_requires_both_visualization_and_prototyping() -> None:
    curriculum = load_curriculum()
    unit_b = next(unit for unit in curriculum["units"] if unit["area"] == "mext.info1.2")
    b7 = next(lesson for lesson in unit_b["lessons"] if lesson["order"] == "B7")

    assert b7["prerequisites"] == [
        "B5: Data Visualization and Misleading Presentation.",
        "B6: Prototyping and Usability Evaluation.",
    ]
    assert b7["depends_on"] == [
        "lesson.info1.design.data.visualization.v1",
        "lesson.info1.design.prototype.usability.v1",
    ]


def test_unit_d_network_security_contracts() -> None:
    curriculum = load_curriculum()
    unit_d = next(
        unit for unit in curriculum["units"]
        if unit["id"] == "unit.info1.networks.data.v1"
    )
    planned = {lesson["order"]: lesson for lesson in unit_d["lessons"]}
    lessons = {
        record["id"]: record for record in load_collection("lessons.ndjson")
    }
    problems = {
        record["id"]: record for record in load_collection("problems.ndjson")
    }
    answers = {
        record["id"]: record for record in load_collection("answers.ndjson")
    }
    rubrics = {
        record["id"]: record for record in load_collection("rubrics.ndjson")
    }
    sources = {
        record["id"]: record for record in load_collection("sources.ndjson")
    }

    unit_d_lesson_ids = {
        planned[order]["lesson_id"] for order in ("D1", "D2", "D3")
    }
    unit_d_problems = [
        problem for problem in problems.values()
        if unit_d_lesson_ids.intersection(problem["lesson_refs"])
    ]
    assert len(unit_d_problems) == 12
    assert all(problem["status"] == "draft" for problem in unit_d_problems)

    d1_text = " ".join([
        *[objective["statement"] for objective in planned["D1"]["learning_objectives"]],
        *planned["D1"]["key_concepts"],
        *[problem["question"] for problem in unit_d_problems if ".protocols." in problem["id"]],
    ])
    for term in (
        "client", "server", "hub", "switch", "router", "LAN", "WAN",
        "IP address", "routing control", "transport control", "protocol layers",
    ):
        assert term.lower() in d1_text.lower()
    assert problems["prob.info1.networks.protocols.003.v1"]["question_type"] == "diagnosis"
    assert "src.ietf.rfc9293.v1" in planned["D1"]["source_refs"]

    d2_trace = " ".join([
        problems["prob.info1.networks.internet.web.002.v1"]["question"],
        answers["ans.prob.info1.networks.internet.web.002.v1"]["canonical_answer"],
        *[criterion["description"] for criterion in rubrics[
            "rubric.prob.info1.networks.internet.web.002.v1"
        ]["criteria"]],
    ])
    for term in (
        "https://library.example.test/books/B204?view=summary",
        "DNS", "192.0.2.24", "スイッチ", "ルーター", "伝送制御",
            "TLS", "証明書", "HTTP要求", "サービス内処理", "表示",
    ):
        assert term in d2_trace
    d2_diagnosis = " ".join([
        problems["prob.info1.networks.internet.web.003.v1"]["question"],
        answers["ans.prob.info1.networks.internet.web.003.v1"]["canonical_answer"],
    ])
    for term in ("DNS", "TLS", "証明書", "HTTP", "アプリケーション", "データベース"):
        assert term in d2_diagnosis

    d3_text = " ".join([
        *[objective["statement"] for objective in planned["D3"]["learning_objectives"]],
        *[problem["question"] for problem in unit_d_problems if ".security." in problem["id"]],
        *[answer["canonical_answer"] for answer in answers.values() if answer["problem_id"].startswith("prob.info1.networks.security.")],
    ])
    for term in (
        "confidentiality", "integrity", "availability", "authentication",
        "authorization", "暗号化", "ハッシュ", "ディジタル署名", "証明書",
        "MFA", "最小権限", "更新", "バックアップ", "フィッシング", "残余",
    ):
        assert term.lower() in d3_text.lower()
    assert "身元確認とは別" in answers[
        "ans.prob.info1.networks.security.001.v1"
    ]["canonical_answer"]

    required_sources = {
        "src.ietf.rfc5737.v1",
        "src.ietf.rfc2606.v1",
        "src.ietf.rfc3986.v1",
        "src.ietf.rfc9110.v1",
        "src.ietf.rfc9293.v1",
        "src.ietf.rfc9499.v1",
        "src.ietf.rfc9525.v1",
        "src.ietf.rfc9846.v1",
        "src.nist.sp800.63b4.v1",
        "src.nist.fips1804.v1",
        "src.nist.fips1865.v1",
    }
    assert required_sources <= set(sources)
    assert required_sources <= set().union(
        *(set(planned[order]["source_refs"]) for order in ("D1", "D2", "D3"))
    )
    assert "updates RFC 1122" in sources["src.ietf.rfc9293.v1"]["notes"]
    assert "obsoletes RFC 6125" in sources["src.ietf.rfc9525.v1"]["notes"]
    assert "obsoletes RFC 8446" in sources["src.ietf.rfc9846.v1"]["notes"]
    assert "supersedes SP 800-63B" in sources["src.nist.sp800.63b4.v1"]["notes"]
    assert "planned revision" in sources["src.nist.fips1804.v1"]["notes"]

    d2_rubric = rubrics["rubric.prob.info1.networks.internet.web.004.v1"]
    assert [criterion["id"] for criterion in d2_rubric["criteria"]] == ["c1", "c2", "c3"]
    assert sum(criterion["points"] for criterion in d2_rubric["criteria"]) == 3

    for problem in unit_d_problems:
        answer = answers[problem["answer_refs"][0]]
        rubric = rubrics[problem["rubric_refs"][0]]
        if problem["id"] == "prob.info1.networks.internet.web.004.v1":
            expected_revision = 7
        elif problem["id"] == "prob.info1.networks.internet.web.002.v1":
            expected_revision = 5
        elif problem["id"] == "prob.info1.networks.internet.web.003.v1":
            expected_revision = 4
        elif ".internet.web." in problem["id"]:
            expected_revision = 3
        else:
            expected_revision = 2
        assert answer["revision"] == expected_revision
        assert answer["status"] == "draft"
        assert answer["review_status"] == "needs_human_review"
        assert "verification_status" not in answer
        assert "verification_evidence" not in answer
        assert rubric["status"] == "draft"

    learner_paths = [
        ROOT / "lessons" / "highschool_information_i" / "networks_data" / filename
        for filename in (
            "00_networks_protocols.md",
            "01_internet_web_services.md",
            "02_security.md",
        )
    ]
    learner_text = "\n".join(path.read_text(encoding="utf-8") for path in learner_paths)
    assert "Python" not in learner_text
    assert "許可のないネットワーク調査は行いません" in learner_text
    assert "実システムを許可なく調査" in learner_text


def test_unit_d_data_foundation_and_investigation_contracts() -> None:
    curriculum = load_curriculum()
    unit_d = next(
        unit for unit in curriculum["units"]
        if unit["id"] == "unit.info1.networks.data.v1"
    )
    planned = {lesson["order"]: lesson for lesson in unit_d["lessons"]}
    problems = {
        record["id"]: record for record in load_collection("problems.ndjson")
    }
    answers = {
        record["id"]: record for record in load_collection("answers.ndjson")
    }
    rubrics = {
        record["id"]: record for record in load_collection("rubrics.ndjson")
    }

    d4_evidence = " ".join([
        *[objective["statement"] for objective in planned["D4"]["learning_objectives"]],
        *planned["D4"]["key_concepts"],
        problems["prob.info1.data.lifecycle.002.v1"]["question"],
        answers["ans.prob.info1.data.lifecycle.002.v1"]["canonical_answer"],
    ]).lower()
    for term in (
        "qualitative", "quantitative", "nominal", "ordinal", "interval", "ratio",
        "名義", "順序", "間隔", "比例",
    ):
        assert term in d4_evidence
    assert "観測idの平均" in d4_evidence
    assert "2倍暖かい" in d4_evidence
    d4_o1_coverage = next(
        coverage for coverage in planned["D4"]["assessment_coverage"]
        if coverage["objective_ref"] == "obj.info1.data.lifecycle.001.v1"
    )
    assert "prob.info1.data.lifecycle.002.v1" in d4_o1_coverage[
        "assessment_item_refs"
    ]

    d5_path = (
        ROOT / "lessons" / "highschool_information_i" / "networks_data"
        / "04_tabular_cleaning.md"
    )
    d6_path = (
        ROOT / "lessons" / "highschool_information_i" / "networks_data"
        / "05_descriptive_analysis.md"
    )
    d5_text = d5_path.read_text(encoding="utf-8")
    d6_text = d6_path.read_text(encoding="utf-8")
    for marker in ("分かち書き済み", "読み取り専用", "除外語一覧", "文脈"):
        assert marker in d5_text
    assert "実在する生徒のコメントを入力・共有させません" in d5_text
    assert "| 図書室 | 1 | 0 | 1 | 0 | 2 |" in d6_text
    assert "頻度は重要度と同じではありません" in d6_text
    assert "Pythonを使わず" in d6_text

    d9_problem = problems["prob.info1.data.investigation.project.004.v1"]
    d9_answer = answers["ans.prob.info1.data.investigation.project.004.v1"]
    d9_rubric = rubrics["rubric.prob.info1.data.investigation.project.004.v1"]
    d9_evidence = " ".join([
        d9_problem["question"],
        d9_answer["canonical_answer"],
        *[criterion["description"] for criterion in d9_rubric["criteria"]],
    ])
    for term in (
        "出所", "データ辞書", "読み取り専用", "変換履歴", "再実行", "照合",
        "本文要約", "結論", "感度分析", "実結果", "限界", "残余リスク",
        "改善案", "発表", "改訂履歴",
    ):
        assert term in d9_evidence
    assert "2件から3件" in d9_answer["canonical_answer"]
    assert {criterion["id"] for criterion in d9_rubric["criteria"]} == {
        "c1_question_ethics",
        "c2_reproducible_workflow",
        "c3_accessible_evidence",
        "c4_bounded_conclusion",
        "c5_limits_improvement",
        "c6_provenance_dictionary",
        "c7_transformation_log",
        "c8_independent_check",
        "c9_sensitivity_results",
        "c10_presentation_revision",
    }
    assert sum(criterion["points"] for criterion in d9_rubric["criteria"]) == 10

    changed_answer_ids = {
        "ans.prob.info1.data.lifecycle.002.v1",
        "ans.prob.info1.data.cleaning.004.v1",
        "ans.prob.info1.data.descriptive.analysis.004.v1",
        "ans.prob.info1.data.investigation.project.004.v1",
    }
    for answer_id in changed_answer_ids:
        answer = answers[answer_id]
        assert answer["revision"] == 2
        assert answer["status"] == "draft"
        assert answer["review_status"] == "needs_human_review"


def test_curriculum_sources_and_existing_lessons_resolve() -> None:
    curriculum = load_curriculum()
    source_ids = load_collection_ids("sources.ndjson")
    canonical_lessons = {
        record["id"]: record
        for record in load_collection("lessons.ndjson")
    }
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

    assert canonical_lessons.keys() <= planned_lessons.keys()
    for lesson_id, canonical in canonical_lessons.items():
        assert planned_lessons[lesson_id]["status"] == canonical["status"]
