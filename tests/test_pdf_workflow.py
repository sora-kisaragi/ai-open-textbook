#!/usr/bin/env python3
"""Tests for the classroom and self-study PDF workflow."""
from __future__ import annotations

from pathlib import Path
import json

from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject, NumberObject
from pypdf import PdfReader, PdfWriter
import pytest

from scripts import build_pdf


ROOT = Path(__file__).resolve().parents[1]


def test_compact_extracted_text_ignores_renderer_whitespace() -> None:
    assert build_pdf.compact_extracted_text("インターネット、Web、\n情報サービス") == (
        "インターネット、Web、情報サービス"
    )


def test_review_token_comparison_detects_only_excess_rendered_occurrences() -> None:
    expected = "B\n本文の値は80です。\n1"
    rendered = "B\n本文の値は80です。\n1\nB\n180は別の値です。"

    assert build_pdf.review_token_occurrences(expected, "B") == 1
    assert build_pdf.review_token_occurrences(rendered, "80") == 1
    assert build_pdf.unexpected_review_tokens(rendered, expected, {"B", "80", "1"}) == ["B"]
    assert build_pdf.review_token_occurrences("Inline B leak", "B") == 1
    assert build_pdf.review_token_occurrences("score is 1 point", "1") == 1


def test_ordered_list_markers_include_start_value_and_nested_lists() -> None:
    parser = build_pdf.OrderedListMarkerParser()
    parser.feed(
        '<ol start="3"><li>three</li><li value="8">eight<ul><li>bullet</li></ul></li>'
        '<li>nine</li></ol>'
    )
    parser.close()

    assert parser.markers == ["3", "8", "9"]


def test_pdf_build_is_repeatable_and_verified(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"

    first_manifest = build_pdf.build(ROOT, first)
    second_manifest = build_pdf.build(ROOT, second)

    assert first_manifest["page_count"] >= 1
    assert first_manifest["edition"] == "classroom"
    assert first_manifest["answer_feedback_count"] == 0
    assert first_manifest["implemented_lesson_count"] == 32
    assert first_manifest["planned_lesson_count"] == 32
    assert first_manifest["figure_count"] == 4
    assert first_manifest["canonical_source_sha256"] == build_pdf.canonical_source_sha256(
        ROOT, "classroom"
    )
    assert any(key.startswith("assets/figures/") for key in first_manifest["input_sha256"])
    assert first_manifest["input_sha256"] == second_manifest["input_sha256"]
    assert first_manifest["semantic_sha256"] == second_manifest["semantic_sha256"]
    assert build_pdf.verify_pdf(ROOT, first) == first_manifest["page_count"]
    assert len(build_pdf.required_figure_markers(ROOT, "classroom")) == 4
    classroom_book = ROOT / "build/site/book.html"
    parser = build_pdf.verify_static_site.parse_page(classroom_book)
    non_svg_text = build_pdf.compact_extracted_text(
        "\n".join(
            [
                parser.text,
                *(value for _, attrs in parser.elements for name, value in attrs.items() if name != "src"),
            ]
        )
    )
    assert all(
        marker not in non_svg_text
        for _, markers in build_pdf.required_figure_markers(ROOT, "classroom")
        for marker in markers
    )

    _, by_type = build_pdf.build_static_site.load_records(ROOT)
    hints = {
        hint
        for answer in by_type.get("answer", [])
        for hint in answer.get("hints", []) or []
    }
    assert hints
    assert hints <= build_pdf.forbidden_review_tokens(ROOT, "classroom")
    pdf_text = build_pdf.compact_extracted_text(
        "\n".join(page.extract_text() or "" for page in PdfReader(first).pages)
    )
    assert all(build_pdf.compact_extracted_text(hint) not in pdf_text for hint in hints)

    monkeypatch.setattr(
        build_pdf,
        "required_figure_markers",
        lambda _root, _edition: [("missing-figure.svg", ["MISSING_FIGURE_MARKER"])],
    )
    with pytest.raises(build_pdf.PdfBuildError, match="missing rendered SVG figure"):
        build_pdf.verify_pdf(ROOT, first)


def test_classroom_forbidden_tokens_include_short_answer_and_rubric_values() -> None:
    _, by_type = build_pdf.build_static_site.load_records(ROOT)
    tokens = build_pdf.forbidden_review_tokens(ROOT, "classroom")

    for answer in by_type.get("answer", []):
        assert str(answer["canonical_answer"]) in tokens
        assert all(str(value) in tokens for value in answer.get("acceptable_answers", []) or [])
        assert all(str(value) in tokens for value in answer.get("hints", []) or [])
    for rubric in by_type.get("rubric", []):
        for criterion in rubric.get("criteria", []):
            assert str(criterion["id"]) in tokens
            assert str(criterion["description"]) in tokens
            assert str(criterion["points"]) in tokens


def test_pdf_manifest_rejects_artifact_tampering(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "classroom.pdf"
    build_pdf.build(ROOT, output)
    manifest_path = output.with_suffix(".manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    monkeypatch.setattr(build_pdf, "canonical_source_sha256", lambda _root, _edition: "0" * 64)
    with pytest.raises(build_pdf.PdfBuildError, match="manifest mismatch for canonical_source_sha256"):
        build_pdf.verify_pdf(ROOT, output)
    monkeypatch.undo()

    writer = PdfWriter()
    writer.clone_document_from_reader(PdfReader(output))
    writer.add_metadata({"/Tampered": "true"})
    with output.open("wb") as stream:
        writer.write(stream)

    assert build_pdf.semantic_sha256(output) == manifest["semantic_sha256"]
    with pytest.raises(build_pdf.PdfBuildError, match="manifest mismatch for output_sha256"):
        build_pdf.verify_pdf(ROOT, output)


def test_figure_marker_must_be_unique_from_surrounding_html(tmp_path: Path) -> None:
    figures = tmp_path / "build/site/assets/figures"
    figures.mkdir(parents=True)
    (figures / "duplicate.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><text>Shared marker</text></svg>',
        encoding="utf-8",
    )
    (tmp_path / "build/site/book.html").write_text(
        '<!doctype html><html><body><main><p>Shared marker</p>'
        '<img src="assets/figures/duplicate.svg" alt="Shared marker"></main></body></html>',
        encoding="utf-8",
    )

    with pytest.raises(build_pdf.PdfBuildError, match="unique from the surrounding book"):
        build_pdf.required_figure_markers(tmp_path, "classroom")


def test_pdf_build_runs_static_verification_before_rendering(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        build_pdf.build_static_site,
        "build",
        lambda root: root / "build" / "site",
    )

    def reject_static_site(_root: Path) -> None:
        raise build_pdf.verify_static_site.SiteVerificationError("verification sentinel")

    monkeypatch.setattr(build_pdf.verify_static_site, "verify", reject_static_site)

    with pytest.raises(build_pdf.PdfBuildError, match="verification sentinel"):
        build_pdf.build(ROOT, tmp_path / "must-not-render.pdf")


def test_self_study_pdf_includes_all_answer_feedback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "self-study.pdf"

    manifest = build_pdf.build(ROOT, output, edition="self-study")

    assert manifest["edition"] == "self-study"
    assert manifest["answer_feedback_count"] == 140
    assert manifest["page_count"] >= 1
    assert len(build_pdf.required_self_study_feedback(ROOT)) == 140
    assert len(build_pdf.required_self_study_support(ROOT)) >= 32
    assert build_pdf.verify_pdf(ROOT, output, edition="self-study") == manifest["page_count"]

    monkeypatch.setattr(
        build_pdf,
        "required_self_study_feedback",
        lambda _root: [("ans.missing.v1", ["MISSING_FEEDBACK_MARKER"])],
    )
    with pytest.raises(build_pdf.PdfBuildError, match="missing answer explanation"):
        build_pdf.verify_pdf(ROOT, output, edition="self-study")


def test_self_study_pdf_requires_staged_support(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "self-study.pdf"
    build_pdf.build(ROOT, output, edition="self-study")

    monkeypatch.setattr(
        build_pdf,
        "required_self_study_support",
        lambda _root: [("ans.missing.v1 hint 1", ["MISSING_SUPPORT_MARKER"])],
    )
    with pytest.raises(build_pdf.PdfBuildError, match="missing ans.missing.v1 hint 1"):
        build_pdf.verify_pdf(ROOT, output, edition="self-study")


def test_semantic_hash_ignores_pdf_metadata(tmp_path: Path) -> None:
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"

    for output, title in ((first, "First"), (second, "Second")):
        writer = PdfWriter()
        writer.add_blank_page(width=build_pdf.A4_WIDTH_POINTS, height=build_pdf.A4_HEIGHT_POINTS)
        writer.add_metadata({"/Title": title})
        with output.open("wb") as stream:
            writer.write(stream)

    assert build_pdf.sha256(first) != build_pdf.sha256(second)
    assert build_pdf.semantic_sha256(first) == build_pdf.semantic_sha256(second)


def test_semantic_hash_detects_changed_image_resource(tmp_path: Path) -> None:
    def write_image_pdf(output: Path, pixel: bytes) -> None:
        writer = PdfWriter()
        page = writer.add_blank_page(width=build_pdf.A4_WIDTH_POINTS, height=build_pdf.A4_HEIGHT_POINTS)
        image = DecodedStreamObject()
        image.set_data(pixel)
        image.update(
            {
                NameObject("/Type"): NameObject("/XObject"),
                NameObject("/Subtype"): NameObject("/Image"),
                NameObject("/Width"): NumberObject(1),
                NameObject("/Height"): NumberObject(1),
                NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
                NameObject("/BitsPerComponent"): NumberObject(8),
            }
        )
        image_ref = writer._add_object(image)
        page[NameObject("/Resources")] = DictionaryObject(
            {NameObject("/XObject"): DictionaryObject({NameObject("/Im0"): image_ref})}
        )
        content = DecodedStreamObject()
        content.set_data(b"q 100 0 0 100 10 10 cm /Im0 Do Q")
        page[NameObject("/Contents")] = writer._add_object(content)
        with output.open("wb") as stream:
            writer.write(stream)

    red = tmp_path / "red.pdf"
    blue = tmp_path / "blue.pdf"
    write_image_pdf(red, bytes((255, 0, 0)))
    write_image_pdf(blue, bytes((0, 0, 255)))

    assert build_pdf.semantic_sha256(red) != build_pdf.semantic_sha256(blue)


def test_semantic_hash_detects_changed_page_geometry(tmp_path: Path) -> None:
    unrotated = tmp_path / "unrotated.pdf"
    rotated = tmp_path / "rotated.pdf"

    for output, rotation in ((unrotated, 0), (rotated, 90)):
        writer = PdfWriter()
        page = writer.add_blank_page(width=build_pdf.A4_WIDTH_POINTS, height=build_pdf.A4_HEIGHT_POINTS)
        page.rotate(rotation)
        with output.open("wb") as stream:
            writer.write(stream)

    assert build_pdf.semantic_sha256(unrotated) != build_pdf.semantic_sha256(rotated)


def test_pdf_verifier_rejects_non_a4_page(tmp_path: Path) -> None:
    output = tmp_path / "letter.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with output.open("wb") as stream:
        writer.write(stream)

    with pytest.raises(build_pdf.PdfBuildError, match="is not A4"):
        build_pdf.verify_pdf(ROOT, output)
