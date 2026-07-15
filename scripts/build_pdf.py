#!/usr/bin/env python3
"""Build and verify the learner-only Information I textbook PDF."""
from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import sys
import tempfile
import unicodedata

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, StreamObject

try:
    from scripts import build_static_site
except ModuleNotFoundError:  # Direct script execution places scripts/ on sys.path.
    import build_static_site


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILENAME = "information-i-textbook.pdf"
A4_WIDTH_POINTS = 595.28
A4_HEIGHT_POINTS = 841.89
PAGE_TOLERANCE_POINTS = 2.0


class PdfBuildError(RuntimeError):
    """Raised for a clear PDF build or verification failure."""


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


def forbidden_review_tokens(root: Path) -> set[str]:
    tokens: set[str] = set()
    collections = root / "data" / "collections"
    for filename in ("answers.ndjson", "rubrics.ndjson"):
        for line in (collections / filename).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            tokens.add(str(record["id"]))
            if record.get("type") == "answer":
                explanation = record.get("explanation")
                if isinstance(explanation, str) and len(explanation) >= 12:
                    tokens.add(explanation)
            if record.get("type") == "rubric":
                for criterion in record.get("criteria", []):
                    description = criterion.get("description")
                    if isinstance(description, str) and len(description) >= 12:
                        tokens.add(description)
    return tokens


def normalize_pdf(source: Path, destination: Path) -> None:
    reader = PdfReader(source)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.metadata = None
    writer.add_metadata(
        {
            "/Title": "情報I Open Textbook Review Candidate",
            "/Author": "AI Open Textbook contributors",
            "/Subject": "Learner review candidate; not approved or published",
            "/Creator": "ai-open-textbook scripts/build_pdf.py",
            "/Producer": "pypdf",
        }
    )
    with destination.open("wb") as stream:
        writer.write(stream)


def verify_pdf(root: Path, pdf_path: Path) -> int:
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
    text = unicodedata.normalize(
        "NFKC", "\n".join(page.extract_text() or "" for page in reader.pages)
    )
    for title in implemented_titles(root):
        if unicodedata.normalize("NFKC", title) not in text:
            raise PdfBuildError(f"generated PDF is missing implemented lesson title: {title}")
    for token in forbidden_review_tokens(root):
        if unicodedata.normalize("NFKC", token) in text:
            raise PdfBuildError(f"learner PDF contains review-only token: {token}")
    return len(reader.pages)


def build(root: Path, output: Path) -> dict:
    root = root.resolve()
    output = output.resolve()
    site = build_static_site.build(root)
    book = site / "book.html"
    stylesheet = site / "assets" / "styles.css"
    if not book.is_file():
        raise PdfBuildError("static site did not generate learner book.html")
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
        normalize_pdf(browser_pdf, normalized_pdf)
        os.replace(normalized_pdf, output)
        page_count = verify_pdf(root, output)
        manifest = {
            "schema_version": "1.0",
            "input_sha256": {
                "book.html": sha256(book),
                "assets/styles.css": sha256(stylesheet),
            },
            "output": output.name,
            "output_sha256": sha256(output),
            "semantic_sha256": semantic_sha256(output),
            "page_count": page_count,
            "implemented_lesson_count": len(implemented_titles(root)),
            "planned_lesson_count": len(curriculum_lessons(root)),
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
    parser.add_argument("--output", type=Path, help="PDF path. Defaults to ROOT/build/information-i-textbook.pdf.")
    parser.add_argument("--verify-only", action="store_true", help="Verify an existing PDF without rebuilding it.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    output = (args.output or root / "build" / DEFAULT_FILENAME).resolve()
    try:
        if args.verify_only:
            pages = verify_pdf(root, output)
            print(f"PDF verification passed: {output} ({pages} A4 pages).")
        else:
            manifest = build(root, output)
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
