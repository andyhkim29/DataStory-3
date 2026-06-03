---

description: "Task list for song popularity analysis implementation"
---

# Tasks: Song Popularity Analysis

**Input**: Design documents from `/specs/001-song-popularity-analysis/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Include focused pytest tasks for reusable helper logic and notebook execution validation because the plan calls for reproducibility checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the notebook-first Python project structure and baseline documentation files.

- [X] T001 Create project directories `data/raw/`, `data/processed/`, `figures/`, `src/song_popularity/`, and `tests/`
- [X] T002 Add placeholder files `data/raw/.gitkeep`, `data/processed/.gitkeep`, and `figures/.gitkeep`
- [X] T003 Create Python package files `src/song_popularity/__init__.py`, `src/song_popularity/data.py`, `src/song_popularity/popularity.py`, and `src/song_popularity/plots.py`
- [X] T004 Create `requirements.txt` with pandas, pyarrow, numpy, scipy, scikit-learn, plotly, kaleido, jupyter, pytest, and nbconvert
- [X] T005 Create initial `notebook.ipynb` with sections for data source, import, field inventory, target definition, analysis, findings, and limitations
- [X] T006 Create initial `README.md` with required headings for project metadata, overview, data links, running instructions, contributing, acknowledgements, and citations
- [X] T007 Create `tests/test_popularity.py` with imports for helper functions planned in `src/song_popularity/popularity.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared loading, validation, and reproducibility helpers required before any story work.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T008 Implement Kaggle data path constants and expected directory helpers in `src/song_popularity/data.py`
- [X] T009 Implement raw data discovery with clear missing-data error messages in `src/song_popularity/data.py`
- [X] T010 Implement column inventory and missingness summary helpers in `src/song_popularity/data.py`
- [X] T011 Implement duplicate detection helper for track URI and track-name/artist-name fallback keys in `src/song_popularity/data.py`
- [X] T012 Implement audio feature range validation helper in `src/song_popularity/data.py`
- [X] T013 Implement processed output writer for reproducible derived files in `src/song_popularity/data.py`
- [X] T014 [P] Add README data access notes for Kaggle URL, raw data placement, 10 MB storage rule, and license/access caveat in `README.md`
- [X] T015 [P] Add notebook setup cells for dependency assumptions, dataset source, raw data placement, and import path checks in `notebook.ipynb`
- [X] T016 [P] Add pytest coverage for missing data errors, duplicate detection, and audio feature range validation in `tests/test_popularity.py`

**Checkpoint**: Foundation ready; dataset can be located or produce clear setup instructions, and data quality helpers can be tested independently.

---

## Phase 3: User Story 1 - Define And Measure Popularity (Priority: P1) MVP

**Goal**: Select and document a defensible popularity target before any driver analysis.

**Independent Test**: Run the notebook through target-selection cells and verify it identifies the chosen target, source fields, target strength, proxy caveat, and top-10% threshold.

### Tests for User Story 1

- [X] T017 [P] [US1] Add tests for direct popularity target selection in `tests/test_popularity.py`
- [X] T018 [P] [US1] Add tests for playlist-derived proxy selection and proxy labeling in `tests/test_popularity.py`
- [X] T019 [P] [US1] Add tests for artist repetition/count weak-proxy fallback and weak-proxy labeling in `tests/test_popularity.py`
- [X] T020 [P] [US1] Add tests for top-10% segment threshold and segment counts in `tests/test_popularity.py`

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement target candidate detection in `src/song_popularity/popularity.py`
- [X] T022 [P] [US1] Implement artist repetition/count fallback target derivation in `src/song_popularity/popularity.py`
- [X] T023 [US1] Implement popularity target selection with `target_type`, `target_strength`, `target_definition`, and `source_fields` in `src/song_popularity/popularity.py`
- [X] T024 [US1] Implement top-10% popularity segmentation with threshold and counts in `src/song_popularity/popularity.py`
- [X] T025 [US1] Add notebook cells for field inventory, target candidate review, selected target explanation, weak-proxy caveat, and top-10% segment output in `notebook.ipynb`
- [X] T026 [US1] Add README section documenting the selected popularity target, proxy caveat, and top-10% popular segment in `README.md`

**Checkpoint**: User Story 1 is complete when the project can define popularity and report the top-10% segment without performing driver analysis.

---

## Phase 4: User Story 2 - Identify Popularity Drivers (Priority: P2)

**Goal**: Produce evidence-backed findings comparing the top 10% popular segment against remaining tracks across audio features and artist/exposure metadata.

**Independent Test**: Run the notebook through driver-analysis cells and verify it produces full-valid-dataset comparisons, ranked drivers, and charts for both audio and metadata drivers when fields are available.

### Tests for User Story 2

- [X] T027 [P] [US2] Add tests for full-valid-dataset filtering and exclusion counts in `tests/test_popularity.py`
- [X] T028 [P] [US2] Add tests for audio feature comparison summary outputs in `tests/test_popularity.py`
- [X] T029 [P] [US2] Add tests for artist/exposure metadata summary outputs in `tests/test_popularity.py`

### Implementation for User Story 2

- [X] T030 [P] [US2] Implement full-valid-dataset filter and exclusion count summary in `src/song_popularity/data.py`
- [X] T031 [P] [US2] Implement audio feature comparison summaries for top 10% versus remaining tracks in `src/song_popularity/popularity.py`
- [X] T032 [P] [US2] Implement artist/exposure metadata comparison summaries in `src/song_popularity/popularity.py`
- [X] T033 [US2] Implement interpretable driver ranking that combines audio-feature and artist/exposure metadata evidence in `src/song_popularity/popularity.py`
- [X] T034 [P] [US2] Implement reusable Plotly chart helpers for target distribution, segment comparisons, and ranked drivers in `src/song_popularity/plots.py`
- [X] T035 [US2] Add notebook cells for full-valid-dataset filtering, exclusion counts, audio comparisons, metadata comparisons, and ranked driver outputs in `notebook.ipynb`
- [X] T036 [US2] Export required charts to `figures/` from `notebook.ipynb`
- [X] T037 [US2] Add preliminary key findings with evidence references to `README.md`

**Checkpoint**: User Story 2 is complete when the notebook produces ranked, evidence-backed popularity driver findings from the full valid dataset.

---

## Phase 5: User Story 3 - Communicate Actionable Findings (Priority: P3)

**Goal**: Deliver a readable data story with supported claims, caveats, reproducibility instructions, and citations.

**Independent Test**: Read `README.md` and execute `notebook.ipynb`; verify every major finding has linked notebook evidence or generated figures and the project can be reproduced from documented data access steps.

### Tests for User Story 3

- [X] T038 [P] [US3] Add notebook execution validation command notes to `specs/001-song-popularity-analysis/quickstart.md`
- [X] T039 [P] [US3] Add README completeness checklist items to `README.md`

### Implementation for User Story 3

- [X] T040 [US3] Finalize notebook narrative for source, methods, selected target, driver findings, and limitations in `notebook.ipynb`
- [X] T041 [US3] Finalize README project information with project name, authors, and GitHub usernames in `README.md`
- [X] T042 [US3] Finalize README overview with main question, approach, data used, tools used, and key findings in `README.md`
- [X] T043 [US3] Finalize README data links and running instructions for reproducing results from a fresh checkout in `README.md`
- [X] T044 [US3] Finalize README contributing, next steps, open questions, known issues, acknowledgements, and citations in `README.md`
- [X] T045 [US3] Verify README and notebook explicitly state that no YouTube/video deliverable is required in `README.md` and `notebook.ipynb`

**Checkpoint**: User Story 3 is complete when a non-technical reviewer can understand the answer and a technical reviewer can reproduce the analysis.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate reproducibility, clean outputs, and prepare for implementation review.

- [X] T046 Run pytest for helper functions using `pytest tests/`
- [X] T047 Execute notebook end-to-end with nbconvert and save executed output to `notebook.executed.ipynb`
- [X] T048 Verify generated figures exist in `figures/` and are referenced from `README.md`
- [X] T049 Verify no raw Kaggle data over 10 MB is staged for commit under `data/raw/`
- [X] T050 Verify every final README claim has supporting notebook evidence or a generated figure reference in `README.md`
- [X] T051 Verify limitations mention proxy popularity, artist exposure, playlist behavior, genre mix, dataset construction, and non-causal interpretation in `README.md`
- [X] T052 Update `specs/001-song-popularity-analysis/quickstart.md` if actual run commands differ from the planned commands

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion and is the MVP.
- **User Story 2 (Phase 4)**: Depends on User Story 1 because driver analysis requires the selected target and top-10% segment.
- **User Story 3 (Phase 5)**: Depends on User Stories 1 and 2 because final communication needs the target, findings, figures, and caveats.
- **Polish (Phase 6)**: Depends on all selected user stories.

### User Story Dependencies

- **US1 Define And Measure Popularity**: Independent MVP after foundation.
- **US2 Identify Popularity Drivers**: Requires US1 target and segment outputs.
- **US3 Communicate Actionable Findings**: Requires US1 target explanation and US2 evidence outputs.

### Within Each User Story

- Tests for helper logic before implementation helpers.
- Data validation before target selection.
- Target selection before segmentation.
- Segmentation before driver comparisons.
- Driver comparisons before final README findings.
- README claims before final evidence audit.

---

## Parallel Opportunities

- T014, T015, and T016 can run in parallel after T008-T013 are planned because they touch README, notebook, and tests separately.
- T017-T020 can run in parallel because they add separate target/segment test cases in `tests/test_popularity.py`.
- T021 and T022 can run in parallel before T023 integrates target selection.
- T027-T029 can run in parallel because they cover separate full-dataset, audio, and metadata behaviors.
- T030, T031, T032, and T034 can run in parallel because they touch separate helper responsibilities.
- T041-T044 can run in parallel after findings are stable if coordinated carefully across README sections.

## Parallel Example: User Story 1

```bash
Task: "T017 [P] [US1] Add tests for direct popularity target selection in tests/test_popularity.py"
Task: "T018 [P] [US1] Add tests for playlist-derived proxy selection and proxy labeling in tests/test_popularity.py"
Task: "T019 [P] [US1] Add tests for artist repetition/count weak-proxy fallback and weak-proxy labeling in tests/test_popularity.py"
Task: "T020 [P] [US1] Add tests for top-10% segment threshold and segment counts in tests/test_popularity.py"
```

## Parallel Example: User Story 2

```bash
Task: "T030 [P] [US2] Implement full-valid-dataset filter and exclusion count summary in src/song_popularity/data.py"
Task: "T031 [P] [US2] Implement audio feature comparison summaries for top 10% versus remaining tracks in src/song_popularity/popularity.py"
Task: "T032 [P] [US2] Implement artist/exposure metadata comparison summaries in src/song_popularity/popularity.py"
Task: "T034 [P] [US2] Implement reusable Plotly chart helpers for target distribution, segment comparisons, and ranked drivers in src/song_popularity/plots.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup.
2. Complete Phase 2 foundational helpers.
3. Complete Phase 3 target definition and top-10% segmentation.
4. Stop and validate that the notebook documents the selected target and proxy caveat.

### Incremental Delivery

1. US1 delivers a defensible popularity target and segment.
2. US2 adds evidence-backed driver findings from the full valid dataset.
3. US3 packages the story into README/notebook deliverables with caveats and citations.

### Final Validation

1. Run `pytest tests/`.
2. Execute `notebook.ipynb` end-to-end.
3. Confirm `README.md` is complete and every final claim has evidence.
4. Confirm no oversized raw data is committed.
