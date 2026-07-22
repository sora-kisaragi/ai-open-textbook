# Information I Semantic Coverage Audit

## Method

This table records 96 objective-level verdicts as three cells for each of the
32 lessons. `Supported` means the referenced problem or criterion directly
elicits the objective, while the second artifact requires a distinct
application, synthesis, or performance observation. Structural link and
criterion validity are checked separately by `validate_ndjson.py`.

Two rows were downgraded to `partial`. D2.O1 has one direct artifact for
distinguishing the Internet, Web, an information service, URI, and URL. D6.O2
has direct numerical calculation evidence but no second artifact that requires
calculating token frequencies. The non-measuring `.004` references were
removed from those rows.

## Verdicts

| Lesson | O1 | O2 | O3 | Evidence reviewed |
| --- | --- | --- | --- | --- |
| A1 Information and Media | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| A2 Source Evaluation | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| A3 Rights and Responsibility | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| A4 Problem Definition | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| A5 Decomposition and Modeling | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| A6 Solution Evaluation | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| A7 Inquiry Project | Supported | Supported | Supported | Items `.001`-`.003` plus rubric criteria `c1`, `c2`, and `c3` respectively |
| B1 Communication Media | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| B2 Digital Representation | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| B3 Audience and Accessibility | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| B4 Information Structure | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| B5 Data Visualization | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| B6 Prototype and Usability | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| B7 Information Design Project | Supported | Supported | Supported | Items `.001`-`.003` plus rubric criteria `c1`, `c6`, and `c8` respectively |
| C1 Computer Systems | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| C2 Variables | Supported | Supported | Supported | Independent items `.003`-`.008`; guided `.001` and `.002` are excluded from coverage |
| C3 Conditionals | Supported | Supported | Supported | Independent tracing, creation, boundary, and transfer items `.001`-`.008` |
| C4 Loops | Supported | Supported | Supported | Independent explanation, tracing, creation, boundary, and transfer items `.001`-`.008` |
| C5 Collections and Strings | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| C6 Functions | Supported | Supported | Supported | Direct items `.001`-`.003` plus executable synthesis `.004` |
| C7 Algorithms | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| C8 Modeling and Simulation | Supported | Supported | Supported | Direct items `.001`-`.003` plus deterministic synthesis `.004` |
| C9 Programming Project | Supported | Supported | Supported | Items `.001`-`.003` plus criteria `c1`, `c2`, and `c5`-`c8` |
| D1 Networks and Protocols | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| D2 Internet and Web Services | Partial | Supported | Supported | O1 retains direct item `.001`; O2 and O3 use direct items plus synthesis `.004` |
| D3 Security | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| D4 Data Lifecycle | Supported | Supported | Supported | Items `.001`-`.003` plus integrated classification and planning item `.004`; `.002` also checks scale choice |
| D5 Data Cleaning | Supported | Supported | Supported | Direct items `.001`-`.003` plus tabular and text synthesis `.004` |
| D6 Descriptive Analysis | Supported | Partial | Supported | O2 retains numerical calculation item `.002`; O1 and O3 use direct items plus synthesis `.004` |
| D7 Visualization Interpretation | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| D8 Databases and Queries | Supported | Supported | Supported | Direct items `.001`-`.003` plus synthesis `.004` |
| D9 Data Investigation Project | Supported | Supported | Supported | Items `.001`-`.003` plus criteria covering ethics, reproducibility, evidence, provenance, transformation, independent checks, bounded conclusions, limits, sensitivity, and revision |

## Review Boundary

This semantic audit supports the Draft PR review. It does not substitute for
the final human decisions on curriculum interpretation, age appropriateness,
scoring validity, or classroom use.
