#!/usr/bin/env python3
"""Validate and execute repository Python examples without third-party packages."""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from typing import BinaryIO
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TIMEOUT_SECONDS = 2.0
MAX_OUTPUT_BYTES = 64 * 1024
MAX_SOURCE_BYTES = 128 * 1024
MAX_LITERAL_INTEGER = 100_000_000
MAX_LITERAL_TEXT_BYTES = 64 * 1024
MAX_CONTAINER_ITEMS = 10_000
MAX_REPETITION_ITEMS = 100_000
MAX_PROCESS_MEMORY_BYTES = 256 * 1024 * 1024
PROCESS_POLL_SECONDS = 0.01
FENCE_RE = re.compile(
    r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>.*?)[ \t]*$"
)
H2_RE = re.compile(r"^ {0,3}##(?!#)[ \t]+(?P<title>.*?)[ \t]*#*[ \t]*$")
# These sections contain intentionally failing demonstrations. Their blocks are
# still parsed and AST-checked, but only ordinary lesson blocks are executed.
NON_RUNNABLE_SECTIONS = {"common mistakes", "よくある間違い"}

DANGEROUS_CALLS = {
    "__import__",
    "breakpoint",
    "bytearray",
    "compile",
    "delattr",
    "dir",
    "eval",
    "exec",
    "exit",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "memoryview",
    "open",
    "quit",
    "setattr",
    "vars",
}
DANGEROUS_MODULE_NAMES = {
    "asyncio",
    "ftplib",
    "http",
    "multiprocessing",
    "os",
    "pathlib",
    "requests",
    "shutil",
    "signal",
    "smtplib",
    "socket",
    "subprocess",
    "sys",
    "tempfile",
    "urllib",
}
DANGEROUS_ATTRIBUTES = {
    "accept",
    "bind",
    "chmod",
    "chown",
    "connect",
    "connect_ex",
    "fork",
    "forkpty",
    "kill",
    "listen",
    "makedirs",
    "mkdir",
    "open",
    "popen",
    "read_bytes",
    "read_text",
    "recv",
    "recvfrom",
    "removedirs",
    "rename",
    "renames",
    "request",
    "rmdir",
    "send",
    "sendall",
    "sendto",
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "startfile",
    "system",
    "touch",
    "unlink",
    "urlopen",
    "urlretrieve",
    "write_bytes",
    "write_text",
}


@dataclass(frozen=True)
class PythonBlock:
    source: str
    line: int
    executable: bool = True


@dataclass(frozen=True)
class ExecutionResult:
    returncode: int
    stdout: bytes
    stderr: bytes


@dataclass
class CheckStats:
    lesson_blocks: int = 0
    problem_blocks: int = 0
    code_answers: int = 0


class ExampleCheckError(RuntimeError):
    """Raised for a repository-level input error that prevents checking."""


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_ndjson(root: Path, filename: str) -> list[dict]:
    path = root / "data" / "collections" / filename
    if not path.is_file():
        raise ExampleCheckError(f"missing collection: {relative_path(path, root)}")

    records: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ExampleCheckError(
            f"cannot read {relative_path(path, root)}: {exc}"
        ) from exc

    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ExampleCheckError(
                f"{relative_path(path, root)}:{line_no}: invalid JSON: {exc}"
            ) from exc
        if not isinstance(record, dict):
            raise ExampleCheckError(
                f"{relative_path(path, root)}:{line_no}: record must be an object"
            )
        record["_collection_file"] = relative_path(path, root)
        record["_collection_line"] = line_no
        records.append(record)
    return records


def is_python_info(info: str) -> bool:
    parts = info.strip().split()
    return bool(parts) and parts[0].casefold() in {"python", "py"}


def extract_python_blocks(text: str, *, markdown_sections: bool) -> list[PythonBlock]:
    blocks: list[PythonBlock] = []
    lines = text.splitlines(keepends=True)
    current_h2 = ""
    index = 0

    while index < len(lines):
        line_without_ending = lines[index].rstrip("\r\n")
        if markdown_sections:
            heading = H2_RE.match(line_without_ending)
            if heading:
                current_h2 = heading.group("title").strip().casefold()

        opening = FENCE_RE.match(line_without_ending)
        if opening is None:
            index += 1
            continue

        fence = opening.group("fence")
        fence_char = fence[0]
        minimum_length = len(fence)
        info = opening.group("info")
        block_line = index + 2
        content: list[str] = []
        index += 1

        while index < len(lines):
            candidate = lines[index].rstrip("\r\n")
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_char)}{{{minimum_length},}}[ \t]*$",
                candidate,
            )
            if closing:
                break
            content.append(lines[index])
            index += 1

        if index >= len(lines):
            raise ExampleCheckError(
                f"line {block_line - 1}: unclosed Markdown fence"
            )

        if is_python_info(info):
            blocks.append(
                PythonBlock(
                    source="".join(content),
                    line=block_line,
                    executable=current_h2 not in NON_RUNNABLE_SECTIONS,
                )
            )
        index += 1

    return blocks


def call_path(node: ast.expr) -> tuple[str, ...]:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return tuple(reversed(parts))


def static_integer(node: ast.AST, limit: int = MAX_REPETITION_ITEMS) -> int | None:
    """Evaluate simple integer syntax while capping expensive operations."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = static_integer(node.operand, limit)
        if value is None:
            return None
        return value if isinstance(node.op, ast.UAdd) else -value
    if not isinstance(node, ast.BinOp):
        return None
    left = static_integer(node.left, limit)
    right = static_integer(node.right, limit)
    if left is None or right is None:
        return None
    try:
        if isinstance(node.op, ast.Add):
            value = left + right
        elif isinstance(node.op, ast.Sub):
            value = left - right
        elif isinstance(node.op, ast.Mult):
            value = left * right
        elif isinstance(node.op, ast.FloorDiv) and right:
            value = left // right
        elif isinstance(node.op, ast.Pow) and 0 <= right <= 64:
            value = pow(left, right)
        else:
            return None
    except (ArithmeticError, OverflowError):
        return limit + 1
    if abs(value) > limit:
        return limit + 1 if value >= 0 else -(limit + 1)
    return value


def range_size(call: ast.Call) -> int | None:
    if call_path(call.func) != ("range",) or call.keywords or not 1 <= len(call.args) <= 3:
        return None
    values = [static_integer(argument) for argument in call.args]
    if any(value is None for value in values):
        return None
    try:
        return len(range(*values))
    except (TypeError, ValueError, OverflowError):
        return MAX_REPETITION_ITEMS + 1


def ast_safety_failures(source: str, label: str) -> list[str]:
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        return [f"source exceeds {MAX_SOURCE_BYTES} UTF-8 bytes"]
    try:
        tree = ast.parse(source, filename=label, mode="exec")
    except SyntaxError as exc:
        location = f"line {exc.lineno}" if exc.lineno is not None else "unknown line"
        return [f"syntax error at {location}: {exc.msg}"]

    failures: list[str] = []
    seen: set[tuple[int, str]] = set()

    def add(node: ast.AST, message: str) -> None:
        key = (getattr(node, "lineno", 0), message)
        if key not in seen:
            seen.add(key)
            failures.append(f"AST line {key[0]}: {message}")

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                if abs(node.value) > MAX_LITERAL_INTEGER:
                    add(node, f"integer literal exceeds {MAX_LITERAL_INTEGER}")
            elif isinstance(node.value, (str, bytes)):
                size = len(node.value.encode("utf-8")) if isinstance(node.value, str) else len(node.value)
                if size > MAX_LITERAL_TEXT_BYTES:
                    add(node, f"text or bytes literal exceeds {MAX_LITERAL_TEXT_BYTES} bytes")
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)) and len(node.elts) > MAX_CONTAINER_ITEMS:
            add(node, f"container literal exceeds {MAX_CONTAINER_ITEMS} items")
        if isinstance(node, ast.Dict) and len(node.keys) > MAX_CONTAINER_ITEMS:
            add(node, f"dict literal exceeds {MAX_CONTAINER_ITEMS} items")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            sequence_side = None
            count_side = None
            if isinstance(node.left, (ast.List, ast.Tuple, ast.Constant)):
                sequence_side, count_side = node.left, node.right
            elif isinstance(node.right, (ast.List, ast.Tuple, ast.Constant)):
                sequence_side, count_side = node.right, node.left
            is_sequence_literal = isinstance(sequence_side, (ast.List, ast.Tuple)) or (
                isinstance(sequence_side, ast.Constant)
                and isinstance(sequence_side.value, (str, bytes))
            )
            if sequence_side is not None and is_sequence_literal:
                count = static_integer(count_side) if count_side is not None else None
                if count is not None and abs(count) > MAX_REPETITION_ITEMS:
                    add(node, f"sequence repetition exceeds {MAX_REPETITION_ITEMS} items")
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp)):
            for generator in node.generators:
                if isinstance(generator.iter, ast.Call):
                    size = range_size(generator.iter)
                    if size is not None and size > MAX_REPETITION_ITEMS:
                        add(node, f"comprehension range exceeds {MAX_REPETITION_ITEMS} items")
        if isinstance(node, ast.Call):
            path = call_path(node.func)
            if path == ("bytes",) and len(node.args) == 1:
                size = static_integer(node.args[0])
                if size is not None and size > MAX_REPETITION_ITEMS:
                    add(node, f"bytes allocation exceeds {MAX_REPETITION_ITEMS} items")
            if path in {("list",), ("tuple",), ("set",)} and len(node.args) == 1:
                source = node.args[0]
                if isinstance(source, ast.Call):
                    size = range_size(source)
                    if size is not None and size > MAX_REPETITION_ITEMS:
                        add(node, f"materialized range exceeds {MAX_REPETITION_ITEMS} items")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            add(node, "imports are not allowed")
            continue
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            add(node, f"dunder attribute access is not allowed: {node.attr}")
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id.startswith("__"):
                add(node, f"dunder name access is not allowed: {node.id}")
            if node.id in DANGEROUS_CALLS:
                add(node, f"dangerous builtin access is not allowed: {node.id}")
            if node.id in DANGEROUS_MODULE_NAMES:
                add(node, f"module access is not allowed: {node.id}")
        if not isinstance(node, ast.Call):
            continue
        path = call_path(node.func)
        if not path:
            continue
        first = path[0]
        last = path[-1]
        if len(path) == 1 and last in DANGEROUS_CALLS:
            add(node, f"dangerous call is not allowed: {last}()")
        if first in DANGEROUS_MODULE_NAMES:
            add(node, f"module call is not allowed: {'.'.join(path)}()")
        if len(path) > 1 and last.casefold() in DANGEROUS_ATTRIBUTES:
            add(node, f"dangerous method is not allowed: {last}()")

    return failures


def subprocess_environment() -> dict[str, str]:
    allowed = ("COMSPEC", "PATH", "SYSTEMDRIVE", "SYSTEMROOT", "TEMP", "TMP", "WINDIR")
    return {name: os.environ[name] for name in allowed if name in os.environ}


def apply_posix_resource_limits() -> None:
    """Bound accidental allocation in the Linux/macOS validation child."""
    import resource

    for limit_name in ("RLIMIT_AS", "RLIMIT_DATA"):
        limit = getattr(resource, limit_name, None)
        if limit is None:
            continue
        try:
            resource.setrlimit(limit, (MAX_PROCESS_MEMORY_BYTES, MAX_PROCESS_MEMORY_BYTES))
        except (OSError, ValueError):
            pass


def run_once(source: str, timeout: float) -> ExecutionResult:
    with tempfile.TemporaryDirectory(prefix="check-examples-") as workdir:
        try:
            process = subprocess.Popen(
                [sys.executable, "-I", "-X", "utf8", "-c", source],
                cwd=workdir,
                env=subprocess_environment(),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=apply_posix_resource_limits if os.name == "posix" else None,
            )
        except OSError as exc:
            raise ExampleCheckError(f"could not start isolated Python: {exc}") from exc

        outputs = {"stdout": bytearray(), "stderr": bytearray()}
        overflow_streams: list[str] = []
        overflow_event = threading.Event()

        def drain(stream_name: str, stream: BinaryIO) -> None:
            buffer = outputs[stream_name]
            while True:
                chunk = stream.read(8192)
                if not chunk:
                    break
                remaining = MAX_OUTPUT_BYTES - len(buffer)
                if remaining > 0:
                    buffer.extend(chunk[:remaining])
                if len(chunk) > remaining and stream_name not in overflow_streams:
                    overflow_streams.append(stream_name)
                    overflow_event.set()
            stream.close()

        assert process.stdout is not None and process.stderr is not None
        readers = [
            threading.Thread(target=drain, args=("stdout", process.stdout), daemon=True),
            threading.Thread(target=drain, args=("stderr", process.stderr), daemon=True),
        ]
        for reader in readers:
            reader.start()

        deadline = time.monotonic() + timeout
        failure: str | None = None
        while process.poll() is None:
            if overflow_event.is_set():
                failure = f"{overflow_streams[0]} exceeded {MAX_OUTPUT_BYTES} bytes"
                try:
                    process.kill()
                except OSError:
                    pass
                break
            if time.monotonic() >= deadline:
                failure = f"timed out after {timeout:g} seconds"
                try:
                    process.kill()
                except OSError:
                    pass
                break
            time.sleep(PROCESS_POLL_SECONDS)

        process.wait()
        for reader in readers:
            reader.join()
        if failure is None and overflow_streams:
            failure = f"{overflow_streams[0]} exceeded {MAX_OUTPUT_BYTES} bytes"
        if failure is not None:
            raise ExampleCheckError(failure)

    return ExecutionResult(process.returncode, bytes(outputs["stdout"]), bytes(outputs["stderr"]))


def display_bytes(value: bytes, limit: int = 500) -> str:
    decoded = value.decode("utf-8", errors="backslashreplace")
    if len(decoded) > limit:
        decoded = decoded[:limit] + "..."
    return repr(decoded)


def execute_checked(
    source: str,
    label: str,
    failures: list[str],
    timeout: float,
) -> ExecutionResult | None:
    safety_failures = ast_safety_failures(source, label)
    if safety_failures:
        failures.extend(f"{label}: {message}" for message in safety_failures)
        return None

    try:
        first = run_once(source, timeout)
    except ExampleCheckError as exc:
        failures.append(f"{label}: {exc}")
        return None
    if first.returncode != 0:
        failures.append(
            f"{label}: execution exited with status {first.returncode}: "
            f"stderr={display_bytes(first.stderr)}"
        )
        return None

    try:
        second = run_once(source, timeout)
    except ExampleCheckError as exc:
        failures.append(f"{label}: second execution {exc}")
        return None
    if second.returncode != 0:
        failures.append(
            f"{label}: second execution exited with status {second.returncode}: "
            f"stderr={display_bytes(second.stderr)}"
        )
        return None
    if first.stdout != second.stdout:
        failures.append(
            f"{label}: stdout is not deterministic: "
            f"first={display_bytes(first.stdout)}, second={display_bytes(second.stdout)}"
        )
        return None
    return first


def remove_one_final_line_ending(stdout: bytes) -> bytes:
    if stdout.endswith(b"\r\n"):
        return stdout[:-2]
    if stdout.endswith((b"\r", b"\n")):
        return stdout[:-1]
    return stdout


def normalize_line_endings(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def as_source(value: object, label: str, failures: list[str]) -> str | None:
    if not isinstance(value, str):
        failures.append(f"{label}: code must be a string")
        return None
    return value


def record_location(record: dict) -> str:
    return f"{record['_collection_file']}:{record['_collection_line']}"


def check_repository(
    root: Path,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> tuple[list[str], CheckStats]:
    if timeout <= 0:
        raise ExampleCheckError("timeout must be greater than zero")
    root = root.resolve()
    if not root.is_dir():
        raise ExampleCheckError(f"repository root is not a directory: {root}")

    lessons = load_ndjson(root, "lessons.ndjson")
    problems = load_ndjson(root, "problems.ndjson")
    answers = load_ndjson(root, "answers.ndjson")
    failures: list[str] = []
    stats = CheckStats()

    answers_by_id: dict[str, dict] = {}
    for answer in answers:
        answer_id = answer.get("id")
        if not isinstance(answer_id, str) or not answer_id:
            failures.append(f"{record_location(answer)}: answer is missing id")
            continue
        if answer_id in answers_by_id:
            failures.append(f"{record_location(answer)}: duplicate answer id: {answer_id}")
            continue
        answers_by_id[answer_id] = answer

    for lesson in lessons:
        lesson_id = lesson.get("id", "<missing-id>")
        body_ref = lesson.get("body_ref")
        if not isinstance(body_ref, str) or not body_ref:
            failures.append(f"{record_location(lesson)}: {lesson_id}: missing body_ref")
            continue
        body_path = (root / body_ref).resolve()
        if not body_path.is_relative_to(root):
            failures.append(
                f"{record_location(lesson)}: {lesson_id}: body_ref escapes root: {body_ref}"
            )
            continue
        if not body_path.is_file():
            failures.append(
                f"{record_location(lesson)}: {lesson_id}: missing body_ref file: {body_ref}"
            )
            continue
        try:
            text = body_path.read_text(encoding="utf-8")
            blocks = extract_python_blocks(text, markdown_sections=True)
        except (OSError, UnicodeError, ExampleCheckError) as exc:
            failures.append(f"{body_ref}: {lesson_id}: {exc}")
            continue
        for number, block in enumerate(blocks, start=1):
            stats.lesson_blocks += 1
            label = f"{body_ref}:{block.line}: lesson {lesson_id} python block {number}"
            safety_failures = ast_safety_failures(block.source, label)
            if safety_failures:
                failures.extend(f"{label}: {message}" for message in safety_failures)
            elif block.executable:
                execute_checked(block.source, label, failures, timeout)

    problem_results: dict[str, tuple[list[PythonBlock], list[ExecutionResult | None]]] = {}
    for problem in problems:
        problem_id = problem.get("id", "<missing-id>")
        question = problem.get("question")
        if not isinstance(question, str):
            failures.append(f"{record_location(problem)}: {problem_id}: question must be a string")
            continue
        try:
            blocks = extract_python_blocks(question, markdown_sections=False)
        except ExampleCheckError as exc:
            failures.append(f"{record_location(problem)}: {problem_id}: question: {exc}")
            continue
        results: list[ExecutionResult | None] = []
        for number, block in enumerate(blocks, start=1):
            stats.problem_blocks += 1
            label = (
                f"{record_location(problem)}: problem {problem_id} question "
                f"python block {number} (question line {block.line})"
            )
            results.append(execute_checked(block.source, label, failures, timeout))
        if isinstance(problem_id, str):
            problem_results[problem_id] = (blocks, results)

    for answer in answers:
        if answer.get("answer_type") != "code":
            continue
        answer_id = answer.get("id", "<missing-id>")
        variants: list[tuple[str, object]] = [("canonical_answer", answer.get("canonical_answer"))]
        acceptable = answer.get("acceptable_answers", [])
        if not isinstance(acceptable, list):
            failures.append(
                f"{record_location(answer)}: answer {answer_id}: acceptable_answers must be a list"
            )
            acceptable = []
        variants.extend(
            (f"acceptable_answers[{index}]", value)
            for index, value in enumerate(acceptable)
        )
        for field, value in variants:
            stats.code_answers += 1
            label = f"{record_location(answer)}: answer {answer_id} {field}"
            source = as_source(value, label, failures)
            if source is not None:
                execute_checked(source, label, failures, timeout)

    for problem in problems:
        if problem.get("question_type") != "predict_output":
            continue
        problem_id = problem.get("id", "<missing-id>")
        blocks, results = problem_results.get(str(problem_id), ([], []))
        location = f"{record_location(problem)}: problem {problem_id}"
        if len(blocks) != 1:
            failures.append(
                f"{location}: predict_output requires exactly one python block; found {len(blocks)}"
            )
            continue
        if not results or results[0] is None:
            continue
        actual = normalize_line_endings(remove_one_final_line_ending(results[0].stdout))
        answer_refs = problem.get("answer_refs")
        if not isinstance(answer_refs, list) or not answer_refs:
            failures.append(f"{location}: predict_output requires linked answer_refs")
            continue
        for answer_ref in answer_refs:
            answer = answers_by_id.get(answer_ref) if isinstance(answer_ref, str) else None
            if answer is None:
                failures.append(f"{location}: linked answer not found: {answer_ref!r}")
                continue
            if answer.get("problem_id") != problem_id:
                failures.append(
                    f"{location}: linked answer {answer_ref} belongs to another problem"
                )
                continue
            expected = answer.get("canonical_answer")
            if not isinstance(expected, str):
                failures.append(
                    f"{location}: linked answer {answer_ref} canonical_answer must be a string"
                )
                continue
            expected_bytes = normalize_line_endings(expected.encode("utf-8"))
            if actual != expected_bytes:
                failures.append(
                    f"{location}: stdout does not match linked canonical answer {answer_ref}: "
                    f"actual={display_bytes(actual)}, expected={display_bytes(expected_bytes)}"
                )

    return failures, stats


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="Repository root. Defaults to the parent of this script directory.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Per-process timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS:g}).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        failures, stats = check_repository(args.root, timeout=args.timeout)
    except ExampleCheckError as exc:
        print(f"Python example check failed: {exc}", file=sys.stderr)
        return 1

    if failures:
        print(
            f"Python example check failed with {len(failures)} finding(s):",
            file=sys.stderr,
        )
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        "Python example check passed: "
        f"{stats.lesson_blocks} lesson block(s), "
        f"{stats.problem_blocks} problem block(s), and "
        f"{stats.code_answers} code answer variant(s) checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
