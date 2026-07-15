#!/usr/bin/env python3
"""Tests for the generated static textbook site."""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from scripts import build_static_site


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_static_site.py"


class AssetReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"href", "src"} and value and not value.startswith("#"):
                self.references.append(value)


def write_ndjson(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    path.write_text(text, encoding="utf-8")


def write_curriculum(path: Path, units: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"units": units}, ensure_ascii=False), encoding="utf-8")


def curriculum_lesson(lesson_id: str, order: str, title: str, objective_id: str) -> dict:
    return {
        "lesson_id": lesson_id,
        "order": order,
        "title": title,
        "learning_objectives": [{"id": objective_id}],
    }


@pytest.fixture
def sample_root(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "site", tmp_path / "site")
    lesson_id = "lesson.info1.programming.variables.v1"
    objective_id = "obj.info1.programming.variables.002.v1"
    problem_id = "prob.info1.variables.001.v1"
    answer_id = "ans.prob.info1.variables.001.v1"
    rubric_id = "rubric.prob.info1.variables.001.v1"

    write_ndjson(
        tmp_path / "data" / "collections" / "lessons.ndjson",
        [{
            "id": lesson_id,
            "type": "lesson",
            "title": "変数と代入",
            "subject": "情報I",
            "unit": "プログラミングの基礎",
            "body_ref": "lessons/highschool_information_i/programming/fixture_lesson.md",
            "status": "human_review_requested",
        }],
    )
    write_ndjson(
        tmp_path / "data" / "collections" / "problems.ndjson",
        [{
            "id": problem_id,
            "type": "problem",
            "question": "変数 `score` に値を書きなさい。",
            "question_type": "short_code",
            "lesson_refs": [lesson_id],
            "objective_refs": [objective_id],
            "answer_refs": [answer_id],
            "rubric_refs": [rubric_id],
            "common_mistakes": ["代入していない。"],
            "status": "human_review_requested",
        }],
    )
    write_ndjson(
        tmp_path / "data" / "collections" / "answers.ndjson",
        [{
            "id": answer_id,
            "type": "answer",
            "problem_id": problem_id,
            "answer_type": "code",
            "canonical_answer": "SECRET_ANSWER_TOKEN",
            "acceptable_answers": ["SECRET_ACCEPTABLE_TOKEN"],
            "explanation": "教師用の説明です。",
            "verification_evidence": [{"method": "test", "expected": "secret", "result": "passed"}],
            "status": "human_review_requested",
        }],
    )
    write_curriculum(
        tmp_path / "curriculum" / "highschool_information_i.curriculum.json",
        [{
            "id": "unit.info1.programming.v1",
            "title": "Computers, Algorithms, and Programming",
            "lessons": [curriculum_lesson(lesson_id, "C2", "Variables and Assignment", objective_id)],
        }],
    )
    write_ndjson(
        tmp_path / "data" / "collections" / "rubrics.ndjson",
        [{
            "id": rubric_id,
            "type": "rubric",
            "problem_id": problem_id,
            "criteria": [{"id": "c1", "description": "SECRET_RUBRIC_TOKEN", "points": 1}],
            "status": "human_review_requested",
        }],
    )
    write_ndjson(tmp_path / "data" / "collections" / "sources.ndjson", [])
    write_ndjson(
        tmp_path / "data" / "collections" / "revisions.ndjson",
        [{
            "id": "rev.20260714.0001",
            "type": "revision",
            "entity_id": lesson_id,
            "reason": "Fixture revision.",
            "status": "draft",
        }],
    )
    lesson_body = tmp_path / "lessons" / "highschool_information_i" / "programming" / "fixture_lesson.md"
    lesson_body.parent.mkdir(parents=True)
    lesson_body.write_text(
        "# 変数と代入\n\n<script>alert('unsafe')</script>\n\n"
        "## 比較\n\n| 案 | 点 |\n| --- | ---: |\n| A | 2 |\n\n## 練習\n\n"
        "- `prob.info1.variables.001.v1`: 内部ID付きの一覧。\n",
        encoding="utf-8",
    )
    teacher = tmp_path / "teacher_guides" / "highschool_information_i" / "programming" / "fixture_lesson.md"
    teacher.parent.mkdir(parents=True)
    teacher.write_text("# 教師用ガイド\n\n指導用の内容です。\n", encoding="utf-8")
    return tmp_path


def run_builder(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(root)],
        text=True,
        capture_output=True,
    )


def snapshot_files(root: Path) -> dict[str, bytes]:
    site = root / "build" / "site"
    return {path.relative_to(site).as_posix(): path.read_bytes() for path in sorted(site.rglob("*")) if path.is_file()}


def test_build_is_offline_deterministic_and_separates_answers(sample_root: Path) -> None:
    index_db = sample_root / "build" / "index.sqlite"
    index_db.parent.mkdir(parents=True, exist_ok=True)
    index_db.write_bytes(b"keep-this-index")

    first = run_builder(sample_root)
    assert first.returncode == 0, first.stdout + first.stderr
    first_snapshot = snapshot_files(sample_root)
    learner = first_snapshot["lessons/programming-variables.html"].decode("utf-8")
    teacher = first_snapshot["teacher/programming-variables.html"].decode("utf-8")
    book = first_snapshot["book.html"].decode("utf-8")
    index = first_snapshot["index.html"].decode("utf-8")

    assert "SECRET_ANSWER_TOKEN" not in learner
    assert "SECRET_ACCEPTABLE_TOKEN" not in learner
    assert "SECRET_RUBRIC_TOKEN" not in learner
    assert "prob.info1.variables.001.v1" not in learner
    assert "練習 1" in learner
    assert "<table>" in learner
    assert '<div class="table-wrap"><table>' in learner
    assert "<th>案</th>" in learner
    assert "&lt;script&gt;alert('unsafe')&lt;/script&gt;" in learner
    assert "SECRET_ANSWER_TOKEN" in teacher
    assert "SECRET_RUBRIC_TOKEN" in teacher
    assert "各レッスンの学習目標、順序、例、時間配分、問題、評価方法は本プロジェクトが作成したドラフト" in teacher
    assert "SECRET_ANSWER_TOKEN" not in book
    assert "SECRET_ACCEPTABLE_TOKEN" not in book
    assert "SECRET_RUBRIC_TOKEN" not in book
    assert "prob.info1.variables.001.v1" not in book
    assert 'id="lesson-programming-variables"' in book
    assert "<table>" in book
    assert '<div class="table-wrap"><table>' in book
    assert 'href="book.html"' in index
    assert "ユニット C" in index
    assert "C2" in learner
    assert teacher.count("<h1") == 1
    assert 'href="../lessons/programming-variables.html"' in teacher
    assert "lessons/fixture-lesson.html" not in first_snapshot
    assert all(b"http://" not in content and b"https://" not in content for content in first_snapshot.values())

    site_root = sample_root / "build" / "site"
    for relative_path, content in first_snapshot.items():
        if not relative_path.endswith(".html"):
            continue
        parser = AssetReferenceParser()
        parser.feed(content.decode("utf-8"))
        page = site_root / relative_path
        for reference in parser.references:
            assert (page.parent / reference).resolve().is_file(), f"broken generated link: {reference}"

    second = run_builder(sample_root)
    assert second.returncode == 0, second.stdout + second.stderr
    assert snapshot_files(sample_root) == first_snapshot
    assert index_db.read_bytes() == b"keep-this-index"


def test_missing_body_ref_fails_clearly(sample_root: Path) -> None:
    lessons = sample_root / "data" / "collections" / "lessons.ndjson"
    record = json.loads(lessons.read_text(encoding="utf-8"))
    record["body_ref"] = "lessons/missing.md"
    write_ndjson(lessons, [record])

    result = run_builder(sample_root)
    assert result.returncode == 1
    assert "missing body_ref file" in result.stderr


def test_duplicate_id_fails_clearly(sample_root: Path) -> None:
    answers = sample_root / "data" / "collections" / "answers.ndjson"
    answer = json.loads(answers.read_text(encoding="utf-8"))
    write_ndjson(answers, [answer, answer])

    result = run_builder(sample_root)
    assert result.returncode == 1
    assert "duplicate id" in result.stderr


def test_broken_reference_fails_clearly(sample_root: Path) -> None:
    problems = sample_root / "data" / "collections" / "problems.ndjson"
    problem = json.loads(problems.read_text(encoding="utf-8"))
    problem["answer_refs"] = ["ans.missing.v1"]
    write_ndjson(problems, [problem])

    result = run_builder(sample_root)
    assert result.returncode == 1
    assert "broken reference in answer_refs" in result.stderr


def test_curriculum_order_units_and_navigation_ignore_body_filenames(sample_root: Path) -> None:
    lessons_path = sample_root / "data" / "collections" / "lessons.ndjson"
    variables = json.loads(lessons_path.read_text(encoding="utf-8"))
    protocols_id = "lesson.info1.networks.protocols.v1"
    protocols_objective = "obj.info1.networks.protocols.001.v1"
    protocols = {
        **variables,
        "id": protocols_id,
        "title": "ネットワークとプロトコル",
        "unit": "ネットワークとデータ",
        "body_ref": "lessons/highschool_information_i/networks/00_first_by_filename.md",
    }
    write_ndjson(lessons_path, [protocols, variables])
    protocols_body = sample_root / protocols["body_ref"]
    protocols_body.parent.mkdir(parents=True)
    protocols_body.write_text("# ネットワークとプロトコル\n\n本文です。\n", encoding="utf-8")
    protocols_teacher = sample_root / "teacher_guides/highschool_information_i/networks/00_first_by_filename.md"
    protocols_teacher.parent.mkdir(parents=True)
    protocols_teacher.write_text("# 教師用ガイド\n\n指導用です。\n", encoding="utf-8")
    write_curriculum(
        sample_root / "curriculum/highschool_information_i.curriculum.json",
        [
            {
                "id": "unit.info1.programming.v1",
                "title": "Computers, Algorithms, and Programming",
                "lessons": [curriculum_lesson(
                    str(variables["id"]),
                    "C2",
                    "Variables and Assignment",
                    "obj.info1.programming.variables.002.v1",
                )],
            },
            {
                "id": "unit.info1.networks.data.v1",
                "title": "Networks, Information Systems, and Data",
                "lessons": [curriculum_lesson(
                    protocols_id,
                    "D1",
                    "Networks and Protocols",
                    protocols_objective,
                )],
            },
        ],
    )

    result = run_builder(sample_root)
    assert result.returncode == 0, result.stdout + result.stderr
    site = sample_root / "build/site"
    index = (site / "index.html").read_text(encoding="utf-8")
    variables_page = (site / "lessons/programming-variables.html").read_text(encoding="utf-8")
    protocols_page = (site / "lessons/networks-protocols.html").read_text(encoding="utf-8")

    assert index.index("programming-variables.html") < index.index("networks-protocols.html")
    assert index.count('class="curriculum-unit"') == 2
    assert 'rel="next" href="networks-protocols.html"' in variables_page
    assert 'rel="prev" href="programming-variables.html"' in protocols_page
    assert not (site / "lessons/00-first-by-filename.html").exists()


def test_problem_objective_must_belong_to_referenced_curriculum_lesson(sample_root: Path) -> None:
    problems = sample_root / "data" / "collections" / "problems.ndjson"
    problem = json.loads(problems.read_text(encoding="utf-8"))
    problem["objective_refs"] = ["obj.info1.networks.protocols.001.v1"]
    write_ndjson(problems, [problem])

    result = run_builder(sample_root)
    assert result.returncode == 1
    assert "objective_refs must belong to a referenced curriculum lesson" in result.stderr


def test_replace_retries_transient_permission_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "destination"
    source.mkdir()
    real_replace = build_static_site.os.replace
    calls = 0

    def flaky_replace(first: Path, second: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise PermissionError("transient lock")
        real_replace(first, second)

    monkeypatch.setattr(build_static_site.os, "replace", flaky_replace)
    monkeypatch.setattr(build_static_site.time, "sleep", lambda _: None)

    build_static_site.replace_with_retry(source, destination)

    assert calls == 2
    assert destination.is_dir()
