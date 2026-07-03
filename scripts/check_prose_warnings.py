#!/usr/bin/env python3
"""Emit warning-only prompts for machine-detectable prose issues.

The script intentionally uses only the Python standard library. Warning
findings exit with status 0; only invalid usage or runtime errors should fail.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TARGETS = [
    Path('docs'),
    Path('prompts'),
    Path('.github/ISSUE_TEMPLATE'),
    Path('.github/PULL_REQUEST_TEMPLATE.md'),
]

EXCLUDED_DIRS = {'.git', 'build', '__pycache__'}
TEXT_SUFFIXES = {
    '.adoc',
    '.cfg',
    '.ini',
    '.md',
    '.rst',
    '.text',
    '.toml',
    '.txt',
    '.yaml',
    '.yml',
}

LONG_LINE_LIMIT = 140
LONG_SENTENCE_WORD_LIMIT = 45
LONG_SENTENCE_CHAR_LIMIT = 180

# Keep this source file UTF-8 so Japanese warning phrases remain matchable.
VAGUE_PHRASES = [
    '重要です',
    '理解を深める',
    'しっかり',
    'さまざま',
    '非常に',
    '見ていきましょう',
    '役立ちます',
    'it is important to',
    'delve into',
    'unlock the power of',
    "in today's world",
    'seamlessly',
    'robust',
    'leverage',
    'elevate',
]

REPEATED_PHRASES = [
    'as needed',
    'as appropriate',
    'at a high level',
    'in order to',
    'this means that',
    'keep in mind',
]

DETECTOR_FRAMING = [
    'ai detector',
    'ai detection',
    'ai-like',
    'ai slop',
    'ai tells',
    'bypass detector',
    'bypass ai',
    'humanizer',
    'humanize',
    'make it sound human',
    'undetectable ai',
]

STALE_PATHS = {
    'docs/MVP_REVIEW_CHECKLIST.md': 'docs/review/MVP_REVIEW_CHECKLIST.md',
}

HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
SENTENCE_RE = re.compile(r'[^.!?。！？]+[.!?。！？]')
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")


@dataclass(frozen=True)
class WarningFinding:
    path: Path
    line: int
    column: int
    category: str
    message: str


class ProseCheckError(RuntimeError):
    """Raised for user-visible runtime errors."""


def rel_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_excluded(path: Path) -> bool:
    rel = path.resolve().relative_to(ROOT.resolve()) if path.resolve().is_relative_to(ROOT.resolve()) else path
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return True
    return len(rel.parts) >= 3 and rel.parts[0:2] == ('data', 'collections') and path.suffix == '.ndjson'


def is_text_like(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def is_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError as exc:
        raise ProseCheckError(f'cannot read {rel_path(path)}: {exc}') from exc
    return b'\0' in chunk


def iter_target_files(targets: list[Path], explicit: bool) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        path = target if target.is_absolute() else ROOT / target
        if not path.exists():
            if explicit:
                raise ProseCheckError(f'explicit path does not exist: {target}')
            continue
        if path.is_file():
            if is_excluded(path):
                continue
            if not is_text_like(path) or is_binary(path):
                continue
            files.append(path)
            continue
        if path.is_dir():
            for child in sorted(path.rglob('*')):
                if not child.is_file() or is_excluded(child):
                    continue
                if not is_text_like(child) or is_binary(child):
                    continue
                files.append(child)
            continue
        if explicit:
            raise ProseCheckError(f'explicit path is not a regular file or directory: {target}')
    return sorted(set(files))


def strip_markdown_noise(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ''
    if stripped.startswith(('#', '|', '>', '- [', '* [', '- ', '* ', '```')):
        return ''
    return stripped


def iter_non_code_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_code = False
    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        lines.append((line_no, line))
    return lines


def add_phrase_warnings(
    findings: list[WarningFinding],
    path: Path,
    lines: list[tuple[int, str]],
    category: str,
    phrases: list[str],
    message: str,
) -> None:
    lowered = [(line_no, line.lower()) for line_no, line in lines]
    matches_by_line: dict[int, list[tuple[int, int]]] = {}
    for phrase in sorted(phrases, key=len, reverse=True):
        phrase_lower = phrase.lower()
        pattern = re.compile(rf'(?<![A-Za-z0-9]){re.escape(phrase_lower)}(?![A-Za-z0-9])')
        for line_no, line in lowered:
            match = pattern.search(line)
            if match is None:
                continue
            span = match.span()
            existing = matches_by_line.setdefault(line_no, [])
            if any(max(start, span[0]) < min(end, span[1]) for start, end in existing):
                continue
            existing.append(span)
            findings.append(
                WarningFinding(
                    path,
                    line_no,
                    span[0] + 1,
                    category,
                    f'{message}: {phrase!r}',
                )
            )


def check_file(path: Path) -> list[WarningFinding]:
    try:
        raw = path.read_bytes()
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ProseCheckError(f'cannot decode {rel_path(path)} as UTF-8: {exc}') from exc
    except OSError as exc:
        raise ProseCheckError(f'cannot read {rel_path(path)}: {exc}') from exc

    findings: list[WarningFinding] = []
    if raw and not raw.endswith(b'\n'):
        line_count = text.count('\n') + 1
        findings.append(
            WarningFinding(
                path,
                line_count,
                1,
                'missing-final-newline',
                'file does not end with a final newline',
            )
        )

    non_code_lines = iter_non_code_lines(text)

    for line_no, line in non_code_lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            continue
        if len(line) > LONG_LINE_LIMIT and not re.search(r'https?://\S+', line):
            findings.append(
                WarningFinding(
                    path,
                    line_no,
                    LONG_LINE_LIMIT + 1,
                    'long-line',
                    f'line is {len(line)} characters; consider reviewing readability',
                )
            )

    for line_no, line in non_code_lines:
        prose_line = strip_markdown_noise(line)
        if not prose_line:
            continue
        for match in SENTENCE_RE.finditer(prose_line):
            sentence = match.group(0).strip()
            words = WORD_RE.findall(sentence)
            has_long_word_count = len(words) > LONG_SENTENCE_WORD_LIMIT
            has_long_char_count = len(sentence) > LONG_SENTENCE_CHAR_LIMIT and len(words) < 8
            if not has_long_word_count and not has_long_char_count:
                continue
            findings.append(
                WarningFinding(
                    path,
                    line_no,
                    line.find(sentence[:10]) + 1,
                    'long-sentence',
                    'sentence is long; consider whether it should be split for reviewability',
                )
            )

    add_phrase_warnings(
        findings,
        path,
        non_code_lines,
        'vague-phrase',
        VAGUE_PHRASES,
        'phrase may be vague or over-polished; review in context',
    )
    add_phrase_warnings(
        findings,
        path,
        non_code_lines,
        'detector-framing',
        DETECTOR_FRAMING,
        'detector-bypass framing can conflict with repository policy; review in context',
    )

    for phrase in REPEATED_PHRASES:
        seen = 0
        phrase_lower = phrase.lower()
        for line_no, line in [(line_no, line.lower()) for line_no, line in non_code_lines]:
            count = line.count(phrase_lower)
            if not count:
                continue
            seen += count
            if seen == 2:
                findings.append(
                    WarningFinding(
                        path,
                        line_no,
                        line.find(phrase_lower) + 1,
                        'repeated-phrase',
                        f'phrase appears repeatedly in this file; review for necessary repetition: {phrase!r}',
                    )
                )

    headings: dict[str, int] = {}
    for line_no, line in non_code_lines:
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = match.group(2).strip().casefold()
        first_line = headings.get(heading)
        if first_line is not None:
            findings.append(
                WarningFinding(
                    path,
                    line_no,
                    1,
                    'heading-duplicate',
                    f'heading duplicates line {first_line}: {match.group(2).strip()!r}',
                )
            )
        else:
            headings[heading] = line_no

    for stale, replacement in STALE_PATHS.items():
        for line_no, line in non_code_lines:
            column = line.find(stale)
            if column != -1:
                findings.append(
                    WarningFinding(
                        path,
                        line_no,
                        column + 1,
                        'stale-path',
                        f'path may be stale; review whether {replacement!r} is intended',
                    )
                )

    return findings


def escape_github(value: str) -> str:
    return value.replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')


def escape_github_property(value: str) -> str:
    return escape_github(value).replace(':', '%3A').replace(',', '%2C')


def emit_text(findings: list[WarningFinding]) -> None:
    if not findings:
        print('Prose warning check passed: no warning prompts found.')
        return
    print(
        f'Prose warning check found {len(findings)} review prompt(s). '
        'These are warnings only and do not approve or reject prose.'
    )
    for item in findings:
        print(
            f'{rel_path(item.path)}:{item.line}:{item.column}: '
            f'{item.category}: {item.message}'
        )


def emit_github(findings: list[WarningFinding]) -> None:
    if not findings:
        print('Prose warning check passed: no warning prompts found.')
        return
    print(
        f'Prose warning check found {len(findings)} review prompt(s). '
        'These are warnings only and do not approve or reject prose.'
    )
    for item in findings:
        file_name = escape_github_property(rel_path(item.path))
        title = escape_github_property(item.category)
        message = escape_github(item.message)
        print(f'::warning file={file_name},line={item.line},col={item.column},title={title}::{message}')


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', help='Optional files or directories to check.')
    parser.add_argument(
        '--format',
        choices=('text', 'github'),
        default='text',
        help='Output format. Use "github" for GitHub Actions warning annotations.',
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    explicit = bool(args.paths)
    targets = [Path(value) for value in args.paths] if explicit else DEFAULT_TARGETS

    try:
        files = iter_target_files(targets, explicit=explicit)
        findings: list[WarningFinding] = []
        for path in files:
            findings.extend(check_file(path))
    except ProseCheckError as exc:
        print(f'Prose warning check failed: {exc}', file=sys.stderr)
        return 2

    findings.sort(key=lambda item: (rel_path(item.path), item.line, item.column, item.category))
    if args.format == 'github':
        emit_github(findings)
    else:
        emit_text(findings)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
