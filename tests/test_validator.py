from datetime import UTC, datetime

import pandas as pd

from ticket_insight.validator import validate_tickets


def test_validator_requires_all_required_columns() -> None:
    dataframe = pd.DataFrame({"ticket_id": ["INC-1"]})

    result = validate_tickets(dataframe)

    assert not result.is_valid
    assert result.errors == [
        "Missing required columns: title, description, opened_at, closed_at, priority"
    ]


def test_validator_handles_open_tickets_with_empty_closed_at() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-1"],
            "title": ["VPN fora"],
            "description": ["Usuario sem acesso a VPN"],
            "opened_at": ["2026-05-01"],
            "closed_at": [""],
            "priority": ["high"],
        }
    )

    result = validate_tickets(
        dataframe,
        processing_datetime=datetime(2026, 5, 3, tzinfo=UTC),
    )

    assert result.is_valid
    assert result.dataframe is not None
    row = result.dataframe.iloc[0]
    assert row["analysis_status_type"] == "open"
    assert row["analysis_ticket_age_days"] == 2
    assert pd.isna(row["analysis_resolution_time_days"])


def test_validator_handles_closed_tickets_with_resolution_time() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-2"],
            "title": ["Impressora indisponivel"],
            "description": ["Fila de impressao travada"],
            "opened_at": ["2026-05-01T10:00:00Z"],
            "closed_at": ["2026-05-02T12:00:00Z"],
            "priority": ["medium"],
        }
    )

    result = validate_tickets(dataframe)

    assert result.is_valid
    assert result.dataframe is not None
    row = result.dataframe.iloc[0]
    assert row["analysis_status_type"] == "closed"
    assert pd.isna(row["analysis_ticket_age_days"])
    assert row["analysis_resolution_time_days"] == 1


def test_validator_rejects_invalid_dates() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-3"],
            "title": ["Wi-Fi lento"],
            "description": ["Sinal instavel no escritorio"],
            "opened_at": ["not-a-date"],
            "closed_at": [""],
            "priority": ["low"],
        }
    )

    result = validate_tickets(dataframe)

    assert not result.is_valid
    assert result.errors == ["Row 2: opened_at has an invalid date value."]


def test_validator_rejects_closed_at_before_opened_at() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-4"],
            "title": ["Conta bloqueada"],
            "description": ["Usuario bloqueado no MFA"],
            "opened_at": ["2026-05-03"],
            "closed_at": ["2026-05-02"],
            "priority": ["high"],
        }
    )

    result = validate_tickets(dataframe)

    assert not result.is_valid
    assert result.errors == ["Row 2: closed_at cannot be before opened_at."]
