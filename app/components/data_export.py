from __future__ import annotations

import pandas as pd
import streamlit as st

from ticket_insight.exporter import dataframe_to_csv_bytes
from ticket_insight.schema import ensure_analysis_columns


def render_data_table(df: pd.DataFrame) -> None:
    st.subheader("Dados")
    st.dataframe(df, use_container_width=True)


def render_export_buttons(full_df: pd.DataFrame, filtered_df: pd.DataFrame) -> None:
    st.subheader("Exportar")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Baixar CSV Completo",
            data=dataframe_to_csv_bytes(ensure_analysis_columns(full_df)),
            file_name="support_tickets_full.csv",
            mime="text/csv",
        )
    with col2:
        st.download_button(
            label="Baixar CSV Filtrado",
            data=dataframe_to_csv_bytes(ensure_analysis_columns(filtered_df)),
            file_name="support_tickets_filtered.csv",
            mime="text/csv",
            disabled=filtered_df.empty,
        )
