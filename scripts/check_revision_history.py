#!/usr/bin/env python3
"""Check Git changes against the append-only canonical revision policy."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

try:
    from scripts import validate_ndjson
except ModuleNotFoundError:  # Direct script execution places scripts/ on sys.path.
    import validate_ndjson


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
NON_CONTENT_FIELDS = {"status", "review_status", "verification_status", "updated_at"}
CONTENT_CHANGE_TYPES = {"update", "supersede", "deprecate"}


class RevisionHistoryError(RuntimeError):
    """Raised when Git history cannot be inspected."""


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RevisionHistoryError(f"git {' '.join(args)} failed: {detail}")
    return result


def records_from_text(text: str, label: str) -> dict[str, dict]:
    records: dict[str, dict] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RevisionHistoryError(f"{label}:{line_no}: invalid JSON: {exc}") from exc
        record_id = record.get("id") if isinstance(record, dict) else None
        if not isinstance(record_id, str) or not record_id:
            raise RevisionHistoryError(f"{label}:{line_no}: record is missing id")
        if record_id in records:
            raise RevisionHistoryError(f"{label}:{line_no}: duplicate id: {record_id}")
        records[record_id] = record
    return records


def current_text(root: Path, relative: str) -> str:
    path = root / relative
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def base_text(root: Path, base_ref: str, relative: str) -> str:
    result = git(root, "show", f"{base_ref}:{relative}", check=False)
    if result.returncode == 0:
        return result.stdout
    missing_markers = ("does not exist in", "exists on disk, but not in", "Path '")
    if any(marker in result.stderr for marker in missing_markers):
        return ""
    raise RevisionHistoryError(
        f"cannot read {relative} at {base_ref}: {result.stderr.strip() or result.stdout.strip()}"
    )


def load_snapshot(root: Path, base_ref: str | None) -> tuple[dict[str, dict], dict[str, dict]]:
    canonical: dict[str, dict] = {}
    revisions: dict[str, dict] = {}
    for filename in validate_ndjson.COLLECTION_FILES:
        relative = f"data/collections/{filename}"
        text = base_text(root, base_ref, relative) if base_ref else current_text(root, relative)
        loaded = records_from_text(text, f"{base_ref or 'worktree'}:{relative}")
        if filename == "revisions.ndjson":
            revisions.update(loaded)
        else:
            canonical.update(loaded)

    curriculum_relative = validate_ndjson.CURRICULUM_PATH.as_posix()
    curriculum_source = (
        base_text(root, base_ref, curriculum_relative)
        if base_ref
        else current_text(root, curriculum_relative)
    )
    if curriculum_source.strip():
        curriculum = json.loads(curriculum_source)
        curriculum_id = curriculum.get("id") if isinstance(curriculum, dict) else None
        if not isinstance(curriculum_id, str):
            raise RevisionHistoryError(f"{curriculum_relative}: curriculum is missing id")
        canonical[curriculum_id] = curriculum
    return canonical, revisions


def changed_paths(root: Path, base_ref: str) -> set[str]:
    tracked = git(root, "diff", "--name-only", "--diff-filter=ACMRD", base_ref, "--")
    untracked = git(root, "ls-files", "--others", "--exclude-standard")
    return {
        line.strip().replace("\\", "/")
        for line in (tracked.stdout + "\n" + untracked.stdout).splitlines()
        if line.strip()
    }


def lesson_content_entities(current: dict[str, dict], paths: set[str]) -> set[str]:
    changed: set[str] = set()
    for record in current.values():
        if record.get("type") != "lesson" or not isinstance(record.get("body_ref"), str):
            continue
        body_ref = record["body_ref"].replace("\\", "/")
        body_path = Path(body_ref)
        teacher_ref = Path("teacher_guides", *body_path.parts[1:]).as_posix()
        if body_ref in paths or teacher_ref in paths:
            changed.add(str(record["id"]))
    return changed


def check_status_transition(
    errors: list[str], old: dict | None, new: dict, events: list[dict]
) -> None:
    new_status = new.get("status")
    if old is None:
        if new_status in {"approved", "published"}:
            errors.append(f"{new['id']}: new records cannot start at status {new_status}")
        return
    old_status = old.get("status")
    if old_status == new_status:
        return
    event_types = {event.get("change_type") for event in events}
    if new_status == "published":
        if old_status != "approved" or "publish" not in event_types:
            errors.append(f"{new['id']}: published requires prior approved status and a publish revision")
    elif new_status == "approved" and old_status != "human_review_requested":
        errors.append(f"{new['id']}: approved requires prior human_review_requested status")
    elif new_status == "human_review_requested" and "review_request" not in event_types:
        errors.append(f"{new['id']}: human_review_requested requires a review_request revision")
    elif new_status == "deprecated" and "deprecate" not in event_types:
        errors.append(f"{new['id']}: deprecated requires a deprecate revision")
    elif new_status == "superseded" and "supersede" not in event_types:
        errors.append(f"{new['id']}: superseded requires a supersede revision")
    if old_status == "published" and new_status not in {"deprecated", "superseded"}:
        errors.append(f"{new['id']}: published records may only move to deprecated or superseded")


def content_changed(old: dict, new: dict) -> bool:
    old_content = {key: value for key, value in old.items() if key not in NON_CONTENT_FIELDS}
    new_content = {key: value for key, value in new.items() if key not in NON_CONTENT_FIELDS}
    return old_content != new_content


def check_repository(root: Path, base_ref: str) -> list[str]:
    root = root.resolve()
    git(root, "rev-parse", "--verify", f"{base_ref}^{{commit}}")
    base, base_revisions = load_snapshot(root, base_ref)
    current, current_revisions = load_snapshot(root, None)
    paths = changed_paths(root, base_ref)
    errors: list[str] = []

    for revision_id, old_revision in base_revisions.items():
        if revision_id not in current_revisions:
            errors.append(f"{revision_id}: revision history is append-only; event was deleted")
        elif current_revisions[revision_id] != old_revision:
            errors.append(f"{revision_id}: revision history is append-only; event was modified")

    new_events = [
        revision for revision_id, revision in current_revisions.items()
        if revision_id not in base_revisions
    ]
    events_by_entity: dict[str, list[dict]] = {}
    for event in new_events:
        events_by_entity.setdefault(str(event.get("entity_id")), []).append(event)

    changed_entities = {
        entity_id
        for entity_id in set(base) | set(current)
        if base.get(entity_id) != current.get(entity_id)
    }
    changed_lesson_content = lesson_content_entities(current, paths)
    changed_entities.update(changed_lesson_content)

    for entity_id in sorted(changed_entities):
        old = base.get(entity_id)
        new = current.get(entity_id)
        if new is None:
            errors.append(f"{entity_id}: canonical entities cannot be deleted without a retained tombstone")
            continue
        events = events_by_entity.get(entity_id, [])
        if not events:
            errors.append(f"{entity_id}: canonical change requires a new revision event")
            continue
        if old is None and not any(event.get("change_type") == "create" for event in events):
            errors.append(f"{entity_id}: new canonical entity requires a create revision")
        if old is not None and (
            content_changed(old, new) or entity_id in changed_lesson_content
        ) and not any(event.get("change_type") in CONTENT_CHANGE_TYPES for event in events):
            errors.append(f"{entity_id}: content change requires an update, supersede, or deprecate revision")
        check_status_transition(errors, old, new, events)

    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Repository root.")
    parser.add_argument("--base-ref", required=True, help="Git commit/ref to compare with the worktree.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        errors = check_repository(args.root, args.base_ref)
    except (OSError, json.JSONDecodeError, RevisionHistoryError) as exc:
        print(f"Revision history check failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("Revision history check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Revision history check passed against {args.base_ref}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
