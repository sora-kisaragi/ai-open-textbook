#!/usr/bin/env python3
"""Tests for the source manifest exporter."""
from __future__ import annotations

from pathlib import Path
import subprocess

from scripts import export_manifest


def test_manifest_excludes_itself_and_generated_directories(tmp_path: Path) -> None:
    (tmp_path / "source.txt").write_text("source", encoding="utf-8")
    (tmp_path / "MANIFEST.json").write_text("stale", encoding="utf-8")
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "artifact.pdf").write_bytes(b"generated")
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "local.txt").write_text("local", encoding="utf-8")

    rows = export_manifest.build_rows(
        tmp_path,
        [
            Path("source.txt"),
            Path("MANIFEST.json"),
            Path("build/artifact.pdf"),
            Path(".venv/local.txt"),
        ],
    )

    assert [row["path"] for row in rows] == ["source.txt"]
    assert rows[0]["bytes"] == 6


def test_manifest_defaults_to_git_index_and_ignores_local_files(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text(".env\n.claude/settings.local.json\n", encoding="utf-8")
    (tmp_path / "tracked.txt").write_text("tracked", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=local", encoding="utf-8")
    local_settings = tmp_path / ".claude" / "settings.local.json"
    local_settings.parent.mkdir()
    local_settings.write_text("{}", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore", "tracked.txt"], cwd=tmp_path, check=True)

    rows = export_manifest.build_rows(tmp_path)

    assert [row["path"] for row in rows] == [".gitignore", "tracked.txt"]
