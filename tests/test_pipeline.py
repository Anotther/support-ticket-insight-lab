import pandas as pd
import pytest

from ticket_insight.pipeline import AnalysisPipelineNotConfiguredError, analyze_tickets


def test_pipeline_does_not_return_mock_analysis() -> None:
    with pytest.raises(AnalysisPipelineNotConfiguredError):
        analyze_tickets(pd.DataFrame())
