"""Popularity target selection and driver analysis helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd

DIRECT_POPULARITY_CANDIDATES = (
    "popularity",
    "track_popularity",
    "spotify_popularity",
    "track_popularity_score",
)

PLAYLIST_PROXY_CANDIDATES = (
    "playlist_count",
    "playlist_frequency",
    "playlist_appearances",
    "num_playlists",
    "playlist_rank",
    "playlist_position",
)

ARTIST_COLUMNS = ("artist_uri", "artist_name")

AUDIO_FEATURE_COLUMNS = (
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "duration_ms",
    "key",
    "mode",
    "time_signature",
)

ACTIVITY_TAG_COLUMNS = (
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

CATEGORICAL_TAG_COLUMNS = ("genre", "emotion", "explicit")


@dataclass(frozen=True)
class PopularityTarget:
    """Selected popularity target metadata."""

    target_name: str
    target_type: str
    target_strength: str
    target_value_column: str
    target_definition: str
    source_fields: tuple[str, ...]


def available_target_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """Return direct and playlist-derived target candidates found in ``df``."""

    rows: list[dict[str, object]] = []
    for column in DIRECT_POPULARITY_CANDIDATES:
        if column in df.columns:
            rows.append(
                {
                    "column": column,
                    "target_type": "direct_score",
                    "target_strength": "direct",
                    "non_null_count": int(df[column].notna().sum()),
                }
            )
    for column in PLAYLIST_PROXY_CANDIDATES:
        if column in df.columns:
            rows.append(
                {
                    "column": column,
                    "target_type": "playlist_proxy",
                    "target_strength": "proxy",
                    "non_null_count": int(df[column].notna().sum()),
                }
            )
    return pd.DataFrame(rows)


def derive_artist_repetition_proxy(
    df: pd.DataFrame,
    preferred_columns: Sequence[str] = ARTIST_COLUMNS,
    output_column: str = "artist_repetition_count",
) -> pd.Series:
    """Derive a weak popularity proxy from repeated artist appearances."""

    artist_column = next((column for column in preferred_columns if column in df.columns), None)
    if artist_column is None:
        raise ValueError(
            "Cannot derive artist repetition proxy; expected artist_uri or artist_name column."
        )
    return df[artist_column].map(df[artist_column].value_counts(dropna=False)).rename(output_column)


def select_popularity_target(df: pd.DataFrame) -> tuple[pd.DataFrame, PopularityTarget]:
    """Select the best available popularity target and return a dataframe copy.

    Preference order:
    1. Direct Spotify-like popularity score.
    2. Playlist-derived proxy.
    3. Artist repetition/count weak proxy.
    """

    working = df.copy()
    candidates = available_target_candidates(working)
    if not candidates.empty:
        candidate = candidates.sort_values(
            by=["target_strength", "non_null_count"],
            key=lambda values: values.map({"direct": 0, "proxy": 1}).fillna(values)
            if values.name == "target_strength"
            else values,
            ascending=[True, False],
        ).iloc[0]
        column = str(candidate["column"])
        target = PopularityTarget(
            target_name=column,
            target_type=str(candidate["target_type"]),
            target_strength=str(candidate["target_strength"]),
            target_value_column=column,
            target_definition=_target_definition(
                str(candidate["target_type"]), str(candidate["target_strength"]), column
            ),
            source_fields=(column,),
        )
        return working, target

    proxy = derive_artist_repetition_proxy(working)
    working[proxy.name] = proxy
    target = PopularityTarget(
        target_name=proxy.name,
        target_type="artist_repetition_proxy",
        target_strength="weak_proxy",
        target_value_column=proxy.name,
        target_definition=(
            "Weak popularity proxy based on how often an artist appears in the dataset. "
            "This reflects artist exposure in this dataset, not universal listener preference."
        ),
        source_fields=tuple(column for column in ARTIST_COLUMNS if column in working.columns),
    )
    return working, target


def _target_definition(target_type: str, target_strength: str, column: str) -> str:
    if target_type == "direct_score":
        return f"Direct popularity score from `{column}`."
    if target_strength == "proxy":
        return (
            f"Playlist-derived popularity proxy from `{column}`. This reflects playlist "
            "presence or prominence rather than universal listener preference."
        )
    return f"Popularity target from `{column}`."


def top_decile_segment(
    df: pd.DataFrame,
    target: PopularityTarget | str,
    segment_column: str = "popularity_segment",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Assign top-10-percent and remaining-track segments by selected target."""

    target_column = target.target_value_column if isinstance(target, PopularityTarget) else target
    if target_column not in df.columns:
        raise ValueError(f"Target column not found: {target_column}")
    working = df.copy()
    values = pd.to_numeric(working[target_column], errors="coerce")
    valid_values = values.dropna()
    if valid_values.empty:
        raise ValueError(f"Target column has no numeric values: {target_column}")
    threshold = float(valid_values.quantile(0.9))
    working[segment_column] = np.where(
        values >= threshold, "top_10_percent", "remaining_tracks"
    )
    working.loc[values.isna(), segment_column] = "missing_target"
    counts = (
        working[segment_column]
        .value_counts(dropna=False)
        .rename_axis("segment_name")
        .reset_index(name="track_count")
    )
    counts["threshold"] = threshold
    counts["target_column"] = target_column
    return working, counts


def audio_feature_comparison(
    df: pd.DataFrame,
    segment_column: str = "popularity_segment",
    feature_columns: Sequence[str] = AUDIO_FEATURE_COLUMNS,
) -> pd.DataFrame:
    """Compare numeric audio features between top-decile and remaining tracks."""

    rows: list[dict[str, object]] = []
    for column in feature_columns:
        if column not in df.columns:
            continue
        values = pd.to_numeric(df[column], errors="coerce")
        top = values[df[segment_column] == "top_10_percent"].dropna()
        rest = values[df[segment_column] == "remaining_tracks"].dropna()
        if top.empty or rest.empty:
            continue
        rows.append(
            {
                "driver": column,
                "driver_type": "audio_feature",
                "top_10_mean": float(top.mean()),
                "remaining_mean": float(rest.mean()),
                "difference": float(top.mean() - rest.mean()),
                "abs_difference": float(abs(top.mean() - rest.mean())),
                "top_10_count": int(len(top)),
                "remaining_count": int(len(rest)),
            }
        )
    return pd.DataFrame(rows).sort_values("abs_difference", ascending=False, ignore_index=True)


def metadata_exposure_comparison(
    df: pd.DataFrame,
    segment_column: str = "popularity_segment",
) -> pd.DataFrame:
    """Summarize artist and album exposure patterns by popularity segment."""

    rows: list[dict[str, object]] = []
    for column in ("artist_uri", "artist_name", "album_uri", "album_name"):
        if column not in df.columns:
            continue
        top = df.loc[df[segment_column] == "top_10_percent", column].dropna()
        rest = df.loc[df[segment_column] == "remaining_tracks", column].dropna()
        if top.empty or rest.empty:
            continue
        rows.append(
            {
                "driver": column,
                "driver_type": "artist_exposure" if column.startswith("artist") else "album_exposure",
                "top_10_unique": int(top.nunique()),
                "remaining_unique": int(rest.nunique()),
                "top_10_repetition_rate": float(1 - top.nunique() / len(top)),
                "remaining_repetition_rate": float(1 - rest.nunique() / len(rest)),
                "difference": float((1 - top.nunique() / len(top)) - (1 - rest.nunique() / len(rest))),
                "abs_difference": float(
                    abs((1 - top.nunique() / len(top)) - (1 - rest.nunique() / len(rest)))
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("abs_difference", ascending=False, ignore_index=True)


def rank_drivers(*comparisons: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Combine comparison tables into one ranked driver summary."""

    available = [table for table in comparisons if table is not None and not table.empty]
    if not available:
        return pd.DataFrame(
            columns=["rank", "driver", "driver_type", "difference", "abs_difference"]
        )
    combined = pd.concat(available, ignore_index=True, sort=False)
    combined = combined.sort_values("abs_difference", ascending=False).head(top_n).copy()
    combined.insert(0, "rank", range(1, len(combined) + 1))
    return combined.reset_index(drop=True)


def categorical_tag_lift(
    df: pd.DataFrame,
    column: str,
    segment_column: str = "popularity_segment",
    min_top_count: int = 100,
) -> pd.DataFrame:
    """Compare categorical tag rates in top-decile tracks versus the rest."""

    top = df.loc[df[segment_column] == "top_10_percent", column].dropna().astype(str)
    rest = df.loc[df[segment_column] == "remaining_tracks", column].dropna().astype(str)
    top_counts = top.value_counts()
    rest_counts = rest.value_counts()
    summary = pd.DataFrame({"top_count": top_counts, "remaining_count": rest_counts}).fillna(0)
    summary["top_pct"] = summary["top_count"] / len(top) if len(top) else 0.0
    summary["remaining_pct"] = summary["remaining_count"] / len(rest) if len(rest) else 0.0
    summary["pct_point_diff"] = summary["top_pct"] - summary["remaining_pct"]
    summary["lift"] = summary["top_pct"] / summary["remaining_pct"].replace(0, np.nan)
    summary = summary[summary["top_count"] >= min_top_count]
    return (
        summary.sort_values(["pct_point_diff", "top_pct"], ascending=False)
        .reset_index(names=column)
        .reset_index(drop=True)
    )


def activity_tag_lift(
    df: pd.DataFrame,
    tag_columns: Sequence[str] = ACTIVITY_TAG_COLUMNS,
    segment_column: str = "popularity_segment",
) -> pd.DataFrame:
    """Compare binary activity tag rates in top-decile tracks versus the rest."""

    rows: list[dict[str, object]] = []
    top_mask = df[segment_column] == "top_10_percent"
    rest_mask = df[segment_column] == "remaining_tracks"
    for column in tag_columns:
        if column not in df.columns:
            continue
        top = pd.to_numeric(df.loc[top_mask, column], errors="coerce").fillna(0) > 0
        rest = pd.to_numeric(df.loc[rest_mask, column], errors="coerce").fillna(0) > 0
        top_pct = float(top.mean()) if len(top) else 0.0
        rest_pct = float(rest.mean()) if len(rest) else 0.0
        rows.append(
            {
                "tag": column,
                "top_count": int(top.sum()),
                "remaining_count": int(rest.sum()),
                "top_pct": top_pct,
                "remaining_pct": rest_pct,
                "pct_point_diff": top_pct - rest_pct,
                "lift": top_pct / rest_pct if rest_pct else np.nan,
            }
        )
    return pd.DataFrame(rows).sort_values("pct_point_diff", ascending=False, ignore_index=True)


def popular_tag_counts(
    df: pd.DataFrame,
    categorical_columns: Sequence[str] = CATEGORICAL_TAG_COLUMNS,
    activity_columns: Sequence[str] = ACTIVITY_TAG_COLUMNS,
    segment_column: str = "popularity_segment",
) -> pd.DataFrame:
    """Count how many popular songs carry each available tag."""

    rows: list[dict[str, object]] = []
    popular = df.loc[df[segment_column] == "top_10_percent"]
    popular_track_count = len(popular)

    for column in categorical_columns:
        if column not in popular.columns:
            continue
        tags = popular[column].dropna().astype(str).str.strip()
        tags = tags[tags.ne("")]
        for tag, count in tags.value_counts().items():
            rows.append(
                {
                    "tag": tag,
                    "tag_group": column,
                    "popular_count": int(count),
                    "popular_share": float(count / popular_track_count)
                    if popular_track_count
                    else 0.0,
                    "popular_track_count": popular_track_count,
                }
            )

    for column in activity_columns:
        if column not in popular.columns:
            continue
        has_tag = pd.to_numeric(popular[column], errors="coerce").fillna(0) > 0
        count = int(has_tag.sum())
        if count == 0:
            continue
        rows.append(
            {
                "tag": column,
                "tag_group": "activity",
                "popular_count": count,
                "popular_share": float(count / popular_track_count)
                if popular_track_count
                else 0.0,
                "popular_track_count": popular_track_count,
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "tag",
                "tag_group",
                "popular_count",
                "popular_share",
                "popular_track_count",
            ]
        )

    return pd.DataFrame(rows).sort_values(
        ["popular_count", "tag_group", "tag"], ascending=[False, True, True], ignore_index=True
    )


def popular_tag_venn_summary(
    df: pd.DataFrame,
    categorical_columns: Sequence[str] = CATEGORICAL_TAG_COLUMNS,
    activity_columns: Sequence[str] = ACTIVITY_TAG_COLUMNS,
    segment_column: str = "popularity_segment",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Summarize exact overlaps among the top three tags on popular songs."""

    popular = df.loc[df[segment_column] == "top_10_percent"].copy()
    top_tags = popular_tag_counts(
        df,
        categorical_columns=categorical_columns,
        activity_columns=activity_columns,
        segment_column=segment_column,
    ).head(3)

    if len(top_tags) < 3 or popular.empty:
        return top_tags, pd.DataFrame(columns=["region", "tags", "count"])

    masks: list[pd.Series] = []
    for tag in top_tags.itertuples(index=False):
        tag_name = str(tag.tag)
        tag_group = str(tag.tag_group)
        if tag_group == "activity":
            masks.append(pd.to_numeric(popular[tag_name], errors="coerce").fillna(0) > 0)
        else:
            values = popular[tag_group].dropna().astype(str).str.strip()
            masks.append(values.reindex(popular.index, fill_value="").eq(tag_name))

    a, b, c = masks
    tag_names = top_tags["tag"].astype(str).tolist()
    regions = [
        ("100", tag_names[0], a & ~b & ~c),
        ("010", tag_names[1], ~a & b & ~c),
        ("001", tag_names[2], ~a & ~b & c),
        ("110", f"{tag_names[0]} + {tag_names[1]}", a & b & ~c),
        ("101", f"{tag_names[0]} + {tag_names[2]}", a & ~b & c),
        ("011", f"{tag_names[1]} + {tag_names[2]}", ~a & b & c),
        ("111", "All three", a & b & c),
        ("000", "None of top three", ~(a | b | c)),
    ]
    return top_tags, pd.DataFrame(
        [{"region": region, "tags": tags, "count": int(mask.sum())} for region, tags, mask in regions]
    )
