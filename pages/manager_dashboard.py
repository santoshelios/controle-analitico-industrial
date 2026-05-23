import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from services.analytics_service import (

    ranking_parametros_criticos,

    ranking_pontos_criticos,

    tendencia_alertas,

    taxa_conformidade,

    total_alertas as calcular_total_alertas,

    total_coletas,

    score_operacional
)


# =========================================================
# DASHBOARD GERENCIAL
# =========================================================

def show_manager_dashboard():

    st.title("📈 Dashboard Gerencial")

    st.markdown("""
    Inteligência operacional corporativa e análise executiva.
    """)

    st.divider()

    # =====================================================
    # STYLE
    # =====================================================

    st.markdown("""

    <style>

    .premium-table {

        width: 100%;
        border-collapse: collapse;
        background: rgba(15,23,42,0.96);
        border-radius: 18px;
        overflow: hidden;
        color: white;
        font-size: 14px;
    }

    .premium-table thead {

        background:
            linear-gradient(
                90deg,
                rgba(30,41,59,1),
                rgba(51,65,85,1)
            );
    }

    .premium-table th {

        padding: 14px;
        text-align: left;
        font-weight: 700;
        color: rgba(255,255,255,0.92);
        border-bottom:
            1px solid rgba(255,255,255,0.06);
    }

    .premium-table td {

        padding: 14px;

        border-bottom:
            1px solid rgba(255,255,255,0.04);

        color:
            rgba(255,255,255,0.88);
    }

    .premium-table tbody tr {

        background:
            rgba(15,23,42,0.75);

        transition:
            all 0.2s ease;
    }

    .premium-table tbody tr:nth-child(even) {

        background:
            rgba(30,41,59,0.65);
    }

    .premium-table tbody tr:hover {

        background:
            rgba(37,99,235,0.25);
    }

    </style>

    """, unsafe_allow_html=True)

    # =====================================================
    # KPIs EXECUTIVOS
    # =====================================================

    conformidade = taxa_conformidade()

    qtd_alertas = calcular_total_alertas()

    coletas = total_coletas()

    score = score_operacional()

    st.subheader("📊 Indicadores Executivos")

    col1, col2, col3, col4 = st.columns(4)

    indicadores = [

        ("📈 CONFORMIDADE", f"{conformidade}%", "Eficiência operacional"),

        ("🚨 ALERTAS", qtd_alertas, "Ocorrências críticas"),

        ("🧪 COLETAS", coletas, "Volume operacional"),

        ("🏭 SCORE", score, "Saúde da planta")
    ]

    colunas = [col1, col2, col3, col4]

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
    # RANKINGS
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # PARÂMETROS CRÍTICOS
    # =====================================================

    with col1:

        st.subheader("🚨 Parâmetros Críticos")

        ranking_parametros = ranking_parametros_criticos()

        if ranking_parametros:

            df_parametros = pd.DataFrame(

                ranking_parametros,

                columns=[

                    "Parâmetro",

                    "Alertas"
                ]
            )

            html_table = """

<table class="premium-table">

<thead>

<tr>

<th>Parâmetro</th>
<th>Alertas</th>

</tr>

</thead>

<tbody>
"""

            for _, row in df_parametros.iterrows():

                html_table += f"""

<tr>

<td>{row["Parâmetro"]}</td>
<td>{row["Alertas"]}</td>

</tr>
"""

            html_table += """

</tbody>

</table>
"""

            st.markdown(

                html_table,

                unsafe_allow_html=True
            )

        else:

            st.info(
                "Nenhum parâmetro crítico no período."
            )

    # =====================================================
    # PONTOS CRÍTICOS
    # =====================================================

    with col2:

        st.subheader("🏭 Pontos Críticos")

        ranking_pontos = ranking_pontos_criticos()

        if ranking_pontos:

            df_pontos = pd.DataFrame(

                ranking_pontos,

                columns=[

                    "Ponto",

                    "Alertas"
                ]
            )

            html_table = """

<table class="premium-table">

<thead>

<tr>

<th>Ponto</th>
<th>Alertas</th>

</tr>

</thead>

<tbody>
"""

            for _, row in df_pontos.iterrows():

                html_table += f"""

<tr>

<td>{row["Ponto"]}</td>
<td>{row["Alertas"]}</td>

</tr>
"""

            html_table += """

</tbody>

</table>
"""

            st.markdown(

                html_table,

                unsafe_allow_html=True
            )

        else:

            st.info(
                "Nenhum ponto crítico no período."
            )

    st.divider()

    # =====================================================
    # TENDÊNCIA EXECUTIVA
    # =====================================================

    st.subheader("📈 Tendência Executiva")

    tendencia = tendencia_alertas()

    if tendencia:

        datas = [

            item[0]

            for item in tendencia
        ]

        valores = [

            item[1]

            for item in tendencia
        ]

        fig = go.Figure()

        fig.add_trace(

            go.Scatter(

                x=datas,

                y=valores,

                mode="lines+markers",

                line=dict(

                    color="#EF4444",

                    width=4
                ),

                marker=dict(

                    size=10,

                    color="#F87171"
                ),

                fill="tozeroy",

                fillcolor="rgba(239,68,68,0.12)"
            )
        )

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(

                color="white",

                family="Inter"
            ),

            height=420,

            margin=dict(

                l=10,

                r=10,

                t=20,

                b=10
            ),

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

    else:

        st.info(
            "Sem dados suficientes para tendência."
        )

    st.divider()

        # =====================================================
    # IA OPERACIONAL V1
    # =====================================================

    st.subheader("🧠 Inteligência Operacional")

    pontos = st.session_state.get(
        "collection_points",
        []
    )

    coletas = st.session_state.get(
        "coletas",
        []
    )

    if pontos:

        cols = st.columns(2)

        for idx, ponto in enumerate(pontos):

            with cols[idx % 2]:

                nome_ponto = ponto.get(
                    "nome",
                    "Ponto"
                )

                coletas_ponto = [

                    c for c in coletas

                    if c.get("ponto") == nome_ponto
                ]

                qtd_alertas = 0

                score_card = 100

                tendencia_card = "Estável"

                status = "🟢 Saudável"

                cor = "#22C55E"

                # =================================================
                # SCORE INTELIGENTE
                # =================================================

                if len(coletas_ponto) > 0:

                    qtd_alertas = sum(

                        1 for c in coletas_ponto

                        if c.get("status") in [
                            "Preditivo",
                            "Moderado",
                            "Crítico"
                        ]
                    )

                    score_card = max(
                        0,
                        100 - (qtd_alertas * 8)
                    )

                    if score_card < 70:

                        status = "🔴 Crítico"

                        cor = "#EF4444"

                        tendencia_card = "Degradação"

                    elif score_card < 85:

                        status = "🟡 Atenção"

                        cor = "#F59E0B"

                        tendencia_card = "Oscilando"

                # =================================================
                # MINI GRÁFICO
                # =================================================

                valores = []

                datas = []

                for coleta in coletas_ponto[-10:]:

                    valor = coleta.get(
                        "valor",
                        0
                    )

                    try:

                        valores.append(
                            float(valor)
                        )

                    except:

                        valores.append(0)

                    datas.append(
                        coleta.get(
                            "data",
                            "Coleta"
                        )
                    )

                fill_color = "rgba(34,197,94,0.15)"

                if cor == "#EF4444":

                    fill_color = "rgba(239,68,68,0.15)"

                elif cor == "#F59E0B":

                    fill_color = "rgba(245,158,11,0.15)"

                fig_card = go.Figure()

                fig_card.add_trace(

                    go.Scatter(

                        x=datas,

                        y=valores,

                        mode="lines+markers",

                        line=dict(

                            color=cor,

                            width=3
                        ),

                        marker=dict(
                            size=6
                        ),

                        fill="tozeroy",

                        fillcolor=fill_color
                    )
                )

                fig_card.update_layout(

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    height=180,

                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10
                    ),

                    xaxis=dict(
                        visible=False
                    ),

                    yaxis=dict(
                        visible=False
                    ),

                    showlegend=False
                )

                # =================================================
                # CARD IA
                # =================================================



                # =================================================
                # IA OPERACIONAL
                # =================================================

            card_html = f"""
                <div style='
                background: linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.98));
                border: 1px solid rgba(255,255,255,0.06);
                border-left: 5px solid {cor};
                border-radius: 24px;
                padding: 24px;
                margin-bottom: 16px;
                box-shadow: 0 18px 40px rgba(0,0,0,0.35);
                '>

                <h3 style='
                margin:0;
                margin-bottom:12px;
                color:white;
                font-size:26px;
                font-weight:800;
                '>
                🏭 {nome_ponto}
                </h3>

                <p style='
                margin:0;
                margin-bottom:18px;
                color:{cor};
                font-size:15px;
                font-weight:700;
                '>
                {status}
                </p>

                <div style='
                display:flex;
                gap:40px;
                margin-bottom:18px;
                '>

                <div>

                <p style='
                margin:0;
                font-size:12px;
                color:rgba(255,255,255,0.60);
                '>
                SCORE
                </p>

                <h2 style='
                margin:0;
                color:white;
                font-size:38px;
                font-weight:900;
                '>
                {score_card}
                </h2>

                </div>

                <div>

                <p style='
                margin:0;
                font-size:12px;
                color:rgba(255,255,255,0.60);
                '>
                ALERTAS
                </p>

                <h2 style='
                margin:0;
                color:white;
                font-size:38px;
                font-weight:900;
                '>
                {qtd_alertas}
                </h2>

                </div>

                </div>

                <p style='
                margin-top:12px;
                margin-bottom:18px;
                color:rgba(255,255,255,0.78);
                font-size:14px;
                line-height:1.7;
                '>

                🧠 Tendência operacional:
                <strong>{tendencia_card}</strong>

                </p>

                </div>
                """

        st.markdown(
                card_html,
                unsafe_allow_html=True
                 )