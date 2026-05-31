# Data Model: 118th Congress Twitter Caucus Analysis

## Tweet Day

**Description**: One daily archive file from the Congressional tweets source.

**Fields**:
- `date`: Calendar date for the archive file, formatted `YYYY-MM-DD`.
- `status`: One of `populated`, `missing`, `download_failed`, or
  `parse_failed`.
- `tweet_count`: Number of tweet objects parsed from the file.
- `cache_path`: Local path under `data/raw/tweets/`.

**Validation rules**:
- A populated file must parse as a JSON array.
- Spot-check tweet counts below 1,000 trigger degraded-coverage warning.
- Expected date windows use inclusive start and exclusive end dates.

## Tweet Record

**Description**: One tweet object inside a daily archive.

**Fields**:
- `id`: Tweet identifier.
- `screen_name`: Twitter account screen name from the archive.
- `user_id`: Twitter user identifier when present.
- `time`: Tweet timestamp.
- `text`: Tweet text.
- `source`: Posting source.
- `link`: Tweet URL.
- `date`: Archive date inherited from the Tweet Day.

**Validation rules**:
- Records without a screen name cannot be joined to account metadata and are
  excluded from member totals.
- Tweet text is not analyzed for sentiment or topic.

## Twitter Account

**Description**: Historical account metadata used to identify member accounts
and attach member attributes.

**Fields**:
- `screen_name`: Current or historical Twitter handle used for joining.
- `user_id`: Twitter user identifier when available.
- `account_type`: Account category used to keep member accounts and exclude
  non-member accounts.
- `bioguide_id`: Stable member identity key.
- `member_name`: Display name for the member.
- `party`: Party label.
- `chamber`: House or Senate.
- `state`: State or jurisdiction label.
- `service_start`: Member service start date when reliable.
- `service_end`: Member service end date when reliable.

**Validation rules**:
- Only records classified as individual member accounts are retained for member
  aggregation.
- Non-member account types, including committee, leadership, and party accounts,
  are excluded.
- Multiple account rows may share one `bioguide_id`.

## Official Service-Date Lookup

**Description**: Supplemental official service timing keyed by member identity,
used when account metadata lacks reliable dates.

**Fields**:
- `bioguide_id`: Stable member identity key.
- `official_start_date`: Official start date of service relevant to the selected
  Congress.
- `official_end_date`: Official end date of service relevant to the selected
  Congress, or selected window end for still-serving members.
- `source_note`: Short note identifying the lookup source or method.

**Validation rules**:
- Lookup is used only when account metadata dates are missing or unreliable.
- If official lookup is unavailable, selected Congress window boundaries may be
  used and the limitation must be documented.

## Member of Congress

**Description**: Person-level unit of analysis after collapsing all member
accounts with the same `bioguide_id`.

**Fields**:
- `bioguide_id`: Unique row key.
- `member_name`: Member display name.
- `party`: Party label.
- `chamber`: Chamber label.
- `state`: State label.
- `total_tweets`: Sum of tweets from all matched accounts during days in scope.
- `tweets_per_day_in_office`: `total_tweets / days_in_office`.
- `account_count`: Number of member accounts collapsed into the row.
- `days_in_office`: Number of days the member served during the selected window.

**Validation rules**:
- `bioguide_id` must be unique in `member_tweet_counts.csv`.
- `days_in_office` is the overlap between the selected analysis window and the
  member service window.
- `tweets_per_day_in_office` must be null or documented only when
  `days_in_office` cannot be computed.

## Coverage Verification Summary

**Description**: Pre-analysis quality record for the selected archive window.

**Fields**:
- `requested_window`: Initial requested window.
- `selected_window`: Final analysis window after fallback checks.
- `expected_days`: Count of expected daily archive files.
- `populated_days`: Count of successfully parsed populated days.
- `missing_days`: Count of unavailable or invalid days.
- `coverage_share`: `populated_days / expected_days`.
- `spot_check_counts`: Date-to-tweet-count mapping for required spot checks.
- `degraded_coverage`: Boolean warning flag.
- `severe_degradation`: Boolean fallback flag.
- `warning_text`: Human-readable caveat printed before analysis.

**Validation rules**:
- Coverage verification must run before member aggregation.
- More than 10% missing days or any required spot-check below 1,000 tweets sets
  `degraded_coverage = true`.
- Fewer than half of expected 118th Congress days populated sets
  `severe_degradation = true` and selects the 117th Congress fallback window.

## Manual Bill Count

**Description**: User-provided supplemental legislative activity counts for the
top 10 tweet-ranked members in the selected analysis Congress.

**Fields**:
- `bioguide_id`: Primary join key.
- `member_name`: Member name used for human verification.
- `bills_sponsored`: Count from the Congress.gov member page for the selected
  analysis Congress, using the Legislation Sponsored tab.
- `bills_enacted`: Count of sponsored bills enacted for the same selected-Congress
  filter.

**Validation rules**:
- Missing file is allowed; placeholder zeros are used and lookup prompts are
  printed with the selected Congress window and Congress.gov lookup method.
- Top-10 output preserves all top-10 tweet rows even if bill-count rows are
  missing.

## Distribution Finding

**Description**: Ranked distribution and cumulative concentration metrics.

**Fields**:
- `rank`: Member rank by descending `total_tweets`.
- `cumulative_tweets`: Running tweet total by rank.
- `cumulative_share`: Share of all member tweets through that rank.
- `top_n_50_share`: Smallest rank where `cumulative_share >= 0.50`.
- `member_share_for_50pct`: `top_n_50_share / total_member_count`.

**Validation rules**:
- Cumulative-share panel must include ranks 1 through 100 or all members when
  fewer than 100 exist.
- Headline concentration number must be traceable to this calculation.
