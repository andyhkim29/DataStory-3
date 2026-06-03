<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles:
- IV. Reproducible Analysis By Default (expanded with notebook/code requirements)
- V. Clear Storytelling With Caveats (expanded with README deliverable requirements)
Added sections:
- Project Deliverables
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ specs/001-song-popularity-analysis/spec.md
- ⚠ .specify/templates/commands/*.md not present in this installation; no update possible
Follow-up TODOs:
- None
-->
# DataStory-3 Constitution

## Core Principles

### I. Data Provenance Is Mandatory

Every analysis MUST identify its dataset source, access method, version or download
date when available, license constraints, and any derived files. Raw inputs MUST
remain distinguishable from processed outputs. Any manual edits, filters, joins,
or exclusions MUST be documented where a reviewer can inspect them.

Rationale: Data stories are only credible when readers can trace conclusions back
to the source and understand what changed between raw data and final evidence.

### II. Popularity Definitions Must Be Honest

Any metric labeled as popularity MUST be explicitly defined before analysis uses
it. If the available data contains only a proxy, such as playlist presence or
frequency, the work MUST call it a proxy and avoid claims about universal listener
preference, streaming counts, cultural impact, or causation.

Rationale: The current project asks what makes songs popular, but the referenced
dataset may not include direct popularity scores. Ambiguous targets create
misleading answers.

### III. Evidence Before Claims

Every major conclusion MUST be supported by a visible statistic, chart, table, or
model result. Analysis MUST distinguish correlation from causation and MUST state
important alternative explanations. Claims that are not supported by the dataset
MUST be removed or labeled as hypotheses.

Rationale: The final story should persuade through inspectable evidence, not
through unsupported narrative.

### IV. Reproducible Analysis By Default

The repository MUST include enough instructions, dependency information, file
paths, and execution order for another person to recreate the final outputs from
the documented inputs. Generated artifacts MUST be reproducible or clearly marked
as manually produced. Large-data workflows MUST use deterministic sampling or
document nondeterministic choices. Project code, including notebooks and scripts,
MUST be well documented enough for another person to run and understand the
analysis without private context.

Rationale: A data analysis that cannot be rerun cannot be reviewed, debugged, or
extended with confidence.

### V. Clear Storytelling With Caveats

Final outputs MUST answer the user-facing question in plain language, prioritize
the most important findings, and include limitations. Visualizations MUST have
clear labels, units, and enough context to be interpreted without reading code.
The report MUST avoid overstating precision or certainty. The repository README
MUST be the entry point for the data story and include project metadata,
overview, data links, replication instructions, contributing notes,
acknowledgements, and citations.

Rationale: This project is a data story, so the deliverable is both analysis and
communication.

## Data And Environment Standards

- Raw downloaded data MUST live outside generated output directories or be clearly
  separated from processed data.
- Processed data files MUST include enough naming or documentation to identify the
  transformation that produced them.
- Large files that cannot reasonably be committed MUST be documented with download
  and placement instructions instead of silently omitted.
- Dependency and runtime assumptions MUST be captured before implementation work
  begins.
- Privacy, licensing, and platform terms MUST be checked before redistributing
  external datasets or derived records.
- If data files total less than 10 MB, they SHOULD be included directly in the
  project folder unless licensing prevents redistribution.
- If data files total 10 MB or more, they MUST be hosted at an accessible external
  location and documented in the README.
- The notebook or code MUST include steps to download or import the data so
  results can be reproduced from a fresh checkout.

## Project Deliverables

- `README.md` MUST include the project name, authors, GitHub usernames, main
  question, approach, data used, tools used, key findings, data links, running
  instructions, contributing or next-step notes, known issues, acknowledgements,
  and citations.
- A YouTube or video link is NOT required for this project unless a future user
  request explicitly restores that deliverable.
- Code deliverables MUST include the notebook, scripts, or equivalent analysis
  files needed to reproduce the results.
- Data deliverables MUST follow the size rule in Data And Environment Standards
  and MUST never rely on undocumented local-only files.

## Workflow And Review Gates

- Specs MUST define the analytical question, target metric, assumptions, and
  success criteria before planning.
- Plans MUST pass a constitution check covering provenance, target definition,
  evidence, reproducibility, scale, and final communication.
- Tasks MUST include explicit work for data validation, reproducible execution,
  evidence generation, and limitation review.
- Reviews MUST verify that final claims match the evidence and that caveats are
  visible in the final output.
- Reviews MUST verify that `README.md` includes the required project metadata,
  overview, data access, replication, contributing, acknowledgements, and
  citation sections.
- Any intentional exception to this constitution MUST be documented in the plan's
  Complexity Tracking section with a simpler alternative considered.

## Governance

This constitution supersedes conflicting local practices for DataStory-3 work.
Amendments require an explicit update to this file, a Sync Impact Report, and a
review of dependent templates and runtime guidance. Versioning follows semantic
versioning: MAJOR for incompatible governance or principle changes, MINOR for new
or materially expanded principles or sections, and PATCH for clarifications that
do not change obligations. Compliance MUST be checked during `/speckit-plan`,
`/speckit-tasks`, and implementation review.

**Version**: 1.1.0 | **Ratified**: 2026-06-03 | **Last Amended**: 2026-06-03
