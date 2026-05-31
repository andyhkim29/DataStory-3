# Implementation Plan: 118th Congress Twitter Caucus Analysis

**Branch**: `001-twitter-caucus-analysis` | **Date**: 2026-05-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-twitter-caucus-analysis/spec.md`

## Summary

Build a reproducible notebook project under `twitter-caucus-118/` that downloads
and caches Congressional tweet archive data, verifies coverage before analysis,
maps account-level tweets to member-level rows, computes ranked concentration
metrics, joins optional manual bill-sponsorship counts for the top 10, and writes
processed CSVs, figures, a rendered table, and a short story-ready caveat-aware
writeup. The implementation uses a single Python notebook plus small documented
CSV contracts rather than a service or application.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: pandas, requests, plotly, notebook/ipykernel; optional kaleido for static image export  
**Storage**: Local filesystem cache and generated CSV/HTML/figure artifacts  
**Testing**: Restart-kernel/run-all notebook execution; output schema checks in notebook; optional nbconvert execution for validation  
**Target Platform**: Local development environment capable of running Jupyter notebooks  
**Project Type**: Reproducible data-story notebook project  
**Performance Goals**: Complete a warm-cache rerun without refetching daily JSON files; handle roughly 730 daily tweet files for the primary window  
**Constraints**: Verification output MUST appear before aggregation; raw downloads should not be committed if cache exceeds 10 MB; manual bill counts are the only required user-provided input  
**Scale/Scope**: 118th Congress window from 2023-01-03 through 2025-01-03, with 117th Congress fallback from 2021-01-03 through 2023-01-03 only if severe 118th coverage degradation occurs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Verification before analysis: PASS. The first notebook section verifies daily
  file coverage and spot-check tweet counts, warning on degraded coverage and
  switching to the 117th Congress window when fewer than half of 118th days are
  populated.
- Reproducible data lineage: PASS. Raw cache, account metadata, optional manual
  CSV, processed CSVs, figure outputs, and writeup claims are all planned as
  named files or notebook outputs.
- Entity traceability: PASS. Member-level aggregation uses `bioguide_id` as the
  person key, excludes non-member accounts, records account counts, and uses an
  official service-date lookup when account metadata lacks reliable service
  dates.
- Story outputs and caveats: PASS. Required outputs include processed tables,
  distribution figure, top-10 table, and an under-500-word caveat-aware writeup.
- Scope control: PASS. The plan excludes engagement, sentiment, topic,
  cross-platform, and cross-Congress comparison analyses except the required
  data-quality fallback.

## Project Structure

### Documentation (this feature)

```text
specs/001-twitter-caucus-analysis/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── processed-data-contract.md
│   └── notebook-output-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
twitter-caucus-118/
├── notebook.ipynb
├── data/
│   ├── raw/
│   │   ├── tweets/
│   │   ├── accounts/
│   │   └── service_dates/
│   ├── processed/
│   │   ├── member_tweet_counts.csv
│   │   └── top10_with_legislation.csv
│   └── manual/
│       └── top10_bill_counts.csv
├── figures/
│   └── distribution.html
└── README.md
```

**Structure Decision**: Use a single self-contained notebook project in
`twitter-caucus-118/`, matching the requested deliverable structure. Supporting
helper functions may live inside the notebook to keep the project runnable from a
fresh clone without a package install step beyond notebook dependencies.

## Phase 0: Research Summary

See [research.md](./research.md). Key decisions:

- Use local cache-first downloads for daily tweet JSON and metadata.
- Use account metadata for member mapping and non-member exclusion, with
  `unitedstates/congress-legislators` as the official service-date lookup
  fallback for service windows.
- Use Plotly for the interactive distribution figure and write HTML as the
  guaranteed figure artifact.
- Treat manual bill counts as optional until supplied, with placeholder zeros and
  printed Congress.gov lookup prompts tied to the selected analysis Congress.

## Phase 1: Design Summary

See [data-model.md](./data-model.md) and [contracts/](./contracts/).

- Primary entities are tweet days, Twitter accounts, official service-date
  records, members, coverage summaries, manual bill counts, and distribution
  findings.
- Public project contracts are the processed CSV schemas and notebook output
  obligations, not web or API endpoints.
- Quickstart validation is notebook-oriented: install dependencies, optionally
  provide manual bill counts, restart/run all, and inspect generated outputs.

## Post-Design Constitution Check

- Verification before analysis: PASS. The notebook output contract requires the
  coverage block before any member-level aggregation.
- Reproducible data lineage: PASS. Processed data contracts define stable
  columns, cache paths, and traceability from final writeup claims to generated
  outputs.
- Entity traceability: PASS. Data model defines `bioguide_id` uniqueness and
  service-date fallback behavior.
- Story outputs and caveats: PASS. Notebook output contract lists chart, table,
  and writeup caveat requirements.
- Scope control: PASS. Contracts and quickstart contain no engagement,
  sentiment, topic, or cross-platform deliverables.

## Complexity Tracking

No constitution violations.
