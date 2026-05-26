import streamlit as st
import pandas as pd


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

    if not coletas:

        st.warning(
            "Nenhuma coleta registrada."
        )

        return

    linhas = []

    for coleta in reversed(coletas):

        resultados = coleta["resultados"]

        for parametro, info in resultados.items():

            status_visual = (

                "🟡 Alerta"

                if info["status"] == "Alerta"

                else "🟢 Conforme"
            )

            linhas.append({

                "Data": coleta["data_coleta"],

                "Hora": coleta["hora_coleta"],

                "Ponto": coleta["ponto"],

                "Parâmetro": parametro,

                "Resultado": info["valor"],

                "Limites": f"{info['limite_min']} / {info['limite_max']}",

                "Desvio": info["desvio"],

                "Operador": coleta["operador"],

                "Status": status_visual
            })

    df = pd.DataFrame(linhas)

    st.subheader("📋 Rastreabilidade Operacional")

    html_table = """

<style>

.history-table {

    width: 100%;

    border-collapse: collapse;

    background-color: #0F172A;

    color: white;

    font-size: 13px;

    border-radius: 12px;

    overflow: hidden;
}

.history-table thead {

    background-color: #1E293B;
}

.history-table th {

    padding: 14px;

    text-align: left;

    font-weight: 600;

    color: #E2E8F0;
}

.history-table td {

    padding: 10px;

    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.history-table tbody tr:hover {

    background-color: rgba(255,255,255,0.03);
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