# Tasks: 118th Congress Twitter Caucus Analysis

**Input**: Design documents from `/specs/001-twitter-caucus-analysis/`
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: No standalone TDD suite was requested. Validation is implemented through notebook run-all checks, schema checks, and generated-output inspection tasks.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently after shared notebook infrastructure is in place.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches a different file or does not depend on incomplete tasks.
- **[Story]**: Applies only to user story phases.
- Every task names the exact target file or directory.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the requested notebook project shell and minimal runnable documentation.

- [ ] T001 Create project directories `twitter-caucus-118/data/raw/tweets/`, `twitter-caucus-118/data/raw/accounts/`, `twitter-caucus-118/data/raw/service_dates/`, `twitter-caucus-118/data/processed/`, `twitter-caucus-118/data/manual/`, and `twitter-caucus-118/figures/`
- [ ] T002 Create the initial notebook file `twitter-caucus-118/notebook.ipynb` with markdown section headings matching the notebook output contract
- [ ] T003 [P] Create `twitter-caucus-118/data/manual/top10_bill_counts.csv` with the required header row and no member data
- [ ] T004 [P] Create `twitter-caucus-118/README.md` with run instructions, dependency list, manual CSV placement, cache behavior, and output inventory
- [ ] T005 Add notebook-top package/version guidance for Python 3.10+, pandas, requests, plotly, notebook/ipykernel, and optional kaleido in `twitter-caucus-118/notebook.ipynb`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define notebook constants and shared helpers required before any user story analysis can run.

**CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T006 Define analysis windows, required spot-check dates, source URLs, cache paths, processed paths, and figure paths in `twitter-caucus-118/notebook.ipynb`
- [ ] T007 Implement cache-first JSON download helper with parse validation and failure status reporting in `twitter-caucus-118/notebook.ipynb`
- [ ] T008 Implement date-window iterator using inclusive start and exclusive end semantics in `twitter-caucus-118/notebook.ipynb`
- [ ] T009 Implement shared CSV schema assertion helpers for processed outputs in `twitter-caucus-118/notebook.ipynb`
- [ ] T010 Implement shared display helpers for warnings, lookup prompts, and summary tables in `twitter-caucus-118/notebook.ipynb`
- [ ] T011 Add raw-cache size check and repository-inclusion warning logic in `twitter-caucus-118/notebook.ipynb`

**Checkpoint**: Notebook constants and helpers exist; user story implementation can begin.

---

## Phase 3: User Story 1 - Verify Coverage Before Analysis (Priority: P1)

**Goal**: The notebook verifies tweet archive coverage and prints a clear quality summary before any member aggregation.

**Independent Test**: Run only through the verification section of `twitter-caucus-118/notebook.ipynb` from an empty cache and confirm the first substantive output reports expected days, populated days, missing days, spot-check counts, degradation flags, and selected window.

### Implementation for User Story 1

- [ ] T012 [US1] Implement daily archive availability checks for the 118th Congress window in `twitter-caucus-118/notebook.ipynb`
- [ ] T013 [US1] Implement tweet-count spot checks for 2023-03-15, 2023-10-15, 2024-06-15, and 2024-11-15 in `twitter-caucus-118/notebook.ipynb`
- [ ] T014 [US1] Implement degraded-coverage warning when more than 10% of days are missing or any spot-check day has fewer than 1,000 tweets in `twitter-caucus-118/notebook.ipynb`
- [ ] T015 [US1] Implement severe-degradation fallback to the 117th Congress window when fewer than half of 118th Congress days are populated in `twitter-caucus-118/notebook.ipynb`
- [ ] T016 [US1] Render the coverage verification summary before loading member metadata in `twitter-caucus-118/notebook.ipynb`
- [ ] T017 [US1] Validate US1 by running the verification cells and confirming no aggregation outputs precede the coverage summary in `twitter-caucus-118/notebook.ipynb`

**Checkpoint**: Data quality verification is complete and independently reviewable.

---

## Phase 4: User Story 2 - Produce Member-Level Tweet Rankings (Priority: P1)

**Goal**: The notebook collapses account-level tweet records into one row per member with official service-window normalization.

**Independent Test**: Run through member aggregation and inspect `twitter-caucus-118/data/processed/member_tweet_counts.csv` for one row per `bioguide_id`, required columns, summed account counts, party/chamber/state labels, and valid days-in-office normalization.

### Implementation for User Story 2

- [ ] T018 [US2] Download and cache `historical-users-filtered.json` account metadata under `twitter-caucus-118/data/raw/accounts/` in `twitter-caucus-118/notebook.ipynb`
- [ ] T019 [US2] Implement member-account filtering that excludes committee, leadership, party, and other non-member accounts in `twitter-caucus-118/notebook.ipynb`
- [ ] T020 [US2] Implement tweet-to-account joining by screen name and exclude unmatched tweet records from member totals in `twitter-caucus-118/notebook.ipynb`
- [ ] T021 [US2] Implement official service-date lookup fallback keyed by `bioguide_id` under `twitter-caucus-118/data/raw/service_dates/` in `twitter-caucus-118/notebook.ipynb`
- [ ] T022 [US2] Implement service-window overlap and `days_in_office` calculation for the selected analysis window in `twitter-caucus-118/notebook.ipynb`
- [ ] T023 [US2] Aggregate matched tweets by `bioguide_id` with `member_name`, `party`, `chamber`, `state`, `total_tweets`, `tweets_per_day_in_office`, `account_count`, and `days_in_office` in `twitter-caucus-118/notebook.ipynb`
- [ ] T024 [US2] Write and validate `twitter-caucus-118/data/processed/member_tweet_counts.csv` against the processed data contract in `twitter-caucus-118/notebook.ipynb`
- [ ] T025 [US2] Validate US2 by confirming `bioguide_id` uniqueness and required columns in `twitter-caucus-118/data/processed/member_tweet_counts.csv`

**Checkpoint**: Member-level tweet ranking data exists and satisfies the processed data contract.

---

## Phase 5: User Story 3 - Quantify Concentration Visually (Priority: P1)

**Goal**: The notebook computes concentration statistics and writes the required ranked distribution figure.

**Independent Test**: Run through distribution analysis and confirm `twitter-caucus-118/figures/distribution.html` shows all ranked members, party coloring, top-10 annotations, cumulative share from ranks 1 through 100, and the 50% concentration marker.

### Implementation for User Story 3

- [ ] T026 [US3] Compute member ranks, cumulative tweet totals, cumulative share, and top-N threshold for 50% of tweets in `twitter-caucus-118/notebook.ipynb`
- [ ] T027 [US3] Build the Plotly ranked tweet-volume panel with rank on x-axis, tweet count on y-axis, hover labels, and party color-coding in `twitter-caucus-118/notebook.ipynb`
- [ ] T028 [US3] Add top-10 member name annotations to the ranked tweet-volume panel in `twitter-caucus-118/notebook.ipynb`
- [ ] T029 [US3] Build the cumulative-share panel for top N members from N = 1 through 100 with a visible 50% threshold marker in `twitter-caucus-118/notebook.ipynb`
- [ ] T030 [US3] Save the interactive figure to `twitter-caucus-118/figures/distribution.html` from `twitter-caucus-118/notebook.ipynb`
- [ ] T031 [US3] Validate US3 by opening or rendering `twitter-caucus-118/figures/distribution.html` and confirming the chart elements required by the notebook output contract

**Checkpoint**: Concentration headline metric and distribution chart are ready for story use.

---

## Phase 6: User Story 4 - Compare Top Tweeters With Bill Sponsorship (Priority: P2)

**Goal**: The notebook joins the top 10 tweet-ranked members to optional manual bill-sponsorship counts and produces a readable comparison table.

**Independent Test**: Run once without `twitter-caucus-118/data/manual/top10_bill_counts.csv` data and once with sample rows; confirm `twitter-caucus-118/data/processed/top10_with_legislation.csv` is produced both times and preserves all top-10 members.

### Implementation for User Story 4

- [ ] T032 [US4] Select the top 10 members by `total_tweets` from `twitter-caucus-118/data/processed/member_tweet_counts.csv` in `twitter-caucus-118/notebook.ipynb`
- [ ] T033 [US4] Implement optional loading and schema validation for `twitter-caucus-118/data/manual/top10_bill_counts.csv` in `twitter-caucus-118/notebook.ipynb`
- [ ] T034 [US4] Implement missing-manual-file behavior that prints top-10 names, bioguide identifiers, selected Congress window, and Congress.gov lookup method with zero placeholders in `twitter-caucus-118/notebook.ipynb`
- [ ] T034a [US4] Document the Congress.gov manual lookup method for `top10_bill_counts.csv`, including selected Congress, sponsored legislation count, and enacted sponsored-bill count, in `twitter-caucus-118/README.md`
- [ ] T035 [US4] Join top-10 tweet rows to bill counts by `bioguide_id` while preserving unmatched top-10 members in `twitter-caucus-118/notebook.ipynb`
- [ ] T036 [US4] Write and validate `twitter-caucus-118/data/processed/top10_with_legislation.csv` against the processed data contract in `twitter-caucus-118/notebook.ipynb`
- [ ] T037 [US4] Render the summary table with party, tweet count, tweets per day, bills sponsored, and bills enacted in `twitter-caucus-118/notebook.ipynb`

**Checkpoint**: Top-10 tweet and legislation comparison works with or without manual bill data.

---

## Phase 7: User Story 5 - Deliver a Reproducible Story Package (Priority: P2)

**Goal**: The project runs end-to-end from a fresh clone and produces the documented outputs, final writeup, and caveats.

**Independent Test**: Restart the kernel, run all cells in `twitter-caucus-118/notebook.ipynb`, and confirm processed CSVs, figure output, rendered summary table, and under-500-word writeup are regenerated.

### Implementation for User Story 5

- [ ] T038 [US5] Add final markdown findings writeup under 500 words with concentration headline, top 10 by name, tweets-versus-bills observation, and data quality caveats in `twitter-caucus-118/notebook.ipynb`
- [ ] T039 [US5] Add required methodological notes about published tweets only, no engagement metrics, Twitter becoming X in July 2023, and bill sponsorship limitations in `twitter-caucus-118/notebook.ipynb`
- [ ] T040 [US5] Update `twitter-caucus-118/README.md` with quickstart steps, expected outputs, optional manual bill-count workflow, cache regeneration, and raw-data size guidance
- [ ] T041 [US5] Validate fresh-clone behavior by clearing generated outputs and raw cache files while preserving notebook and manual template, then rerunning `twitter-caucus-118/notebook.ipynb`
- [ ] T042 [US5] Validate warm-cache behavior by rerunning `twitter-caucus-118/notebook.ipynb` and confirming cached files under `twitter-caucus-118/data/raw/` are reused
- [ ] T043 [US5] Trace every quantitative claim in the final writeup to `twitter-caucus-118/data/processed/member_tweet_counts.csv`, `twitter-caucus-118/data/processed/top10_with_legislation.csv`, or a displayed notebook calculation

**Checkpoint**: The data story package is reproducible and ready for review.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Tighten usability, documentation, and final validation across all stories.

- [ ] T044 Review notebook markdown for narrative order and section openings in `twitter-caucus-118/notebook.ipynb`
- [ ] T045 Review inline comments so non-obvious choices are justified without over-commenting in `twitter-caucus-118/notebook.ipynb`
- [ ] T046 Verify generated CSV schemas match `specs/001-twitter-caucus-analysis/contracts/processed-data-contract.md`
- [ ] T047 Verify notebook visible outputs match `specs/001-twitter-caucus-analysis/contracts/notebook-output-contract.md`
- [ ] T048 Run the quickstart validation steps from `specs/001-twitter-caucus-analysis/quickstart.md`
- [ ] T049 Inspect raw cache size under `twitter-caucus-118/data/raw/` and update `twitter-caucus-118/README.md` if external hosting or non-commit guidance applies
- [ ] T050 Confirm no out-of-scope engagement, sentiment, topic, or cross-platform analysis was added to `twitter-caucus-118/notebook.ipynb`
- [ ] T051 Verify service-date output uses the official `unitedstates/congress-legislators` lookup where available or visibly caveats selected-window boundary fallback in `twitter-caucus-118/notebook.ipynb`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories.
- **US1 Verification (Phase 3)**: Depends on Foundational; must complete before US2-US5 because it selects the analysis window.
- **US2 Member Rankings (Phase 4)**: Depends on US1 because it uses the selected window and verified cache.
- **US3 Distribution (Phase 5)**: Depends on US2 because it uses `member_tweet_counts.csv`.
- **US4 Bill Comparison (Phase 6)**: Depends on US2 because it uses the top 10 by tweet count; can run after US2 and before or after US3.
- **US5 Reproducible Package (Phase 7)**: Depends on US1-US4 because it validates all outputs and writes final findings.
- **Polish**: Depends on all desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Independent after Foundational; MVP verification slice.
- **US2 (P1)**: Requires US1 selected window and cache status.
- **US3 (P1)**: Requires US2 member-level output.
- **US4 (P2)**: Requires US2 top-10 ranking.
- **US5 (P2)**: Requires US1-US4 outputs.

### Within Each User Story

- Implement notebook logic before validation tasks in the same story.
- Generate processed files before schema validation tasks.
- Generate distribution metrics before figure rendering.
- Render top-10 table before final writeup.

### Parallel Opportunities

- T003 and T004 can run in parallel after T001 because they touch different files.
- Documentation updates in T040 can be drafted while US3 or US4 notebook logic is being implemented, then reconciled after outputs exist.
- US3 and US4 can proceed in parallel after US2 if two developers coordinate edits to `twitter-caucus-118/notebook.ipynb`.
- Final contract checks T046 and T047 can run in parallel after notebook outputs exist.

---

## Parallel Example: After Setup

```text
Task: "Create twitter-caucus-118/data/manual/top10_bill_counts.csv with the required header row"
Task: "Create twitter-caucus-118/README.md with run instructions and output inventory"
```

## Parallel Example: After Member Rankings

```text
Task: "Implement distribution figure generation in twitter-caucus-118/notebook.ipynb"
Task: "Implement optional bill-count join in twitter-caucus-118/notebook.ipynb"
```

---

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Complete US1 so the notebook proves archive coverage before analysis.
3. Stop and validate that the first substantive notebook output is the coverage summary.

### Incremental Delivery

1. Add US2 to produce `member_tweet_counts.csv`.
2. Add US3 to produce concentration metrics and `figures/distribution.html`.
3. Add US4 to produce `top10_with_legislation.csv` and the rendered top-10 table.
4. Add US5 to complete README, caveats, final writeup, and end-to-end validation.

### Single-Developer Sequence

Follow tasks in numeric order. Most implementation tasks touch the same notebook,
so sequential execution is the safest default.

## Notes

- `[P]` tasks are limited because the main deliverable is a single notebook.
- Keep raw cache files out of commits if they exceed the documented size limit.
- Do not add engagement, sentiment, topic modeling, or cross-platform analysis.
- Each story checkpoint should be validated before moving to the next story.
