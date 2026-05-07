import pandas as pd
import pytest
from ticket_insight.filters import filter_tickets

def test_filter_tickets_categorical():
    df = pd.DataFrame({
        "priority": ["high", "low", "medium", "high"],
        "assigned_team": ["A", "B", "A", "C"]
    })
    
    filters = {"priority": ["high"]}
    result = filter_tickets(df, categorical_filters=filters)
    assert len(result) == 2
    assert all(result["priority"] == "high")

    filters = {"priority": ["high"], "assigned_team": ["A"]}
    result = filter_tickets(df, categorical_filters=filters)
    assert len(result) == 1
    assert result.iloc[0]["priority"] == "high"
    assert result.iloc[0]["assigned_team"] == "A"

def test_filter_tickets_date_range():
    df = pd.DataFrame({
        "opened_at": [
            "2026-04-01T10:00:00Z",
            "2026-04-10T10:00:00Z",
            "2026-04-20T10:00:00Z"
        ]
    })
    
    start_date = pd.to_datetime("2026-04-05T00:00:00Z")
    end_date = pd.to_datetime("2026-04-15T00:00:00Z")
    
    result = filter_tickets(df, date_range=(start_date, end_date))
    assert len(result) == 1
    assert result.iloc[0]["opened_at"] == "2026-04-10T10:00:00Z"

def test_filter_tickets_empty_filters():
    df = pd.DataFrame({"priority": ["high", "low"]})
    result = filter_tickets(df, categorical_filters={"priority": []})
    assert len(result) == 2

def test_filter_tickets_missing_column():
    df = pd.DataFrame({"priority": ["high", "low"]})
    result = filter_tickets(df, categorical_filters={"missing_col": ["val"]})
    assert len(result) == 2

def test_filter_tickets_empty_dataframe():
    df = pd.DataFrame({"priority": []})
    result = filter_tickets(df, categorical_filters={"priority": ["high"]})
    assert len(result) == 0
