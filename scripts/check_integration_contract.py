#!/usr/bin/env python3
"""Check the Information I integration contract for Issue 81."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = Path("curriculum/highschool_information_i.curriculum.json")
AUDIT_PATH = Path("docs/review/INFORMATION_I_COVERAGE_AUDIT.md")
TRANSFER_HEADING = "## 別の場面への転移"
SCHEDULE_HEADING = "## 50分授業の到達点と判断"
SCHEDULE_COLUMNS = ["時限", "学習者の到達点", "50分の区切り", "続行条件"]
DETERMINISTIC_QUESTION_TYPES = {"predict_output"}
REVIEWED_EXECUTABLE_EXEMPLARS = {
    "ans.prob.info1.programming.functions.004.v1",
    "ans.prob.info1.programming.modeling.simulation.003.v1",
    "ans.prob.info1.programming.modeling.simulation.004.v1",
    "ans.prob.info1.programming.project.002.v1",
    "ans.prob.info1.programming.project.003.v1",
    "ans.prob.info1.programming.project.004.v1",
    "ans.prob.info1.conditionals.008.v1",
    "ans.prob.info1.loops.008.v1",
}


@dataclass(frozen=True)
class IntegrationStats:
    lessons: int
    transfer_probes: int
    scheduled_periods: int
    coverage_rows: int
    machine_checked_answers: int


def load_ndjson(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def section(markdown: str, heading: str) -> str | None:
    marker = f"{heading}\n"
    if markdown.count(marker) != 1:
        return None
    body = markdown.split(marker, 1)[1]
    return re.split(r"(?m)^## ", body, maxsplit=1)[0].strip()


def table_rows(markdown_section: str) -> tuple[list[str], list[list[str]]]:
    lines = [line.strip() for line in markdown_section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    cells = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
    return cells[0], cells[2:]


def check_repository(root: Path = DEFAULT_ROOT) -> tuple[list[str], IntegrationStats]:
    failures: list[str] = []
    curriculum = json.loads((root / CURRICULUM_PATH).read_text(encoding="utf-8"))
    lesson_records = {
        record["id"]: record
        for record in load_ndjson(root / "data/collections/lessons.ndjson")
    }
    problems = {
        record["id"]: record
        for record in load_ndjson(root / "data/collections/problems.ndjson")
    }
    answers = load_ndjson(root / "data/collections/answers.ndjson")

    lesson_plans = [lesson for unit in curriculum["units"] for lesson in unit["lessons"]]
    transfer_count = 0
    scheduled_periods = 0
    coverage_rows = 0

    if len(lesson_plans) != 32:
        failures.append(f"expected 32 curriculum lessons, found {len(lesson_plans)}")

    mandatory_total = curriculum["classroom_route"]["mandatory_periods"]
    for unit in curriculum["units"]:
        unit_minimum = sum(
            lesson["instructional_time"]["class_periods_50_min"][0]
            for lesson in unit["lessons"]
        )
        share = unit_minimum / mandatory_total
        if not 0.15 <= share <= 0.35:
            failures.append(
                f"{unit['id']}: mandatory period share {share:.1%} is outside 15%-35%"
            )
        projects = [
            lesson for lesson in unit["lessons"]
            if lesson["instructional_time"]["is_multi_session_project"]
        ]
        if len(projects) != 1:
            failures.append(f"{unit['id']}: expected one multi-session performance project")

    for plan in lesson_plans:
        record = lesson_records[plan["lesson_id"]]
        learner_path = root / record["body_ref"]
        teacher_path = root / record["body_ref"].replace("lessons/", "teacher_guides/", 1)

        learner_text = learner_path.read_text(encoding="utf-8")
        transfer = section(learner_text, TRANSFER_HEADING)
        if transfer is None:
            failures.append(f"{learner_path.relative_to(root)}: expected one transfer section")
        elif len(transfer) < 40:
            failures.append(f"{learner_path.relative_to(root)}: transfer probe is too short")
        elif "```python" in transfer:
            failures.append(f"{learner_path.relative_to(root)}: transfer probe depends on Python syntax")
        else:
            transfer_count += 1

        teacher_text = teacher_path.read_text(encoding="utf-8")
        schedule = section(teacher_text, SCHEDULE_HEADING)
        if schedule is None:
            failures.append(f"{teacher_path.relative_to(root)}: expected one schedule section")
            continue
        headers, rows = table_rows(schedule)
        minimum = plan["instructional_time"]["class_periods_50_min"][0]
        if headers != SCHEDULE_COLUMNS:
            failures.append(f"{teacher_path.relative_to(root)}: schedule headers do not match contract")
        if len(rows) != minimum:
            failures.append(
                f"{teacher_path.relative_to(root)}: expected {minimum} schedule rows, found {len(rows)}"
            )
        for index, row in enumerate(rows, 1):
            if len(row) != 4 or row[0] != f"第{index}時" or any(len(cell) < 4 for cell in row[1:]):
                failures.append(f"{teacher_path.relative_to(root)}: invalid schedule row {index}")
        scheduled_periods += len(rows)

        for coverage in plan["assessment_coverage"]:
            coverage_rows += 1
            if coverage["status"] == "complete" and not (
                len(coverage["assessment_item_refs"]) >= 2
                or (
                    coverage["assessment_item_refs"]
                    and coverage["performance_criterion_refs"]
                )
            ):
                failures.append(f"{coverage['objective_ref']}: unsupported complete coverage")

    if coverage_rows != 96:
        failures.append(f"expected 96 coverage rows, found {coverage_rows}")

    audit_text = (root / AUDIT_PATH).read_text(encoding="utf-8")
    audit_verdicts = len(re.findall(r"\| (?:Supported|Partial|Not started) (?=\|)", audit_text))
    if audit_verdicts != coverage_rows:
        failures.append(
            f"coverage audit records {audit_verdicts} objective verdicts, expected {coverage_rows}"
        )
    for plan in lesson_plans:
        if f"| {plan['order']} " not in audit_text:
            failures.append(f"coverage audit is missing lesson {plan['order']}")
    if scheduled_periods != mandatory_total:
        failures.append(
            f"teacher schedules cover {scheduled_periods} periods, expected {mandatory_total}"
        )

    machine_checked = 0
    for answer in answers:
        problem = problems[answer["problem_id"]]
        intrinsically_deterministic = (
            answer["answer_type"] == "code"
            or problem["question_type"] in DETERMINISTIC_QUESTION_TYPES
        )
        reviewed_exemplar = answer["id"] in REVIEWED_EXECUTABLE_EXEMPLARS
        claims_machine_check = answer.get("verification_status") == "machine_checked"
        if (intrinsically_deterministic or reviewed_exemplar) and not claims_machine_check:
            failures.append(f"{answer['id']}: deterministic answer is not machine_checked")
        if answer.get("verification_status") not in (None, "machine_checked"):
            failures.append(f"{answer['id']}: unknown verification_status")
        if claims_machine_check and not (intrinsically_deterministic or reviewed_exemplar):
            failures.append(f"{answer['id']}: qualitative answer has an unreviewed machine_checked claim")
        if claims_machine_check:
            machine_checked += 1
            evidence = answer.get("verification_evidence", [])
            if not evidence or any(item.get("result") != "passed" for item in evidence):
                failures.append(f"{answer['id']}: machine_checked answer lacks passing evidence")
            if any(not item.get("command") or not item.get("expected") for item in evidence):
                failures.append(f"{answer['id']}: verification evidence lacks command or expectation")

    stats = IntegrationStats(
        lessons=len(lesson_plans),
        transfer_probes=transfer_count,
        scheduled_periods=scheduled_periods,
        coverage_rows=coverage_rows,
        machine_checked_answers=machine_checked,
    )
    return failures, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    failures, stats = check_repository(args.root.resolve())
    for failure in failures:
        print(f"ERROR: {failure}")
    if failures:
        print(f"Integration contract failed with {len(failures)} error(s).")
        return 1
    print(
        "Integration contract passed: "
        f"{stats.lessons} lessons, {stats.transfer_probes} transfer probes, "
        f"{stats.scheduled_periods} scheduled periods, {stats.coverage_rows} coverage rows, "
        f"{stats.machine_checked_answers} machine-checked answers."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
