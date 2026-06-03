from pathlib import Path

import pandas as pd
import pytest

from song_popularity.data import (
    DataNotFoundError,
    discover_raw_data_files,
    duplicate_summary,
    full_valid_dataset,
    load_table,
    normalize_analysis_columns,
    validate_audio_feature_ranges,
)
from song_popularity.popularity import (
    activity_tag_lift,
    audio_feature_comparison,
    categorical_tag_lift,
    metadata_exposure_comparison,
    popular_tag_counts,
    popular_tag_venn_summary,
    rank_drivers,
    select_popularity_target,
    top_decile_segment,
)


def test_discover_raw_data_files_reports_missing_directory(tmp_path: Path) -> None:
    with pytest.raises(DataNotFoundError, match="Download the Kaggle dataset"):
        discover_raw_data_files(tmp_path / "missing")


def test_discover_raw_data_files_reports_empty_directory(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / ".gitkeep").write_text("", encoding="utf-8")
    with pytest.raises(DataNotFoundError, match="data/raw"):
        discover_raw_data_files(raw)


def test_load_table_reads_single_table_sqlite_database(tmp_path: Path) -> None:
    sqlite_path = tmp_path / "songs.sqlite"
    source = pd.DataFrame(
        {"track_uri": ["spotify:track:1", "spotify:track:2"], "danceability": [0.3, 0.7]}
    )
    import sqlite3

    with sqlite3.connect(sqlite_path) as connection:
        source.to_sql("extracted", connection, index=False)

    loaded = load_table(sqlite_path, columns=["track_uri"])

    assert loaded.to_dict(orient="records") == [
        {"track_uri": "spotify:track:1"},
        {"track_uri": "spotify:track:2"},
    ]


def test_normalize_analysis_columns_maps_900k_spotify_fields() -> None:
    df = pd.DataFrame(
        {
            "Artist(s)": ["Artist"],
            "song": ["Song"],
            "Length": ["03:47"],
            "Loudness (db)": ["-6.85db"],
            "Time signature": ["4/4"],
            "Popularity": [40],
            "Positiveness": [87],
        }
    )

    normalized = normalize_analysis_columns(df)

    assert normalized["artist_name"].iloc[0] == "Artist"
    assert normalized["track_name"].iloc[0] == "Song"
    assert normalized["duration_ms"].iloc[0] == 227000
    assert normalized["loudness"].iloc[0] == pytest.approx(-6.85)
    assert normalized["time_signature"].iloc[0] == 4
    assert normalized["popularity"].iloc[0] == 40
    assert normalized["valence"].iloc[0] == pytest.approx(0.87)


def test_duplicate_summary_uses_track_uri_and_name_artist_keys() -> None:
    df = pd.DataFrame(
        {
            "track_uri": ["a", "a", "b"],
            "track_name": ["Song", "Song", "Other"],
            "artist_name": ["Artist", "Artist", "Artist"],
        }
    )
    summary = duplicate_summary(df)
    assert set(summary["key"]) == {"track_uri", "track_name+artist_name"}
    assert summary.loc[summary["key"] == "track_uri", "duplicate_rows"].iloc[0] == 2


def test_validate_audio_feature_ranges_counts_invalid_values() -> None:
    df = pd.DataFrame({"danceability": [0.1, 1.2, None], "energy": [0.4, 0.5, 0.6]})
    summary = validate_audio_feature_ranges(df)
    row = summary.loc[summary["column"] == "danceability"].iloc[0]
    assert row["missing_count"] == 1
    assert row["out_of_range_count"] == 1
    assert row["valid_count"] == 1


def test_select_popularity_target_prefers_direct_score() -> None:
    df = pd.DataFrame({"popularity": [10, 90], "playlist_count": [100, 1]})
    selected_df, target = select_popularity_target(df)
    assert selected_df.equals(df)
    assert target.target_name == "popularity"
    assert target.target_type == "direct_score"
    assert target.target_strength == "direct"


def test_select_popularity_target_uses_playlist_proxy_when_no_direct_score() -> None:
    df = pd.DataFrame({"playlist_count": [1, 5, 9], "artist_name": ["a", "b", "c"]})
    _, target = select_popularity_target(df)
    assert target.target_name == "playlist_count"
    assert target.target_type == "playlist_proxy"
    assert target.target_strength == "proxy"
    assert "Playlist-derived" in target.target_definition


def test_select_popularity_target_uses_artist_repetition_weak_proxy() -> None:
    df = pd.DataFrame({"artist_name": ["a", "a", "b"], "track_name": ["x", "y", "z"]})
    selected_df, target = select_popularity_target(df)
    assert target.target_name == "artist_repetition_count"
    assert target.target_type == "artist_repetition_proxy"
    assert target.target_strength == "weak_proxy"
    assert selected_df["artist_repetition_count"].tolist() == [2, 2, 1]


def test_top_decile_segment_reports_threshold_and_counts() -> None:
    df = pd.DataFrame({"popularity": list(range(10))})
    segmented, counts = top_decile_segment(df, "popularity")
    assert "popularity_segment" in segmented.columns
    assert counts["track_count"].sum() == 10
    assert set(counts["segment_name"]) == {"top_10_percent", "remaining_tracks"}
    assert counts["threshold"].iloc[0] == pytest.approx(8.1)


def test_full_valid_dataset_filters_missing_required_values() -> None:
    df = pd.DataFrame({"popularity": [1, None, 3], "danceability": [0.2, 0.3, None]})
    valid, summary = full_valid_dataset(df, ["popularity", "danceability"])
    assert len(valid) == 1
    assert summary["raw_records"].iloc[0] == 3
    assert summary["excluded_records"].iloc[0] == 2
    assert summary["valid_records"].iloc[0] == 1


def test_audio_feature_comparison_summarizes_top_vs_remaining() -> None:
    df = pd.DataFrame(
        {
            "popularity_segment": ["top_10_percent", "top_10_percent", "remaining_tracks"],
            "danceability": [0.8, 0.6, 0.2],
        }
    )
    comparison = audio_feature_comparison(df, feature_columns=["danceability"])
    assert comparison["driver"].iloc[0] == "danceability"
    assert comparison["difference"].iloc[0] == pytest.approx(0.5)


def test_metadata_exposure_comparison_summarizes_repetition() -> None:
    df = pd.DataFrame(
        {
            "popularity_segment": [
                "top_10_percent",
                "top_10_percent",
                "remaining_tracks",
                "remaining_tracks",
            ],
            "artist_name": ["a", "a", "b", "c"],
        }
    )
    comparison = metadata_exposure_comparison(df)
    assert comparison["driver"].iloc[0] == "artist_name"
    assert comparison["difference"].iloc[0] == pytest.approx(0.5)


def test_rank_drivers_combines_comparison_tables() -> None:
    audio = pd.DataFrame(
        [{"driver": "danceability", "driver_type": "audio_feature", "abs_difference": 0.2}]
    )
    metadata = pd.DataFrame(
        [{"driver": "artist_name", "driver_type": "artist_exposure", "abs_difference": 0.5}]
    )
    ranked = rank_drivers(audio, metadata)
    assert ranked["driver"].tolist() == ["artist_name", "danceability"]
    assert ranked["rank"].tolist() == [1, 2]


def test_categorical_tag_lift_reports_overrepresented_tags() -> None:
    df = pd.DataFrame(
        {
            "popularity_segment": [
                "top_10_percent",
                "top_10_percent",
                "remaining_tracks",
                "remaining_tracks",
            ],
            "genre": ["pop", "pop", "rock", "pop"],
        }
    )

    summary = categorical_tag_lift(df, "genre", min_top_count=1)

    assert summary["genre"].iloc[0] == "pop"
    assert summary["top_pct"].iloc[0] == pytest.approx(1.0)
    assert summary["remaining_pct"].iloc[0] == pytest.approx(0.5)


def test_activity_tag_lift_compares_binary_tag_rates() -> None:
    df = pd.DataFrame(
        {
            "popularity_segment": [
                "top_10_percent",
                "top_10_percent",
                "remaining_tracks",
                "remaining_tracks",
            ],
            "Good for Party": [1, 0, 0, 0],
        }
    )

    summary = activity_tag_lift(df, tag_columns=["Good for Party"])

    assert summary["tag"].iloc[0] == "Good for Party"
    assert summary["top_pct"].iloc[0] == pytest.approx(0.5)
    assert summary["remaining_pct"].iloc[0] == pytest.approx(0.0)


def test_popular_tag_counts_combines_available_tag_sources() -> None:
    df = pd.DataFrame(
        {
            "popularity_segment": [
                "top_10_percent",
                "top_10_percent",
                "top_10_percent",
                "remaining_tracks",
            ],
            "genre": ["pop", "rock", "pop", "rock"],
            "emotion": ["happy", "happy", "sad", "sad"],
            "Good for Party": [1, 0, 1, 1],
        }
    )

    summary = popular_tag_counts(
        df,
        categorical_columns=["genre", "emotion"],
        activity_columns=["Good for Party"],
    )

    pop = summary.loc[summary["tag"] == "pop"].iloc[0]
    party = summary.loc[summary["tag"] == "Good for Party"].iloc[0]
    assert pop["popular_count"] == 2
    assert pop["popular_share"] == pytest.approx(2 / 3)
    assert party["tag_group"] == "activity"
    assert party["popular_count"] == 2


def test_popular_tag_venn_summary_reports_exact_top_three_overlaps() -> None:
    df = pd.DataFrame(
        {
            "popularity_segment": [
                "top_10_percent",
                "top_10_percent",
                "top_10_percent",
                "top_10_percent",
                "remaining_tracks",
            ],
            "genre": ["pop", "pop", "rock", "pop", "pop"],
            "emotion": ["happy", "sad", "happy", "happy", "happy"],
            "Good for Party": [1, 0, 1, 1, 1],
        }
    )

    top_tags, regions = popular_tag_venn_summary(
        df,
        categorical_columns=["genre", "emotion"],
        activity_columns=["Good for Party"],
    )

    assert set(top_tags["tag"]) == {"Good for Party", "happy", "pop"}
    assert dict(zip(regions["region"], regions["count"], strict=False)) == {
        "100": 0,
        "010": 0,
        "001": 1,
        "110": 1,
        "101": 0,
        "011": 0,
        "111": 2,
        "000": 0,
    }
