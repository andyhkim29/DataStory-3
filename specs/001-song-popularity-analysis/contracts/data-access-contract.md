# Contract: Data Access And Storage

## Purpose

Define how the project obtains, stores, and documents the Kaggle song dataset so
the analysis can be reproduced without private local files.

## Inputs

- Kaggle dataset URL: `https://www.kaggle.com/datasets/devdope/900k-spotify`
- KaggleHub handle: `devdope/900k-spotify`
- Local raw-data directory: `data/raw/`
- Local processed-data directory: `data/processed/`

## Required Behavior

- The README must link to the dataset source and state any access constraints.
- The notebook or code must include a documented download/import step.
- If the source data totals 10 MB or more, it must not be committed directly.
- If a derived dataset is committed, its generation step must be documented.
- Raw data and processed data must remain distinguishable by path and filename.

## Expected Files

```text
data/raw/
└── <downloaded-kaggle-file-or-placeholder>

data/processed/
└── <derived-analysis-file>
```

## Validation

- A fresh checkout plus documented data access steps can recreate the processed
  data required by the notebook.
- Missing data produces a clear instruction, not a silent failure.
