#!/usr/bin/env python3
"""Build an offline static textbook site from canonical Markdown and NDJSON."""
from __future__ import annotations

import argparse
from collections import Counter
import html
import json
import os
import re
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from string import Template

from markdown_it import MarkdownIt


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_FILE = Path("curriculum/highschool_information_i.curriculum.json")
COLLECTION_FILES = (
    "lessons.ndjson",
    "problems.ndjson",
    "answers.ndjson",
    "rubrics.ndjson",
    "sources.ndjson",
    "revisions.ndjson",
)
DIFFICULTY_ORDER = {"basic": 0, "standard": 1, "advanced": 2}
ACTIVITY_PAGES = (
    Path("activities/b7_keyboard_start.html"),
    Path("activities/b7_keyboard_confirm.html"),
    Path("activities/b7_keyboard_complete.html"),
)


class SiteBuildError(RuntimeError):
    """Raised for a clear, user-facing static-site build failure."""


@dataclass(frozen=True)
class CurriculumPosition:
    """Ordered curriculum metadata for one canonical lesson."""

    unit_id: str
    unit_title: str
    unit_index: int
    lesson_index: int
    order: str
    curriculum_title: str
    objective_ids: frozenset[str]


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def markdown_renderer() -> MarkdownIt:
    renderer = MarkdownIt(
        "commonmark",
        {
            "html": False,
            "linkify": False,
            "typographer": False,
        },
    ).enable("table")

    def table_open(_renderer, _tokens, _index, _options, _env) -> str:
        return '<div class="table-wrap"><table>\n'

    def table_close(_renderer, _tokens, _index, _options, _env) -> str:
        return "</table></div>\n"

    renderer.add_render_rule("table_open", table_open)
    renderer.add_render_rule("table_close", table_close)
    return renderer


def load_records(root: Path) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    collections = root / "data" / "collections"
    by_id: dict[str, dict] = {}
    by_type: dict[str, list[dict]] = {}

    for filename in COLLECTION_FILES:
        path = collections / filename
        if not path.exists():
            raise SiteBuildError(f"missing collection: {path.relative_to(root)}")
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SiteBuildError(f"{path.relative_to(root)}:{line_no}: invalid JSON: {exc}") from exc
            record_id = record.get("id")
            if not isinstance(record_id, str) or not record_id:
                raise SiteBuildError(f"{path.relative_to(root)}:{line_no}: missing record id")
            if record_id in by_id:
                raise SiteBuildError(f"duplicate id: {record_id}")
            by_id[record_id] = record
            by_type.setdefault(str(record.get("type")), []).append(record)

    return by_id, by_type


def load_curriculum(root: Path) -> dict[str, CurriculumPosition]:
    curriculum = load_curriculum_document(root)
    units = curriculum.get("units")
    if not isinstance(units, list) or not units:
        raise SiteBuildError("curriculum must contain a non-empty units list")

    positions: dict[str, CurriculumPosition] = {}
    objective_owners: dict[str, str] = {}
    for unit_index, unit in enumerate(units):
        if not isinstance(unit, dict):
            raise SiteBuildError(f"curriculum units[{unit_index}] must be an object")
        unit_id = unit.get("id")
        unit_title = unit.get("title")
        planned_lessons = unit.get("lessons")
        if not isinstance(unit_id, str) or not isinstance(unit_title, str):
            raise SiteBuildError(f"curriculum units[{unit_index}] is missing id or title")
        if not isinstance(planned_lessons, list) or not planned_lessons:
            raise SiteBuildError(f"curriculum unit has no lessons: {unit_id}")

        for lesson_index, planned in enumerate(planned_lessons):
            if not isinstance(planned, dict):
                raise SiteBuildError(f"curriculum lesson in {unit_id} must be an object")
            lesson_id = planned.get("lesson_id")
            order = planned.get("order")
            title = planned.get("title")
            objectives = planned.get("learning_objectives")
            if not all(isinstance(value, str) and value for value in (lesson_id, order, title)):
                raise SiteBuildError(f"curriculum lesson in {unit_id} is missing lesson_id, order, or title")
            if lesson_id in positions:
                raise SiteBuildError(f"duplicate curriculum lesson id: {lesson_id}")
            if not isinstance(objectives, list) or not objectives:
                raise SiteBuildError(f"curriculum lesson has no learning objectives: {lesson_id}")

            objective_ids: set[str] = set()
            for objective in objectives:
                objective_id = objective.get("id") if isinstance(objective, dict) else None
                if not isinstance(objective_id, str) or not objective_id:
                    raise SiteBuildError(f"curriculum lesson has an invalid objective: {lesson_id}")
                if objective_id in objective_owners:
                    raise SiteBuildError(f"duplicate curriculum objective id: {objective_id}")
                objective_owners[objective_id] = lesson_id
                objective_ids.add(objective_id)

            positions[lesson_id] = CurriculumPosition(
                unit_id=unit_id,
                unit_title=unit_title,
                unit_index=unit_index,
                lesson_index=lesson_index,
                order=order,
                curriculum_title=title,
                objective_ids=frozenset(objective_ids),
            )

    return positions


def load_curriculum_document(root: Path) -> dict:
    path = root / CURRICULUM_FILE
    if not path.is_file():
        raise SiteBuildError(f"missing curriculum: {CURRICULUM_FILE.as_posix()}")
    try:
        curriculum = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SiteBuildError(f"{CURRICULUM_FILE.as_posix()}: invalid JSON: {exc}") from exc

    if not isinstance(curriculum, dict):
        raise SiteBuildError("curriculum root must be an object")
    return curriculum


def repository_path(root: Path, relative: object, field: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise SiteBuildError(f"missing {field}")
    root_resolved = root.resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root_resolved):
        raise SiteBuildError(f"{field} escapes repository root: {relative}")
    return path


def require_reference(by_id: dict[str, dict], ref: object, expected_type: str, field: str) -> dict:
    if not isinstance(ref, str) or ref not in by_id:
        raise SiteBuildError(f"broken reference in {field}: {ref}")
    record = by_id[ref]
    if record.get("type") != expected_type:
        raise SiteBuildError(f"{field} must reference {expected_type}: {ref}")
    return record


def validate_graph(
    root: Path,
    by_id: dict[str, dict],
    by_type: dict[str, list[dict]],
    curriculum: dict[str, CurriculumPosition],
) -> None:
    lessons = by_type.get("lesson", [])
    if not lessons:
        raise SiteBuildError("no lesson records found")

    for lesson in lessons:
        lesson_id = str(lesson["id"])
        if lesson_id not in curriculum:
            raise SiteBuildError(f"lesson is not present in curriculum: {lesson_id}")
        body = repository_path(root, lesson.get("body_ref"), "body_ref")
        if not body.is_file():
            raise SiteBuildError(f"missing body_ref file: {lesson.get('body_ref')}")
        body_ref = Path(str(lesson["body_ref"]))
        if not body_ref.parts or body_ref.parts[0] != "lessons":
            raise SiteBuildError(f"lesson body_ref must be under lessons/: {body_ref.as_posix()}")
        teacher_ref = Path("teacher_guides", *body_ref.parts[1:])
        teacher = repository_path(root, teacher_ref.as_posix(), "teacher guide")
        if not teacher.is_file():
            raise SiteBuildError(f"missing teacher guide: {teacher_ref.as_posix()}")

    for problem in by_type.get("problem", []):
        lesson_refs = problem.get("lesson_refs", []) or []
        for ref in lesson_refs:
            require_reference(by_id, ref, "lesson", "lesson_refs")
        objective_refs = problem.get("objective_refs", []) or []
        if not objective_refs:
            raise SiteBuildError(f"problem has no objective_refs: {problem.get('id')}")
        allowed_objectives = {
            objective_id
            for lesson_ref in lesson_refs
            for objective_id in curriculum[str(lesson_ref)].objective_ids
        }
        for ref in objective_refs:
            if not isinstance(ref, str) or ref not in allowed_objectives:
                raise SiteBuildError(
                    f"objective_refs must belong to a referenced curriculum lesson: {ref}"
                )
        for ref in problem.get("answer_refs", []) or []:
            require_reference(by_id, ref, "answer", "answer_refs")
        for ref in problem.get("rubric_refs", []) or []:
            require_reference(by_id, ref, "rubric", "rubric_refs")

    for answer in by_type.get("answer", []):
        require_reference(by_id, answer.get("problem_id"), "problem", "problem_id")
    for rubric in by_type.get("rubric", []):
        require_reference(by_id, rubric.get("problem_id"), "problem", "problem_id")


def render_template(root: Path, name: str, values: dict[str, str]) -> str:
    path = root / "site" / "templates" / name
    if not path.is_file():
        raise SiteBuildError(f"missing site template: {path.relative_to(root)}")
    try:
        return Template(path.read_text(encoding="utf-8")).substitute(values)
    except KeyError as exc:
        raise SiteBuildError(f"missing template value {exc.args[0]!r} for {name}") from exc


def render_without_practice_ids(md: MarkdownIt, source: str) -> str:
    tokens = md.parse(source)
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or token.tag != "h2":
            continue
        if index + 1 < len(tokens) and tokens[index + 1].type == "inline":
            if tokens[index + 1].content.strip() == "練習":
                return md.renderer.render(tokens[:index], md.options, {})
    return md.renderer.render(tokens, md.options, {})


def render_without_leading_h1(md: MarkdownIt, source: str) -> str:
    tokens = md.parse(source)
    if len(tokens) >= 3 and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
        tokens = tokens[3:]
    return md.renderer.render(tokens, md.options, {})


def render_source_context(lesson: dict, by_id: dict[str, dict]) -> str:
    items: list[str] = []
    for source_ref in lesson.get("source_refs", []) or []:
        source = require_reference(by_id, source_ref, "source", "source_refs")
        accessed_at = source.get("accessed_at")
        accessed_html = (
            f'<span><strong>確認日:</strong> {escape(accessed_at)}</span>'
            if accessed_at
            else ""
        )
        notes = source.get("notes")
        notes_html = f'<p class="source-context-note">{escape(notes)}</p>' if notes else ""
        items.append(
            "<li>"
            f'<a href="{escape(source.get("url", ""))}">'
            f'<strong>{escape(source.get("title", source_ref))}</strong></a>'
            '<p class="source-context-meta">'
            f'<span><strong>種別:</strong> {escape(source.get("source_type", ""))}</span>'
            f"{accessed_html}</p>{notes_html}</li>"
        )

    source_list = f'<ul class="source-context-list">{"".join(items)}</ul>' if items else "<p>参照出典はありません。</p>"
    return (
        '<p class="source-scope-note">ここに示す出典は、一般的な教育課程上の位置付けや技術事項を確認するための参照です。'
        "各レッスンの学習目標、順序、例、時間配分、問題、評価方法は本プロジェクトが作成したドラフトであり、"
        "文部科学省が定めた表現や授業案ではありません。</p>"
        f"{source_list}"
    )


def render_source_bibliography(sources: list[dict]) -> str:
    active_sources = sorted(
        (source for source in sources if source.get("status") not in {"deprecated", "superseded"}),
        key=lambda source: (str(source.get("issuer", "")), str(source.get("title", "")), str(source.get("id", ""))),
    )
    if not active_sources:
        return '<p class="muted">参照出典はありません。</p><ol class="source-bibliography"></ol>'

    items: list[str] = []
    for source in active_sources:
        metadata = []
        if source.get("issuer"):
            metadata.append(f'<span><strong>発行:</strong> {escape(source["issuer"])}</span>')
        if source.get("publication_date"):
            metadata.append(f'<span><strong>公開:</strong> {escape(source["publication_date"])}</span>')
        if source.get("accessed_at"):
            metadata.append(f'<span><strong>確認:</strong> {escape(source["accessed_at"])}</span>')
        items.append(
            '<li class="source-bibliography-item"><a href="{}"><strong>{}</strong></a>'
            '<p class="source-context-meta">{}</p></li>'.format(
                escape(source.get("url", "")),
                escape(source.get("title", source.get("id", ""))),
                "".join(metadata),
            )
        )
    return f'<ol class="source-bibliography">{"".join(items)}</ol>'


def slug_for_lesson(lesson: dict) -> str:
    lesson_id = str(lesson.get("id", ""))
    parts = lesson_id.split(".")
    if len(parts) < 4 or parts[0] != "lesson" or not re.fullmatch(r"v[1-9][0-9]*", parts[-1]):
        raise SiteBuildError(f"cannot derive semantic slug from lesson id: {lesson_id}")
    semantic_parts = parts[2:-1]
    if not semantic_parts or any(not re.fullmatch(r"[a-z0-9]+", part) for part in semantic_parts):
        raise SiteBuildError(f"cannot derive semantic slug from lesson id: {lesson_id}")
    return "-".join(semantic_parts)


def render_list(items: list[object], css_class: str = "detail-list") -> str:
    if not items:
        return '<p class="muted">なし</p>'
    return f'<ul class="{css_class}">' + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def render_practices(md: MarkdownIt, problems: list[dict], id_prefix: str = "practice") -> str:
    blocks = []
    for number, problem in enumerate(problems, start=1):
        question = md.render(str(problem.get("question", "")))
        section_id = f"{id_prefix}-{number}"
        blocks.append(
            '<section class="practice-item" aria-labelledby="{}">'
            '<p class="section-kicker">練習 {}</p>'
            '<h3 id="{}">自分で考えてみよう</h3>{}'
            '<div class="answer-space" aria-hidden="true"></div>'
            "</section>".format(section_id, number, section_id, question)
        )
    return "".join(blocks)


def render_canonical_answer(md: MarkdownIt, answer: dict) -> str:
    canonical = str(answer.get("canonical_answer", ""))
    if answer.get("answer_type") == "text":
        return f'<div class="canonical-answer canonical-answer-prose">{md.render(canonical)}</div>'
    return f'<pre class="canonical-answer canonical-answer-code"><code>{escape(canonical)}</code></pre>'


def render_self_study_practices(
    md: MarkdownIt,
    problems: list[dict],
    by_id: dict[str, dict],
    id_prefix: str = "self-study-practice",
) -> str:
    blocks = []
    for number, problem in enumerate(problems, start=1):
        question = md.render(str(problem.get("question", "")))
        section_id = f"{id_prefix}-{number}"
        answer_reveals = []
        for answer in (
            require_reference(by_id, ref, "answer", "answer_refs")
            for ref in problem.get("answer_refs", []) or []
        ):
            acceptable = answer.get("acceptable_answers", []) or []
            acceptable_html = ""
            if acceptable:
                acceptable_html = (
                    "<h4>別の解答例</h4>"
                    + render_list(acceptable, css_class="acceptable-answer-list")
                )
            explanation = md.render(str(answer.get("explanation", "")))
            mistakes = problem.get("common_mistakes", []) or []
            mistakes_html = ""
            if mistakes:
                mistakes_html = (
                    "<h4>確認したい点</h4>"
                    + render_list(mistakes, css_class="common-mistake-list")
                )
            answer_reveals.append(
                '<details class="answer-reveal">'
                "<summary>解答例と解説を確認</summary>"
                '<div class="answer-feedback">'
                "<h4>解答例</h4>"
                f'{render_canonical_answer(md, answer)}'
                f"{acceptable_html}"
                "<h4>解説</h4>"
                f'<div class="answer-explanation">{explanation}</div>'
                f"{mistakes_html}"
                "</div></details>"
            )
        blocks.append(
            '<section class="practice-item self-study-practice" aria-labelledby="{}">'
            '<p class="section-kicker">練習 {}</p>'
            '<h3 id="{}">自分で考えてみよう</h3>{}{}'
            "</section>".format(
                section_id,
                number,
                section_id,
                question,
                "".join(answer_reveals),
            )
        )
    return "".join(blocks)


def instructional_range(lesson: dict, field: str) -> tuple[int, int]:
    value = lesson.get("instructional_time", {}).get(field, [0, 0])
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(not isinstance(item, int) or isinstance(item, bool) or item < 0 for item in value)
    ):
        return 0, 0
    return value[0], value[1]


def build_semantic_coverage_report(
    curriculum_document: dict,
    by_type: dict[str, list[dict]],
) -> dict:
    problems = by_type.get("problem", [])
    rubrics = by_type.get("rubric", [])
    problems_by_objective: dict[str, set[str]] = {}
    for problem in problems:
        for objective_ref in problem.get("objective_refs", []) or []:
            problems_by_objective.setdefault(str(objective_ref), set()).add(str(problem["id"]))

    rubric_criteria: dict[str, tuple[str, set[str]]] = {}
    for rubric in rubrics:
        problem_id = str(rubric.get("problem_id", ""))
        rubric_criteria[str(rubric.get("id", ""))] = (
            problem_id,
            {
                str(criterion["id"])
                for criterion in rubric.get("criteria", []) or []
                if isinstance(criterion, dict) and criterion.get("id")
            },
        )

    rows = []
    for unit in curriculum_document.get("units", []):
        for lesson in unit.get("lessons", []):
            coverage_by_objective = {
                str(item.get("objective_ref")): item
                for item in lesson.get("assessment_coverage", []) or []
                if isinstance(item, dict)
            }
            for objective in lesson.get("learning_objectives", []) or []:
                objective_id = str(objective.get("id", ""))
                coverage = coverage_by_objective.get(objective_id, {})
                linked_problem_refs = sorted(problems_by_objective.get(objective_id, set()))
                declared_problem_refs = sorted(
                    str(ref) for ref in coverage.get("assessment_item_refs", []) or []
                )
                valid_problem_refs = sorted(set(declared_problem_refs) & set(linked_problem_refs))
                declared_criterion_refs = sorted(
                    (
                        {
                            "rubric_ref": str(ref.get("rubric_ref", "")),
                            "criterion_id": str(ref.get("criterion_id", "")),
                        }
                        for ref in coverage.get("performance_criterion_refs", []) or []
                        if isinstance(ref, dict)
                    ),
                    key=lambda ref: (ref["rubric_ref"], ref["criterion_id"]),
                )
                valid_criterion_refs = [
                    ref
                    for ref in declared_criterion_refs
                    if ref["rubric_ref"] in rubric_criteria
                    and rubric_criteria[ref["rubric_ref"]][0] in linked_problem_refs
                    and ref["criterion_id"] in rubric_criteria[ref["rubric_ref"]][1]
                ]
                if len(valid_problem_refs) >= 2 or (
                    valid_problem_refs and valid_criterion_refs
                ):
                    support_level = "supported"
                elif valid_problem_refs or valid_criterion_refs:
                    support_level = "partial"
                else:
                    support_level = "unsupported"
                rows.append(
                    {
                        "objective_ref": objective_id,
                        "objective_label": objective.get("label"),
                        "objective_statement": objective.get("statement"),
                        "unit_ref": unit.get("id"),
                        "lesson_ref": lesson.get("lesson_id"),
                        "lesson_order": lesson.get("order"),
                        "declared_status": coverage.get("status", "missing"),
                        "requirement": coverage.get("requirement", "missing"),
                        "declared_assessment_item_refs": declared_problem_refs,
                        "linked_assessment_item_refs": linked_problem_refs,
                        "valid_declared_assessment_item_refs": valid_problem_refs,
                        "declared_performance_criterion_refs": declared_criterion_refs,
                        "valid_performance_criterion_refs": valid_criterion_refs,
                        "support_level": support_level,
                        "semantic_review_state": "needs_human_review",
                    }
                )

    counts = Counter(str(row["support_level"]) for row in rows)
    return {
        "schema_version": "1.0",
        "artifact": "semantic_coverage_audit",
        "source": CURRICULUM_FILE.as_posix(),
        "review_status": "needs_human_review",
        "method": (
            "Deterministic cross-record support audit. It checks declared objective-to-problem "
            "and performance-criterion links; human review is still required for semantic quality."
        ),
        "row_count": len(rows),
        "support_counts": {
            level: counts.get(level, 0) for level in ("supported", "partial", "unsupported")
        },
        "partial_objective_refs": [
            row["objective_ref"] for row in rows if row["support_level"] == "partial"
        ],
        "unsupported_objective_refs": [
            row["objective_ref"] for row in rows if row["support_level"] == "unsupported"
        ],
        "rows": rows,
    }


def build_unit_balance_report(curriculum_document: dict) -> dict:
    units = []
    for unit in curriculum_document.get("units", []):
        lessons = unit.get("lessons", []) or []
        class_ranges = [instructional_range(lesson, "class_periods_50_min") for lesson in lessons]
        study_ranges = [instructional_range(lesson, "self_study_minutes") for lesson in lessons]
        units.append(
            {
                "unit_ref": unit.get("id"),
                "title": unit.get("title"),
                "lesson_count": len(lessons),
                "mandatory_class_periods": sum(value[0] for value in class_ranges),
                "maximum_planned_class_periods": sum(value[1] for value in class_ranges),
                "self_study_minutes_min": sum(value[0] for value in study_ranges),
                "self_study_minutes_max": sum(value[1] for value in study_ranges),
            }
        )
    route = curriculum_document.get("classroom_route", {}) or {}
    return {
        "schema_version": "1.0",
        "artifact": "unit_balance_and_period_allocation",
        "source": CURRICULUM_FILE.as_posix(),
        "review_status": "needs_human_review",
        "period_minutes": route.get("period_minutes"),
        "mandatory_periods": route.get("mandatory_periods"),
        "recommended_extension_periods": route.get("recommended_extension_periods"),
        "recommended_total_periods": route.get("recommended_total_periods"),
        "calculated_mandatory_periods": sum(unit["mandatory_class_periods"] for unit in units),
        "calculated_maximum_planned_periods": sum(
            unit["maximum_planned_class_periods"] for unit in units
        ),
        "extension_allocations": route.get("extension_allocations", []),
        "units": units,
    }


def write_reports(destination: Path, curriculum_document: dict, by_type: dict[str, list[dict]]) -> None:
    reports = destination / "reports"
    reports.mkdir(parents=True)
    artifacts = {
        "semantic-coverage-audit.json": build_semantic_coverage_report(curriculum_document, by_type),
        "unit-balance-report.json": build_unit_balance_report(curriculum_document),
    }
    for filename, payload in artifacts.items():
        (reports / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def problem_instructional_order(problem: dict) -> tuple[int, str]:
    return (
        DIFFICULTY_ORDER.get(str(problem.get("difficulty", "")), len(DIFFICULTY_ORDER)),
        str(problem.get("id", "")),
    )


def render_verification(evidence: list[dict]) -> str:
    if not evidence:
        return '<p class="muted">No verification evidence.</p>'
    rows = []
    for item in evidence:
        rows.append(
            "<tr>"
            f"<td>{escape(item.get('method', ''))}</td>"
            f"<td><code>{escape(item.get('expected', ''))}</code></td>"
            f"<td>{escape(item.get('result', ''))}</td>"
            "</tr>"
        )
    return (
        '<div class="table-wrap"><table><thead><tr><th>Method</th><th>Expected</th><th>Result</th>'
        f"</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
    )


def render_review_problem(md: MarkdownIt, problem: dict, by_id: dict[str, dict]) -> str:
    answers = [require_reference(by_id, ref, "answer", "answer_refs") for ref in problem.get("answer_refs", [])]
    rubrics = [require_reference(by_id, ref, "rubric", "rubric_refs") for ref in problem.get("rubric_refs", [])]

    answer_sections = []
    for answer in answers:
        acceptable = render_list(answer.get("acceptable_answers", []) or [])
        answer_sections.append(
            '<section class="review-subsection">'
            "<h4>Answer</h4>"
            f'<p class="record-id"><code>{escape(answer["id"])}</code></p>'
            f'{render_canonical_answer(md, answer)}'
            f'<div class="teacher-copy">{md.render(str(answer.get("explanation", "")))}</div>'
            "<h5>Acceptable answers</h5>"
            f"{acceptable}"
            "<h5>Verification evidence</h5>"
            f'{render_verification(answer.get("verification_evidence", []) or [])}'
            "</section>"
        )

    rubric_sections = []
    for rubric in rubrics:
        criteria = "".join(
            "<li>"
            f'<span>{escape(item.get("description", ""))}</span>'
            f'<strong>{escape(item.get("points", 0))} pt</strong>'
            "</li>"
            for item in rubric.get("criteria", []) or []
        )
        rubric_sections.append(
            '<section class="review-subsection">'
            "<h4>Rubric</h4>"
            f'<p class="record-id"><code>{escape(rubric["id"])}</code></p>'
            f'<ul class="rubric-list">{criteria}</ul>'
            "</section>"
        )

    return (
        '<article class="review-record">'
        '<header class="review-record-header">'
        f'<div><p class="section-kicker">{escape(problem.get("question_type", "problem"))}</p>'
        f'<h3>{escape(problem["id"])}</h3></div>'
        f'<span class="status-badge">{escape(problem.get("status", ""))}</span>'
        "</header>"
        f'<div class="teacher-copy">{md.render(str(problem.get("question", "")))}</div>'
        "<h4>Common mistakes</h4>"
        f'{render_list(problem.get("common_mistakes", []) or [])}'
        f'{"".join(answer_sections)}'
        f'{"".join(rubric_sections)}'
        "</article>"
    )


def render_revisions(revisions: list[dict], entity_ids: set[str]) -> str:
    selected = sorted(
        (revision for revision in revisions if revision.get("entity_id") in entity_ids),
        key=lambda revision: str(revision.get("id", "")),
    )
    if not selected:
        return '<p class="muted">No revision records.</p>'
    return '<ol class="revision-list">' + "".join(
        "<li>"
        f'<code>{escape(item.get("id", ""))}</code>'
        f'<span>{escape(item.get("reason", ""))}</span>'
        "</li>"
        for item in selected
    ) + "</ol>"


def write_site(
    root: Path,
    destination: Path,
    by_id: dict[str, dict],
    by_type: dict[str, list[dict]],
    curriculum: dict[str, CurriculumPosition],
) -> None:
    md = markdown_renderer()
    assets = destination / "assets"
    lesson_dir = destination / "lessons"
    teacher_dir = destination / "teacher"
    self_study_dir = destination / "self-study"
    self_study_lesson_dir = self_study_dir / "lessons"
    assets.mkdir(parents=True)
    lesson_dir.mkdir(parents=True)
    teacher_dir.mkdir(parents=True)
    self_study_lesson_dir.mkdir(parents=True)

    stylesheet = root / "site" / "assets" / "styles.css"
    if not stylesheet.is_file():
        raise SiteBuildError(f"missing site asset: {stylesheet.relative_to(root)}")
    shutil.copyfile(stylesheet, assets / "styles.css")
    activities_source = root / "site" / "activities"
    if not activities_source.is_dir():
        raise SiteBuildError(f"missing site activities: {activities_source.relative_to(root)}")
    shutil.copytree(activities_source, destination / "activities")
    content_license = root / "LICENSE-CONTENT-CC-BY-4.0.md"
    if not content_license.is_file():
        raise SiteBuildError(f"missing content license: {content_license.relative_to(root)}")
    shutil.copyfile(content_license, destination / "LICENSE-CONTENT-CC-BY-4.0.txt")

    output_slugs: set[str] = set()
    lessons = sorted(
        by_type.get("lesson", []),
        key=lambda item: (
            curriculum[str(item["id"])].unit_index,
            curriculum[str(item["id"])].lesson_index,
        ),
    )
    problems = by_type.get("problem", [])
    revisions = by_type.get("revision", [])
    lesson_views: list[dict[str, object]] = []

    for lesson in lessons:
        lesson_id = str(lesson["id"])
        position = curriculum[lesson_id]
        linked_problems = sorted(
            (problem for problem in problems if lesson_id in (problem.get("lesson_refs", []) or [])),
            key=problem_instructional_order,
        )
        body_path = repository_path(root, lesson["body_ref"], "body_ref")
        body_source = body_path.read_text(encoding="utf-8")
        lesson_html = render_without_practice_ids(md, body_source)
        practice_html = render_practices(md, linked_problems)
        self_study_practice_html = render_self_study_practices(md, linked_problems, by_id)
        slug = slug_for_lesson(lesson)
        if slug in output_slugs:
            raise SiteBuildError(f"duplicate lesson output slug: {slug}")
        output_slugs.add(slug)
        page_title = str(lesson.get("title", ""))
        lesson_views.append(
            {
                "lesson": lesson,
                "position": position,
                "problems": linked_problems,
                "slug": slug,
                "page_title": page_title,
                "lesson_html": lesson_html,
                "practice_html": practice_html,
                "self_study_practice_html": self_study_practice_html,
            }
        )

    for index, view in enumerate(lesson_views):
        lesson = view["lesson"]
        position = view["position"]
        linked_problems = view["problems"]
        slug = str(view["slug"])
        page_title = str(view["page_title"])
        assert isinstance(lesson, dict)
        assert isinstance(position, CurriculumPosition)
        assert isinstance(linked_problems, list)

        def navigation_link(target_index: int, direction: str) -> str:
            if target_index < 0 or target_index >= len(lesson_views):
                return '<span class="lesson-nav-placeholder" aria-hidden="true"></span>'
            target = lesson_views[target_index]
            target_position = target["position"]
            assert isinstance(target_position, CurriculumPosition)
            label = "前のレッスン" if direction == "prev" else "次のレッスン"
            return (
                f'<a class="lesson-nav-link {direction}" rel="{direction}" '
                f'href="{escape(target["slug"])}.html">'
                f'<span>{label}</span><strong>{escape(target_position.order)} '
                f'{escape(target["page_title"])}</strong></a>'
            )

        learner_page = render_template(
            root,
            "learner.html",
            {
                "page_title": escape(page_title),
                "subject": escape(lesson.get("subject", "")),
                "unit": escape(lesson.get("unit", "")),
                "curriculum_order": escape(position.order),
                "lesson_html": str(view["lesson_html"]),
                "practice_html": str(view["practice_html"]),
                "previous_link": navigation_link(index - 1, "prev"),
                "next_link": navigation_link(index + 1, "next"),
            },
        )
        (lesson_dir / f"{slug}.html").write_text(learner_page, encoding="utf-8", newline="\n")

        self_study_page = render_template(
            root,
            "self-study-lesson.html",
            {
                "page_title": escape(page_title),
                "subject": escape(lesson.get("subject", "")),
                "unit": escape(lesson.get("unit", "")),
                "curriculum_order": escape(position.order),
                "lesson_html": str(view["lesson_html"]),
                "practice_html": str(view["self_study_practice_html"]),
                "previous_link": navigation_link(index - 1, "prev"),
                "next_link": navigation_link(index + 1, "next"),
            },
        )
        (self_study_lesson_dir / f"{slug}.html").write_text(
            self_study_page,
            encoding="utf-8",
            newline="\n",
        )

        lesson_id = str(lesson["id"])
        body_ref = Path(str(lesson["body_ref"]))
        teacher_ref = Path("teacher_guides", *body_ref.parts[1:])
        teacher_path = repository_path(root, teacher_ref.as_posix(), "teacher guide")
        teacher_html = render_without_leading_h1(md, teacher_path.read_text(encoding="utf-8"))
        review_html = "".join(render_review_problem(md, problem, by_id) for problem in linked_problems)
        entity_ids = {lesson_id}
        for problem in linked_problems:
            entity_ids.add(str(problem["id"]))
            entity_ids.update(problem.get("answer_refs", []) or [])
            entity_ids.update(problem.get("rubric_refs", []) or [])
        revision_html = render_revisions(revisions, entity_ids)
        source_context_html = render_source_context(lesson, by_id)
        teacher_page = render_template(
            root,
            "teacher.html",
            {
                "page_title": escape(page_title),
                "curriculum_order": escape(position.order),
                "unit": escape(lesson.get("unit", "")),
                "lesson_id": escape(lesson_id),
                "lesson_status": escape(lesson.get("status", "")),
                "learner_href": f"../lessons/{escape(slug)}.html",
                "teacher_guide_html": teacher_html,
                "review_html": review_html,
                "source_context_html": source_context_html,
                "revision_html": revision_html,
            },
        )
        (teacher_dir / f"{slug}.html").write_text(teacher_page, encoding="utf-8", newline="\n")

    unit_groups: list[list[dict[str, object]]] = []
    for view in lesson_views:
        position = view["position"]
        assert isinstance(position, CurriculumPosition)
        if not unit_groups or unit_groups[-1][0]["position"].unit_id != position.unit_id:
            unit_groups.append([])
        unit_groups[-1].append(view)

    index_units = []
    self_study_index_units = []
    teacher_units = []
    book_toc_units = []
    self_study_book_toc_units = []
    book_units = []
    self_study_book_units = []
    for group in unit_groups:
        first = group[0]
        first_lesson = first["lesson"]
        first_position = first["position"]
        assert isinstance(first_lesson, dict)
        assert isinstance(first_position, CurriculumPosition)
        unit_code = re.match(r"[A-Z]+", first_position.order)
        unit_label = unit_code.group(0) if unit_code else first_position.order
        display_unit = str(first_lesson.get("unit", "")) or first_position.unit_title
        unit_anchor = f"unit-{unit_label.lower()}"

        contents_items = []
        self_study_contents_items = []
        teacher_items = []
        book_toc_items = []
        book_articles = []
        self_study_book_articles = []
        for view in group:
            lesson = view["lesson"]
            position = view["position"]
            assert isinstance(lesson, dict)
            assert isinstance(position, CurriculumPosition)
            slug = str(view["slug"])
            page_title = str(view["page_title"])
            contents_items.append(
                '<li class="contents-item">'
                f'<a href="lessons/{escape(slug)}.html">'
                f'<span class="lesson-number">{escape(position.order)}</span>'
                f'<strong>{escape(page_title)}</strong>'
                f'<span>{escape(lesson.get("unit", ""))}</span>'
                "</a></li>"
            )
            self_study_contents_items.append(
                '<li class="contents-item">'
                f'<a href="lessons/{escape(slug)}.html">'
                f'<span class="lesson-number">{escape(position.order)}</span>'
                f'<strong>{escape(page_title)}</strong>'
                f'<span>{escape(lesson.get("unit", ""))}</span>'
                "</a></li>"
            )
            teacher_items.append(
                '<li><a href="teacher/{}.html"><span>{}</span> '
                '<strong>教師・レビュー用: {}</strong></a></li>'.format(
                    escape(slug), escape(position.order), escape(page_title)
                )
            )
            book_toc_items.append(
                f'<li><a href="#lesson-{escape(slug)}">'
                f'{escape(position.order)} {escape(page_title)}</a></li>'
            )
            book_practices = render_practices(
                md,
                view["problems"],
                id_prefix=f"book-{slug}-practice",
            )
            book_articles.append(
                f'<article class="book-lesson" id="lesson-{escape(slug)}">'
                '<header class="book-lesson-meta">'
                f'<p>{escape(position.order)} / {escape(display_unit)}</p>'
                "</header>"
                f'<div class="lesson-article">{view["lesson_html"]}</div>'
                '<section class="practice-section" aria-label="練習">'
                f"{book_practices}</section></article>"
            )
            self_study_book_practices = render_self_study_practices(
                md,
                view["problems"],
                by_id,
                id_prefix=f"self-study-book-{slug}-practice",
            )
            self_study_book_articles.append(
                f'<article class="book-lesson" id="lesson-{escape(slug)}">'
                '<header class="book-lesson-meta">'
                f'<p>{escape(position.order)} / {escape(display_unit)}</p>'
                "</header>"
                f'<div class="lesson-article">{view["lesson_html"]}</div>'
                '<section class="practice-section" aria-label="練習">'
                f"{self_study_book_practices}</section></article>"
            )

        index_units.append(
            f'<section class="curriculum-unit" id="{escape(unit_anchor)}">'
            f'<p class="section-kicker">ユニット {escape(unit_label)}</p>'
            f'<h2>{escape(display_unit)}</h2><ol class="contents-list">'
            f'{"".join(contents_items)}</ol></section>'
        )
        self_study_index_units.append(
            f'<section class="curriculum-unit" id="{escape(unit_anchor)}-self-study">'
            f'<p class="section-kicker">ユニット {escape(unit_label)}</p>'
            f'<h2>{escape(display_unit)}</h2><ol class="contents-list">'
            f'{"".join(self_study_contents_items)}</ol></section>'
        )
        teacher_units.append(
            '<section class="teacher-index-unit">'
            f'<h3>{escape(unit_label)} {escape(display_unit)}</h3><ul>'
            f'{"".join(teacher_items)}</ul></section>'
        )
        book_toc_units.append(
            f'<li><a href="#{escape(unit_anchor)}-book">'
            f'{escape(unit_label)} {escape(display_unit)}</a><ol>'
            f'{"".join(book_toc_items)}</ol></li>'
        )
        book_units.append(
            f'<section class="book-unit" id="{escape(unit_anchor)}-book">'
            f'<header class="book-unit-heading"><p>ユニット {escape(unit_label)}</p>'
            f'<h2>{escape(display_unit)}</h2></header>{"".join(book_articles)}</section>'
        )
        self_study_book_toc_units.append(
            f'<li><a href="#{escape(unit_anchor)}-self-study-book">'
            f'{escape(unit_label)} {escape(display_unit)}</a><ol>'
            f'{"".join(book_toc_items)}</ol></li>'
        )
        self_study_book_units.append(
            f'<section class="book-unit" id="{escape(unit_anchor)}-self-study-book">'
            f'<header class="book-unit-heading"><p>ユニット {escape(unit_label)}</p>'
            f'<h2>{escape(display_unit)}</h2></header>'
            f'{"".join(self_study_book_articles)}</section>'
        )

    index_page = render_template(
        root,
        "index.html",
        {
            "curriculum_units": "".join(index_units),
            "teacher_units": "".join(teacher_units),
        },
    )
    (destination / "index.html").write_text(index_page, encoding="utf-8", newline="\n")

    self_study_index_page = render_template(
        root,
        "self-study-index.html",
        {"curriculum_units": "".join(self_study_index_units)},
    )
    (self_study_dir / "index.html").write_text(
        self_study_index_page,
        encoding="utf-8",
        newline="\n",
    )

    book_page = render_template(
        root,
        "book.html",
        {
            "book_toc": "".join(book_toc_units),
            "book_units": "".join(book_units),
            "source_bibliography": render_source_bibliography(by_type.get("source", [])),
        },
    )
    (destination / "book.html").write_text(book_page, encoding="utf-8", newline="\n")

    self_study_book_page = render_template(
        root,
        "self-study-book.html",
        {
            "book_toc": "".join(self_study_book_toc_units),
            "book_units": "".join(self_study_book_units),
        },
    )
    (self_study_dir / "book.html").write_text(
        self_study_book_page,
        encoding="utf-8",
        newline="\n",
    )

    write_reports(destination, load_curriculum_document(root), by_type)


def replace_with_retry(source: Path, destination: Path, attempts: int = 5) -> None:
    for attempt in range(attempts):
        try:
            os.replace(source, destination)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            time.sleep(0.05 * (2**attempt))


def replace_site(
    root: Path,
    by_id: dict[str, dict],
    by_type: dict[str, list[dict]],
    curriculum: dict[str, CurriculumPosition],
) -> Path:
    build = root / "build"
    output = build / "site"
    backup = build / ".site-backup"
    build.mkdir(parents=True, exist_ok=True)
    if output.is_symlink() or backup.is_symlink():
        raise SiteBuildError("refusing to replace a symlinked site output")
    if backup.exists():
        shutil.rmtree(backup)
    temp = Path(tempfile.mkdtemp(prefix=".site-build-", dir=build))

    try:
        write_site(root, temp, by_id, by_type, curriculum)
        if output.exists():
            replace_with_retry(output, backup)
        try:
            replace_with_retry(temp, output)
        except OSError:
            if backup.exists() and not output.exists():
                replace_with_retry(backup, output)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        if temp.exists():
            shutil.rmtree(temp)

    return output


def build(root: Path) -> Path:
    root = root.resolve()
    by_id, by_type = load_records(root)
    curriculum = load_curriculum(root)
    validate_graph(root, by_id, by_type, curriculum)
    return replace_site(root, by_id, by_type, curriculum)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Repository root. Defaults to the parent of this script directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output = build(args.root)
    except (OSError, SiteBuildError) as exc:
        print(f"Static site build failed: {exc}", file=sys.stderr)
        return 1
    print(f"Built static textbook site at {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
