#!/usr/bin/env python3
"""Smoke test for the starter data."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_validate_sample():
    result = subprocess.run([sys.executable, 'scripts/validate_ndjson.py'], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
