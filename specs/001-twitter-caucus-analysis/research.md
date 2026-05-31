# Research: 118th Congress Twitter Caucus Analysis

## Daily Tweet Acquisition and Caching

**Decision**: Download daily JSON files from the public congresstweets archive
only when a valid local cache file is absent. Store daily files under
`twitter-caucus-118/data/raw/tweets/YYYY-MM-DD.json`.

**Rationale**: The project expects roughly 730 daily files for the primary
window. Cache-first behavior makes reruns practical and satisfies reproducibility
without requiring every raw file to be committed.

**Alternatives considered**:
- Always refetch every file: simpler code but slow and fragile.
- Commit all raw files: reproducible but conflicts with the size constraint when
  raw data exceeds 10 MB.

## Coverage Verification

**Decision**: Treat a day as populated only when its JSON file exists locally or
downloads successfully and parses as an array. Compute expected days over the
selected inclusive start and exclusive end window. For 118th Congress coverage,
spot-check 2023-03-15, 2023-10-15, 2024-06-15, and 2024-11-15.

**Rationale**: This directly implements the acceptance criteria and makes archive
quality visible before any finding is calculated.

**Alternatives considered**:
- Verify only spot-check dates: misses broad missing-file patterns.
- Verify only total file count: misses low-volume dates that can indicate
  degraded coverage.

## Member Mapping and Account Filtering

**Decision**: Use `historical-users-filtered.json` as the authoritative mapping
from Twitter screen names/accounts to member identities and account type. Keep
only member-of-Congress accounts, exclude committee, leadership, party, and other
non-member accounts, and aggregate by `bioguide_id`.

**Rationale**: The story question is member-level, and `bioguide_id` is the
stable identity key needed to collapse multiple accounts per person.

**Alternatives considered**:
- Aggregate by screen name: incorrectly splits members with multiple accounts or
  changed handles.
- Include institutional accounts: changes the unit of analysis away from
  individual members.

## Service-Date Normalization

**Decision**: Use account metadata service timing when reliable. If missing or
unreliable, use an official service-date lookup source keyed by `bioguide_id`.
Only if both are unavailable should the notebook use the selected Congress
window boundaries and document that limitation.

**Rationale**: The clarified requirement makes tweets per day in office an
official service-overlap measure rather than an account metadata artifact.

**Alternatives considered**:
- Default all missing dates to the full Congress window: easier but can
  understate partial-term tweet rates.
- Drop members with missing service dates: loses relevant members and can distort
  the ranking.

## Visualization Format

**Decision**: Build the distribution chart with Plotly and save
`figures/distribution.html` as the guaranteed artifact. Static export may also be
written when the optional image engine is available.

**Rationale**: Plotly supports hover labels for large ranked distributions and
works well inside notebooks. HTML avoids requiring a browser-image export stack
for the acceptance criteria.

**Alternatives considered**:
- Matplotlib-only figure: simpler static export but weaker hover inspection.
- Static image only: less useful for reviewing top members and party labels.

## Manual Bill Counts

**Decision**: Treat `data/manual/top10_bill_counts.csv` as optional. If absent,
the notebook writes the top 10 with `bills_sponsored = 0` and
`bills_enacted = 0`, and prints the names and bioguide identifiers for manual
lookup.

**Rationale**: The top 10 are not known until the tweet aggregation runs, so the
notebook must be useful before manual lookup is complete.

**Alternatives considered**:
- Fail when the manual file is missing: blocks the main analysis.
- Automatically scrape bill counts: outside scope and less transparent than the
  user-specified manual source.

## Dependency Pinning

**Decision**: Put version guidance in a notebook-top markdown or comment block,
and keep dependencies minimal: Python 3.10+, pandas, requests, plotly, notebook
or JupyterLab, and optional kaleido.

**Rationale**: The user requested package-version guidance in the notebook, but
the deliverable does not require a full package or application scaffold.

**Alternatives considered**:
- Add a package manager project: more machinery than a notebook data story
  needs.
- Leave versions undocumented: weakens reproducibility.
