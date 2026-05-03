import pandas as pd

from ticket_insight.exporter import dataframe_to_csv_bytes


def test_dataframe_to_csv_bytes_preserves_columns() -> None:
    result = dataframe_to_csv_bytes(pd.DataFrame({"ticket_id": ["INC-1"], "priority": ["high"]}))

    assert result.decode("utf-8") == "ticket_id,priority\nINC-1,high\n"
