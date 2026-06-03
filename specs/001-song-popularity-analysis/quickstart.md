# Quickstart: Song Popularity Analysis

## Prerequisites

- Python 3.13
- Kaggle account access for the dataset if direct download is required
- Enough local disk space for the raw dataset and processed outputs

## Setup

1. Create and activate a virtual environment.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies after `requirements.txt` exists.

   ```bash
   pip install -r requirements.txt
   ```

3. Obtain the dataset from Kaggle:

   `https://www.kaggle.com/datasets/devdope/900k-spotify`

   Or use KaggleHub:

   ```python
   import kagglehub
   path = kagglehub.dataset_download("devdope/900k-spotify")
   print("Path to dataset files:", path)
   ```

4. Place or symlink `spotify_dataset.csv` in `data/raw/`.

## Reproduce The Analysis

1. Launch Jupyter.

   ```bash
   jupyter notebook notebook.ipynb
   ```

2. Run the notebook from top to bottom.

3. Confirm generated outputs appear in:

   ```text
   data/processed/
   figures/
   ```

4. Confirm README findings are supported by notebook charts, tables, or
   statistics.

## Validation Checklist

- The notebook defines the popularity target before comparisons.
- The `Popularity` field is selected as the direct popularity target.
- Popular songs are defined as the top 10% of tracks by the selected target.
- Final findings are based on the full valid dataset after cleaning, not a sample.
- Dataset source and access instructions are visible.
- Large data is not committed directly when it exceeds 10 MB.
- Every final claim is backed by evidence.
- The README includes project metadata, data links, running instructions,
  contributing/known issues, acknowledgements, and citations.
- No YouTube/video deliverable is required for this project.

## Execution Validation Commands

Run helper tests:

```bash
PYTHONPATH=src pytest tests/
```

Run the notebook end-to-end:

```bash
PYTHONPATH=src jupyter nbconvert --to notebook --execute notebook.ipynb --output notebook.executed.ipynb
```
