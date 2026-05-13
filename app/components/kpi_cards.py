from __future__ import annotations

import pandas as pd
import streamlit as st

from ticket_insight.metrics import get_kpis


def render_kpi_cards(df: pd.DataFrame) -> None:
    st.subheader("Indicadores Principais")
    kpis = get_kpis(df)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total de Tickets", kpis["total"])
    col2.metric("Abertos", kpis["open"])
    col3.metric("Fechados", kpis["closed"])
    col4.metric("Prioridade Alta/Crítica", kpis["high_priority"])
    col5.metric("Idade Média (dias)", kpis["avg_age_days"])
    col6.metric("Tempo Médio de Resolução", kpis["avg_resolution_days"])
