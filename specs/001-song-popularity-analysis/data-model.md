# Data Model: Song Popularity Analysis

## Track

Represents one unique song recording.

**Fields**

- `track_uri`: Unique Spotify track identifier when available.
- `track_name`: Song title.
- `artist_uri`: Spotify artist identifier when available.
- `artist_name`: Artist display name.
- `album_uri`: Spotify album identifier when available.
- `album_name`: Album display name.
- `duration_ms`: Track duration in milliseconds.
- `audio_feature_profile`: One-to-one relationship to Audio Feature Profile.
- `popularity_target`: One-to-one derived relationship to Popularity Target.

**Validation Rules**

- A valid analysis row must have a track identifier or a stable track-name and
  artist-name pair.
- Duration must be positive when used in comparisons.
- Duplicate recordings must be documented and either deduplicated or aggregated
  consistently.

## Artist

Represents the performer or creator associated with tracks.

**Fields**

- `artist_uri`: Artist identifier when available.
- `artist_name`: Artist display name.
- `track_count`: Number of dataset tracks associated with the artist.
- `popularity_summary`: Aggregated popularity proxy or direct score across the
  artist's tracks.

**Validation Rules**

- Missing artist identifiers may be accepted if artist name is present.
- Artist-level summaries must state whether they are influenced by track count
  or playlist exposure.

## Album

Represents a release associated with tracks.

**Fields**

- `album_uri`: Album identifier when available.
- `album_name`: Album display name.
- `artist_uri`: Linked artist identifier when available.
- `track_count`: Number of dataset tracks associated with the album.

**Validation Rules**

- Album analysis is optional when album fields are sparse.
- Album-level findings must not be used as song-level evidence without clear
  aggregation language.

## Audio Feature Profile

Represents Spotify-derived numeric and categorical audio characteristics for a
track.

**Fields**

- `danceability`: Numeric score from 0 to 1 when available.
- `energy`: Numeric score from 0 to 1 when available.
- `loudness`: Numeric loudness value.
- `speechiness`: Numeric score from 0 to 1 when available.
- `acousticness`: Numeric score from 0 to 1 when available.
- `instrumentalness`: Numeric score from 0 to 1 when available.
- `liveness`: Numeric score from 0 to 1 when available.
- `valence`: Numeric score from 0 to 1 when available.
- `tempo`: Numeric beats per minute.
- `key`: Categorical or integer key estimate.
- `mode`: Major/minor indicator when available.
- `time_signature`: Estimated meter.

**Validation Rules**

- Bounded Spotify audio features must fall within documented ranges before use.
- Invalid, missing, or out-of-range values must be counted and handled before
  final comparisons.
- Categorical features must preserve missing or unknown states where relevant.

## Popularity Target

Represents the outcome used to rank or segment songs.

**Fields**

- `target_name`: Name of the selected target field or derived proxy.
- `target_type`: `direct_score`, `playlist_proxy`, or `artist_repetition_proxy`.
- `target_strength`: `direct`, `proxy`, or `weak_proxy`.
- `target_value`: Numeric value used for ranking or modeling.
- `target_definition`: Plain-language definition suitable for README/report use.
- `source_fields`: Dataset fields used to derive the target.

**Validation Rules**

- The selected target must be defined before feature comparisons or modeling.
- If the target is playlist-derived, all outputs must label it as a proxy.
- If the target uses artist repetition/counts because no direct or
  playlist-derived field is usable, all outputs must label it as a weak proxy.
- Target construction must avoid using audio features as inputs to the target.

## Popularity Segment

Represents grouped popularity labels for comparison.

**Fields**

- `segment_name`: Human-readable label such as `top_10_percent` or
  `remaining_tracks`.
- `segment_rule`: Top 10% by selected target for the primary popular segment;
  all other valid tracks are the comparison segment.
- `track_count`: Number of tracks in the segment.

**Validation Rules**

- Segment thresholds must be documented and reproducible.
- Segment counts must be reported so readers understand group balance.
- Segments must be based only on the selected Popularity Target.
- Final reported segment comparisons must use the full valid dataset after
  documented cleaning/exclusion rules.

## Final Finding

Represents one evidence-backed claim in the final data story.

**Fields**

- `claim`: Plain-language finding.
- `evidence_type`: Statistic, chart, ranked comparison, or model result.
- `artifact_path`: Path to supporting figure/table/notebook section.
- `caveat`: Limitation or alternative explanation.

**Validation Rules**

- Every final finding must have a supporting artifact.
- Claims must avoid causal language unless the analysis design supports it.
