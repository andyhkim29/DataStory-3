# Research: Song Popularity Analysis

## Decision: Use A Notebook-First Python Workflow

**Rationale**: The deliverable is a data story with reproducible analysis, charts,
and plain-language conclusions. A Jupyter notebook is the most direct format for
combining field inspection, data cleaning, exploratory analysis, model summaries,
figures, and narrative.

**Alternatives considered**: A full application was rejected because there is no
user-facing interactive product requirement. A scripts-only workflow was rejected
because the project needs readable narrative and evidence in one place.

## Decision: Use pandas With pyarrow/Parquet For Large-File Handling

**Rationale**: The 900k Spotify dataset ships as large CSV/JSON files. The CSV is
large enough to benefit from typed reads, column selection, and optional Parquet
conversion, but still practical for local analysis with efficient file handling.
pandas keeps the workflow accessible for review, while pyarrow improves
CSV/Parquet I/O.

**Alternatives considered**: DuckDB was considered for scalable SQL-style local
analysis, but it adds another query layer that may not be needed. Polars was
considered for performance, but pandas is more familiar and sufficient unless
the raw file proves too slow.

## Decision: Define Popularity From Available Dataset Fields

**Rationale**: The `devdope/900k-spotify` CSV includes a direct `Popularity`
field. The analysis still inspects actual columns first, then uses `Popularity`
as the primary target. If a future dataset lacks a direct field, the helper code
can still fall back to the strongest available proxy and label it clearly.

**Alternatives considered**: Inferring popularity from audio features alone was
rejected because it would make the target circular or unsupported. Pulling live
Spotify popularity from the API was rejected for v1 because it adds credentials,
rate limits, and temporal drift beyond the provided dataset.

## Decision: Use Top 10% As The Primary Popular Segment

**Rationale**: The clarified spec defines popular songs as the top 10% of tracks
by the selected target. A top-decile segment is easy to explain, reproducible,
and makes the popular-vs-rest comparison concrete without implying a universal
industry threshold.

**Alternatives considered**: Top quartile was rejected because it is less
selective. Tertiles were rejected because they dilute the "popular" label. A
continuous-only target was rejected because the story and visual comparisons need
a primary popular segment.

## Decision: Compare Features Before Modeling

**Rationale**: The core question is explanatory. The analysis should first show
transparent comparisons between the top 10% popular segment and remaining tracks
across audio features, duration, and artist/exposure metadata patterns.
Interpretable modeling can then rank drivers after the target and cleaning rules
are clear.

**Alternatives considered**: A black-box model-first approach was rejected
because it would make findings harder to explain and easier to overstate.

## Decision: Use Interpretable Modeling Only As Supporting Evidence

**Rationale**: A regularized regression, tree-based model with permutation
importance, or similar interpretable summary can help rank associations, but the
report must avoid causal claims. Feature importance will support, not replace,
distributional evidence and grouped comparisons.

**Alternatives considered**: Deep learning and recommendation models were
rejected because the feature asks for explanation, not prediction or production
recommendation.

## Decision: Final Findings Use The Full Valid Dataset

**Rationale**: The clarified spec requires final reported findings to use the
full valid dataset after documented cleaning/exclusion rules. Sampling is allowed
for exploratory development or performance checks only.

**Alternatives considered**: Sampling final findings was rejected because it
would weaken trust in a dataset-scale question. Splitting summaries and models
between full data and samples was rejected for v1 to keep the evidence standard
simple and consistent.

## Decision: No Video Deliverable

**Rationale**: The constitution and feature spec explicitly exclude a YouTube or
video deliverable unless restored later. The README and notebook will carry the
story.

**Alternatives considered**: Including a placeholder video section was rejected
because it would conflict with the user's instruction to ignore the data video
step.
