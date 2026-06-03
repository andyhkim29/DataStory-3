"""Data loading and validation helpers for the song popularity analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
from typing import Iterable, Sequence

import pandas as pd

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
FIGURES_DIR = Path("figures")

SUPPORTED_DATA_SUFFIXES = {".csv", ".parquet", ".feather", ".json", ".jsonl", ".sqlite", ".db"}

AUDIO_FEATURE_RANGES: dict[str, tuple[float, float]] = {
    "danceability": (0.0, 1.0),
    "energy": (0.0, 1.0),
    "speechiness": (0.0, 1.0),
    "acousticness": (0.0, 1.0),
    "instrumentalness": (0.0, 1.0),
    "liveness": (0.0, 1.0),
    "valence": (0.0, 1.0),
}

SPOTIFY_900K_COLUMN_MAP = {
    "Artist(s)": "artist_name",
    "song": "track_name",
    "Length": "length",
    "Genre": "genre",
    "Album": "album_name",
    "Release Date": "release_date",
    "Key": "key",
    "Tempo": "tempo",
    "Loudness (db)": "loudness",
    "Time signature": "time_signature",
    "Explicit": "explicit",
    "Popularity": "popularity",
    "Energy": "energy",
    "Danceability": "danceability",
    "Positiveness": "valence",
    "Speechiness": "speechiness",
    "Liveness": "liveness",
    "Acousticness": "acousticness",
    "Instrumentalness": "instrumentalness",
}
DEFAULT_ANALYSIS_SOURCE_COLUMNS = tuple(SPOTIFY_900K_COLUMN_MAP)
TAG_SOURCE_COLUMNS = (
    "emotion",
    "Genre",
    "Explicit",
    "Key",
    "Good for Party",
    "Good for Work/Study",
    "Good for Relaxation/Meditation",
    "Good for Exercise",
    "Good for Running",
    "Good for Yoga/Stretching",
    "Good for Driving",
    "Good for Social Gatherings",
    "Good for Morning Routine",
)


class DataNotFoundError(FileNotFoundError):
    """Raised when no local raw dataset file can be found."""


@dataclass(frozen=True)
class DatasetPaths:
    """Project data directories used by the analysis."""

    raw: Path = RAW_DATA_DIR
    processed: Path = PROCESSED_DATA_DIR
    figures: Path = FIGURES_DIR

    def ensure(self) -> None:
        """Create expected project data directories."""

        for directory in (self.raw, self.processed, self.figures):
            directory.mkdir(parents=True, exist_ok=True)


def expected_paths() -> DatasetPaths:
    """Return the expected data/output paths for this project."""

    return DatasetPaths()


def discover_raw_data_files(raw_dir: Path | str = RAW_DATA_DIR) -> list[Path]:
    """Return supported raw data files under ``raw_dir``.

    Hidden files and placeholder files are ignored. The function returns files in
    stable sorted order so notebook output is reproducible.
    """

    raw_path = Path(raw_dir)
    if not raw_path.exists():
        raise DataNotFoundError(_missing_data_message(raw_path))

    files = sorted(
        path
        for path in raw_path.iterdir()
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in SUPPORTED_DATA_SUFFIXES
    )
    if not files:
        raise DataNotFoundError(_missing_data_message(raw_path))
    return files


def _missing_data_message(raw_path: Path) -> str:
    return (
        f"No supported raw data files found in {raw_path}. Download the Kaggle "
        "dataset from "
        "https://www.kaggle.com/datasets/devdope/900k-spotify "
        "and place or symlink spotify_dataset.csv in data/raw/."
    )


def load_table(path: Path | str, columns: Sequence[str] | None = None) -> pd.DataFrame:
    """Load a supported raw or processed table."""

    table_path = Path(path)
    suffix = table_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(table_path, usecols=columns)
    if suffix == ".parquet":
        return pd.read_parquet(table_path, columns=list(columns) if columns else None)
    if suffix == ".feather":
        return pd.read_feather(table_path, columns=list(columns) if columns else None)
    if suffix in {".json", ".jsonl"}:
        return pd.read_json(table_path, lines=suffix == ".jsonl")
    if suffix in {".sqlite", ".db"}:
        return load_sqlite_table(table_path, columns=columns)
    raise ValueError(f"Unsupported data file type: {table_path}")


def normalize_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize known source datasets to the canonical analysis column names."""

    working = df.rename(columns={k: v for k, v in SPOTIFY_900K_COLUMN_MAP.items() if k in df.columns})
    if "length" in working.columns and "duration_ms" not in working.columns:
        working["duration_ms"] = working["length"].map(_duration_to_ms)
    if "loudness" in working.columns:
        working["loudness"] = (
            working["loudness"].astype(str).str.replace("db", "", case=False, regex=False)
        )
    if "time_signature" in working.columns:
        working["time_signature"] = working["time_signature"].map(_time_signature_numerator)
    for column in AUDIO_FEATURE_RANGES:
        if column in working.columns:
            numeric = pd.to_numeric(working[column], errors="coerce")
            if numeric.dropna().gt(1).any():
                numeric = numeric / 100
            working[column] = numeric
    for column in (
        "popularity",
        "duration_ms",
        "tempo",
        "loudness",
        "time_signature",
    ):
        if column in working.columns:
            working[column] = pd.to_numeric(working[column], errors="coerce")
    return working


def _duration_to_ms(value: object) -> int | None:
    if value is None or pd.isna(value):
        return None
    parts = str(value).strip().split(":")
    if len(parts) != 2:
        return None
    try:
        minutes = int(parts[0])
        seconds = int(parts[1])
    except ValueError:
        return None
    return (minutes * 60 + seconds) * 1000


def _time_signature_numerator(value: object) -> int | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if "/" in text:
        text = text.split("/", 1)[0]
    try:
        return int(text)
    except ValueError:
        return None


def load_sqlite_table(
    path: Path | str,
    table_name: str | None = None,
    columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Load a table from a SQLite database.

    If ``table_name`` is omitted, the database must contain exactly one table.
    """

    sqlite_path = Path(path)
    with sqlite3.connect(sqlite_path) as connection:
        selected_table = table_name or _single_sqlite_table(connection, sqlite_path)
        table_identifier = _quote_sqlite_identifier(selected_table)
        if columns:
            selected_columns = ", ".join(_quote_sqlite_identifier(column) for column in columns)
        else:
            selected_columns = "*"
        return pd.read_sql_query(
            f"SELECT {selected_columns} FROM {table_identifier}",
            connection,
        )


def _single_sqlite_table(connection: sqlite3.Connection, sqlite_path: Path) -> str:
    tables = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name",
        connection,
    )["name"].tolist()
    if not tables:
        raise ValueError(f"No tables found in SQLite database: {sqlite_path}")
    if len(tables) > 1:
        raise ValueError(
            f"SQLite database {sqlite_path} has multiple tables; pass table_name explicitly."
        )
    return str(tables[0])


def _quote_sqlite_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def column_inventory(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize columns, dtypes, missingness, and unique counts."""

    row_count = len(df)
    return pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(dtype) for dtype in df.dtypes],
            "missing_count": [int(df[column].isna().sum()) for column in df.columns],
            "missing_pct": [
                float(df[column].isna().mean()) if row_count else 0.0
                for column in df.columns
            ],
            "unique_count": [int(df[column].nunique(dropna=True)) for column in df.columns],
        }
    )


def duplicate_summary(
    df: pd.DataFrame,
    id_column: str = "track_uri",
    fallback_columns: Sequence[str] = ("track_name", "artist_name"),
) -> pd.DataFrame:
    """Return duplicate counts for track identity keys available in ``df``."""

    rows: list[dict[str, object]] = []
    if id_column in df.columns:
        duplicate_count = int(df.duplicated(subset=[id_column], keep=False).sum())
        rows.append(
            {
                "key": id_column,
                "available": True,
                "duplicate_rows": duplicate_count,
            }
        )

    available_fallback = [column for column in fallback_columns if column in df.columns]
    if len(available_fallback) == len(fallback_columns):
        duplicate_count = int(df.duplicated(subset=list(fallback_columns), keep=False).sum())
        rows.append(
            {
                "key": "+".join(fallback_columns),
                "available": True,
                "duplicate_rows": duplicate_count,
            }
        )

    if not rows:
        rows.append({"key": "track identity", "available": False, "duplicate_rows": None})
    return pd.DataFrame(rows)


def validate_audio_feature_ranges(
    df: pd.DataFrame,
    ranges: dict[str, tuple[float, float]] | None = None,
) -> pd.DataFrame:
    """Count missing and out-of-range values for bounded Spotify audio features."""

    checks = ranges or AUDIO_FEATURE_RANGES
    rows: list[dict[str, object]] = []
    for column, (minimum, maximum) in checks.items():
        if column not in df.columns:
            rows.append(
                {
                    "column": column,
                    "available": False,
                    "missing_count": None,
                    "out_of_range_count": None,
                    "valid_count": None,
                }
            )
            continue
        series = pd.to_numeric(df[column], errors="coerce")
        missing = int(series.isna().sum())
        out_of_range = int(((series < minimum) | (series > maximum)).sum())
        rows.append(
            {
                "column": column,
                "available": True,
                "missing_count": missing,
                "out_of_range_count": out_of_range,
                "valid_count": int(len(series) - missing - out_of_range),
            }
        )
    return pd.DataFrame(rows)


def full_valid_dataset(
    df: pd.DataFrame,
    required_columns: Iterable[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return rows valid for final findings and an exclusion summary."""

    required = [column for column in required_columns if column in df.columns]
    if not required:
        summary = pd.DataFrame(
            [
                {
                    "raw_records": len(df),
                    "excluded_records": 0,
                    "valid_records": len(df),
                    "required_columns": "",
                }
            ]
        )
        return df.copy(), summary

    mask = df[required].notna().all(axis=1)
    valid = df.loc[mask].copy()
    summary = pd.DataFrame(
        [
            {
                "raw_records": int(len(df)),
                "excluded_records": int((~mask).sum()),
                "valid_records": int(len(valid)),
                "required_columns": ", ".join(required),
            }
        ]
    )
    return valid, summary


def write_processed_table(
    df: pd.DataFrame,
    filename: str,
    processed_dir: Path | str = PROCESSED_DATA_DIR,
) -> Path:
    """Write a reproducible processed table to CSV or Parquet."""

    output_path = Path(processed_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix == ".csv":
        df.to_csv(output_path, index=False)
    elif suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    else:
        raise ValueError("Processed output must end with .csv or .parquet")
    return output_path
