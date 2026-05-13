from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from theme import (
    COLOR_MAP_CATEGORY,
    COLOR_MAP_PRIORITY,
    COLOR_MAP_SENTIMENT,
    COLOR_MAP_SLA,
    PLOTLY_LAYOUT_DEFAULTS,
)

_ANALYSIS_COLS = [
    "analysis_sentiment",
    "analysis_category",
    "analysis_priority_suggestion",
    "analysis_sla_risk",
]


def render_analysis_charts(df: pd.DataFrame) -> None:
    if not any(col in df.columns and df[col].notna().any() for col in _ANALYSIS_COLS):
        return

    st.subheader("Relatório de Análise")

    col1, col2 = st.columns(2)
    fig = _sentiment_chart(df)
    if fig:
        col1.plotly_chart(fig, use_container_width=True)
    fig = _sla_chart(df)
    if fig:
        col2.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    fig = _priority_chart(df)
    if fig:
        col3.plotly_chart(fig, use_container_width=True)
    fig = _category_chart(df)
    if fig:
        col4.plotly_chart(fig, use_container_width=True)

    _render_period_note(df)


def _sentiment_chart(df: pd.DataFrame) -> go.Figure | None:
    col = "analysis_sentiment"
    if col not in df.columns or not df[col].notna().any():
        return None
    counts = df[col].dropna().value_counts().reset_index()
    counts.columns = ["Sentimento", "Quantidade"]
    fig = px.bar(
        counts,
        x="Sentimento",
        y="Quantidade",
        color="Sentimento",
        color_discrete_map=COLOR_MAP_SENTIMENT,
        title="Distribuição de Sentimento",
        text_auto=True,
    )
    fig.update_traces(textposition="outside", textfont_color="#E8EDF4")
    fig.update_layout(showlegend=False, **PLOTLY_LAYOUT_DEFAULTS)
    return fig


def _sla_chart(df: pd.DataFrame) -> go.Figure | None:
    col = "analysis_sla_risk"
    if col not in df.columns or not df[col].notna().any():
        return None
    counts = df[col].dropna().value_counts().reset_index()
    counts.columns = ["Risco SLA", "Quantidade"]
    fig = px.bar(
        counts,
        x="Risco SLA",
        y="Quantidade",
        color="Risco SLA",
        color_discrete_map=COLOR_MAP_SLA,
        title="Distribuição de Risco de SLA",
        text_auto=True,
    )
    fig.update_traces(textposition="outside", textfont_color="#E8EDF4")
    fig.update_layout(showlegend=False, **PLOTLY_LAYOUT_DEFAULTS)
    return fig


def _priority_chart(df: pd.DataFrame) -> go.Figure | None:
    col = "analysis_priority_suggestion"
    if col not in df.columns or not df[col].notna().any():
        return None
    order = ["Baixa", "Media", "Alta", "Critica"]
    counts = df[col].dropna().value_counts().reindex(order).dropna().reset_index()
    counts.columns = ["Prioridade Sugerida", "Quantidade"]
    fig = px.bar(
        counts,
        x="Prioridade Sugerida",
        y="Quantidade",
        color="Prioridade Sugerida",
        color_discrete_map=COLOR_MAP_PRIORITY,
        title="Distribuição de Prioridade Sugerida",
        text_auto=True,
    )
    fig.update_traces(textposition="outside", textfont_color="#E8EDF4")
    fig.update_layout(showlegend=False, **PLOTLY_LAYOUT_DEFAULTS)
    return fig


def _category_chart(df: pd.DataFrame) -> go.Figure | None:
    col = "analysis_category"
    if col not in df.columns or not df[col].notna().any():
        return None
    counts = df[col].dropna().value_counts().head(10).reset_index()
    counts.columns = ["Categoria", "Quantidade"]
    fig = px.bar(
        counts,
        x="Quantidade",
        y="Categoria",
        orientation="h",
        color_discrete_sequence=[COLOR_MAP_CATEGORY],
        title="Top 10 Categorias",
        text_auto=True,
    )
    fig.update_traces(textposition="outside", textfont_color="#E8EDF4")
    fig.update_layout(showlegend=False, **PLOTLY_LAYOUT_DEFAULTS)
    return fig


def _render_period_note(df: pd.DataFrame) -> None:
    if "opened_at" not in df.columns:
        return
    dates = pd.to_datetime(df["opened_at"], errors="coerce").dropna()
    if dates.empty:
        return
    start = dates.min().strftime("%d/%m/%Y")
    end = dates.max().strftime("%d/%m/%Y")
    st.caption(f"Período analisado: {start} — {end}")
