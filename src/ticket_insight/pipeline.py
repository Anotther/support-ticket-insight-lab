from __future__ import annotations

import pandas as pd


class AnalysisPipelineNotConfiguredError(RuntimeError):
    """Raised when analysis is requested before a provider client is configured."""


def analyze_tickets(_dataframe: pd.DataFrame) -> pd.DataFrame:
    raise AnalysisPipelineNotConfiguredError("Analysis provider clients are not implemented yet.")
