from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

import pandas as pd

from ticket_insight.schema import ensure_analysis_columns


class AnalysisPipelineNotConfiguredError(RuntimeError):
    """Raised when analysis is requested before a provider client is configured."""


@dataclass(frozen=True)
class TicketAnalysisResult:
    category: str
    sentiment: str
    priority_suggestion: str
    priority_reason: str
    summary: str
    sla_risk: str


class TicketAnalyzer(Protocol):
    def analyze(self, ticket: Mapping[str, object], provider: str) -> TicketAnalysisResult:
        """Analyze a single ticket with the selected provider."""


def analyze_tickets(
    dataframe: pd.DataFrame,
    *,
    analyzer: TicketAnalyzer | None = None,
    provider: str | None = None,
    processed_at: datetime | None = None,
) -> pd.DataFrame:
    if analyzer is None or provider is None:
        message = "Analysis provider clients are not implemented yet."
        raise AnalysisPipelineNotConfiguredError(message)

    enriched = ensure_analysis_columns(dataframe)
    processed_at_value = _format_processed_at(processed_at or datetime.now(UTC))

    categories: list[str] = []
    sentiments: list[str] = []
    priority_suggestions: list[str] = []
    priority_reasons: list[str] = []
    summaries: list[str] = []
    sla_risks: list[str] = []

    for ticket in enriched.to_dict(orient="records"):
        result = analyzer.analyze(ticket=ticket, provider=provider)
        categories.append(result.category)
        sentiments.append(result.sentiment)
        priority_suggestions.append(result.priority_suggestion)
        priority_reasons.append(result.priority_reason)
        summaries.append(result.summary)
        sla_risks.append(result.sla_risk)

    enriched["analysis_category"] = categories
    enriched["analysis_sentiment"] = sentiments
    enriched["analysis_priority_suggestion"] = priority_suggestions
    enriched["analysis_priority_reason"] = priority_reasons
    enriched["analysis_summary"] = summaries
    enriched["analysis_sla_risk"] = sla_risks
    enriched["analysis_provider"] = provider
    enriched["analysis_processed_at"] = processed_at_value

    return enriched


def _format_processed_at(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()
