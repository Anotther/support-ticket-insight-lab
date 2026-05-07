from __future__ import annotations

from typing import Any

import pandas as pd


def get_kpis(dataframe: pd.DataFrame) -> dict[str, Any]:
    """Calculate key performance indicators from the validated tickets dataframe."""
    total_tickets = len(dataframe)
    if total_tickets == 0:
        return {
            "total": 0,
            "open": 0,
            "closed": 0,
            "high_priority": 0,
            "avg_age_days": 0.0,
            "avg_resolution_days": 0.0,
        }

    # Open vs Closed
    # Requires analysis_status_type to be populated
    if "analysis_status_type" in dataframe.columns:
        open_count = int((dataframe["analysis_status_type"] == "open").sum())
        closed_count = int((dataframe["analysis_status_type"] == "closed").sum())
    else:
        open_count = 0
        closed_count = 0

    # High/Critical priority
    if "priority" in dataframe.columns:
        high_priority = int(dataframe["priority"].str.lower().isin(["high", "critical"]).sum())
    else:
        high_priority = 0

    # Average Age (for open tickets)
    if "analysis_ticket_age_days" in dataframe.columns:
        # FillNA with 0 for calculation if needed, but mean() handles NA by skipping
        avg_age = float(dataframe["analysis_ticket_age_days"].mean())
        if pd.isna(avg_age):
            avg_age = 0.0
    else:
        avg_age = 0.0

    # Average Resolution Time (for closed tickets)
    if "analysis_resolution_time_days" in dataframe.columns:
        avg_res = float(dataframe["analysis_resolution_time_days"].mean())
        if pd.isna(avg_res):
            avg_res = 0.0
    else:
        avg_res = 0.0

    return {
        "total": total_tickets,
        "open": open_count,
        "closed": closed_count,
        "high_priority": high_priority,
        "avg_age_days": round(avg_age, 1),
        "avg_resolution_days": round(avg_res, 1),
    }
