
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. Define file paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW = PROJECT_ROOT / "data/raw/council_voting_records.csv"
PROCESSED = PROJECT_ROOT / "data/processed/council_voting_clean.parquet"
REVIEW = PROJECT_ROOT / "data/processed/votes_to_review.csv"


def clean_data(df):
    """Clean council voting records and flag potential issues."""

    df = df.copy()

    # --------------------------------------------------
    # 2. Convert date columns
    # --------------------------------------------------

    df["vote_date"] = pd.to_datetime(
        df["vote_date"],
        errors="raise"
    )

    df["vote_start_date_time"] = pd.to_datetime(
        df["vote_start_date_time"],
        errors="raise",
        utc=True
    )

    # --------------------------------------------------
    # 3. Validate identifiers
    # --------------------------------------------------

    assert df["vote_detail_id"].is_unique, (
        "Duplicate vote_detail_id values found."
    )

    # --------------------------------------------------
    # 4. Resolve redundant voting records
    # --------------------------------------------------

    # Count unique voting statuses for each councillor per vote
    status_counts = (
        df.groupby(["vote_number", "council_member"])["vote"]
        .transform("nunique")
    )

    # Flag combinations with conflicting voting statuses
    df["conflicting_vote_flag"] = status_counts > 1

    # Remove repeated records only when their voting statuses agree.
    # Preserve all records with conflicting statuses.
    redundant = (
        ~df["conflicting_vote_flag"]
        & df.duplicated(
            subset=["vote_number", "council_member"],
            keep="first"
        )
    )

    print("Redundant records removed:", redundant.sum())

    df = df.loc[~redundant].copy()

    # --------------------------------------------------
    # 5. Flag date inconsistencies
    # --------------------------------------------------

    # Convert UTC timestamps to Vancouver local dates
    local_dates = (
        df["vote_start_date_time"]
        .dt.tz_convert("America/Vancouver")
        .dt.date
    )

    df["date_mismatch_flag"] = (
        local_dates != df["vote_date"].dt.date
    )

    # --------------------------------------------------
    # 6. Flag potentially inconsistent decisions
    # --------------------------------------------------

    # Count voting statuses for each council vote
    vote_counts = (
        df.groupby(["vote_number", "vote"])
        .size()
        .unstack(fill_value=0)
    )

    # Ensure both categories are available
    vote_counts = vote_counts.reindex(
        columns=["In Favour", "In Opposition"],
        fill_value=0
    )

    # Get the recorded decision for each vote
    decisions = (
        df.groupby("vote_number")["decision"].first()
    )

    # Unanimous decisions with opposition votes
    unanimous_conflict = (
        (decisions == "Carried Unanimously")
        & (vote_counts["In Opposition"] > 0)
    )

    # Lost decisions with votes in favour
    # but no votes in opposition
    lost_conflict = (
        (decisions == "Lost")
        & (vote_counts["In Favour"] > 0)
        & (vote_counts["In Opposition"] == 0)
    )

    suspicious_votes = decisions.index[
        unanimous_conflict | lost_conflict
    ]

    df["decision_anomaly_flag"] = (
        df["vote_number"].isin(suspicious_votes)
    )

    # --------------------------------------------------
    # 7. Flag votes with unusually low coverage
    # --------------------------------------------------

    # Count unique members represented in each vote
    unique_members = (
        df.groupby("vote_number")["council_member"]
        .transform("nunique")
    )

    df["low_coverage_flag"] = unique_members < 11

    # --------------------------------------------------
    # 8. Validate cleaned dataset
    # --------------------------------------------------

    assert df["vote_detail_id"].is_unique, (
        "Duplicate vote detail IDs remain."
    )

    assert df["vote_date"].notna().all(), (
        "Missing or invalid vote dates found."
    )

    assert df["vote_start_date_time"].notna().all(), (
        "Missing or invalid timestamps found."
    )

    # Remaining repeated councillor-vote records
    # must belong to flagged conflicting combinations
    remaining_duplicates = df.duplicated(
        subset=["vote_number", "council_member"],
        keep=False
    )

    assert df.loc[
        remaining_duplicates, "conflicting_vote_flag"
    ].all(), (
        "Unexpected repeated councillor-vote records remain."
    )

    return df


def main():
    # --------------------------------------------------
    # 9. Load the original dataset
    # --------------------------------------------------

    df = pd.read_csv(RAW, sep=";")

    print("Original dataset shape:", df.shape)

    # --------------------------------------------------
    # 10. Clean the dataset
    # --------------------------------------------------

    cleaned = clean_data(df)

    print("Cleaned dataset shape:", cleaned.shape)

    # --------------------------------------------------
    # 11. Extract records requiring review
    # --------------------------------------------------

    flag_columns = [
        "conflicting_vote_flag",
        "date_mismatch_flag",
        "decision_anomaly_flag",
        "low_coverage_flag"
    ]

    review_records = cleaned.loc[
        cleaned[flag_columns].any(axis=1)
    ].copy()

    # --------------------------------------------------
    # 12. Save processed datasets
    # --------------------------------------------------

    PROCESSED.parent.mkdir(parents=True, exist_ok=True)

    # Parquet preserves datetime, integer, and Boolean types
    cleaned.to_parquet(PROCESSED, index=False)

    # CSV is convenient for manually reviewing flagged records
    review_records.to_csv(REVIEW, index=False)

    # --------------------------------------------------
    # 13. Print cleaning summary
    # --------------------------------------------------

    print("\n--- Cleaning Summary ---")

    print("Original records:", len(df))
    print("Cleaned records:", len(cleaned))
    print("Records removed:", len(df) - len(cleaned))

    print(
        "Conflicting councillor-vote combinations:",
        cleaned.loc[
            cleaned["conflicting_vote_flag"],
            ["vote_number", "council_member"]
        ].drop_duplicates().shape[0]
    )

    print(
        "Date mismatch records:",
        cleaned["date_mismatch_flag"].sum()
    )

    print(
        "Potentially inconsistent decisions:",
        cleaned.loc[
            cleaned["decision_anomaly_flag"],
            "vote_number"
        ].nunique()
    )

    print(
        "Votes with fewer than 11 members:",
        cleaned.loc[
            cleaned["low_coverage_flag"],
            "vote_number"
        ].nunique()
    )

    print("\nCleaned data saved to:", PROCESSED)
    print("Review records saved to:", REVIEW)


if __name__ == "__main__":
    main()
