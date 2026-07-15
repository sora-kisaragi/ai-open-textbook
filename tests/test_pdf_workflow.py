#!/usr/bin/env python3
"""Tests for the learner-only PDF workflow."""
from __future__ import annotations

from pathlib import Path

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
    assert first_manifest["implemented_lesson_count"] == 8
    assert first_manifest["planned_lesson_count"] == 32
    assert first_manifest["input_sha256"] == second_manifest["input_sha256"]
    assert first_manifest["output_sha256"] == second_manifest["output_sha256"]
    assert build_pdf.verify_pdf(ROOT, first) == first_manifest["page_count"]


def test_pdf_verifier_rejects_non_a4_page(tmp_path: Path) -> None:
    output = tmp_path / "letter.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with output.open("wb") as stream:
        writer.write(stream)

    with pytest.raises(build_pdf.PdfBuildError, match="is not A4"):
        build_pdf.verify_pdf(ROOT, output)
