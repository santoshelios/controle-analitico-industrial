import streamlit as st
import pandas as pd


# =========================================================
# AUDITORIA
# =========================================================

def show_audit():

    st.title("📜 Auditoria do Sistema")

    st.markdown("""
    Rastreabilidade completa de ações críticas do sistema.
    """)

    st.divider()

    # =====================================================
    # SESSION
    # =====================================================

    if "audit_logs" not in st.session_state:

        st.session_state.audit_logs = []

    logs = st.session_state.audit_logs

    # =====================================================
    # KPIs
    # =====================================================

    total_logs = len(logs)

    total_logins = len([

        l for l in logs

        if l.get("acao") == "LOGIN"
    ])

    total_exclusoes = len([

        l for l in logs

        if "EXCLUI" in l.get("acao", "")
    ])

    total_edicoes = len([

        l for l in logs

        if "EDIT" in l.get("acao", "")
    ])

    usuarios_unicos = len(set([

        l.get("usuario", "N/A")

        for l in logs
    ]))

    # =====================================================
    # KPI STYLE
    # =====================================================

    st.markdown("""

    <style>

    .custom-kpi {

        background:
            linear-gradient(
                135deg,
                rgba(37,99,235,0.92),
                rgba(15,23,42,0.96)
            );

        border:
            1px solid rgba(96,165,250,0.35);

        border-radius: 22px;

        padding: 24px;

        min-height: 180px;

        box-shadow:
            0 18px 50px rgba(37,99,235,0.25);

        position: relative;

        overflow: hidden;

        transition:
            all 0.25s ease;
    }

    .custom-kpi:hover {

        transform:
            translateY(-4px);

        box-shadow:
            0 24px 60px rgba(59,130,246,0.40);
    }

    .custom-kpi::before {

        content: "";

        position: absolute;

        top: 0;
        left: 0;

        width: 100%;
        height: 5px;

        background:
            linear-gradient(
                90deg,
                rgba(59,130,246,0),
                rgba(255,255,255,1),
                rgba(59,130,246,0)
            );
    }

    </style>

    """, unsafe_allow_html=True)

    # =====================================================
    # KPIs
    # =====================================================

    st.subheader("📈 Indicadores de Auditoria")

    col1, col2, col3, col4, col5 = st.columns(5)

    indicadores = [

        ("📜 Logs", total_logs, "Eventos registrados"),

        ("🔐 Logins", total_logins, "Acessos realizados"),

        ("🗑️ Exclusões", total_exclusoes, "Eventos críticos"),

        ("✏️ Edições", total_edicoes, "Alterações registradas"),

        ("👥 Usuários", usuarios_unicos, "Usuários distintos")
    ]

    colunas = [col1, col2, col3, col4, col5]

    for coluna, indicador in zip(colunas, indicadores):

        titulo, valor, descricao = indicador

        card_html = f"""
<div class="custom-kpi">

<h4 style="
margin:0;
margin-bottom:24px;
font-size:15px;
font-weight:800;
color:white;
text-transform:uppercase;
letter-spacing:0.5px;
">
{titulo}
</h4>

<h1 style="
margin:0;
margin-bottom:18px;
font-size:54px;
font-weight:900;
color:white;
line-height:1;
text-shadow:0 0 28px rgba(255,255,255,0.25);
">
{valor}
</h1>

<p style="
margin:0;
font-size:14px;
color:rgba(255,255,255,0.86);
line-height:1.5;
">
{descricao}
</p>

</div>
"""

        with coluna:

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )

    st.divider()

    # =====================================================
    # TABELA
    # =====================================================

    st.subheader("🕒 Eventos do Sistema")

    if logs:

        df = pd.DataFrame(logs)

        df = df.iloc[::-1]

        html_table = """

<style>

.audit-table {

    width: 100%;

    border-collapse: collapse;

    background-color: #0F172A;

    color: white;

    font-size: 14px;

    border-radius: 12px;

    overflow: hidden;
}

.audit-table thead {

    background-color: #1E293B;
}

.audit-table th {

    padding: 14px;

    text-align: left;

    font-weight: 600;

    color: #E2E8F0;
}

.audit-table td {

    padding: 12px;

    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.audit-table tbody tr:hover {

    background-color: rgba(255,255,255,0.03);
}

</style>

<table class="audit-table">

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

    else:

        st.info(
            "Nenhum log de auditoria encontrado."
        )