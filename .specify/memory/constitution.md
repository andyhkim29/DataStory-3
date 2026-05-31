<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- Placeholder Principle 1 -> I. Verification Before Analysis
- Placeholder Principle 2 -> II. Reproducible Data Lineage
- Placeholder Principle 3 -> III. Person-Level Measures and Traceability
- Placeholder Principle 4 -> IV. Story Outputs With Explicit Caveats
- Placeholder Principle 5 -> V. Scoped, Minimal Analysis
Added sections:
- Data and Storage Standards
- Development Workflow and Quality Gates
Removed sections:
- Template placeholder sections
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ⚠ .specify/templates/commands/*.md not present in this installation
Follow-up TODOs:
- None
-->
# DataStory-3 Constitution

## Core Principles

### I. Verification Before Analysis

Every data story MUST verify source coverage, integrity, and known quality risks
before deriving findings. If verification fails or reveals degraded coverage, the
notebook or pipeline MUST make the degradation visible before downstream outputs
and MUST either apply a documented fallback or label findings as limited. This is
non-negotiable because story claims are only defensible when the input evidence
has been checked first.

### II. Reproducible Data Lineage

Every delivered number, chart, and written claim MUST be reproducible from the
repository plus documented external data sources. Raw data acquisition MUST be
cached or otherwise repeatable, processed data MUST be written to stable files,
and transformations MUST be documented enough for a reviewer to trace outputs
back to inputs. Manual inputs are allowed only when they are small, named, and
clearly separated from generated data.

### III. Person-Level Measures and Traceability

Analyses involving public officials, organizations, or other real-world entities
MUST define the unit of analysis explicitly and preserve stable identifiers
through every join and aggregation. Entity collapsing, exclusions, date-window
normalization, and unmatched records MUST be documented in the notebook or
supporting files. This prevents technically valid calculations from answering
the wrong substantive question.

### IV. Story Outputs With Explicit Caveats

The project MUST produce outputs that support a clear data story: cleaned data,
figures or tables, and concise narrative findings. Visual and written outputs
MUST include the caveats needed to interpret the claim, including coverage
limits, missing measures, and the distinction between suggestive comparisons and
causal or exhaustive conclusions. Claims MUST not exceed what the dataset can
measure.

### V. Scoped, Minimal Analysis

Each feature MUST stay inside its stated analytical scope unless a documented
quality failure requires a fallback. New methods, data sources, or abstractions
MUST be added only when they directly support the accepted story requirements.
Out-of-scope analyses MUST remain out of the implementation plan to keep the
work auditable and finishable.

## Data and Storage Standards

Source data, processed data, manual inputs, and figures MUST live in distinct,
documented locations. Large raw caches SHOULD be regenerated from public sources
or hosted externally instead of committed when they would make the repository
hard to clone or review. Processed outputs that support story claims MUST use
stable schemas with documented columns. Manual files MUST include the source and
lookup method in the notebook or README.

## Development Workflow and Quality Gates

Specifications MUST define the analysis window, data sources, verification
rules, expected outputs, and out-of-scope boundaries. Plans MUST pass a
constitution check covering data verification, reproducibility, entity
traceability, story deliverables, caveats, and scope control before
implementation. Tasks MUST include validation steps that rerun the notebook or
pipeline end-to-end and confirm generated files match the specification.

## Governance

This constitution supersedes conflicting local practices for data-story work in
this repository. Amendments require an update to this file, a Sync Impact Report,
and review of dependent Spec Kit templates. Versioning follows semantic
versioning: MAJOR for incompatible governance or principle changes, MINOR for
new or materially expanded principles or sections, and PATCH for clarifications
that do not change compliance expectations. Each feature plan MUST state whether
it passes the constitution check; any violation MUST include a concrete
justification and a simpler alternative considered.

**Version**: 1.0.0 | **Ratified**: 2026-05-31 | **Last Amended**: 2026-05-31
