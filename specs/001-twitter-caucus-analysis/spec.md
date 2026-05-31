# Feature Specification: 118th Congress Twitter Caucus Analysis

**Feature Branch**: `001-twitter-caucus-analysis`  
**Created**: 2026-05-31  
**Status**: Draft  
**Input**: User description: "118th Congress Twitter Caucus Analysis: reproducible data analysis quantifying concentration of Twitter activity across members of the 118th US Congress, with data quality verification, member-level aggregation, top 10 bill sponsorship comparison, charts, processed data, and a short story-ready writeup."

## Clarifications

### Session 2026-05-31

- Q: How should tweets-per-day-in-office handle missing or unreliable service dates in the Twitter account metadata? -> A: Add an official service-date lookup source for missing or unreliable member start/end dates.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify Coverage Before Analysis (Priority: P1)

A data storyteller needs the analysis to check whether the Congressional tweet archive is complete enough for the 118th Congress window before calculating any findings, so that the final story does not overstate results from degraded data.

**Why this priority**: All downstream findings depend on archive coverage. The project is not trustworthy unless data quality is summarized first and severe degradation triggers the fallback window.

**Independent Test**: Run the analysis from a fresh project state and confirm that the first substantive output is a coverage summary covering daily file availability, four named spot-check dates, degradation warnings, and the selected analysis window.

**Acceptance Scenarios**:

1. **Given** no prior downloaded tweet cache, **When** the analysis is run, **Then** it checks file availability for 2023-01-03 through 2025-01-03 before performing member aggregation.
2. **Given** any spot-check date has fewer than 1,000 tweets or more than 10% of expected days are missing, **When** verification completes, **Then** the analysis prints a clear warning and records that caveat for the final writeup.
3. **Given** fewer than half of expected 118th Congress days are populated, **When** verification completes, **Then** the analysis switches the primary window to 2021-01-03 through 2023-01-03 and states that fallback explicitly.

---

### User Story 2 - Produce Member-Level Tweet Rankings (Priority: P1)

A data storyteller needs one cleaned member-level table that collapses all official member Twitter accounts into a single row per member, so that the concentration distribution reflects people in Congress rather than individual accounts.

**Why this priority**: The central finding is about members of Congress. Account-level rows would split members with multiple accounts and distort the ranking.

**Independent Test**: Run the analysis and inspect the processed member table to confirm one row per member identity, summed tweet totals across all matching member accounts, party and chamber labels, and per-day normalization.

**Acceptance Scenarios**:

1. **Given** the account metadata contains multiple member accounts for one bioguide identifier, **When** tweet counts are aggregated, **Then** those accounts are summed into one member-level row.
2. **Given** the account metadata includes committee, leadership, or party accounts, **When** member filtering is applied, **Then** those non-member accounts are excluded from the member-level output.
3. **Given** a member served only part of the selected Congress window, **When** per-day values are calculated, **Then** the denominator is that member's days in office during the selected window.

---

### User Story 3 - Quantify Concentration Visually (Priority: P1)

A video producer needs a chart that shows both the full ranked tweet distribution and the cumulative share of tweets produced by the top-ranked members, so the story can support a concise headline such as "X% of members produce 50% of tweets."

**Why this priority**: The shape of the distribution is the central story. The visualization must make both the ranked distribution and the headline concentration number traceable.

**Independent Test**: Run the analysis and confirm the figure file exists, includes party color-coding, top-10 annotations by name, and a cumulative-share panel from ranks 1 through 100.

**Acceptance Scenarios**:

1. **Given** member-level tweet counts exist, **When** the distribution chart is generated, **Then** all ranked members appear on the rank axis with tweet volume on the value axis and party color applied.
2. **Given** the top 10 members are identified, **When** the chart is rendered, **Then** those 10 members are annotated by name.
3. **Given** cumulative shares are computed, **When** the chart is rendered, **Then** it clearly indicates the member share needed to account for 50% of tweets.

---

### User Story 4 - Compare Top Tweeters With Bill Sponsorship (Priority: P2)

A data storyteller needs the top 10 tweeters joined to manually supplied bill-sponsorship counts for the selected analysis Congress, so the final story can assess whether the loudest tweeters are also the most legislatively active by that measure.

**Why this priority**: This comparison supplements the main concentration story and supports a more nuanced narrative for the video.

**Independent Test**: Run the analysis with and without the manual bill-count file and confirm that the top-10 table is produced in both cases, using provided counts when present and visible placeholder zeros when absent.

**Acceptance Scenarios**:

1. **Given** the manual bill-count file is absent, **When** the top 10 are identified, **Then** the analysis prints the top 10 names, bioguide identifiers, selected Congress window, and Congress.gov lookup method with placeholder zeros for lookup.
2. **Given** the manual bill-count file is present, **When** the join is performed, **Then** each top-10 member includes bills sponsored and bills enacted counts.
3. **Given** a manual bill-count row does not match a top-10 bioguide identifier, **When** the join completes, **Then** the unmatched member remains in the output with clear missing or placeholder bill values.

---

### User Story 5 - Deliver a Reproducible Story Package (Priority: P2)

A collaborator needs a project directory that can be rerun end-to-end after cloning, producing processed data, figures, a top-10 table, and a concise final writeup without manual setup beyond the bill-count CSV.

**Why this priority**: The output is intended for a 3-4 minute data story and must be auditable by another person.

**Independent Test**: Restart the notebook kernel and run all cells from a fresh clone after optionally adding the manual CSV; confirm that the same processed files, figure outputs, and final markdown summary are generated.

**Acceptance Scenarios**:

1. **Given** an empty local cache, **When** the notebook is run, **Then** it downloads and caches source data locally so future runs do not refetch unchanged daily files.
2. **Given** the notebook completes, **When** the project outputs are inspected, **Then** the required processed CSVs, distribution figure, rendered top-10 summary table, and under-500-word markdown writeup are present.
3. **Given** numbers appear in the final writeup, **When** a reviewer traces them backward, **Then** each number is derived from a specific processed file or notebook cell output.

### Edge Cases

- The 118th Congress tweet archive may have missing days, failed downloads, malformed JSON, or low-volume spot-check days.
- The fallback 117th Congress archive may also be degraded; the analysis still reports coverage and caveats for the chosen window.
- A tweet screen name may not match a member account in the historical metadata and must be excluded from member-level totals.
- A member may have multiple accounts, changed account names, partial service dates, or missing official service-date fields.
- Independents and caucusing members require party labels that do not assume a strict two-party split.
- Manual bill-count data may be missing, incomplete, stale, or contain identifiers that do not match the top-10 output.
- Downloaded raw data may exceed a size suitable for repository inclusion, requiring outputs to rely on cache regeneration or external hosting guidance.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The analysis MUST create a self-contained project named `twitter-caucus-118` with a notebook, data folders for raw, processed, and manual inputs, a figures folder, and a README.
- **FR-002**: The notebook MUST begin with package/version guidance and MUST be organized as a narrative with sections for dataset verification, loading and account filtering, member aggregation, distribution analysis, top-10 bill counts, and findings/caveats.
- **FR-003**: Before member aggregation, the notebook MUST verify data coverage for the initial 118th Congress window from 2023-01-03 through 2025-01-03.
- **FR-004**: Coverage verification MUST report the share and count of expected daily files found or retrievable for the selected window.
- **FR-005**: Coverage verification MUST record total tweet counts for 2023-03-15, 2023-10-15, 2024-06-15, and 2024-11-15 when evaluating the 118th Congress window.
- **FR-006**: The notebook MUST print a clear degraded-coverage warning if more than 10% of expected days are missing or if any required spot-check day has fewer than 1,000 tweets.
- **FR-007**: If fewer than half of expected 118th Congress days are populated, the notebook MUST rerun the analysis on 2021-01-03 through 2023-01-03 and make that the primary analysis window.
- **FR-008**: The notebook MUST cache downloaded daily tweet data and account metadata locally so repeat runs reuse existing valid files.
- **FR-009**: The analysis MUST load account metadata and use it to identify member-of-Congress accounts only, excluding committee, leadership, party, and other non-member accounts.
- **FR-010**: The analysis MUST define "member-level" as collapsing multiple Twitter accounts per member by summing tweets across all accounts with the same bioguide identifier.
- **FR-011**: The member-level output MUST include bioguide identifier, member name, party, chamber, state, total tweets, tweets per day in office, account count, and days in office.
- **FR-012**: The analysis MUST normalize partial-term members by calculating tweets per day in office from each member's service overlap with the selected Congress window, using the `unitedstates/congress-legislators` service-date data as the official lookup source when account metadata lacks reliable start or end dates, and explicitly caveating any fallback to selected-window boundaries.
- **FR-013**: The analysis MUST produce a ranked distribution of member tweet counts and identify the top 10 most prolific tweeters.
- **FR-014**: The analysis MUST read bill-sponsorship values from `data/manual/top10_bill_counts.csv` when present, using bioguide identifier as the primary join key.
- **FR-015**: If the manual bill-count file is absent, the notebook MUST print the identified top 10 names and identifiers with placeholder zeros for bills sponsored and bills enacted.
- **FR-015a**: The notebook or README MUST document the manual bill-count lookup method, including Congress.gov as the source, the selected Congress filter, the Sponsored Legislation tab/count, and the enacted sponsored-bill filter/count.
- **FR-016**: The notebook MUST write `data/processed/member_tweet_counts.csv` with one row per member in the chosen analysis window.
- **FR-017**: The notebook MUST write `data/processed/top10_with_legislation.csv` with the top 10 tweet-ranked members and their bill-count fields.
- **FR-018**: The notebook MUST generate a distribution figure in `figures/distribution.*` with a ranked tweet-volume panel colored by party and annotated top-10 names.
- **FR-019**: The distribution figure MUST include a cumulative-share panel showing the percent of total tweets accounted for by top N members for N from 1 through 100.
- **FR-020**: The notebook MUST compute and display the headline concentration number: the percentage of members needed to account for 50% of member tweets.
- **FR-021**: The notebook MUST render a summary table containing the top 10 members, party, tweet count, tweets per day, bills sponsored, and bills enacted.
- **FR-022**: The final notebook writeup MUST be under 500 words and include the concentration headline, the top 10 by name, the tweets-versus-bills observation, and the data quality caveats required by FR-023 through FR-026.
- **FR-023**: The notebook MUST explicitly note that the tweet dataset captures published tweets only and does not include deleted tweets.
- **FR-024**: The notebook MUST explicitly note that the dataset does not include engagement metrics and that the analysis measures volume, not engagement.
- **FR-025**: The notebook MUST explicitly note that Twitter became X in July 2023 as contextual information, without analyzing that platform change.
- **FR-026**: The notebook MUST explicitly note that bill sponsorship is only one measure of legislative activity and does not capture co-sponsorships, committee work, floor speeches, or vote attendance.
- **FR-027**: The README MUST explain how to run the notebook from a fresh clone, where to place the optional manual bill-count CSV, what outputs are generated, and how raw-data caching works.
- **FR-028**: If cached or downloaded tweet data exceeds a reasonable repository inclusion size, the project MUST avoid requiring those raw files to be committed and MUST document regeneration or external-hosting expectations.

### Key Entities *(include if feature involves data)*

- **Tweet Day**: A daily archive file for one calendar date containing tweet records with identifiers, account names, timestamps, text, source, and links.
- **Twitter Account**: A historical account record with screen names, account type, member identity attributes, party, chamber, state, bioguide identifier, and service timing where available.
- **Official Service-Date Lookup**: A supplemental source used only when account metadata lacks reliable member start or end dates, preserving official service overlap for tweets-per-day calculations.
- **Member of Congress**: The person-level unit of analysis, identified by bioguide identifier and enriched with member name, party, chamber, state, service dates, account count, and tweet totals.
- **Coverage Verification Summary**: The pre-analysis record of expected days, populated days, missing days, spot-check tweet counts, degradation status, and selected analysis window.
- **Manual Bill Count**: A user-provided top-10 supplemental record keyed by bioguide identifier, containing member name, bills sponsored, and bills enacted for the selected analysis Congress.
- **Distribution Finding**: The ranked member tweet distribution, cumulative share by rank, top-10 list, and 50%-share concentration statistic used in the final writeup.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reviewer can run the notebook end-to-end from a fresh clone, after optionally providing the manual bill-count CSV, and obtain all required processed files, figures, and notebook-rendered outputs.
- **SC-002**: The first analysis result visible in the notebook is a data quality summary that includes daily coverage and the four required 118th Congress spot-check dates.
- **SC-003**: The processed member tweet count file contains no more than one row per bioguide identifier and includes all required columns.
- **SC-004**: The distribution chart displays all ranked members, party coloring, top-10 name annotations, cumulative share for ranks 1 through 100, and the 50%-share headline statistic.
- **SC-005**: The final writeup is under 500 words and every quantitative claim in it can be traced to a processed file or displayed notebook calculation.
- **SC-006**: Running the notebook a second time uses the local cache for already downloaded tweet and metadata files, reducing unnecessary refetching while preserving reproducible outputs.
- **SC-007**: If 118th Congress coverage is severely degraded, the output clearly uses the 117th Congress fallback window and labels all findings with that selected window.

## Assumptions

- The primary audience is a data-story collaborator or video producer who needs transparent, reproducible evidence rather than an operational application.
- The manual bill-count CSV is supplied by the user only after the top 10 are known; until then, placeholder bill values are acceptable and must be visible.
- The account metadata is the authoritative source for mapping Twitter accounts to member identities and for excluding non-member accounts.
- If service dates are incomplete or unreliable in account metadata, the analysis will use an official service-date lookup source before falling back to selected Congress window boundaries as a documented limitation.
- The project should avoid committing large raw downloaded archives when cache regeneration from public URLs is sufficient.
- Cross-platform, sentiment, topic, and engagement analyses are outside scope unless data quality requires the explicitly specified fallback Congress window.
