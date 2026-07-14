# AI Open Textbook

This repository builds Japanese open educational material for Information I.
It is designed for public GitHub development, agent-assisted workflows, human
review, and versioned educational data.

## Scope

The current v0.2 review-candidate plan targets:

- Stage: High school
- Subject: Information I
- Scope: all four provisional Information I content areas
- Curriculum: 4 units and 32 planned lessons
- Delivery: Japanese learner material, supplemental teacher guides, offline HTML,
  and reproducible print/PDF output
- Example programming language: Python, used to teach transferable concepts

See `docs/MVP_SCOPE.md`, `docs/CURRICULUM_MAP.md`, and
`docs/INFORMATION_I_COMPLETION_MATRIX.md` for the active draft scope and direct
evidence requirements.

This repository does **not** claim to be an official government-approved
textbook or finally curriculum-aligned. It is an open educational material,
supplemental teaching aid, and self-study resource under human review.

## Design choice

Educational records use canonical NDJSON under `data/collections/`. The
subject-wide plan is canonicalized separately in
`curriculum/highschool_information_i.curriculum.json`. SQLite is a generated
index under `build/`, not a canonical database.

Why:

- Educational answers, rubrics, and explanations change over time.
- Each item needs independent review status, evidence, and revision history.
- NDJSON is easy to diff, review, migrate, and process in GitHub PRs.
- SQLite remains useful for search, reports, and local dashboards.

## Quick start

```bash
uv sync --locked --extra dev
uv run python -m playwright install chromium
uv run python scripts/validate_ndjson.py
uv run python scripts/build_sqlite_index.py
uv run python scripts/check_examples.py
uv run python scripts/build_static_site.py
uv run python scripts/verify_static_site.py
uv run python scripts/build_pdf.py
uv run python -m pytest
```

For a branch or pull request, also run
`uv run python scripts/check_revision_history.py --base-ref <base-commit>`.
This enforces revision events against the actual Git change set.

On Windows, keep `uv run python` so the locked environment is used. If direct
interpreter invocation is required, use `.venv\Scripts\python.exe`; do not
substitute an unqualified system `python` after `uv sync`.
GNU Make users may run the complete sequence with:

```bash
make check
```

## Key files

- `AGENTS.md`: Repository-wide instructions for AI agents.
- `CLAUDE.md`: Claude Code bridge that points to `AGENTS.md`.
- `docs/OPERATING_RULES.md`: Human and AI operating rules.
- `docs/DATA_MODEL.md`: NoSQL-first data model and SQLite projection.
- `docs/TOOLING_GATES.md`: Locked validation, execution, HTML, and PDF gates.
- `docs/PROCESS.md`: End-to-end production flow.
- `.claude/agents/`: Specialist subagent definitions.
- `data/collections/`: Versioned NDJSON collections.
- `schemas/`: Executable JSON Schema contracts for canonical records and curriculum.
- `scripts/`: Validation, execution, indexing, HTML, and PDF build utilities.

## Licensing

- Educational content: CC BY 4.0 unless noted otherwise.
- Code and scripts: MIT License unless noted otherwise.

See `LICENSE-CONTENT-CC-BY-4.0.md` and `LICENSE-CODE-MIT.md`.
