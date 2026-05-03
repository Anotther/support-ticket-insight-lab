from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import pandas as pd

from ticket_insight.schema import REQUIRED_COLUMNS


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: list[str]
    dataframe: pd.DataFrame | None = None


def validate_tickets(
    dataframe: pd.DataFrame,
    *,
    processing_datetime: datetime | None = None,
) -> ValidationResult:
    """Validate ticket CSV data and calculate open/closed date fields."""
    errors: list[str] = []
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        return ValidationResult(
            is_valid=False,
            errors=[f"Missing required columns: {', '.join(missing_columns)}"],
        )

    processing_timestamp = _as_utc_timestamp(processing_datetime or datetime.now(UTC))
    validated = dataframe.copy()

    opened_values: list[pd.Timestamp] = []
    closed_values: list[pd.Timestamp | pd.NaT] = []
    status_values: list[str] = []
    age_days: list[int | None] = []
    resolution_days: list[int | None] = []

    for index, row in validated.iterrows():
        row_number = index + 2
        opened_at = _parse_required_datetime(row["opened_at"], row_number, "opened_at", errors)
        closed_at = _parse_optional_datetime(row["closed_at"], row_number, "closed_at", errors)

        opened_values.append(opened_at)
        closed_values.append(closed_at)

        if pd.isna(opened_at):
            status_values.append("invalid")
            age_days.append(None)
            resolution_days.append(None)
            continue

        if pd.isna(closed_at):
            status_values.append("open")
            age_days.append(max((processing_timestamp - opened_at).days, 0))
            resolution_days.append(None)
            continue

        if closed_at < opened_at:
            errors.append(f"Row {row_number}: closed_at cannot be before opened_at.")
            status_values.append("invalid")
            age_days.append(None)
            resolution_days.append(None)
            continue

        status_values.append("closed")
        age_days.append(None)
        resolution_days.append((closed_at - opened_at).days)

    if errors:
        return ValidationResult(is_valid=False, errors=errors)

    validated["opened_at"] = opened_values
    validated["closed_at"] = closed_values
    validated["analysis_status_type"] = status_values
    validated["analysis_ticket_age_days"] = pd.Series(age_days, dtype="Int64")
    validated["analysis_resolution_time_days"] = pd.Series(resolution_days, dtype="Int64")

    return ValidationResult(is_valid=True, errors=[], dataframe=validated)


def _parse_required_datetime(
    value: object,
    row_number: int,
    column: str,
    errors: list[str],
) -> pd.Timestamp:
    if _is_empty(value):
        errors.append(f"Row {row_number}: {column} is required.")
        return pd.NaT

    parsed = pd.to_datetime(value, errors="coerce", utc=True)
    if pd.isna(parsed):
        errors.append(f"Row {row_number}: {column} has an invalid date value.")
        return pd.NaT
    return parsed


def _parse_optional_datetime(
    value: object,
    row_number: int,
    column: str,
    errors: list[str],
) -> pd.Timestamp | pd.NaT:
    if _is_empty(value):
        return pd.NaT

    parsed = pd.to_datetime(value, errors="coerce", utc=True)
    if pd.isna(parsed):
        errors.append(f"Row {row_number}: {column} has an invalid date value.")
        return pd.NaT
    return parsed


def _is_empty(value: object) -> bool:
    return pd.isna(value) or (isinstance(value, str) and value.strip() == "")


def _as_utc_timestamp(value: datetime) -> pd.Timestamp:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return pd.Timestamp(value).tz_convert(UTC)
