# AI Open Textbook Starter

This repository is a starter kit for building AI-native open educational materials.
It is designed for public GitHub development, agent-assisted workflows, human review, and versioned educational data.

## Scope

The first MVP targets:

- Stage: High school
- Subject: Information I
- Unit: Programming Basics
- Lessons:
  1. Variables and Assignment
  2. Conditionals
  3. Loops

This repository does **not** claim to be an official government-approved textbook.
It is an open educational material, supplemental teaching aid, and self-study resource.

## Design choice

The source of truth is NoSQL-style NDJSON under `data/collections/`.
SQLite is treated as a generated index under `build/`, not as the canonical database.

Why:

- Educational answers, rubrics, and explanations change over time.
- Each item needs independent review status, evidence, and revision history.
- NDJSON is easy to diff, review, migrate, and process in GitHub PRs.
- SQLite remains useful for search, reports, and local dashboards.

## Quick start

```bash
python3 scripts/validate_ndjson.py
python3 scripts/build_sqlite_index.py
```

Optional:

```bash
make validate
make sqlite
```

## Key files

- `AGENTS.md`: Repository-wide instructions for AI agents.
- `CLAUDE.md`: Claude Code bridge that points to `AGENTS.md`.
- `docs/OPERATING_RULES.md`: Human and AI operating rules.
- `docs/DATA_MODEL.md`: NoSQL-first data model and SQLite projection.
- `docs/PROCESS.md`: End-to-end production flow.
- `.claude/agents/`: Specialist subagent definitions.
- `data/collections/`: Versioned NDJSON collections.
- `schemas/`: Lightweight JSON schema documents.
- `scripts/`: Validation and indexing utilities.

## Licensing

- Educational content: CC BY 4.0 unless noted otherwise.
- Code and scripts: MIT License unless noted otherwise.

See `LICENSE-CONTENT-CC-BY-4.0.md` and `LICENSE-CODE-MIT.md`.
