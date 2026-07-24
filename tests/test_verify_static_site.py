#!/usr/bin/env python3
"""Tests for production verification of the generated static site."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_static_site.py"
VERIFIER = ROOT / "scripts" / "verify_static_site.py"


def write_ndjson(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


@pytest.fixture
def built_site_root(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "site", tmp_path / "site")
    shutil.copyfile(
        ROOT / "LICENSE-CONTENT-CC-BY-4.0.md",
        tmp_path / "LICENSE-CONTENT-CC-BY-4.0.md",
    )
    lesson_id = "lesson.info1.programming.variables.v1"
    objective_id = "obj.info1.programming.variables.002.v1"
    problem_id = "prob.info1.variables.001.v1"
    answer_id = "ans.prob.info1.variables.001.v1"
    rubric_id = "rubric.prob.info1.variables.001.v1"

    write_ndjson(
        tmp_path / "data/collections/lessons.ndjson",
        [{
            "id": lesson_id,
            "type": "lesson",
            "title": "変数と代入",
            "subject": "情報I",
            "unit": "プログラミングの基礎",
            "body_ref": "lessons/fixture/source_name_is_not_a_slug.md",
            "status": "human_review_requested",
        }],
    )
    write_ndjson(
        tmp_path / "data/collections/problems.ndjson",
        [{
            "id": problem_id,
            "type": "problem",
            "question": "変数に値を代入しなさい。",
            "question_type": "short_code",
            "lesson_refs": [lesson_id],
            "objective_refs": [objective_id],
            "answer_refs": [answer_id],
            "rubric_refs": [rubric_id],
            "status": "human_review_requested",
        }],
    )
    write_ndjson(
        tmp_path / "data/collections/answers.ndjson",
        [{
            "id": answer_id,
            "type": "answer",
            "problem_id": problem_id,
            "canonical_answer": "SECRET_CANONICAL_ANSWER",
            "acceptable_answers": ["SECRET_ACCEPTABLE_ANSWER", "5", "OK"],
            "explanation": "SECRET_ANSWER_EXPLANATION",
            "hints": ["SECRET_HINT_ONE", "SECRET_HINT_TWO"],
            "verification_evidence": [{
                "method": "SECRET_VERIFICATION_METHOD",
                "expected": "SECRET_VERIFICATION_EXPECTED",
                "result": "passed",
            }],
            "status": "human_review_requested",
        }],
    )
    write_ndjson(
        tmp_path / "data/collections/rubrics.ndjson",
        [{
            "id": rubric_id,
            "type": "rubric",
            "problem_id": problem_id,
            "criteria": [{"id": "c1", "description": "SECRET_RUBRIC_TEXT", "points": 1}],
            "status": "human_review_requested",
        }],
    )
    write_ndjson(tmp_path / "data/collections/sources.ndjson", [])
    write_ndjson(tmp_path / "data/collections/revisions.ndjson", [])

    curriculum = {
        "units": [{
            "id": "unit.info1.programming.v1",
            "title": "Computers, Algorithms, and Programming",
            "lessons": [{
                "lesson_id": lesson_id,
                "order": "C2",
                "title": "Variables and Assignment",
                "learning_objectives": [{"id": objective_id}],
            }],
        }],
    }
    curriculum_path = tmp_path / "curriculum/highschool_information_i.curriculum.json"
    curriculum_path.parent.mkdir(parents=True)
    curriculum_path.write_text(json.dumps(curriculum), encoding="utf-8")

    body = tmp_path / "lessons/fixture/source_name_is_not_a_slug.md"
    body.parent.mkdir(parents=True)
    body.write_text(
        "# 変数と代入\n\n[外部の出典](https://example.com/reference)を確認します。\n"
        "\n## 練習\n\n- `prob.info1.variables.001.v1`\n",
        encoding="utf-8",
    )
    teacher = tmp_path / "teacher_guides/fixture/source_name_is_not_a_slug.md"
    teacher.parent.mkdir(parents=True)
    teacher.write_text("# 教師用ガイド\n\n教師用です。\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(tmp_path)],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return tmp_path


def run_verifier(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), "--root", str(root)],
        text=True,
        capture_output=True,
    )


def test_verifier_accepts_complete_offline_site_and_external_citation(built_site_root: Path) -> None:
    result = run_verifier(built_site_root)

    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        "1 classroom page(s), 1 self-study page(s), 1 teacher page(s), "
        "1 answer reveal(s), 2 books"
    ) in result.stdout


def test_verifier_rejects_unrendered_markdown_emphasis(built_site_root: Path) -> None:
    page = built_site_root / "build/site/lessons/programming-variables.html"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "</main>", "<p>**unrendered emphasis**</p></main>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "unrendered Markdown emphasis delimiter" in result.stderr


def test_verifier_allows_exponent_operator_in_code(built_site_root: Path) -> None:
    page = built_site_root / "build/site/lessons/programming-variables.html"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "</main>", "<p><code>2 ** 3</code></p></main>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    "secret",
    [
        "SECRET_VERIFICATION_METHOD",
        "SECRET_RUBRIC_TEXT",
        "prob.info1.variables.001.v1",
        "ans.prob.info1.variables.001.v1",
        "rubric.prob.info1.variables.001.v1",
    ],
)
def test_verifier_rejects_teacher_only_data_in_self_study_book(
    built_site_root: Path,
    secret: str,
) -> None:
    book = built_site_root / "build/site/self-study/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("</main>", f"<p>{secret}</p></main>", 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "leaked into book.html" in result.stderr


def test_verifier_rejects_inaccessible_self_study_reveal(built_site_root: Path) -> None:
    lesson = built_site_root / "build/site/self-study/lessons/programming-variables.html"
    lesson.write_text(
        lesson.read_text(encoding="utf-8").replace("<summary>", "<p>", 1).replace(
            "</summary>", "</p>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "each hint and answer reveal requires a summary" in result.stderr


def test_verifier_rejects_inaccessible_self_study_book_reveal(built_site_root: Path) -> None:
    book = built_site_root / "build/site/self-study/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("<summary>", "<p>", 1).replace(
            "</summary>", "</p>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "each hint and answer reveal requires a summary" in result.stderr


def test_verifier_rejects_teacher_only_data_in_self_study_lesson(built_site_root: Path) -> None:
    lesson = built_site_root / "build/site/self-study/lessons/programming-variables.html"
    lesson.write_text(
        lesson.read_text(encoding="utf-8").replace(
            "</main>", "<p>SECRET_VERIFICATION_METHOD</p></main>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "leaked into programming-variables.html" in result.stderr


def test_verifier_rejects_teacher_only_data_in_self_study_index(built_site_root: Path) -> None:
    index = built_site_root / "build/site/self-study/index.html"
    index.write_text(
        index.read_text(encoding="utf-8").replace(
            "</main>", "<p>SECRET_VERIFICATION_METHOD</p></main>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "leaked into index.html" in result.stderr


def test_verifier_rejects_stale_coverage_report(built_site_root: Path) -> None:
    report = built_site_root / "build/site/reports/semantic-coverage-audit.json"
    payload = json.loads(report.read_text(encoding="utf-8"))
    payload["row_count"] = 999
    report.write_text(json.dumps(payload), encoding="utf-8")

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "generated report is stale or inconsistent" in result.stderr


def test_verifier_rejects_orphan_answer_from_self_study_delivery(built_site_root: Path) -> None:
    answers = built_site_root / "data/collections/answers.ndjson"
    records = [json.loads(line) for line in answers.read_text(encoding="utf-8").splitlines()]
    orphan = {**records[0], "id": "ans.prob.info1.variables.orphan.v1"}
    write_ndjson(answers, [*records, orphan])

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "render every answer record exactly once" in result.stderr


def test_verifier_rejects_book_feedback_that_differs_from_lessons(built_site_root: Path) -> None:
    book = built_site_root / "build/site/self-study/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace(
            "SECRET_CANONICAL_ANSWER", "DIFFERENT_SELF_STUDY_ANSWER", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "answer feedback does not match" in result.stderr


def test_verifier_rejects_broken_local_fragment(built_site_root: Path) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace(
            'href="#lesson-programming-variables"',
            'href="#lesson-missing"',
            1,
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "broken fragment" in result.stderr


def test_verifier_rejects_broken_local_image(built_site_root: Path) -> None:
    lesson = built_site_root / "build/site/lessons/programming-variables.html"
    lesson.write_text(
        lesson.read_text(encoding="utf-8").replace(
            "</article>",
            '<img src="../assets/figures/missing.svg" alt="変数へ値を保存する流れ"></article>',
            1,
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "broken local reference" in result.stderr


def test_verifier_rejects_active_content_in_generated_svg(built_site_root: Path) -> None:
    asset = built_site_root / "build/site/assets/figures/unsafe.svg"
    asset.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "active SVG element" in result.stderr


@pytest.mark.parametrize("alt", ("", "図", "assignment-flow.svg"))
def test_verifier_rejects_low_information_image_alt(
    built_site_root: Path,
    alt: str,
) -> None:
    asset = built_site_root / "build/site/assets/figures/assignment-flow.svg"
    asset.parent.mkdir(parents=True, exist_ok=True)
    asset.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
    lesson = built_site_root / "build/site/lessons/programming-variables.html"
    lesson.write_text(
        lesson.read_text(encoding="utf-8").replace(
            "</article>",
            f'<img src="../assets/figures/assignment-flow.svg" alt="{alt}"></article>',
            1,
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "meaningful image alt text required" in result.stderr


def test_verifier_rejects_external_runtime_asset(built_site_root: Path) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace(
            'href="assets/styles.css"',
            'href="https://example.com/styles.css"',
            1,
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "external runtime reference" in result.stderr


def test_verifier_rejects_inline_activity_handler(built_site_root: Path) -> None:
    activity = built_site_root / "build/site/activities/b7_keyboard_start.html"
    activity.write_text(
        activity.read_text(encoding="utf-8").replace(
            '<button type="submit">',
            '<button type="submit" onclick="alert(1)">',
            1,
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "inline event handler" in result.stderr


def test_verifier_rejects_unexpected_activity_file(built_site_root: Path) -> None:
    extra = built_site_root / "build/site/activities/unexpected.txt"
    extra.write_text("unexpected", encoding="utf-8")

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "unexpected activity file set" in result.stderr


def test_verifier_rejects_escaped_css_runtime_reference(built_site_root: Path) -> None:
    stylesheet = built_site_root / "build/site/assets/styles.css"
    stylesheet.write_text(
        stylesheet.read_text(encoding="utf-8")
        + "\n@media screen { body { background: u\\72l(https://example.com/tracker); } }\n",
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "CSS escapes are not allowed" in result.stderr


@pytest.mark.parametrize(
    "secret",
    [
        "SECRET_CANONICAL_ANSWER",
        "SECRET_ACCEPTABLE_ANSWER",
        "SECRET_ANSWER_EXPLANATION",
        "SECRET_VERIFICATION_METHOD",
        "SECRET_RUBRIC_TEXT",
        "prob.info1.variables.001.v1",
        "ans.prob.info1.variables.001.v1",
        "rubric.prob.info1.variables.001.v1",
    ],
)
def test_verifier_rejects_teacher_only_data_in_learner_book(
    built_site_root: Path,
    secret: str,
) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("</main>", f"<p>{secret}</p></main>", 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "leaked into book.html" in result.stderr


def test_verifier_rejects_excess_standalone_numeric_answer_in_learner_text(
    built_site_root: Path,
) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("</main>", "<p>5</p></main>", 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "teacher-only value" in result.stderr


def test_verifier_rejects_standalone_alphabetic_answer_in_learner_text(
    built_site_root: Path,
) -> None:
    answers = built_site_root / "data/collections/answers.ndjson"
    records = [json.loads(line) for line in answers.read_text(encoding="utf-8").splitlines()]
    records[0]["acceptable_answers"].append("B")
    write_ndjson(answers, records)
    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(built_site_root)],
        check=True,
        text=True,
        capture_output=True,
    )
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("</main>", "<p>B</p></main>", 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "teacher-only value" in result.stderr


@pytest.mark.parametrize(
    "payload",
    (
        '<details><summary>5</summary></details>',
        '<section class="success-criteria"><p>5</p></section>',
        '<div class="hint-reveal"><p>5</p></div>',
        '<div class="answer-reveal"><p>5</p></div>',
    ),
)
def test_verifier_structurally_rejects_classroom_support_ui(
    built_site_root: Path,
    payload: str,
) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("</main>", f"{payload}</main>", 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "answer/hint/success-criteria structure leaked into book.html" in result.stderr


@pytest.mark.parametrize(
    "attribute",
    (
        'data-answer="5"',
        'data-answer-id="ans.prob.info1.variables.001.v1"',
        'title="SECRET_HINT_ONE"',
        'aria-label="answer 5"',
        'title="result=OK"',
        'data-criterion-id="c1"',
        'data-points="1"',
    ),
)
def test_verifier_rejects_classroom_leakage_in_attributes(
    built_site_root: Path,
    attribute: str,
) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace(
            "</main>", f"<div {attribute}></div></main>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "leaked into book.html" in result.stderr


def test_verifier_rejects_numeric_answer_in_review_only_structure(
    built_site_root: Path,
) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace(
            "</main>", '<section class="review-subsection"><p>5</p></section></main>', 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "review-only structure leaked into book.html" in result.stderr


@pytest.mark.parametrize("token", ("5", "1"))
def test_verifier_rejects_inline_short_review_value(
    built_site_root: Path,
    token: str,
) -> None:
    page = built_site_root / "build/site/lessons/programming-variables.html"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "</main>", f"<p>Inline {token} leak</p></main>", 1
        ),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "teacher-only value" in result.stderr


def test_verifier_rejects_wrong_page_count_and_missing_structure(built_site_root: Path) -> None:
    teacher = built_site_root / "build/site/teacher/programming-variables.html"
    teacher.unlink()

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "unexpected HTML page set" in result.stderr

    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(built_site_root)],
        check=True,
        text=True,
        capture_output=True,
    )
    learner = built_site_root / "build/site/lessons/programming-variables.html"
    learner.write_text(
        learner.read_text(encoding="utf-8").replace('class="lesson-navigation"', 'class="removed"', 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 1
    assert "missing required structure nav.lesson-navigation" in result.stderr
