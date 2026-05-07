import pandas as pd

from ticket_insight.metrics import get_kpis


def test_get_kpis_empty() -> None:
    empty_df = pd.DataFrame()
    kpis = get_kpis(empty_df)
    assert kpis == {
        "total": 0,
        "open": 0,
        "closed": 0,
        "high_priority": 0,
        "avg_age_days": 0.0,
        "avg_resolution_days": 0.0,
    }


def test_get_kpis_calculated() -> None:
    df = pd.DataFrame(
        {
            "ticket_id": ["INC-1", "INC-2", "INC-3"],
            "priority": ["high", "low", "critical"],
            "analysis_status_type": ["open", "closed", "closed"],
            "analysis_ticket_age_days": pd.Series([5, None, None], dtype="Int64"),
            "analysis_resolution_time_days": pd.Series([None, 2, 4], dtype="Int64"),
        }
    )

    kpis = get_kpis(df)
    assert kpis["total"] == 3
    assert kpis["open"] == 1
    assert kpis["closed"] == 2
    assert kpis["high_priority"] == 2
    assert kpis["avg_age_days"] == 5.0
    assert kpis["avg_resolution_days"] == 3.0
