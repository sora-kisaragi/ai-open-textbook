#!/usr/bin/env python3
"""Build an offline static textbook site from canonical Markdown and NDJSON."""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from string import Template

from markdown_it import MarkdownIt


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
COLLECTION_FILES = (
    "lessons.ndjson",
    "problems.ndjson",
    "answers.ndjson",
    "rubrics.ndjson",
    "sources.ndjson",
    "revisions.ndjson",
)


class SiteBuildError(RuntimeError):
    """Raised for a clear, user-facing static-site build failure."""


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def markdown_renderer() -> MarkdownIt:
    return MarkdownIt(
        "commonmark",
        {
            "html": False,
            "linkify": False,
            "typographer": False,
        },
    )


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


def validate_graph(root: Path, by_id: dict[str, dict], by_type: dict[str, list[dict]]) -> None:
    lessons = by_type.get("lesson", [])
    if not lessons:
        raise SiteBuildError("no lesson records found")

    for lesson in lessons:
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
        for ref in problem.get("lesson_refs", []) or []:
            require_reference(by_id, ref, "lesson", "lesson_refs")
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


def slug_for_lesson(lesson: dict) -> str:
    return Path(str(lesson["body_ref"])).stem.replace("_", "-")


def render_list(items: list[object], css_class: str = "detail-list") -> str:
    if not items:
        return '<p class="muted">なし</p>'
    return f'<ul class="{css_class}">' + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>"


def render_practices(md: MarkdownIt, problems: list[dict]) -> str:
    blocks = []
    for number, problem in enumerate(problems, start=1):
        question = md.render(str(problem.get("question", "")))
        blocks.append(
            '<section class="practice-item" aria-labelledby="practice-{}">'
            '<p class="section-kicker">練習 {}</p>'
            '<h3 id="practice-{}">自分で考えてみよう</h3>{}'
            '<div class="answer-space" aria-hidden="true"></div>'
            "</section>".format(number, number, number, question)
        )
    return "".join(blocks)


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
            f'<pre><code>{escape(answer.get("canonical_answer", ""))}</code></pre>'
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


def write_site(root: Path, destination: Path, by_id: dict[str, dict], by_type: dict[str, list[dict]]) -> None:
    md = markdown_renderer()
    assets = destination / "assets"
    lesson_dir = destination / "lessons"
    teacher_dir = destination / "teacher"
    assets.mkdir(parents=True)
    lesson_dir.mkdir(parents=True)
    teacher_dir.mkdir(parents=True)

    stylesheet = root / "site" / "assets" / "styles.css"
    if not stylesheet.is_file():
        raise SiteBuildError(f"missing site asset: {stylesheet.relative_to(root)}")
    shutil.copyfile(stylesheet, assets / "styles.css")

    index_items = []
    teacher_items = []
    output_slugs: set[str] = set()
    lessons = sorted(by_type.get("lesson", []), key=lambda item: str(item.get("body_ref", "")))
    problems = by_type.get("problem", [])
    revisions = by_type.get("revision", [])

    for lesson_number, lesson in enumerate(lessons, start=1):
        lesson_id = str(lesson["id"])
        linked_problems = sorted(
            (problem for problem in problems if lesson_id in (problem.get("lesson_refs", []) or [])),
            key=lambda item: str(item.get("id", "")),
        )
        body_path = repository_path(root, lesson["body_ref"], "body_ref")
        body_source = body_path.read_text(encoding="utf-8")
        lesson_html = render_without_practice_ids(md, body_source)
        practice_html = render_practices(md, linked_problems)
        slug = slug_for_lesson(lesson)
        if slug in output_slugs:
            raise SiteBuildError(f"duplicate lesson output slug: {slug}")
        output_slugs.add(slug)
        page_title = str(lesson.get("title", ""))

        learner_page = render_template(
            root,
            "learner.html",
            {
                "page_title": escape(page_title),
                "subject": escape(lesson.get("subject", "")),
                "unit": escape(lesson.get("unit", "")),
                "lesson_html": lesson_html,
                "practice_html": practice_html,
            },
        )
        (lesson_dir / f"{slug}.html").write_text(learner_page, encoding="utf-8", newline="\n")

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
        teacher_page = render_template(
            root,
            "teacher.html",
            {
                "page_title": escape(page_title),
                "lesson_id": escape(lesson_id),
                "lesson_status": escape(lesson.get("status", "")),
                "learner_href": f"../lessons/{escape(slug)}.html",
                "teacher_guide_html": teacher_html,
                "review_html": review_html,
                "revision_html": revision_html,
            },
        )
        (teacher_dir / f"{slug}.html").write_text(teacher_page, encoding="utf-8", newline="\n")

        index_items.append(
            '<li class="contents-item">'
            f'<a href="lessons/{escape(slug)}.html">'
            f'<span class="lesson-number">Lesson {lesson_number:02d}</span>'
            f'<strong>{escape(page_title)}</strong>'
            f'<span>{escape(lesson.get("unit", ""))}</span>'
            "</a></li>"
        )
        teacher_items.append(
            '<li><a href="teacher/{}.html">教師・レビュー用: {}</a></li>'.format(
                escape(slug), escape(page_title)
            )
        )

    index_page = render_template(
        root,
        "index.html",
        {
            "contents_items": "".join(index_items),
            "teacher_items": "".join(teacher_items),
        },
    )
    (destination / "index.html").write_text(index_page, encoding="utf-8", newline="\n")


def replace_with_retry(source: Path, destination: Path, attempts: int = 5) -> None:
    for attempt in range(attempts):
        try:
            os.replace(source, destination)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            time.sleep(0.05 * (2**attempt))


def replace_site(root: Path, by_id: dict[str, dict], by_type: dict[str, list[dict]]) -> Path:
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
        write_site(root, temp, by_id, by_type)
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
    validate_graph(root, by_id, by_type)
    return replace_site(root, by_id, by_type)


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
