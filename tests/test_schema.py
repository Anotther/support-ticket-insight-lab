from ticket_insight.schema import ANALYSIS_COLUMNS, RECOMMENDED_COLUMNS, REQUIRED_COLUMNS


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
    assert "analysis_status_type" in ANALYSIS_COLUMNS
    assert "analysis_resolution_time_days" in ANALYSIS_COLUMNS
