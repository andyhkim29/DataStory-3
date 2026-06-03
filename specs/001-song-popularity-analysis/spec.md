# Feature Specification: Song Popularity Analysis

**Feature Branch**: `002-song-popularity-analysis`  
**Created**: 2026-06-03  
**Status**: Draft  
**Input**: User description: "I want to analyze this data set now: https://www.kaggle.com/datasets/krishsharma0413/2-million-songs-from-mpd-with-audio-features. The question is what makes songs popular?"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define And Measure Popularity (Priority: P1)

A data analyst wants a defensible definition of song popularity for the Kaggle dataset so that all later analysis answers the same question.

**Why this priority**: The dataset is based on playlist and Spotify audio-feature data, and "popular" must be defined before any comparisons or modeling can be trusted.

**Independent Test**: Can be fully tested by reviewing the dataset fields, selecting an explicit popularity target, and producing a short data dictionary entry that explains how the target is calculated.

**Acceptance Scenarios**:

1. **Given** the dataset is available, **When** the analyst inspects its fields, **Then** the analysis identifies the strongest available popularity proxy and records why it was chosen.
2. **Given** no direct popularity score is present, **When** the analyst prepares the target, **Then** the analysis uses playlist prominence or frequency signals where available and labels the output as a proxy rather than direct popularity.
3. **Given** multiple plausible popularity signals exist, **When** the analyst selects the target, **Then** the analysis documents each candidate and explains the final choice.

---

### User Story 2 - Identify Popularity Drivers (Priority: P2)

A reader wants to understand which song attributes are most associated with popularity, including audio features and metadata patterns.

**Why this priority**: The central question is explanatory: what makes songs popular, not just which songs are popular.

**Independent Test**: Can be tested by producing ranked findings that compare popular and less-popular songs across audio features, duration, artist patterns, and other available metadata.

**Acceptance Scenarios**:

1. **Given** a prepared dataset with a popularity target, **When** the analyst compares feature distributions, **Then** the output shows which attributes differ most between popular and less-popular songs.
2. **Given** numeric audio features are present, **When** the analyst evaluates associations, **Then** the output reports direction and strength for each major feature.
3. **Given** metadata such as artist, album, and track identifiers is present, **When** the analyst analyzes non-audio factors, **Then** the output distinguishes artist/playlist exposure effects from track-level audio effects where possible.

---

### User Story 3 - Communicate Actionable Findings (Priority: P3)

A project reviewer wants a clear story, charts, and caveats explaining what the data suggests about popular songs.

**Why this priority**: The analysis is only useful if the final story can be read and evaluated without inspecting the raw dataset.

**Independent Test**: Can be tested by reading the final narrative and verifying that each major claim is supported by a chart, statistic, or model result.

**Acceptance Scenarios**:

1. **Given** completed analysis results, **When** the reader opens the final report, **Then** they can identify the top drivers of popularity within the first summary section.
2. **Given** a stated driver such as danceability, energy, or duration, **When** the reader checks the supporting evidence, **Then** the report includes a clear visualization or measured relationship.
3. **Given** the data has limitations, **When** the reader reviews the conclusion, **Then** the report explains what cannot be inferred from the dataset.

### Edge Cases

- The dataset may not include a direct popularity score; the analysis must avoid presenting playlist-derived proxies as universal popularity.
- Playlist frequency may favor older songs, genre-specific playlist behavior, or songs from highly represented artists.
- Duplicate track names, remasters, covers, and artist collaborations may distort song-level aggregation.
- Missing or invalid audio-feature values must be handled before comparisons are made.
- Extremely long tracks, speech-heavy recordings, live recordings, or instrumental pieces may behave differently from mainstream songs.
- The dataset may be too large for interactive workflows unless sampling, aggregation, or staged processing is used.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The analysis MUST ingest the Kaggle dataset and produce a field inventory covering song metadata, artist metadata, album metadata, playlist-related fields when present, and Spotify audio features.
- **FR-002**: The analysis MUST define a popularity target before modeling or comparison begins.
- **FR-003**: If a direct popularity score is unavailable, the analysis MUST use the best available playlist-derived proxy and clearly label it as a proxy.
- **FR-004**: The analysis MUST clean or exclude records with missing, duplicate, or invalid values in fields required for the popularity target and core audio-feature comparisons.
- **FR-005**: The analysis MUST summarize the dataset size, number of unique tracks, number of unique artists, missingness, duplicate patterns, and feature ranges.
- **FR-006**: The analysis MUST compare popular and less-popular songs across core audio features including danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration, key, mode, and time signature when those fields are available.
- **FR-007**: The analysis MUST evaluate whether metadata factors such as artist repetition, album repetition, and playlist exposure explain popularity separately from audio features where the data supports that distinction.
- **FR-008**: The analysis MUST rank the strongest popularity drivers using interpretable evidence, such as grouped comparisons, association measures, or model-based feature importance.
- **FR-009**: The analysis MUST include visual outputs that support the main findings, including distributions, comparisons between popularity groups, and at least one ranked driver summary.
- **FR-010**: The final report MUST state limitations, including that the data source is based on playlist inclusion and Spotify API-derived features, not listener intent or complete streaming behavior.
- **FR-011**: The final report MUST answer the question "what makes songs popular?" in plain language with evidence-backed conclusions and caveats.
- **FR-012**: The project README MUST include project name, authors, GitHub usernames, overview, main question, approach, data used, tools used, key findings, data links, running instructions, contributing notes, known issues, acknowledgements, and citations.
- **FR-013**: The project code MUST include documented notebook or script steps for downloading or importing the dataset so results can be reproduced from a fresh checkout.
- **FR-014**: If analyzed data files total less than 10 MB, they SHOULD be included in the project folder when licensing allows; if larger, the README and notebook/code MUST point to an accessible external data location.
- **FR-015**: The project MUST NOT require a YouTube or video deliverable unless that requirement is explicitly restored later.

### Key Entities *(include if feature involves data)*

- **Track**: A unique song recording represented by track URI or equivalent identifier, with name, artist, album, duration, and audio-feature attributes.
- **Artist**: The performer or creator associated with a track, represented by artist name and artist URI when available.
- **Album**: The release associated with a track, represented by album name and album URI when available.
- **Audio Feature Profile**: Numeric and categorical song attributes such as danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, key, mode, and time signature.
- **Popularity Target**: The selected measurable outcome used to separate or rank popular songs, preferably a direct popularity field if present, otherwise a documented playlist-derived proxy.
- **Popularity Segment**: A grouped label such as high, medium, or low popularity used for comparisons and visual summaries.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The completed analysis identifies and documents one primary popularity target before presenting driver findings.
- **SC-002**: The completed analysis reports dataset coverage, missingness, and duplicate handling for all fields used in the final conclusions.
- **SC-003**: The final report includes at least five evidence-backed findings about attributes associated with song popularity.
- **SC-004**: Every major conclusion in the final report is supported by a statistic, chart, or ranked comparison.
- **SC-005**: A reader can distinguish direct popularity evidence from proxy-based popularity evidence throughout the report.
- **SC-006**: The final report includes at least three clear limitations or alternative explanations for the observed popularity patterns.
- **SC-007**: The final output can be reviewed by a non-technical reader and still communicates the answer to "what makes songs popular?" without requiring raw data inspection.
- **SC-008**: A new reviewer can use README.md to locate the data, install or prepare required tools, run the code, and understand the main findings.

## Assumptions

- The Kaggle dataset is the "2M unique spotify songs with audio features" dataset by Krish Sharma, combining Million Playlist Dataset information with Spotify API audio features.
- The dataset contains approximately 2.26 million unique songs and fields such as track and artist identifiers, album metadata, duration, danceability, energy, key, loudness, speechiness, mode, acousticness, instrumentalness, liveness, valence, tempo, and time signature.
- The dataset may not include a native Spotify popularity score; playlist presence, playlist frequency, or related MPD-derived signals will be used as the popularity proxy if a direct score is absent.
- The first version focuses on explanatory analysis and storytelling, not production recommendation systems or causal claims.
- The analysis will avoid claiming that audio features alone cause popularity because playlist exposure, artist recognition, genre, release timing, and platform behavior may also affect popularity.

## Data Story Requirements *(mandatory for analysis features)*

- **Dataset Source**: Kaggle dataset "2M unique spotify songs with audio features" by Krish Sharma, accessed from the user-provided Kaggle URL.
- **Target Metric**: A direct popularity field if present; otherwise the strongest playlist-derived proxy available in the dataset, clearly labeled as a proxy.
- **Evidence Standard**: Each final claim must be supported by a statistic, chart, ranked comparison, or interpretable model result generated from the analyzed data.
- **Required Caveats**: The final story must explain that playlist-derived popularity may reflect playlist inclusion behavior, artist exposure, genre mix, and dataset construction rather than universal listener preference or causal drivers.
- **README Requirements**: README.md must include project metadata, overview, key findings, data links, running instructions, contributing or next-step notes, known issues, acknowledgements, and citations.
- **Video Requirement**: No YouTube or video link is required for this project unless explicitly restored later.
- **Data Access Rule**: Data under 10 MB should be committed when licensing allows; larger data must be externally hosted and downloaded or imported by the notebook/code.
