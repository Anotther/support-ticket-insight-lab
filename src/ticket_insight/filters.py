from typing import Any

import pandas as pd


def filter_tickets(
    dataframe: pd.DataFrame,
    date_range: tuple[pd.Timestamp, pd.Timestamp] | None = None,
    categorical_filters: dict[str, list[Any]] | None = None,
) -> pd.DataFrame:
    """
    Applies filters to the tickets dataframe.
    """
    if dataframe.empty:
        return dataframe

    filtered = dataframe.copy()

    if categorical_filters:
        for col, values in categorical_filters.items():
            if col in filtered.columns and values:
                filtered = filtered[filtered[col].isin(values)]

    if date_range and "opened_at" in filtered.columns:
        start_date, end_date = date_range
        opened_at_dt = pd.to_datetime(filtered["opened_at"], errors="coerce")

        # Ensure we can compare timezone-aware or naive datetimes properly
        # Usually it's safer to convert everything to UTC
        start_date_utc = pd.to_datetime(start_date, utc=True)
        end_date_utc = pd.to_datetime(end_date, utc=True)
        opened_at_utc = pd.to_datetime(opened_at_dt, utc=True)

        mask = (opened_at_utc >= start_date_utc) & (opened_at_utc <= end_date_utc)
        filtered = filtered[mask]

    return filtered
