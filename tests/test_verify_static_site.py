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
            "acceptable_answers": ["SECRET_ACCEPTABLE_ANSWER", "5"],
            "explanation": "SECRET_ANSWER_EXPLANATION",
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
    assert "1 learner page(s), 1 teacher page(s), 1 book" in result.stdout


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


def test_verifier_allows_standalone_numeric_answer_in_unrelated_learner_text(
    built_site_root: Path,
) -> None:
    book = built_site_root / "build/site/book.html"
    book.write_text(
        book.read_text(encoding="utf-8").replace("</main>", "<p>5</p></main>", 1),
        encoding="utf-8",
    )

    result = run_verifier(built_site_root)

    assert result.returncode == 0, result.stdout + result.stderr


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
