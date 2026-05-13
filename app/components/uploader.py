from __future__ import annotations

import streamlit as st

from ticket_insight.schema import RECOMMENDED_COLUMNS, REQUIRED_COLUMNS


def render_upload_header() -> None:
    st.subheader("Enviar CSV")
    st.write("Envie um arquivo CSV com as colunas obrigatorias abaixo.")
    st.code(", ".join(REQUIRED_COLUMNS), language="text")
    with st.expander("Colunas recomendadas"):
        st.write(", ".join(RECOMMENDED_COLUMNS))


def render_file_widget(*, use_mock: bool):
    return st.file_uploader(
        "Arquivo CSV de tickets",
        type=["csv"],
        disabled=use_mock,
        on_change=_clear_processed_df,
    )


def _clear_processed_df() -> None:
    if "processed_df" in st.session_state:
        del st.session_state["processed_df"]
