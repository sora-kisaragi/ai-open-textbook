#!/usr/bin/env python3
"""Tests for the learner-only PDF workflow."""
from __future__ import annotations

from pathlib import Path

from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject, NumberObject
from pypdf import PdfWriter
import pytest

from scripts import build_pdf


ROOT = Path(__file__).resolve().parents[1]


def test_pdf_build_is_repeatable_and_verified(tmp_path: Path) -> None:
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"

    first_manifest = build_pdf.build(ROOT, first)
    second_manifest = build_pdf.build(ROOT, second)

    assert first_manifest["page_count"] >= 1
    assert first_manifest["implemented_lesson_count"] == 23
    assert first_manifest["planned_lesson_count"] == 32
    assert first_manifest["input_sha256"] == second_manifest["input_sha256"]
    assert first_manifest["semantic_sha256"] == second_manifest["semantic_sha256"]
    assert build_pdf.verify_pdf(ROOT, first) == first_manifest["page_count"]


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
