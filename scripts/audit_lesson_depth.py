#!/usr/bin/env python3
"""Report structural depth evidence without making educational approval claims."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
PILOT_ORDERS = frozenset({"A3", "B5", "C1", "D2"})
HEADING_LINE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FIGURE_REFERENCE = re.compile(r"\]\(figure:([A-Za-z0-9][A-Za-z0-9._/-]*\.svg)\)")
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
MIN_SUBSTANTIVE_SECTION_CHARACTERS = 40
CLAIM_LEDGER_HEADERS = (
    "claim locator",
    "exact claim",
    "claim type",
    "evidence",
    "check",
    "scope note",
)
CLAIM_TYPES = frozenset(
    {
        "factual",
        "legal",
        "statistical",
        "standard",
        "technical",
        "deterministic calculation",
        "methodological guidance",
        "artifact observation",
    }
)
CLAIM_CHECK_STATUSES = frozenset({"supported", "needs_revision", "open_question"})
CLAIM_LESSON_LOCATOR = re.compile(
    r"`(lesson\.[a-z0-9]+(?:\.[a-z0-9]+)*\.v[1-9][0-9]*)`\s*(?:/|>)\s*\S"
)
CLAIM_SOURCE_ID = re.compile(r"`(src\.[a-z0-9]+(?:\.[a-z0-9]+)*\.v[1-9][0-9]*)`")
ISO_DATE = re.compile(r"\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b")


class DepthAuditError(RuntimeError):
    """Raised when canonical audit inputs are missing or malformed."""


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DepthAuditError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DepthAuditError(f"expected an object in {path}")
    return value


def read_ndjson(path: Path) -> list[dict]:
    records: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise DepthAuditError(f"cannot read {path}: {exc}") from exc
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DepthAuditError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
        if not isinstance(value, dict):
            raise DepthAuditError(f"{path}:{line_no}: expected an object")
        records.append(value)
    return records


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    folded = text.casefold()
    return any(term.casefold() in folded for term in terms)


def heading_matches(title: str, terms: tuple[str, ...]) -> bool:
    normalized = re.sub(
        r"^(?:第[0-9]+時|学習パート[0-9]+|パート[0-9]+)(?:の)?[\s:：-]*",
        "",
        title.strip().casefold(),
    )
    return any(normalized.startswith(term.casefold()) for term in terms)


def has_substantive_section_body(body: str) -> bool:
    without_images = MARKDOWN_IMAGE.sub(" ", HTML_COMMENT.sub(" ", body))
    without_markup = re.sub(r"<[^>]+>|[`#>*_~|\[\]():-]", " ", without_images)
    meaningful_characters = re.findall(
        r"[A-Za-z0-9\u3040-\u30ff\u3400-\u9fff]",
        without_markup,
    )
    return len(meaningful_characters) >= MIN_SUBSTANTIVE_SECTION_CHARACTERS


def has_substantive_text(value: str, minimum: int = 20) -> bool:
    return len(re.findall(r"[A-Za-z0-9\u3040-\u30ff\u3400-\u9fff]", value)) >= minimum


def claim_ledger_row_is_valid(
    cells: list[str],
    valid_source_ids: set[str] | None = None,
    expected_lesson_id: str | None = None,
) -> bool:
    if len(cells) != len(CLAIM_LEDGER_HEADERS) or not all(cells):
        return False
    locator, claim, claim_type, evidence, check, scope_note = cells
    locator_match = CLAIM_LESSON_LOCATOR.search(locator)
    if locator_match is None:
        return False
    if expected_lesson_id is not None and locator_match.group(1) != expected_lesson_id:
        return False
    if not has_substantive_text(claim) or claim_type.casefold() not in CLAIM_TYPES:
        return False

    folded_evidence = evidence.casefold()
    cited_source_ids = set(CLAIM_SOURCE_ID.findall(evidence))
    has_source = bool(cited_source_ids)
    if valid_source_ids is not None and not cited_source_ids <= valid_source_ids:
        return False
    deterministic_evidence = (
        claim_type.casefold() == "deterministic calculation"
        or "deterministic calculation" in folded_evidence
    ) and contains_any(
        evidence,
        ("arithmetic", "calculation", "subtraction", "ratio", "project-authored"),
    )
    artifact_evidence = claim_type.casefold() == "artifact observation" and contains_any(
        evidence,
        ("project-authored", "direct comparison"),
    )
    if not (has_source or deterministic_evidence or artifact_evidence):
        return False

    statuses = {status for status in CLAIM_CHECK_STATUSES if status in check.casefold()}
    reviewer_text = ISO_DATE.sub("", check)
    for status in CLAIM_CHECK_STATUSES:
        reviewer_text = reviewer_text.replace(f"`{status}`", "")
        reviewer_text = reviewer_text.replace(status, "")
    if ISO_DATE.search(check) is None or len(statuses) != 1 or not has_substantive_text(reviewer_text, 4):
        return False
    return has_substantive_text(scope_note)


def heading_evidence(text: str, terms: tuple[str, ...]) -> list[str]:
    lines = text.splitlines()
    evidence: list[str] = []
    for index, line in enumerate(lines):
        match = HEADING_LINE.fullmatch(line)
        if match is None or not 2 <= len(match.group(1)) <= 4:
            continue
        if not heading_matches(match.group(2), terms):
            continue
        body_lines = []
        for candidate in lines[index + 1:]:
            next_heading = HEADING_LINE.fullmatch(candidate)
            if next_heading is not None:
                break
            body_lines.append(candidate)
        if has_substantive_section_body("\n".join(body_lines)):
            evidence.append(match.group(2))
    return evidence


def claim_ledger_evidence(
    text: str,
    valid_source_ids: set[str] | None = None,
    expected_lesson_id: str | None = None,
) -> list[str]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = HEADING_LINE.fullmatch(line)
        if match is None or not 2 <= len(match.group(1)) <= 4:
            continue
        title = match.group(2)
        if not heading_matches(title, ("claim review ledger", "claim-level evidence ledger")):
            continue
        body_lines = []
        for candidate in lines[index + 1:]:
            if HEADING_LINE.fullmatch(candidate) is not None:
                break
            body_lines.append(candidate)
        for table_index, candidate in enumerate(body_lines[:-2]):
            if not candidate.strip().startswith("|"):
                continue
            headers = tuple(
                cell.strip().casefold()
                for cell in candidate.strip().strip("|").split("|")
            )
            if headers != CLAIM_LEDGER_HEADERS:
                continue
            separator = body_lines[table_index + 1].strip().strip("|").split("|")
            if len(separator) != len(CLAIM_LEDGER_HEADERS) or not all(
                re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in separator
            ):
                continue
            rows: list[list[str]] = []
            for row in body_lines[table_index + 2:]:
                if not row.strip().startswith("|"):
                    break
                cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
                rows.append(cells)
            if rows and all(
                claim_ledger_row_is_valid(cells, valid_source_ids, expected_lesson_id)
                for cells in rows
            ):
                return [title]
    return []


def phrase_context_evidence(text: str, terms: tuple[str, ...], label: str) -> list[str]:
    folded = text.casefold()
    for term in terms:
        index = folded.find(term.casefold())
        if index >= 0 and has_substantive_section_body(text[index:index + 2000]):
            return [label]
    return []


def check_item(key: str, label: str, present: bool, evidence: list[str] | str) -> dict:
    if isinstance(evidence, str):
        evidence = [evidence] if evidence else []
    return {"key": key, "label": label, "present": present, "evidence": evidence}


def linked_records(problem: dict, field: str, by_id: dict[str, dict]) -> list[dict]:
    return [by_id[ref] for ref in problem.get(field, []) or [] if ref in by_id]


def lesson_checks(
    root: Path,
    planned: dict,
    canonical: dict,
    problems: list[dict],
    by_id: dict[str, dict],
) -> list[dict]:
    body_ref = str(canonical.get("body_ref", ""))
    body_path = root / body_ref
    body = body_path.read_text(encoding="utf-8") if body_path.is_file() else ""
    body_ref_path = Path(body_ref)
    teacher_path = root / "teacher_guides" / Path(*body_ref_path.parts[1:])
    teacher = teacher_path.read_text(encoding="utf-8") if teacher_path.is_file() else ""
    answers = [record for problem in problems for record in linked_records(problem, "answer_refs", by_id)]
    figure_refs = sorted(set(FIGURE_REFERENCE.findall(body + "\n" + teacher)))
    equivalent_terms = (
        "text equivalent", "non-visual equivalent", "文字による説明", "テキスト等価",
        "図の完全なテキスト", "図のテキスト等価版", "表による代替", "完全な代替",
        "アクセシビリティの代替", "非視覚", "読み上げ用",
    )

    readiness = heading_evidence(body, ("前提", "準備", "readiness"))
    remediation = heading_evidence(
        body,
        ("診断と修正", "復習", "remediation", "retry", "再挑戦"),
    )
    if readiness and contains_any(body, ("迷ったら", "答えられなければ", "確認してから")):
        remediation.append("readiness branch in lesson text")
    concept = heading_evidence(
        body,
        (
            "概念モデル", "考え方のモデル", "コンピュータを役割", "webサービスまでの役割モデル",
            "しくみ", "流れ", "役割", "concept model", "model", "仕組み",
        ),
    )
    examples = heading_evidence(body, ("例題", "worked example", "具体例", "考え方を追う例"))
    contrasts = heading_evidence(
        body,
        ("よくある間違い", "間違い例", "誤解", "誤り", "対比", "non-example"),
    )
    guided = heading_evidence(body, ("ガイド付き", "一緒に", "guided", "段階練習", "やってみよう"))
    transfer = heading_evidence(body, ("別の場面への転移", "独立課題", "independent", "transfer"))
    mastery = heading_evidence(body, ("到達", "自己確認の診断", "退出", "mastery"))
    timing = heading_evidence(teacher, ("時間配分", "授業時間", "進行表", "timing"))
    expected = heading_evidence(
        teacher,
        ("想定される応答", "期待される応答", "期待する反応", "expected response"),
    )
    timing.extend(phrase_context_evidence(
        teacher,
        ("| 時間 | 学習活動 |", "| 時限 | 学習者の到達点 |"),
        "detailed timing table",
    ))
    expected.extend(phrase_context_evidence(
        teacher,
        ("期待される学習者の反応", "期待する反応"),
        "expected learner response table",
    ))
    feedback = heading_evidence(teacher, ("フィードバック", "形成的評価", "feedback"))
    accessibility = heading_evidence(teacher, ("アクセシビリティ", "支援", "accessibility"))
    stopping = heading_evidence(
        teacher,
        ("50分授業の到達点", "区切り", "到達点", "停止点", "stopping point"),
    )
    extension = heading_evidence(teacher, ("補充と任意発展", "補習と任意発展", "発展", "extension"))
    materials = heading_evidence(teacher, ("教材", "materials", "準備物"))

    hints_complete = bool(answers) and all(
        isinstance(answer.get("hints"), list)
        and len(answer["hints"]) == 2
        and all(isinstance(item, str) and item.strip() for item in answer["hints"])
        for answer in answers
    )
    explanations_complete = bool(answers) and all(
        isinstance(answer.get("explanation"), str) and answer["explanation"].strip()
        for answer in answers
    )
    learner_checks_complete = bool(problems) and all(
        isinstance(problem.get("learner_checks"), list)
        and 2 <= len(problem["learner_checks"]) <= 4
        and all(isinstance(item, str) and item.strip() for item in problem["learner_checks"])
        and len(set(problem["learner_checks"])) == len(problem["learner_checks"])
        for problem in problems
    )
    learner_check_evidence = [
        f"{problem.get('id')}: {len(problem.get('learner_checks', []) or [])} check(s)"
        for problem in problems
    ]
    objective_count = len(planned.get("learning_objectives", []) or [])
    source_refs = canonical.get("source_refs", []) or []
    claim_ledger = claim_ledger_evidence(
        teacher,
        set(source_refs),
        str(canonical.get("id", "")),
    )
    source_route_complete = bool(source_refs and claim_ledger) and all(
        isinstance(source_ref, str) and by_id.get(source_ref, {}).get("type") == "source"
        for source_ref in source_refs
    )

    return [
        check_item("outcome", "Observable objective-mapped outcome", objective_count > 0, f"{objective_count} objective(s)"),
        check_item("readiness_remediation", "Readiness check and remediation route", bool(readiness and remediation), readiness + remediation),
        check_item("concept_model", "Language- and tool-independent concept model", bool(concept), concept + ([f"{len(figure_refs)} figure reference(s)"] if figure_refs else [])),
        check_item("worked_example", "Reasoned worked example", bool(examples), examples),
        check_item("misconception_contrast", "Misconception contrast or non-example", bool(contrasts), contrasts),
        check_item("guided_attempt", "Guided learner attempt", bool(guided), guided),
        check_item("independent_transfer", "Independent transfer task", bool(transfer), transfer),
        check_item("exit_mastery", "Exit artifact and mastery decision", bool(mastery), mastery),
        check_item("practice", "Linked canonical practice", bool(problems), f"{len(problems)} problem(s)"),
        check_item("staged_hints", "Exactly two staged hints for each answer", hints_complete, f"{len(answers)} answer(s)"),
        check_item("answer_explanations", "Full self-study answer explanations", explanations_complete, f"{len(answers)} answer(s)"),
        check_item("success_criteria", "Task-specific learner-facing success criteria", learner_checks_complete, learner_check_evidence),
        check_item("teacher_timing", "Teacher timing", bool(timing), timing),
        check_item("teacher_materials", "Teacher materials", bool(materials), materials),
        check_item("teacher_expected_responses", "Teacher expected responses", bool(expected), expected),
        check_item("teacher_feedback", "Teacher feedback moves", bool(feedback), feedback),
        check_item("teacher_accessibility", "Teacher accessibility fallback", bool(accessibility), accessibility),
        check_item("teacher_stopping_point", "Teacher stopping point", bool(stopping), stopping),
        check_item("teacher_extension", "Teacher extension", bool(extension), extension),
        check_item(
            "claim_review_route",
            "Claim-level source review route",
            source_route_complete,
            [f"{len(source_refs)} source reference(s)", *claim_ledger],
        ),
        check_item(
            "visual_equivalent",
            "Text/data equivalent for each figure",
            not figure_refs
            or len(heading_evidence(body + "\n" + teacher, equivalent_terms)) >= len(figure_refs),
            "no figure used"
            if not figure_refs
            else [
                f"{len(figure_refs)} distinct figure(s)",
                f"{len(heading_evidence(body + chr(10) + teacher, equivalent_terms))} equivalent heading(s)",
            ],
        ),
    ]


def audit_repository(root: Path, *, strict_pilots: bool = True) -> dict:
    root = root.resolve()
    curriculum = read_json(root / "curriculum/highschool_information_i.curriculum.json")
    collections = root / "data/collections"
    records = [
        record
        for filename in (
            "lessons.ndjson",
            "problems.ndjson",
            "answers.ndjson",
            "rubrics.ndjson",
            "sources.ndjson",
        )
        for record in read_ndjson(collections / filename)
    ]
    by_id = {str(record.get("id")): record for record in records if record.get("id")}
    canonical_lessons = {record["id"]: record for record in records if record.get("type") == "lesson"}
    problems = [record for record in records if record.get("type") == "problem"]
    planned_lessons = [lesson for unit in curriculum.get("units", []) for lesson in unit.get("lessons", [])]
    if len(planned_lessons) != 32:
        raise DepthAuditError(f"expected 32 curriculum lessons, got {len(planned_lessons)}")

    lesson_reports = []
    warning_count = 0
    error_count = 0
    for planned in planned_lessons:
        lesson_id = str(planned.get("lesson_id", ""))
        canonical = canonical_lessons.get(lesson_id)
        if canonical is None:
            raise DepthAuditError(f"missing canonical lesson: {lesson_id}")
        linked = [problem for problem in problems if lesson_id in (problem.get("lesson_refs", []) or [])]
        checks = lesson_checks(root, planned, canonical, linked, by_id)
        strict = strict_pilots and planned.get("order") in PILOT_ORDERS
        findings = []
        for check in checks:
            if check["present"]:
                continue
            severity = "error" if strict else "warning"
            findings.append({"severity": severity, "check": check["key"], "message": check["label"]})
            warning_count += severity == "warning"
            error_count += severity == "error"
        lesson_reports.append({
            "order": planned.get("order"),
            "lesson_id": lesson_id,
            "pilot": planned.get("order") in PILOT_ORDERS,
            "structural_status": "evidence_found" if not findings else "evidence_missing",
            "checks": checks,
            "findings": findings,
        })

    return {
        "audit": "information_i_content_depth",
        "decision_scope": "structural evidence only; human review remains required",
        "strict_pilots": strict_pilots,
        "summary": {
            "lesson_count": len(lesson_reports),
            "pilot_count": sum(report["pilot"] for report in lesson_reports),
            "warning_count": warning_count,
            "error_count": error_count,
        },
        "lessons": lesson_reports,
    }


def text_report(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "Information I content-depth structural audit",
        f"Lessons: {summary['lesson_count']} (strict pilots: {summary['pilot_count']})",
        f"Warnings: {summary['warning_count']}; Errors: {summary['error_count']}",
        "Decision scope: structural evidence only; human review remains required.",
    ]
    for lesson in report["lessons"]:
        findings = lesson["findings"]
        state = "complete" if not findings else ", ".join(
            f"{finding['severity']}:{finding['check']}" for finding in findings
        )
        lines.append(f"{lesson['order']} {lesson['lesson_id']}: {state}")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="downgrade missing pilot evidence to warnings and always return success",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = audit_repository(args.root, strict_pilots=not args.report_only)
    except DepthAuditError as exc:
        print(f"Depth audit failed: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else text_report(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 1 if report["summary"]["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
