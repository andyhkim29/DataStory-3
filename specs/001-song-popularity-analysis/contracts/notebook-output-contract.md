# Contract: Notebook And Report Outputs

## Purpose

Define the minimum outputs the notebook and README must produce for the song
popularity data story.

## Required Notebook Sections

- Dataset source and import instructions.
- Field inventory and data quality summary.
- Popularity target definition.
- Direct-popularity target explanation for the dataset's `Popularity` field.
- Cleaning and deduplication decisions.
- Top-10% popularity segment construction.
- Audio-feature comparisons.
- Artist/exposure metadata comparisons where supported.
- Ranked driver summary.
- Limitations and alternative explanations.

## Required Generated Artifacts

- At least one dataset coverage or missingness summary.
- At least one distribution chart for the selected popularity target.
- At least one comparison chart between the top 10% popular segment and remaining
  tracks.
- At least one ranked driver chart or table.
- Exported figures in `figures/` for README use.

## README Requirements

- Project name.
- Authors and GitHub usernames.
- Main question.
- Approach.
- Data used and data links.
- Tools used.
- Key findings.
- Running instructions.
- Contributing, next steps, open questions, or known issues.
- Acknowledgements and citations.
- No YouTube/video link unless explicitly restored later.

## Validation

- Every major README finding links to or references notebook evidence.
- Notebook execution recreates the figures or tables used in the README.
- Limitations are visible in both the notebook and final README.
- Final reported findings are computed from the full valid dataset, not a sample.
