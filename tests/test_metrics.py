import pandas as pd

from ticket_insight.metrics import count_tickets


def test_count_tickets() -> None:
    assert count_tickets(pd.DataFrame({"ticket_id": ["INC-1", "INC-2"]})) == 2
