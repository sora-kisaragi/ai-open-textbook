#!/usr/bin/env bash
# Register the MVP issue set on GitHub.
# Prerequisites: gh CLI installed and authenticated (gh auth status),
# repo remote configured. Run from the repository root:
#   bash docs/issue-drafts/create_issues.sh
set -euo pipefail

DRAFT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Ensure labels exist (idempotent) ---
ensure_label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --color "$color" --description "$desc" 2>/dev/null \
    || echo "label exists: $name"
}

ensure_label "phase:mvp"                 "0052CC" "MVP phase work"
ensure_label "subject:information-i"     "1D76DB" "Japanese HS Information I"
ensure_label "type:planning"             "C2E0C6" "Scope and planning"
ensure_label "type:curriculum"           "BFD4F2" "Curriculum mapping"
ensure_label "type:lesson"               "0E8A16" "Lesson requirements/content"
ensure_label "type:problem-bank"         "5319E7" "Exercises, answers, rubrics"
ensure_label "type:data-model"           "FBCA04" "NDJSON schema and data policy"
ensure_label "type:review"               "D93F0B" "Review process work"
ensure_label "type:release"              "B60205" "Release preparation"
ensure_label "type:automation"           "006B75" "Validation and build automation"
ensure_label "status:needs-human-review" "E99695" "Requires human review before approval"
ensure_label "risk:copyright"            "D4C5F9" "Copyright/originality risk"
ensure_label "risk:pedagogy"             "F9D0C4" "Pedagogy/age-fit risk"
ensure_label "risk:accessibility"        "C5DEF5" "Accessibility risk"

# --- Create issues from drafts (frontmatter stripped) ---
create_issue() {
  local file="$1" title="$2" labels="$3"
  local body
  body="$(awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2' "$DRAFT_DIR/$file")"
  gh issue create --title "$title" --label "$labels" --body "$body"
}

create_issue "01-mvp-scope.md" \
  "Define MVP scope and release boundary" \
  "phase:mvp,type:planning,subject:information-i"

create_issue "02-curriculum-map.md" \
  "Create curriculum map for Programming Basics" \
  "phase:mvp,type:curriculum,subject:information-i,status:needs-human-review"

create_issue "03-schema-validation-policy.md" \
  "Strengthen schema and validation policy for NDJSON collections" \
  "phase:mvp,type:data-model,type:automation"

create_issue "04-lesson-01-variables.md" \
  "Draft Lesson 01 requirements: Variables and assignment" \
  "phase:mvp,type:lesson,subject:information-i,status:needs-human-review"

create_issue "05-lesson-02-conditionals.md" \
  "Draft Lesson 02 requirements: Conditionals" \
  "phase:mvp,type:lesson,subject:information-i,status:needs-human-review"

create_issue "06-lesson-03-loops.md" \
  "Draft Lesson 03 requirements: Loops" \
  "phase:mvp,type:lesson,subject:information-i,status:needs-human-review"

create_issue "07-problem-bank-design.md" \
  "Design the MVP problem bank" \
  "phase:mvp,type:problem-bank,subject:information-i,status:needs-human-review"

create_issue "08-answer-rubric-versioning.md" \
  "Define answer and rubric versioning workflow" \
  "phase:mvp,type:data-model,type:review"

create_issue "09-teacher-guide-requirements.md" \
  "Create teacher guide requirements for the MVP lessons" \
  "phase:mvp,type:lesson,type:review,subject:information-i"

create_issue "10-review-checklist.md" \
  "Define pedagogy, copyright, and accessibility review checklist" \
  "phase:mvp,type:review,risk:pedagogy,risk:copyright,risk:accessibility"

create_issue "11-export-index-workflow.md" \
  "Prepare export and index workflow for review builds" \
  "phase:mvp,type:automation,type:data-model"

create_issue "12-release-checklist.md" \
  "Prepare MVP release checklist" \
  "phase:mvp,type:release,type:review,status:needs-human-review"

echo "Done. 12 issues created."
