from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ticket_insight.config import resolve_provider_api_key  # noqa: E402
from ticket_insight.filters import filter_tickets  # noqa: E402
from ticket_insight.loader import load_csv  # noqa: E402
from ticket_insight.metrics import get_kpis  # noqa: E402
from ticket_insight.providers import PROVIDER_METADATA, SUPPORTED_PROVIDERS  # noqa: E402
from ticket_insight.schema import RECOMMENDED_COLUMNS, REQUIRED_COLUMNS  # noqa: E402
from ticket_insight.validator import validate_tickets  # noqa: E402


def main() -> None:
    st.set_page_config(page_title="Support Ticket Insight Lab", layout="wide")
    st.title("Support Ticket Insight Lab")
    st.caption("Analise tickets de infraestrutura a partir de um CSV enviado pelo usuario.")

    st.subheader("Enviar CSV")
    st.write(
        "Envie um arquivo CSV com as colunas obrigatorias abaixo. "
        "A aplicacao nao usa dados de demonstracao nem registros mockados."
    )
    st.code(", ".join(REQUIRED_COLUMNS), language="text")

    with st.expander("Colunas recomendadas"):
        st.write(", ".join(RECOMMENDED_COLUMNS))

    st.subheader("Provedor de IA")
    selected_provider = st.selectbox(
        "Provedor de IA",
        options=SUPPORTED_PROVIDERS,
        format_func=lambda provider: PROVIDER_METADATA[provider].label,
    )
    provider_metadata = PROVIDER_METADATA[selected_provider]
    session_key_name = f"{selected_provider}_api_key"
    env_resolution = resolve_provider_api_key(selected_provider)

    session_api_key = None
    if env_resolution.is_available:
        st.success("Chave encontrada nas variaveis de ambiente para este provedor.")
    else:
        st.info("Informe a chave API para continuar. Ela sera usada somente nesta sessao.")
        session_api_key = st.text_input(
            "Chave API",
            type="password",
            key=session_key_name,
            help=f"Configure {provider_metadata.env_var} para evitar digitar a chave manualmente.",
        )

    key_resolution = resolve_provider_api_key(selected_provider, session_api_key=session_api_key)

    use_mock = st.checkbox("Usar dados mockados para teste")

    uploaded_file = st.file_uploader("Arquivo CSV de tickets", type=["csv"], disabled=use_mock)

    if use_mock:
        try:
            dataframe = load_csv(ROOT / "support_tickets_mock.csv")
        except FileNotFoundError:
            st.error("Arquivo de mock não encontrado.")
            return
    elif uploaded_file is not None:
        try:
            dataframe = load_csv(uploaded_file)
        except pd.errors.ParserError as exc:
            st.error(f"Nao foi possivel ler o CSV: {exc}")
            return
    else:
        st.info("Envie um CSV ou marque a opção de dados mockados para iniciar a validacao.")
        return

    result = validate_tickets(dataframe)
    if not result.is_valid:
        st.error("O CSV contem erros de validacao.")
        st.dataframe(pd.DataFrame({"erro": result.errors}), use_container_width=True)
        return

    st.success("CSV validado com sucesso.")

    df = result.dataframe.copy()
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

    categorical_filters = {}
    for col in categorical_columns:
        if col in df.columns and not df[col].dropna().empty:
            unique_values = df[col].dropna().unique().tolist()
            try:
                unique_values.sort()
            except TypeError:
                pass
            
            label = col.replace("_", " ").title()
            selected = st.sidebar.multiselect(label, options=unique_values, default=[])
            categorical_filters[col] = selected

    filtered_df = filter_tickets(
        df, 
        date_range=date_range, 
        categorical_filters=categorical_filters
    )

    # Exibir KPIs
    st.subheader("Indicadores Principais")
    kpis = get_kpis(filtered_df)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total de Tickets", kpis["total"])
    col2.metric("Abertos", kpis["open"])
    col3.metric("Fechados", kpis["closed"])
    col4.metric("Prioridade Alta/Crítica", kpis["high_priority"])
    col5.metric("Idade Média (dias)", kpis["avg_age_days"])
    col6.metric("Tempo Médio de Resolução", kpis["avg_resolution_days"])

    st.subheader("Dados")
    st.dataframe(filtered_df, use_container_width=True)

    if st.button("Processar tickets"):
        if not key_resolution.is_available:
            st.error(
                "Nao foi possivel processar: informe uma chave API ou configure a "
                "variavel de ambiente do provedor selecionado."
            )
            return

        st.warning(
            "A chave API foi resolvida, mas a chamada ao provedor de IA ainda nao foi "
            "implementada. Nenhuma analise mockada foi gerada."
        )


if __name__ == "__main__":
    main()
