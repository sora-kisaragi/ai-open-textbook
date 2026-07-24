#!/usr/bin/env python3
"""Build and verify classroom or self-study Information I textbook PDFs."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
from xml.etree import ElementTree

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, StreamObject

try:
    from scripts import build_static_site, verify_static_site
except ModuleNotFoundError:  # Direct script execution places scripts/ on sys.path.
    import build_static_site
    import verify_static_site


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILENAME = "information-i-textbook.pdf"
SELF_STUDY_FILENAME = "information-i-self-study.pdf"
EDITIONS = {
    "classroom": (Path("book.html"), DEFAULT_FILENAME),
    "self-study": (Path("self-study/book.html"), SELF_STUDY_FILENAME),
}
A4_WIDTH_POINTS = 595.28
A4_HEIGHT_POINTS = 841.89
PAGE_TOLERANCE_POINTS = 2.0


class PdfBuildError(RuntimeError):
    """Raised for a clear PDF build or verification failure."""


class OrderedListMarkerParser(HTMLParser):
    """Collect decimal list markers that Chromium adds outside HTML text nodes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._list_stack: list[dict[str, int | str]] = []
        self.markers: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        if tag == "ol":
            try:
                start = int(attributes.get("start", "1"))
            except ValueError:
                start = 1
            self._list_stack.append({"tag": "ol", "next": start})
        elif tag == "ul":
            self._list_stack.append({"tag": "ul", "next": 0})
        elif tag == "li" and self._list_stack and self._list_stack[-1]["tag"] == "ol":
            current = self._list_stack[-1]
            try:
                marker = int(attributes.get("value", str(current["next"])))
            except ValueError:
                marker = int(current["next"])
            self.markers.append(str(marker))
            current["next"] = marker + 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"ol", "ul"} and self._list_stack:
            self._list_stack.pop()


def compact_extracted_text(value: str) -> str:
    """Normalize PDF text while ignoring renderer-dependent whitespace."""
    return "".join(unicodedata.normalize("NFKC", value).split())


def review_token_occurrences(value: str, token: str) -> int:
    """Count a sensitive token without losing short-token boundaries."""
    normalized_token = compact_extracted_text(token)
    if not normalized_token:
        return 0
    if re.fullmatch(r"[A-Za-z0-9_]+", normalized_token):
        normalized_value = unicodedata.normalize("NFKC", value)
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_]){re.escape(normalized_token)}(?![A-Za-z0-9_])"
        )
        return len(pattern.findall(normalized_value))
    return compact_extracted_text(value).count(normalized_token)


def unexpected_review_tokens(
    rendered_text: str,
    expected_text: str,
    tokens: set[str],
) -> list[str]:
    """Return review tokens rendered more often than canonical learner text allows."""
    return sorted(
        token
        for token in tokens
        if review_token_occurrences(rendered_text, token)
        > review_token_occurrences(expected_text, token)
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_pdf_object(value: object, active: set[int] | None = None) -> bytes:
    """Serialize a PDF object without indirect object numbers or stream encoding details."""
    if isinstance(value, IndirectObject):
        value = value.get_object()
    active = active or set()
    if isinstance(value, (DictionaryObject, ArrayObject)):
        marker = id(value)
        if marker in active:
            return b"<cycle>"
        active.add(marker)
        try:
            if isinstance(value, StreamObject):
                ignored = {"/Length", "/Filter", "/DecodeParms"}
                entries = [
                    canonical_pdf_object(key, active) + b":" + canonical_pdf_object(item, active)
                    for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
                    if str(key) not in ignored
                ]
                return b"stream{" + b",".join(entries) + b"}" + value.get_data()
            if isinstance(value, DictionaryObject):
                entries = [
                    canonical_pdf_object(key, active) + b":" + canonical_pdf_object(item, active)
                    for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
                ]
                return b"dict{" + b",".join(entries) + b"}"
            return b"array[" + b",".join(canonical_pdf_object(item, active) for item in value) + b"]"
        finally:
            active.remove(marker)
    if isinstance(value, bytes):
        return b"bytes:" + value
    return f"{type(value).__name__}:{value}".encode("utf-8")


def semantic_sha256(path: Path) -> str:
    """Hash stable page semantics without depending on PDF object numbering."""
    reader = PdfReader(path)
    digest = hashlib.sha256()

    def add(value: bytes) -> None:
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)

    add(str(len(reader.pages)).encode("ascii"))
    for page in reader.pages:
        boxes = (page.mediabox, page.cropbox, page.bleedbox, page.trimbox, page.artbox)
        geometry = ";".join(
            ",".join(f"{float(coordinate):.4f}" for coordinate in box)
            for box in boxes
        )
        geometry += f";rotate={int(page.get('/Rotate', 0)) % 360};userunit={float(page.get('/UserUnit', 1)):.4f}"
        text = unicodedata.normalize("NFKC", page.extract_text() or "").replace("\r\n", "\n")
        contents = page.get_contents()
        content_data = contents.get_data() if contents is not None else b""
        resources = canonical_pdf_object(page.get("/Resources"))
        add(geometry.encode("ascii"))
        add(text.encode("utf-8"))
        add(content_data)
        add(resources)
    return digest.hexdigest()


def curriculum_lessons(root: Path) -> list[dict]:
    path = root / "curriculum" / "highschool_information_i.curriculum.json"
    try:
        curriculum = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PdfBuildError(f"cannot load curriculum: {exc}") from exc
    return [lesson for unit in curriculum["units"] for lesson in unit["lessons"]]


def implemented_titles(root: Path) -> list[str]:
    path = root / "data" / "collections" / "lessons.ndjson"
    titles: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise PdfBuildError(f"cannot load lesson records: {exc}") from exc
    for line in lines:
        if line.strip():
            record = json.loads(line)
            titles.append(str(record["title"]))
    return titles


def forbidden_review_tokens(root: Path, edition: str) -> set[str]:
    tokens: set[str] = set()

    def add_token(value: object) -> None:
        if isinstance(value, (str, int, float, bool)) and str(value).strip():
            tokens.add(str(value))

    collections = root / "data" / "collections"
    for filename in ("problems.ndjson", "answers.ndjson", "rubrics.ndjson"):
        for line in (collections / filename).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            add_token(record["id"])
            if record.get("type") == "answer":
                if edition == "classroom":
                    for field in ("canonical_answer", "acceptable_answers", "explanation", "hints"):
                        value = record.get(field)
                        values = value if isinstance(value, list) else [value]
                        for item in values:
                            add_token(item)
                for evidence in record.get("verification_evidence", []) or []:
                    if isinstance(evidence, dict):
                        for item in evidence.values():
                            add_token(item)
            if record.get("type") == "rubric":
                for criterion in record.get("criteria", []):
                    for field in ("id", "description", "points"):
                        add_token(criterion.get(field))
    return tokens


def allowed_learner_source_text(root: Path, edition: str) -> str:
    by_id, by_type = build_static_site.load_records(root)
    values: list[str] = []
    for lesson in by_type.get("lesson", []):
        body = build_static_site.repository_path(root, lesson.get("body_ref"), "body_ref")
        values.append(body.read_text(encoding="utf-8"))
    for problem in by_type.get("problem", []):
        values.append(str(problem.get("question", "")))
        if edition == "self-study":
            values.extend(str(item) for item in problem.get("common_mistakes", []) or [])
            for answer_ref in problem.get("answer_refs", []) or []:
                answer = build_static_site.require_reference(by_id, answer_ref, "answer", "answer_refs")
                values.append(str(answer.get("canonical_answer", "")))
                values.extend(str(item) for item in answer.get("acceptable_answers", []) or [])
                values.extend(str(item) for item in answer.get("hints", []) or [])
                values.append(str(answer.get("explanation", "")))
            values.extend(build_static_site.learner_success_criteria(problem))
    for source in by_type.get("source", []):
        if source.get("status") in {"deprecated", "superseded"}:
            continue
        values.extend(
            str(source.get(field, ""))
            for field in ("title", "issuer", "publication_date", "accessed_at", "url")
        )
    return "\n".join(values)


def required_self_study_feedback(root: Path) -> list[tuple[str, list[str]]]:
    _, by_type = build_static_site.load_records(root)
    answers = [
        (str(answer.get("id", "answer")), compact_extracted_text(answer.get("explanation", "")))
        for answer in by_type.get("answer", [])
        if str(answer.get("explanation", "")).strip()
    ]
    required = []
    for answer_id, explanation in answers:
        candidates = {
            explanation[index:index + 12]
            for index in range(max(1, len(explanation) - 11))
            if len(explanation[index:index + 12]) == 12
        }
        unique_markers = sorted(
            marker
            for marker in candidates
            if not any(marker in other for other_id, other in answers if other_id != answer_id)
        )
        required.append((answer_id, unique_markers or [explanation]))
    return required


def required_self_study_support(root: Path) -> list[tuple[str, list[str]]]:
    _, by_type = build_static_site.load_records(root)
    support: list[tuple[str, str]] = []
    for answer in by_type.get("answer", []):
        answer_id = str(answer.get("id", "answer"))
        support.extend(
            (f"{answer_id} hint {index}", compact_extracted_text(hint))
            for index, hint in enumerate(answer.get("hints", []) or [], start=1)
        )
    curriculum = build_static_site.load_curriculum(root)
    problems = by_type.get("problem", [])
    lessons = sorted(
        by_type.get("lesson", []),
        key=lambda item: (
            curriculum[str(item["id"])].unit_index,
            curriculum[str(item["id"])].lesson_index,
        ),
    )
    for lesson in lessons:
        lesson_id = str(lesson["id"])
        linked_problems = sorted(
            (
                problem
                for problem in problems
                if lesson_id in (problem.get("lesson_refs", []) or [])
            ),
            key=build_static_site.problem_instructional_order,
        )
        for number, problem in enumerate(linked_problems, start=1):
            problem_id = str(problem.get("id", "problem"))
            practice_label = f"{curriculum[lesson_id].order}-{number}"
            support.append(
                (
                    f"{problem_id} learner checks",
                    compact_extracted_text(f"できたか確認（{practice_label}）"),
                )
            )
    required = []
    for label, learner_text in support:
        candidates = {
            learner_text[index:index + 8]
            for index in range(max(1, len(learner_text) - 7))
            if len(learner_text[index:index + 8]) == 8
        }
        unique_markers = sorted(
            marker
            for marker in candidates
            if not any(marker in other for other_label, other in support if other_label != label)
        )
        required.append((label, unique_markers or [learner_text]))
    return required


def referenced_svg_figures(root: Path, edition: str) -> list[Path]:
    site = (root / "build" / "site").resolve()
    book = (site / EDITIONS[edition][0]).resolve()
    if not book.is_file():
        raise PdfBuildError(f"missing generated {edition} book for figure verification")
    try:
        parser = verify_static_site.parse_page(book)
    except verify_static_site.SiteVerificationError as exc:
        raise PdfBuildError(f"cannot inspect generated book figures: {exc}") from exc
    figures_root = (site / "assets" / "figures").resolve()
    figures = {
        (book.parent / attrs["src"]).resolve()
        for tag, attrs in parser.elements
        if tag == "img" and attrs.get("src", "").lower().endswith(".svg")
    }
    for figure in figures:
        if not figure.is_relative_to(figures_root) or not figure.is_file():
            raise PdfBuildError(f"invalid referenced SVG figure: {figure}")
    return sorted(figures)


def expected_pdf_text(root: Path, edition: str) -> str:
    """Return generated text plus browser-created list and SVG text."""
    book = (root / "build" / "site" / EDITIONS[edition][0]).resolve()
    try:
        parser = verify_static_site.parse_page(book)
        source = book.read_text(encoding="utf-8")
    except (OSError, UnicodeError, verify_static_site.SiteVerificationError) as exc:
        raise PdfBuildError(f"cannot inspect generated book text: {exc}") from exc

    list_parser = OrderedListMarkerParser()
    list_parser.feed(source)
    list_parser.close()
    svg_text: list[str] = []
    for figure in referenced_svg_figures(root, edition):
        try:
            svg = ElementTree.parse(figure).getroot()
        except (OSError, ElementTree.ParseError) as exc:
            raise PdfBuildError(f"cannot inspect SVG figure text: {figure}: {exc}") from exc
        svg_text.extend(text for text in svg.itertext() if text.strip())
    return "\n".join((parser.text, *list_parser.markers, *svg_text))


def required_figure_markers(root: Path, edition: str) -> list[tuple[str, list[str]]]:
    figures = referenced_svg_figures(root, edition)
    book = (root / "build" / "site" / EDITIONS[edition][0]).resolve()
    try:
        parser = verify_static_site.parse_page(book)
    except verify_static_site.SiteVerificationError as exc:
        raise PdfBuildError(f"cannot inspect generated book text: {exc}") from exc
    non_svg_text = compact_extracted_text(
        "\n".join(
            [
                parser.text,
                *(value for _, attrs in parser.elements for name, value in attrs.items() if name != "src"),
            ]
        )
    )
    visible_text: dict[Path, list[str]] = {}
    for figure in figures:
        try:
            svg = ElementTree.parse(figure).getroot()
        except (OSError, ElementTree.ParseError) as exc:
            raise PdfBuildError(f"cannot inspect SVG figure {figure.name}: {exc}") from exc
        visible_text[figure] = [
            marker
            for element in svg.iter()
            if element.tag.rsplit("}", 1)[-1] == "text"
            if (marker := compact_extracted_text("".join(element.itertext())))
        ]

    required = []
    for figure, markers in visible_text.items():
        other_text = "\n".join(
            marker
            for other, other_markers in visible_text.items()
            if other != figure
            for marker in other_markers
        )
        unique_markers = sorted(
            (
                marker
                for marker in markers
                if marker not in other_text and marker not in non_svg_text
            ),
            key=lambda marker: (-len(marker), marker),
        )
        if not unique_markers:
            raise PdfBuildError(
                f"SVG figure has no visible text marker unique from the surrounding book: {figure.name}"
            )
        required.append((figure.name, unique_markers))
    return required


def normalize_pdf(source: Path, destination: Path, edition: str) -> None:
    reader = PdfReader(source)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.metadata = None
    writer.add_metadata(
        {
            "/Title": f"Information I Open Textbook {edition.title()} Review Candidate",
            "/Author": "AI Open Textbook contributors",
            "/Subject": "Learner review candidate; not approved or published",
            "/Creator": "ai-open-textbook scripts/build_pdf.py",
            "/Producer": "pypdf",
        }
    )
    with destination.open("wb") as stream:
        writer.write(stream)


def current_input_sha256(root: Path, edition: str) -> dict[str, str]:
    site = root / "build" / "site"
    book = site / EDITIONS[edition][0]
    stylesheet = site / "assets" / "styles.css"
    return {
        "book.html": sha256(book),
        "assets/styles.css": sha256(stylesheet),
        **{
            figure.relative_to(site).as_posix(): sha256(figure)
            for figure in sorted((site / "assets" / "figures").rglob("*.svg"))
        },
    }


def canonical_source_sha256(root: Path, edition: str) -> str:
    """Hash canonical educational inputs that must precede site and PDF builds."""
    patterns = (
        "curriculum/**/*.json",
        "data/collections/*.ndjson",
        "lessons/**/*.md",
        "teacher_guides/**/*.md",
        "site/assets/styles.css",
        "site/assets/figures/**/*.svg",
    )
    files = sorted({path for pattern in patterns for path in root.glob(pattern) if path.is_file()})
    digest = hashlib.sha256()
    digest.update(edition.encode("utf-8"))
    digest.update(b"\0")
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def verify_pdf_manifest(root: Path, pdf_path: Path, edition: str, page_count: int) -> None:
    manifest_path = pdf_path.with_suffix(".manifest.json")
    if not manifest_path.is_file():
        raise PdfBuildError(f"PDF manifest is missing: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PdfBuildError(f"cannot read PDF manifest: {exc}") from exc
    expected = {
        "edition": edition,
        "output": pdf_path.name,
        "output_sha256": sha256(pdf_path),
        "semantic_sha256": semantic_sha256(pdf_path),
        "page_count": page_count,
        "input_sha256": current_input_sha256(root, edition),
        "canonical_source_sha256": canonical_source_sha256(root, edition),
        "review_status": "needs_human_review",
    }
    for field, value in expected.items():
        if manifest.get(field) != value:
            raise PdfBuildError(f"PDF manifest mismatch for {field}")


def verify_pdf(
    root: Path,
    pdf_path: Path,
    edition: str = "classroom",
    *,
    require_manifest: bool = True,
) -> int:
    if edition not in EDITIONS:
        raise PdfBuildError(f"unknown edition: {edition}")
    if require_manifest:
        try:
            verify_static_site.verify(root)
        except (OSError, build_static_site.SiteBuildError, verify_static_site.SiteVerificationError) as exc:
            raise PdfBuildError(f"static site verification failed before PDF verification: {exc}") from exc
    if not pdf_path.is_file() or pdf_path.stat().st_size < 100:
        raise PdfBuildError(f"PDF is missing or unexpectedly small: {pdf_path}")
    try:
        reader = PdfReader(pdf_path)
    except Exception as exc:
        raise PdfBuildError(f"cannot read generated PDF: {exc}") from exc
    if not reader.pages:
        raise PdfBuildError("generated PDF has no pages")
    for index, page in enumerate(reader.pages, start=1):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - A4_WIDTH_POINTS) > PAGE_TOLERANCE_POINTS or abs(height - A4_HEIGHT_POINTS) > PAGE_TOLERANCE_POINTS:
            raise PdfBuildError(f"page {index} is not A4: {width:.2f} x {height:.2f} points")
    rendered_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = compact_extracted_text(rendered_text)
    book = root / "build" / "site" / EDITIONS[edition][0]
    expected_text = expected_pdf_text(root, edition)
    for title in implemented_titles(root):
        if compact_extracted_text(title) not in text:
            raise PdfBuildError(f"generated PDF is missing implemented lesson title: {title}")
    unexpected_tokens = unexpected_review_tokens(
        rendered_text,
        expected_text,
        forbidden_review_tokens(root, edition),
    )
    if unexpected_tokens:
        raise PdfBuildError(f"learner PDF contains review-only token: {unexpected_tokens[0]}")
    for figure, markers in required_figure_markers(root, edition):
        if not any(marker in text for marker in markers):
            raise PdfBuildError(f"generated PDF is missing rendered SVG figure: {figure}")
    if edition == "self-study":
        for answer_id, markers in required_self_study_feedback(root):
            if not any(marker in text for marker in markers):
                raise PdfBuildError(
                    f"self-study PDF is missing answer explanation for {answer_id}"
                )
        for label, markers in required_self_study_support(root):
            if not any(marker in text for marker in markers):
                raise PdfBuildError(f"self-study PDF is missing {label}")
    page_count = len(reader.pages)
    if require_manifest:
        verify_pdf_manifest(root, pdf_path, edition, page_count)
    return page_count


def build(root: Path, output: Path, edition: str = "classroom") -> dict:
    if edition not in EDITIONS:
        raise PdfBuildError(f"unknown edition: {edition}")
    root = root.resolve()
    output = output.resolve()
    site = build_static_site.build(root)
    try:
        verify_static_site.verify(root)
    except (OSError, build_static_site.SiteBuildError, verify_static_site.SiteVerificationError) as exc:
        raise PdfBuildError(f"static site verification failed before PDF generation: {exc}") from exc
    book = site / EDITIONS[edition][0]
    stylesheet = site / "assets" / "styles.css"
    if not book.is_file():
        raise PdfBuildError(f"static site did not generate {edition} book.html")
    output.parent.mkdir(parents=True, exist_ok=True)
    browser_pdf_fd, browser_pdf_name = tempfile.mkstemp(prefix="book-browser-", suffix=".pdf", dir=output.parent)
    os.close(browser_pdf_fd)
    normalized_fd, normalized_name = tempfile.mkstemp(prefix="book-normalized-", suffix=".pdf", dir=output.parent)
    os.close(normalized_fd)
    browser_pdf = Path(browser_pdf_name)
    normalized_pdf = Path(normalized_name)
    browser_version = "unknown"
    blocked_requests: list[str] = []
    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except PlaywrightError as exc:
                raise PdfBuildError(
                    "Chromium is unavailable. Run: python -m playwright install chromium"
                ) from exc
            browser_version = browser.version
            page = browser.new_page()

            def block_remote_request(route) -> None:
                if route.request.url.startswith(("http://", "https://", "//")):
                    blocked_requests.append(route.request.url)
                    route.abort()
                    return
                route.continue_()

            page.route("**/*", block_remote_request)
            page.goto(book.as_uri(), wait_until="load")
            page.emulate_media(media="print")
            if edition == "self-study":
                page.locator("details.hint-reveal, details.answer-reveal").evaluate_all(
                    "elements => elements.forEach(element => element.open = true)"
                )
            page.evaluate("document.fonts.ready")
            page.pdf(
                path=str(browser_pdf),
                format="A4",
                print_background=True,
                display_header_footer=False,
                prefer_css_page_size=True,
                tagged=True,
                outline=True,
            )
            browser.close()
        if blocked_requests:
            raise PdfBuildError(f"print document attempted remote requests: {blocked_requests}")
        normalize_pdf(browser_pdf, normalized_pdf, edition)
        os.replace(normalized_pdf, output)
        page_count = verify_pdf(root, output, edition, require_manifest=False)
        answer_feedback_count = book.read_text(encoding="utf-8").count(
            '<details class="answer-reveal">'
        )
        figure_count = len(required_figure_markers(root, edition))
        manifest = {
            "schema_version": "1.0",
            "edition": edition,
            "input_sha256": current_input_sha256(root, edition),
            "canonical_source_sha256": canonical_source_sha256(root, edition),
            "output": output.name,
            "output_sha256": sha256(output),
            "semantic_sha256": semantic_sha256(output),
            "page_count": page_count,
            "implemented_lesson_count": len(implemented_titles(root)),
            "planned_lesson_count": len(curriculum_lessons(root)),
            "answer_feedback_count": answer_feedback_count,
            "figure_count": figure_count,
            "playwright_version": version("playwright"),
            "chromium_version": browser_version,
            "pypdf_version": version("pypdf"),
            "reproducibility": "Pinned repeatable workflow; semantic identity is checked within the same toolchain while output_sha256 identifies the exact artifact.",
            "review_status": "needs_human_review",
        }
        manifest_path = output.with_suffix(".manifest.json")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        return manifest
    finally:
        for temporary in (browser_pdf, normalized_pdf):
            if temporary.exists():
                temporary.unlink()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Repository root.")
    parser.add_argument(
        "--edition",
        choices=sorted(EDITIONS),
        default="classroom",
        help="Learner edition to build or verify.",
    )
    parser.add_argument("--output", type=Path, help="PDF path. Defaults to the edition-specific build path.")
    parser.add_argument("--verify-only", action="store_true", help="Verify an existing PDF without rebuilding it.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output = (args.output or root / "build" / EDITIONS[args.edition][1]).resolve()
    try:
        if args.verify_only:
            pages = verify_pdf(root, output, args.edition)
            print(f"PDF verification passed: {output} ({pages} A4 pages).")
        else:
            manifest = build(root, output, args.edition)
            print(
                f"Built and verified {output} with {manifest['page_count']} A4 pages; "
                f"manifest={output.with_suffix('.manifest.json')}."
            )
    except (OSError, PdfBuildError, PlaywrightError, json.JSONDecodeError) as exc:
        print(f"PDF build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
