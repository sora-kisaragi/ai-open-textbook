#!/usr/bin/env python3
"""Tests for the content-depth structural audit."""
from __future__ import annotations

import json
from pathlib import Path

from scripts import audit_lesson_depth


ROOT = Path(__file__).resolve().parents[1]


def test_report_covers_all_lessons_and_limits_errors_to_strict_pilots() -> None:
    report = audit_lesson_depth.audit_repository(ROOT)

    assert report["summary"]["lesson_count"] == 32
    assert report["summary"]["pilot_count"] == 4
    assert [item["order"] for item in report["lessons"]] == [
        *(f"A{index}" for index in range(1, 8)),
        *(f"B{index}" for index in range(1, 8)),
        *(f"C{index}" for index in range(1, 10)),
        *(f"D{index}" for index in range(1, 10)),
    ]
    error_orders = {
        lesson["order"]
        for lesson in report["lessons"]
        if any(finding["severity"] == "error" for finding in lesson["findings"])
    }
    assert error_orders <= audit_lesson_depth.PILOT_ORDERS
    assert report["summary"]["error_count"] == 0
    assert all(len(lesson["checks"]) == 21 for lesson in report["lessons"])
    assert "human review remains required" in report["decision_scope"]


def test_report_only_downgrades_all_missing_evidence_to_warnings(tmp_path: Path) -> None:
    output = tmp_path / "depth-report.json"

    result = audit_lesson_depth.main([
        "--root", str(ROOT),
        "--format", "json",
        "--output", str(output),
        "--report-only",
    ])
    report = json.loads(output.read_text(encoding="utf-8"))

    assert result == 0
    assert report["strict_pilots"] is False
    assert report["summary"]["error_count"] == 0
    assert all(
        finding["severity"] == "warning"
        for lesson in report["lessons"]
        for finding in lesson["findings"]
    )


def test_heading_evidence_requires_substantive_section_body() -> None:
    insufficient_bodies = (
        "",
        "![Only a figure](figure:example.svg)",
        "x",
        "TODO",
        "Placeholder",
    )
    for body in insufficient_bodies:
        assert audit_lesson_depth.heading_evidence(
            f"## Worked example\n\n{body}\n",
            ("worked example",),
        ) == []
    assert audit_lesson_depth.heading_evidence(
        "## Worked example\n\n"
        "The learner traces each decision, records the changing state, compares the "
        "observed result with the expected result, and explains why the evidence supports "
        "the conclusion.\n",
        ("worked example",),
    ) == ["Worked example"]


def test_heading_evidence_rejects_title_middle_match_and_nested_only_content() -> None:
    assert audit_lesson_depth.heading_evidence(
        "# Data visualization and misconception risks\n\n"
        "This title must not serve as a misconception section even when the document "
        "contains enough prose to exceed the minimum evidence threshold.\n",
        ("misconception",),
    ) == []
    assert audit_lesson_depth.heading_evidence(
        "## Review\n\n### Mastery decision\n\n"
        "The learner cites two independent pieces of evidence before choosing the next route.\n",
        ("review",),
    ) == []
    assert audit_lesson_depth.heading_evidence(
        "## Chart and misconception review\n\n"
        "The learner identifies a claim, compares it with the source data, and records why "
        "the display cannot support the conclusion.\n",
        ("misconception",),
    ) == []


def test_remediation_heading_does_not_count_as_mastery() -> None:
    text = (
        "## Review and retry\n\n"
        "The learner returns to the worked example, repairs the missing relationship, and "
        "tries the guided item again before moving forward.\n"
    )
    assert audit_lesson_depth.heading_evidence(text, ("review", "retry")) == ["Review and retry"]
    assert audit_lesson_depth.heading_evidence(text, ("mastery", "exit")) == []


def test_concept_model_does_not_pass_from_figure_alone(tmp_path: Path) -> None:
    body_ref = "lessons/pilot.md"
    body = tmp_path / body_ref
    body.parent.mkdir(parents=True)
    body.write_text(
        "# Pilot\n\n## Concept model\n\n![Concept diagram](figure:concept.svg)\n",
        encoding="utf-8",
    )

    checks = audit_lesson_depth.lesson_checks(
        tmp_path,
        {"learning_objectives": [{"id": "obj.pilot.v1"}], "source_refs": []},
        {"body_ref": body_ref},
        [],
        {},
    )

    concept = next(check for check in checks if check["key"] == "concept_model")
    assert concept["present"] is False
    assert "1 figure reference(s)" in concept["evidence"]

    body.write_text(
        "# Pilot\n\n## Concept model\n\n"
        "The model separates state, transformation, and observable output.\n\n"
        "![Concept diagram](figure:concept.svg)\n",
        encoding="utf-8",
    )
    checks = audit_lesson_depth.lesson_checks(
        tmp_path,
        {"learning_objectives": [{"id": "obj.pilot.v1"}], "source_refs": []},
        {"body_ref": body_ref},
        [],
        {},
    )

    assert next(check for check in checks if check["key"] == "concept_model")["present"] is True


def test_claim_review_requires_six_field_ledger(tmp_path: Path) -> None:
    generic = (
        "## Source\n\n"
        "This generic source note has enough prose to pass the normal substantive-section threshold.\n"
    )
    assert audit_lesson_depth.claim_ledger_evidence(generic) == []

    incomplete = (
        "## Claim Review Ledger\n\n"
        "| Claim locator | Evidence | Check |\n"
        "| --- | --- | --- |\n"
        "| lesson.example.v1 | src.example.v1, section 1 | supported |\n"
    )
    assert audit_lesson_depth.claim_ledger_evidence(incomplete) == []

    complete = (
        "## Claim Review Ledger\n\n"
        "| Claim locator | Exact claim | Claim type | Evidence | Check | Scope note |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| `lesson.example.v1` / model | The bounded model has two states. | factual | "
        "`src.example.v1`, section 1 | 2026-07-23, reviewer, supported | "
        "Synthetic classroom case only; no external behavior is inferred. |\n"
    )
    assert audit_lesson_depth.claim_ledger_evidence(complete) == ["Claim Review Ledger"]
    assert audit_lesson_depth.claim_ledger_evidence(
        complete,
        {"src.example.v1"},
        "lesson.example.v1",
    ) == ["Claim Review Ledger"]
    assert audit_lesson_depth.claim_ledger_evidence(
        complete,
        {"src.example.v1"},
        "lesson.other.v1",
    ) == []
    assert audit_lesson_depth.claim_ledger_evidence(
        complete,
        {"src.other.v1"},
    ) == []

    assert audit_lesson_depth.claim_ledger_evidence(
        complete.replace("factual", "unsupported type")
    ) == []
    assert audit_lesson_depth.claim_ledger_evidence(
        complete.replace(", supported", "")
    ) == []
    mixed_rows = complete.replace(
        "Synthetic classroom case only; no external behavior is inferred. |\n",
        "Synthetic classroom case only; no external behavior is inferred. |\n"
        "| invalid locator | Another bounded claim with enough substantive content. | factual | "
        "not-a-source | 2026-07-23, reviewer, supported | "
        "Synthetic classroom case only; no external behavior is inferred. |\n",
    )
    assert audit_lesson_depth.claim_ledger_evidence(mixed_rows) == []
