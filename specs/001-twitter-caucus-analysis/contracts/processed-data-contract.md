# Processed Data Contract

## `twitter-caucus-118/data/processed/member_tweet_counts.csv`

One row per member of Congress in the selected analysis window.

Required columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `bioguide_id` | string | yes | Unique member identity key. |
| `member_name` | string | yes | Display name used in tables and annotations. |
| `party` | string | yes | Party label from account metadata. |
| `chamber` | string | yes | House or Senate. |
| `state` | string | yes | State or jurisdiction label. |
| `total_tweets` | integer | yes | Sum of matched tweets across all member accounts. |
| `tweets_per_day_in_office` | number | yes | Tweet count normalized by days served in selected window. |
| `account_count` | integer | yes | Number of Twitter accounts collapsed into the member row. |
| `days_in_office` | integer | yes | Service overlap days for the selected window. |

Validation expectations:
- `bioguide_id` is unique.
- `total_tweets`, `account_count`, and `days_in_office` are non-negative.
- Rows are sorted by descending `total_tweets` or include a reproducible rank in
  the notebook calculation.

## `twitter-caucus-118/data/processed/top10_with_legislation.csv`

Top 10 rows by tweet count, joined to manual bill-count values when present.

Required columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `bioguide_id` | string | yes | Unique member identity key. |
| `member_name` | string | yes | Display name. |
| `party` | string | yes | Party label. |
| `chamber` | string | yes | Chamber label. |
| `state` | string | yes | State label. |
| `total_tweets` | integer | yes | Tweet count over the selected window. |
| `tweets_per_day_in_office` | number | yes | Tweet rate over official service overlap. |
| `account_count` | integer | yes | Collapsed account count. |
| `days_in_office` | integer | yes | Service overlap days. |
| `bills_sponsored` | integer | yes | Manual bill sponsorship count for the selected analysis Congress, or 0 placeholder. |
| `bills_enacted` | integer | yes | Manual enacted sponsored bill count for the selected analysis Congress, or 0 placeholder. |

Validation expectations:
- Exactly 10 rows when at least 10 members have matched tweets.
- All top-10 tweet rows are preserved even if manual bill data is missing.
- Missing manual file causes placeholder zeros and a printed lookup list.

## `twitter-caucus-118/data/manual/top10_bill_counts.csv`

Optional user-provided input.

Required columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `bioguide_id` | string | yes | Join key from top-10 output. |
| `member_name` | string | yes | Human-readable verification name. |
| `bills_sponsored` | integer | yes | Congress.gov Legislation Sponsored count for the selected analysis Congress. |
| `bills_enacted` | integer | yes | Congress.gov enacted sponsored-bill count for the selected analysis Congress. |

Validation expectations:
- Extra rows are allowed and ignored unless they match the top 10.
- Non-matching top-10 members remain in output with placeholders or missing-value
  indicators documented by the notebook.
