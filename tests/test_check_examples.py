#!/usr/bin/env python3
"""Tests for isolated Python example checking."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import check_examples


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_examples.py"


def write_ndjson(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def base_records() -> tuple[list[dict], list[dict], list[dict]]:
    lesson_id = "lesson.test.python.examples.v1"
    predict_id = "prob.test.python.predict.v1"
    code_id = "prob.test.python.code.v1"
    predict_answer_id = "ans.prob.test.python.predict.v1"
    code_answer_id = "ans.prob.test.python.code.v1"
    lessons = [{
        "id": lesson_id,
        "type": "lesson",
        "body_ref": "lessons/test.md",
    }]
    problems = [
        {
            "id": predict_id,
            "type": "problem",
            "question_type": "predict_output",
            "question": "Predict the output.\n\n```python\nprint(\"value \")\n```",
            "answer_refs": [predict_answer_id],
            "lesson_refs": [lesson_id],
        },
        {
            "id": code_id,
            "type": "problem",
            "question_type": "short_code",
            "question": "Assign 80 to score.",
            "answer_refs": [code_answer_id],
            "lesson_refs": [lesson_id],
        },
    ]
    answers = [
        {
            "id": predict_answer_id,
            "type": "answer",
            "problem_id": predict_id,
            "answer_type": "text",
            "canonical_answer": "value ",
            "acceptable_answers": [],
        },
        {
            "id": code_answer_id,
            "type": "answer",
            "problem_id": code_id,
            "answer_type": "code",
            "canonical_answer": "score = 80",
            "acceptable_answers": ["score=80"],
        },
    ]
    return lessons, problems, answers


@pytest.fixture
def example_root(tmp_path: Path) -> Path:
    lessons, problems, answers = base_records()
    write_ndjson(tmp_path / "data" / "collections" / "lessons.ndjson", lessons)
    write_ndjson(tmp_path / "data" / "collections" / "problems.ndjson", problems)
    write_ndjson(tmp_path / "data" / "collections" / "answers.ndjson", answers)
    lesson = tmp_path / "lessons" / "test.md"
    lesson.parent.mkdir(parents=True)
    lesson.write_text(
        "# Test\n\n## Example\n\n```python\nscore = 80\nprint(score)\n```\n\n"
        "## Common Mistakes\n\n```python\nprint(not_assigned)\n```\n",
        encoding="utf-8",
    )
    return tmp_path


def read_records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_valid_examples_answers_and_predict_output_pass(example_root: Path) -> None:
    failures, stats = check_examples.check_repository(example_root, timeout=1)

    assert failures == []
    assert stats.lesson_blocks == 2
    assert stats.problem_blocks == 1
    assert stats.code_answers == 2


@pytest.mark.parametrize(
    ("source", "message"),
    [
        ("import math", "imports are not allowed"),
        ('open("created.txt", "w")', "dangerous call is not allowed: open()"),
        ('socket.connect(("example.com", 80))', "module access is not allowed: socket"),
        ('subprocess.run(["echo", "unsafe"])', "module access is not allowed: subprocess"),
        ("input()", "dangerous call is not allowed: input()"),
        ('eval("1 + 1")', "dangerous call is not allowed: eval()"),
        ('exec("value = 1")', "dangerous call is not allowed: exec()"),
        ("bytearray(2_000_000_000)", "dangerous builtin access is not allowed: bytearray"),
        ("value = 2_000_000_000", "integer literal exceeds 100000000"),
        ("items = [0] * 100_000_000", "sequence repetition exceeds 100000 items"),
        ("items = [0] * (10 ** 8)", "sequence repetition exceeds 100000 items"),
        ("items = list(range(10 ** 8))", "materialized range exceeds 100000 items"),
    ],
)
def test_dangerous_lesson_code_is_rejected_before_execution(
    example_root: Path,
    source: str,
    message: str,
) -> None:
    (example_root / "lessons" / "test.md").write_text(
        f"# Test\n\n## Example\n\n```python\n{source}\n```\n",
        encoding="utf-8",
    )

    failures, _ = check_examples.check_repository(example_root, timeout=1)

    assert any(message in failure for failure in failures)


def test_dangerous_code_in_common_mistakes_is_still_rejected(example_root: Path) -> None:
    (example_root / "lessons" / "test.md").write_text(
        '# Test\n\n## Common Mistakes\n\n```python\nopen("created.txt", "w")\n```\n',
        encoding="utf-8",
    )

    failures, _ = check_examples.check_repository(example_root, timeout=1)

    assert any("dangerous call is not allowed: open()" in failure for failure in failures)


def test_normal_remove_and_replace_methods_are_allowed_by_ast() -> None:
    source = 'items = [1]\nitems.remove(1)\nprint("a".replace("a", "b"))\n'

    assert check_examples.ast_safety_failures(source, "normal methods") == []


def test_timeout_is_reported_clearly(example_root: Path) -> None:
    (example_root / "lessons" / "test.md").write_text(
        "# Test\n\n## Example\n\n```python\nwhile True:\n    pass\n```\n",
        encoding="utf-8",
    )

    failures, _ = check_examples.check_repository(example_root, timeout=0.1)

    assert any("timed out after 0.1 seconds" in failure for failure in failures)
    assert any("lesson lesson.test.python.examples.v1" in failure for failure in failures)


def test_excessive_stdout_is_stopped_and_reported(example_root: Path) -> None:
    (example_root / "lessons" / "test.md").write_text(
        '# Test\n\n## Example\n\n```python\nprint("x" * 70000)\n```\n',
        encoding="utf-8",
    )

    failures, _ = check_examples.check_repository(example_root, timeout=3)

    assert any("stdout exceeded 65536 bytes" in failure for failure in failures)


def test_nondeterministic_stdout_is_rejected(example_root: Path) -> None:
    (example_root / "lessons" / "test.md").write_text(
        '# Test\n\n## Example\n\n```python\nprint(hash("determinism-probe"))\n```\n',
        encoding="utf-8",
    )

    failures, _ = check_examples.check_repository(example_root, timeout=1)

    assert any("stdout is not deterministic" in failure for failure in failures)


def test_code_answer_variants_must_execute_without_error(example_root: Path) -> None:
    path = example_root / "data" / "collections" / "answers.ndjson"
    answers = read_records(path)
    answers[1]["acceptable_answers"].append('raise RuntimeError("bad variant")')
    write_ndjson(path, answers)

    failures, _ = check_examples.check_repository(example_root, timeout=1)

    assert any(
        "answer ans.prob.test.python.code.v1 acceptable_answers[1]" in failure
        and "execution exited with status" in failure
        for failure in failures
    )


def test_predict_output_preserves_non_line_ending_whitespace(example_root: Path) -> None:
    path = example_root / "data" / "collections" / "answers.ndjson"
    answers = read_records(path)
    answers[0]["canonical_answer"] = "value"
    write_ndjson(path, answers)

    failures, _ = check_examples.check_repository(example_root, timeout=1)

    assert any(
        "stdout does not match linked canonical answer" in failure
        and "actual='value '" in failure
        and "expected='value'" in failure
        for failure in failures
    )


def test_predict_output_removes_only_one_final_line_ending(example_root: Path) -> None:
    problems_path = example_root / "data" / "collections" / "problems.ndjson"
    problems = read_records(problems_path)
    problems[0]["question"] = 'Predict.\n\n```python\nprint("line 1\\n")\n```'
    write_ndjson(problems_path, problems)

    answers_path = example_root / "data" / "collections" / "answers.ndjson"
    answers = read_records(answers_path)
    answers[0]["canonical_answer"] = "line 1"
    write_ndjson(answers_path, answers)

    failures, _ = check_examples.check_repository(example_root, timeout=1)

    assert any(
        "stdout does not match linked canonical answer" in failure
        and "actual='line 1" in failure
        and "expected='line 1'" in failure
        for failure in failures
    )


@pytest.mark.parametrize(
    ("stdout", "expected"),
    [
        (b"value\r\n", b"value"),
        (b"value\n", b"value"),
        (b"value\r", b"value"),
        (b"value\n\n", b"value\n"),
        (b"value \r\n", b"value "),
    ],
)
def test_remove_one_final_line_ending(stdout: bytes, expected: bytes) -> None:
    assert check_examples.remove_one_final_line_ending(stdout) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (b"line 1\r\nline 2", b"line 1\nline 2"),
        (b"line 1\nline 2", b"line 1\nline 2"),
        (b"line 1\rline 2", b"line 1\nline 2"),
    ],
)
def test_normalize_line_endings(value: bytes, expected: bytes) -> None:
    assert check_examples.normalize_line_endings(value) == expected


def test_cli_supports_root_and_reports_clear_failure(example_root: Path) -> None:
    (example_root / "lessons" / "test.md").write_text(
        "# Test\n\n## Example\n\n```python\n1 / 0\n```\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(example_root)],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "Python example check failed with" in result.stderr
    assert "lessons/test.md:6" in result.stderr
    assert "execution exited with status" in result.stderr


def test_current_repository_examples_pass() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(ROOT)],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Python example check passed" in result.stdout
