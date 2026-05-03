from __future__ import annotations

from typing import IO

import pandas as pd


def load_csv(source: str | IO[bytes] | IO[str]) -> pd.DataFrame:
    """Load a ticket CSV without substituting fallback data."""
    return pd.read_csv(source)
