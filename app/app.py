from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
for _p in (str(ROOT / "src"), str(APP_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import theme  # noqa: E402
from components.charts import render_analysis_charts  # noqa: E402
from components.data_export import render_data_table, render_export_buttons  # noqa: E402
from components.kpi_cards import render_kpi_cards  # noqa: E402
from components.sidebar import (  # noqa: E402
    SidebarConfig,
    render_sidebar_config,
    render_sidebar_filters,
)
from components.uploader import render_file_widget, render_upload_header  # noqa: E402

from ticket_insight.analyzer import LLMTicketAnalyzer  # noqa: E402
from ticket_insight.filters import filter_tickets  # noqa: E402
from ticket_insight.loader import load_csv  # noqa: E402
from ticket_insight.pipeline import analyze_tickets  # noqa: E402
from ticket_insight.validator import validate_tickets  # noqa: E402


def main() -> None:
    st.set_page_config(
        page_title="Support Ticket Insight Lab",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    theme.apply_global_css()
    st.title("Support Ticket Insight Lab")
    st.caption("Analise tickets de infraestrutura a partir de um CSV enviado pelo usuario.")

    render_upload_header()
    sidebar_cfg = render_sidebar_config()

    df = _load_data(sidebar_cfg)
    if df is None:
        return

    result = validate_tickets(df)
    if not result.is_valid:
        st.error("O CSV contem erros de validacao.")
        st.dataframe(pd.DataFrame({"erro": result.errors}), use_container_width=True)
        return

    st.success("CSV validado com sucesso.")
    df = result.dataframe.copy()

    if "processed_df" in st.session_state:
        df = st.session_state.processed_df
        if st.session_state.get("just_processed"):
            st.success(f"Todos os {len(df)} tickets foram processados com sucesso.")
            del st.session_state["just_processed"]

    filter_cfg = render_sidebar_filters(df)
    filtered_df = filter_tickets(
        df,
        date_range=filter_cfg.date_range,
        categorical_filters=filter_cfg.categorical_filters,
    )

    render_kpi_cards(filtered_df)
    render_analysis_charts(filtered_df)
    render_data_table(filtered_df)
    render_export_buttons(full_df=df, filtered_df=filtered_df)
    _render_process_button(df, sidebar_cfg)


def _load_data(sidebar_cfg: SidebarConfig) -> pd.DataFrame | None:
    uploaded_file = render_file_widget(use_mock=sidebar_cfg.use_mock)
    if sidebar_cfg.use_mock:
        try:
            return load_csv(ROOT / "support_tickets_mock.csv")
        except FileNotFoundError:
            st.error("Arquivo de mock não encontrado.")
            return None
    if uploaded_file is not None:
        try:
            return load_csv(uploaded_file)
        except pd.errors.ParserError as exc:
            st.error(f"Nao foi possivel ler o CSV: {exc}")
            return None
    st.info("Envie um CSV ou ative os dados mock no sidebar para iniciar a validacao.")
    return None


def _render_process_button(df: pd.DataFrame, sidebar_cfg: SidebarConfig) -> None:
    if not st.button("Processar tickets"):
        return

    if not sidebar_cfg.key_resolution.is_available:
        st.error(
            "Nao foi possivel processar: informe uma chave API ou configure a "
            "variavel de ambiente do provedor selecionado."
        )
        return

    analyzer = LLMTicketAnalyzer(
        api_key=sidebar_cfg.key_resolution.api_key,
        model=sidebar_cfg.selected_model,
    )
    total_tickets = len(df)
    progress_bar = st.progress(0, text=f"Analisando ticket 0 de {total_tickets}...")
    status_placeholder = st.empty()

    def update_progress(current: int, total: int) -> None:
        progress_bar.progress(current / total, text=f"Analisando ticket {current} de {total}...")

    try:
        analyzed_df = analyze_tickets(
            dataframe=df,
            analyzer=analyzer,
            provider=sidebar_cfg.selected_provider,
            on_progress=update_progress,
        )
        progress_bar.progress(1.0, text="Análise concluída!")
        st.session_state.processed_df = analyzed_df
        st.session_state.just_processed = True
        st.rerun()
    except Exception as e:
        progress_bar.empty()
        status_placeholder.error(f"Erro durante a análise: {e}")


if __name__ == "__main__":
    main()
