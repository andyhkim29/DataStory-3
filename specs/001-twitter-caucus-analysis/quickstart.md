# Quickstart: 118th Congress Twitter Caucus Analysis

## Prerequisites

- Python 3.10 or newer.
- Jupyter Notebook or JupyterLab.
- Python packages: `pandas`, `requests`, `plotly`, `notebook` or `jupyterlab`.
- Optional package for static image export: `kaleido`.

The final notebook should include a top comment or markdown block with the
specific versions used during development.

## Run From a Fresh Clone

1. Open the repository root.
2. Install the notebook dependencies in your preferred Python environment.
3. Optional: create `twitter-caucus-118/data/manual/top10_bill_counts.csv` with
   columns `bioguide_id`, `member_name`, `bills_sponsored`, `bills_enacted`.
   Counts should come from Congress.gov for the selected analysis Congress shown
   by the notebook: use each member page's Legislation Sponsored count for
   `bills_sponsored` and the enacted sponsored-bill count for `bills_enacted`.
4. Open `twitter-caucus-118/notebook.ipynb`.
5. Restart the kernel and run all cells.

## Expected Outputs

After a successful run, inspect:

- `twitter-caucus-118/data/processed/member_tweet_counts.csv`
- `twitter-caucus-118/data/processed/top10_with_legislation.csv`
- `twitter-caucus-118/figures/distribution.html`
- The rendered coverage summary near the top of the notebook.
- The rendered top-10 table and final under-500-word writeup near the end.

## Manual Bill Count Workflow

If `top10_bill_counts.csv` is missing, the notebook still completes. It prints
the identified top 10 names and bioguide identifiers with zero placeholders so
the user can look up Congress.gov counts for the selected analysis Congress and
fill the manual CSV. Rerun the notebook after adding counts to regenerate
`top10_with_legislation.csv` and the summary table.

Use Congress.gov as the source. For each top-10 member, select the Congress that
matches the notebook's selected analysis window, record the Legislation Sponsored
count as `bills_sponsored`, and record the enacted sponsored-bill count as
`bills_enacted`.

## Cache Behavior

Daily tweet JSON files, account metadata, and service-date lookup data are
cached under `twitter-caucus-118/data/raw/`. A second notebook run should reuse
valid cached files rather than refetching the full archive.

If raw downloaded data exceeds 10 MB, do not commit the cache. Commit the
notebook, README, manual CSV template, processed outputs if appropriate, and
documentation explaining how the cache regenerates.

## Validation Checklist

- The first substantive notebook output is the coverage verification summary.
- The selected window is clearly labeled as 118th Congress or 117th fallback.
- Processed CSV schemas match `contracts/processed-data-contract.md`.
- Distribution chart includes party coloring, top-10 annotations, and cumulative
  share through top 100.
- The final writeup includes the concentration headline, top 10 by name,
  tweets-versus-bills observation, and caveats.
- To simulate a fresh clone, remove `twitter-caucus-118/data/raw/`,
  `twitter-caucus-118/data/processed/`, and generated figure files, then rerun
  the notebook from a restarted kernel.
