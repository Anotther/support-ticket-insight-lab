from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS: tuple[str, ...] = (
    "ticket_id",
    "title",
    "description",
    "opened_at",
    "closed_at",
    "priority",
)

RECOMMENDED_COLUMNS: tuple[str, ...] = (
    "status",
    "requester_department",
    "requester_location",
    "affected_service",
    "asset_id",
    "assigned_team",
    "assignee",
    "channel",
    "impact",
    "urgency",
    "resolution_notes",
)

ANALYSIS_COLUMNS: tuple[str, ...] = (
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


def ensure_analysis_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    enriched = dataframe.copy()
    for column in ANALYSIS_COLUMNS:
        if column not in enriched.columns:
            enriched[column] = pd.NA
    return enriched
