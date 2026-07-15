#!/usr/bin/env python3
"""Verify the generated static textbook site for production review."""
from __future__ import annotations

import argparse
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

if __package__:
    from . import build_static_site
else:
    import build_static_site


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
URL_ATTRIBUTES = frozenset({"href", "src", "poster", "action", "formaction", "data"})
FORBIDDEN_RUNTIME_TAGS = frozenset({"script", "iframe", "object", "embed"})
INTERNAL_LEARNER_ID = re.compile(
    r"\b(?:ans|prob|rubric)\.[a-z0-9]+(?:\.[a-z0-9]+)*\.v[1-9][0-9]*\b"
)
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+(?:url\(\s*)?['\"]?([^'\"\s;)]+)", re.IGNORECASE)
LOW_INFORMATION_SENSITIVE_VALUE = re.compile(
    r"^(?:(?:[+-]?\d+(?:\.\d+)?)(?:\s+[+-]?\d+(?:\.\d+)?)*|True|False|None)$"
)
REVIEW_ONLY_CLASSES = frozenset(
    {
        "review-record",
        "review-record-header",
        "review-subsection",
        "record-id",
        "teacher-copy",
        "rubric-list",
    }
)


class SiteVerificationError(RuntimeError):
    """Raised when generated output is incomplete, unsafe, or inconsistent."""


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[tuple[str, dict[str, str]]] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str, str]] = []
        self.text_parts: list[str] = []
        self.inline_css: list[str] = []
        self._style_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        self.elements.append((tag, attributes))
        if tag == "style":
            self._style_depth += 1
        if attributes.get("style"):
            self.inline_css.append(attributes["style"])
        element_id = attributes.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        for name, value in attributes.items():
            if name in URL_ATTRIBUTES and value:
                self.references.append((tag, name, value))
            elif name == "srcset" and value:
                for candidate in value.split(","):
                    url = candidate.strip().split(maxsplit=1)[0]
                    if url:
                        self.references.append((tag, name, url))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag == "style":
            self._style_depth -= 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "style" and self._style_depth:
            self._style_depth -= 1

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)
        if self._style_depth:
            self.inline_css.append(data)

    @property
    def text(self) -> str:
        return "\n".join(self.text_parts)

    def has(self, tag: str, *, element_id: str | None = None, css_class: str | None = None) -> bool:
        return self.count(tag, element_id=element_id, css_class=css_class) > 0

    def count(self, tag: str, *, element_id: str | None = None, css_class: str | None = None) -> int:
        count = 0
        for candidate_tag, attrs in self.elements:
            if candidate_tag != tag:
                continue
            if element_id is not None and attrs.get("id") != element_id:
                continue
            if css_class is not None and css_class not in attrs.get("class", "").split():
                continue
            count += 1
        return count

    def links(self, *, rel: str | None = None) -> list[str]:
        links = []
        for tag, attrs in self.elements:
            if tag != "a" or "href" not in attrs:
                continue
            if rel is not None and rel not in attrs.get("rel", "").split():
                continue
            links.append(attrs["href"])
        return links


def normalize_text(value: object) -> str:
    return " ".join(html.unescape(str(value)).split())


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        raise SiteVerificationError(f"cannot read HTML page {path}: {exc}") from exc
    if parser.duplicate_ids:
        duplicates = ", ".join(sorted(parser.duplicate_ids))
        raise SiteVerificationError(f"duplicate fragment id(s) in {path.name}: {duplicates}")
    return parser


def require_structure(
    parser: PageParser,
    relative: str,
    requirements: list[tuple[str, str | None, str | None]],
) -> None:
    for tag, element_id, css_class in requirements:
        if not parser.has(tag, element_id=element_id, css_class=css_class):
            description = tag
            if element_id:
                description += f"#{element_id}"
            if css_class:
                description += f".{css_class}"
            raise SiteVerificationError(f"{relative}: missing required structure {description}")


def resolve_local_reference(site: Path, page: Path, value: str) -> tuple[Path, str]:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        raise SiteVerificationError(f"external runtime reference in {page.relative_to(site)}: {value}")
    if "\\" in parsed.path:
        raise SiteVerificationError(f"non-portable local reference in {page.relative_to(site)}: {value}")
    target = page if not parsed.path else (page.parent / unquote(parsed.path)).resolve()
    site_resolved = site.resolve()
    if not target.is_relative_to(site_resolved):
        raise SiteVerificationError(f"local reference escapes site root in {page.relative_to(site)}: {value}")
    if not target.is_file():
        raise SiteVerificationError(f"broken local reference in {page.relative_to(site)}: {value}")
    return target, unquote(parsed.fragment)


def verify_references(site: Path, pages: dict[Path, PageParser]) -> None:
    for page, parser in pages.items():
        for tag, attribute, value in parser.references:
            parsed = urlsplit(value)
            if parsed.scheme in {"http", "https"} and tag == "a" and attribute == "href":
                continue
            if parsed.scheme or parsed.netloc or value.startswith("//"):
                raise SiteVerificationError(
                    f"external runtime reference in {page.relative_to(site)}: {value}"
                )
            target, fragment = resolve_local_reference(site, page, value)
            if fragment:
                if target.suffix.lower() != ".html":
                    raise SiteVerificationError(
                        f"fragment targets a non-HTML asset in {page.relative_to(site)}: {value}"
                    )
                target_parser = pages.get(target)
                if target_parser is None:
                    target_parser = parse_page(target)
                    pages[target] = target_parser
                if fragment not in target_parser.ids:
                    raise SiteVerificationError(
                        f"broken fragment in {page.relative_to(site)}: {value}"
                    )


def verify_css_text(site: Path, source: Path, css: str) -> None:
    if "\\" in css:
        raise SiteVerificationError(
            f"CSS escapes are not allowed in offline assets: {source.relative_to(site)}"
        )
    references = [match.group(2) for match in CSS_URL.finditer(css)]
    references.extend(match.group(1) for match in CSS_IMPORT.finditer(css))
    for reference in references:
        if reference.startswith("#"):
            continue
        resolve_local_reference(site, source, reference)


def verify_css(site: Path, pages: dict[Path, PageParser]) -> None:
    stylesheet = site / "assets" / "styles.css"
    if not stylesheet.is_file():
        raise SiteVerificationError("missing required asset: assets/styles.css")
    verify_css_text(site, stylesheet, stylesheet.read_text(encoding="utf-8"))
    for page, parser in pages.items():
        for css in parser.inline_css:
            verify_css_text(site, page, css)


def flatten_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in flatten_strings(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in flatten_strings(child)]
    return []


def sensitive_values(by_type: dict[str, list[dict]]) -> list[tuple[str, str]]:
    """Return values suitable for substring checks; structural checks cover low-information values."""
    values: list[tuple[str, str]] = []
    for answer in by_type.get("answer", []):
        answer_id = str(answer.get("id", "answer"))
        for field in ("canonical_answer", "acceptable_answers", "explanation", "verification_evidence"):
            for value in flatten_strings(answer.get(field)):
                normalized = normalize_text(value)
                if normalized and not LOW_INFORMATION_SENSITIVE_VALUE.fullmatch(normalized):
                    values.append((f"{answer_id}.{field}", value))
    for rubric in by_type.get("rubric", []):
        rubric_id = str(rubric.get("id", "rubric"))
        for criterion in rubric.get("criteria", []) or []:
            if isinstance(criterion, dict):
                description = criterion.get("description")
                if isinstance(description, str) and normalize_text(description):
                    values.append((f"{rubric_id}.criteria", description))
    return values


def verify_learner_separation(
    learner_pages: dict[Path, PageParser],
    allowed_sources: dict[Path, str],
    forbidden_values: list[tuple[str, str]],
) -> None:
    for page, parser in learner_pages.items():
        page_text = normalize_text(parser.text)
        allowed_text = normalize_text(allowed_sources[page])
        review_classes = sorted(
            REVIEW_ONLY_CLASSES.intersection(
                css_class
                for _, attrs in parser.elements
                for css_class in attrs.get("class", "").split()
            )
        )
        if review_classes:
            raise SiteVerificationError(
                f"review-only structure leaked into {page.name}: {', '.join(review_classes)}"
            )
        internal_id = INTERNAL_LEARNER_ID.search(page_text)
        if internal_id:
            raise SiteVerificationError(
                f"internal answer/rubric/problem id leaked into {page.name}: {internal_id.group(0)}"
            )
        for source, raw_value in forbidden_values:
            value = normalize_text(raw_value)
            if value in allowed_text:
                continue
            if value and value in page_text:
                raise SiteVerificationError(f"teacher-only value from {source} leaked into {page.name}")


def verify(root: Path) -> tuple[int, int]:
    root = root.resolve()
    site = root / "build" / "site"
    if not site.is_dir():
        raise SiteVerificationError("missing generated site: build/site")
    content_license = site / "LICENSE-CONTENT-CC-BY-4.0.txt"
    if not content_license.is_file():
        raise SiteVerificationError("missing generated content license")

    by_id, by_type = build_static_site.load_records(root)
    curriculum = build_static_site.load_curriculum(root)
    build_static_site.validate_graph(root, by_id, by_type, curriculum)
    lessons = sorted(
        by_type.get("lesson", []),
        key=lambda item: (
            curriculum[str(item["id"])].unit_index,
            curriculum[str(item["id"])].lesson_index,
        ),
    )
    slugs = [build_static_site.slug_for_lesson(lesson) for lesson in lessons]
    expected_learner = [site / "lessons" / f"{slug}.html" for slug in slugs]
    expected_teacher = [site / "teacher" / f"{slug}.html" for slug in slugs]
    expected_html = {site / "index.html", site / "book.html", *expected_learner, *expected_teacher}
    actual_html = {path.resolve() for path in site.rglob("*.html") if path.is_file()}
    expected_html = {path.resolve() for path in expected_html}
    if actual_html != expected_html:
        missing = sorted(path.relative_to(site).as_posix() for path in expected_html - actual_html)
        extra = sorted(path.relative_to(site).as_posix() for path in actual_html - expected_html)
        raise SiteVerificationError(f"unexpected HTML page set; missing={missing}, extra={extra}")

    pages = {path: parse_page(path) for path in sorted(expected_html)}
    for path, parser in pages.items():
        forbidden_tags = sorted({tag for tag, _ in parser.elements if tag in FORBIDDEN_RUNTIME_TAGS})
        if forbidden_tags:
            raise SiteVerificationError(
                f"runtime element(s) in {path.relative_to(site)}: {', '.join(forbidden_tags)}"
            )

    index_path = (site / "index.html").resolve()
    book_path = (site / "book.html").resolve()
    index_parser = pages[index_path]
    require_structure(
        index_parser,
        "index.html",
        [("body", None, "contents-page"), ("main", "main", None), ("div", None, "curriculum-units")],
    )
    included_units = {curriculum[str(lesson["id"])].unit_id for lesson in lessons}
    if index_parser.count("section", css_class="curriculum-unit") != len(included_units):
        raise SiteVerificationError("index.html: curriculum unit count does not match source data")

    book_parser = pages[book_path]
    require_structure(
        book_parser,
        "book.html",
        [("section", "book-imprint", "book-imprint"), ("ol", None, "source-bibliography")],
    )
    active_source_count = sum(
        source.get("status") not in {"deprecated", "superseded"}
        for source in by_type.get("source", [])
    )
    if book_parser.count("li", css_class="source-bibliography-item") != active_source_count:
        raise SiteVerificationError("book.html: source bibliography is incomplete")

    learner_parsers: dict[Path, PageParser] = {}
    allowed_sources: dict[Path, str] = {}
    all_allowed_sources: list[str] = []
    problems = by_type.get("problem", [])
    for index, (lesson, slug) in enumerate(zip(lessons, slugs, strict=True)):
        learner_path = (site / "lessons" / f"{slug}.html").resolve()
        teacher_path = (site / "teacher" / f"{slug}.html").resolve()
        learner_parser = pages[learner_path]
        teacher_parser = pages[teacher_path]
        require_structure(
            learner_parser,
            learner_path.relative_to(site).as_posix(),
            [
                ("body", None, "lesson-page"),
                ("main", "lesson-content", None),
                ("article", None, "lesson-article"),
                ("section", None, "practice-section"),
                ("nav", None, "lesson-navigation"),
            ],
        )
        if index > 0 and learner_parser.links(rel="prev") != [f"{slugs[index - 1]}.html"]:
            raise SiteVerificationError(f"{learner_path.name}: missing or incorrect previous link")
        if index == 0 and learner_parser.links(rel="prev"):
            raise SiteVerificationError(f"{learner_path.name}: unexpected previous link")
        if index + 1 < len(slugs) and learner_parser.links(rel="next") != [f"{slugs[index + 1]}.html"]:
            raise SiteVerificationError(f"{learner_path.name}: missing or incorrect next link")
        if index + 1 == len(slugs) and learner_parser.links(rel="next"):
            raise SiteVerificationError(f"{learner_path.name}: unexpected next link")
        require_structure(
            teacher_parser,
            teacher_path.relative_to(site).as_posix(),
            [
                ("body", None, "teacher-page"),
                ("main", "teacher-content", None),
                ("aside", None, "teacher-notice"),
            ],
        )
        if "教師・レビュー用" not in teacher_parser.text:
            raise SiteVerificationError(f"{teacher_path.name}: missing teacher/reviewer label")
        if f"../lessons/{slug}.html" not in teacher_parser.links():
            raise SiteVerificationError(f"{teacher_path.name}: missing learner-page link")

        linked_questions = [
            str(problem.get("question", ""))
            for problem in problems
            if str(lesson["id"]) in (problem.get("lesson_refs", []) or [])
        ]
        body_path = build_static_site.repository_path(root, lesson["body_ref"], "body_ref")
        allowed = body_path.read_text(encoding="utf-8") + "\n" + "\n".join(linked_questions)
        learner_parsers[learner_path] = learner_parser
        allowed_sources[learner_path] = allowed
        all_allowed_sources.append(allowed)

    book_parser = pages[book_path]
    require_structure(
        book_parser,
        "book.html",
        [
            ("body", None, "book-page"),
            ("main", "book-content", None),
            ("nav", None, "book-toc"),
            ("div", None, "book-units"),
        ],
    )
    if book_parser.count("article", css_class="book-lesson") != len(lessons):
        raise SiteVerificationError("book.html: learner lesson count does not match source data")
    for slug in slugs:
        if not book_parser.has("article", element_id=f"lesson-{slug}", css_class="book-lesson"):
            raise SiteVerificationError(f"book.html: missing lesson fragment lesson-{slug}")
    if any(link.startswith("teacher/") for link in book_parser.links()):
        raise SiteVerificationError("book.html: teacher/reviewer link found in learner-only book")
    learner_parsers[book_path] = book_parser
    bibliography_metadata = "\n".join(
        str(source.get(field, ""))
        for source in by_type.get("source", [])
        if source.get("status") not in {"deprecated", "superseded"}
        for field in ("title", "issuer", "publication_date", "accessed_at", "url")
    )
    allowed_sources[book_path] = "\n".join([*all_allowed_sources, bibliography_metadata])

    verify_references(site.resolve(), pages)
    verify_css(site.resolve(), pages)
    verify_learner_separation(learner_parsers, allowed_sources, sensitive_values(by_type))
    return len(expected_learner), len(expected_teacher)


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
        learner_count, teacher_count = verify(args.root)
    except (OSError, build_static_site.SiteBuildError, SiteVerificationError) as exc:
        print(f"Static site verification failed: {exc}", file=sys.stderr)
        return 1
    print(
        f"Verified static textbook site at {(args.root.resolve() / 'build' / 'site')}: "
        f"{learner_count} learner page(s), {teacher_count} teacher page(s), 1 book."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
