import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter

import json

from db_connection import get_safe_connection



from services.analytics_service import (

    total_coletas,

    total_alertas,

    total_conformes,

    taxa_conformidade,

    total_pontos,

    total_parametros,

    ultimas_coletas,

    score_operacional
)



# =========================================================
# DASHBOARD PAGE
# =========================================================

def show_dashboard():

    st.title("📊 Dashboard Operacional")

    st.markdown("""
    Monitoramento analítico industrial em tempo real.
    """)

    st.divider()

    # =====================================================
    # SESSION STATE
    # =====================================================

    # =====================================================
    # POSTGRESQL
    # =====================================================

    conn = get_safe_connection()

    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT

            data_coleta,
            hora_coleta,
            ponto,
            operador,
            status,
            resultados,
            planta,
            setor

        FROM collections

        ORDER BY data_coleta DESC

        """

    )

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

            "setor": row[7]
        })

    # =====================================================
    # KPIs OPERACIONAIS
    # =====================================================

    total_parametros_analisados = 0

    total_conformes = 0

    total_preditivos = 0

    total_criticos = 0

    pontos_monitorados = set()

    parametros_monitorados = set()

    for coleta in coletas:

        pontos_monitorados.add(
            coleta["ponto"]
        )

        resultados = coleta["resultados"]

        # =============================================
        # JSONB
        # =============================================

        if isinstance(resultados, str):

            resultados = json.loads(
                resultados
            )

        for parametro, resultado in resultados.items():

            total_parametros_analisados += 1

            parametros_monitorados.add(
                parametro
            )

            status = resultado.get(
                "status",
                "Conforme"
            )

            if status == "Conforme":

                total_conformes += 1

            elif status == "Preditivo":

                total_preditivos += 1

            elif status == "Crítico":

                total_criticos += 1

    # =====================================================
    # KPIs
    # =====================================================

    kpi_total_coletas = len(coletas)

    kpi_total_alertas = (

        total_preditivos
        +
        total_criticos
    )

    kpi_total_conformes = total_conformes

    kpi_total_pontos = len(
        pontos_monitorados
    )

    kpi_total_parametros = len(
        parametros_monitorados
    )

    # =====================================================
    # CONFORMIDADE
    # =====================================================

    if total_parametros_analisados > 0:

        kpi_taxa_conformidade = round(

            (
                total_conformes
                /
                total_parametros_analisados
            ) * 100,

            1
        )

    else:

        kpi_taxa_conformidade = 0

    # =====================================================
    # SCORE OPERACIONAL
    # =====================================================

    if kpi_taxa_conformidade >= 95:

        kpi_score = "Excelente"

    elif kpi_taxa_conformidade >= 80:

        kpi_score = "Bom"

    elif kpi_taxa_conformidade >= 60:

        kpi_score = "Moderado"

    else:

        kpi_score = "Crítico"




# =====================================================
# KPI STYLE - ISA INDUSTRIAL
# =====================================================

st.markdown("""

<style>

.custom-kpi {

    background:
        #252526;

    border:
        1px solid #3A3A3A;

    border-radius:
        12px;

    padding:
        24px;

    min-height:
        180px;

    box-shadow:
        none;

    position:
        relative;

    overflow:
        hidden;

    transition:
        all 0.2s ease;
}

/* REMOVE GLOW */

.custom-kpi::before {

    display:
        none;
}

/* HOVER */

.custom-kpi:hover {

    background:
        #2D2D30;

    border:
        1px solid #5A5A5A;

    transform:
        translateY(-2px);
}

/* KPI TITLE */

.custom-kpi h4 {

    margin:
        0;

    margin-bottom:
        26px;

    font-size:
        13px;

    font-weight:
        700;

    color:
        #A0A0A0;

    text-transform:
        uppercase;

    letter-spacing:
        0.6px;
}

/* KPI VALUE */

.custom-kpi h1 {

    margin:
        0;

    margin-bottom:
        18px;

    font-size:
        52px;

    font-weight:
        800;

    color:
        #F2F2F2;

    line-height:
        1;

    text-shadow:
        none;
}

/* KPI DESCRIPTION */

.custom-kpi p {

    margin:
        0;

    font-size:
        13px;

    color:
        #BFBFBF;

    line-height:
        1.5;
}

</style>

""", unsafe_allow_html=True)

    # =====================================================
    # INDICADORES
    # =====================================================

    st.subheader("📈 Indicadores Operacionais")

    col1, col2, col3, col4, col5 = st.columns(5)

    indicadores = [

        ("📊 Coletas", kpi_total_coletas, "Registros operacionais"),

        ("✅ Conformes", kpi_total_conformes, "Dentro dos limites"),

        ("🚨 Alertas", kpi_total_alertas, "Ocorrências monitoradas"),

        ("📈 Conformidade", f"{kpi_taxa_conformidade}%", "Taxa operacional"),

        ("🏭 Score", kpi_score, "Saúde operacional")
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
    # PAINÉIS
    # =====================================================

    col1, col2 = st.columns([2, 1])

    # =====================================================
    # OPERAÇÃO
    # =====================================================

    with col1:

        with st.container(border=True):

            st.subheader("🏭 Operação Industrial")

            if kpi_total_alertas > 0:

                st.warning(

                    f"⚠️ {kpi_total_alertas} ocorrência(s) fora da conformidade."
                )

            else:

                st.success(

                    "✅ Sistema operando dentro da conformidade."
                )

            st.markdown(f"""

### Status operacional

- ✅ Sistema operacional ativo
- ✅ Monitoramento contínuo
- ✅ Analytics online
- ✅ {kpi_total_pontos} pontos monitorados
- ✅ {kpi_total_parametros} parâmetros ativos

""")

    # =====================================================
    # STATUS AMBIENTE
    # =====================================================

    with col2:

        with st.container(border=True):

            st.subheader("🟢 Status Ambiente")

            st.markdown(f"""

### Infraestrutura

🟢 API Online

🟢 Segurança Ativa

🟢 Analytics Online

🟢 Sistema Estável

### Operação

📈 Score: {kpi_score}

📊 Conformidade: {kpi_taxa_conformidade}%
""")

    st.divider()

    # =====================================================
    # CENTRAL INTELIGENTE DE ALERTAS
    # =====================================================

    st.subheader("🚨 Central Inteligente de Alertas")

    alertas = []

    for coleta in coletas:

        resultados = coleta["resultados"]

        # =============================================
        # JSONB
        # =============================================

        if isinstance(resultados, str):

            resultados = json.loads(
                resultados
            )

        for parametro, resultado in resultados.items():

            status = resultado.get(
                "status",
                "Conforme"
            )

            valor = resultado.get(
                "valor",
                "-"
            )

            # =========================================
            # CRÍTICO
            # =========================================

            if status == "Crítico":

                alertas.append({

                    "tipo": "🔴 ALERTA CRÍTICO",

                    "mensagem":
                    f"{parametro} fora da faixa operacional. Valor atual: {valor}"
                })

            # =========================================
            # PREDITIVO
            # =========================================

            elif status == "Preditivo":

                alertas.append({

                    "tipo": "🟡 ALERTA PREDITIVO",

                    "mensagem":
                    f"{parametro} próximo do limite operacional. Valor atual: {valor}"
                })

    # =====================================================
    # EXIBIÇÃO
    # =====================================================

    if alertas:

        for alerta in alertas[:5]:

            tipo = alerta["tipo"]

            mensagem = alerta["mensagem"]

            if "CRÍTICO" in tipo:

                st.error(
                    f"{tipo} — {mensagem}"
                )

            else:

                st.warning(
                    f"{tipo} — {mensagem}"
                )

    else:

        st.success(
            "✅ Nenhum alerta inteligente ativo."
        )

    st.divider()

    # =====================================================
    # TENDÊNCIA
    # =====================================================

    st.subheader("📈 Tendência Operacional")

    if coletas:

        contador = Counter()

        for coleta in coletas:

            data = coleta["data_coleta"]

            contador[data] += 1

        dias = list(contador.keys())

        volumes = list(contador.values())

    else:

        dias = ["Sem Dados"]

        volumes = [0]

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=dias,

            y=volumes,

            mode="lines+markers",

            line=dict(

                color="#3B82F6",

                width=4
            ),

            marker=dict(

                size=10,

                color="#60A5FA"
            ),

            fill="tozeroy",

            fillcolor="rgba(59,130,246,0.10)"
        )
    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(

            color="white",

            family="Inter"
        ),

        margin=dict(

            l=10,

            r=10,

            t=20,

            b=10
        ),

        height=380,

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(

            showgrid=True,

            gridcolor="rgba(255,255,255,0.05)"
        )
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )

    st.divider()

     # =====================================================
    # ATIVIDADE RECENTE
    # =====================================================

    st.subheader("🕒 Atividade Recente")

    atividade = []

    for coleta in coletas:

        resultados = coleta["resultados"]

        # =============================================
        # JSONB
        # =============================================

        if isinstance(resultados, str):

            resultados = json.loads(
                resultados
            )

        for parametro, resultado in resultados.items():

            status = resultado.get(

                "status",

                "Conforme"
            )

            if status == "Crítico":

                status_formatado = "🔴 Crítico"

            elif status == "Preditivo":

                status_formatado = "🟡 Preditivo"

            else:

                status_formatado = "🟢 Conforme"

            atividade.append({

                "Data": coleta["data_coleta"],

                "Hora": coleta["hora_coleta"],

                "Ponto": coleta["ponto"],

                "Parâmetro": parametro,

                "Valor": resultado.get(
                    "valor",
                    "-"
                ),
                "Desvio": resultado.get(
                 "desvio",
                    "-"
                ),
               

                "Status": status_formatado,

                "Criticidade": resultado.get(
                    "criticidade",
                    "-"
                ),

                "Operador": coleta["operador"]
            })

    if atividade:

        df = pd.DataFrame(atividade)

        # =============================================
        # MAIS RECENTES PRIMEIRO
        # =============================================

        df = df.sort_values(

            by=["Data", "Hora"],

            ascending=False
        )

        # =============================================
        # LIMITA EXIBIÇÃO
        # =============================================

        df = df.head(20)

        html_table = """

<style>

.dashboard-table {

    width: 100%;
    border-collapse: collapse;
    background-color: #0F172A;
    color: white;
    font-size: 14px;
    border-radius: 12px;
    overflow: hidden;
}

.dashboard-table thead {

    background-color: #1E293B;
}

.dashboard-table th {

    padding: 14px;
    text-align: left;
    font-weight: 600;
    color: #E2E8F0;
}

.dashboard-table td {

    padding: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.dashboard-table tbody tr:hover {

    background-color: rgba(255,255,255,0.03);
}

</style>

<table class="dashboard-table">

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
            "Nenhuma coleta registrada."
        )