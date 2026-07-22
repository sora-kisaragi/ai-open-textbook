#!/usr/bin/env python3
"""Tests for the Information I integration contract."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts import check_integration_contract


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def integration_root(tmp_path: Path) -> Path:
    for relative in ("curriculum", "data", "docs", "lessons", "teacher_guides"):
        shutil.copytree(ROOT / relative, tmp_path / relative)
    return tmp_path


def test_repository_satisfies_integration_contract() -> None:
    failures, stats = check_integration_contract.check_repository(ROOT)

    assert failures == []
    assert stats.lessons == 32
    assert stats.transfer_probes == 32
    assert stats.scheduled_periods == 65
    assert stats.coverage_rows == 96
    assert stats.machine_checked_answers == 22


def test_missing_transfer_probe_is_rejected(integration_root: Path) -> None:
    path = integration_root / "lessons/highschool_information_i/society/01_information_media.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("## 別の場面への転移", "## 転移を削除", 1)
    path.write_text(text, encoding="utf-8")

    failures, _ = check_integration_contract.check_repository(integration_root)

    assert any("expected one transfer section" in failure for failure in failures)


def test_schedule_must_cover_mandatory_periods(integration_root: Path) -> None:
    path = integration_root / "teacher_guides/highschool_information_i/programming/01_variables.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("| 第1時 |", "| 第2時 |", 1)
    path.write_text(text, encoding="utf-8")

    failures, _ = check_integration_contract.check_repository(integration_root)

    assert any("invalid schedule row 1" in failure for failure in failures)


def test_coverage_audit_must_record_all_objectives(integration_root: Path) -> None:
    path = integration_root / "docs/review/INFORMATION_I_COVERAGE_AUDIT.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("| Supported | Supported | Supported |", "| Missing | Supported | Supported |", 1)
    path.write_text(text, encoding="utf-8")

    failures, _ = check_integration_contract.check_repository(integration_root)

    assert any("coverage audit records 95" in failure for failure in failures)


def test_unreviewed_machine_claim_is_rejected(integration_root: Path) -> None:
    path = integration_root / "data/collections/answers.ndjson"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    answer = next(
        record for record in records
        if record["id"] == "ans.prob.info1.society.information.media.001.v1"
    )
    answer["verification_status"] = "machine_checked"
    answer["verification_evidence"] = [{
        "checked_at": "2026-07-22",
        "command": "manual comparison",
        "expected": "a qualitative judgment",
        "method": "compare prose",
        "result": "passed",
    }]
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )

    failures, _ = check_integration_contract.check_repository(integration_root)

    assert any("unreviewed machine_checked claim" in failure for failure in failures)


def test_reviewed_exemplar_must_keep_machine_evidence(integration_root: Path) -> None:
    path = integration_root / "data/collections/answers.ndjson"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    answer = next(
        record for record in records
        if record["id"] == "ans.prob.info1.programming.project.004.v1"
    )
    answer.pop("verification_status")
    answer.pop("verification_evidence")
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )

    failures, _ = check_integration_contract.check_repository(integration_root)

    assert any("deterministic answer is not machine_checked" in failure for failure in failures)
