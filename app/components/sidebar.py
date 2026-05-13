from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from ticket_insight.config import ProviderKeyResolution, resolve_provider_api_key
from ticket_insight.providers import PROVIDER_METADATA, SUPPORTED_PROVIDERS


@dataclass
class SidebarConfig:
    selected_provider: str
    selected_model: str
    key_resolution: ProviderKeyResolution
    use_mock: bool


@dataclass
class FilterConfig:
    date_range: tuple | None
    categorical_filters: dict[str, list]


def render_sidebar_config() -> SidebarConfig:
    if "use_mock" not in st.session_state:
        st.session_state.use_mock = False

    st.sidebar.header("Configurações da API")
    selected_provider = st.sidebar.selectbox(
        "Provedor de IA",
        options=SUPPORTED_PROVIDERS,
        format_func=lambda p: PROVIDER_METADATA[p].label,
    )
    provider_metadata = PROVIDER_METADATA[selected_provider]
    selected_model = st.sidebar.selectbox("Modelo de IA", options=provider_metadata.models)

    env_resolution = resolve_provider_api_key(selected_provider)
    session_api_key = None
    if env_resolution.is_available:
        st.sidebar.success("Chave encontrada nas variaveis de ambiente.")
    else:
        st.sidebar.info("Informe a chave API para continuar.")
        session_api_key = st.sidebar.text_input(
            "Chave API",
            type="password",
            key=f"{selected_provider}_api_key",
            help=f"Configure {provider_metadata.env_var} para evitar digitar a chave manualmente.",
        )
    key_resolution = resolve_provider_api_key(selected_provider, session_api_key=session_api_key)

    st.sidebar.divider()
    st.sidebar.header("Dados de Teste")
    mock_label = "Voltar ao upload" if st.session_state.use_mock else "Usar dados mock"
    if st.sidebar.button(mock_label):
        st.session_state.use_mock = not st.session_state.use_mock
        st.session_state.pop("processed_df", None)
        st.rerun()

    return SidebarConfig(
        selected_provider=selected_provider,
        selected_model=selected_model,
        key_resolution=key_resolution,
        use_mock=st.session_state.use_mock,
    )


def render_sidebar_filters(df: pd.DataFrame) -> FilterConfig:
    st.sidebar.divider()
    st.sidebar.header("Filtros")

    date_range = None
    if "opened_at" in df.columns and not df["opened_at"].dropna().empty:
        opened_at_dt = pd.to_datetime(df["opened_at"], errors="coerce").dropna()
        if not opened_at_dt.empty:
            min_date = opened_at_dt.min().date()
            max_date = opened_at_dt.max().date()
            date_selection = st.sidebar.date_input(
                "Período de Abertura",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )
            if isinstance(date_selection, tuple) and len(date_selection) == 2:
                start_dt = pd.to_datetime(date_selection[0])
                end_dt = pd.to_datetime(date_selection[1]) + pd.Timedelta(days=1, seconds=-1)
                date_range = (start_dt, end_dt)

    categorical_columns = [
        "priority",
        "analysis_status_type",
        "requester_department",
        "affected_service",
        "assigned_team",
        "analysis_category",
        "analysis_sentiment",
        "analysis_sla_risk",
    ]
    categorical_filters: dict[str, list] = {}
    for col in categorical_columns:
        if col in df.columns and not df[col].dropna().empty:
            unique_values = df[col].dropna().unique().tolist()
            try:
                unique_values.sort()
            except TypeError:
                pass
            label = col.replace("_", " ").title()
            categorical_filters[col] = st.sidebar.multiselect(
                label, options=unique_values, default=[]
            )

    return FilterConfig(date_range=date_range, categorical_filters=categorical_filters)
