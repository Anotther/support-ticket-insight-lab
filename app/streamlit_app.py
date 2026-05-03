from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ticket_insight.loader import load_csv  # noqa: E402
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

    uploaded_file = st.file_uploader("Arquivo CSV de tickets", type=["csv"])
    if uploaded_file is None:
        st.info("Envie um CSV para iniciar a validacao.")
        return

    try:
        dataframe = load_csv(uploaded_file)
    except pd.errors.ParserError as exc:
        st.error(f"Nao foi possivel ler o CSV: {exc}")
        return

    result = validate_tickets(dataframe)
    if not result.is_valid:
        st.error("O CSV contem erros de validacao.")
        st.dataframe(pd.DataFrame({"erro": result.errors}), use_container_width=True)
        return

    st.success("CSV validado com sucesso.")
    st.dataframe(result.dataframe, use_container_width=True)


if __name__ == "__main__":
    main()
