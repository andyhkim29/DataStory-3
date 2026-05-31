# Notebook Output Contract

## Required Execution Order

The notebook must present the first substantive output as data quality
verification. Member aggregation, charting, top-10 selection, and writeup cells
must appear after the verification summary.

## Required Notebook Sections

1. The dataset and verification
2. Loading and account filtering
3. Member-level aggregation
4. Distribution analysis
5. Top 10 with bill counts
6. Findings and caveats

## Required Visible Outputs

- Coverage summary with expected days, populated days, missing days, coverage
  share, required spot-check tweet counts, degradation warning status, and
  selected analysis window.
- Printed top-10 lookup list when `data/manual/top10_bill_counts.csv` is absent.
- Rendered top-10 table with party, tweet count, tweets per day, bills sponsored,
  and bills enacted.
- Final markdown writeup under 500 words.

## Required File Outputs

- `data/processed/member_tweet_counts.csv`
- `data/processed/top10_with_legislation.csv`
- `figures/distribution.html`
- Optional static figure export such as `figures/distribution.png` when export
  dependencies are available.

## Figure Requirements

The distribution figure must include:

- Ranked member tweet count panel with rank on x-axis and tweet volume on y-axis.
- Party color-coding.
- Top-10 member name annotations.
- Cumulative share panel for top N members from N = 1 through 100.
- A visible marker or annotation for the smallest N where cumulative share
  reaches at least 50%.

## Caveat Requirements

The final writeup and relevant notebook sections must state:

- Published tweets only; deleted tweets are not represented.
- No engagement metrics are available; this is volume, not engagement.
- Twitter became X in July 2023; that platform change is context only.
- Bill sponsorship is only one measure of legislative activity and does not
  cover co-sponsorships, committee work, floor speeches, or vote attendance.
- Any degraded coverage or fallback-window decision from verification.
