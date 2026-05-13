from collections.abc import Mapping
from datetime import UTC, datetime

import pandas as pd
import pytest

from ticket_insight.pipeline import (
    AnalysisPipelineNotConfiguredError,
    TicketAnalysisResult,
    analyze_tickets,
)
from ticket_insight.schema import ANALYSIS_COLUMNS


class FakeAnalyzer:
    def analyze(self, ticket: Mapping[str, object], provider: str) -> TicketAnalysisResult:
        assert provider == "openai"
        return TicketAnalysisResult(
            category=f"category:{ticket['ticket_id']}",
            sentiment="negative",
            priority_suggestion="high",
            priority_reason="Ticket mentions service impact.",
            summary=f"Summary for {ticket['ticket_id']}",
            sla_risk="at_risk",
        )


class CapturingAnalyzer:
    def __init__(self) -> None:
        self.tickets: list[Mapping[str, object]] = []

    def analyze(self, ticket: Mapping[str, object], provider: str) -> TicketAnalysisResult:
        assert provider == "openai"
        self.tickets.append(dict(ticket))
        return TicketAnalysisResult(
            category="Infraestrutura",
            sentiment="Neutro",
            priority_suggestion="Alta",
            priority_reason="Ticket reavaliado com impacto no servico.",
            summary="Resumo atualizado do ticket.",
            sla_risk="Medio",
        )


def test_pipeline_does_not_return_mock_analysis() -> None:
    with pytest.raises(AnalysisPipelineNotConfiguredError):
        analyze_tickets(pd.DataFrame())


def test_pipeline_requires_provider_when_analyzer_is_configured() -> None:
    with pytest.raises(AnalysisPipelineNotConfiguredError):
        analyze_tickets(pd.DataFrame(), analyzer=FakeAnalyzer())


def test_pipeline_preserves_original_columns_and_adds_analysis_schema() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-1"],
            "title": ["VPN fora"],
            "description": ["Usuario sem acesso a VPN"],
            "opened_at": ["2026-05-01"],
            "closed_at": [""],
            "priority": ["high"],
            "analysis_status_type": ["open"],
            "analysis_ticket_age_days": [2],
            "analysis_resolution_time_days": [pd.NA],
        }
    )

    result = analyze_tickets(
        dataframe,
        analyzer=FakeAnalyzer(),
        provider="openai",
        processed_at=datetime(2026, 5, 3, 12, 30, tzinfo=UTC),
    )

    for column in dataframe.columns:
        assert column in result.columns
    for column in ANALYSIS_COLUMNS:
        assert column in result.columns

    row = result.iloc[0]
    assert row["ticket_id"] == "INC-1"
    assert row["title"] == "VPN fora"
    assert row["analysis_status_type"] == "open"
    assert row["analysis_ticket_age_days"] == 2
    assert pd.isna(row["analysis_resolution_time_days"])
    assert row["analysis_category"] == "category:INC-1"
    assert row["analysis_sentiment"] == "negative"
    assert row["analysis_priority_suggestion"] == "high"
    assert row["analysis_priority_reason"] == "Ticket mentions service impact."
    assert row["analysis_summary"] == "Summary for INC-1"
    assert row["analysis_sla_risk"] == "at_risk"
    assert row["analysis_provider"] == "openai"
    assert row["analysis_processed_at"] == "2026-05-03T12:30:00+00:00"


def test_pipeline_processed_at_naive_datetime_is_serialized_as_utc() -> None:
    dataframe = pd.DataFrame({"ticket_id": ["INC-2"]})

    result = analyze_tickets(
        dataframe,
        analyzer=FakeAnalyzer(),
        provider="openai",
        processed_at=datetime(2026, 5, 3, 12, 30),
    )

    assert result.iloc[0]["analysis_processed_at"] == "2026-05-03T12:30:00+00:00"


def test_pipeline_does_not_send_generated_analysis_fields_to_analyzer() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["INC-3"],
            "title": ["Wi-Fi instavel"],
            "description": ["Quedas frequentes na rede sem fio"],
            "opened_at": ["2026-05-01"],
            "closed_at": [""],
            "priority": ["medium"],
            "requester_department": ["Financeiro"],
            "analysis_status_type": ["open"],
            "analysis_ticket_age_days": [3],
            "analysis_resolution_time_days": [pd.NA],
            "analysis_category": ["Rede antiga"],
            "analysis_sentiment": ["Negativo"],
            "analysis_priority_suggestion": ["Critica"],
            "analysis_priority_reason": ["Resultado anterior"],
            "analysis_summary": ["Resumo anterior"],
            "analysis_sla_risk": ["Alto"],
            "analysis_provider": ["openai"],
            "analysis_processed_at": ["2026-05-02T12:30:00+00:00"],
        }
    )
    analyzer = CapturingAnalyzer()

    result = analyze_tickets(
        dataframe,
        analyzer=analyzer,
        provider="openai",
        processed_at=datetime(2026, 5, 3, 12, 30, tzinfo=UTC),
    )

    assert len(analyzer.tickets) == 1
    captured_ticket = analyzer.tickets[0]
    assert captured_ticket.keys() == {
        "ticket_id",
        "title",
        "description",
        "opened_at",
        "closed_at",
        "priority",
        "requester_department",
        "analysis_status_type",
        "analysis_ticket_age_days",
        "analysis_resolution_time_days",
    }
    assert captured_ticket["ticket_id"] == "INC-3"
    assert captured_ticket["title"] == "Wi-Fi instavel"
    assert captured_ticket["description"] == "Quedas frequentes na rede sem fio"
    assert captured_ticket["opened_at"] == "2026-05-01"
    assert captured_ticket["closed_at"] == ""
    assert captured_ticket["priority"] == "medium"
    assert captured_ticket["requester_department"] == "Financeiro"
    assert captured_ticket["analysis_status_type"] == "open"
    assert captured_ticket["analysis_ticket_age_days"] == 3
    assert pd.isna(captured_ticket["analysis_resolution_time_days"])

    excluded_fields = {
        "analysis_category",
        "analysis_sentiment",
        "analysis_priority_suggestion",
        "analysis_priority_reason",
        "analysis_summary",
        "analysis_sla_risk",
        "analysis_provider",
        "analysis_processed_at",
    }
    assert excluded_fields.isdisjoint(captured_ticket)

    for column in ANALYSIS_COLUMNS:
        assert column in result.columns

    row = result.iloc[0]
    assert row["analysis_category"] == "Infraestrutura"
    assert row["analysis_sentiment"] == "Neutro"
    assert row["analysis_priority_suggestion"] == "Alta"
    assert row["analysis_priority_reason"] == "Ticket reavaliado com impacto no servico."
    assert row["analysis_summary"] == "Resumo atualizado do ticket."
    assert row["analysis_sla_risk"] == "Medio"
    assert row["analysis_provider"] == "openai"
    assert row["analysis_processed_at"] == "2026-05-03T12:30:00+00:00"
