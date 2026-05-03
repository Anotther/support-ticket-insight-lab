import pandas as pd

from ticket_insight.schema import (
    ANALYSIS_COLUMNS,
    RECOMMENDED_COLUMNS,
    REQUIRED_COLUMNS,
    ensure_analysis_columns,
)


def test_required_columns_match_ticket_csv_contract() -> None:
    assert REQUIRED_COLUMNS == (
        "ticket_id",
        "title",
        "description",
        "opened_at",
        "closed_at",
        "priority",
    )


def test_schema_lists_recommended_and_analysis_columns() -> None:
    assert "affected_service" in RECOMMENDED_COLUMNS
    assert ANALYSIS_COLUMNS == (
        "analysis_category",
        "analysis_sentiment",
        "analysis_priority_suggestion",
        "analysis_priority_reason",
        "analysis_summary",
        "analysis_status_type",
        "analysis_ticket_age_days",
        "analysis_resolution_time_days",
        "analysis_sla_risk",
        "analysis_provider",
        "analysis_processed_at",
    )


def test_ensure_analysis_columns_preserves_existing_data() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-1"],
            "analysis_status_type": ["open"],
        }
    )

    result = ensure_analysis_columns(dataframe)

    assert result is not dataframe
    assert result.iloc[0]["ticket_id"] == "INC-1"
    assert result.iloc[0]["analysis_status_type"] == "open"
    for column in ANALYSIS_COLUMNS:
        assert column in result.columns
