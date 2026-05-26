
# =========================================================
# HISTORY PAGE
# =========================================================

def show_history():

    st.title("📚 Histórico Analítico")

    st.markdown("""
    Central operacional de rastreabilidade e auditoria analítica.
    """)

    st.divider()

from db_connection import get_safe_connection

import streamlit as st
import pandas as pd
import json

from db_connection import get_safe_connection


# =========================================================
# HISTORY PAGE
# =========================================================

def show_history():

    st.title("📚 Histórico Analítico")

    st.markdown("""
    Central operacional de rastreabilidade e auditoria analítica.
    """)

    st.divider()

    # =====================================================
    # POSTGRESQL
    # =====================================================

    conn = get_safe_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        data_coleta,
        hora_coleta,
        ponto,
        operador,
        status,
        resultados,
        planta,
        setor,
        observacoes

    FROM collections

    ORDER BY data_coleta DESC,
    hora_coleta DESC

    """)

    rows = cursor.fetchall()

    cursor.close()

    coletas = []

    for row in rows:

        coletas.append({

            "data_coleta": str(row[0]),
            "hora_coleta": str(row[1]),
            "ponto": row[2],
            "operador": row[3],
            "status": row[4],
            "resultados": row[5],
            "planta": row[6],
            "setor": row[7],
            "observacoes": row[8]
        })

    # =====================================================
    # SEM DADOS
    # =====================================================

    if not coletas:

        st.warning(
            "Nenhuma coleta registrada."
        )

        return

    # =====================================================
    # LINHAS
    # =====================================================

    linhas = []

    for coleta in reversed(coletas):

        resultados = coleta["resultados"]

        # =============================================
        # JSONB
        # =============================================

        if isinstance(resultados, str):

            resultados = json.loads(
                resultados
            )

        for parametro, info in resultados.items():

            status = info.get(
                "status",
                "Conforme"
            )

            # =========================================
            # STATUS VISUAL
            # =========================================

            if status == "Crítico":

                status_visual = "🔴 Crítico"

            elif status == "Preditivo":

                status_visual = "🟡 Preditivo"

            else:

                status_visual = "🟢 Conforme"

            linhas.append({

                "Data": coleta["data_coleta"],

                "Hora": coleta["hora_coleta"],

                "Ponto": coleta["ponto"],

                "Parâmetro": parametro,

                "Resultado": info.get(
                    "valor",
                    "-"
                ),

                "Desvio": info.get(
                    "desvio",
                    "-"
                ),

                "Operador": coleta["operador"],

                "Status": status_visual
            })

    # =====================================================
    # DATAFRAME
    # =====================================================

    df = pd.DataFrame(linhas)

    st.subheader("📋 Rastreabilidade Operacional")

    # =====================================================
    # TABLE ISA
    # =====================================================

    html_table = """

<style>

.history-table {

    width: 100%;

    border-collapse: collapse;

    background-color: #252526;

    color: #D9D9D9;

    font-size: 13px;

    border-radius: 12px;

    overflow: hidden;
}

.history-table thead {

    background-color: #2D2D30;
}

.history-table th {

    padding: 14px;

    text-align: left;

    font-weight: 700;

    color: #F2F2F2;
}

.history-table td {

    padding: 10px;

    border-bottom: 1px solid #3A3A3A;
}

.history-table tbody tr:hover {

    background-color: #2D2D30;
}

</style>

<table class="history-table">

<thead>

<tr>

"""

    for coluna in df.columns:

        html_table += f"<th>{coluna}</th>"

    html_table += "</tr></thead><tbody>"

    for _, row in df.iterrows():

        html_table += "<tr>"

        for valor in row:

            html_table += f"<td>{valor}</td>"

        html_table += "</tr>"

    html_table += "</tbody></table>"

    st.markdown(

        html_table,

        unsafe_allow_html=True
    )