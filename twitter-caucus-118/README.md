# 118th Congress Twitter Caucus Analysis

This project is a reproducible notebook analysis of how Congressional Twitter
activity was concentrated across members of Congress during the 118th Congress
window, January 3, 2023 through January 3, 2025. If archive coverage for that
window is severely degraded, the notebook falls back to the 117th Congress
window, January 3, 2021 through January 3, 2023.

## Requirements

- Python 3.10+
- Jupyter Notebook or JupyterLab
- `pandas`
- `requests`
- `plotly`
- `ipykernel`
- `PyYAML`
- Optional: `kaleido` for static Plotly image export

The notebook contains a top dependency block with the version guidance used for
the analysis. To install the same dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run

1. From the repository root, install the Python requirements in your preferred
   environment.
2. Optional: fill `data/manual/top10_bill_counts.csv` after the notebook prints
   the top 10 names and bioguide identifiers. The file must keep these columns:
   `bioguide_id`, `member_name`, `bills_sponsored`, `bills_enacted`.
   Use Congress.gov for the selected analysis Congress shown by the notebook:
   record each member page's Legislation Sponsored count as `bills_sponsored`
   and the enacted sponsored-bill count as `bills_enacted`.
3. Open `notebook.ipynb`.
4. Restart the kernel and run all cells.

The only manual input expected by the project is the bill-count CSV. If it is
left as just the header row, the notebook still runs and uses zero placeholders
while printing the lookup list and selected Congress window.

## Outputs

The notebook writes:

- `data/processed/member_tweet_counts.csv`
- `data/processed/top10_with_legislation.csv`
- `figures/distribution.html`

It also renders:

- a coverage verification summary before analysis;
- a top-10 table with tweet and bill-count columns;
- a short final markdown writeup with the concentration headline, top 10, the
  tweets-versus-bills observation, and caveats.

## Cache Behavior

Daily tweet JSON files are cached under `data/raw/tweets/`. Account metadata is
cached under `data/raw/accounts/`. Service-date lookup data, if downloaded or
generated, is cached under `data/raw/service_dates/`.

The raw cache can exceed 10 MB, so it is ignored by git. A fresh clone regenerates
the cache from the public source URLs when the notebook runs.

To simulate a fresh clone during validation, remove `data/raw/`,
`data/processed/`, and generated files under `figures/`, then restart the kernel
and rerun all notebook cells. Preserve `notebook.ipynb` and the manual CSV
template.

## Manual Bill Count Lookup

Use Congress.gov as the source for `data/manual/top10_bill_counts.csv`. After the
notebook identifies the top 10, choose the Congress that matches the selected
analysis window printed by the notebook. For each member, use the member page's
Legislation Sponsored count for `bills_sponsored` and the enacted sponsored-bill
count for `bills_enacted`.

## Caveats

The congresstweets archive captures published tweets only; deleted tweets are
not represented. It does not include likes, retweets, replies, or other
engagement metrics, so this is a volume analysis rather than an engagement
analysis. Twitter became X in July 2023; this is noted as context and not
analyzed. Bill sponsorship is one measure of legislative activity and does not
capture co-sponsorships, committee work, floor speeches, or vote attendance.
When account metadata lacks reliable service dates, the notebook attempts the
official `unitedstates/congress-legislators` service-date lookup before falling
back to selected-window boundaries, and reports that fallback in the notebook.
