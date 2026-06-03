# Implementation Plan: Song Popularity Analysis

**Branch**: `002-song-popularity-analysis` | **Date**: 2026-06-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-song-popularity-analysis/spec.md`

**Note**: This template is filled in by the `/speckit-plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Analyze the Kaggle `devdope/900k-spotify` dataset to
answer "what makes songs popular?" The implementation will build a reproducible
Python notebook workflow that downloads or imports the dataset, inventories
available fields, uses the built-in `Popularity` field as the direct popularity
target, compares the top 10% of tracks by that target against the remaining full
valid dataset across audio features and artist/album metadata, and produces a
README-backed data story with evidence, caveats, and replication instructions.

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: pandas, pyarrow, numpy, scipy, scikit-learn, plotly, kaleido, jupyter, kagglehub  
**Storage**: Local project files with `data/raw/` for source data or download placeholders, `data/processed/` for reproducible derived data, and `figures/` for generated charts  
**Testing**: Notebook execution plus focused pytest checks for reusable data-preparation helpers if scripts are factored out  
**Target Platform**: Local macOS/Linux development environment with a Python virtual environment  
**Project Type**: Reproducible data-analysis notebook with optional helper scripts  
**Performance Goals**: Process the full valid analysis subset from the 900k Spotify CSV without silently dropping records; final findings use the full valid dataset; use column selection, typed reads, Parquet conversion, or deterministic sampling only for exploratory development/performance checks  
**Constraints**: Do not commit the full Kaggle dataset if it exceeds 10 MB; notebook/code must document or perform data download/import; final claims must be supported by visible evidence; no YouTube/video deliverable is required  
**Scale/Scope**: One data story focused on explaining popularity associations for songs in the referenced dataset, not a production recommender or causal inference system

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Data provenance**: PASS. The plan requires Kaggle dataset citation, access URL,
  license/access notes, raw/processed boundaries, and download/import steps.
- **Popularity/target definition**: PASS. The plan requires field inventory and
  uses the built-in `Popularity` field as the direct popularity score.
- **Evidence discipline**: PASS. Every final claim must map to a statistic, chart,
  ranked comparison, or interpretable model result.
- **Reproducibility**: PASS. The workflow includes dependency capture, a rerunnable
  notebook, generated artifact paths, and quickstart validation.
- **Scale handling**: PASS. The plan accounts for large CSV inputs through column
  selection, typed reads, and optional Parquet conversion while requiring final findings
  to use the full valid dataset.
- **Storytelling and caveats**: PASS. The final README and notebook must include
  plain-language findings, labeled visuals, limitations, and alternatives.
- **README deliverable**: PASS. README sections are required for metadata,
  overview, data links, running instructions, contributing/open questions,
  acknowledgements, and citations.
- **Data access rule**: PASS. Large data is externally hosted or downloaded from
  Kaggle; smaller derived data can be committed when licensing allows.
- **Video scope**: PASS. The feature explicitly excludes a YouTube/video
  deliverable unless restored later.

## Project Structure

### Documentation (this feature)

```text
specs/001-song-popularity-analysis/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── data-access-contract.md
│   └── notebook-output-contract.md
├── checklists/
│   └── requirements.md
└── spec.md
```

### Source Code (repository root)

```text
README.md
notebook.ipynb
requirements.txt
data/
├── raw/
│   └── .gitkeep
└── processed/
    └── .gitkeep
figures/
└── .gitkeep
src/
└── song_popularity/
    ├── __init__.py
    ├── data.py
    ├── popularity.py
    └── plots.py
tests/
└── test_popularity.py
```

**Structure Decision**: Use a single notebook-first Python project. The notebook
is the primary readable data story and execution surface. Small helper modules
under `src/song_popularity/` are planned only for reusable loading, target
definition, top-10% segmentation, weak-proxy labeling, and plotting logic that
benefits from tests. `data/raw/` holds downloaded Kaggle inputs or placeholders,
`data/processed/` holds reproducible derived files, and `figures/` holds exported
visuals used by the README.

## Complexity Tracking

No constitution violations are planned.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
